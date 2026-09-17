from company_ai.capabilities.models import (
    CapabilityMetadata,
    CapabilityRequest,
    CapabilityResult,
    CapabilityType,
)


def test_capability_metadata():

    metadata = CapabilityMetadata(
        capability_id="sql_analysis",
        name="SQL Analysis",
        capability_type=CapabilityType.ANALYZER,
    )

    assert metadata.capability_id == (
        "sql_analysis"
    )

    assert metadata.version == "1.0"


def test_capability_request():

    request = CapabilityRequest(
        capability_id="sql_analysis",
        input={
            "query": "select 1"
        },
    )

    assert request.capability_id == (
        "sql_analysis"
    )

    assert request.input["query"] == (
        "select 1"
    )


def test_capability_result():

    result = CapabilityResult(
        success=True,
        capability_id="sql_analysis",
        output={
            "rows": 10
        },
    )

    assert result.success is True

    assert result.output["rows"] == 10