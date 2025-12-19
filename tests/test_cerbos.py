from app.cerbos_client import check_access

def test_cerbos_allows_access(mocker):
    mocker.patch(
        "requests.post",
        return_value=mocker.Mock(
            raise_for_status=lambda: None,
            json=lambda: {
                "results": [{
                    "actions": {"update": "EFFECT_ALLOW"}
                }]
            }
        )
    )

    allowed = check_access(
        principal_id="user-123",
        role="user",
        resource="profile",
        action="update",
        resource_attrs={"user_id": "user-123"}
    )

    assert allowed is True
