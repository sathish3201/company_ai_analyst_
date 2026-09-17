from company_ai.capabilities.decorators import (
    capability,
)

from company_ai.capabilities.metadata import (
    CapabilityMetadataReader,
)

from company_ai.capabilities.models import (
    CapabilityType,
)


@capability(
    capability_id="test_capability",
    name="Test Capability",
    capability_type=CapabilityType.TOOL,
    tags=["test"],
)
class TestCapability:
    pass


def test_metadata_reader():

    metadata = (
        CapabilityMetadataReader.read(
            TestCapability
        )
    )

    assert metadata.capability_id == (
        "test_capability"
    )

    assert metadata.name == (
        "Test Capability"
    )

    assert metadata.capability_type == (
        CapabilityType.TOOL
    )


def test_class_name():

    name = (
        CapabilityMetadataReader
        .get_class_name(TestCapability)
    )

    assert name == "TestCapability"


def test_module():

    module = (
        CapabilityMetadataReader
        .get_module(TestCapability)
    )

    assert module == __name__