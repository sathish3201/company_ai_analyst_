import pytest

from company_ai.capabilities.models import (
    CapabilityRequest,
)
from company_ai.data.analysis.profiler import (
    DataProfiler,
)
from company_ai.data.capabilities.profiling import (
    DataProfilingCapability,
)


@pytest.mark.asyncio
async def test_profiling_capability():

    capability = DataProfilingCapability(
        DataProfiler()
    )

    result = await capability.execute(
        CapabilityRequest(
            capability_id="data.profile",
            input={
                "data": [
                    {"name": "Alice"},
                    {"name": "Bob"},
                ]
            },
        )
    )

    assert result.success is True
    assert result.output["row_count"] == 2