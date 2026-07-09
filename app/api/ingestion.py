from fastapi import APIRouter

from app.models.ingestion import IngestionRequest, IngestionResponse
from app.services.database import get_webpages_collection
from app.services.deduplication import document_exists, normalize_url
from app.workers.tasks import process_ingestion_job

router = APIRouter(
    prefix="/api/v1",
    tags=["Ingestion"],
)


@router.post(
    "/ingest",
    response_model=IngestionResponse,
    status_code=202,
)
async def ingest_urls(request: IngestionRequest) -> IngestionResponse:
    webpages_collection = get_webpages_collection()

    urls_queued = []
    urls_skipped = []

    for url in request.urls:
        normalized_url = normalize_url(str(url))

        if document_exists(webpages_collection, normalized_url):
            urls_skipped.append(normalized_url)
        else:
            process_ingestion_job.delay(normalized_url)
            urls_queued.append(normalized_url)

    return IngestionResponse(
        message="Ingestion request processed.",
        queued_urls=len(urls_queued),
        skipped_urls=len(urls_skipped),
        urls_queued=urls_queued,
        urls_skipped=urls_skipped,
    )