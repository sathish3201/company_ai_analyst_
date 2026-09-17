import pytest

from company_ai.workflows.router import (
    WorkflowRouter,
)


def test_router_registration():

    router = WorkflowRouter()

    router.register(
        "route_by_type",
        lambda state: state["route"],
    )

    assert router.has("route_by_type")


def test_router_execution():

    router = WorkflowRouter()

    router.register(
        "route_by_type",
        lambda state: state["route"],
    )

    result = router.route(
        "route_by_type",
        {"route": "research"},
    )

    assert result == "research"


def test_missing_router_fails():

    router = WorkflowRouter()

    with pytest.raises(KeyError):

        router.route(
            "unknown",
            {},
        )


def test_duplicate_router_fails():

    router = WorkflowRouter()

    router.register(
        "router",
        lambda state: "a",
    )

    with pytest.raises(ValueError):

        router.register(
            "router",
            lambda state: "b",
        )


def test_unregister_router():

    router = WorkflowRouter()

    router.register(
        "router",
        lambda state: "a",
    )

    router.unregister("router")

    assert not router.has("router")