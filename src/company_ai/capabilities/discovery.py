import importlib
import inspect
import pkgutil
from types import ModuleType
from typing import Any

from company_ai.capabilities.contracts import (
    CapabilityPort,
)

from company_ai.capabilities.registry import (
    CapabilityRegistry,
)


class CapabilityDiscovery:
    """
    Dynamically discovers capability implementations
    from Python modules/packages.
    """

    def __init__(
        self,
        registry: CapabilityRegistry,
    ) -> None:

        self._registry = registry

    def discover_module(
        self,
        module_name: str,
    ) -> list[type[CapabilityPort]]:

        module = importlib.import_module(
            module_name
        )

        return self._discover_module(
            module
        )

    def discover_package(
        self,
        package_name: str,
    ) -> list[type[CapabilityPort]]:

        package = importlib.import_module(
            package_name
        )

        discovered: list[
            type[CapabilityPort]
        ] = []

        if not hasattr(
            package,
            "__path__",
        ):
            return discovered

        for module_info in pkgutil.walk_packages(
            package.__path__,
            package.__name__ + ".",
        ):

            module = importlib.import_module(
                module_info.name
            )

            discovered.extend(
                self._discover_module(
                    module
                )
            )

        return discovered

    def _discover_module(
        self,
        module: ModuleType,
    ) -> list[type[CapabilityPort]]:

        discovered: list[
            type[CapabilityPort]
        ] = []

        for _, obj in inspect.getmembers(
            module,
            inspect.isclass,
        ):

            if obj is CapabilityPort:
                continue

            if not issubclass(
                obj,
                CapabilityPort,
            ):
                continue

            if obj.__module__ != module.__name__:
                continue

            if not hasattr(
                obj,
                "__capability_metadata__",
            ):
                continue

            self._registry.register(obj)

            discovered.append(obj)

        return discovered