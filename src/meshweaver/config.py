from dataclasses import dataclass, field


@dataclass
class Config:
    host: str = "127.0.0.1"
    port: int = 9000

    secret_key: str = "meshweaver-dev-key"

    bootstrap_peers: list[tuple[str, int]] = field(default_factory=list)

    max_pending_requests: int = 100
    request_timeout: float = 3.0