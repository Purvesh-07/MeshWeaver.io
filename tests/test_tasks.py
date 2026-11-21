from meshweaver.tasks import (
    WorkerState,
    TaskRouter,
    TASK_ACCEPT,
)

from meshweaver.tasks import (
    WorkerState,
    TaskRouter,
    TASK_REJECT,
)

def test_accept():

    state = WorkerState()

    router = TaskRouter(None)

    assert (
        router.offer_task(
            state
        )
        == TASK_ACCEPT
    )
def test_reject():

    state = WorkerState()

    state.max_tasks = 1
    state.inflight = 1

    router = TaskRouter(None)

    assert (
        router.offer_task(
            state
        )
        == TASK_REJECT
    )
    