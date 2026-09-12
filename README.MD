# 🏠 Smart Home Agentic API

An agentic smart-home automation system built with **Python, FastAPI, Google Gemini, Pydantic, and Streamlit**.

The system accepts natural-language commands such as:

> "I'm going to bed, secure the house."

The AI agent interprets the user's intent, creates a plan, observes the current state of the home, reasons about what actions are required, executes only the necessary actions, verifies the resulting state, and returns a natural-language response.

---

# 🌐 Live Demo

### 🚀 Live Smart Home Agent

https://smart-home-agentic-api-fxxsg8dybpftepyeouyirt.streamlit.app/

The live application supports:

- 🎤 Voice commands
- ⌨️ Text commands
- 🧠 AI-powered command interpretation
- 🏠 Mock smart-home hardware
- 🔊 Text-to-speech responses
- 🔄 State verification

---

# 🔗 Backend

### FastAPI Backend

https://smart-home-agentic-api-xpov.onrender.com

### Interactive API Documentation

https://smart-home-agentic-api-xpov.onrender.com/docs

### GitHub Repository

https://github.com/Priya-tech07/smart-home-agentic-api

---

# 📌 Project Overview

This project demonstrates an **agentic AI architecture for smart-home automation**.

Instead of directly mapping every natural-language command to a hard-coded action, the AI agent follows a reasoning loop:

```text
Understand
    ↓
Plan
    ↓
Observe
    ↓
Reason
    ↓
Act
    ↓
Verify
    ↓
Respond
```

For example, when the user says:

```text
"I'm going to bed, secure the house."
```

the agent can determine that it should:

1. Understand the user's intent.
2. Create a plan for securing the house.
3. Check the current door status.
4. Check the current window status.
5. Check the current light status.
6. Determine which devices require changes.
7. Close open windows.
8. Lock unlocked doors.
9. Turn off lights that are currently on.
10. Verify the resulting device state.
11. Return a natural-language response.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │        User         │
                         │    Voice / Text     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │        ASR          │
                         │ Gemini Transcription│
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Streamlit       │
                         │    Web Interface    │
                         └──────────┬──────────┘
                                    │ HTTP
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │  /api/v1/command    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    AI Agent / LLM   │
                         │       Gemini        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Agentic Reasoning │
                         │        Loop         │
                         │                     │
                         │ Understand → Plan   │
                         │ Observe → Reason    │
                         │ Act → Verify        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                ┌─────────────────────────────────────┐
                │          Smart Home Tools           │
                │                                     │
                │ get_door_status()                   │
                │ get_window_status()                 │
                │ get_light_status()                  │
                │ close_windows()                     │
                │ lock_doors()                        │
                │ turn_off_lights()                   │
                └────────────────┬────────────────────┘
                                 │
                                 ▼
                         ┌─────────────────────┐
                         │   Mock Home State   │
                         │                     │
                         │ Doors               │
                         │ Windows             │
                         │ Lights              │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       Verify        │
                         │  Final Device State │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Agent Response    │
                         │       + TTS         │
                         └─────────────────────┘
```

---

# 🧠 Agentic Reasoning Loop

The core of the application is an agentic reasoning loop.

## 1. Understand

The agent interprets the natural-language command.

Example:

```text
"I'm going to bed, secure the house."
```

The agent identifies the user's intent as securing the home.

## 2. Plan

The agent determines which operations may be required to achieve the requested goal.

Example:

```text
Check doors
Check windows
Check lights
Close open windows
Lock unlocked doors
Turn off lights that are on
Verify final state
```

## 3. Observe

Before performing an action, the agent evaluates the current state using status tools.

Available status tools:

```text
get_door_status
get_window_status
get_light_status
```

This prevents the agent from making decisions based on assumptions.

## 4. Reason

The agent compares the requested goal with the observed state.

Example:

```text
Front door: unlocked
Back door: locked

Bedroom window: open
Living room window: closed

Bedroom light: on
Living room light: off
```

The agent determines which devices actually require changes.

## 5. Act

The agent executes only the required actions.

Example:

```python
close_windows(["bedroom_window"])

lock_doors(["front_door"])

