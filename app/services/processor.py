import re

from bs4 import BeautifulSoup


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_html(value: str) -> str:
    normalized = normalize_text(value)
    normalized = re.sub(r">\s+<", "><", normalized)
    return normalized


def process_html(content: str) -> dict:
    soup = BeautifulSoup(content, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    headings = [
        normalize_text(heading.get_text())
        for heading in soup.find_all(["h1", "h2", "h3"])
    ]

    paragraphs = [
        normalize_text(paragraph.get_text())
        for paragraph in soup.find_all("p")
    ]

    clean_text = normalize_text(" ".join(headings + paragraphs))

    return {
        "title": title,
        "headings": headings,
        "paragraphs": paragraphs,
        "clean_text": clean_text,
        "normalized_html": normalize_html(content),
    }