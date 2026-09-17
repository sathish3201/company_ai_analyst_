import pytest

from company_ai.agents.reducer import (
    DeepAgentResultReducer,
)


@pytest.mark.asyncio
async def test_reducer():

    reducer = DeepAgentResultReducer()

    results = [
        {
            "task_id": "1",
            "task": "Get data",
            "result": {
                "rows": 100
            },
        },
        {
            "task_id": "2",
            "task": "Analyze data",
            "result": {
                "average": 50
            },
        },
    ]

    result = await reducer.reduce(
        goal="Analyze sales",
        results=results,
    )

    assert result["goal"] == "Analyze sales"

    assert result["total_results"] == 2

    assert len(
        result["results"]
    ) == 2