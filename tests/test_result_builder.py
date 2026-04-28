"""Tests for backend A report builder."""

from datetime import datetime

from core.result_builder import build_general_report
from core.saju_calculator import calculate_saju


def test_build_general_report_contains_expected_keys():
    """General report returns display-ready sections."""
    saju = calculate_saju(datetime(1997, 3, 24, 9, 30))
    report = build_general_report(saju)

    assert report["pillars"]["year"] == saju.year_pillar
    assert report["five_elements"] == saju.five_elements
    assert "general" in report["fortune"]
    assert "daily_cody" in report["fortune"]
    assert "lucky_menu" in report["fortune"]
