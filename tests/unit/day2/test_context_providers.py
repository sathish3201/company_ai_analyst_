import pytest

from company_ai.context_engine.providers.enterprise_provider import (
    EnterpriseContextProvider,
)
from company_ai.context_engine.providers.memory_provider import (
    MemoryContextProvider,
)
from company_ai.context_engine.providers.request_provider import (
    RequestContextProvider,
)
from company_ai.context_engine.providers.user_provider import (
    UserContextProvider,
)


@pytest.mark.asyncio
async def test_request_provider():
    provider = RequestContextProvider()

    result = await provider.provide(
        "Show sales data"
    )

    assert len(result.items) == 1
    assert result.items[0].source == "request"
    assert result.items[0].content == "Show sales data"
    assert result.items[0].relevance == 1.0


@pytest.mark.asyncio
async def test_user_provider():
    provider = UserContextProvider(
        user_context="User is a data analyst"
    )

    result = await provider.provide(
        "Show sales"
    )

    assert len(result.items) == 1
    assert result.items[0].source == "user"
    assert result.items[0].content == (
        "User is a data analyst"
    )


@pytest.mark.asyncio
async def test_empty_user_provider():
    provider = UserContextProvider()

    result = await provider.provide(
        "Show sales"
    )

    assert result.items == []


@pytest.mark.asyncio
async def test_enterprise_provider():
    provider = EnterpriseContextProvider(
        enterprise_context="Company fiscal year is Q1-Q4"
    )

    result = await provider.provide(
        "Show revenue"
    )

    assert len(result.items) == 1
    assert result.items[0].source == "enterprise"


@pytest.mark.asyncio
async def test_memory_provider():
    provider = MemoryContextProvider(
        memories=[
            "User prefers SQL reports",
            "User works with APAC data",
        ]
    )

    result = await provider.provide(
        "Show revenue"
    )

    assert len(result.items) == 2
    assert result.items[0].source == "memory"


@pytest.mark.asyncio
async def test_empty_memory_provider():
    provider = MemoryContextProvider()

    result = await provider.provide(
        "Show revenue"
    )

    assert result.items == []