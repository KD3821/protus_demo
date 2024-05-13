import httpx
from fastapi import Response

from src.settings import fast_gate_settings


class ProxyClient:
    API_KEY = fast_gate_settings.api_key
    AUTH_HOST = fast_gate_settings.auth_host
    AUTH_PORT = fast_gate_settings.auth_port
    PAYMENTS_HOST = fast_gate_settings.payments_host
    PAYMENTS_PORT = fast_gate_settings.payments_port

    def __init__(self):
        self.client = httpx.AsyncClient()

    async def proxy_post_request(self, host, port, path, data, user_type):
        try:
            res = await self.client.post(
                url=f"http://{host}:{port}/{user_type}/{path}/",
                headers={"Authorization": self.API_KEY},
                json=data if isinstance(data, dict) else data.model_dump(),
            )
        finally:
            await self.client.aclose()

        try:
            res.raise_for_status()
        except httpx.HTTPStatusError as exc:
            return Response(
                content=exc.response.content, status_code=exc.response.status_code
            )

        return res.json()

    async def proxy_get_request(self, host, port, path, user_type, user):
        try:
            res = await self.client.get(
                url=f"http://{host}:{port}/{user_type}/{path}/",
                headers={"User": user, "Authorization": self.API_KEY},
            )
        finally:
            await self.client.aclose()

        try:
            res.raise_for_status()
        except httpx.HTTPStatusError as exc:
            return Response(
                content=exc.response.content, status_code=exc.response.status_code
            )

        return res.json()
