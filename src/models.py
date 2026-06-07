import json

from dataclasses import dataclass
from io import TextIOWrapper
from typing import List, Dict, Any


@dataclass(slots=True)
class ProxyInfo:
    url: str
    host: str
    port: int
    secret: str
    alive: bool
    latency_ms: float | None


@dataclass(frozen=True)
class ProxyMetrics:
    total: int
    valid: Any
    alive_count: int
    dead_count: int
    avg_latency: float
    rate: float