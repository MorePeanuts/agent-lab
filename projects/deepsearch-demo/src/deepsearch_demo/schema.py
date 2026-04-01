from pydantic import BaseModel, Field


class Item(BaseModel):
    title: str = Field(description='The title of this paragraph.')
    content: str = Field(description='The expected main content of this paragraph should include.')


class ReportStructure(BaseModel):
    items: list[Item] = Field(
        description='Plan the report structure, with each item containing the title of one section and the expected content.'
    )
