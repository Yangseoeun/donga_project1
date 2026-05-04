"""Streamlit entrypoint — My Energy-Up Coach 랜딩 페이지."""

from datetime import date, datetime, time

import streamlit as st

from core.saju_calculator import calculate_saju
from ui.components import (
    render_guide_section,
    render_input_complete_banner,
    render_landing_hero,
)
from ui.styles import apply_landing_styles
from utils.helpers import init_session_state


st.set_page_config(
    page_title="My Energy-Up Coach",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_session_state()
apply_landing_styles()

profile = st.session_state.get("birth_profile", {})

default_name = profile.get("name", "")
default_gender = profile.get("gender", "female")
default_calendar_type = profile.get("calendar_type", "solar")
default_birth_date = date(1997, 1, 1)
default_birth_time = time(9, 0)

if profile.get("birth_date"):
    try:
        default_birth_date = datetime.strptime(profile["birth_date"], "%Y. %m. %d").date()
    except ValueError:
        pass

if profile.get("birth_time"):
    try:
        default_birth_time = datetime.strptime(profile["birth_time"], "%H:%M").time()
    except ValueError:
        pass

# ── 히어로 섹션
render_landing_hero()

# ── 입력 폼 (중앙 정렬: 좌우 여백 컬럼으로 구현)
_, form_col, _ = st.columns([0.75, 2.5, 0.75])
with form_col:
    with st.form("birth_profile_form"):
        st.markdown(
            '<p class="form-desc">생년월일을 입력한 뒤 원하는 방식으로 상담을 시작하세요.</p>',
            unsafe_allow_html=True,
        )

        name = st.text_input("이름", value=default_name, placeholder="이름")

        col_a, col_b = st.columns(2)
        with col_a:
            gender = st.selectbox(
                "성별",
                ["female", "male"],
                index=["female", "male"].index(default_gender) if default_gender in ["female", "male"] else 0,
                format_func={
                    "female": "여성",
                    "male": "남성",
                }.get,
            )
        with col_b:
            calendar_type = st.radio(
                "달력",
                ["solar", "lunar"],
                index=["solar", "lunar"].index(default_calendar_type) if default_calendar_type in ["solar", "lunar"] else 0,
                format_func={"solar": "양력", "lunar": "음력"}.get,
                horizontal=True,
            )

        col_c, col_d = st.columns(2)
        with col_c:
           birth_date = st.date_input("생년월일", value=default_birth_date, min_value=date(1900, 1, 1), max_value=date.today())
        with col_d:
            birth_time = st.time_input("출생 시간", value=default_birth_time)

        submitted = st.form_submit_button(
            "정보 입력 완료",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        birth_dt = datetime.combine(birth_date, birth_time)
        st.session_state["user_saju"] = calculate_saju(birth_dt, gender)
        st.session_state["birth_profile"] = {
            "name": name,
            "gender": gender,
            "birth_date": birth_date.strftime("%Y. %m. %d"),
            "birth_time": birth_time.strftime("%H:%M"),
            "calendar_type": calendar_type,
        }
        st.session_state["chat_history"] = []
        st.session_state["consultation_count"] += 1

# ── 입력 완료 배너 + 가이드 섹션 (saju 계산 완료 후 표시)
saju    = st.session_state.get("user_saju")
profile = st.session_state.get("birth_profile", {})

if saju is not None:
    _, banner_col, _ = st.columns([0.75, 2.5, 0.75])
    with banner_col:
        render_input_complete_banner(profile, saju)

    _, guide_col, _ = st.columns([0.75, 2.5, 0.75])
    with guide_col:
        render_guide_section()
