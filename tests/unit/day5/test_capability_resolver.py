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
async def test_resolver_executes_capability():

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

    resolver = CapabilityResolver(
        factory
    )

    request = CapabilityRequest(
        capability_id="text_analysis",
        input={
            "text": "hello world"
        },
    )

    result = await resolver.execute(
        capability_id="text_analysis",
        request=request,
    )

    assert result.success is True

    assert result.output["length"] == 11

    assert result.output["words"] == 2