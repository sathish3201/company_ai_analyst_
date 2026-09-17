from company_ai.capabilities.contracts import (
    CapabilityPort,
)

from company_ai.capabilities.decorators import (
    capability,
)

from company_ai.capabilities.models import (
    CapabilityRequest,
    CapabilityResult,
    CapabilityType,
)


@capability(
    capability_id="text_analysis",
    name="Text Analysis",
    capability_type=CapabilityType.ANALYZER,
    version="1.0",
    description="Analyzes text input.",
    tags=[
        "text",
        "analysis",
    ],
)
class TextAnalysisCapability(
    CapabilityPort
):

    def __init__(
        self,
        prefix: str = "",
    ) -> None:

        self._prefix = prefix

    @property
    def metadata(self):

        return self.__capability_metadata__

    async def execute(
        self,
        request: CapabilityRequest,
    ) -> CapabilityResult:

        text = request.input.get(
            "text",
            "",
        )

        result = {
            "text": text,
            "length": len(text),
            "words": len(
                text.split()
            ),
            "prefix": self._prefix,
        }

        return CapabilityResult(
            success=True,
            capability_id=(
                self.metadata.capability_id
            ),
            output=result,
        )


@capability(
    capability_id="customer_lookup",
    name="Customer Lookup",
    capability_type=CapabilityType.TOOL,
    version="1.0",
    description="Looks up customer information.",
    tags=[
        "customer",
        "lookup",
    ],
)
class CustomerLookupCapability(
    CapabilityPort
):

    @property
    def metadata(self):

        return self.__capability_metadata__

    async def execute(
        self,
        request: CapabilityRequest,
    ) -> CapabilityResult:

        customer_id = request.input.get(
            "customer_id"
        )

        return CapabilityResult(
            success=True,
            capability_id=(
                self.metadata.capability_id
            ),
            output={
                "customer_id": customer_id,
                "status": "found",
            },
        )