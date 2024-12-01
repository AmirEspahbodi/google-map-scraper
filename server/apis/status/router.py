from fastapi import APIRouter, Request

from core.config import RedisConfig, AppConfig
from utils import (
    get_imported_requests, get_not_imported_requests
)
from .schema import ResponseBody
from core.connection import redis


status_router = APIRouter()


@status_router.get("/status", response_model=ResponseBody, status_code=200)
async def question(request: Request):
    """
    get scrap status
    """
    imported_requests = get_imported_requests()
    not_imported_requests = get_not_imported_requests()

    waiting_requests: list[str] = redis.lrange(
        name=RedisConfig.REDIS_REQUESTED_SEARCH_QUERY_QUEUE_NAME,
        start=0,
        end=-1,
    )
    google_map_in_processing: str = redis.get(
        RedisConfig.REDIS_IN_PROCESSING_SEARCH_QUERY
    )

    return {
        "imported_requests": imported_requests,
        "not_imported_requests": not_imported_requests,
        "in_process": google_map_in_processing,
        "waiting_to_scrape": waiting_requests,
    }
