from typing import Any

from company_ai.capabilities.contracts import (
    CapabilityPort,
)

from company_ai.capabilities.factory import (
    CapabilityFactory,
)

from company_ai.capabilities.models import (
    CapabilityRequest,
    CapabilityResult,
)


class CapabilityResolver:
    """
    Resolves workflow capability IDs into executable
    capability instances.
    """

    def __init__(
        self,
        factory: CapabilityFactory,
    ) -> None:

        self._factory = factory

    def resolve(
        self,
        capability_id: str,
        config: dict[str, Any] | None = None,
    ) -> CapabilityPort:

        return self._factory.create(
            capability_id=capability_id,
            config=config,
        )

    async def execute(
        self,
        capability_id: str,
        request: CapabilityRequest,
    ) -> CapabilityResult:

        capability = self.resolve(
            capability_id=capability_id,
            config=request.config,
        )

        return await capability.execute(
            request
        )