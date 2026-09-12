# Smart Home Agentic API

An asynchronous FastAPI-based smart home agent that accepts natural-language commands, reasons about the current home state, executes appropriate hardware actions, and verifies the final result.

## Overview

This project implements a small agentic smart-home system based on the following flow:

**Natural Language Command → Agent Reasoning → Observe → Plan → Act → Verify → Response**

For example:

> "I'm heading to bed, secure the house."

The agent interprets the command, checks the current state of the home, determines the required actions, executes only the necessary actions, and verifies that the requested security state was achieved.

## Features

- Asynchronous REST API using FastAPI
- Natural-language command understanding using Google Gemini
- Local intent-classification fallback for testing
- Agentic reasoning flow:
  - Understand
  - Observe
  - Plan
  - Act
  - Verify
  - Respond
- Mock smart-home hardware tools
- Strict Pydantic-based tool schemas
- Mandatory state observation before actions
- Safety check for open windows
- Final state verification after actions
- Automated tests using pytest
- Interactive API documentation through Swagger UI

## Supported Command

The current implementation supports the following intent:

### Secure House

Example:

```text
I'm heading to bed, secure the house.

The agent will:

Understand the user's intent.
Check the current door status.
Check the current window status.
Check the current light status.
Stop if any window is open.
Lock any unlocked doors.
Turn off any lights that are on.
Verify the final state.
Return the result to the user.

Architecture
The intended system flow is:

Audio Trigger
     │
     ▼
    ASR
     │
     ▼
 FastAPI REST API
     │
     ▼
 Agent / Gemini
     │
     ▼
 Understand Intent
     │
     ▼
 Observe Home State
     │
     ├── get_door_status
     ├── get_window_status
     └── get_light_status
     │
     ▼
   Plan Actions
     │
     ├── lock_doors
     └── turn_off_lights
     │
     ▼
 Final Verification
     │
     ▼
    TTS
     │
     ▼
 User Response

The audio/ASR and TTS components are represented as the intended integration points. The current implementation focuses on the FastAPI agent and mock hardware layer.

Project Structure
smart home agent/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── agent.py
│   │
│   └── hardware/
│       ├── __init__.py
│       ├── state.py
│       └── tools.py
│
├── tests/
│   ├── test_hardware.py
│   ├── test_agent.py
│   └── test_agent_command.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
Hardware Tools

The project currently contains five mock hardware tools.

Status Tools

These tools are used to observe the current physical state before taking action:

get_door_status
get_window_status
get_light_status
Action Tools

These tools modify the simulated home state:

lock_doors
turn_off_lights

The agent must evaluate the status of the home before triggering action tools.

Safety Logic

The agent follows a simple safety-first approach.

Open Windows

If any window is open, the agent does not perform the security actions.

For example:

I could not fully secure the house because these windows are open: bedroom_window.

This prevents the agent from claiming that the house is fully secured when an important part of the physical state is unsafe.

Unnecessary Actions

The agent only performs actions that are required by the observed state.

For example:

Already locked door → no locking action required
Already off light → no light action required
Unlocked door → lock it
Light that is on → turn it off
Final Verification

After performing actions, the agent checks the hardware state again.

Successful verification requires:

All doors locked
All windows closed
All lights off

The API reports failure if the final state cannot be verified.

API
Health / Root Endpoint
GET /

Example response:

{
  "message": "Smart Home Agentic API is running"
}
Command Endpoint
POST /api/v1/command

Request:

{
  "command": "I'm heading to bed, secure the house"
}

Successful response:

{
  "success": true,
  "message": "All windows are closed. Unlocked doors were locked. Lights that were on were turned off. House security was verified successfully."
}

Unsupported commands return:

{
  "success": false,
  "message": "I could not understand the requested smart home action."
}
Technologies
Python 3.11
FastAPI
Uvicorn
Pydantic
Google Gemini API
python-dotenv
pytest
Setup
1. Create and activate a virtual environment

Windows PowerShell:

python -m venv .venv
.venv\Scripts\Activate.ps1
2. Install dependencies
pip install -r requirements.txt
3. Configure Gemini

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key
USE_GEMINI=true

Do not commit the .env file to source control.

The .gitignore file should contain:

.env
.venv/
__pycache__/
.pytest_cache/
4. Start the API
uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs
Testing

Run the automated tests with:

python -m pytest

Current test status:

2 passed

The tests cover the hardware tools and agent behavior.

Local Mode

The agent can also run without Gemini for local testing.

Set:

USE_GEMINI=false

In local mode, supported commands are identified using simple keyword-based intent matching.

This mode is useful for testing the agent and hardware behavior without making Gemini API calls.

Agent Flow

The core reasoning loop is:

Understand
    ↓
Observe
    ↓
Plan
    ↓
Act
    ↓
Verify
    ↓
Respond

The important safety constraint is:

Observe state before taking action

The agent therefore does not blindly execute hardware commands based only on the user's natural-language request.

Example Demonstration
Initial State
Doors:
  front_door: unlocked
  back_door: locked

Windows:
  bedroom_window: closed
  living_room_window: closed

Lights:
  bedroom: on
  living_room: off
User Command
I'm going to bed, secure the house.
Agent Reasoning
1. Intent detected: secure_house

2. Observe:
   - Front door is unlocked
   - Back door is locked
   - All windows are closed
   - Bedroom light is on

3. Plan:
   - Lock doors
   - Turn off lights

4. Execute actions

5. Verify:
   - All doors locked
   - All windows closed
   - All lights off
Final Response
House security was verified successfully.
Future Extensions

Possible future extensions include:

Real ASR integration
Real TTS integration
Additional smart-home devices
Per-device action parameters
More natural-language intents
Persistent hardware state
Real hardware/API integrations
More comprehensive agent evaluation tests

After saving it, run:

```powershell
python -m pytest