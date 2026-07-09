from app.services.indexer import ELASTICSEARCH_INDEX, client


def search_documents(query: str) -> list[dict]:
    response = client.search(
        index=ELASTICSEARCH_INDEX,
        query={
            "multi_match": {
                "query": query,
                "fields": ["title^3", "headings^2", "paragraphs", "clean_text"],
            }
        },
        highlight={
            "fields": {
                "title": {},
                "clean_text": {},
            }
        },
    )

    results = []

    for hit in response["hits"]["hits"]:
        source = hit["_source"]

        results.append(
            {
                "score": hit["_score"],
                "url": source.get("url"),
                "title": source.get("title"),
                "clean_text": source.get("clean_text"),
                "highlights": hit.get("highlight", {}),
            }
        )

    return results