from fastapi import APIRouter, Request

from core.config import RedisConfig
from utils import get_completed_requests
from .schema import ResponseBody
from core.connection import redis


status_router = APIRouter()


@status_router.get("/status", response_model=ResponseBody, status_code=200)
async def question(request: Request):
    """
    get scrap status
    """
    waiting_requests = redis.lrange(name=RedisConfig.REDIS_SEARCH_QUERY_QUEUE_NAME, start=0, end=-1)
    in_processing = redis.get(RedisConfig.REDIS_IN_PROCESSING_SEARCH_QUERY)
    completed_requests = get_completed_requests()

    return {
        "completed": completed_requests,
        "in_process": in_processing,
        "waiting": waiting_requests,
    }
