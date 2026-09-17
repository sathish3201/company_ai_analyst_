from company_ai.security.authorization import (
    DefaultAuthorizationService,
)

from company_ai.models.security import (
    UserIdentity,
    PermissionContext,
)


def create_service():

    user = UserIdentity(
        user_id="user-1",
        company_id="company-1",
        role="analyst",
    )

    permissions = PermissionContext(
        allowed_tools=["sql", "python"],
        allowed_tables=["sales", "customers"],
        allowed_columns=["sales.revenue"],
        can_read=True,
        can_write=False,
        can_access_pii=False,
    )

    return DefaultAuthorizationService(
        user=user,
        permissions=permissions,
    )

def test_allowed_tool():

    service = create_service()

    assert service.can_use_tool("sql") is True


def test_disallowed_tool():

    service = create_service()

    assert service.can_use_tool("email") is False


def test_allowed_table():

    service = create_service()

    assert service.can_access_table("sales") is True


def test_disallowed_table():

    service = create_service()

    assert service.can_access_table("payroll") is False


def test_write_not_allowed():

    service = create_service()

    assert service.can_write() is False


def test_pii_not_allowed():

    service = create_service()

    assert service.can_access_pii() is False