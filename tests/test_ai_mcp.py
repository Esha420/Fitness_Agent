from app.ai import ask_ai

def test_mcp_context_sent(mocker, profile, user_id):
    mocker.patch(
        "app.ai._run_langflow",
        return_value="OK"
    )

    response = ask_ai(profile, "Hello", user_id)
    assert response == "OK"