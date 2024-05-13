import redis.asyncio as redis

from src.settings import fast_gate_settings

redis_conn_pool = redis.ConnectionPool.from_url(fast_gate_settings.redis_url)


async def get_redis():
    return redis.Redis(connection_pool=redis_conn_pool)


async def cache_set(key, data, ex=fast_gate_settings.redis_expiration):
    rds = await get_redis()
    await rds.set(name=key, value=data, ex=ex)
