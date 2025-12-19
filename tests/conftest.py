import pytest

@pytest.fixture
def user_id():
    return "user-123"

@pytest.fixture
def other_user_id():
    return "user-999"

@pytest.fixture
def profile(user_id):
    return {
        "_id": 1,
        "user_id": user_id,
        "general": {"name": "Test"},
        "goals": ["Muscle Gain"]
    }
