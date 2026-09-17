from typing import Any

from company_ai.capabilities.models import (
    CapabilityMetadata,
    CapabilityType,
)


def capability(
    *,
    capability_id: str,
    name: str,
    capability_type: CapabilityType,
    version: str = "1.0",
    description: str = "",
    tags: list[str] | None = None,
    input_schema: dict[str, Any] | None = None,
    output_schema: dict[str, Any] | None = None,
    dependencies: list[str] | None = None,
):
    """
    Decorator used to dynamically register metadata
    on a capability class.
    """

    metadata = CapabilityMetadata(
        capability_id=capability_id,
        name=name,
        capability_type=capability_type,
        version=version,
        description=description,
        tags=tags or [],
        input_schema=input_schema or {},
        output_schema=output_schema or {},
        dependencies=dependencies or [],
    )

    def decorator(
        cls: type,
    ) -> type:

        cls.__capability_metadata__ = metadata

        return cls

    return decorator