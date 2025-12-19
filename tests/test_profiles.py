from app.profiles import get_profile

def test_profile_isolation(mocker, user_id, other_user_id):
    mock_collection = mocker.patch(
        "app.profiles.personal_data_collection"
    )

    mock_collection.find_one.return_value = None

    profile = get_profile(1, other_user_id)
    assert profile is None
