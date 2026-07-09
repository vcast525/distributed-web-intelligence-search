from pydantic import BaseModel, HttpUrl


class IngestionRequest(BaseModel):
    urls: list[HttpUrl]


class IngestionResponse(BaseModel):
    message: str
    queued_urls: int
    skipped_urls: int
    urls_queued: list[str]
    urls_skipped: list[str]