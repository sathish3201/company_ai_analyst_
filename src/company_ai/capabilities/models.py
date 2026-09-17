from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class CapabilityType(str, Enum):
    """
    High-level category of a capability.
    """

    AGENT = "agent"
    TOOL = "tool"
    WORKER = "worker"
    SUBAGENT = "subagent"
    DATA_SOURCE = "data_source"
    ANALYZER = "analyzer"
    RETRIEVER = "retriever"


class CapabilityMetadata(BaseModel):
    """
    Metadata describing a dynamically registered capability.
    """

    capability_id: str

    name: str

    capability_type: CapabilityType

    version: str = "1.0"

    description: str = ""

    tags: list[str] = Field(
        default_factory=list
    )

    input_schema: dict[str, Any] = Field(
        default_factory=dict
    )

    output_schema: dict[str, Any] = Field(
        default_factory=dict
    )

    dependencies: list[str] = Field(
        default_factory=list
    )

    config: dict[str, Any] = Field(
        default_factory=dict
    )


class CapabilityRequest(BaseModel):
    """
    Runtime request sent to a capability.
    """

    capability_id: str

    input: dict[str, Any] = Field(
        default_factory=dict
    )

    context: dict[str, Any] = Field(
        default_factory=dict
    )

    config: dict[str, Any] = Field(
        default_factory=dict
    )


class CapabilityResult(BaseModel):
    """
    Standardized capability result.
    """

    success: bool

    capability_id: str

    output: Any = None

    error: str | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )