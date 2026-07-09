from pymongo import MongoClient, ASCENDING

MONGODB_URL = "mongodb://mongodb:27017"
MONGODB_DATABASE = "web_intelligence"
MONGODB_COLLECTION = "webpages"

_client = None


def get_mongo_client() -> MongoClient:
    global _client

    if _client is None:
        _client = MongoClient(MONGODB_URL)

    return _client


def get_webpages_collection():
    client = get_mongo_client()
    database = client[MONGODB_DATABASE]
    collection = database[MONGODB_COLLECTION]

    collection.create_index(
        [("url", ASCENDING)],
        unique=True,
    )

    return collection