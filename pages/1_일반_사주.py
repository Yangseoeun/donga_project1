"""일반 사주 — 데일리 리포트 전용 페이지."""

import base64
from html import escape
from pathlib import Path

import streamlit as st

from core.daily_report_builder import build_daily_report
from ui.styles import apply_custom_styles
from utils.helpers import init_session_state

# ── 이미지 경로
_IMG_DIR = Path(__file__).parent.parent / "img" / "proj1_report"


@st.cache_data
def _img_b64(filename: str) -> str:
    """이미지 파일을 base64로 인코딩하여 반환."""
    with open(_IMG_DIR / filename, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ── 오행별 색상 (데일리 리포트 디자인 토큰)
_ELEMENT_COLORS: dict[str, str] = {
    "wood":  "#A8C69F",
    "fire":  "#F8A1A4",
    "earth": "#EBD9B4",
    "metal": "#D1D1D1",
    "water": "#3E8EAB",
}
_ELEMENT_KR: dict[str, str] = {
    "wood": "木", "fire": "火", "earth": "土", "metal": "金", "water": "水",
}
_ELEMENT_SUB_KR: dict[str, str] = {
    "wood": "목", "fire": "화", "earth": "토", "metal": "금", "water": "수",
}

# ── 운세 섹션 메타
_FORTUNE_META = [
    ("총운",       "#6cbf8e", "✦", "총운"),
    ("재물운",     "#e8c46a", "💰", "재물운"),
    ("비즈니스운", "#7ab3d4", "🏢", "비즈니스(사업/직장)"),
    ("애정운",     "#e8837a", "♡",  "애정운(연애/인간관계)"),
    ("건강운",     "#a89fd8", "⊕",  "건강운"),
]

# ── 코칭 섹션 메타 (icon_bg, icon_color, 파스텔 팔레트)
_COACHING_META = [
    ("outfit",      "rgba(255,193,100,0.25)", "#c47c00", "👔", "의상 코칭",
     ["돋보이는 코디 및 색상", "행운의 아이템 & 액세서리", "피해야 할 의상"]),
    ("food",        "rgba(62,142,171,0.25)",  "#3E8EAB", "🍵", "푸드 코칭",
     ["점심/회식 추천 메뉴", "주류 및 음료", "피해야 할 음식/주류/음료"]),
    ("environment", "rgba(168,198,159,0.30)", "#5a9e6f", "🌿", "환경 코칭",
     ["업무 효율용 공간 제안", "행운의 방향", "피해야 할 장소"]),
    ("action",      "rgba(248,161,164,0.25)", "#d04b50", "⚡", "행동 전략 코칭",
     ["커뮤니케이션 팁", "네트워킹 팁"]),
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

        /* ── 로고 / 타이틀 */
        .dr-logo-row {
            color: #3E8EAB; font-size: 0.76rem; font-weight: 700;
            letter-spacing: 1.5px; text-transform: uppercase;
            margin-bottom: 0.2rem;
        }
        .dr-page-title {
            font-size: 1.8rem; font-weight: 800;
            color: #1A374D; margin: 0 0 0.8rem;
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
        .st-key-header_actions .st-key-chat_consult_action {
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
        .dr-profile-card {
            background: #ffffff; border-radius: 12px;
            padding: 1.4rem 1.2rem;
            min-height: 315px;
            box-sizing: border-box;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }
        .dr-avatar {
            width: 60px; height: 60px; border-radius: 50%;
            background: #dde3ec;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.5rem; margin-bottom: 0.5rem;
        }
        .dr-profile-name { font-size: 1rem; font-weight: 700; color: #1A374D; margin: 0 0 0.1rem; }
        .dr-profile-birth { font-size: 0.72rem; color: #8a94a6; margin-bottom: 0.7rem; }
        .dr-pillar-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.3rem 0.5rem; }
        .dr-pm-label { font-size: 0.68rem; color: #8a94a6; display: block; }
        .dr-pm-value { font-size: 0.88rem; font-weight: 700; color: #1A374D; }

        /* ── Balance Status 카드 */
        .dr-balance-card {
            background: #ffffff; border-radius: 12px;
            padding: 1.1rem 1.4rem 0.8rem;
            min-height: 315px;
            box-sizing: border-box;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }
        .balance-title { font-size: 0.77rem; color: #8a94a6; font-weight: 600; margin-bottom: 0.7rem; }
        .balance-bar-wrap { display: flex; align-items: flex-end; gap: 0.5rem; height: 245px; }
        .balance-bar-col {
            display: flex; flex-direction: column;
            align-items: center; flex: 1;
            height: 100%; justify-content: flex-end;
        }
        .balance-pct { font-size: 0.75rem; font-weight: 700; color: #fff; padding-top: 6px; }
        .balance-bar {
            width: 100%; border-radius: 16px 16px 0 0; min-height: 20px;
            display: flex; align-items: flex-start;
            justify-content: center;
        }
        .balance-lbl  { font-size: 0.82rem; color: #072f48; margin-top: 0.35rem; font-weight: 700; }
        .balance-lbl2 { font-size: 0.72rem; color: #7a7a7a; font-weight: 400; }

        /* ── 한 줄 요약 */
        .dr-summary-box {
            background: #ffffff; border-radius: 20px;
            padding: 1.2rem 1.8rem; text-align: center;
            margin-bottom: 1rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }
        .dr-summary-box p {
            font-size: 1.03rem; font-weight: 700;
            color: #1A374D; margin: 0; line-height: 1.5;
        }

        /* ── 섹션 레이블 */
        .dr-slabel {
            font-size: 0.71rem; font-weight: 700;
            color: #8a94a6; letter-spacing: 1px;
            text-transform: uppercase; margin: 0 0 0.6rem;
        }

        /* ── 운세 카드 */
        .dr-fortune-card {
            background: #ffffff; border-radius: 20px;
            padding: 1.1rem 1.3rem;
            margin-bottom: 0.65rem;
            box-shadow: 0 1px 6px rgba(0,0,0,0.05);
        }
        .dr-fortune-badge-primary {
            display: inline-flex; align-items: center; gap: 6px;
            background: #1A374D; color: #e9f4f6;
            border-radius: 32px; padding: 3px 16px;
            font-size: 0.88rem; font-weight: 700;
            margin-bottom: 0.6rem;
        }
        .dr-fortune-badge-secondary {
            display: inline-flex; align-items: center; gap: 6px;
            background: rgba(62,142,171,0.18); color: #3E8EAB;
            border-radius: 32px; padding: 3px 16px;
            font-size: 0.88rem; font-weight: 700;
            margin-bottom: 0.6rem;
        }
        .dr-ftext  { font-size: 0.88rem; line-height: 1.75; color: #333333; margin: 0; }

        /* ── 코칭 카드 */
        .dr-coaching-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.85rem;
            margin-bottom: 0.5rem;
        }
        .dr-coaching-card {
            background: #ffffff; border-radius: 20px;
            padding: 1rem 1.1rem;
            box-shadow: 0 1px 6px rgba(0,0,0,0.05);
            height: 100%;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
        }
        .dr-cc-header { display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.7rem; }
        .dr-cc-icon {
            width: 28px; height: 28px; border-radius: 7px;
            display: flex; align-items: center; justify-content: center; font-size: 0.9rem;
        }
        .dr-cc-title { font-size: 1rem; font-weight: 700; color: #1a2035; }
        .dr-coaching-card ul { list-style: none; margin: 0; padding: 0; flex: 1; }
        .dr-coaching-card li {
            font-size: 1rem !important; line-height: 1.7; color: #333333;
            padding: 0.25rem 0; border-bottom: 1px solid #f0f2f5;
            display: flex; gap: 0.4rem;
        }
        .dr-coaching-card li span { font-size: 1rem !important; line-height: 1.7; }
        .dr-coaching-card li:last-child { border-bottom: none; }
        .dr-ck-key { font-size: 1rem !important; font-weight: 700; white-space: nowrap; min-width: 6rem; color: #1A374D; }

        /* ── 통합 리포트 박스 */
        .dr-unified-report {
            background: #ffffff;
            border-radius: 12px;
            padding: 32px 42px 34px;
            margin: 1rem 0 1.2rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        }
        .dr-unified-summary {
            color: #07314a;
            font-size: 1.18rem;
            font-weight: 800;
            line-height: 1.55;
            margin: 0 0 34px;
            text-align: center;
        }
        .dr-unified-section {
            margin: 0 0 24px;
        }
        .dr-unified-section:last-child {
            margin-bottom: 0;
        }
        .dr-unified-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #a8e6ed;
            border-radius: 999px;
            color: #07314a;
            font-size: 0.86rem;
            font-weight: 800;
            line-height: 1;
            padding: 5px 14px;
            margin: 0 0 8px;
        }
        .dr-unified-badge-primary {
            background: #07314a;
            color: #ffffff;
        }
        .dr-unified-text {
            color: #222222;
            font-size: 0.88rem;
            line-height: 1.75;
            margin: 0;
        }
        .dr-unified-text strong {
            color: #111111;
            font-weight: 800;
        }

        @media (max-width: 720px) {
            .balance-bar-wrap { height: 130px; }
            .dr-coaching-grid { grid-template-columns: 1fr; }
            .dr-unified-report { padding: 24px 20px; }
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
    name       = profile.get("name") or "익명"
    birth_date = profile.get("birth_date", "")
    birth_time = profile.get("birth_time", "")
    cal        = "양력" if profile.get("calendar_type") == "solar" else "음력"

    elems      = saju.five_elements
    total      = sum(elems.values()) or 1
    elem_order = ["wood", "fire", "earth", "metal", "water"]

    day_master = saju.day_master or "미정"
    yongsin    = saju.yongsin or "미정"
    gisin      = saju.gisin or "미정"
    yr  = saju.year_pillar  or "-"
    mo  = saju.month_pillar or "-"
    day = saju.day_pillar   or "-"
    hr  = saju.hour_pillar  or "-"

    bars_html = ""
    for en in elem_order:
        color  = _ELEMENT_COLORS[en]
        pct    = _pct(elems.get(en, 0), total)
        height = max(int(pct * 2.0), 20)
        gradient = (
            f"linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.4) 100%), "
            f"linear-gradient(to left, {color}, {color})"
        )
        bars_html += f"""
        <div class="balance-bar-col">
            <div class="balance-bar" style="background:{gradient};height:{height}px;">
                <span class="balance-pct">{pct}%</span>
            </div>
            <div class="balance-lbl">{_ELEMENT_KR[en]}</div>
            <div class="balance-lbl2">{_ELEMENT_SUB_KR[en]}</div>
        </div>"""

    col_profile, col_balance = st.columns([1, 3])

    with col_profile:
        st.markdown(
            f"""
            <div class="dr-profile-card">
              <div class="dr-avatar">🧑</div>
              <p class="dr-profile-name">{escape(name)}</p>
              <p class="dr-profile-birth">{escape(birth_date)} {escape(birth_time)} | {cal}</p>
              <div class="dr-pillar-grid">
                <div><span class="dr-pm-label">일간</span><span class="dr-pm-value">{escape(day_master)}</span></div>
                <div><span class="dr-pm-label">용신</span><span class="dr-pm-value">{escape(yongsin)}</span></div>
                <div><span class="dr-pm-label">기신</span><span class="dr-pm-value">{escape(gisin)}</span></div>
                <div><span class="dr-pm-label">연</span><span class="dr-pm-value">{escape(yr)}</span></div>
                <div><span class="dr-pm-label">월</span><span class="dr-pm-value">{escape(mo)}</span></div>
                <div></div>
                <div><span class="dr-pm-label">일</span><span class="dr-pm-value">{escape(day)}</span></div>
                <div><span class="dr-pm-label">시</span><span class="dr-pm-value">{escape(hr)}</span></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_balance:
        st.markdown(
            f"""
            <div class="dr-balance-card">
              <div class="balance-title">Balance Status</div>
              <div class="balance-bar-wrap">{bars_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_fortune(detailed: dict) -> None:
    st.markdown('<div class="dr-slabel">오늘의 운세</div>', unsafe_allow_html=True)
    for i, (key, _color, icon, label) in enumerate(_FORTUNE_META):
        text       = escape(detailed.get(key, ""))
        badge_cls  = "dr-fortune-badge-primary" if i == 0 else "dr-fortune-badge-secondary"
        st.markdown(
            f"""
            <div class="dr-fortune-card">
                <div class="{badge_cls}">{icon}&nbsp;{label}</div>
                <p class="dr-ftext">{text}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_coaching(coaching: dict) -> None:

    cards_html = ""
    for key, icon_bg, icon_color, icon, title, fields in _COACHING_META:
        section    = coaching.get(key, {})
        items_html = "".join(
            f'<li><span class="dr-ck-key">{escape(f)}</span>'
            f'<span>{escape(str(section.get(f, "")))}</span></li>'
            for f in fields
        )
        cards_html += f"""
        <div class="dr-coaching-card">
            <div class="dr-cc-header">
                <div class="dr-cc-icon" style="background:{icon_bg};color:{icon_color};">{icon}</div>
                <span class="dr-cc-title" style="color:{icon_color};">{title}</span>
            </div>
            <ul>{items_html}</ul>
        </div>"""

    st.markdown(
        f'<div class="dr-coaching-grid">{cards_html}</div>',
        unsafe_allow_html=True
    )


def _render_unified_report(daily: dict) -> None:
    summary = escape(daily.get("one_line_summary", ""))
    detailed = daily.get("detailed_fortune", {})

    sections_html = ""
    for idx, (key, _color, icon, label) in enumerate(_FORTUNE_META):
        badge_cls = "dr-unified-badge dr-unified-badge-primary" if idx == 0 else "dr-unified-badge"
        sections_html += f"""
        <section class="dr-unified-section">
            <div class="{badge_cls}">{icon}&nbsp;{label}</div>
            <p class="dr-unified-text">{escape(detailed.get(key, ""))}</p>
        </section>
        """

    st.markdown(
        f"""
        <div class="dr-unified-report">
            <p class="dr-unified-summary">“{summary}”</p>
            {sections_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ===========================================================================
# 메인
# ===========================================================================
st.set_page_config(
    page_title="데일리 리포트",
    page_icon="🌅",
    layout="wide",
    initial_sidebar_state="collapsed",
)
init_session_state()
apply_custom_styles()
_inject_css()

saju    = st.session_state.get("user_saju")
profile = st.session_state.get("birth_profile", {})

if saju is None:
    st.warning("아직 입력된 정보가 없습니다. 첫페이지에서 기본 정보를 먼저 입력해주세요.")
    if st.button("첫페이지로 돌아가기", type="primary"):
        st.switch_page("app.py")
    st.stop()

# ── 헤더
header_l, header_r = st.columns([3, 1])
with header_l:
    logo_b64 = _img_b64("로고.png")
    st.markdown(
        f'<img src="data:image/png;base64,{logo_b64}" style="height:82px; margin-bottom:8px; display:block;" />'
        '<div style="font-size:32px; font-weight:800; color:#000000; line-height:1.2; margin-bottom:0;">데일리 리포트</div>',
        unsafe_allow_html=True,
    )
with header_r:
    with st.container(key="header_actions"):
        if st.button("← 처음으로", key="home_action"):
            st.switch_page("app.py")
        if st.button("💬 1:1 채팅 상담", key="chat_consult_action"):
            st.switch_page("pages/2_채팅_사주.py")

st.markdown("<div style='height:0'></div>", unsafe_allow_html=True)

# ── 본문
daily = build_daily_report(saju)

_render_top_panel(saju, profile)
_render_unified_report(daily)
_render_coaching(daily["coaching"])

