import json
import os

from dotenv import load_dotenv
from google import genai

from app.hardware.tools import (
    get_door_status,
    get_window_status,
    get_light_status,
    close_windows,
    lock_doors,
    turn_off_lights,
)


# -------------------------------------------------------------------
# Environment and Gemini setup
# -------------------------------------------------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Do not fail during module import when running tests or CI.
# The Gemini client is created only when an API key is available.
client = None

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.8-flash"


# -------------------------------------------------------------------
# Strict tool declarations
# -------------------------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "name": "get_door_status",
        "description": (
            "Returns the actual current lock status of all doors. "
            "Use this when the user asks about door state or before "
            "changing door state."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_window_status",
        "description": (
            "Returns the actual current open or closed status of all "
            "windows. Use this when the user asks about window state "
            "or before changing window state."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_light_status",
        "description": (
            "Returns the actual current on or off status of all lights. "
            "Use this when the user asks about light state or before "
            "changing light state."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "close_windows",
        "description": (
            "Closes the specified windows. "
            "Only use this after checking the current window status."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "windows": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "bedroom_window",
                            "living_room_window",
                        ],
                    },
                    "minItems": 1,
                    "uniqueItems": True,
                }
            },
            "required": ["windows"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "lock_doors",
        "description": (
            "Locks the specified doors. "
            "Only use this after checking the current door status."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "doors": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "front_door",
                            "back_door",
                        ],
                    },
                    "minItems": 1,
                    "uniqueItems": True,
                }
            },
            "required": ["doors"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "turn_off_lights",
        "description": (
            "Turns off the specified lights. "
            "Only use this after checking the current light status."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "lights": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "bedroom",
                            "living_room",
                        ],
                    },
                    "minItems": 1,
                    "uniqueItems": True,
                }
            },
            "required": ["lights"],
            "additionalProperties": False,
        },
    },
]


# -------------------------------------------------------------------
# Tool execution
# -------------------------------------------------------------------

def execute_tool(name: str, arguments: dict | None = None):
    """
    Execute a hardware tool requested by Gemini.
    """

    arguments = arguments or {}

    tools = {
        "get_door_status": get_door_status,
        "get_window_status": get_window_status,
        "get_light_status": get_light_status,
        "close_windows": close_windows,
        "lock_doors": lock_doors,
        "turn_off_lights": turn_off_lights,
    }

    if name not in tools:
        raise ValueError(f"Unknown tool: {name}")

    result = tools[name](**arguments)

    if hasattr(result, "model_dump"):
        return result.model_dump()

    return result


# -------------------------------------------------------------------
# Safety mapping
# -------------------------------------------------------------------

STATUS_TOOLS = {
    "get_door_status",
    "get_window_status",
    "get_light_status",
}

ACTION_TO_STATUS = {
    "close_windows": "get_window_status",
    "lock_doors": "get_door_status",
    "turn_off_lights": "get_light_status",
}


# -------------------------------------------------------------------
# LLM agent
# -------------------------------------------------------------------

