"""Tests for chat engine behavior."""

from core.chat_engine import build_chat_messages, build_fallback_answer, trim_history
from utils.helpers import get_demo_saju_context


def test_trim_history_keeps_latest_messages(monkeypatch):
    """History trimming keeps only the latest configured turns."""
    monkeypatch.setenv("MAX_HISTORY_TURNS", "1")
    history = [
        {"role": "user", "content": "1"},
        {"role": "assistant", "content": "2"},
        {"role": "user", "content": "3"},
    ]

    assert trim_history(history) == [
        {"role": "assistant", "content": "2"},
        {"role": "user", "content": "3"},
    ]


def test_build_chat_messages_includes_saju_context():
    """Built messages include system saju context and latest user input."""
    messages = build_chat_messages(
        get_demo_saju_context(),
        [],
        "올해 흐름은 어때요?",
        "general",
    )

    assert messages[0]["role"] == "system"
    assert "무토" in messages[0]["content"]
    assert messages[-1] == {"role": "user", "content": "올해 흐름은 어때요?"}


def test_build_fallback_answer_uses_saju_context():
    """Fallback answer includes saju context without calling the LLM."""
    answer = build_fallback_answer(get_demo_saju_context(), "재물운은요?")

    assert "재물운은요?" in answer
    assert "무토" in answer
