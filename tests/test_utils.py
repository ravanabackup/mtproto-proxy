import pytest
from src.utils import evaluate_proxy_rate, ProxyRateEvaluation
from src.models import ProxyMetrics


def test_evaluate_proxy_rate():
    fake_proxy_stats_bad = ProxyMetrics(
        total=20,
        alive_count=10,
        avg_latency=1337.1,
        dead_count=5,
        rate=44.9,
        valid=None
    )

    evaluation = evaluate_proxy_rate(fake_proxy_stats_bad)
    assert evaluation is ProxyRateEvaluation.BAD

    fake_proxy_stats_normal = ProxyMetrics(
        total=20,
        alive_count=10,
        avg_latency=1337.1,
        dead_count=5,
        rate=49.9,
        valid=None
    )

    evaluation = evaluate_proxy_rate(fake_proxy_stats_normal)
    assert evaluation is ProxyRateEvaluation.NORMAL

    fake_proxy_stats_good = ProxyMetrics(
        total=20,
        alive_count=10,
        avg_latency=1337.1,
        dead_count=5,
        rate=50,
        valid=None
    )

    evaluation = evaluate_proxy_rate(fake_proxy_stats_good)
    assert evaluation is ProxyRateEvaluation.GOOD