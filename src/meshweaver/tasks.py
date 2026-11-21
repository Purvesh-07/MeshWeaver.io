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

    def can_accept(self):

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

    def __init__(self, gossip):

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

        return candidates[0]

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