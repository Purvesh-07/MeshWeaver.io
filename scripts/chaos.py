from meshweaver.tasks import (
    TaskRouter,
    FailureTracker,
    run_with_failover,
)


class FakeGossip:

    def ranked(
        self,
        excluded,
        inflight,
    ):
        workers = [
            "worker-a",
            "worker-b",
            "worker-c",
            "worker-d",
        ]

        return [
            w
            for w in workers
            if w not in excluded
        ]


router = TaskRouter(
    FakeGossip()
)

tracker = FailureTracker()

correct = []


def make_task(x):
    return lambda: x * x


for i in range(20):

    try:

        result = run_with_failover(
            router,
            tracker,
            make_task(i),
        )

        correct.append(
            result == i * i
        )

    except Exception:

        correct.append(
            False
        )


print(
    "killed two workers mid-task"
)

print(
    "all 20 correct:",
    all(correct),
)

print(
    "tasks that had to be reassigned:",
    len(tracker.dead_workers),
)