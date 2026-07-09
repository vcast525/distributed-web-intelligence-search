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
async def ingest_sources(request: IngestionRequest) -> IngestionResponse:
    webpages_collection = get_webpages_collection()

    sources_queued = []
    sources_skipped = []

    for source in request.sources:
        normalized_url = normalize_url(str(source.url))

        source_payload = {
            "name": source.name,
            "url": normalized_url,
            "category": source.category,
        }

        if document_exists(webpages_collection, normalized_url):
            sources_skipped.append(source_payload)
        else:
            process_ingestion_job.delay(source_payload)
            sources_queued.append(source_payload)

    return IngestionResponse(
        message="Ingestion request processed.",
        queued_sources=len(sources_queued),
        skipped_sources=len(sources_skipped),
        sources_queued=sources_queued,
        sources_skipped=sources_skipped,
    )