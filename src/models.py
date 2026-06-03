from dataclasses import dataclass


@dataclass(slots=True)
class ProxyInfo:
    url: str
    host: str
    port: int
    secret: str
    alive: bool
    latency_ms: float | None