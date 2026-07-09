from bson import ObjectId
from bson.errors import InvalidId

from app.services.database import get_webpages_collection
from app.services.indexer import client, ELASTICSEARCH_INDEX


def get_all_sources() -> list[dict]:
    webpages_collection = get_webpages_collection()

    documents = webpages_collection.find(
        {},
        {
            "_id": 1,
            "name": 1,
            "url": 1,
            "category": 1,
            "title": 1,
            "status_code": 1,
            "processing_status": 1,
            "indexing_status": 1,
            "crawled_at": 1,
            "indexed_at": 1,
            "elasticsearch_id": 1,
        },
    ).sort("crawled_at", -1)

    sources = []

    for document in documents:
        sources.append(
            {
                "document_id": str(document["_id"]),
                "name": document.get("name"),
                "url": document.get("url"),
                "category": document.get("category"),
                "title": document.get("title"),
                "status_code": document.get("status_code"),
                "processing_status": document.get("processing_status"),
                "indexing_status": document.get("indexing_status"),
                "crawled_at": document.get("crawled_at"),
                "indexed_at": document.get("indexed_at"),
                "elasticsearch_id": document.get("elasticsearch_id"),
            }
        )

    return sources


def delete_source(document_id: str) -> dict:
    webpages_collection = get_webpages_collection()

    try:
        object_id = ObjectId(document_id)
    except InvalidId:
        return {
            "status": "invalid_id",
            "message": "The provided MongoDB document ID is invalid.",
        }

    document = webpages_collection.find_one({"_id": object_id})

    if document is None:
        return {
            "status": "not_found",
            "message": "Source was not found.",
        }

    elasticsearch_id = document.get("elasticsearch_id")

    if elasticsearch_id:
        client.delete(
            index=ELASTICSEARCH_INDEX,
            id=elasticsearch_id,
            ignore=[404],
        )

    webpages_collection.delete_one({"_id": object_id})

    return {
        "status": "deleted",
        "message": "Source deleted successfully.",
        "document_id": document_id,
        "name": document.get("name"),
        "url": document.get("url"),
        "category": document.get("category"),
    }