"""Saju chatbot page."""

import os

import streamlit as st

from core.chat_engine import build_fallback_answer, run_chat, run_chat_stream
from core.llm_client import LLMConfigurationError
from ui.components import render_chat_message, render_context_preview
from ui.styles import apply_custom_styles
from utils.helpers import get_demo_saju_context, init_session_state
from utils.logger import get_logger


logger = get_logger(__name__)

st.set_page_config(page_title="채팅 사주", page_icon="💬", layout="wide")
init_session_state()
apply_custom_styles()

st.title("채팅 사주")

with st.sidebar:
    st.header("상담 설정")
    mode = st.selectbox(
        "상담 모드",
        ["general", "business", "love", "health"],
        format_func={
            "general": "일반",
            "business": "사업/커리어",
            "love": "연애/관계",
            "health": "건강/컨디션",
        }.get,
    )
    st.session_state["current_mode"] = mode
    stream_enabled = st.toggle(
        "스트리밍 응답",
        value=os.getenv("STREAM_ENABLED", "true").lower() == "true",
    )
    if st.button("대화 초기화", use_container_width=True):
        st.session_state["chat_history"] = []
        st.rerun()

saju = st.session_state.get("user_saju")
if saju is None:
    saju = get_demo_saju_context()
    st.warning("아직 계산된 사주가 없어 데모 컨텍스트로 채팅합니다. 일반 사주 페이지에서 먼저 계산하면 실제 입력값이 연결됩니다.")
    st.page_link("pages/1_일반_사주.py", label="일반 사주에서 계산하기", icon="📋")

profile = st.session_state.get("birth_profile", {})
st.caption(
    f"현재 사주 컨텍스트: {saju.day_master or '미정'} / 용신 {saju.yongsin or '미정'} "
    f"/ 입력자: {profile.get('name') or '익명'}"
)

render_context_preview(saju)

for message in st.session_state["chat_history"]:
    render_chat_message(message["role"], message["content"])

user_input = st.chat_input("궁금한 사주 상담 내용을 입력하세요")

if user_input:
    st.session_state["chat_history"].append({"role": "user", "content": user_input})
    render_chat_message("user", user_input)

    try:
        with st.spinner("사주 컨텍스트를 바탕으로 답변을 생성하는 중입니다..."):
            prior_history = st.session_state["chat_history"][:-1]
            if stream_enabled:
                chunks = run_chat_stream(saju, prior_history, user_input, mode)
                answer = st.write_stream(chunks)
            else:
                answer = run_chat(saju, prior_history, user_input, mode)
                render_chat_message("assistant", answer)
        st.session_state["chat_history"].append({"role": "assistant", "content": answer})
        st.session_state["consultation_count"] += 1
    except LLMConfigurationError as error:
        logger.warning("LLM 설정 오류: %s", error)
        answer = build_fallback_answer(saju, user_input)
        st.warning(".env에 OPENAI_API_KEY를 설정하면 실제 AI 상담을 사용할 수 있습니다. 지금은 로컬 요약 답변을 표시합니다.")
        render_chat_message("assistant", answer)
        st.session_state["chat_history"].append({"role": "assistant", "content": answer})
    except Exception as error:
        logger.error("채팅 응답 실패: %s", error)
        answer = build_fallback_answer(saju, user_input)
        st.warning("AI API 연결이 잠시 실패해서 로컬 요약 답변을 표시합니다.")
        render_chat_message("assistant", answer)
        st.session_state["chat_history"].append({"role": "assistant", "content": answer})
