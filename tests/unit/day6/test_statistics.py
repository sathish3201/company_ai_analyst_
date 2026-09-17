from company_ai.data.analysis.statistics import (
    StatisticsAnalyzer,
)


def test_mean():

    analyzer = StatisticsAnalyzer()

    assert analyzer.mean(
        [10, 20, 30]
    ) == 20


def test_median():

    analyzer = StatisticsAnalyzer()

    assert analyzer.median(
        [10, 30, 20]
    ) == 20


def test_summary():

    analyzer = StatisticsAnalyzer()

    result = analyzer.summary(
        [10, 20, 30]
    )

    assert result["count"] == 3
    assert result["mean"] == 20


def test_z_scores():

    analyzer = StatisticsAnalyzer()

    result = analyzer.z_scores(
        [10, 20, 30]
    )

    assert len(result) == 3