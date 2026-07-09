from pydantic import BaseModel, HttpUrl


class SourceInput(BaseModel):
    name: str
    url: HttpUrl
    category: str


class IngestionRequest(BaseModel):
    sources: list[SourceInput]


class IngestionResponse(BaseModel):
    message: str
    queued_sources: int
    skipped_sources: int
    sources_queued: list[dict]
    sources_skipped: list[dict]