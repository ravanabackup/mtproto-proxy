from enum import Enum
from models import ProxyMetrics


class ProxyRateEvaluation(Enum):
    GOOD = "Good"
    NORMAL = "Normal"
    BAD = "Bad"


def evaluate_proxy_rate(stats: ProxyMetrics) -> ProxyRateEvaluation:
    if stats.rate >= 50:
        print("GOOD")
        return ProxyRateEvaluation.GOOD
    elif stats.rate < 50 and stats.rate >= 45:
        print("NORMAL")
        return ProxyRateEvaluation.NORMAL
    else:
        print("BAD")
        return ProxyRateEvaluation.BAD