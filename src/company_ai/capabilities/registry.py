from typing import Any

from company_ai.capabilities.contracts import (
    CapabilityPort,
    CapabilityRegistryPort,
)

from company_ai.capabilities.metadata import (
    CapabilityMetadataReader,
)


class CapabilityRegistry(
    CapabilityRegistryPort
):
    """
    Runtime registry for dynamically discovered
    capability classes.
    """

    def __init__(self) -> None:

        self._capabilities: dict[
            str,
            type[CapabilityPort],
        ] = {}

    def register(
        self,
        capability_class: type[CapabilityPort],
    ) -> None:

        metadata = (
            CapabilityMetadataReader.read(
                capability_class
            )
        )

        capability_id = (
            metadata.capability_id
        )

        if capability_id in self._capabilities:

            raise ValueError(
                "Capability already registered: "
                f"{capability_id}"
            )

        self._capabilities[
            capability_id
        ] = capability_class

    def unregister(
        self,
        capability_id: str,
    ) -> None:

        self._capabilities.pop(
            capability_id,
            None,
        )

    def get(
        self,
        capability_id: str,
    ) -> type[CapabilityPort]:

        try:

            return self._capabilities[
                capability_id
            ]

        except KeyError as exc:

            raise KeyError(
                "Capability not registered: "
                f"{capability_id}"
            ) from exc

    def has(
        self,
        capability_id: str,
    ) -> bool:

        return (
            capability_id
            in self._capabilities
        )

    def names(
        self,
    ) -> tuple[str, ...]:

        return tuple(
            self._capabilities.keys()
        )

    def metadata(
        self,
    ) -> list[Any]:

        return [
            CapabilityMetadataReader.read(
                capability_class
            )
            for capability_class
            in self._capabilities.values()
        ]

    def all(
        self,
    ) -> dict[
        str,
        type[CapabilityPort],
    ]:

        return dict(
            self._capabilities
        )