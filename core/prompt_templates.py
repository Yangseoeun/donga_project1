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

# 모든 모드에 공통 적용되는 응답 형식 지시
# build_system_prompt() 에서 시스템 프롬프트 끝에 자동으로 추가됩니다.
_RESPONSE_FORMAT_INSTRUCTION = """
사용자가 질문하면 반드시 아래 형식으로 답변하세요.

**전략 핵심**: [사주 오행 기준 1줄 핵심 전략]

**衣 (의상 코칭)**:
- **코디/색상**: [오행 보완 색상 및 코디 팁]
- **행운의 아이템**: [액세서리 및 소품]
- **피해야 할 의상**: [기운을 낮추는 의상]

**食 (푸드 코칭)**:
- **식사/회식**: [추천 메뉴]
- **음료/주류**: [추천 음료 및 페어링]
- **피해야 할 음식**: [기운을 낮추는 음식·음료]

**宙 (공간 코칭)**:
- **공간/인테리어**: [업무·활동 효율 공간 제안]
- **행운의 방향**: [방향]
- **피해야 할 장소**: [기운을 낮추는 장소]

**행동전략 코칭**:
- **커뮤니케이션 팁**: [구체적인 대화·관계 전략]
- **네트워킹 팁**: [연결·확장 전략]

답변 마지막에 반드시 이 문장을 추가하세요:
"혹시 **비즈니스 / 연애 / 재물 / 학업 / 건강** 중 다른 분야도 궁금하신가요?"

사용자가 더 이상 궁금한 분야가 없다고 하면 짧고 강렬한 격려 한 문장으로 대화를 마무리하세요.
"""

