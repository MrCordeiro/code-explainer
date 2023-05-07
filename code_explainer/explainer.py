import os
from functools import partial

import openai
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def send_question(question: str) -> dict:
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a developer."},
            {"role": "user", "content": question},
        ],
    )


def _parse_ai_answer(response: dict) -> str:
    return response["choices"][0]["message"]["content"]


def _get_code_info(question: str, code: str) -> str:
    resp = send_question(f"{question}\n\n{code}")
    return _parse_ai_answer(resp)


get_code_language = partial(
    _get_code_info,
    question="Can you explain to me in what language this code is written?",
)


get_code_explanation = partial(
    _get_code_info,
    question="Can you explain to me what this code base does in a few words?",
)
