"""LLM client wrapper for all OpenAI chat calls."""

import os
from collections.abc import Generator
from typing import Any

from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential


load_dotenv()


class LLMConfigurationError(RuntimeError):
    """Raised when required LLM settings are missing."""


def _get_client() -> Any:
    """
    Lazily initialize the OpenAI client.

    Returns:
        Any: OpenAI client instance.

    Raises:
        LLMConfigurationError: If OPENAI_API_KEY is not configured.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise LLMConfigurationError("OPENAI_API_KEY가 설정되지 않았습니다.")

    from openai import OpenAI

    return OpenAI(api_key=api_key)


def _get_model() -> str:
    """
    Return the configured chat model.

    Returns:
        str: Model name.
    """
    return os.getenv("OPENAI_MODEL", "gpt-4o")


@retry(wait=wait_exponential(multiplier=1, min=1, max=8), stop=stop_after_attempt(3))
def _create_completion(
    messages: list[dict[str, str]],
    stream: bool,
    temperature: float,
) -> Any:
    """
    Create a chat completion with retry.

    Args:
        messages (list[dict[str, str]]): OpenAI-compatible messages.
        stream (bool): Whether to stream the response.
        temperature (float): Sampling temperature.

    Returns:
        Any: OpenAI response object or stream iterator.
    """
    client = _get_client()
    return client.chat.completions.create(
        model=_get_model(),
        messages=messages,
        stream=stream,
        temperature=temperature,
    )


def _stream_text(response: Any) -> Generator[str, None, None]:
    """
    Yield text chunks from a streaming response.

    Args:
        response (Any): OpenAI streaming response.

    Yields:
        str: Delta text chunk.
    """
    for chunk in response:
        delta = chunk.choices[0].delta
        content = getattr(delta, "content", None)
        if content:
            yield content


def get_chat_response(
    messages: list[dict[str, str]],
    stream: bool = True,
    temperature: float = 0.7,
) -> str | Generator[str, None, None]:
    """
    Get a chat response from the configured LLM.

    Args:
        messages (list[dict[str, str]]): OpenAI-compatible messages.
        stream (bool): Whether to return a token generator.
        temperature (float): Sampling temperature.

    Returns:
        str | Generator[str, None, None]: Full text or stream generator.
    """
    response = _create_completion(messages, stream=stream, temperature=temperature)
    if stream:
        return _stream_text(response)

    content = response.choices[0].message.content
    return content or ""