turn_off_lights(["bedroom"])
```

Already-correct devices do not need unnecessary actions.

## 6. Verify

After executing actions, the agent checks the device state again.

The agent verifies:

```text
Required doors are locked
Required windows are closed
Required lights are off
```

An action is not considered successful simply because the tool call completed.

## 7. Respond

The agent returns a natural-language response.

Example:

```text
The house is secured. I closed the bedroom window,
locked the front door, and turned off the bedroom light.
```

---

# 🏠 Mock Smart-Home Hardware

This project uses **simulated smart-home hardware** for demonstration purposes.

The mock environment contains:

```text
Doors:
- front_door
- back_door

Windows:
- bedroom_window
- living_room_window

Lights:
- bedroom
- living_room
```

The home state is stored in:

```text
app/hardware/state.py
```

Example initial state:

```python
home_state = {
    "doors": {
        "front_door": "unlocked",
        "back_door": "locked"
    },
    "windows": {
        "bedroom_window": "open",
        "living_room_window": "closed"
    },
    "lights": {
        "bedroom": "on",
        "living_room": "off"
    }
}
```

The mock hardware layer provides a safe environment for testing agent behavior without requiring physical IoT devices.

---

# 🔧 Hardware Tools

The agent has access to six smart-home tools.

## Status Tools

### `get_door_status`

Returns the current state of all doors.

Possible states:

```text
locked
unlocked
```

### `get_window_status`

Returns the current state of all windows.

Possible states:

```text
open
closed
```

### `get_light_status`

Returns the current state of all lights.

Possible states:

```text
on
off
```

## Action Tools

### `close_windows`

Closes the specified windows.

Example:

```python
close_windows(["bedroom_window"])
```

### `lock_doors`

Locks the specified doors.

Example:

```python
lock_doors(["front_door"])
```

### `turn_off_lights`

Turns off the specified lights.

Example:

```python
turn_off_lights(["bedroom"])
```

---

# 🔐 Strict JSON Tool Schemas

The hardware tools use structured inputs and validation.

Action tools accept arrays containing specific device names.

Example:

```json
{
  "doors": [
    "front_door"
  ]
}
```

The tool schemas enforce:

- Valid input structure
- Known device names
- At least one device
- Unique device names
- No unexpected properties

The schemas use:

```text
additionalProperties: false
```

This prevents the agent from sending unexpected parameters to hardware tools.

---

# 🛡️ Safety and Verification

The system follows several safety principles.

## Status Before Action

The agent must evaluate the relevant device status before triggering an action.

```text
Status Tool
     ↓
   Reason
     ↓
Action Tool
```

This allows the agent to make state-aware decisions.

## Avoid Unnecessary Actions

If a device is already in the requested state, the agent does not need to modify it.

Example:

```text
Back door = locked
```

The agent does not need to lock it again.

## Verify After Action

After an action is executed, the agent checks the resulting state.

```text
Action
  ↓
Status Check
  ↓
Verification
```

## Unknown State

The agent should not assume that a device is safe when its state cannot be determined.

## Tool Failures

If a hardware operation fails, the failure should not be reported as a successful action.

The user should receive an appropriate failure message.

---

# 🚀 REST API

The main REST API endpoint is:

```text
POST /api/v1/command
```

## Request

```json
{
  "command": "I'm heading to bed, secure the house."
}
```

## Response

```json
{
  "success": true,
  "message": "The house has been secured."
}
```

---

# 📡 Example API Request

Using `curl`:

```bash
curl -X POST "https://smart-home-agentic-api-xpov.onrender.com/api/v1/command" \
  -H "Content-Type: application/json" \
  -d "{\"command\":\"I'm heading to bed, secure the house.\"}"
```

---

# 📖 Interactive API Documentation

FastAPI automatically provides Swagger UI.

Open:

https://smart-home-agentic-api-xpov.onrender.com/docs

Swagger UI allows you to:

- View the API endpoint
- Inspect request models
- Inspect response models
- Send test commands
- Test the deployed API directly
- Understand the API schema

---

# 🎤 Voice Command Flow

The application supports voice interaction.

The complete flow is:

```text
User speaks
    ↓
Microphone
    ↓
Gemini Speech-to-Text
    ↓
Natural-language transcript
    ↓
FastAPI
    ↓
Gemini Agent
    ↓
Agentic Reasoning Loop
    ↓
Hardware Tools
    ↓
Verification
    ↓
Agent Response
    ↓
Text-to-Speech
```

The application uses Gemini's transcription model:

```text
gemini-3.5-transcribe
```

The voice interface allows users to interact with the smart-home system without manually typing commands.

---

# ⌨️ Text Command Flow

Users can also enter commands directly through the Streamlit interface.

Example:

```text
Turn off the bedroom lights and lock the front door.
```

The command is sent to:

```text
POST /api/v1/command
```

The agent then follows:

```text
Understand
    ↓
