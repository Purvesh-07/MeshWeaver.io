from meshweaver.security import ReplayGuard


def test_replay_guard():

    guard = ReplayGuard()

    assert guard.allow(
        "abc"
    )

    assert not guard.allow(
        "abc"
    )

from meshweaver.security import RateLimiter


def test_rate_limit():

    limiter = RateLimiter(
        limit=2,
        period=60,
    )

    assert limiter.allow(
        "node-a"
    )

    assert limiter.allow(
        "node-a"
    )

    assert not limiter.allow(
        "node-a"
    )

from meshweaver.security import (
    create_server_context,
    create_client_context,
)


def test_tls_contexts():

    assert (
        create_server_context()
        is not None
    )

    assert (
        create_client_context()
        is not None
    )