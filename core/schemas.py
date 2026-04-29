"""Shared data schemas for backend A and backend B."""

from typing import Literal

from pydantic import BaseModel, Field


ConsultationMode = Literal["general", "business", "love", "wealth", "study", "health"]


class BirthProfile(BaseModel):
    """User birth input retained only in Streamlit session state."""

    name: str = ""
    gender: Literal["female", "male", "unknown"] = "unknown"
    birth_date: str
    birth_time: str
    calendar_type: Literal["solar", "lunar"] = "solar"


class SajuResult(BaseModel):
    """Canonical saju result shared by calculation, report, and chat modules."""

    year_pillar: str = Field(..., description="연주")
    month_pillar: str = Field(..., description="월주")
    day_pillar: str = Field(..., description="일주")
    hour_pillar: str = Field(..., description="시주")
    five_elements: dict[str, int] = Field(default_factory=dict)
    day_master: str = ""
    yongsin: str = ""
    gisin: str = ""
    summary: str = ""


class GeneralReport(BaseModel):
    """Display-ready general saju report."""

    pillars: dict[str, str] = Field(default_factory=dict)
    five_elements: dict[str, int] = Field(default_factory=dict)
    day_master: str = ""
    yongsin: str = ""
    gisin: str = ""
    summary: str = ""
    fortune: dict[str, str] = Field(default_factory=dict)


class ChatMessage(BaseModel):
    """OpenAI-compatible chat message."""

    role: Literal["system", "user", "assistant"]
    content: str
