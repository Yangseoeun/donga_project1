"""Reusable Streamlit UI components."""

from html import escape

import streamlit as st

from core.schemas import SajuResult


def render_intro_panel() -> None:
    """
    Render the main introduction panel.

    Returns:
        None
    """
    st.markdown(
        """
        <div class="hero-panel">
            <div class="hero-copy">
                <p class="eyebrow">AI SAJU CONSULTATION</p>
                <h2>사주 리포트와 AI 상담을 하나의 흐름으로</h2>
                <p>
                    생년월일시를 입력하면 백엔드 A가 사주 컨텍스트를 만들고,
                    백엔드 B가 같은 컨텍스트를 바탕으로 대화형 상담을 이어갑니다.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_card(saju: SajuResult | None) -> None:
    """
    Render the current session status card.

    Args:
        saju (SajuResult | None): Current session saju result.

    Returns:
        None
    """
    if saju is None:
        body = """
            <h4>현재 연결 상태</h4>
            <p>아직 입력된 사주가 없습니다.</p>
            <p>일반 사주에서 먼저 계산해보세요.</p>
        """
    else:
        body = f"""
            <h4>현재 연결 상태</h4>
            <p>사주 계산 완료</p>
            <p>일간: {escape(saju.day_master or "미정")}</p>
            <p>용신: {escape(saju.yongsin or "미정")}</p>
        """

    st.markdown(
        f"<div class='saju-card compact-card'>{body}</div>",
        unsafe_allow_html=True,
    )


def render_quick_links() -> None:
    """
    Render page links.

    Returns:
        None
    """
    col1, col2 = st.columns(2)
    with col1:
        st.page_link("pages/1_일반_사주.py", label="일반 사주 리포트", icon="📋")
    with col2:
        st.page_link("pages/2_채팅_사주.py", label="AI 사주 채팅", icon="💬")


def render_connection_flow() -> None:
    """
    Render frontend-backend connection flow.

    Returns:
        None
    """
    flow1, flow2, flow3 = st.columns(3)
    with flow1:
        render_small_card("1. 입력", "프론트가 생년월일시를 받고 세션에 보관합니다.")
    with flow2:
        render_small_card("2. 계산", "백엔드 A가 사주 결과와 일반 리포트를 생성합니다.")
    with flow3:
        render_small_card("3. 상담", "백엔드 B가 사주 컨텍스트로 AI 답변을 생성합니다.")


def render_small_card(title: str, body: str) -> None:
    """
    Render a compact card.

    Args:
        title (str): Card title.
        body (str): Card body.

    Returns:
        None
    """
    st.markdown(
        f"""
        <div class="saju-card compact-card">
            <h4>{escape(title)}</h4>
            <p>{escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_pillars(saju: SajuResult) -> None:
    """
    Render the four saju pillars.

    Args:
        saju (SajuResult): Saju result.

    Returns:
        None
    """
    st.markdown(
        f"""
        <div class="metric-row">
            <div class="pillar-box"><span>연주</span><strong>{escape(saju.year_pillar)}</strong></div>
            <div class="pillar-box"><span>월주</span><strong>{escape(saju.month_pillar)}</strong></div>
            <div class="pillar-box"><span>일주</span><strong>{escape(saju.day_pillar)}</strong></div>
            <div class="pillar-box"><span>시주</span><strong>{escape(saju.hour_pillar)}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_saju_summary(saju: SajuResult) -> None:
    """
    Render day master, yongsin, and gisin metrics.

    Args:
        saju (SajuResult): Saju result.

    Returns:
        None
    """
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("일간", saju.day_master or "미정")
    with col2:
        st.metric("용신", saju.yongsin or "미정")
    with col3:
        st.metric("기신", saju.gisin or "미정")


def render_report_card(report: dict) -> None:
    """
    Render the general consultation report.

    Args:
        report (dict): Report returned by result_builder.

    Returns:
        None
    """
    fortune = report["fortune"]
    rows = [
        ("총운", fortune["general"]),
        ("재물운", fortune["wealth"]),
        ("연애운", fortune["love"]),
        ("오늘의 코디", fortune["daily_cody"]),
        ("행운의 식사 메뉴", fortune["lucky_menu"]),
    ]
    html = "".join(
        f"<div class='report-item'><h4>{escape(title)}</h4><p>{escape(body)}</p></div>"
        for title, body in rows
    )
    st.markdown(f"<div class='saju-card report-card'>{html}</div>", unsafe_allow_html=True)


def render_context_preview(saju: SajuResult) -> None:
    """
    Render backend context preview for the chat page.

    Args:
        saju (SajuResult): Saju result.

    Returns:
        None
    """
    with st.expander("백엔드에서 받은 사주 컨텍스트 보기"):
        left, right = st.columns(2)
        with left:
            render_pillars(saju)
        with right:
            st.bar_chart(saju.five_elements)


def render_chat_message(role: str, content: str) -> None:
    """
    Render a chat message bubble.

    Args:
        role (str): Message role.
        content (str): Message content.

    Returns:
        None
    """
    css_class = "chat-message-user" if role == "user" else "chat-message-ai"
    speaker = "나" if role == "user" else "AI 상담사"
    st.markdown(
        f"<div class='{css_class}'><strong>{speaker}</strong><br>{escape(content)}</div>",
        unsafe_allow_html=True,
    )
