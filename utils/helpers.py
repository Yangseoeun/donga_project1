"""Shared helper functions for Streamlit pages."""

import streamlit as st

from core.schemas import SajuResult


def init_session_state() -> None:
    """
    Initialize Streamlit session state once.

    Returns:
        None
    """
    defaults = {
        "chat_history": [],
        "user_saju": None,
        "current_mode": "general",
        "consultation_count": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_demo_saju_context() -> SajuResult:
    """
    Return a temporary saju context until backend A calculation is connected.

    Returns:
        SajuResult: Demo saju result.
    """
    return SajuResult(
        year_pillar="갑자",
        month_pillar="병인",
        day_pillar="무오",
        hour_pillar="경신",
        five_elements={"wood": 2, "fire": 1, "earth": 2, "metal": 2, "water": 1},
        day_master="무토(戊土)",
        yongsin="목(木)",
        gisin="금(金)",
        summary="안정감과 실행력이 강하며, 새로운 성장 자극을 받을 때 균형이 좋아지는 타입입니다.",
    )
