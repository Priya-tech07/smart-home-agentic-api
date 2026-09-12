import os

# Keep this test independent of Gemini API quota.
os.environ["USE_GEMINI"] = "false"

from app.agent import process_command


def test_process_command_empty():
    result = process_command("")

    assert result["success"] is False
    assert result["result"]["message"] == (
        "Please provide a smart-home command."
    )