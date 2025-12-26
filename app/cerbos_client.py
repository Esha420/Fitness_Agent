#app/cerbos_client.py
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource

CERBOS_URL = "http://localhost:3592"

client = CerbosClient(CERBOS_URL)


def check_access(
    *,
    principal_id: str,
    role: str,
    action: str,
    resource_kind: str,
    resource_id: str,
    resource_owner_id: str | None = None,
):
    principal = Principal(
        id=principal_id,
        roles=[role],
    )

    resource = Resource(
        id=resource_id,
        kind=resource_kind,
        attr={"user_id": resource_owner_id} if resource_owner_id else {},
    )

    return client.is_allowed(action, principal, resource)
