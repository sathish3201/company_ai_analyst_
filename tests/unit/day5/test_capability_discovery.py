from company_ai.capabilities.discovery import (
    CapabilityDiscovery,
)

from company_ai.capabilities.registry import (
    CapabilityRegistry,
)


def test_discover_module():

    registry = CapabilityRegistry()

    discovery = CapabilityDiscovery(
        registry
    )

    discovered = (
        discovery.discover_module(
            "company_ai.capabilities.examples.basic"
        )
    )

    ids = {
        capability.__capability_metadata__.capability_id
        for capability in discovered
    }

    assert "text_analysis" in ids

    assert "customer_lookup" in ids

    assert registry.has(
        "text_analysis"
    )

    assert registry.has(
        "customer_lookup"
    )