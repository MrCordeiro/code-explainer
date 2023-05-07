"""Convert text to speech using the Eleven Labs API."""

import os
import time
from http import HTTPStatus

import httpx
from dotenv import load_dotenv
from httpx import Response

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
BASE_URL = "https://api.elevenlabs.io"
DEFAULT_VOICE = "Elli"
MAX_RETRIES = 10


def _get_id_from_name(response: Response, name: str) -> str:
    """Return the voice id from the voice name."""
    id_to_name = {
        item.get("name"): item.get("voice_id") for item in response.json()["voices"]
    }
    return id_to_name[name]


def _save_binary_to_mp3(content: bytes, filename: str) -> None:
    """Save the binary content to a mp3 file."""
    with open(filename, "wb") as mp3_file:
        mp3_file.write(content)


def list_available_names() -> list[str]:
    """Return a list of available voices names."""
    voices_response = httpx.get(
        f"{BASE_URL}/v1/voices", params={"xi-api-key": API_KEY}, timeout=5
    )
    # Ensure the DEFAULT_VOICE is the first one.
    return sorted(
        [voice.get("name") for voice in voices_response.json()["voices"]],
        key=lambda x: x != DEFAULT_VOICE,
    )


def convert_text_to_mp3(message: str, voice_name: str, mp3_filename: str) -> None:
    """Convert the text to speech and save it to a mp3 file."""
    voices_response = httpx.get(
        f"{BASE_URL}/v1/voices", params={"xi-api-key": API_KEY}, timeout=5
    )

    voice_id = _get_id_from_name(response=voices_response, name=voice_name)

    payload = {
        "text": message,
        "voice_settings": {"stability": 0.75, "similarity_boost": 0.75},
    }

    for _ in range(MAX_RETRIES):
        text_to_speech_response = httpx.post(
            f"{BASE_URL}/v1/text-to-speech/{voice_id}/stream",
            params={"voice_id": voice_id, "xi-api-key": API_KEY},
            json=payload,
            timeout=5,
        )
        if text_to_speech_response.status_code == HTTPStatus.OK:
            return _save_binary_to_mp3(
                content=text_to_speech_response.content, filename=mp3_filename
            )

        time.sleep(5)
        print("Trying again, the API maybe busy...")

    raise RuntimeError("The API is busy, please try again later.")
