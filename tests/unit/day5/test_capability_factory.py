from company_ai.capabilities.discovery import (
    CapabilityDiscovery,
)

from company_ai.capabilities.factory import (
    CapabilityFactory,
)

from company_ai.capabilities.registry import (
    CapabilityRegistry,
)


def test_factory_creates_capability():

    registry = CapabilityRegistry()

    discovery = CapabilityDiscovery(
        registry
    )

    discovery.discover_module(
        "company_ai.capabilities.examples.basic"
    )

    factory = CapabilityFactory(
        registry
    )

    capability = factory.create(
        capability_id="text_analysis",
        config={
            "prefix": "TEST"
        },
    )

    assert capability is not None

    assert capability.__class__.__name__ == (
        "TextAnalysisCapability"
    )

    assert capability._prefix == "TEST"