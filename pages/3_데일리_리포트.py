# 백엔드 A 가 새로 만든 파일입니다.
"""데일리 리포트 페이지 — 이미지 디자인 기준 재구현."""

from html import escape

import streamlit as st

from core.daily_report_builder import build_daily_report
from core.result_builder import build_general_report
from ui.styles import apply_custom_styles
from utils.helpers import init_session_state

# ── 오행별 색상 팔레트 (Balance Status 차트용)
_ELEMENT_COLORS: dict[str, str] = {
    "wood":  "#6cbf8e",
    "fire":  "#e8837a",
    "earth": "#c4a96a",
    "metal": "#9eb5c8",
    "water": "#5fa8c8",
}
_ELEMENT_KR: dict[str, str] = {
    "wood": "木", "fire": "火", "earth": "土", "metal": "金", "water": "水",
}

# ── 운세 섹션 메타 (key, 아이콘 배경색, 아이콘 문자, 표시 레이블)
_FORTUNE_META = [
    ("총운",       "#6cbf8e", "✦", "총운"),
    ("재물운",     "#e8c46a", "💰", "재물운"),
    ("비즈니스운", "#7ab3d4", "🏢", "비즈니스(사업/직장)"),
    ("애정운",     "#e8837a", "♡",  "애정운(연애/인간관계)"),
    ("건강운",     "#a89fd8", "⊕",  "건강운"),
]

