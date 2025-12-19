import pytest
from app.form_submit import update_personal_info

def test_update_denied_by_cerbos(mocker, profile, other_user_id):
    mocker.patch(
        "app.form_submit.check_access",
        return_value=False
    )

    with pytest.raises(PermissionError):
        update_personal_info(
            profile,
            section="general",
            user_id=other_user_id,
            role="user",
            name="Hacker"
        )
