from pydantic import BaseModel, Field


class UserIdentity(BaseModel):
    user_id: str
    company_id: str
    role: str


class PermissionContext(BaseModel):
    allowed_tools: list[str] = Field(default_factory=list)
    allowed_tables: list[str] = Field(default_factory=list)
    allowed_columns: list[str] = Field(default_factory=list)

    can_read: bool = True
    can_write: bool = False
    can_access_pii: bool = False


class SessionContext(BaseModel):
    session_id: str
    user: UserIdentity
    permissions: PermissionContext