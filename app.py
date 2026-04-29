"""Streamlit entrypoint for the AI saju consultation app."""

from datetime import date, datetime, time

import streamlit as st

from core.saju_calculator import calculate_saju
from ui.styles import apply_custom_styles
from utils.helpers import init_session_state


st.set_page_config(
    page_title="AI 사주 상담",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_session_state()
apply_custom_styles()

st.title("AI 사주 상담")
st.caption("먼저 기본 정보를 입력한 뒤 원하는 방식으로 상담을 시작하세요.")

left, right = st.columns([1.2, 1])

with left:
    st.subheader("기본 정보 입력")
    with st.form("birth_profile_form"):
        name = st.text_input("이름", placeholder="선택 입력")

        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox(
                "성별",
                ["unknown", "female", "male"],
                format_func={
                    "unknown": "선택 안 함",
                    "female": "여성",
                    "male": "남성",
                }.get,
            )
            birth_date = st.date_input("생년월일", value=date(1997, 1, 1))
        with col2:
            calendar_type = st.radio(
                "달력",
                ["solar", "lunar"],
                format_func={"solar": "양력", "lunar": "음력"}.get,
                horizontal=True,
            )
            birth_time = st.time_input("출생 시간", value=time(9, 0))

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
            "birth_date": birth_date.isoformat(),
            "birth_time": birth_time.strftime("%H:%M"),
            "calendar_type": calendar_type,
        }
        st.session_state["chat_history"] = []
        st.session_state["consultation_count"] += 1
        st.success("입력이 완료되었습니다. 아래에서 상담 방식을 선택하세요.")

with right:
    st.subheader("상담 시작")
    saju = st.session_state.get("user_saju")
    profile = st.session_state.get("birth_profile", {})

    if saju is None:
        st.info("정보를 입력하면 일반모드와 채팅모드를 선택할 수 있습니다.")
    else:
        st.markdown(
            f"""
            <div class="saju-card compact-card">
                <h4>현재 입력 정보</h4>
                <p>이름: {profile.get("name") or "익명"}</p>
                <p>생년월일시: {profile.get("birth_date")} {profile.get("birth_time")}</p>
                <p>일간: {saju.day_master or "미정"}</p>
                <p>용신: {saju.yongsin or "미정"}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        mode_col1, mode_col2 = st.columns(2)
        with mode_col1:
            if st.button("일반모드로 보기", type="primary", use_container_width=True):
                st.switch_page("pages/1_일반_사주.py")
        with mode_col2:
            if st.button("채팅모드로 상담하기", use_container_width=True):
                st.switch_page("pages/2_채팅_사주.py")
