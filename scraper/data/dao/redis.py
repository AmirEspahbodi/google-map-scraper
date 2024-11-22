import redis
from config.redis import RedisConfig


class RedisDao:
    def __init__(self):
        self.redis_client = redis.StrictRedis(
            host=RedisConfig.REDIS_HOST,
            port=RedisConfig.REDIS_PORT,
            decode_responses=True,
            encoding="UTF-8",
        )

    def dequeue(self, queue_name=RedisConfig.REDIS_SEARCH_QUERY_QUEUE_NAME):
        if self.redis_client.exists(queue_name):
            search_query = self.redis_client.lpop(queue_name)
            self.set_inprocessing(search_query)
            return search_query
        return False

    def set_inprocessing(self, search_query):
        self.redis_client.set(RedisConfig.REDIS_IN_PROCESSING_SEARCH_QUERY, search_query)
