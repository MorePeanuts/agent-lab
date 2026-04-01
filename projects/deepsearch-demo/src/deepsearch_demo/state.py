from typing import TypedDict
from .schema import ReportStructure


class Search(TypedDict):
    query: str
    url: str
    title: str
    content: str
    score: float | None
    timestamp: str


class Research(TypedDict):
    search_history: list[Search]
    latest_summary: str
    reflection_iteration: int
    is_completed: bool


class Paragraph(TypedDict):
    title: str
    content: str
    research: Research
    order: int


class State(TypedDict):
    query: str
    report_title: str
    paragraphs: list[Paragraph]
    final_report: str
    is_completed: bool
    created_at: str
    updated_at: str
