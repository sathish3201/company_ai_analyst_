from company_ai.core.context import RequestContext
from company_ai.models.security import (
    UserIdentity,
    PermissionContext,
)
from company_ai.core.request import RequestIdentity


def create_context():

    return RequestContext(
        request=RequestIdentity.create(),
        user=UserIdentity(
            user_id="user-1",
            company_id="company-1",
            role="analyst",
        ),
        permissions=PermissionContext(
            allowed_tools=["sql"],
            allowed_tables=["sales"],
            can_read=True,
            can_write=False,
        ),
    )


def test_request_context():

    context = create_context()

    assert context.user_id == "user-1"
    assert context.company_id == "company-1"
    assert context.role == "analyst"