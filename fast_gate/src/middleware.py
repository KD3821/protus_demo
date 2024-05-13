from fastapi import Request

from src.logger import logger


async def logging_middleware(request: Request, call_next):
    logging_data = {
        "url": request.url.path,
        "method": request.method,
        "user_type": request.headers.get("User-Type"),
    }
    logger.info(logging_data, extra=logging_data)
    response = await call_next(request)
    return response
