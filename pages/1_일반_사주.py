"""일반 사주 — 데일리 리포트 전용 페이지."""

from html import escape

import streamlit as st

from core.daily_report_builder import build_daily_report
from ui.styles import apply_custom_styles
from utils.helpers import init_session_state

# ── 오행별 색상
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

# ── 운세 섹션 메타
_FORTUNE_META = [
    ("총운",       "#6cbf8e", "✦", "총운"),
    ("재물운",     "#e8c46a", "💰", "재물운"),
    ("비즈니스운", "#7ab3d4", "🏢", "비즈니스(사업/직장)"),
    ("애정운",     "#e8837a", "♡",  "애정운(연애/인간관계)"),
    ("건강운",     "#a89fd8", "⊕",  "건강운"),
]

# ── 코칭 섹션 메타
_COACHING_META = [
    ("outfit",      "#7ab3d4", "👔", "의상 코칭",
     ["돋보이는 코디 및 색상", "행운의 아이템 & 액세서리", "피해야 할 의상"]),
    ("food",        "#6cbf8e", "🍵", "푸드 코칭",
     ["점심/회식 추천 메뉴", "주류 및 음료", "피해야 할 음식/주류/음료"]),
    ("environment", "#a89fd8", "🌿", "공간 코칭",
     ["업무 효율용 공간 제안", "행운의 방향", "피해야 할 장소"]),
    ("action",      "#e8c46a", "⚡", "행동 전략 코칭",
     ["커뮤니케이션 팁", "네트워킹 팁"]),
]


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
def _inject_css() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] > .main { background: #f5f6f8; }
        [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none; }

        /* ── 로고 / 타이틀 */
        .dr-logo-row {
            color: #3b82a0; font-size: 0.76rem; font-weight: 700;
            letter-spacing: 1.5px; text-transform: uppercase;
            margin-bottom: 0.2rem;
        }
        .dr-page-title {
            font-size: 1.8rem; font-weight: 800;
            color: #1a2035; margin: 0 0 0.8rem;
        }

        /* ── 상단 패널 */
        .dr-top-panel {
            background: #ffffff; border-radius: 14px;
            padding: 1.5rem 1.8rem; margin-bottom: 1.1rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }
        .dr-top-inner {
            display: grid;
            grid-template-columns: 200px 1fr;
            gap: 2rem; align-items: end;
        }

        /* ── 프로필 */
        .dr-avatar {
            width: 68px; height: 68px; border-radius: 50%;
            background: #dde3ec;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.7rem; margin-bottom: 0.55rem;
        }
        .dr-profile-name { font-size: 1.05rem; font-weight: 700; color: #1a2035; margin: 0 0 0.15rem; }
        .dr-profile-birth { font-size: 0.74rem; color: #8a94a6; margin-bottom: 0.8rem; }
        .dr-pillar-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.4rem 0.7rem; }
        .dr-pm-label { font-size: 0.69rem; color: #8a94a6; display: block; }
        .dr-pm-value { font-size: 0.9rem; font-weight: 700; color: #1a2035; }

        /* ── Balance Status */
        .balance-title { font-size: 0.77rem; color: #8a94a6; font-weight: 600; margin-bottom: 0.7rem; }
        .balance-bar-wrap { display: flex; align-items: flex-end; gap: 0.5rem; height: 180px; }
        .balance-bar-col {
            display: flex; flex-direction: column;
            align-items: center; flex: 1;
            height: 100%; justify-content: flex-end;
        }
        .balance-pct { font-size: 0.67rem; font-weight: 700; color: #fff; margin-bottom: 3px; }
        .balance-bar {
            width: 100%; border-radius: 6px 6px 0 0; min-height: 16px;
            display: flex; align-items: flex-start;
            justify-content: center; padding-top: 4px;
        }
        .balance-lbl  { font-size: 0.74rem; color: #5a6272; margin-top: 0.3rem; font-weight: 600; }
        .balance-lbl2 { font-size: 0.64rem; color: #b0bac8; }

        /* ── 한 줄 요약 */
        .dr-summary-box {
            background: #ffffff; border-radius: 12px;
            padding: 1.2rem 1.8rem; text-align: center;
            margin-bottom: 1rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }
        .dr-summary-box p {
            font-size: 1.03rem; font-weight: 700;
            color: #1a2035; margin: 0; line-height: 1.5;
        }

        /* ── 섹션 레이블 */
        .dr-slabel {
            font-size: 0.71rem; font-weight: 700;
            color: #8a94a6; letter-spacing: 1px;
            text-transform: uppercase; margin: 0 0 0.6rem;
        }

        /* ── 운세 카드 */
        .dr-fortune-card {
            background: #ffffff; border-radius: 12px;
            padding: 0.95rem 1.15rem 0.95rem 0.95rem;
            margin-bottom: 0.65rem;
            box-shadow: 0 1px 6px rgba(0,0,0,0.05);
            display: flex; gap: 0.8rem; align-items: flex-start;
        }
        .dr-fortune-dot {
            width: 32px; height: 32px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 0.9rem; flex-shrink: 0; margin-top: 1px;
        }
        .dr-flabel { font-size: 0.74rem; font-weight: 700; margin-bottom: 0.25rem; }
        .dr-ftext  { font-size: 0.84rem; line-height: 1.7; color: #3a4155; margin: 0; }

        /* ── 코칭 카드 */
        .dr-coaching-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.85rem;
            margin-bottom: 0.5rem;
        }
        .dr-coaching-card {
            background: #ffffff; border-radius: 12px;
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
        .dr-cc-title { font-size: 0.86rem; font-weight: 700; color: #1a2035; }
        .dr-coaching-card ul { list-style: none; margin: 0; padding: 0; flex: 1; }
        .dr-coaching-card li {
            font-size: 0.8rem; line-height: 1.6; color: #3a4155;
            padding: 0.25rem 0; border-bottom: 1px solid #f0f2f5;
            display: flex; gap: 0.4rem;
        }
        .dr-coaching-card li:last-child { border-bottom: none; }
        .dr-ck-key { font-weight: 700; white-space: nowrap; min-width: 5rem; color: #1a2035; }

        @media (max-width: 720px) {
            .dr-top-inner { grid-template-columns: 1fr; }
            .balance-bar-wrap { height: 130px; }
            .dr-coaching-grid { grid-template-columns: 1fr; }
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
        height = max(int(pct * 1.6), 18)
        bars_html += f"""
        <div class="balance-bar-col">
            <div class="balance-bar" style="background:{color};height:{height}px;">
                <span class="balance-pct">{pct}%</span>
            </div>
            <div class="balance-lbl">{_ELEMENT_KR[en]}</div>
            <div class="balance-lbl2">{en[:2]}</div>
        </div>"""

    st.markdown(
        f"""
        <div class="dr-top-panel">
          <div class="dr-top-inner">
            <div>
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
            <div>
              <div class="balance-bar-wrap">{bars_html}</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_fortune(detailed: dict) -> None:
    st.markdown('<div class="dr-slabel">오늘의 운세</div>', unsafe_allow_html=True)
    for key, color, icon, label in _FORTUNE_META:
        text = escape(detailed.get(key, ""))
        st.markdown(
            f"""
            <div class="dr-fortune-card">
                <div class="dr-fortune-dot" style="background:{color}22;color:{color};">{icon}</div>
                <div style="flex:1;">
                    <div class="dr-flabel" style="color:{color};">{label}</div>
                    <p class="dr-ftext">{text}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_coaching(coaching: dict) -> None:
    st.markdown(
        '<div class="dr-slabel" style="margin-top:1.1rem;">라이프 코칭</div>',
        unsafe_allow_html=True,
    )

    cards_html = ""
    for key, color, icon, title, fields in _COACHING_META:
        section    = coaching.get(key, {})
        items_html = "".join(
            f'<li><span class="dr-ck-key">{escape(f)}</span>'
            f'<span>{escape(str(section.get(f, "")))}</span></li>'
            for f in fields
        )
        cards_html += f"""
        <div class="dr-coaching-card">
            <div class="dr-cc-header">
                <div class="dr-cc-icon" style="background:{color}22;color:{color};">{icon}</div>
                <span class="dr-cc-title">{title}</span>
            </div>
            <ul>{items_html}</ul>
        </div>"""

    st.markdown(
        f'<div class="dr-coaching-grid">{cards_html}</div>',
        unsafe_allow_html=True
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

# ── 본문
daily = build_daily_report(saju)

_render_top_panel(saju, profile)
_render_fortune_summary = daily["one_line_summary"]
st.markdown(
    f'<div class="dr-summary-box"><p>{escape(_render_fortune_summary)}</p></div>',
    unsafe_allow_html=True,
)
_render_fortune(daily["detailed_fortune"])
st.markdown("<div style='height:0.2rem'></div>", unsafe_allow_html=True)
_render_coaching(daily["coaching"])

