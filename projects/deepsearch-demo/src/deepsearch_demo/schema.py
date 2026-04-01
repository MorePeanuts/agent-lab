from pydantic import BaseModel, Field


class Item(BaseModel):
    title: str = Field(description='The title of this paragraph.')
    content: str = Field(description='The expected main content of this paragraph should include.')


class ReportStructure(BaseModel):
    items: list[Item] = Field(
        description='Plan the report structure, with each item containing the title of one section and the expected content.'
    )


class ReflectionSummary(BaseModel):
    stop_reflection: bool = Field(
        description='Whether to terminate iterative reflection. If you believe the information is sufficient and iterative thinking can be terminated, set this field to True.'
    )
    summary: str = Field(description='Latest state of the paragraph')
