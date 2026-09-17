from abc import ABC, abstractmethod

from company_ai.models.security import (
    PermissionContext,
    UserIdentity,
)


class AuthorizationPort(ABC):
    """
    Abstract authorization contract.

    Higher-level application code depends on this interface rather than
    the concrete authorization implementation.
    """

    @abstractmethod
    def can_use_tool(
        self,
        tool_name: str,
        permissions: PermissionContext,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def can_access_table(
        self,
        table_name: str,
        permissions: PermissionContext,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def can_access_column(
        self,
        column_name: str,
        permissions: PermissionContext,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def can_write(
        self,
        permissions: PermissionContext,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def can_access_pii(
        self,
        permissions: PermissionContext,
    ) -> bool:
        raise NotImplementedError


class DefaultAuthorizationService(AuthorizationPort):
    """
    Default enterprise authorization service.

    The user identity and permission context are injected into the service,
    following dependency injection principles.

    Permission checks remain explicit and deterministic.
    """

    def __init__(
        self,
        user: UserIdentity,
        permissions: PermissionContext,
    ) -> None:
        self.user = user
        self.permissions = permissions

    def can_use_tool(
        self,
        tool_name: str,
        permissions: PermissionContext | None = None,
    ) -> bool:
        context = permissions or self.permissions
        return tool_name in context.allowed_tools

    def can_access_table(
        self,
        table_name: str,
        permissions: PermissionContext | None = None,
    ) -> bool:
        context = permissions or self.permissions
        return table_name in context.allowed_tables

    def can_access_column(
        self,
        column_name: str,
        permissions: PermissionContext | None = None,
    ) -> bool:
        context = permissions or self.permissions
        return column_name in context.allowed_columns

    def can_write(
        self,
        permissions: PermissionContext | None = None,
    ) -> bool:
        context = permissions or self.permissions
        return context.can_write

    def can_access_pii(
        self,
        permissions: PermissionContext | None = None,
    ) -> bool:
        context = permissions or self.permissions
        return context.can_access_pii