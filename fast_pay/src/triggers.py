import httpx
from fastapi import Response


async def trigger_webhook(url, data, wh_secret, user_type):
    client = httpx.AsyncClient()
    try:
        res = await client.post(
            url=url,
            json=data if isinstance(data, dict) else data.model_dump(),
            headers={
                "Authorization": wh_secret,  # TODO add WEBHOOK_SECRET field to Company model
                "User-Type": user_type,
            },
        )
    finally:
        await client.aclose()

    try:
        res.raise_for_status()
    except httpx.HTTPStatusError as exc:
        return Response(
            content=exc.response.content, status_code=exc.response.status_code
        )

    return res
