import asyncio
import logging
from datetime import datetime, UTC

from pymongo.errors import DuplicateKeyError

from app.services.crawler import fetch_url
from app.services.database import get_webpages_collection
from app.services.deduplication import normalize_url, document_exists
from app.services.indexer import index_document
from app.services.processor import process_html
from app.workers.celery_app import celery_app


logger = logging.getLogger("web_intelligence.pipeline")


@celery_app.task
def process_ingestion_job(source: dict) -> dict:
    source_name = source["name"]
    normalized_url = normalize_url(source["url"])
    category = source["category"]

    webpages_collection = get_webpages_collection()

    logger.info(
        "[PIPELINE] 1/5 SOURCE RECEIVED | name=%s | category=%s | url=%s",
        source_name,
        category,
        normalized_url,
    )

    if document_exists(webpages_collection, normalized_url):
        logger.info(
            "[PIPELINE] DUPLICATE SKIPPED | url=%s",
            normalized_url,
        )

        return {
            "status": "skipped",
            "message": "URL already exists and was not processed again.",
            "name": source_name,
            "url": normalized_url,
            "category": category,
        }

    crawl_result = asyncio.run(fetch_url(normalized_url))

    if crawl_result["success"]:
        logger.info(
            "[PIPELINE] 2/5 WEBSITE CRAWLED | url=%s | http_status=%s",
            normalized_url,
            crawl_result["status_code"],
        )

        processed_content = process_html(crawl_result["content"])

        document = {
            "name": source_name,
            "url": normalized_url,
            "category": category,
            "status_code": crawl_result["status_code"],
            "title": processed_content["title"],
            "clean_text": processed_content["clean_text"],
            "headings": processed_content["headings"],
            "paragraphs": processed_content["paragraphs"],
            "processing_status": "processed",
            "indexing_status": "pending",
            "crawled_at": datetime.now(UTC),
            "indexed_at": None,
            "elasticsearch_id": None,
            "raw_html": crawl_result["content"],
            "normalized_html": processed_content["normalized_html"],
        }

        try:
            insert_result = webpages_collection.insert_one(document)
        except DuplicateKeyError:
            logger.info(
                "[PIPELINE] DUPLICATE BLOCKED BY MONGODB | url=%s",
                normalized_url,
            )

            return {
                "status": "skipped",
                "message": "URL already exists and was not processed again.",
                "name": source_name,
                "url": normalized_url,
                "category": category,
            }

        logger.info(
            "[PIPELINE] 3/5 MONGODB STORED | document_id=%s",
            str(insert_result.inserted_id),
        )

        index_result = index_document(document)

        webpages_collection.update_one(
            {"_id": insert_result.inserted_id},
            {
                "$set": {
                    "indexing_status": "indexed",
                    "indexed_at": datetime.now(UTC),
                    "elasticsearch_id": index_result["elasticsearch_id"],
                }
            },
        )

        logger.info(
            "[PIPELINE] 4/5 ELASTICSEARCH INDEXED | elasticsearch_id=%s",
            index_result["elasticsearch_id"],
        )

        logger.info(
            "[PIPELINE] 5/5 PIPELINE COMPLETED | name=%s | category=%s | url=%s",
            source_name,
            category,
            normalized_url,
        )

        logger.info(
            "[PIPELINE SUMMARY] SUCCESS | name=%s | category=%s | url=%s | title=%s | mongo_document_id=%s | elasticsearch_id=%s",
            source_name,
            category,
            normalized_url,
            processed_content["title"],
            str(insert_result.inserted_id),
            index_result["elasticsearch_id"],
        )

        return {
            "status": "completed",
            "message": "Source crawled, processed, stored, and indexed successfully.",
            "name": source_name,
            "url": normalized_url,
            "category": category,
            "status_code": crawl_result["status_code"],
            "title": processed_content["title"],
            "mongo_document_id": str(insert_result.inserted_id),
            "elasticsearch_id": index_result["elasticsearch_id"],
        }

    logger.error(
        "[PIPELINE] FAILED | name=%s | category=%s | url=%s | http_status=%s",
        source_name,
        category,
        normalized_url,
        crawl_result["status_code"],
    )

    return {
        "status": "failed",
        "message": "Source crawl failed.",
        "name": source_name,
        "url": normalized_url,
        "category": category,
        "status_code": crawl_result["status_code"],
    }