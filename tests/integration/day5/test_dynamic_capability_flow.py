import pytest

from company_ai.capabilities.discovery import (
    CapabilityDiscovery,
)

from company_ai.capabilities.factory import (
    CapabilityFactory,
)

from company_ai.capabilities.models import (
    CapabilityRequest,
)

from company_ai.capabilities.registry import (
    CapabilityRegistry,
)

from company_ai.capabilities.resolver import (
    CapabilityResolver,
)


@pytest.mark.asyncio
async def test_dynamic_capability_end_to_end():

    registry = CapabilityRegistry()

    discovery = CapabilityDiscovery(
        registry
    )

    discovered = (
        discovery.discover_module(
            "company_ai.capabilities.examples.basic"
        )
    )

    assert len(discovered) >= 2

    factory = CapabilityFactory(
        registry
    )

    resolver = CapabilityResolver(
        factory
    )

    request = CapabilityRequest(
        capability_id="customer_lookup",
        input={
            "customer_id": "CUST-001"
        },
    )

    result = await resolver.execute(
        capability_id="customer_lookup",
        request=request,
    )

    assert result.success is True

    assert result.capability_id == (
        "customer_lookup"
    )

    assert result.output["customer_id"] == (
        "CUST-001"
    )

    assert result.output["status"] == (
        "found"
    )