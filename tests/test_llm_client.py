"""Tests for LLM client behavior."""

import pytest

from core.llm_client import LLMConfigurationError, _get_client


def test_get_client_requires_api_key(monkeypatch):
    """Client creation fails clearly when API key is missing."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(LLMConfigurationError):
        _get_client()
