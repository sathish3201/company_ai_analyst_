from company_ai.context_engine.filter import ContextFilter
from company_ai.context_engine.ranker import ContextRanker
from company_ai.models.context import ContextItem


def create_items():
    return [
        ContextItem(
            source="low",
            content="Low relevance",
            relevance=0.2,
        ),
        ContextItem(
            source="high",
            content="High relevance",
            relevance=0.9,
        ),
        ContextItem(
            source="medium",
            content="Medium relevance",
            relevance=0.5,
        ),
    ]


def test_ranker_orders_by_relevance():
    ranker = ContextRanker()

    result = ranker.rank(
        create_items()
    )

    assert [
        item.source
        for item in result
    ] == [
        "high",
        "medium",
        "low",
    ]


def test_filter_limits_items():
    context_filter = ContextFilter()

    result = context_filter.filter(
        create_items(),
        max_items=2,
    )

    assert len(result) == 2


def test_filter_zero_items():
    context_filter = ContextFilter()

    result = context_filter.filter(
        create_items(),
        max_items=0,
    )

    assert result == []