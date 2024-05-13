import json

import aio_pika

from src import callbacks
from src.settings import fast_pay_settings

__all__ = ["broker_handler"]


class Broker:
    _connection: aio_pika.abc.AbstractRobustConnection = None
    _channel: aio_pika.abc.AbstractChannel = None
    _request_queue: aio_pika.abc.AbstractQueue = None

    def __init__(self, amqp_dsn: str, service_name: str):
        self._amqp_dsn = amqp_dsn
        self._service_name = service_name

    async def connect(self) -> None:
        self._connection = await aio_pika.connect_robust(self._amqp_dsn)
        self._channel = await self._connection.channel()
        self._request_queue = await self._channel.declare_queue(
            f"{self._service_name}_requests", durable=True
        )
        await self._request_queue.consume(self._consume)

    async def _consume(self, message: aio_pika.abc.AbstractIncomingMessage) -> None:
        msg_body = json.loads(message.body.decode("utf-8"))

        handler = msg_body.pop("callback")
        handler_data = handler.split(".")
        callback_handler = getattr(
            callbacks, handler_data[0]
        )()  # init Model_Callback_Handler()

        result = await getattr(callback_handler, handler_data[1])(
            msg_body
        )  # get method and call it

        await self._response(
            to=message.reply_to,
            correlation_id=message.correlation_id,
            payload={"service": self._service_name, "result": result},
        )
        await message.ack()

    async def _response(self, *, to: str, correlation_id: str, payload: dict):
        message = aio_pika.message.Message(
            body=json.dumps(payload).encode("utf-8"), correlation_id=correlation_id
        )

        await self._channel.default_exchange.publish(message, routing_key=to)


broker_handler = Broker(str(fast_pay_settings.amqp_dsn), fast_pay_settings.service_name)
