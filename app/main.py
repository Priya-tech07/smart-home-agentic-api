from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool

from app.models import CommandRequest, CommandResponse
from app.agent import process_command


app = FastAPI(
    title="Smart Home Agentic API",
    description="Agentic API for smart home automation",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "message": "Smart Home Agentic API is running"
    }


@app.post("/api/v1/command", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    # process_command() performs synchronous work, including
    # Gemini API calls and mock hardware operations.
    #
    # Run it in a threadpool so the FastAPI event loop
    # remains responsive while the agent is working.
    result = await run_in_threadpool(
        process_command,
        request.command,
    )

    # If the agent produced a known result, return its message.
    if result["result"] is not None:
        agent_result = result["result"]

        return CommandResponse(
            success=result["success"],
            message=agent_result["message"],
        )

    # Unknown command / unsupported intent.
    return CommandResponse(
        success=False,
        message="I could not understand the requested smart home action.",
    )