def run_agent(command: str):
    """
    Run the LLM-driven smart-home agent.

    Gemini:
    - understands the natural-language request
    - decides which tools are relevant
    - reasons about the returned hardware state
    - decides which actions are necessary
    - produces the final natural-language response

    Python:
    - executes hardware tools
    - enforces status-before-action safety
    - prevents unsupported tool calls
    """

    if client is None:
        return {
            "success": False,
            "message": (
                "Gemini API key is not configured. "
                "Please configure GEMINI_API_KEY."
            ),
            "actions": [],
        }

    system_instruction = """
You are an autonomous smart-home voice assistant.

Understand the user's natural-language request and determine what
smart-home operations are appropriate.

Available capabilities:

- Check door status
- Check window status
- Check light status
- Close windows
- Lock doors
- Turn off lights

IMPORTANT SAFETY RULES:

1. Never assume the current state of a device.
2. When the user asks about a device's state, call the relevant
   status tool.
3. Before performing an action, call the corresponding status tool.
4. Use the observed state to determine whether an action is
   necessary.
5. Do not perform unnecessary actions.
6. After changing a device state, verify the relevant state again.
7. Never claim an action succeeded if the hardware tool failed.
8. Never invent devices.
9. Never invent device states.
10. Do not use hard-coded user phrases.
11. Interpret the meaning and intent of the user's natural language.
12. Multiple tools may be required for one request.
13. Keep the response focused on what the user actually asked about.

IMPORTANT RESPONSE RULES:

The hardware tool results are the authoritative source of truth.

Never contradict a status-tool result.

Do not mention devices that are irrelevant to the user's request
unless they are necessary to explain the result.

For example, if the user asks specifically about the front door,
do not unnecessarily discuss the back door.

If the user asks whether any windows are open, report the windows
that are actually open.

If the user asks to lock the front door if it is unlocked:

1. Check the door status.
2. Determine the front door's actual state.
3. Lock it only if it is unlocked.
4. Verify the result.
5. Respond naturally about the front door.

Do not produce database-style responses.

Respond like a natural voice assistant: concise, conversational,
and directly relevant to what the user asked.

Do not mention internal tools, function calls, Gemini, schemas,
Python, or implementation details in the final response.
"""

    print()
    print("=" * 70)
    print("SMART HOME AGENT")
    print("=" * 70)
    print("User command:", command)

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=command,
        tools=TOOLS,
        system_instruction=system_instruction,
        generation_config={
            "thinking_level": "low",
        },
    )

    executed_actions = []
    observed_status = set()

    max_iterations = 12

    # ---------------------------------------------------------------
    # Agentic reasoning loop
    # ---------------------------------------------------------------

    for iteration in range(max_iterations):

        print()
        print(f"--- Agent iteration {iteration + 1} ---")

        function_calls = [
            step
            for step in interaction.steps
            if step.type == "function_call"
        ]

        # Gemini has finished reasoning.
        if not function_calls:

            final_message = interaction.output_text

            print("Agent response:", final_message)

            return {
                "success": True,
                "message": final_message,
                "actions": executed_actions,
            }

        function_results = []

        for call in function_calls:

            tool_name = call.name
            arguments = call.arguments or {}

            print("Gemini requested:", tool_name)
            print("Arguments:", arguments)

            # -------------------------------------------------------
            # Safety enforcement
            # -------------------------------------------------------

            if tool_name in ACTION_TO_STATUS:

                required_status_tool = ACTION_TO_STATUS[tool_name]

                if required_status_tool not in observed_status:

                    error_message = (
                        f"Action '{tool_name}' was prevented because "
                        f"'{required_status_tool}' has not been checked yet."
                    )

                    print("SAFETY:", error_message)

                    result = {
                        "success": False,
                        "error": error_message,
                    }

                    function_results.append(
                        {
                            "type": "function_result",
                            "name": tool_name,
                            "call_id": call.id,
                            "result": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result),
                                }
                            ],
                        }
                    )

                    continue

            # -------------------------------------------------------
            # Execute hardware tool
            # -------------------------------------------------------

            try:

                result = execute_tool(
                    tool_name,
                    arguments,
                )

                print("Tool result:", result)

                if tool_name in STATUS_TOOLS:
                    observed_status.add(tool_name)

                if tool_name in ACTION_TO_STATUS:
                    executed_actions.append(tool_name)

                function_results.append(
                    {
                        "type": "function_result",
                        "name": tool_name,
                        "call_id": call.id,
                        "result": [
                            {
                                "type": "text",
                                "text": json.dumps(result),
                            }
                        ],
                    }
                )

            except Exception as exc:

                error_message = str(exc)

                print("Tool error:", error_message)

                result = {
                    "success": False,
                    "error": error_message,
                }

                function_results.append(
                    {
                        "type": "function_result",
                        "name": tool_name,
                        "call_id": call.id,
                        "result": [
                            {
                                "type": "text",
                                "text": json.dumps(result),
                            }
                        ],
                    }
                )

        # -----------------------------------------------------------
        # Send tool results back to Gemini
        # -----------------------------------------------------------

        interaction = client.interactions.create(
            model=MODEL_NAME,
            previous_interaction_id=interaction.id,
            input=function_results,
            tools=TOOLS,
            generation_config={
                "thinking_level": "low",
            },
        )

    return {
        "success": False,
        "message": (
            "The smart-home agent could not complete the request "
            "within the allowed reasoning steps."
        ),
        "actions": executed_actions,
    }


# -------------------------------------------------------------------
# API-facing command processor
# -------------------------------------------------------------------

def process_command(command: str):
    """
    Process an arbitrary natural-language command.

    No hard-coded intent classification is used.
    """

    if not command or not command.strip():

        return {
            "success": False,
            "intent": "unknown",
            "result": {
                "message": "Please provide a smart-home command."
            },
        }

    result = run_agent(command)

    return {
        "success": result["success"],
        "intent": "llm_agent",
        "result": result,
    }