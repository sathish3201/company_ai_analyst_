from company_ai.models.context import (
    ContextBundle,
    ContextItem,
    IntentType,
)


def test_context_item():
    item = ContextItem(
        source="request",
        content="Show sales",
        relevance=1.0,
    )

    assert item.source == "request"
    assert item.content == "Show sales"
    assert item.relevance == 1.0


def test_context_bundle_text():
    bundle = ContextBundle(
        items=[
            ContextItem(
                source="request",
                content="Show sales",
            ),
            ContextItem(
                source="user",
                content="User is analyst",
            ),
        ]
    )

    assert "Show sales" in bundle.text
    assert "User is analyst" in bundle.text


def test_intent_enum():
    assert IntentType.DATA_ANALYSIS.value == "data_analysis"