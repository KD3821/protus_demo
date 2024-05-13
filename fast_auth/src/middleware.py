import json

from fastapi import Request, Response, status

from src.settings import fast_auth_settings


async def check_api_key_middleware(request: Request, call_next):
    api_key = request.headers.get("Authorization")
    if api_key != fast_auth_settings.api_key:
        return Response(
            content=json.dumps({"detail": "Access Denied by API"}),
            status_code=status.HTTP_403_FORBIDDEN,
        )
    response = await call_next(request)
    return response
