from app.mcp_metrics import log_mcp_event

def test_mcp_metrics_logged(mocker):
    mock_collection = mocker.patch(
        "app.mcp_metrics.metrics_collection"
    )

    log_mcp_event({
        "user_id": "user-123",
        "agent": "qa-agent",
        "latency_ms": 100,
        "status": "success"
    })

    mock_collection.insert_one.assert_called_once()
