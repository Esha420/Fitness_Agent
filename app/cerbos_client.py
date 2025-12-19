# app/cerbos_client.py
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource

CERBOS_URL = "http://localhost:3592"

def check_access(action: str, resource_kind: str, resource_id: str, principal_id: str, resource_owner_id: str, role: str = "user"):
    """
    Checks if a principal (user) can perform an action on a resource.
    """
    with CerbosClient(CERBOS_URL) as client:
        principal = Principal(id=principal_id, roles=[role])
        resource = Resource(id=resource_id, kind=resource_kind, attr={"user_id": resource_owner_id})

        allowed = client.is_allowed(action, principal, resource)
        return allowed
