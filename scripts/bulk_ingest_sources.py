import json
from pathlib import Path

import requests


API_URL = "http://127.0.0.1:8000/api/v1/ingest"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_FILE = PROJECT_ROOT / "data" / "source_taxonomy.json"


def load_sources() -> list[dict]:
    with SOURCE_FILE.open("r", encoding="utf-8") as file:
        source_data = json.load(file)

    return source_data["sources"]


def submit_sources(sources: list[dict]) -> dict:
    response = requests.post(
        API_URL,
        json={"sources": sources},
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def main() -> None:
    sources = load_sources()

    print("=" * 60)
    print("APEX FINANCIAL INTELLIGENCE")
    print("BULK SOURCE INGESTION")
    print("=" * 60)

    print(f"Sources loaded: {len(sources)}")
    print("Submitting sources to ingestion API...")

    result = submit_sources(sources)

    print("-" * 60)
    print("INGESTION REQUEST ACCEPTED")
    print(f"Sources queued:  {result['queued_sources']}")
    print(f"Sources skipped: {result['skipped_sources']}")
    print("-" * 60)
    print("Sources are now being processed asynchronously.")
    print("Check the Celery worker logs for pipeline progress.")
    print("=" * 60)


if __name__ == "__main__":
    main()