Plan
    ↓
Observe
    ↓
Reason
    ↓
Act
    ↓
Verify
    ↓
Respond
```

---

# 🧪 Example Commands

Try commands such as:

```text
I'm going to bed, secure the house.
```

```text
Lock the front door.
```

```text
Turn off the bedroom lights.
```

```text
Close the bedroom window.
```

```text
Secure the house before I leave.
```

```text
Lock all unlocked doors and turn off any lights that are on.
```

```text
Close all open windows.
```

```text
Turn off the bedroom light.
```

The agent determines which hardware tools are required based on the user's command and the current home state.

---

# 📁 Project Structure

```text
smart-home-agentic-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── agent.py
│   ├── streamlit_app.py
│   │
│   └── hardware/
│       ├── __init__.py
│       ├── state.py
│       └── tools.py
│
├── tests/
│   ├── test_hardware.py
│   ├── test_agent.py
│   ├── test_agent_command.py
│   └── test_gemini.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.MD
```

---

# ⚙️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| FastAPI | REST API |
| Uvicorn | ASGI server |
| Pydantic | Data validation and schemas |
| Google Gemini | AI reasoning and transcription |
| Streamlit | Web interface |
| gTTS | Text-to-speech |
| streamlit-mic-recorder | Voice input |
| Requests | HTTP communication |
| Pytest | Automated testing |
| GitHub Actions | Continuous integration |
| Render | FastAPI deployment |
| Streamlit Community Cloud | Frontend deployment |

---

# 🔑 Environment Variables

For local development, create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
FASTAPI_URL=http://127.0.0.1:8000/api/v1/command
```

For Streamlit Cloud, configure the secrets as:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
FASTAPI_URL = "https://smart-home-agentic-api-xpov.onrender.com/api/v1/command"
```

> **Never commit your actual API key to GitHub.**

Make sure `.env` is included in `.gitignore`.

---

# 💻 Local Setup

## 1. Clone the Repository

```bash
git clone https://github.com/Priya-tech07/smart-home-agentic-api.git
```

Move into the project directory:

```bash
cd smart-home-agentic-api
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create:

```text
.env
```

Add:

```env
GEMINI_API_KEY=your_gemini_api_key
FASTAPI_URL=http://127.0.0.1:8000/api/v1/command
```

---

# ▶️ Run the FastAPI Backend

Start the API using:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# ▶️ Run the Streamlit Frontend

Open another terminal and run:

```bash
streamlit run app/streamlit_app.py
```

The Streamlit interface will open in your browser.

The frontend communicates with the FastAPI backend through the configured `FASTAPI_URL`.

---

# 🧪 Running Tests

Run the complete test suite:

```bash
pytest -q
```

The project includes tests for:

- Hardware state
- Hardware tools
- Agent behavior
- Command processing
- Gemini configuration

The Gemini API connection can be tested separately so that CI does not require a private API key or unnecessarily consume API quota.

---

# 🔄 Continuous Integration

GitHub Actions automatically runs the test suite whenever changes are pushed.

The CI workflow follows:

```text
Git Push
   ↓
GitHub Actions
   ↓
Install Dependencies
   ↓
Run Pytest
   ↓
All Tests Pass
```

This helps ensure that changes do not break existing functionality.

---

# ☁️ Deployment

## FastAPI Backend

The FastAPI backend is deployed using **Render**.

### Backend

https://smart-home-agentic-api-xpov.onrender.com

### API Documentation

https://smart-home-agentic-api-xpov.onrender.com/docs

## Streamlit Frontend

The Streamlit frontend is deployed using **Streamlit Community Cloud**.

### 🌐 Live Website

https://smart-home-agentic-api-fxxsg8dybpftepyeouyirt.streamlit.app/

---

# 🎯 Key Design Decisions

## Agent Before Hardware

Natural-language commands are interpreted by the AI agent before any hardware operation is performed.

This separates:

```text
User Intent
     ↓
AI Reasoning
     ↓
Hardware Action
```

rather than directly connecting natural language to hardware.

## Observe Before Act

The agent checks the current device state before executing an action.

This prevents unnecessary operations and supports safer automation.

## Parameterized Hardware Tools

