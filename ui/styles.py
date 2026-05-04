"""Centralized Streamlit CSS."""

import base64
from pathlib import Path

import streamlit as st


_MAIN_IMG_DIR = Path(__file__).parent.parent / "img" / "proj1_main"
_FONT_DIR = Path(__file__).parent / "fonts" / "pretendard_woff"


@st.cache_data
def _main_img_b64(filename: str) -> str:
    with open(_MAIN_IMG_DIR / filename, "rb") as f:
        return base64.b64encode(f.read()).decode()


@st.cache_data
def _font_b64(filename: str) -> str:
    with open(_FONT_DIR / filename, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _pretendard_font_css() -> str:
    return """
        @font-face {
            font-family: 'Pretendard';
            src: url(data:font/woff;base64,__PRETENDARD_REGULAR__) format('woff');
            font-weight: 400;
            font-style: normal;
            font-display: swap;
        }
        @font-face {
            font-family: 'Pretendard';
            src: url(data:font/woff;base64,__PRETENDARD_MEDIUM__) format('woff');
            font-weight: 500;
            font-style: normal;
            font-display: swap;
        }
        @font-face {
            font-family: 'Pretendard';
            src: url(data:font/woff;base64,__PRETENDARD_SEMIBOLD__) format('woff');
            font-weight: 600;
            font-style: normal;
            font-display: swap;
        }
        @font-face {
            font-family: 'Pretendard';
            src: url(data:font/woff;base64,__PRETENDARD_BOLD__) format('woff');
            font-weight: 700;
            font-style: normal;
            font-display: swap;
        }
    """.replace("__PRETENDARD_REGULAR__", _font_b64("Pretendard-Regular.woff")).replace(
        "__PRETENDARD_MEDIUM__", _font_b64("Pretendard-Medium.woff")
    ).replace(
        "__PRETENDARD_SEMIBOLD__", _font_b64("Pretendard-SemiBold.woff")
    ).replace(
        "__PRETENDARD_BOLD__", _font_b64("Pretendard-Bold.woff")
    )


def apply_custom_styles() -> None:
    """
    Apply custom CSS used by all Streamlit pages.

    Returns:
        None
    """
    css = """
        <style>
        __PRETENDARD_FONT_CSS__
        html, body, .stApp, button, input, textarea, select,
        [data-testid="stMarkdownContainer"] {
            font-family: 'Pretendard', sans-serif !important;
        }
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"] {
            display: none;
        }
        .hero-panel {
            min-height: 260px;
            border: 1px solid rgba(226, 232, 240, 0.14);
            border-radius: 8px;
            padding: 2rem;
            margin: 1rem 0;
            background:
                linear-gradient(135deg, rgba(107, 70, 193, 0.24), rgba(14, 165, 233, 0.10)),
                radial-gradient(circle at 85% 20%, rgba(245, 158, 11, 0.18), transparent 28%),
                rgba(22, 33, 62, 0.68);
            display: flex;
            align-items: end;
        }
        .hero-copy {
            max-width: 760px;
        }
        .hero-copy h2 {
            font-size: 2.35rem;
            line-height: 1.2;
            margin: 0.4rem 0 0.8rem;
        }
        .hero-copy p {
            line-height: 1.75;
            margin: 0;
        }
        .eyebrow {
            color: #A78BFA;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0;
        }
        .saju-card {
            background: rgba(107, 70, 193, 0.12);
            border: 1px solid rgba(107, 70, 193, 0.32);
            border-radius: 8px;
            padding: 1.25rem;
            margin: 1rem 0;
        }
        .compact-card p {
            margin: 0.35rem 0;
        }
        .report-card {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.75rem;
        }
        .report-item {
            background: rgba(226, 232, 240, 0.05);
            border: 1px solid rgba(226, 232, 240, 0.10);
            border-radius: 8px;
            padding: 1rem;
        }
        .report-item h4 {
            margin: 0 0 0.45rem;
        }
        .report-item p {
            line-height: 1.65;
            margin: 0;
        }
        .metric-row {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.75rem;
        }
        .pillar-box {
            background: rgba(226, 232, 240, 0.06);
            border: 1px solid rgba(226, 232, 240, 0.12);
            border-radius: 8px;
            padding: 0.9rem;
            min-height: 88px;
        }
        .pillar-box span {
            color: rgba(226, 232, 240, 0.74);
            font-size: 0.88rem;
        }
        .pillar-box strong {
            display: block;
            margin-top: 0.35rem;
            font-size: 1.35rem;
        }
        .chat-message-user,
        .chat-message-ai {
            border-radius: 8px;
            padding: 0.85rem 1rem;
            margin: 0.65rem 0;
            line-height: 1.65;
        }
        .chat-message-user {
            background: rgba(59, 130, 246, 0.16);
            border: 1px solid rgba(59, 130, 246, 0.32);
        }
        .chat-message-ai {
            background: rgba(107, 70, 193, 0.16);
            border: 1px solid rgba(107, 70, 193, 0.32);
        }
        .choice-panel {
            background: #dbeafe;
            color: #111827;
            border-radius: 0;
            padding: 1rem 1.2rem;
            margin: 1rem 0 0.75rem;
            line-height: 1.65;
        }
        .choice-panel p {
            margin: 0 0 0.85rem;
        }
        .choice-panel p:last-child {
            margin-bottom: 0;
        }
        .choice-hint {
            font-size: 0.95rem;
        }
        @media (max-width: 720px) {
            .hero-panel {
                min-height: 220px;
                padding: 1.25rem;
            }
            .hero-copy h2 {
                font-size: 1.7rem;
            }
            .metric-row {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
            .report-card {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """.replace("__PRETENDARD_FONT_CSS__", _pretendard_font_css())
    st.markdown(
        css,
        unsafe_allow_html=True,
    )


def apply_landing_styles() -> None:
    """
    랜딩 페이지(app.py) 전용 CSS.
    Figma 디자인 토큰 기반으로 작성. 다른 페이지에서는 호출하지 않는다.
    """
    bg_b64 = _main_img_b64("Frame 1000004456.png")
    css = """
        <style>
        /* ── Pretendard 폰트 */
        __PRETENDARD_FONT_CSS__
        html, body, .stApp, button, input, textarea, select,
        [data-testid="stMarkdownContainer"] {
            font-family: 'Pretendard', sans-serif !important;
        }

        /* ── 사이드바 숨김 */
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"] { display: none; }
        [data-testid="stHeader"] { background: transparent; }

        /* ── 앱 배경 (conic gradient → e9f4f6 페이드) */
        .stApp,
        [data-testid="stAppViewContainer"] > .main {
            background: url("data:image/png;base64,__BG_B64__") center top / cover no-repeat fixed !important;
            font-family: 'Pretendard', sans-serif;
        }
        [data-testid="stMainBlockContainer"] {
            padding-top: 0 !important;
        }

        /* ── 랜딩 히어로 */
        .landing-hero {
            padding: 0 24px 20px;
            text-align: center;
        }
        .landing-logo-badge {
            display: inline-block;
            margin-bottom: 46px;
        }
        .landing-logo-badge img {
            width: 220px;
            height: auto;
            max-width: 80vw;
            display: block;
            margin: 0 auto;
        }
        .landing-headline {
            font-family: 'Pretendard', sans-serif;
            font-size: 42px; font-weight: 900;
            color: #000000 !important; letter-spacing: 0;
            margin: 0 0 16px; line-height: 1.2;
        }
        .landing-headline span {
            color: #000000 !important;
        }
        .landing-brand-line {
            font-family: 'Pretendard', sans-serif;
            font-size: 22px; color: #000000; margin: 0;
            line-height: 1.45;
            font-weight: 500;
        }
        .landing-brand-line strong {
            color: #000000;
            font-weight: 900;
        }

        /* ── 폼 설명 */
        .form-desc {
            font-family: 'Pretendard', sans-serif;
            font-size: 14px;
            color: #000000;
            text-align: center;
            margin: 0 0 18px;
        }

        /* ── 폼 컨테이너 카드 (glassmorphism) */
        [data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.72) !important;
            border-radius: 12px !important;
            padding: 20px 140px 24px !important;
            border: 1px solid rgba(255, 255, 255, 0.90) !important;
            backdrop-filter: blur(8px) !important;
        }

        /* ── Streamlit 입력 필드 → Figma 스타일 오버라이드 */
        [data-testid="stTextInput"] input {
            border-radius: 8px !important;
            border: 1px solid #cfd7d9 !important;
            height: 42px !important;
            font-family: 'Pretendard', sans-serif !important;
            font-size: 14px !important;
            background: #ffffff !important;
            color: #000000 !important;
        }
        [data-testid="stTextInput"] [data-baseweb="input"],
        [data-testid="stDateInput"] [data-baseweb="input"],
        [data-testid="stTimeInput"] [data-baseweb="input"],
        [data-baseweb="input"] {
            background-color: #ffffff !important;
            background: #ffffff !important;
            color: #000000 !important;
        }
        [data-testid="stTextInput"] [data-baseweb="input"] *,
        [data-testid="stDateInput"] [data-baseweb="input"] *,
        [data-testid="stTimeInput"] [data-baseweb="input"] *,
        [data-baseweb="input"] * {
            background-color: #ffffff !important;
            color: #000000 !important;
            font-family: 'Pretendard', sans-serif !important;
            font-size: 14px !important;
        }
        [data-testid="stDateInput"] input {
            border-radius: 8px !important;
            border: none !important;
            height: 42px !important;
            font-family: 'Pretendard', sans-serif !important;
            font-size: 14px !important;
            background: #ffffff !important;
            color: #000000 !important;
        }
        [data-testid="stDateInput"] [data-baseweb="input"] {
            height: 42px !important;
            min-height: 42px !important;
            border-radius: 8px !important;
            border: 1px solid #cfd7d9 !important;
            background: #ffffff !important;
            box-shadow: none !important;
            overflow: hidden !important;
        }
        [data-testid="stDateInput"] [data-baseweb="input"] > div {
            height: 42px !important;
            min-height: 42px !important;
            border-radius: 8px !important;
            background: #ffffff !important;
        }
        [data-testid="stSelectbox"] > div > div[data-baseweb="select"] > div:first-child {
            border-radius: 8px !important;
            border: 1px solid #cfd7d9 !important;
            background: #ffffff !important;
            min-height: 42px !important;
            color: #000000 !important;
        }
        [data-testid="stSelectbox"] [data-baseweb="select"],
        [data-testid="stSelectbox"] [data-baseweb="select"] > div,
        [data-testid="stSelectbox"] [data-baseweb="select"] div {
            background-color: #ffffff !important;
            color: #000000 !important;
            font-family: 'Pretendard', sans-serif !important;
            font-size: 14px !important;
        }
        [data-testid="stSelectbox"] svg {
            fill: #000000 !important;
            color: #000000 !important;
        }
        [data-testid="stTimeInput"] input {
            border-radius: 8px !important;
            border: 1px solid #cfd7d9 !important;
            height: 42px !important;
            font-family: 'Pretendard', sans-serif !important;
            font-size: 14px !important;
            background: #ffffff !important;
            color: #000000 !important;
        }
        [data-testid="stTimeInput"] > div,
        [data-testid="stTimeInput"] div,
        [data-testid="stTimeInput"] button {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        [data-testid="stTimeInput"] svg {
            fill: #000000 !important;
            color: #000000 !important;
        }
        /* ── 라디오 버튼: 미선택 = 파란 테두리 + 흰 배경 */
        [data-testid="stRadio"] input[type="radio"] {
            accent-color: #087f9b !important;
        }
        [data-testid="stRadio"] [role="radio"] {
            background-color: #ffffff !important;
            border: 2px solid #087f9b !important;
            border-radius: 50% !important;
            width: 20px !important;
            height: 20px !important;
            position: relative !important;
        }
        /* 미선택 상태: 내부 점 없음 (흰 배경만) */
        [data-testid="stRadio"] [role="radio"]::after {
            content: none !important;
        }
        /* 선택된 상태: 파란 테두리 유지 */
        [data-testid="stRadio"] [role="radio"][aria-checked="true"],
        [data-testid="stRadio"] [role="radio"][data-checked="true"],
        [data-testid="stRadio"] [role="radiogroup"] label [aria-checked="true"],
        [data-testid="stRadio"] [role="radiogroup"] label [data-checked="true"] {
            background-color: #ffffff !important;
            border: 2px solid #087f9b !important;
        }
        /* 선택된 상태: 파란색 내부 점 */
        [data-testid="stRadio"] [role="radio"][aria-checked="true"]::after,
        [data-testid="stRadio"] [role="radio"][data-checked="true"]::after,
        [data-testid="stRadio"] [role="radiogroup"] label [aria-checked="true"]::after,
        [data-testid="stRadio"] [role="radiogroup"] label [data-checked="true"]::after {
            background-color: #087f9b !important;
            border: none !important;
            border-radius: 50% !important;
            content: "" !important;
            display: block !important;
            height: 10px !important;
            width: 10px !important;
            left: 50% !important;
            position: absolute !important;
            top: 50% !important;
            transform: translate(-50%, -50%) !important;
        }
        [data-testid="stTextInput"] label,
        [data-testid="stDateInput"] label,
        [data-testid="stTimeInput"] label,
        [data-testid="stSelectbox"] label,
        [data-testid="stRadio"] label,
        [data-testid="stRadio"] p,
        [data-testid="stRadio"] span {
            color: #000000 !important;
            font-size: 14px !important;
        }
        [data-testid="stRadio"] [role="radiogroup"] label span {
            font-size: 14px !important;
            font-weight: 700 !important;
        }
        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stDateInput"] input::placeholder,
        [data-testid="stTimeInput"] input::placeholder {
            color: rgba(0, 0, 0, 0.42) !important;
        }

        /* ── 폼 제출 버튼 */
        [data-testid="stFormSubmitButton"] > button {
            background: #072f48 !important;
            color: #ffffff !important;
            border-radius: 100px !important;
            height: 52px !important;
            font-family: 'Pretendard', sans-serif !important;
            font-size: 14px !important;
            font-weight: 700 !important;
            border: none !important;
            margin-top: 8px;
        }

        /* ── 완료 배너 (다크 네이비) */
        .complete-banner {
            background: #072f48;
            border-radius: 8px;
            padding: 22px 24px;
            margin: 18px 0 8px;
            display: flex;
            align-items: center;
            justify-content: space-around;
            gap: 0;
            flex-wrap: nowrap;
        }
        .complete-item {
            display: flex; align-items: center;
            gap: 12px; flex: 1 1 0; min-width: 0;
        }
        .complete-icon-circle {
            background: #e9f4f6; border-radius: 50%;
            width: 52px; height: 52px; flex-shrink: 0;
            display: flex; align-items: center;
            justify-content: center; font-size: 1.25rem;
        }
        .complete-text-label {
            font-family: 'Pretendard', sans-serif;
            font-size: 13px; color: #e9f4f6;
            font-weight: 400; margin: 0;
        }
        .complete-text-value {
            font-family: 'Pretendard', sans-serif;
            font-size: 16px; color: #e9f4f6;
            font-weight: 700; margin: 3px 0 0;
            white-space: nowrap;
        }
        .complete-sep {
            display: none;
        }

        /* ── 가이드 섹션 */
        .guide-title {
            font-family: 'Pretendard', sans-serif;
            font-size: 22px; font-weight: 800;
            color: #000; text-align: center;
            margin: 20px 0 14px;
        }
        .guide-card {
            background: #f9f9f9;
            border-radius: 8px;
            padding: 24px 24px 70px;
            text-align: center;
            height: 290px;
            box-sizing: border-box;
            display: flex; flex-direction: column;
            align-items: center; gap: 10px;
            margin-bottom: -58px;
        }
        .guide-card-emoji { font-size: 52px; margin-bottom: 0; }
        .guide-card-name {
            font-family: 'Pretendard', sans-serif;
            font-size: 17px; font-weight: 800;
            color: #000; margin: 0;
        }
        .guide-card-desc {
            font-family: 'Pretendard', sans-serif;
            font-size: 11px; color: #666;
            line-height: 1.65; margin: 0;
        }

        /* ── 가이드 버튼 */
        .st-key-landing_btn_daily,
        .st-key-landing_btn_coaching {
            padding: 0 24px 18px;
        }
        [data-testid="stBaseButton-primary"] {
            background: #072f48 !important;
            color: #ffffff !important;
            border-radius: 100px !important;
            height: 28px !important;
            font-family: 'Pretendard', sans-serif !important;
            font-size: 12px !important; font-weight: 800 !important;
            border: none !important;
        }
        [data-testid="stBaseButton-secondary"] {
            background: #ffffff !important;
            color: #072f48 !important;
            border: 1.8px solid #072f48 !important;
            border-radius: 100px !important;
            height: 28px !important;
            font-family: 'Pretendard', sans-serif !important;
            font-size: 12px !important; font-weight: 800 !important;
        }

        /* ── 반응형 */
        @media (max-width: 768px) {
            .landing-headline { font-size: 26px; }
            [data-testid="stForm"] { padding: 18px 20px 22px !important; }
            .complete-banner  { flex-direction: column; gap: 18px; }
            .complete-sep     { width: 100%; height: 1px; }
            .guide-card       { min-height: auto; }
        }
        </style>
        """.replace("__PRETENDARD_FONT_CSS__", _pretendard_font_css()).replace("__BG_B64__", bg_b64)
    st.markdown(
        css,
        unsafe_allow_html=True,
    )
