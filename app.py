"""Streamlit entrypoint for the AI saju consultation app."""

import streamlit as st

from ui.components import (
    render_connection_flow,
    render_intro_panel,
    render_quick_links,
    render_status_card,
)
from ui.styles import apply_custom_styles
from utils.helpers import init_session_state


st.set_page_config(
    page_title="AI 사주 상담",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
apply_custom_styles()

st.title("AI 사주 상담")

left, right = st.columns([2, 1])

with left:
    render_intro_panel()
    st.info(
        "일반 사주 페이지에서 입력한 계산 결과가 `st.session_state['user_saju']`에 저장되고, "
        "채팅 사주 페이지는 같은 값을 읽어 AI 상담 컨텍스트로 사용합니다."
    )

with right:
    render_status_card(st.session_state.get("user_saju"))

st.divider()
st.subheader("바로가기")
render_quick_links()

st.divider()
st.subheader("연결 흐름")
render_connection_flow()