Hardware actions receive specific device lists instead of blindly modifying every device.

For example:

```python
lock_doors(["front_door"])
```

instead of:

```python
lock_all_doors()
```

This allows the agent to make state-aware decisions.

## Verification

The system verifies the resulting state after actions.

The preferred workflow is:

```text
Observe → Act → Verify
```

rather than:

```text
Act → Assume Success
```

---

# 🧩 Example Agent Execution

For the command:

```text
I'm going to bed, secure the house.
```

The agent may observe:

```text
Front door: unlocked
Back door: locked

Bedroom window: open
Living room window: closed

Bedroom light: on
Living room light: off
```

The agent reasons that only these actions are required:

```text
Close bedroom window
Lock front door
Turn off bedroom light
```

The agent then executes:

```python
close_windows(["bedroom_window"])
lock_doors(["front_door"])
turn_off_lights(["bedroom"])
```

After executing the actions, it verifies the final state:

```text
Front door: locked
Back door: locked

Bedroom window: closed
Living room window: closed

Bedroom light: off
Living room light: off
```

The user then receives a natural-language confirmation:

```text
The house is secured. I closed the bedroom window,
locked the front door, and turned off the bedroom light.
```

---

# 📌 API Design

## Endpoint

```text
POST /api/v1/command
```

## Input Schema

```json
{
  "command": "string"
}
```

## Output Schema

```json
{
  "success": true,
  "message": "string"
}
```

## API Flow

```text
Client
  ↓
POST /api/v1/command
  ↓
Pydantic Validation
  ↓
AI Agent
  ↓
Reasoning Loop
  ↓
Hardware Tools
  ↓
Verification
  ↓
JSON Response
```

---

# 🚧 Scope

This project currently uses **mock smart-home hardware** for demonstration and development.

The hardware layer can later be replaced with real integrations such as:

- Smart locks
- Smart lights
- Window sensors
- Door sensors
- Home automation platforms
- IoT devices
- MQTT-based devices
- REST-based smart-home APIs

The agent architecture can remain largely the same while replacing the mock tool implementations with real hardware APIs.

The project is therefore designed to demonstrate the **agentic architecture and decision-making workflow** rather than control physical hardware directly.

---

# 👤 Author

**Priya**

### GitHub

https://github.com/Priya-tech07/smart-home-agentic-api

---

# 🔗 Project Links

| Resource | Link |
|---|---|
| 🌐 Live Website | https://smart-home-agentic-api-fxxsg8dybpftepyeouyirt.streamlit.app/ |
| 🚀 FastAPI Backend | https://smart-home-agentic-api-xpov.onrender.com |
| 📖 API Documentation | https://smart-home-agentic-api-xpov.onrender.com/docs |
| 💻 GitHub Repository | https://github.com/Priya-tech07/smart-home-agentic-api |

---

# ⭐ If You Find This Project Useful

Feel free to ⭐ star the repository and explore the agentic smart-home architecture.

---

# 📋 Quick Start

```bash
git clone https://github.com/Priya-tech07/smart-home-agentic-api.git

cd smart-home-agentic-api

python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key
FASTAPI_URL=http://127.0.0.1:8000/api/v1/command
```

Run FastAPI:

```bash
uvicorn app.main:app --reload
```

Run Streamlit in another terminal:

```bash
streamlit run app/streamlit_app.py
```

Run tests:

```bash
pytest -q
```

---

# 🏁 End-to-End Architecture

The complete application works as:

```text
                  USER
                   │
          ┌────────┴────────┐
          │                 │
       VOICE               TEXT
          │                 │
          ▼                 │
        ASR                 │
          │                 │
          └────────┬────────┘
                   ▼
              STREAMLIT
                   │
                   ▼
               FASTAPI
                   │
                   ▼
             GEMINI AGENT
                   │
                   ▼
              UNDERSTAND
                   │
                   ▼
                  PLAN
                   │
                   ▼
                OBSERVE
                   │
                   ▼
                 REASON
                   │
                   ▼
                  ACT
                   │
                   ▼
            HARDWARE TOOLS
                   │
                   ▼
           MOCK HOME STATE
                   │
                   ▼
                VERIFY
                   │
                   ▼
             AGENT RESPONSE
                   │
                   ▼
                  TTS
                   │
                   ▼
                  USER
```

This architecture demonstrates how an AI agent can reason over device state, choose appropriate tools, execute actions, verify outcomes, and communicate the result to the user.
