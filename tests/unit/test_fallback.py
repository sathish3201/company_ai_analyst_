from company_ai.llm.fallback import FallbackPolicy


def test_retryable_error():

    policy = FallbackPolicy(
        retryable_errors=(TimeoutError,),
        max_attempts=3,
    )

    assert policy.should_retry(
        TimeoutError(),
        attempt=1,
    )


def test_non_retryable_error():

    policy = FallbackPolicy(
        retryable_errors=(TimeoutError,),
        max_attempts=3,
    )

    assert not policy.should_retry(
        ValueError(),
        attempt=1,
    )


def test_max_attempts():

    policy = FallbackPolicy(
        retryable_errors=(TimeoutError,),
        max_attempts=3,
    )

    assert not policy.should_retry(
        TimeoutError(),
        attempt=3,
    )