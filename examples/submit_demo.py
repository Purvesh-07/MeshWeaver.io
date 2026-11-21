from meshweaver.tasks import (
    WorkerState,
    TaskRouter,
)

class FakeGossip:

    def ranked(
        self,
        excluded,
        inflight,
    ):
        return [
            "worker-a",
            "worker-b",
        ]

router = TaskRouter(
    FakeGossip()
)

worker = router.choose_worker()

print(
    "selected:",
    worker,
)

results = []

for i in range(12):  

    results.append(
       i * i
)

print(
    f"got {len(results)} results"
)