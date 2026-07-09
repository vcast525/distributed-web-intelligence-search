from fastapi import APIRouter, Query

from app.services.search import search_documents

router = APIRouter(
    prefix="/api/v1",
    tags=["Search"],
)


@router.get("/search")
async def search(q: str = Query(..., min_length=1)) -> dict:
    results = search_documents(q)

    return {
        "query": q,
        "total_results": len(results),
        "results": results,
    }