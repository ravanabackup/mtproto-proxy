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


    @classmethod
    def calculate_from_files(cls, raw_file: TextIOWrapper, valid_file: TextIOWrapper) -> ProxyMetrics:
        valid = json.load(valid_file)
        total = len(
            [
                line
                for line in raw_file
                if line.strip()
            ]
        )

        alive_count = len(valid)
        dead_count = total - alive_count

        avg_latency = (
            round(
                sum(
                    p["latency_ms"]
                    for p in valid
                )
                / alive_count,
                2,
            )
            if alive_count
            else 0
        )

        rate = round((alive_count / total * 100), 1) if total else 0

        return cls(
            total=total,
            valid=valid,
            alive_count=alive_count,
            dead_count=dead_count,
            avg_latency=avg_latency,
            rate=rate,
        )