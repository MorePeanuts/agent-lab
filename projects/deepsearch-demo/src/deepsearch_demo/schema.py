from pydantic import BaseModel, Field


class Item(BaseModel):
    title: str
    content: str


class ReportStructure(BaseModel):
    items: list[Item]
