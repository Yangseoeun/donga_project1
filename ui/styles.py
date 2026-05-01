"""Centralized Streamlit CSS."""

import streamlit as st


def apply_custom_styles() -> None:
    """
    Apply custom CSS used by all Streamlit pages.

    Returns:
        None
    """
    st.markdown(
        """
        <style>
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
        """,
        unsafe_allow_html=True,
    )


def apply_landing_styles() -> None:
    """
    랜딩 페이지(app.py) 전용 CSS.
    Figma 디자인 토큰 기반으로 작성. 다른 페이지에서는 호출하지 않는다.
    """
    st.markdown(
        """
        <style>
        /* ── Pretendard 폰트 */
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.8/dist/web/static/pretendard.css');

        /* ── 사이드바 숨김 */
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"] { display: none; }
        [data-testid="stHeader"] { background: transparent; }

        /* ── 앱 배경 (conic gradient → e9f4f6 페이드) */
        .stApp,
        [data-testid="stAppViewContainer"] > .main {
            background:
                conic-gradient(
                    from 180deg at 50% 0%,
                    rgba(182, 226, 214, 0.90) 0deg,
                    rgba(209, 238, 237, 0.75) 90deg,
                    rgba(233, 244, 246, 0.60) 180deg,
                    rgba(209, 238, 237, 0.75) 270deg,
                    rgba(182, 226, 214, 0.90) 360deg
                ),
                linear-gradient(
                    180deg,
                    rgba(229, 246, 245, 0.60) 0%,
                    rgba(233, 244, 246, 1.00) 55%,
                    rgba(233, 244, 246, 1.00) 100%
                ) !important;
            font-family: 'Pretendard', sans-serif;
        }

        /* ── 랜딩 히어로 */
        .landing-hero {
            padding: 52px 24px 40px;
            text-align: center;
        }
        .landing-logo-badge {
            display: inline-block;
            font-size: 13px; font-weight: 700;
            color: #2a6a7a; letter-spacing: 2.5px;
            text-transform: uppercase; margin-bottom: 20px;
        }
        .landing-headline {
            font-family: 'Pretendard', sans-serif;
            font-size: 40px; font-weight: 700;
            color: #000; letter-spacing: -0.02em;
            margin: 0 0 14px; line-height: 1.25;
        }
        .landing-brand-line {
            font-family: 'Pretendard', sans-serif;
            font-size: 18px; color: #333; margin: 0;
            line-height: 1.6;
        }

        /* ── 폼 설명 */
        .form-desc {
            font-family: 'Pretendard', sans-serif;
            font-size: 15px; color: #555;
            text-align: center; margin-bottom: 18px;
        }

        /* ── 폼 컨테이너 카드 (glassmorphism) */
        [data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.6) !important;
            border-radius: 16px !important;
            padding: 24px 32px !important;
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
            backdrop-filter: blur(8px) !important;
        }

        /* ── Streamlit 입력 필드 → Figma 스타일 오버라이드 */
        [data-testid="stTextInput"] input {
            border-radius: 16px !important;
            border: 2px solid #d5d5d5 !important;
            height: 56px !important;
            font-family: 'Pretendard', sans-serif !important;
            font-size: 16px !important;
            background: #ffffff !important;
        }
        [data-testid="stDateInput"] input {
            border-radius: 16px !important;
            border: 2px solid #d5d5d5 !important;
            font-family: 'Pretendard', sans-serif !important;
            background: #ffffff !important;
        }
        [data-testid="stSelectbox"] > div > div[data-baseweb="select"] > div:first-child {
            border-radius: 16px !important;
            border: 2px solid #d5d5d5 !important;
            background: #ffffff !important;
            min-height: 52px !important;
        }

        /* ── 폼 제출 버튼 */
        [data-testid="stFormSubmitButton"] > button {
            background: #072f48 !important;
            color: #ffffff !important;
            border-radius: 100px !important;
            height: 52px !important;
            font-family: 'Pretendard', sans-serif !important;
            font-size: 17px !important;
            font-weight: 700 !important;
            border: none !important;
            margin-top: 8px;
        }

        /* ── 완료 배너 (다크 네이비) */
        .complete-banner {
            background: #072f48;
            border-radius: 16px;
            padding: 28px 36px;
            margin: 20px 0 8px;
            display: flex;
            align-items: center;
            justify-content: space-around;
            gap: 8px;
            flex-wrap: wrap;
        }
        .complete-item {
            display: flex; align-items: center;
            gap: 14px; flex: 1; min-width: 120px;
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
            font-size: 20px; color: #e9f4f6;
            font-weight: 700; margin: 3px 0 0;
            white-space: nowrap;
        }
        .complete-sep {
            width: 1px; height: 52px;
            background: rgba(233, 244, 246, 0.22);
            flex-shrink: 0;
        }

        /* ── 가이드 섹션 */
        .guide-title {
            font-family: 'Pretendard', sans-serif;
            font-size: 30px; font-weight: 700;
            color: #000; text-align: center;
            margin: 28px 0 18px;
        }
        .guide-card {
            background: #f9f9f9;
            border-radius: 16px;
            padding: 32px 24px 20px;
            text-align: center;
            min-height: 280px;
            display: flex; flex-direction: column;
            align-items: center; gap: 10px;
            margin-bottom: 10px;
        }
        .guide-card-emoji { font-size: 68px; margin-bottom: 2px; }
        .guide-card-name {
            font-family: 'Pretendard', sans-serif;
            font-size: 24px; font-weight: 700;
            color: #000; margin: 0;
        }
        .guide-card-desc {
            font-family: 'Pretendard', sans-serif;
            font-size: 15px; color: #666;
            line-height: 1.65; margin: 0;
        }

        /* ── 가이드 버튼 */
        [data-testid="stBaseButton-primary"] {
            background: #072f48 !important;
            color: #ffffff !important;
            border-radius: 100px !important;
            height: 50px !important;
            font-family: 'Pretendard', sans-serif !important;
            font-size: 17px !important; font-weight: 700 !important;
            border: none !important;
        }
        [data-testid="stBaseButton-secondary"] {
            background: #ffffff !important;
            color: #072f48 !important;
            border: 2.5px solid #072f48 !important;
            border-radius: 100px !important;
            height: 50px !important;
            font-family: 'Pretendard', sans-serif !important;
            font-size: 17px !important; font-weight: 700 !important;
        }

        /* ── 반응형 */
        @media (max-width: 768px) {
            .landing-headline { font-size: 26px; }
            .complete-banner  { flex-direction: column; gap: 18px; }
            .complete-sep     { width: 100%; height: 1px; }
            .guide-card       { min-height: auto; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
