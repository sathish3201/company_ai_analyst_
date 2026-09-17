from company_ai.data.analysis.profiler import (
    DataProfiler,
)


def test_profiler():

    data = [
        {"name": "Alice", "salary": 100},
        {"name": "Bob", "salary": 200},
        {"name": "Charlie", "salary": None},
    ]

    profile = DataProfiler().profile(data)

    assert profile.row_count == 3
    assert profile.column_count == 2

    assert (
        profile.columns["salary"]["null_count"]
        == 1
    )

    assert (
        profile.columns["salary"]["unique_count"]
        == 2
    )