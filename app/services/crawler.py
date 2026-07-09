import httpx

async def fetch_url(url: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)

        return {
            "url": url,
            "status_code": response.status_code,
            "content": response.text,
            "success": True,
        }

    except httpx.RequestError as error:
        return {
            "url": url,
            "status_code": None,
            "content": None,
            "success": False,
            "error": str(error),
        }