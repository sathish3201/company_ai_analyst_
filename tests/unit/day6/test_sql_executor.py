import pytest

from company_ai.data.access.connection import (
    InMemorySQLConnection,
)
from company_ai.data.access.query_validator import (
    ReadOnlyQueryValidator,
)
from company_ai.data.access.sql_executor import (
    ReadOnlySQLExecutor,
)
from company_ai.data.models import QueryRequest


@pytest.mark.asyncio
async def test_sql_executor():

    query = "SELECT * FROM employees"

    connection = InMemorySQLConnection(
        {
            query: [
                {
                    "id": 1,
                    "name": "Alice",
                },
                {
                    "id": 2,
                    "name": "Bob",
                },
            ]
        }
    )

    executor = ReadOnlySQLExecutor(
        connection=connection,
        validator=ReadOnlyQueryValidator(),
    )

    result = await executor.execute(
        QueryRequest(query=query)
    )

    assert result.row_count == 2
    assert result.columns == [
        "id",
        "name",
    ]


@pytest.mark.asyncio
async def test_sql_executor_respects_row_limit():

    query = "SELECT * FROM employees"

    connection = InMemorySQLConnection(
        {
            query: [
                {"id": 1},
                {"id": 2},
                {"id": 3},
            ]
        }
    )

    executor = ReadOnlySQLExecutor(
        connection=connection,
        validator=ReadOnlyQueryValidator(),
    )

    result = await executor.execute(
        QueryRequest(
            query=query,
            max_rows=2,
        )
    )

    assert result.row_count == 2
    assert result.truncated is True