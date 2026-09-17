from company_ai.capabilities.decorators import (
    capability,
)

from company_ai.capabilities.models import (
    CapabilityType,
)


def test_capability_decorator():

    @capability(
        capability_id="dynamic_test",
        name="Dynamic Test",
        capability_type=CapabilityType.WORKER,
        version="2.0",
        description="Test capability",
        tags=[
            "dynamic",
            "test",
        ],
    )
    class DynamicTest:

        pass

    metadata = (
        DynamicTest.__capability_metadata__
    )

    assert metadata.capability_id == (
        "dynamic_test"
    )

    assert metadata.version == "2.0"

    assert "dynamic" in metadata.tags