from company_ai.contracts.security import AuthorizationPort
from company_ai.core.context import RequestContext


class DefaultAuthorizationService(AuthorizationPort):

    def can_use_tool(
        self,
        context: RequestContext,
        tool_name: str,
    ) -> bool:
        return tool_name in context.permissions.allowed_tools

    def can_access_table(
        self,
        context: RequestContext,
        table_name: str,
    ) -> bool:
        return table_name in context.permissions.allowed_tables

    def can_access_column(
        self,
        context: RequestContext,
        table_name: str,
        column_name: str,
    ) -> bool:
        return (
            self.can_access_table(context, table_name)
            and column_name in context.permissions.allowed_columns
        )

    def can_write(
        self,
        context: RequestContext,
    ) -> bool:
        return context.permissions.can_write

    def can_access_pii(
        self,
        context: RequestContext,
    ) -> bool:
        return context.permissions.can_access_pii