import redis

from core.config import RedisConfig

redis = redis.from_url(
    url=f"redis://{RedisConfig.REDIS_HOST}:{RedisConfig.REDIS_PORT}",
    decode_responses=True,
)
