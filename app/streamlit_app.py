import io
import os

import requests
import streamlit as st
from dotenv import load_dotenv
from google import genai
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder


# -------------------------------------------------------------------
# Environment configuration
# -------------------------------------------------------------------

load_dotenv()


def get_secret(name: str):
    """
    Read configuration from Streamlit Secrets first,
    then fall back to environment variables.

    This supports both Streamlit Cloud and local development.
    """

    try:
        value = st.secrets.get(name)
        if value:
            return value
    except Exception:
        pass

    return os.getenv(name)


GEMINI_API_KEY = get_secret("GEMINI_API_KEY")

FASTAPI_URL = get_secret("FASTAPI_URL")

if not FASTAPI_URL:
    FASTAPI_URL = (
        "http://127.0.0.1:8000/api/v1/command"
    )

if not GEMINI_API_KEY:
    st.error(
        "GEMINI_API_KEY is not configured. "
        "Add it to your environment variables or Streamlit Secrets."
    )
    st.stop()


gemini_client = genai.Client(
    api_key=GEMINI_API_KEY
)


# -------------------------------------------------------------------
# Streamlit page
# -------------------------------------------------------------------

st.set_page_config(
    page_title="Smart Home Agent",
    page_icon="🏠",
)

st.title("🏠 Smart Home Agent")
st.write("Speak a command or type one below.")


# -------------------------------------------------------------------
# Speech-to-text
# -------------------------------------------------------------------

def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Convert recorded audio into text using Gemini's
    dedicated transcription model.
    """

    audio_file = gemini_client.files.upload(
        file=io.BytesIO(audio_bytes),
        config={
            "mime_type": "audio/wav",
        },
    )

    interaction = gemini_client.interactions.create(
        model="gemini-3.5-transcribe",
        input=[
            {
                "type": "audio",
                "uri": audio_file.uri,
                "mime_type": audio_file.mime_type,
            }
        ],
    )

    transcript = (
        interaction.output_text or ""
    ).strip()

    if not transcript:
        raise ValueError(
            "Gemini did not return a transcription."
        )

    return transcript


# -------------------------------------------------------------------
# FastAPI command
# -------------------------------------------------------------------

def send_command(command: str) -> str:
    """
    Send the natural-language command to the
    deployed FastAPI agent.
    """

    response = requests.post(
        FASTAPI_URL,
        json={
            "command": command,
        },
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "message",
        "No response was returned by the smart home agent.",
    )


# -------------------------------------------------------------------
# Text-to-speech
# -------------------------------------------------------------------

def speak_response(text: str):
    """
    Convert the agent response to speech.
    """

    audio_buffer = io.BytesIO()

    tts = gTTS(
        text=text,
        lang="en",
    )

    tts.write_to_fp(audio_buffer)

    audio_buffer.seek(0)

    st.audio(
        audio_buffer,
        format="audio/mp3",
        autoplay=True,
    )


# -------------------------------------------------------------------
# Voice command interface
# -------------------------------------------------------------------

st.subheader("🎤 Voice Command")

audio = mic_recorder(
    start_prompt="Start Recording",
    stop_prompt="Stop Recording",
    just_once=True,
    use_container_width=True,
    format="wav",
)

if audio:
    audio_bytes = audio["bytes"]

    try:
        with st.spinner("Transcribing..."):
            transcript = transcribe_audio(
                audio_bytes
            )

        st.write("**You said:**")
        st.info(transcript)

        with st.spinner(
            "Smart home agent is thinking..."
        ):
            message = send_command(transcript)

        st.write("**Agent:**")
        st.success(message)

        speak_response(message)

    except Exception as exc:
        st.error(
            "Speech-to-text or command processing "
            f"failed: {exc}"
        )


# -------------------------------------------------------------------
# Text command interface
# -------------------------------------------------------------------

st.divider()

st.subheader("⌨️ Text Command")

text_command = st.text_input(
    "Enter a smart-home command",
    placeholder=(
        "I'm heading to bed, secure the house"
    ),
)

if st.button("Send Command"):
    if not text_command.strip():
        st.warning(
            "Please enter a smart-home command."
        )
    else:
        try:
            with st.spinner(
                "Smart home agent is thinking..."
            ):
                message = send_command(
                    text_command.strip()
                )

            st.write("**Agent:**")
            st.success(message)

            speak_response(message)

        except Exception as exc:
            st.error(
                f"Command processing failed: {exc}"
            )