import time
import ssl


class ReplayGuard:

    def __init__(
        self,
        window_seconds=60,
    ):
        self.window_seconds = window_seconds

        self.seen = {}

    def allow(
        self,
        message_id,
    ):
        now = time.time()

        expired = [
            mid
            for mid, ts in self.seen.items()
            if now - ts > self.window_seconds
        ]

        for mid in expired:
            del self.seen[mid]

        if message_id in self.seen:
            return False

        self.seen[message_id] = now

        return True

class RateLimiter:

    def __init__(
        self,
        limit=5,
        period=60,
    ):
        self.limit = limit

        self.period = period

        self.events = {}

    def allow(
        self,
        source,
    ):
        now = time.time()

        history = self.events.setdefault(
            source,
            [],
        )

        history[:] = [
            ts
            for ts in history
            if now - ts < self.period
        ]

        if len(history) >= self.limit:
            return False

        history.append(now)

        return True

def create_server_context():

    ctx = ssl.create_default_context(
        ssl.Purpose.CLIENT_AUTH
    )

    return ctx


def create_client_context():

    ctx = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH
    )
        
    return ctx