# 모드 버튼 클릭 시 채팅창에 즉시 표시되는 인사말
# pages/2_채팅_사주.py 에서 import 하여 사용합니다.
MODE_GREETING: dict[str, str] = {
    "business": (
        "귀하의 사주에 깃든 업무의 기운을 살피니,\n"
        "중요한 결단의 순간이 다가오고 있음이 느껴집니다.\n\n"
        "오늘 어떤 구체적인 비즈니스 이벤트를 앞두고 계신가요?\n"
        "핵심 발표, 계약 협상, 팀 설득 — 상황을 알려주시면\n"
        "오행 데이터를 기반으로 오늘 당신에게 가장 유리한 전략을 설계해 드리겠습니다."
    ),
    "love": (
        "귀하의 사주에서 관계의 기운을 읽어내니,\n"
        "감정의 흐름이 분기점에 서 있는 것이 보입니다.\n\n"
        "오늘 어떤 관계에서 어떤 상황이 펼쳐지고 있나요?\n"
        "새로운 만남, 오래된 감정의 정리, 혹은 중요한 대화 —\n"
        "구체적인 맥락을 공유해 주시면 당신의 에너지가 가장 빛나는 방향을 찾아드리겠습니다."
    ),
    "wealth": (
        "귀하의 사주에 흐르는 재물의 기운을 분석하니,\n"
        "움직임과 정착 사이에서 선택이 필요한 시점임이 감지됩니다.\n\n"
        "오늘 어떤 재무적 결정을 앞두고 계신가요?\n"
        "투자 진입, 계약 체결, 지출 조율 — 상황을 알려주시면\n"
        "오행의 흐름으로 지금 가장 유리한 재물 전략을 도출해 드리겠습니다."
    ),
    "study": (
        "귀하의 사주에서 지식과 성취의 기운을 읽으니,\n"
        "집중력과 방향성이 승패를 가를 시기가 다가오고 있습니다.\n\n"
        "지금 어떤 도전 앞에 서 계신가요?\n"
        "시험 준비, 자격증 취득, 새로운 커리어 학습 —\n"
        "상황을 공유해 주시면 오늘의 기운에 맞는 최적의 집중 전략을 설계해 드리겠습니다."
    ),
    "health": (
        "귀하의 사주에 담긴 생체 리듬의 기운을 살피니,\n"
        "몸과 마음이 균형을 요청하고 있는 신호가 보입니다.\n\n"
        "오늘 어떤 부분에서 에너지의 이상을 느끼고 계신가요?\n"
        "체력 저하, 수면 문제, 또는 지속적인 피로감 —\n"
        "구체적인 증상을 알려주시면 오행 기반의 회복 전략을 제안해 드리겠습니다."
    ),
}


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
        str: System prompt with saju context and response format instruction.
    """
    base_prompt = PROMPT_BY_MODE.get(mode, GENERAL_SYSTEM_PROMPT)
    saju_ctx = format_saju_context(saju)
    # general 모드는 자유 형식 유지, 나머지 모드는 구조화 출력 + 타 분야 질문 지시 추가
    if mode == "general":
        return f"{base_prompt.strip()}\n\n{saju_ctx.strip()}"
    return f"{base_prompt.strip()}\n\n{saju_ctx.strip()}\n\n{_RESPONSE_FORMAT_INSTRUCTION.strip()}"


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


# ===========================================================================
# 오행 기반 '부족 기운 보완형 전략 처방전' 파이프라인
# (백엔드 B 전담 — 백엔드 A·프론트 코드 수정 없이 독립 추가)
#
# 흐름:
#   SajuResult.five_elements
#     → find_weakest_elements()   부족 원소 탐지
#     → generate_prescription()   카테고리 처방 클래스 선택
#     → _BasePrescription.build() 4대 영역(衣食宙행동) 딕셔너리 반환
# ===========================================================================

# ---------------------------------------------------------------------------
# 오행 속성 정의표
# 각 원소의 보완 색상·아이템·음식·공간·행운 방향을 정의한 데이터 소스.
# 처방전 클래스들이 이 딕셔너리를 참조해 처방 내용을 생성합니다.
# ---------------------------------------------------------------------------

ELEMENT_PROFILE: dict[str, dict] = {
    "木": {
        "name": "목(木)",
        "quality": "직관·추진력·성장",
        "colors": ["초록색", "청록색"],
        "avoid_colors": ["흰색", "은색"],
        "lucky_items": ["나무 소품", "식물 액세서리", "청록 스카프"],
        "avoid_items": ["금속성 장신구 과다 착용"],
        "foods": ["신맛 음식", "새싹 채소", "녹차", "부추"],
        "avoid_foods": ["매운 음식", "흰 쌀밥 위주 단조 식단"],
        "drinks": ["녹차", "민트 티", "청포도 주스"],
        "spaces": ["동쪽 창가", "자연 채광 카페", "공원 근처 작업 공간"],
        "avoid_spaces": ["지하 밀폐 공간", "서향 어두운 사무실"],
        "lucky_direction": "동쪽",
    },
    "火": {
        "name": "화(火)",
        "quality": "매력·열정·표현력",
        "colors": ["빨간색", "주황색", "핑크색"],
        "avoid_colors": ["검정색", "남색"],
        "lucky_items": ["빨간 포인트 아이템", "골드 액세서리", "따뜻한 톤 스카프"],
        "avoid_items": ["검은색 계열 전체 착장"],
        "foods": ["쓴맛 음식", "통곡물", "홍삼", "토마토"],
        "avoid_foods": ["찬 음식 과다", "날 음식 위주 식단"],
        "drinks": ["생강차", "루이보스 티", "레드 와인"],
        "spaces": ["남향 밝은 공간", "카페 창가", "따뜻한 조명 룸"],
        "avoid_spaces": ["북향 어두운 방", "지하 공간"],
        "lucky_direction": "남쪽",
    },
    "土": {
        "name": "토(土)",
        "quality": "신뢰·안정·지구력",
        "colors": ["노란색", "황토색", "베이지색"],
        "avoid_colors": ["초록색", "청색 계열"],
        "lucky_items": ["도자기·세라믹 소품", "황토색 파우치", "천연 소재 의류"],
        "avoid_items": ["과도한 청록·초록 계열 착장"],
        "foods": ["단맛 음식", "고구마", "땅콩", "두부", "견과류"],
        "avoid_foods": ["과도한 신맛 음식", "생채소 과다 섭취"],
        "drinks": ["꿀물", "대추차", "곡물 음료"],
        "spaces": ["중앙 위치 작업 공간", "정돈된 도서관", "안정적인 단골 카페"],
        "avoid_spaces": ["소란스럽고 변동이 잦은 공간"],
        "lucky_direction": "중앙(사방)",
    },
    "金": {
        "name": "금(金)",
        "quality": "냉철함·결단력·매듭",
        "colors": ["흰색", "은색", "회색", "금색"],
        "avoid_colors": ["빨간색", "주황색"],
        "lucky_items": ["은색 액세서리", "미니멀 금속 소품", "흰색 셔츠"],
        "avoid_items": ["화려한 컬러 레이어링"],
        "foods": ["매운맛 음식", "생강", "무", "배"],
        "avoid_foods": ["과도한 단맛", "기름진 튀김류"],
        "drinks": ["페퍼민트 티", "애플 사이다", "화이트 와인"],
        "spaces": ["서향 정돈된 사무실", "미니멀한 작업 공간", "조용한 독서실"],
        "avoid_spaces": ["어수선한 공간", "과열된 남향 환경"],
        "lucky_direction": "서쪽",
    },
    "水": {
        "name": "수(水)",
        "quality": "유연함·지혜·적응력",
        "colors": ["검정색", "남색", "파란색"],
        "avoid_colors": ["노란색", "황토색"],
        "lucky_items": ["파란 계열 액세서리", "유리 소품", "물 모티프 아이템"],
        "avoid_items": ["황토·베이지 전체 착장"],
        "foods": ["짠맛 음식", "검은콩", "미역", "블루베리"],
        "avoid_foods": ["과도한 단맛", "기름진 튀김류"],
        "drinks": ["블랙커피", "블루베리 스무디", "미네랄 워터"],
        "spaces": ["북향 서늘한 공간", "물 뷰 카페", "수변 공원"],
        "avoid_spaces": ["과열된 남향 공간"],
        "lucky_direction": "북쪽",
    },
}


# ---------------------------------------------------------------------------
# 오행 부족 기운 탐지
# SajuResult.five_elements (세션 스테이트에서 전달) 을 분석해
# 수치가 낮은 원소를 순서대로 반환합니다.
# ---------------------------------------------------------------------------


def find_weakest_elements(
    ohaeng: dict[str, int],
    top_n: int = 2,
) -> list[str]:
    """
    오행 분포에서 수치가 가장 낮은 원소를 오름차순으로 반환합니다.

    Args:
        ohaeng: SajuResult.five_elements 딕셔너리.
                예) {"木": 2, "火": 0, "土": 3, "金": 1, "水": 1}
        top_n:  반환할 부족 원소 개수 (기본 2개).

    Returns:
        부족한 원소 리스트 (수치 오름차순). 예) ["火", "金"]
    """
    # 정의된 5개 원소만 필터링해 안전하게 정렬
    valid = {k: ohaeng.get(k, 0) for k in ELEMENT_PROFILE}
    return sorted(valid, key=lambda e: valid[e])[:top_n]


# ---------------------------------------------------------------------------
# 카테고리별 전략 처방전 클래스
# _BasePrescription 을 상속받아 각 상담 영역의 핵심 오행 쌍을 정의하고,
# build() 메서드에서 4대 영역(衣食宙행동) 처방 딕셔너리를 생성합니다.
# ---------------------------------------------------------------------------


class _BasePrescription:
    """처방전 기본 클래스: 4대 영역(衣食宙행동) 처방 딕셔너리를 생성합니다."""

    KEY_ELEMENTS: tuple[str, str] = ("", "")  # 서브클래스에서 오버라이드
    CATEGORY_LABEL: str = ""
    ACTION_TIPS: dict[str, str] = {}  # 오행 원소 → 행동 전략 문구

    def build(self, weakest: list[str], ohaeng: dict[str, int]) -> dict:
        """
        부족 기운 목록을 받아 4대 영역 처방전 딕셔너리를 반환합니다.

        Args:
            weakest: find_weakest_elements() 결과 리스트.
            ohaeng:  전체 오행 분포 (표시용).

        Returns:
            衣·食·宙·행동전략·격려_메시지를 포함한 처방전 딕셔너리.
        """
        # 핵심 오행 중 실제로 부족한 원소를 1순위 보완 대상으로 삼음.
        # 해당 카테고리의 핵심 오행이 모두 충분한 경우엔 첫 번째 핵심 원소를 기본값으로 사용.
        targets = [e for e in self.KEY_ELEMENTS if e in weakest] or list(self.KEY_ELEMENTS)
        primary = targets[0]
        profile = ELEMENT_PROFILE[primary]

        return {
            "category": self.CATEGORY_LABEL,
            "weakest_elements": weakest,
            "ohaeng_distribution": ohaeng,
            "primary_boost": primary,
            "衣": {
                "보완_색상": profile["colors"],
                "행운_아이템": profile["lucky_items"],
                "피해야_할_의상": profile["avoid_items"],
            },
            "食": {
                "에너지_상승_메뉴": profile["foods"],
                "음료_페어링": profile["drinks"],
                "피해야_할_음식": profile["avoid_foods"],
            },
            "宙": {
                "추천_공간": profile["spaces"],
                "행운의_방향": profile["lucky_direction"],
                "피해야_할_장소": profile["avoid_spaces"],
            },
            "행동전략": self.ACTION_TIPS.get(
                primary,
                f"{profile['name']} 기운을 높이는 활동에 집중하세요.",
            ),
            "격려_메시지": build_encouragement_message(self.CATEGORY_LABEL),
        }


class BusinessPrescription(_BasePrescription):
    """비즈니스: 신뢰(土)와 냉철함(金)의 밸런스 전략."""

    KEY_ELEMENTS = ("土", "金")
    CATEGORY_LABEL = "비즈니스"
    ACTION_TIPS = {
        "土": (
            "미팅 전 상대방의 배경과 니즈를 철저히 파악하세요. "
            "말보다 듣는 시간을 늘리면 신뢰가 쌓입니다. "
            "약속한 마감과 수치를 반드시 지키세요."
        ),
        "金": (
            "협상 전 '이것만은 양보 못 한다'는 핵심 조건을 미리 정하세요. "
            "감정적 동의 대신 계약서·메일로 결과를 명문화하세요. "
            "불필요한 회의를 줄이고 결정 속도를 높이세요."
        ),
    }


class LovePrescription(_BasePrescription):
    """연애: 매력(火)과 유연한 흐름(水)의 전략."""

    KEY_ELEMENTS = ("火", "水")
    CATEGORY_LABEL = "연애"
    ACTION_TIPS = {
        "火": (
            "오늘 대화에서 상대의 이름을 3번 이상 불러주세요. "
            "작은 칭찬을 구체적으로 표현하면 매력 지수가 오릅니다. "
            "밝은 색상 옷차림이 첫인상을 높여줍니다."
        ),
        "水": (
            "상대의 속도에 맞춰 대화하세요. 먼저 결론 짓지 마세요. "
            "침묵을 두려워하지 말고, 여백을 줘야 상대가 다가옵니다. "
            "계획을 느슨하게 잡아 즉흥적인 순간을 허용하세요."
        ),
    }


class WealthPrescription(_BasePrescription):
    """재물: 직관(木)과 냉정한 매듭(金)의 전략."""

    KEY_ELEMENTS = ("木", "金")
    CATEGORY_LABEL = "재물"
    ACTION_TIPS = {
        "木": (
            "새벽 혹은 이른 아침에 하루 재물 계획을 세우세요. "
            "직관이 오면 24시간 안에 소규모 테스트를 실행해 보세요. "
            "성장 가능성 있는 분야에 작은 씨앗을 먼저 뿌리세요."
        ),
        "金": (
            "지출 내역을 주 1회 반드시 정산하세요. "
            "수익 목표가 달성되면 욕심 부리지 말고 일단 매듭 짓는 연습을 하세요. "
            "계약·투자 결정은 감정이 아닌 숫자로만 판단하세요."
        ),
    }


class StudyPrescription(_BasePrescription):
    """학업/업무: 지구력(土)과 추진력(木)의 돌파 전략."""

    KEY_ELEMENTS = ("土", "木")
    CATEGORY_LABEL = "학업/업무"
    ACTION_TIPS = {
        "土": (
            "공부·업무 루틴을 요일별로 고정하세요. "
            "25분 집중 + 5분 휴식 사이클(포모도로)로 체력을 아끼세요. "
            "진도를 눈에 보이게 기록하면 지구력이 강해집니다."
        ),
        "木": (
            "큰 과제를 '3일 단위' 마일스톤으로 쪼개세요. "
            "아이디어가 떠오르면 즉시 메모하고 바로 초안을 시작하세요. "
            "완벽주의를 내려놓고 '일단 60점짜리 초고'를 먼저 완성하세요."
        ),
    }


class HealthPrescription(_BasePrescription):
    """건강: 유연함(水)과 기초 체력(土)의 회복 전략."""

    KEY_ELEMENTS = ("水", "土")
    CATEGORY_LABEL = "건강"
    ACTION_TIPS = {
        "水": (
            "하루 물 섭취량 1.5L를 채우세요. "
            "스트레칭·요가 등 유연성 운동을 매일 10분 추가하세요. "
            "잠들기 1시간 전 화면을 끄고 이완하는 시간을 가지세요."
        ),
        "土": (
            "규칙적인 식사 시간을 지키세요. "
            "걷기·스쿼트 등 하체 근력 운동으로 기초 체력을 다지세요. "
            "같은 시간에 잠들고 일어나는 수면 루틴을 2주 이상 유지하세요."
        ),
    }


# 카테고리 키 → 처방전 인스턴스 매핑
_PRESCRIPTION_MAP: dict[str, _BasePrescription] = {
    "business": BusinessPrescription(),
    "love":     LovePrescription(),
    "wealth":   WealthPrescription(),
    "study":    StudyPrescription(),
    "health":   HealthPrescription(),
}


# ---------------------------------------------------------------------------
# 격려 메시지 생성기
# 처방전 마무리에 카테고리별 긍정적인 격려 문구를 포함합니다.
# ---------------------------------------------------------------------------

_ENCOURAGEMENT: dict[str, str] = {
    "비즈니스": (
        "오늘의 처방을 실행한 당신은 이미 절반을 이긴 겁니다. "
        "신뢰와 결단력으로 반드시 승리하세요!"
    ),
    "연애": (
        "당신의 에너지가 빛나는 오늘, 그 진심이 반드시 전해질 겁니다. "
        "자신감 있게 나아가세요!"
    ),
    "재물": (
        "직관과 냉정함이 당신 편입니다. "
        "오늘의 작은 실행이 내일의 큰 결실이 됩니다. 파이팅!"
    ),
    "학업/업무": (
        "한 걸음씩 쌓은 노력은 배신하지 않습니다. "
        "오늘 하루도 당신의 성장을 응원합니다!"
    ),
    "건강": (
        "몸이 회복되면 모든 것이 달라집니다. "
        "오늘 처방을 실천한 당신, 이미 건강을 되찾는 중입니다. 화이팅!"
    ),
}


def build_encouragement_message(category_label: str) -> str:
    """카테고리에 맞는 격려 메시지를 반환합니다."""
    return _ENCOURAGEMENT.get(
        category_label,
        "오늘의 처방을 실천하는 당신을 응원합니다. 반드시 좋은 결과가 찾아옵니다!",
    )


# ---------------------------------------------------------------------------
# 메인 처방전 생성 함수 (UI 또는 chat_engine 에서 호출)
# ---------------------------------------------------------------------------


def generate_prescription(ohaeng: dict[str, int], case: str) -> dict:
    """
    오행 분포와 상담 케이스를 받아 4대 영역 전략 처방전을 반환합니다.

    Args:
        ohaeng: SajuResult.five_elements 딕셔너리.
                예) {"木": 2, "火": 0, "土": 3, "金": 1, "水": 1}
        case:   상담 케이스.
                "business" | "love" | "wealth" | "study" | "health"

    Returns:
        아래 키를 포함한 처방전 딕셔너리::

            {
                "category": str,
                "weakest_elements": list[str],
                "ohaeng_distribution": dict[str, int],
                "primary_boost": str,
                "衣": {"보완_색상": ..., "행운_아이템": ..., "피해야_할_의상": ...},
                "食": {"에너지_상승_메뉴": ..., "음료_페어링": ..., "피해야_할_음식": ...},
                "宙": {"추천_공간": ..., "행운의_방향": ..., "피해야_할_장소": ...},
                "행동전략": str,
                "격려_메시지": str,
            }

    Raises:
        ValueError: case 가 지원하지 않는 값인 경우.

    Example::

        >>> result = generate_prescription(
        ...     {"木": 2, "火": 0, "土": 3, "金": 1, "水": 1},
        ...     "love",
        ... )
        >>> result["primary_boost"]
        '火'
    """
    if case not in _PRESCRIPTION_MAP:
        supported = list(_PRESCRIPTION_MAP.keys())
        raise ValueError(f"지원하지 않는 케이스: '{case}'. 지원 목록: {supported}")

    weakest = find_weakest_elements(ohaeng, top_n=2)
    return _PRESCRIPTION_MAP[case].build(weakest=weakest, ohaeng=ohaeng)
