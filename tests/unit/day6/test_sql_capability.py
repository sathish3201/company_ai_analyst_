import pytest

from company_ai.capabilities.models import (
    CapabilityRequest,
)
from company_ai.data.access.connection import (
    InMemorySQLConnection,
)
from company_ai.data.access.query_validator import (
    ReadOnlyQueryValidator,
)
from company_ai.data.access.sql_executor import (
    ReadOnlySQLExecutor,
)
from company_ai.data.capabilities.sql import (
    SQLQueryCapability,
)


@pytest.mark.asyncio
async def test_sql_capability():

    query = "SELECT * FROM employees"

    connection = InMemorySQLConnection(
        {
            query: [
                {
                    "id": 1,
                    "name": "Alice",
                }
            ]
        }
    )

    executor = ReadOnlySQLExecutor(
        connection,
        ReadOnlyQueryValidator(),
    )

    capability = SQLQueryCapability(
        executor
    )

    result = await capability.execute(
        CapabilityRequest(
            capability_id="data.sql.query",
            input={
                "query": query,
            },
        )
    )

    assert result.success is True
    assert result.output["row_count"] == 1