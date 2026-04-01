from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SearchState:
    query: str = ''
    url: str = ''
    title: str = ''
    content: str = ''
    score: float | None = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ResearchState:
    search_history: list[SearchState] = field(default_factory=list)
    latest_summary: str = ''
    reflection_iteration: int = 0
    is_completed: bool = False


@dataclass
class ParagraphState:
    title: str = ''
    content: str = ''
    research: ResearchState = field(default_factory=ResearchState)
    order: int = 0


@dataclass
class State:
    query: str = ''
    report_title: str = ''
    paragraphs: list[ParagraphState] = field(default_factory=list)
    final_report: str = ''
    is_completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
