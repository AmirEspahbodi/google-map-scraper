from fastapi import APIRouter, HTTPException, status
from .schema import RequestBody, ResponseBody
from core.connection import redis
from core.config import RedisConfig
from utils import get_completed_requests

scrap_req_router = APIRouter()


@scrap_req_router.post("/request", response_model=ResponseBody, status_code=200)
async def request(body: RequestBody):
    """
    request search query to scrap
    """
    waiting_requests = redis.lrange(name=RedisConfig.REDIS_SEARCH_QUERY_QUEUE_NAME, start=0, end=-1)
    in_processing = redis.get(RedisConfig.REDIS_IN_PROCESSING_SEARCH_QUERY)
    completed_requests = get_completed_requests()
    
    search_query = f"{body.place_title.strip()} {body.verb.strip()} {body.city.strip()}"

    if waiting_requests is not None and search_query in waiting_requests:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="request is in queue and waiting for process",
        )
    if completed_requests is not None and search_query in completed_requests:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="request already completed"
        )

    redis.rpush(RedisConfig.REDIS_SEARCH_QUERY_QUEUE_NAME, search_query)
    return {
        "completed": completed_requests,
        "in_process": in_processing,
        "waiting": waiting_requests+[search_query],
    }
