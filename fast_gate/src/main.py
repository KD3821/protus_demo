import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from src.api import router
from src.broker import broker_handler
from src.middleware import logging_middleware
from src.settings import fast_gate_settings


async def delay(coro, seconds):  # custom coroutine wrapper
    await asyncio.sleep(seconds)
    await coro


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.create_task(
        delay(broker_handler.connect(), 30)  # waiting when broker is ready to accept
    )
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Gateway Service For PROTUS",
    description="One payment account for all online services",
    version="1.0.1",
)

app.include_router(router)

allow_origins = ["*"]  # 'http://localhost:8080', 'http://127.0.0.1:8080'

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=logging_middleware,  # disabled now: too much spam?
)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=fast_gate_settings.server_host,
        port=fast_gate_settings.server_port,
        reload_dirs=["src"],
    )


"""
from outside of 'src' directory run: python3 -m src.main
"""
