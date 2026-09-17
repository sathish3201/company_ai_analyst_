from company_ai.core.request import RequestIdentity


def test_request_identity_creation():

    identity = RequestIdentity.create()

    assert identity.request_id
    assert identity.trace_id

    assert identity.request_id != identity.trace_id


from uuid import UUID


def test_request_ids_are_valid_uuid():

    identity = RequestIdentity.create()

    UUID(identity.request_id)
    UUID(identity.trace_id)