from meshweaver.tasks import (
    FailureTracker,
    TaskRouter,
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


def test_retry_selection():

    tracker = FailureTracker()

    tracker.mark_dead(
        "worker-a"
    )

    router = TaskRouter(
        FakeGossip()
    )

    worker = router.choose_with_retry(
        tracker
    )

    assert worker != "worker-a"