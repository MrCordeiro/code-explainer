"""Explains code snippets using a LLM."""

import os
from functools import partial

import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def send_question(question: str) -> dict:
    """Send a question to the OpenAI API and return the response."""
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a developer."},
            {"role": "user", "content": question},
        ],
    )  # type: ignore


def _parse_ai_answer(response: dict) -> str:
    """Parse the response from the OpenAI API and return just the answer."""
    return response["choices"][0]["message"]["content"]


def _get_code_info(question: str, code: str) -> str:
    """
    Send a question and a code snippet to the OpenAI API and return the answer.
    """
    resp = send_question(f"{question}\n\n{code}")
    return _parse_ai_answer(resp)


get_code_language = partial(
    _get_code_info,
    question="Can you explain to me in what language this code is written?",
)


get_code_explanation = partial(
    _get_code_info,
    question="Can you explain to me what this code does in a few words?",
)
