from dataclasses import dataclass


@dataclass(frozen=True)
class FallbackPolicy:
    retryable_errors: tuple[type[Exception], ...]
    max_attempts: int = 3

    def should_retry(
        self,
        error: Exception,
        attempt: int,
    ) -> bool:
        if attempt >= self.max_attempts:
            return False

        return isinstance(
            error,
            self.retryable_errors,
        )