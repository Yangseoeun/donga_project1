"""Pure saju calculation helpers for backend A."""

from datetime import datetime
from typing import Literal

from core.schemas import SajuResult


HEAVENLY_STEMS = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
EARTHLY_BRANCHES = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

STEM_ELEMENTS = {
    "갑": "wood",
    "을": "wood",
    "병": "fire",
    "정": "fire",
    "무": "earth",
    "기": "earth",
    "경": "metal",
    "신": "metal",
    "임": "water",
    "계": "water",
}

BRANCH_ELEMENTS = {
    "자": "water",
    "축": "earth",
    "인": "wood",
    "묘": "wood",
    "진": "earth",
    "사": "fire",
    "오": "fire",
    "미": "earth",
    "신": "metal",
    "유": "metal",
    "술": "earth",
    "해": "water",
}

ELEMENT_LABELS = {
    "wood": "목(木)",
    "fire": "화(火)",
    "earth": "토(土)",
    "metal": "금(金)",
    "water": "수(水)",
}

STEM_HANJA = {
    "갑": "甲",
    "을": "乙",
    "병": "丙",
    "정": "丁",
    "무": "戊",
    "기": "己",
    "경": "庚",
    "신": "辛",
    "임": "壬",
    "계": "癸",
}


def _make_pillar(index: int) -> str:
    """
    Build a sexagenary pillar from an index.

    Args:
        index (int): Zero-based cycle index.

    Returns:
        str: Pillar text such as 갑자.
    """
    return f"{HEAVENLY_STEMS[index % 10]}{EARTHLY_BRANCHES[index % 12]}"


def _get_year_pillar(birth_dt: datetime) -> str:
    """
    Calculate the year pillar with a simple ipchun boundary.

    Args:
        birth_dt (datetime): Birth datetime.

    Returns:
        str: Year pillar.
    """
    saju_year = birth_dt.year
    if (birth_dt.month, birth_dt.day) < (2, 4):
        saju_year -= 1
    return _make_pillar((saju_year - 1984) % 60)


def _get_month_pillar(birth_dt: datetime, year_pillar: str) -> str:
    """
    Calculate an approximate month pillar.

    Args:
        birth_dt (datetime): Birth datetime.
        year_pillar (str): Calculated year pillar.

    Returns:
        str: Month pillar.
    """
    month_branch_by_solar_month = {
        1: "축",
        2: "인",
        3: "묘",
        4: "진",
        5: "사",
        6: "오",
        7: "미",
        8: "신",
        9: "유",
        10: "술",
        11: "해",
        12: "자",
    }
    tiger_month_stem_by_year_stem = {
        "갑": "병",
        "기": "병",
        "을": "무",
        "경": "무",
        "병": "경",
        "신": "경",
        "정": "임",
        "임": "임",
        "무": "갑",
        "계": "갑",
    }
    branch = month_branch_by_solar_month[birth_dt.month]
    offset = (EARTHLY_BRANCHES.index(branch) - EARTHLY_BRANCHES.index("인")) % 12
    first_stem = tiger_month_stem_by_year_stem[year_pillar[0]]
    stem = HEAVENLY_STEMS[(HEAVENLY_STEMS.index(first_stem) + offset) % 10]
    return f"{stem}{branch}"


def _get_day_pillar(birth_dt: datetime) -> str:
    """
    Calculate day pillar from a fixed reference day.

    Args:
        birth_dt (datetime): Birth datetime.

    Returns:
        str: Day pillar.
    """
    reference = datetime(1984, 2, 2)
    days = (birth_dt.date() - reference.date()).days
    return _make_pillar(days % 60)


def _get_hour_pillar(birth_dt: datetime, day_pillar: str) -> str:
    """
    Calculate hour pillar from birth hour and day stem.

    Args:
        birth_dt (datetime): Birth datetime.
        day_pillar (str): Calculated day pillar.

    Returns:
        str: Hour pillar.
    """
    branch_index = ((birth_dt.hour + 1) // 2) % 12
    first_hour_stem_by_day_stem = {
        "갑": "갑",
        "기": "갑",
        "을": "병",
        "경": "병",
        "병": "무",
        "신": "무",
        "정": "경",
        "임": "경",
        "무": "임",
        "계": "임",
    }
    first_stem = first_hour_stem_by_day_stem[day_pillar[0]]
    stem = HEAVENLY_STEMS[(HEAVENLY_STEMS.index(first_stem) + branch_index) % 10]
    return f"{stem}{EARTHLY_BRANCHES[branch_index]}"


def _count_five_elements(pillars: list[str]) -> dict[str, int]:
    """
    Count five elements from stems and branches.

    Args:
        pillars (list[str]): Four saju pillars.

    Returns:
        dict[str, int]: Five element distribution.
    """
    counts = {"wood": 0, "fire": 0, "earth": 0, "metal": 0, "water": 0}
    for pillar in pillars:
        counts[STEM_ELEMENTS[pillar[0]]] += 1
        counts[BRANCH_ELEMENTS[pillar[1]]] += 1
    return counts


def _pick_balance_elements(counts: dict[str, int]) -> tuple[str, str]:
    """
    Pick simple yongsin and gisin candidates by element balance.

    Args:
        counts (dict[str, int]): Five element distribution.

    Returns:
        tuple[str, str]: Yongsin and gisin labels.
    """
    yongsin_key = min(counts, key=counts.get)
    gisin_key = max(counts, key=counts.get)
    return ELEMENT_LABELS[yongsin_key], ELEMENT_LABELS[gisin_key]


def calculate_saju(
    birth_dt: datetime,
    gender: Literal["female", "male", "unknown"] = "unknown",
) -> SajuResult:
    """
    Calculate a basic saju result from birth datetime.

    Args:
        birth_dt (datetime): User birth datetime.
        gender (Literal["female", "male", "unknown"]): User gender.

    Returns:
        SajuResult: Calculated saju result.
    """
    year_pillar = _get_year_pillar(birth_dt)
    month_pillar = _get_month_pillar(birth_dt, year_pillar)
    day_pillar = _get_day_pillar(birth_dt)
    hour_pillar = _get_hour_pillar(birth_dt, day_pillar)
    pillars = [year_pillar, month_pillar, day_pillar, hour_pillar]
    five_elements = _count_five_elements(pillars)
    yongsin, gisin = _pick_balance_elements(five_elements)
    day_stem = day_pillar[0]
    day_master = f"{day_stem}{STEM_ELEMENTS[day_stem].replace('wood', '목').replace('fire', '화').replace('earth', '토').replace('metal', '금').replace('water', '수')}({STEM_HANJA[day_stem]})"
    gender_note = "중립적인 흐름" if gender == "unknown" else "개인의 선택과 환경을 함께 보는 흐름"

    return SajuResult(
        year_pillar=year_pillar,
        month_pillar=month_pillar,
        day_pillar=day_pillar,
        hour_pillar=hour_pillar,
        five_elements=five_elements,
        day_master=day_master,
        yongsin=yongsin,
        gisin=gisin,
        summary=f"{day_master} 일간을 중심으로 {yongsin} 기운을 보완하면 균형이 좋아지는 {gender_note}입니다.",
    )
