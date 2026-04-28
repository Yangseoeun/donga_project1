"""Tests for backend A saju calculation."""

from datetime import datetime

from core.saju_calculator import calculate_saju
from core.schemas import SajuResult


def test_calculate_saju_returns_schema():
    """Calculation returns a SajuResult with four pillars."""
    result = calculate_saju(datetime(1997, 3, 24, 9, 30), "unknown")

    assert isinstance(result, SajuResult)
    assert len(result.year_pillar) == 2
    assert len(result.month_pillar) == 2
    assert len(result.day_pillar) == 2
    assert len(result.hour_pillar) == 2


def test_calculate_saju_counts_eight_characters():
    """Five element counts represent eight pillar characters."""
    result = calculate_saju(datetime(2000, 1, 1, 0, 0), "female")

    assert set(result.five_elements) == {"wood", "fire", "earth", "metal", "water"}
    assert sum(result.five_elements.values()) == 8


def test_calculate_saju_uses_ipchun_boundary():
    """Dates before February 4 use the previous saju year."""
    before = calculate_saju(datetime(1984, 2, 3, 12, 0), "male")
    after = calculate_saju(datetime(1984, 2, 4, 12, 0), "male")

    assert before.year_pillar != after.year_pillar
    assert after.year_pillar == "갑자"
