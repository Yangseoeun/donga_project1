"""Prompt templates and message builders for saju consultation modes."""

from core.schemas import ConsultationMode, SajuResult


GENERAL_SYSTEM_PROMPT = """
당신은 전통 사주 이론을 현대적인 언어로 설명하는 AI 사주 상담사입니다.
사용자의 사주 컨텍스트를 근거로 말하되, 단정적인 예언이나 공포 조장은 피하세요.
답변은 따뜻하고 구체적으로 작성하고, 선택 가능한 행동 조언을 포함하세요.
"""

BUSINESS_SYSTEM_PROMPT = """
당신은 커리어와 사업운을 중심으로 상담하는 AI 사주 상담사입니다.
재물, 협업, 의사결정, 실행 타이밍을 현실적인 조언으로 풀어주세요.
투자 수익을 보장하거나 법률, 세무, 금융 전문가의 조언을 대체하지 마세요.
"""

LOVE_SYSTEM_PROMPT = """
당신은 연애운과 인간관계를 상담하는 AI 사주 상담사입니다.
상대방을 조종하는 방식이 아니라 자기 이해, 대화 방식, 관계 균형을 중심으로 답하세요.
"""

HEALTH_SYSTEM_PROMPT = """
당신은 생활 리듬과 컨디션 관리를 중심으로 상담하는 AI 사주 상담사입니다.
의학적 진단을 하지 말고, 건강 문제는 전문가 상담을 권하세요.
"""

WEALTH_SYSTEM_PROMPT = """
당신은 재물운과 소비 흐름을 중심으로 상담하는 AI 사주 상담사입니다.
수입, 지출, 저축, 투자 성향을 현실적인 생활 조언으로 풀어주세요.
수익 보장이나 금융 전문가 조언처럼 말하지 말고, 선택 전에 점검할 기준을 제안하세요.
"""

STUDY_SYSTEM_PROMPT = """
당신은 학업, 시험, 집중력, 성장 루틴을 중심으로 상담하는 AI 사주 상담사입니다.
사용자의 사주 흐름을 바탕으로 오늘의 공부 방식, 우선순위, 컨디션 관리 팁을 구체적으로 제안하세요.
결과를 단정하지 말고 실행 가능한 작은 행동으로 안내하세요.
"""
#
#git test git test
# test


PROMPT_BY_MODE: dict[str, str] = {
    "general": GENERAL_SYSTEM_PROMPT,
    "business": BUSINESS_SYSTEM_PROMPT,
    "love": LOVE_SYSTEM_PROMPT,
    "wealth": WEALTH_SYSTEM_PROMPT,
    "study": STUDY_SYSTEM_PROMPT,
    "health": HEALTH_SYSTEM_PROMPT,
}


def format_saju_context(saju: SajuResult) -> str:
    """
    Convert a saju result into compact prompt context.

    Args:
        saju (SajuResult): Calculated saju result.

    Returns:
        str: Human-readable context block.
    """
    elements = ", ".join(
        f"{name}: {count}" for name, count in saju.five_elements.items()
    )
    return f"""
[사용자 사주 컨텍스트]
- 연주: {saju.year_pillar}
- 월주: {saju.month_pillar}
- 일주: {saju.day_pillar}
- 시주: {saju.hour_pillar}
- 오행 분포: {elements or "미정"}
- 일간: {saju.day_master or "미정"}
- 용신: {saju.yongsin or "미정"}
- 기신: {saju.gisin or "미정"}
- 요약: {saju.summary or "아직 요약 없음"}
"""


def build_system_prompt(saju: SajuResult, mode: ConsultationMode = "general") -> str:
    """
    Build the system prompt for a consultation mode.

    Args:
        saju (SajuResult): Calculated saju result.
        mode (ConsultationMode): Consultation mode.

    Returns:
        str: System prompt with saju context.
    """
    base_prompt = PROMPT_BY_MODE.get(mode, GENERAL_SYSTEM_PROMPT)
    return f"{base_prompt.strip()}\n\n{format_saju_context(saju).strip()}"


def build_messages(
    system_prompt: str,
    history: list[dict[str, str]],
    user_input: str,
) -> list[dict[str, str]]:
    """
    Build OpenAI-compatible messages from system, history, and latest input.

    Args:
        system_prompt (str): System prompt.
        history (list[dict[str, str]]): Prior chat messages.
        user_input (str): Latest user question.

    Returns:
        list[dict[str, str]]: OpenAI-compatible messages.
    """
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(
        message
        for message in history
        if message.get("role") in {"user", "assistant"} and message.get("content")
    )
    messages.append({"role": "user", "content": user_input})
    return messages
