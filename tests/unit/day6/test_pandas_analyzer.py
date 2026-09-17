from company_ai.data.analysis.pandas_analyzer import (
    PandasAnalyzer,
)
from company_ai.data.models import (
    AnalysisRequest,
)


def test_head():

    request = AnalysisRequest(
        operation="head",
        data=[
            {"department": "IT", "salary": 100},
            {"department": "HR", "salary": 200},
        ],
        parameters={
            "count": 1,
        },
    )

    result = PandasAnalyzer().analyze(request)

    assert result.success is True
    assert len(result.result) == 1


def test_group_by_count():

    request = AnalysisRequest(
        operation="group_by",
        data=[
            {"department": "IT"},
            {"department": "IT"},
            {"department": "HR"},
        ],
        parameters={
            "group_column": "department",
            "aggregation": "count",
        },
    )

    result = PandasAnalyzer().analyze(request)

    assert result.success is True
    assert len(result.result) == 2


def test_filter():

    request = AnalysisRequest(
        operation="filter",
        data=[
            {"department": "IT"},
            {"department": "HR"},
        ],
        parameters={
            "column": "department",
            "value": "IT",
        },
    )

    result = PandasAnalyzer().analyze(request)

    assert result.success is True
    assert len(result.result) == 1