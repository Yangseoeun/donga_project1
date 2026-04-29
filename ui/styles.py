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
