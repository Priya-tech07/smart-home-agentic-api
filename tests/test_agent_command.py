from app.agent import process_command


def test_process_command_returns_result(monkeypatch):
    def mock_run_agent(command):
        return {
            "success": True,
            "message": "Front door locked successfully.",
        }

    monkeypatch.setattr(
        "app.agent.run_agent",
        mock_run_agent,
    )

    result = process_command(
        "I'm heading to bed, secure the house."
    )

    assert result["success"] is True
    assert result["intent"] == "llm_agent"
    assert result["result"]["message"] == (
        "Front door locked successfully."
    )