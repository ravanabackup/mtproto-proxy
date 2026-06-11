from enum import Enum
from src.models import ProxyMetrics


class ProxyRateEvaluation(Enum):
    GOOD = "Good"
    NORMAL = "Normal"
    BAD = "Bad"


def evaluate_proxy_rate(stats: ProxyMetrics) -> ProxyRateEvaluation:
    if stats.rate >= 50:
        return ProxyRateEvaluation.GOOD
    elif stats.rate < 50 and stats.rate >= 45:
        return ProxyRateEvaluation.NORMAL
    else:
        return ProxyRateEvaluation.BAD