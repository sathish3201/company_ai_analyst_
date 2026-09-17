import pytest

from company_ai.capabilities.models import (
    CapabilityRequest,
)
from company_ai.data.analysis.pandas_analyzer import (
    PandasAnalyzer,
)
from company_ai.data.capabilities.analysis import (
    DataAnalysisCapability,
)


@pytest.mark.asyncio
async def test_analysis_capability():

    capability = DataAnalysisCapability(
        PandasAnalyzer()
    )

    result = await capability.execute(
        CapabilityRequest(
            capability_id="data.analysis",
            input={
                "operation": "head",
                "data": [
                    {"name": "Alice"},
                    {"name": "Bob"},
                ],
                "parameters": {
                    "count": 1,
                },
            },
        )
    )

    assert result.success is True
    assert len(result.output) == 1