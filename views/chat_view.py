"""Saju chatbot page — 1:1 코칭."""

import base64
import os
from html import escape
from pathlib import Path

import streamlit as st

from core.chat_engine import build_fallback_answer, run_chat, run_chat_stream
from core.llm_client import LLMConfigurationError
from core.prompt_templates import MODE_GREETING
from ui.styles import apply_custom_styles
from utils.helpers import init_session_state
from utils.logger import get_logger


logger = get_logger(__name__)

# ── 이미지 경로
_IMG_DIR = Path(__file__).parent.parent / "img" / "proj1_report"


@st.cache_data
def _img_b64(filename: str) -> str:
    """이미지 파일을 base64로 인코딩하여 반환."""
    with open(_IMG_DIR / filename, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ── 오행 색상 (Figma 디자인 토큰)
_ELEMENT_COLORS = {
    "wood": "#9db26c", "fire": "#ff8985",
    "earth": "#f4d383", "metal": "#ccc6bd", "water": "#146f8a",
}
_ELEMENT_KR = {"wood": "木", "fire": "火", "earth": "土", "metal": "金", "water": "水"}
_ELEMENT_SUB_KR = {"wood": "목", "fire": "화", "earth": "토", "metal": "금", "water": "수"}
_ELEM_ORDER = ["wood", "fire", "earth", "metal", "water"]

# ── 모드 메타 (key, 이모지, 제목, 설명)
MODE_META = [
    ("business", "🏢", "비즈니스", "계약 및 협상 테이블에서 승리하는 타이밍을 알려드립니다."),
    ("love",     "❤️", "연애",    "고백, 데이트 등 실패 없는 실전 행동 지침을 코칭합니다."),
    ("wealth",   "💰", "재물",    "돈이 들어오는 길목을 지키는 돈줄 전략을 공개합니다."),
    ("study",    "📚", "학업",    "시험 합격 및 성적 향상을 위한 맞춤형 처방을 드립니다."),
    ("health",   "💪", "건강",    "에너지 고갈을 막고 최상의 컨디션을 유지하는 법을 조언합니다."),
]


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
def _inject_css() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {
            background: #e9eff0 !important;
        }
        [data-testid="stAppViewContainer"] > .main { background: #E9F1F6; }
        [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none; }
        [data-testid="stBottomBlockContainer"] {
            background: #e9eff0 !important;
        }
        [data-testid="stBottomBlockContainer"] [data-testid="stChatInput"] {
            background: #a5bec3 !important;
            border-radius: 10px !important;
            border: none !important;
        }
        [data-testid="stBottomBlockContainer"] [data-testid="stChatInput"] > div,
        [data-testid="stBottomBlockContainer"] .st-emotion-cache-mjrxj2 {
            background: #a5bec3 !important;
            border-radius: 10px !important;
            border: none !important;
        }
        [data-testid="stBottomBlockContainer"] textarea {
            background: #a5bec3 !important;
            color: #ffffff !important;
        }
        [data-testid="stBottomBlockContainer"] textarea::placeholder {
            color: rgba(255, 255, 255, 0.72) !important;
        }

        /* ── 로고 / 타이틀 */
        .chat-logo-row {
            color: #3b82a0; font-size: 0.76rem; font-weight: 700;
            letter-spacing: 1.5px; text-transform: uppercase;
            margin-bottom: 0.2rem;
        }
        .chat-page-title {
            font-size: 1.8rem; font-weight: 800;
            color: #1a2035; margin: 0 0 0.8rem;
        }
        .st-key-header_actions {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            justify-content: flex-end;
            width: 100%;
            padding-top: 64px;
            margin-bottom: -2px;
            gap: 6px;
        }
        .st-key-header_actions [data-testid="stButton"] {
            width: auto;
            margin-left: auto;
        }
        .st-key-header_actions .st-key-home_action,
        .st-key-header_actions .st-key-reset_chat_action {
            display: flex !important;
            justify-content: flex-end !important;
            width: fit-content !important;
            margin-left: auto !important;
        }
        .st-key-header_actions [data-testid="stButton"] button {
            width: auto !important;
            min-height: 0 !important;
            height: 32px !important;
            padding: 0 16px !important;
            border-radius: 999px !important;
            background: #07314a !important;
            border: none !important;
            color: #ffffff !important;
            font-size: 12px !important;
            font-weight: 700 !important;
            line-height: 1 !important;
        }
        .st-key-header_actions [data-testid="stButton"] button p {
            color: #ffffff !important;
            font-size: 12px !important;
            line-height: 1 !important;
            margin: 0 !important;
        }

        /* ── 프로필 카드 */
        .cp-card {
            background: #ffffff; border-radius: 12px;
            padding: 1.4rem 1.2rem;
            min-height: 315px;
            box-sizing: border-box;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }
        .cp-avatar {
            width: 60px; height: 60px; border-radius: 50%;
            background: #dde3ec;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.5rem; margin-bottom: 0.5rem;
        }
        .cp-name  { font-size: 1rem; font-weight: 700; color: #1a2035; margin: 0 0 0.1rem; }
        .cp-birth { font-size: 0.72rem; color: #8a94a6; margin-bottom: 0.7rem; }
        .cp-grid  { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.3rem 0.5rem; }
        .cp-label { font-size: 0.68rem; color: #8a94a6; display: block; }
        .cp-value { font-size: 0.88rem; font-weight: 700; color: #1a2035; }

        /* ── Balance Status 카드 */
        .bs-card {
            background: #ffffff; border-radius: 12px;
            padding: 1.1rem 1.4rem 0.8rem;
            min-height: 315px;
            box-sizing: border-box;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }
        .bs-title { font-size: 0.77rem; color: #8a94a6; font-weight: 600; margin-bottom: 0.6rem; }
        .bs-bar-wrap { display: flex; align-items: flex-end; gap: 0.5rem; height: 245px; }
        .bs-bar-col  {
            display: flex; flex-direction: column; align-items: center;
            flex: 1; height: 100%; justify-content: flex-end;
        }
        .bs-bar  {
            width: 100%; border-radius: 16px 16px 0 0; min-height: 20px;
            display: flex; align-items: flex-start; justify-content: center;
        }
        .bs-pct  { font-size: 0.72rem; font-weight: 700; color: #fff; padding-top: 5px; }
        .bs-lbl  { font-size: 0.8rem; color: #072f48; margin-top: 0.3rem; font-weight: 700; }
        .bs-lbl2 { font-size: 0.7rem; color: #7a7a7a; }

        /* ── 한줄 요약 배너 */
        .chat-summary-bar {
            background: #ffffff; border-radius: 12px;
            padding: 1rem 1.8rem; text-align: center;
            margin: 0.8rem 0 0;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }
        .chat-summary-bar p {
            font-size: 1rem; font-weight: 700;
            color: #072f48; margin: 0; line-height: 1.5;
        }

        /* ── 모드 질문 배너 */
        .mode-question-banner {
            background: #146f8a; border-radius: 16px;
            padding: 1.1rem 2.5rem; text-align: center;
            margin: 1rem 0 0.6rem;
        }
        .mode-question-banner p {
            font-size: 1.05rem; font-weight: 700; color: #e9eff0; margin: 0;
        }

        /* ── 모드 카드 */
        .mode-card {
            background: #ffffff; border-radius: 24px;
            padding: 1.2rem 1rem; text-align: left;
            border: 2.5px solid transparent;
            height: 200px;
            box-sizing: border-box;
            cursor: pointer;
            transition: box-shadow 0.15s ease, transform 0.15s ease;
        }
        .mode-card:hover {
            box-shadow: 0 4px 18px rgba(0,0,0,0.10);
            transform: translateY(-2px);
        }
        .mode-card-selected {
            background: #ffffff; border-radius: 24px;
            padding: 1.2rem 1rem; text-align: left;
            border: 3px solid #1A374D;
            height: 200px;
            box-sizing: border-box;
            cursor: pointer;
            box-shadow: 0 4px 18px rgba(26,55,77,0.15);
            transition: box-shadow 0.15s ease, transform 0.15s ease;
        }
        .mode-card-selected:hover {
            box-shadow: 0 6px 22px rgba(26,55,77,0.20);
            transform: translateY(-2px);
        }
        .mode-card-icon {
            background: #f5f7fa; border-radius: 14px;
            width: 58px; height: 58px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.8rem; margin-bottom: 0.7rem;
        }
        .mode-card-title { font-size: 0.95rem; font-weight: 700; color: #292929; margin: 0 0 0.35rem; }
        .mode-card-desc  { font-size: 0.75rem; color: #6e6e6e; line-height: 1.55; margin: 0; }

        .chat-thread-row {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin: 18px 0;
            width: 100%;
        }
        .chat-thread-row-ai {
            justify-content: flex-start;
        }
        .chat-thread-row-user {
            justify-content: flex-end;
        }
        .chat-avatar {
            width: 52px;
            height: 52px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex: 0 0 52px;
            color: #ffffff;
            font-size: 1.55rem;
            font-weight: 700;
        }
        .chat-avatar-ai {
            background: #146f8a;
        }
        .chat-avatar-user {
            background: #d7d7d7;
            color: #ffffff;
            order: 2;
        }
        .chat-bubble {
            background: #ffffff;
            border: none;
            border-radius: 8px;
            color: #111111;
            line-height: 1.75;
            padding: 18px 22px;
            font-size: 0.92rem;
            box-shadow: none;
            white-space: normal;
        }
        .chat-bubble-ai {
            max-width: 760px;
        }
        .chat-bubble-user {
            max-width: 560px;
            order: 1;
        }
        .chat-bubble strong {
            color: #111111;
            display: none;
        }
        .stream-chat-row {
            margin: 18px 0;
        }
        .stream-chat-row [data-testid="stHorizontalBlock"] {
            align-items: flex-start;
            gap: 12px;
        }
        .stream-chat-row [data-testid="column"]:first-child {
            flex: 0 0 52px !important;
            width: 52px !important;
            min-width: 52px !important;
        }
        .stream-chat-avatar {
            width: 52px;
            height: 52px;
            border-radius: 8px;
            background: #146f8a;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.55rem;
            font-weight: 700;
        }
        .st-key-stream_ai_bubble {
            background: #ffffff;
            border: none;
            border-radius: 8px;
            color: #111111;
            line-height: 1.75;
            padding: 18px 22px;
            max-width: 760px;
            box-shadow: none;
        }
        .st-key-stream_ai_bubble [data-testid="stMarkdownContainer"],
        .st-key-stream_ai_bubble [data-testid="stMarkdownContainer"] * {
            color: #111111 !important;
            line-height: 1.75;
        }
        .st-key-stream_ai_bubble [data-testid="stMarkdownContainer"] p:first-child {
            margin-top: 0;
        }
        .st-key-stream_ai_bubble [data-testid="stMarkdownContainer"] p:last-child {
            margin-bottom: 0;
        }

        .st-key-mode_picker [data-testid="stButton"] {
            height: 200px;
        }
        .st-key-mode_picker [data-testid="stButton"] button {
            width: 100% !important;
            height: 200px !important;
            min-height: 200px !important;
            display: block !important;
            padding: 1.2rem 1rem !important;
            border-radius: 24px !important;
            border: 2.5px solid transparent !important;
            background: #ffffff !important;
            color: #292929 !important;
            box-shadow: none !important;
            text-align: left !important;
            white-space: normal !important;
            transition: box-shadow 0.15s ease, transform 0.15s ease !important;
        }
        .st-key-mode_picker [data-testid="stButton"] button:hover {
            box-shadow: 0 4px 18px rgba(0,0,0,0.10) !important;
            transform: translateY(-2px);
            border-color: transparent !important;
            color: #292929 !important;
        }
        .st-key-mode_picker [data-testid="stButton"] button:focus {
            border-color: #1A374D !important;
            box-shadow: 0 4px 18px rgba(26,55,77,0.15) !important;
            color: #292929 !important;
        }
        .st-key-mode_picker [data-testid="stButton"] button [data-testid="stMarkdownContainer"] {
            width: 100%;
        }
        .st-key-mode_picker [data-testid="stButton"] button p {
            color: inherit !important;
            line-height: 1.55 !important;
            margin: 0 !important;
            text-align: left !important;
        }
        .st-key-mode_picker [data-testid="stButton"] button p:first-child {
            font-size: 1.8rem !important;
            line-height: 1 !important;
            margin-bottom: 0.8rem !important;
        }
        .st-key-mode_picker [data-testid="stButton"] button strong {
            display: block;
            font-size: 0.95rem;
            line-height: 1.35;
            margin-bottom: 0.35rem;
        }

        /* ── 스피너 텍스트 색상 */
        [data-testid="stSpinner"] p,
        [data-testid="stSpinner"] span,
        div[data-testid="stSpinner"] > div > span {
            color: #111111 !important;
        }

        @media (max-width: 768px) {
            .bs-bar-wrap { height: 120px; }
            .mode-card, .mode-card-selected { height: 160px; }
            .st-key-mode_picker [data-testid="stButton"],
            .st-key-mode_picker [data-testid="stButton"] button {
                height: 160px !important;
                min-height: 160px !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# 렌더링 헬퍼
# ---------------------------------------------------------------------------
def _pct(val: int, total: int) -> int:
    return round(val / total * 100) if total > 0 else 0


def _render_top_panel(saju, profile: dict) -> None:
    name       = escape(profile.get("name") or "익명")
    birth_date = escape(profile.get("birth_date", ""))
    birth_time = escape(profile.get("birth_time", ""))
    cal        = "양력" if profile.get("calendar_type") == "solar" else "음력"
    day_master = escape(saju.day_master or "미정")
    yongsin    = escape(saju.yongsin   or "미정")
    gisin      = escape(saju.gisin     or "미정")
    yr  = escape(saju.year_pillar  or "-")
    mo  = escape(saju.month_pillar or "-")
    day = escape(saju.day_pillar   or "-")
    hr  = escape(saju.hour_pillar  or "-")

    col_profile, col_balance = st.columns([1, 3])

    with col_profile:
        st.markdown(
            f"""
            <div class="cp-card">
              <div class="cp-avatar">🧑</div>
              <p class="cp-name">{name}</p>
              <p class="cp-birth">{birth_date} {birth_time} | {cal}</p>
              <div class="cp-grid">
                <div><span class="cp-label">일간</span><span class="cp-value">{day_master}</span></div>
                <div><span class="cp-label">용신</span><span class="cp-value">{yongsin}</span></div>
                <div><span class="cp-label">기신</span><span class="cp-value">{gisin}</span></div>
                <div><span class="cp-label">연</span><span class="cp-value">{yr}</span></div>
                <div><span class="cp-label">월</span><span class="cp-value">{mo}</span></div>
                <div></div>
                <div><span class="cp-label">일</span><span class="cp-value">{day}</span></div>
                <div><span class="cp-label">시</span><span class="cp-value">{hr}</span></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_balance:
        elems = saju.five_elements
        total = sum(elems.values()) or 1
        bars_html = ""
        for en in _ELEM_ORDER:
            color    = _ELEMENT_COLORS[en]
            pct      = _pct(elems.get(en, 0), total)
            height   = max(int(pct * 1.6), 20)
            gradient = (
                f"linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.4) 100%), "
                f"linear-gradient(to left, {color}, {color})"
            )
            bars_html += f"""
            <div class="bs-bar-col">
                <div class="bs-bar" style="background:{gradient};height:{height}px;">
                    <span class="bs-pct">{pct}%</span>
                </div>
                <div class="bs-lbl">{_ELEMENT_KR[en]}</div>
                <div class="bs-lbl2">{_ELEMENT_SUB_KR[en]}</div>
            </div>"""

        st.markdown(
            f"""
            <div class="bs-card">
              <div class="bs-title">Balance Status</div>
              <div class="bs-bar-wrap">{bars_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_summary_bar(saju) -> None:
    summary = getattr(saju, "summary", None)
    if not summary:
        return
    st.markdown(
        f'<div class="chat-summary-bar"><p>"{escape(summary)}"</p></div>',
        unsafe_allow_html=True,
    )


def _render_chat_bubble(role: str, content: str) -> None:
    safe_content = escape(content).replace("\n", "<br>")
    if role == "user":
        st.markdown(
            f"""
            <div class="chat-thread-row chat-thread-row-user">
                <div class="chat-avatar chat-avatar-user">◇</div>
                <div class="chat-bubble chat-bubble-user">{safe_content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f"""
        <div class="chat-thread-row chat-thread-row-ai">
            <div class="chat-avatar chat-avatar-ai">♧</div>
            <div class="chat-bubble chat-bubble-ai">{safe_content}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _write_streaming_ai_bubble(chunks) -> str:
    st.markdown('<div class="stream-chat-row">', unsafe_allow_html=True)
    icon_col, bubble_col = st.columns([0.07, 0.93])
    with icon_col:
        st.markdown('<div class="stream-chat-avatar">♧</div>', unsafe_allow_html=True)
    with bubble_col:
        with st.container(key="stream_ai_bubble"):
            answer = st.write_stream(chunks)
    st.markdown("</div>", unsafe_allow_html=True)
    return answer


def _get_mode_meta(mode_key: str) -> tuple[str, str, str, str] | None:
    return next((item for item in MODE_META if item[0] == mode_key), None)


def _select_mode(mode_key: str) -> None:
    st.session_state["current_mode"] = mode_key
    st.session_state["prev_mode"] = mode_key
    st.rerun()


def _render_mode_section() -> str | None:
    mode_placeholder = st.empty()
    current_mode = st.session_state.get("current_mode")

    if not _get_mode_meta(current_mode):
        st.session_state["current_mode"] = None
        current_mode = None

    with mode_placeholder.container():
        st.markdown(
            '<div class="mode-question-banner">'
            '<p>오늘 집중적인 코칭이 필요한 영역이 무엇인가요?</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        with st.container(key="mode_picker"):
            cols = st.columns(len(MODE_META))
            for idx, (mode_key, icon, title, desc) in enumerate(MODE_META):
                with cols[idx]:
                    if st.button(
                        f"{icon}\n\n**{title}**\n\n{desc}",
                        key=f"mode_btn_{mode_key}",
                        use_container_width=True,
                    ):
                        mode_placeholder.empty()
                        _select_mode(mode_key)

    return current_mode

def render_chat_page() -> None:
    # ===========================================================================
    # 메인
    # ===========================================================================
    init_session_state()
    apply_custom_styles()
    _inject_css()

    saju    = st.session_state.get("user_saju")
    profile = st.session_state.get("birth_profile", {})

    if saju is None:
        st.warning("아직 입력된 정보가 없습니다. 첫페이지에서 기본 정보를 먼저 입력해주세요.")
        if st.button("첫페이지로 돌아가기", type="primary"):
            st.session_state["active_view"] = "home"
            st.rerun()
        st.stop()

    if "prev_mode" not in st.session_state:
        st.session_state["prev_mode"] = None

    # ── 헤더
    header_l, header_r = st.columns([3, 1])
    with header_l:
        logo_b64  = _img_b64("로고.png")
        st.markdown(
            f'<img src="data:image/png;base64,{logo_b64}" style="height:82px; margin-bottom:8px; display:block;" />'
            '<div style="font-size:32px; font-weight:800; color:#000000; line-height:1.2; margin-bottom:0;">1:1코칭</div>',
            unsafe_allow_html=True,
        )
    with header_r:
        with st.container(key="header_actions"):
            if st.button("← 처음으로", key="home_action"):
                st.session_state["active_view"] = "home"
                st.rerun()
            if st.button("대화 초기화", key="reset_chat_action"):
                st.session_state["chat_history"] = []
                st.session_state["current_mode"] = None
                st.session_state["prev_mode"] = None
                st.rerun()

    st.markdown("<div style='height:0'></div>", unsafe_allow_html=True)

    # ── 프로필 + Balance Status
    _render_top_panel(saju, profile)

    # ── 한줄 요약
    _render_summary_bar(saju)

    # ── 모드 선택
    selected_mode = _render_mode_section()
    if selected_mode is None:
        st.stop()

    stream_enabled = os.getenv("STREAM_ENABLED", "true").lower() == "true"

    # ── 현재 모드 안내 말풍선 (chat_history에 누적하지 않음)
    mode_greeting = MODE_GREETING.get(selected_mode, "")
    if mode_greeting:
        _render_chat_bubble("assistant", mode_greeting)

    # ── 채팅 히스토리
    for message in st.session_state["chat_history"]:
        _render_chat_bubble(message["role"], message["content"])

    # ── 입력창
    user_input = st.chat_input("궁금한 사주 상담 내용을 입력하세요")

    if user_input:
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        _render_chat_bubble("user", user_input)

        try:
            with st.spinner("사주 컨텍스트를 바탕으로 답변을 생성하는 중입니다..."):
                prior_history = st.session_state["chat_history"][:-1]
                if stream_enabled:
                    chunks = run_chat_stream(saju, prior_history, user_input, selected_mode)
                    answer = _write_streaming_ai_bubble(chunks)
                else:
                    answer = run_chat(saju, prior_history, user_input, selected_mode)
                    _render_chat_bubble("assistant", answer)
            st.session_state["chat_history"].append({"role": "assistant", "content": answer})
            st.session_state["consultation_count"] += 1
        except LLMConfigurationError as error:
            logger.warning("LLM 설정 오류: %s", error)
            answer = build_fallback_answer(saju, user_input)
            st.warning(".env에 OPENAI_API_KEY를 설정하면 실제 AI 상담을 사용할 수 있습니다. 지금은 로컬 요약 답변을 표시합니다.")
            _render_chat_bubble("assistant", answer)
            st.session_state["chat_history"].append({"role": "assistant", "content": answer})
        except Exception as error:
            logger.error("채팅 응답 실패: %s", error)
            answer = build_fallback_answer(saju, user_input)
            st.warning("AI API 연결이 잠시 실패해서 로컬 요약 답변을 표시합니다.")
            _render_chat_bubble("assistant", answer)
            st.session_state["chat_history"].append({"role": "assistant", "content": answer})
