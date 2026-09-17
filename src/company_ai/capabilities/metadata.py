from typing import Any

from company_ai.capabilities.models import (
    CapabilityMetadata,
)


class CapabilityMetadataReader:
    """
    Reads capability metadata using reflection/introspection.
    """

    @staticmethod
    def read(
        capability_class: type,
    ) -> CapabilityMetadata:

        metadata = getattr(
            capability_class,
            "__capability_metadata__",
            None,
        )

        if metadata is None:
            raise ValueError(
                "Capability class does not contain "
                "registered metadata: "
                f"{capability_class.__name__}"
            )

        if isinstance(
            metadata,
            CapabilityMetadata,
        ):
            return metadata

        if isinstance(
            metadata,
            dict,
        ):
            return CapabilityMetadata(
                **metadata
            )

        raise TypeError(
            "Invalid capability metadata type"
        )

    @staticmethod
    def get_class_name(
        capability_class: type,
    ) -> str:

        return capability_class.__name__

    @staticmethod
    def get_module(
        capability_class: type,
    ) -> str:

        return capability_class.__module__

    @staticmethod
    def get_methods(
        capability_class: type,
    ) -> tuple[str, ...]:

        return tuple(
            name
            for name in dir(capability_class)
            if not name.startswith("_")
        )

    @staticmethod
    def get_annotations(
        capability_class: type,
    ) -> dict[str, Any]:

        return dict(
            getattr(
                capability_class,
                "__annotations__",
                {},
            )
        )