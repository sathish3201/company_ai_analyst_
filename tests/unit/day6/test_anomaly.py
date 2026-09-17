from company_ai.data.analysis.anomaly import (
    ZScoreAnomalyDetector,
)
from company_ai.data.analysis.statistics import (
    StatisticsAnalyzer,
)


def test_anomaly_detector():

    detector = ZScoreAnomalyDetector(
        StatisticsAnalyzer()
    )

    values = [
        10,
        11,
        10,
        12,
        11,
        10,
        100,
    ]

    result = detector.detect(
        values,
        threshold=2.0,
    )

    assert result