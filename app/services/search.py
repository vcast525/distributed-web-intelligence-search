from app.services.indexer import ELASTICSEARCH_INDEX, client


def search_documents(query: str) -> list[dict]:
    response = client.search(
        index=ELASTICSEARCH_INDEX,
        query={
            "multi_match": {
                "query": query,
                "fields": [
                    "name^4",
                    "title^3",
                    "category^2",
                    "headings^2",
                    "paragraphs",
                    "clean_text",
                ],
            }
        },
        highlight={
            "fields": {
                "name": {},
                "title": {},
                "category": {},
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
                "name": source.get("name"),
                "url": source.get("url"),
                "category": source.get("category"),
                "title": source.get("title"),
                "clean_text": source.get("clean_text"),
                "highlights": hit.get("highlight", {}),
            }
        )

    return results