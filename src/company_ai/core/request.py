from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class RequestIdentity:
    request_id: str
    trace_id: str

    @classmethod
    def create(cls) -> "RequestIdentity":
        return cls(
            request_id=str(uuid4()),
            trace_id=str(uuid4()),
        )