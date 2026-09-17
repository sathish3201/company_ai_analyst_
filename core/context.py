from dataclasses import dataclass

from company_ai.contracts.security import (
    PermissionContext,
    UserIdentity,
)
from company_ai.core.request import RequestIdentity


@dataclass(frozen=True)
class RequestContext:
    request: RequestIdentity
    user: UserIdentity
    permissions: PermissionContext

    @property
    def user_id(self) -> str:
        return self.user.user_id

    @property
    def company_id(self) -> str:
        return self.user.company_id

    @property
    def role(self) -> str:
        return self.user.role