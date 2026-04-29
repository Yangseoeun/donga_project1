"""General saju report page."""

import streamlit as st

from core.result_builder import build_general_report
from ui.components import render_pillars, render_report_card, render_saju_summary
from ui.styles import apply_custom_styles
from utils.helpers import init_session_state


st.set_page_config(
    page_title="일반 사주",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)
init_session_state()
apply_custom_styles()

st.title("일반 사주")

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
        f"{profile.get('name') or '익명'} / "
        f"{profile.get('birth_date')} {profile.get('birth_time')} / "
        f"{profile.get('calendar_type', 'solar')}"
    )
with top_right:
    if st.button("채팅모드로 상담하기", use_container_width=True):
        st.switch_page("pages/2_채팅_사주.py")

report = build_general_report(saju)

render_pillars(saju)

st.divider()

render_saju_summary(saju)

st.subheader("오행 분포")
st.bar_chart(saju.five_elements)

st.subheader("오늘의 상담")
render_report_card(report)
