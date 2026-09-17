import pytest

from company_ai.workflows.registry import (
    WorkflowNodeRegistry,
)


def handler_one(**kwargs):
    return "one"


def handler_two(**kwargs):
    return "two"


def test_register_handler():

    registry = WorkflowNodeRegistry()

    registry.register(
        "agent",
        handler_one,
    )

    assert registry.has("agent")
    assert registry.get("agent") is handler_one


def test_duplicate_registration_fails():

    registry = WorkflowNodeRegistry()

    registry.register(
        "agent",
        handler_one,
    )

    with pytest.raises(ValueError):

        registry.register(
            "agent",
            handler_two,
        )


def test_missing_handler_fails():

    registry = WorkflowNodeRegistry()

    with pytest.raises(KeyError):

        registry.get("agent")


def test_unregister_handler():

    registry = WorkflowNodeRegistry()

    registry.register(
        "agent",
        handler_one,
    )

    registry.unregister("agent")

    assert not registry.has("agent")


def test_names():

    registry = WorkflowNodeRegistry()

    registry.register(
        "agent",
        handler_one,
    )

    registry.register(
        "worker",
        handler_two,
    )

    assert registry.names() == (
        "agent",
        "worker",
    )