# ── 코칭 섹션 메타 (section_key, 아이콘 배경색, 아이콘, 제목, 필드목록)
_COACHING_META = [
    ("outfit",      "#7ab3d4", "👔", "의상 코칭",
     ["추천 스타일", "행운의 아이템", "주의 할 스타일"]),
    ("food",        "#6cbf8e", "🍵", "푸드 코칭",
     ["추천 식단",   "음료 페어링",   "주의 할 음식"]),
    ("environment", "#a89fd8", "🌿", "환경 코칭",
     ["행운의 공간", "에너지 방향",   "주의 할 장소"]),
    ("action",      "#e8c46a", "⚡", "행동 전략 코칭",
     ["커뮤니케이션", "네트워킹 전략"]),
]


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
def _inject_css() -> None:
    st.markdown(
        """
        <style>
        /* ── 전체 배경 */
        [data-testid="stAppViewContainer"] > .main {
            background: #f5f6f8;
        }
        [data-testid="stSidebar"], [data-testid="collapsedControl"] {
            display: none;
        }

        /* ── 로고 & 타이틀 */
        .dr-logo-row {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            color: #3b82a0;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }
        .dr-page-title {
            font-size: 1.85rem;
            font-weight: 800;
            color: #1a2035;
            margin: 0;
        }

        /* ── 상단 카드 (프로필 + Balance) */
        .top-panel {
            background: #ffffff;
            border-radius: 14px;
            padding: 1.6rem 1.8rem;
            margin-bottom: 1.1rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }
        .top-panel-inner {
            display: grid;
            grid-template-columns: 200px 1fr;
            gap: 2.2rem;
            align-items: start;
        }

        /* ── 프로필 */
        .profile-avatar {
            width: 68px; height: 68px;
            border-radius: 50%;
            background: #dde3ec;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.7rem;
            margin-bottom: 0.6rem;
        }
        .profile-name {
            font-size: 1.1rem; font-weight: 700;
            color: #1a2035; margin: 0 0 0.18rem;
        }
        .profile-birth {
            font-size: 0.76rem; color: #8a94a6; margin-bottom: 0.85rem;
        }
        .pillar-mini-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.45rem 0.7rem;
            margin-top: 0.3rem;
        }
        .pm-label {
            font-size: 0.7rem; color: #8a94a6; display: block;
        }
        .pm-value {
            font-size: 0.92rem; font-weight: 700; color: #1a2035;
        }

        /* ── Balance Status */
        .balance-title {
            font-size: 0.78rem; color: #8a94a6;
            font-weight: 600; letter-spacing: 0.4px;
            margin-bottom: 0.75rem;
        }
        .balance-bar-wrap {
            display: flex; align-items: flex-end;
            gap: 0.5rem; height: 130px;
        }
        .balance-bar-col {
            display: flex; flex-direction: column;
            align-items: center; flex: 1;
            height: 100%; justify-content: flex-end;
        }
        .balance-pct {
            font-size: 0.68rem; font-weight: 700;
            color: #fff; margin-bottom: 3px;
        }
        .balance-bar {
            width: 100%; border-radius: 6px 6px 0 0;
            min-height: 18px;
            display: flex; align-items: flex-start;
            justify-content: center; padding-top: 5px;
        }
        .balance-label  { font-size: 0.76rem; color: #5a6272; margin-top: 0.35rem; font-weight: 600; }
        .balance-label2 { font-size: 0.66rem; color: #b0bac8; }

        /* ── 한 줄 요약 */
        .summary-quote-box {
            background: #ffffff;
            border-radius: 12px;
            padding: 1.3rem 2rem;
            text-align: center;
            margin-bottom: 1.1rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }
        .summary-quote-box p {
            font-size: 1.05rem; font-weight: 700;
            color: #1a2035; margin: 0; line-height: 1.5;
        }

        /* ── 섹션 레이블 */
        .dr-section-label {
            font-size: 0.72rem; font-weight: 700;
            color: #8a94a6; letter-spacing: 1px;
            text-transform: uppercase;
            margin: 0 0 0.65rem;
        }

        /* ── 운세 카드 */
        .fortune-item-card {
            background: #ffffff;
            border-radius: 12px;
            padding: 1rem 1.2rem 1rem 1rem;
            margin-bottom: 0.7rem;
            box-shadow: 0 1px 6px rgba(0,0,0,0.05);
            display: flex; gap: 0.85rem; align-items: flex-start;
        }
        .fortune-icon-dot {
            width: 34px; height: 34px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 0.95rem; flex-shrink: 0; margin-top: 1px;
        }
        .fortune-item-label {
            font-size: 0.76rem; font-weight: 700; margin-bottom: 0.3rem;
        }
        .fortune-item-text {
            font-size: 0.86rem; line-height: 1.7;
            color: #3a4155; margin: 0;
        }

        /* ── 코칭 카드 */
        .coaching-card {
            background: #ffffff;
            border-radius: 12px;
            padding: 1.05rem 1.15rem;
            box-shadow: 0 1px 6px rgba(0,0,0,0.05);
            margin-bottom: 0.5rem;
        }
        .coaching-card-header {
            display: flex; align-items: center;
            gap: 0.45rem; margin-bottom: 0.75rem;
        }
        .coaching-card-icon {
            width: 30px; height: 30px; border-radius: 8px;
            display: flex; align-items: center;
            justify-content: center; font-size: 0.95rem;
        }
        .coaching-card-title {
            font-size: 0.88rem; font-weight: 700; color: #1a2035;
        }
        .coaching-card ul {
            list-style: none; margin: 0; padding: 0;
        }
        .coaching-card li {
            font-size: 0.82rem; line-height: 1.6; color: #3a4155;
            padding: 0.28rem 0;
            border-bottom: 1px solid #f0f2f5;
            display: flex; gap: 0.45rem;
        }
        .coaching-card li:last-child { border-bottom: none; }
        .ck-key {
            font-weight: 700; white-space: nowrap;
            min-width: 5.2rem; color: #1a2035;
        }

        @media (max-width: 720px) {
            .top-panel-inner { grid-template-columns: 1fr; }
            .balance-bar-wrap { height: 90px; }
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
    name = profile.get("name") or "익명"
    birth_date = profile.get("birth_date", "")
    birth_time = profile.get("birth_time", "")
    cal = "양력" if profile.get("calendar_type") == "solar" else "음력"

    elems = saju.five_elements
    total = sum(elems.values()) or 1
    elem_order = ["wood", "fire", "earth", "metal", "water"]

    day_master = saju.day_master or "미정"
    yongsin    = saju.yongsin or "미정"
    gisin      = saju.gisin or "미정"
    yr  = saju.year_pillar or "-"
    mo  = saju.month_pillar or "-"
    day = saju.day_pillar or "-"
    hr  = saju.hour_pillar or "-"

    bars_html = ""
    for en in elem_order:
        color  = _ELEMENT_COLORS[en]
        pct    = _pct(elems.get(en, 0), total)
        height = max(int(pct * 1.1), 16)
        bars_html += f"""
        <div class="balance-bar-col">
            <div class="balance-bar" style="background:{color};height:{height}px;">
                <span class="balance-pct">{pct}%</span>
            </div>
            <div class="balance-label">{_ELEMENT_KR[en]}</div>
            <div class="balance-label2">{en[:2]}</div>
        </div>"""

    st.markdown(
        f"""
        <div class="top-panel">
          <div class="top-panel-inner">
            <div>
              <div class="profile-avatar">🧑</div>
              <p class="profile-name">{escape(name)}</p>
              <p class="profile-birth">{escape(birth_date)} {escape(birth_time)} | {cal}</p>
              <div class="pillar-mini-grid">
                <div><span class="pm-label">일간</span><span class="pm-value">{escape(day_master)}</span></div>
                <div><span class="pm-label">용신</span><span class="pm-value">{escape(yongsin)}</span></div>
                <div><span class="pm-label">기신</span><span class="pm-value">{escape(gisin)}</span></div>
                <div><span class="pm-label">연</span><span class="pm-value">{escape(yr)}</span></div>
                <div><span class="pm-label">월</span><span class="pm-value">{escape(mo)}</span></div>
                <div></div>
                <div><span class="pm-label">일</span><span class="pm-value">{escape(day)}</span></div>
                <div><span class="pm-label">시</span><span class="pm-value">{escape(hr)}</span></div>
              </div>
            </div>
            <div>
              <div class="balance-title">Balance Status</div>
              <div class="balance-bar-wrap">{bars_html}</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_summary_quote(text: str) -> None:
    st.markdown(
        f'<div class="summary-quote-box"><p>{escape(text)}</p></div>',
        unsafe_allow_html=True,
    )


def _render_fortune_section(detailed: dict) -> None:
    st.markdown('<div class="dr-section-label">오늘의 운세</div>', unsafe_allow_html=True)
    for key, color, icon, label in _FORTUNE_META:
        text = escape(detailed.get(key, ""))
        st.markdown(
            f"""
            <div class="fortune-item-card">
                <div class="fortune-icon-dot" style="background:{color}22;color:{color};">{icon}</div>
                <div style="flex:1;">
                    <div class="fortune-item-label" style="color:{color};">{label}</div>
                    <p class="fortune-item-text">{text}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_coaching_section(coaching: dict) -> None:
    st.markdown(
        '<div class="dr-section-label" style="margin-top:1.2rem;">라이프 코칭</div>',
        unsafe_allow_html=True,
    )
    col_top = st.columns(2)
    col_bot = st.columns(2)
    col_map = [col_top[0], col_top[1], col_bot[0], col_bot[1]]

    for i, (key, color, icon, title, fields) in enumerate(_COACHING_META):
        section = coaching.get(key, {})
        items_html = "".join(
            f'<li><span class="ck-key">{escape(f)}</span>'
            f'<span>{escape(str(section.get(f, "")))}</span></li>'
            for f in fields
        )
        card_html = f"""
        <div class="coaching-card">
            <div class="coaching-card-header">
                <div class="coaching-card-icon" style="background:{color}22;color:{color};">{icon}</div>
                <span class="coaching-card-title">{title}</span>
            </div>
            <ul>{items_html}</ul>
        </div>"""
        with col_map[i]:
            st.markdown(card_html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 메인
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="데일리 리포트",
    page_icon="🌅",
    layout="wide",
    initial_sidebar_state="collapsed",
)
init_session_state()
apply_custom_styles()
_inject_css()

saju   = st.session_state.get("user_saju")
profile = st.session_state.get("birth_profile", {})

if saju is None:
    st.warning("아직 입력된 정보가 없습니다. 첫 페이지에서 기본 정보를 먼저 입력해주세요.")
    if st.button("첫 페이지로 돌아가기", type="primary"):
        st.switch_page("app.py")
    st.stop()

# 데이터 생성
build_general_report(saju)        # 기존 호환성 유지
daily = build_daily_report(saju)

# ── 페이지 헤더
header_l, header_r = st.columns([3, 1])
with header_l:
    st.markdown(
        '<div class="dr-logo-row">⚡ MY ENERGY-UP COACH</div>'
        '<div class="dr-page-title">데일리 리포트</div>',
        unsafe_allow_html=True,
    )
with header_r:
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    if st.button("💬 1:1 채팅 상담", use_container_width=True):
        st.switch_page("pages/2_채팅_사주.py")

st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

# ── 상단 패널
_render_top_panel(saju, profile)

# ── 한 줄 요약
_render_summary_quote(daily["one_line_summary"])

# ── 운세
_render_fortune_section(daily["detailed_fortune"])

st.markdown("<div style='height:0.2rem'></div>", unsafe_allow_html=True)

# ── 코칭
_render_coaching_section(daily["coaching"])

# ── 개발자용 JSON
st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
with st.expander("🔍 원본 JSON 데이터 확인 (개발자용)"):
    st.json(daily)
