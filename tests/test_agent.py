import os
import sys

# Add the project root to Python's import path.
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    ),
)

# Keep this test independent of Gemini API quota.
os.environ["USE_GEMINI"] = "false"

from app.agent import process_command


def test_process_command_empty():
    result = process_command("")

    assert result["success"] is False
    assert result["result"]["message"] == (
        "Please provide a smart-home command."
    )