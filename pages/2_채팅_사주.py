"""Saju chatbot page."""

import os

import streamlit as st

from core.chat_engine import build_fallback_answer, run_chat, run_chat_stream
from core.llm_client import LLMConfigurationError
from ui.components import render_chat_message, render_context_preview
from ui.styles import apply_custom_styles
from utils.helpers import init_session_state
from utils.logger import get_logger


logger = get_logger(__name__)

MODE_OPTIONS = [
    ("business", "1. 비즈니스"),
    ("love", "2. 연애"),
    ("wealth", "3. 재물"),
    ("study", "4. 학업"),
    ("health", "5. 건강"),
]


st.set_page_config(
    page_title="채팅 사주",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)
init_session_state()
apply_custom_styles()

st.title("채팅 사주")

saju = st.session_state.get("user_saju")
profile = st.session_state.get("birth_profile", {})

if saju is None:
    st.warning("아직 입력된 정보가 없습니다. 첫페이지에서 기본 정보를 먼저 입력해주세요.")
    if st.button("첫페이지로 돌아가기", type="primary"):
        st.switch_page("app.py")
    st.stop()

top_left, top_right = st.columns([2, 1])
with top_left:
    st.caption(
        f"현재 사주 컨텍스트: {saju.day_master or '미정'} / "
        f"용신 {saju.yongsin or '미정'} / "
        f"입력자 {profile.get('name') or '익명'}"
    )
with top_right:
    if st.button("대화 초기화", use_container_width=True):
        st.session_state["chat_history"] = []
        st.rerun()

render_context_preview(saju)

st.markdown(
    """
    <div class="choice-panel">
        <p>오늘 어떤 게 가장 고민인가요?</p>
        <p class="choice-hint">(선택지 노출: 1. 비즈니스 / 2. 연애 / 3. 재물 / 4. 학업 / 5. 건강)</p>
    </div>
    """,
    unsafe_allow_html=True,
)

selected_mode = st.session_state.get("current_mode", "business")
mode_cols = st.columns(len(MODE_OPTIONS))
for index, (mode_key, mode_label) in enumerate(MODE_OPTIONS):
    with mode_cols[index]:
        if st.button(
            mode_label,
            type="primary" if selected_mode == mode_key else "secondary",
            use_container_width=True,
        ):
            st.session_state["current_mode"] = mode_key
            selected_mode = mode_key

stream_enabled = os.getenv("STREAM_ENABLED", "true").lower() == "true"

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
                chunks = run_chat_stream(saju, prior_history, user_input, selected_mode)
                answer = st.write_stream(chunks)
            else:
                answer = run_chat(saju, prior_history, user_input, selected_mode)
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
