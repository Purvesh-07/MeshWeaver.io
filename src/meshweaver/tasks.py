import cloudpickle

from dataclasses import dataclass


TASK_OFFER = "TASK_OFFER"
TASK_ACCEPT = "TASK_ACCEPT"
TASK_REJECT = "TASK_REJECT"


class RemoteTaskError(Exception):
    pass


def serialize_task(
    func,
    args,
    kwargs,
):
    return cloudpickle.dumps(
        (
            func,
            args,
            kwargs,
        )
    )


def deserialize_task(
    payload,
):
    return cloudpickle.loads(
        payload
    )


def execute_payload(
    payload,
):
    try:

        func, args, kwargs = deserialize_task(
            payload
        )

        return func(
            *args,
            **kwargs,
        )

    except Exception as exc:

        raise RemoteTaskError(
            f"{type(exc).__name__}: {exc}"
        )


class WorkerState:

    def __init__(self):

        self.inflight = 0

        self.max_tasks = 4

    def can_accept(
        self,
    ):
        return (
            self.inflight
            < self.max_tasks
        )


@dataclass
class TaskRecord:

    task_id: str

    assignee: str

    state: str

    attempt: int = 1


class TaskRouter:

    def __init__(
        self,
        gossip,
    ):
        self.gossip = gossip

        self.tasks = {}

    def choose_worker(
        self,
        excluded=None,
    ):
        if excluded is None:
            excluded = set()

        candidates = self.gossip.ranked(
            excluded,
            {},
        )

        if not candidates:
            raise RuntimeError(
                "No workers available"
            )

        return candidates[0]

    def choose_with_retry(
        self,
        tracker,
    ):
        excluded = set()

        while True:

            worker = self.choose_worker(
                excluded
            )

            if not tracker.is_dead(
                worker
            ):
                return worker

            excluded.add(
                worker
            )

    def offer_task(
        self,
        worker_state,
    ):
        if worker_state.can_accept():

            worker_state.inflight += 1

            return TASK_ACCEPT

        return TASK_REJECT

    def complete_task(
        self,
        worker_state,
    ):
        worker_state.inflight -= 1

        if worker_state.inflight < 0:

            worker_state.inflight = 0


class FailureTracker:

    def __init__(
        self,
    ):
        self.dead_workers = set()

    def mark_dead(
        self,
        worker,
    ):
        self.dead_workers.add(
            worker
        )

    def is_dead(
        self,
        worker,
    ):
        return worker in self.dead_workers


def execute_on_worker(
    worker,
    task,
):
    if worker in {
        "worker-b",
        "worker-c",
    }:
        raise ConnectionError(
            "worker disappeared"
        )

    return task()


def run_with_failover(
    router,
    tracker,
    task,
):

    record = TaskRecord(
        task_id="demo-task",
        assignee="",
        state="RUNNING",
    )

    while True:

        worker = router.choose_with_retry(
            tracker
        )

        record.assignee = worker

        try:

            result = execute_on_worker(
                worker,
                task,
            )

            record.state = "COMPLETE"

            return result

        except ConnectionError:

            tracker.mark_dead(
                worker
            )

            record.attempt += 1

            record.state = (
                "REASSIGNED"
            )