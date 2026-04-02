from dataclasses import dataclass, field, asdict
import json
from pathlib import Path
from .schema import ReportStructure
from .tools import SearchResult


@dataclass
class Research:
    search_history: list[SearchResult] = field(default_factory=list)
    latest_summary: str = ''
    reflection_iteration: int = 0
    is_completed: bool = False

    def to_dict(self) -> dict:
        return {
            'search_history': [sr.to_dict() for sr in self.search_history],
            'latest_summary': self.latest_summary,
            'reflection_iteration': self.reflection_iteration,
            'is_completed': self.is_completed,
        }


@dataclass
class Paragraph:
    title: str = ''
    content: str = ''
    research: Research = field(default_factory=Research)
    order: int = 0

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'content': self.content,
            'research': self.research.to_dict(),
            'order': self.order,
        }


@dataclass
class State:
    query: str = ''
    report_title: str = ''
    paragraphs: list[Paragraph] = field(default_factory=list)
    paragraph_index: int = 0
    final_report: str = ''
    is_completed: bool = False

    def to_dict(self) -> dict:
        return {
            'query': self.query,
            'report_title': self.report_title,
            'paragraphs': [p.to_dict() for p in self.paragraphs],
            'paragraph_index': self.paragraph_index,
            'final_report': self.final_report,
            'is_completed': self.is_completed,
        }

    def to_json(self, indent: int = 2, ensure_ascii: bool = False) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=ensure_ascii)

    def save(self, path: Path):
        with path.open('w', encoding='utf-8') as f:
            f.write(self.to_json())
