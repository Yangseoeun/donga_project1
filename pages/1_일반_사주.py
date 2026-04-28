"""General saju report page."""

from datetime import date, datetime, time

import streamlit as st

from core.result_builder import build_general_report
from core.saju_calculator import calculate_saju
from ui.components import render_pillars, render_report_card, render_saju_summary
from ui.styles import apply_custom_styles
from utils.helpers import get_demo_saju_context, init_session_state


st.set_page_config(page_title="일반 사주", page_icon="📋", layout="wide")
init_session_state()
apply_custom_styles()

st.title("일반 사주")

with st.sidebar:
    st.header("입력")
    name = st.text_input("이름", placeholder="선택 입력")
    gender = st.selectbox("성별", ["unknown", "female", "male"], format_func={
        "unknown": "선택 안 함",
        "female": "여성",
        "male": "남성",
    }.get)
    birth_date = st.date_input("생년월일", value=date(1997, 1, 1))
    birth_time = st.time_input("출생 시간", value=time(9, 0))
    calendar_type = st.radio("달력", ["solar", "lunar"], format_func={
        "solar": "양력",
        "lunar": "음력",
    }.get)
    submitted = st.button("사주 보기", type="primary", use_container_width=True)

if submitted:
    birth_dt = datetime.combine(birth_date, birth_time)
    st.session_state["user_saju"] = calculate_saju(birth_dt, gender)
    st.session_state["birth_profile"] = {
        "name": name,
        "gender": gender,
        "birth_date": birth_date.isoformat(),
        "birth_time": birth_time.strftime("%H:%M"),
        "calendar_type": calendar_type,
    }
    st.session_state["consultation_count"] += 1
    st.success("입력값을 바탕으로 사주 컨텍스트를 생성했습니다.")

saju = st.session_state.get("user_saju") or get_demo_saju_context()
report = build_general_report(saju)

render_pillars(saju)

st.divider()

render_saju_summary(saju)

st.subheader("오행 분포")
st.bar_chart(saju.five_elements)

st.subheader("오늘의 상담")
render_report_card(report)

st.info(
    f"입력값 확인: {name or '익명'} / {gender} / {birth_date} {birth_time} / {calendar_type}. "
    "현재는 개인정보를 저장하지 않고 세션에서만 사용합니다."
)

st.page_link("pages/2_채팅_사주.py", label="이 사주로 AI 채팅 이어가기", icon="💬")
