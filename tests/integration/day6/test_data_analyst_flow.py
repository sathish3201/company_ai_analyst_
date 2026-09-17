import pytest

from company_ai.capabilities.discovery import (
    CapabilityDiscovery,
)
from company_ai.capabilities.registry import (
    CapabilityRegistry,
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
from company_ai.data.analysis.pandas_analyzer import (
    PandasAnalyzer,
)
from company_ai.data.analysis.profiler import (
    DataProfiler,
)
from company_ai.data.capabilities.analysis import (
    DataAnalysisCapability,
)
from company_ai.data.capabilities.profiling import (
    DataProfilingCapability,
)
from company_ai.data.capabilities.sql import (
    SQLQueryCapability,
)


@pytest.mark.asyncio
async def test_dynamic_data_capabilities():

    registry = CapabilityRegistry()

    registry.register(
        SQLQueryCapability
    )

    registry.register(
        DataProfilingCapability
    )

    registry.register(
        DataAnalysisCapability
    )

    assert registry.has(
        "data.sql.query"
    )

    assert registry.has(
        "data.profile"
    )

    assert registry.has(
        "data.analysis"
    )

    sql = SQLQueryCapability(
        ReadOnlySQLExecutor(
            InMemorySQLConnection(
                {
                    "SELECT * FROM sales": [
                        {
                            "department": "IT",
                            "amount": 100,
                        },
                        {
                            "department": "HR",
                            "amount": 200,
                        },
                    ]
                }
            ),
            ReadOnlyQueryValidator(),
        )
    )

    result = await sql.execute(
        __import__(
            "company_ai.capabilities.models",
            fromlist=["CapabilityRequest"],
        ).CapabilityRequest(
            capability_id="data.sql.query",
            input={
                "query": "SELECT * FROM sales",
            },
        )
    )

    assert result.success is True

    profiler = DataProfilingCapability(
        DataProfiler()
    )

    profile = await profiler.execute(
        __import__(
            "company_ai.capabilities.models",
            fromlist=["CapabilityRequest"],
        ).CapabilityRequest(
            capability_id="data.profile",
            input={
                "data": result.output["rows"]
            },
        )
    )

    assert profile.success is True

    analyzer = DataAnalysisCapability(
        PandasAnalyzer()
    )

    analysis = await analyzer.execute(
        __import__(
            "company_ai.capabilities.models",
            fromlist=["CapabilityRequest"],
        ).CapabilityRequest(
            capability_id="data.analysis",
            input={
                "operation": "group_by",
                "data": result.output["rows"],
                "parameters": {
                    "group_column": "department",
                    "aggregation": "sum",
                    "value_column": "amount",
                },
            },
        )
    )

    assert analysis.success is True