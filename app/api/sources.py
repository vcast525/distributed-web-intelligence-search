from fastapi import APIRouter, HTTPException

from app.services.source_manager import get_all_sources, delete_source


router = APIRouter(
    prefix="/api/v1/sources",
    tags=["Sources"],
)


@router.get("")
def list_sources():
    sources = get_all_sources()

    return {
        "total_sources": len(sources),
        "sources": sources,
    }


@router.delete("/{document_id}")
def remove_source(document_id: str):
    result = delete_source(document_id)

    if result["status"] == "invalid_id":
        raise HTTPException(
            status_code=400,
            detail=result["message"],
        )

    if result["status"] == "not_found":
        raise HTTPException(
            status_code=404,
            detail=result["message"],
        )

    return result