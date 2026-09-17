import pytest

from company_ai.capabilities.contracts import (
    CapabilityPort,
)

from company_ai.capabilities.decorators import (
    capability,
)

from company_ai.capabilities.models import (
    CapabilityType,
)

from company_ai.capabilities.registry import (
    CapabilityRegistry,
)


@capability(
    capability_id="registry_test",
    name="Registry Test",
    capability_type=CapabilityType.TOOL,
)
class RegistryTestCapability(
    CapabilityPort
):

    @property
    def metadata(self):

        return self.__capability_metadata__

    async def execute(
        self,
        request,
    ):

        raise NotImplementedError


def test_register():

    registry = CapabilityRegistry()

    registry.register(
        RegistryTestCapability
    )

    assert registry.has(
        "registry_test"
    )

    assert registry.get(
        "registry_test"
    ) is RegistryTestCapability


def test_duplicate_registration():

    registry = CapabilityRegistry()

    registry.register(
        RegistryTestCapability
    )

    with pytest.raises(ValueError):

        registry.register(
            RegistryTestCapability
        )


def test_missing_capability():

    registry = CapabilityRegistry()

    with pytest.raises(KeyError):

        registry.get(
            "missing"
        )


def test_unregister():

    registry = CapabilityRegistry()

    registry.register(
        RegistryTestCapability
    )

    registry.unregister(
        "registry_test"
    )

    assert not registry.has(
        "registry_test"
    )