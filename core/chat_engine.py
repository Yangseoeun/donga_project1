"""Chat orchestration for saju-aware LLM consultation."""

import os
from collections.abc import Generator

from core import llm_client
from core.prompt_templates import build_messages, build_system_prompt
from core.schemas import ConsultationMode, SajuResult


def get_max_history_messages() -> int:
    """
    Return maximum retained history messages.

    Returns:
        int: Maximum number of messages to include.
    """
    turns = int(os.getenv("MAX_HISTORY_TURNS", "10"))
    return max(turns * 2, 0)


def trim_history(history: list[dict[str, str]]) -> list[dict[str, str]]:
    """
    Keep only the latest valid chat history messages.

    Args:
        history (list[dict[str, str]]): Full chat history.

    Returns:
        list[dict[str, str]]: Trimmed history.
    """
    valid_history = [
        message
        for message in history
        if message.get("role") in {"user", "assistant"} and message.get("content")
    ]
    max_messages = get_max_history_messages()
    if max_messages == 0:
        return []
    return valid_history[-max_messages:]


def build_chat_messages(
    saju: SajuResult,
    history: list[dict[str, str]],
    user_input: str,
    mode: ConsultationMode = "general",
) -> list[dict[str, str]]:
    """
    Compose final messages for the LLM.

    Args:
        saju (SajuResult): Calculated saju result.
        history (list[dict[str, str]]): Prior chat messages.
        user_input (str): Latest user question.
        mode (ConsultationMode): Consultation mode.

    Returns:
        list[dict[str, str]]: OpenAI-compatible messages.
    """
    system_prompt = build_system_prompt(saju=saju, mode=mode)
    return build_messages(system_prompt, trim_history(history), user_input)


def run_chat(
    saju: SajuResult,
    history: list[dict[str, str]],
    user_input: str,
    mode: ConsultationMode = "general",
) -> str:
    """
    Run a non-streaming saju chat turn.

    Args:
        saju (SajuResult): Calculated saju result.
        history (list[dict[str, str]]): Prior chat messages.
        user_input (str): Latest user question.
        mode (ConsultationMode): Consultation mode.

    Returns:
        str: Assistant answer.
    """
    messages = build_chat_messages(saju, history, user_input, mode)
    response = llm_client.get_chat_response(messages, stream=False)
    return str(response)


def run_chat_stream(
    saju: SajuResult,
    history: list[dict[str, str]],
    user_input: str,
    mode: ConsultationMode = "general",
) -> Generator[str, None, None]:
    """
    Run a streaming saju chat turn.

    Args:
        saju (SajuResult): Calculated saju result.
        history (list[dict[str, str]]): Prior chat messages.
        user_input (str): Latest user question.
        mode (ConsultationMode): Consultation mode.

    Yields:
        str: Assistant answer chunks.
    """
    messages = build_chat_messages(saju, history, user_input, mode)
    response = llm_client.get_chat_response(messages, stream=True)
    yield from response


def build_fallback_answer(saju: SajuResult, user_input: str) -> str:
    """
    Build a local answer when an LLM API key is not configured.

    Args:
        saju (SajuResult): Calculated saju result.
        user_input (str): Latest user question.

    Returns:
        str: Local fallback answer.
    """
    has_api_key = bool(os.getenv("OPENAI_API_KEY"))
    reason = (
        "AI API 연결이 실패해서 로컬 요약으로 답변합니다."
        if has_api_key
        else "현재 API 키가 없어 로컬 요약으로 답변합니다."
    )
    next_step = (
        "잠시 후 다시 시도하거나 네트워크 연결 상태를 확인해주세요."
        if has_api_key
        else "실제 LLM 상담을 사용하려면 `.env`에 `OPENAI_API_KEY`를 설정해주세요."
    )

    return (
        f"{reason}\n\n"
        f"질문: {user_input}\n\n"
        f"당신의 일간은 {saju.day_master or '미정'}이고, "
        f"용신 후보는 {saju.yongsin or '미정'}입니다. "
        f"{saju.summary or '사주 계산 결과를 먼저 생성하면 더 구체적인 상담이 가능합니다.'} "
        f"{next_step}"
    )
