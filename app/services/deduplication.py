from urllib.parse import urlparse, urlunparse


def normalize_url(url: str) -> str:
    parsed_url = urlparse(url)

    normalized = parsed_url._replace(
        scheme=parsed_url.scheme.lower(),
        netloc=parsed_url.netloc.lower(),
        path=parsed_url.path.rstrip("/") or "/",
        params="",
        query="",
        fragment="",
    )

    return urlunparse(normalized)


def document_exists(collection, url: str) -> bool:
    return collection.find_one({"url": url}) is not None