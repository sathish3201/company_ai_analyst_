from typing import Any

from company_ai.capabilities.contracts import (
    CapabilityFactoryPort,
    CapabilityPort,
)

from company_ai.capabilities.registry import (
    CapabilityRegistry,
)


class CapabilityFactory(
    CapabilityFactoryPort
):
    """
    Creates capability instances from registry metadata.
    """

    def __init__(
        self,
        registry: CapabilityRegistry,
    ) -> None:

        self._registry = registry

    def create(
        self,
        capability_id: str,
        config: dict[str, Any] | None = None,
    ) -> CapabilityPort:

        capability_class = (
            self._registry.get(
                capability_id
            )
        )

        configuration = config or {}

        return capability_class(
            **configuration
        )