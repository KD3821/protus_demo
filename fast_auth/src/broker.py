import asyncio
import json
import uuid
from typing import Any, Dict

import aio_pika

from src.settings import fast_auth_settings

__all__ = ["broker_handler"]


class Broker:
    _connection: aio_pika.abc.AbstractRobustConnection = None
    _channel: aio_pika.abc.AbstractChannel = None
    _response_queue: aio_pika.abc.AbstractQueue = None
    _futures: Dict[str, asyncio.Future] = {}

    def __init__(self, amqp_dsn: str, service_name: str):
        self._amqp_dsn = amqp_dsn
        self._service_name = service_name

    async def connect(self) -> None:
        self._connection = await aio_pika.connect_robust(self._amqp_dsn)
        self._channel = await self._connection.channel()
        self._response_queue = await self._channel.declare_queue(
            f"{self._service_name}_responses", durable=True
        )
        await self._response_queue.consume(self._consume)

    async def _consume(self, message: aio_pika.abc.AbstractIncomingMessage) -> None:
        correlation_id = message.correlation_id
        future = self._futures.get(correlation_id, None)
        if future:
            future.set_result(json.loads(message.body.decode("utf-8")))
        await message.ack()

    async def _request(self, *, to: str, payload: dict):
        request_id = str(uuid.uuid4())
        self._futures[request_id] = asyncio.Future()
        message = aio_pika.message.Message(
            body=json.dumps(payload).encode("utf-8"),
            correlation_id=request_id,
            reply_to=self._response_queue.name,
        )
        await self._channel.default_exchange.publish(message, routing_key=to)
        return await self._futures[request_id]

    async def process_request(
        self, service_name: str, data: Dict[str, Any]
    ) -> asyncio.Future:
        return await self._request(to=f"{service_name}_requests", payload=data)


broker_handler = Broker(
    str(fast_auth_settings.amqp_dsn), fast_auth_settings.service_name
)


"""
docker run -d --name fast-rabbit -p 5672:5672 -p 5673:5673 -p 15672:15672 rabbitmq:3-management
"""
