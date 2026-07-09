from datetime import datetime, UTC

from elasticsearch import Elasticsearch


ELASTICSEARCH_URL = "http://elasticsearch:9200"
ELASTICSEARCH_INDEX = "web_intelligence"

client = Elasticsearch(ELASTICSEARCH_URL)


def index_document(document: dict) -> dict:
    search_document = {
        "url": document["url"],
        "title": document["title"],
        "headings": document["headings"],
        "paragraphs": document["paragraphs"],
        "clean_text": document["clean_text"],
        "status_code": document["status_code"],
        "crawled_at": document["crawled_at"],
        "indexed_at": datetime.now(UTC),
    }

    response = client.index(
        index=ELASTICSEARCH_INDEX,
        document=search_document,
    )

    return {
        "indexed": True,
        "index": ELASTICSEARCH_INDEX,
        "elasticsearch_id": response["_id"],
    }