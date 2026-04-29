"""Build display-ready reports from saju results."""

from core.schemas import GeneralReport, SajuResult


def _dominant_element(five_elements: dict[str, int]) -> str:
    """
    Return the strongest five element key.

    Args:
        five_elements (dict[str, int]): Five element counts.

    Returns:
        str: Dominant element key.
    """
    if not five_elements:
        return "earth"
    return max(five_elements, key=five_elements.get)


def build_general_report(saju: SajuResult) -> dict:
    """
    Build a general saju report without calling an LLM.

    Args:
        saju (SajuResult): Calculated saju result.

    Returns:
        dict: Display-ready report JSON.
    """
    dominant = _dominant_element(saju.five_elements)
    color_by_element = {
        "wood": "초록색이나 자연스러운 소재",
        "fire": "따뜻한 레드나 포인트 액세서리",
        "earth": "베이지, 브라운 계열의 안정적인 스타일",
        "metal": "화이트, 실버 계열의 깔끔한 스타일",
        "water": "네이비, 블랙 계열의 차분한 스타일",
    }
    menu_by_element = {
        "wood": "신선한 샐러드나 나물 비빔밥",
        "fire": "따뜻한 국물 요리나 구운 음식",
        "earth": "든든한 밥상이나 뿌리채소 요리",
        "metal": "담백한 생선구이나 깔끔한 한식",
        "water": "죽, 수프, 해산물 메뉴",
    }

    report = GeneralReport(
        pillars={
            "year": saju.year_pillar,
            "month": saju.month_pillar,
            "day": saju.day_pillar,
            "hour": saju.hour_pillar,
        },
        five_elements=saju.five_elements,
        day_master=saju.day_master,
        yongsin=saju.yongsin,
        gisin=saju.gisin,
        summary=saju.summary,
        fortune={
            "general": f"{saju.day_master}의 성향을 바탕으로 오늘은 균형과 속도 조절이 중요합니다.",
            "wealth": "큰 결정보다는 지출 흐름을 점검하고 작은 기회를 정리하기 좋은 날입니다.",
            "love": "상대의 반응을 단정하기보다 편안한 대화로 분위기를 여는 것이 좋습니다.",
            "daily_cody": color_by_element[dominant],
            "lucky_menu": menu_by_element[dominant],
        },
    )
    return report.model_dump()

##
# 이것은 서한진 테스트 입니다.#....
##  이제 다시 시작해보겠습니다.