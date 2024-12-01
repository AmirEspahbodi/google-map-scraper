from fastapi import APIRouter, HTTPException, status
from .schema import RequestBody, ResponseBody
from core.connection import redis
from core.config import RedisConfig
from utils import (
    get_not_imported_requests,
    get_imported_requests
)
from core.config import AppConfig

scrap_req_router = APIRouter()


@scrap_req_router.post(
    "/request", response_model=ResponseBody, status_code=200
)
async def request(body: RequestBody):
    """
    request search query to scrap in google map
    """
    waiting_requests: list[str] = redis.lrange(
        name=RedisConfig.REDIS_REQUESTED_SEARCH_QUERY_QUEUE_NAME,
        start=0,
        end=-1,
    )
    in_processing: str = redis.get(
        RedisConfig.REDIS_IN_PROCESSING_SEARCH_QUERY
    )

    imported_requests = get_not_imported_requests()
    not_imported_requests = get_imported_requests()

    error_message = ""

    requested_search_query = (
        f"{body.listing_type.strip()}"
        + f"{AppConfig.LISTING_TYPE_ITEMS_SEPARATOR.strip()}"
        + f"{body.verb.strip()}"
        + f"{AppConfig.LISTING_TYPE_ITEMS_SEPARATOR.strip()}"
        + f"{body.city.strip()}"
    )
    clean_requested_search_query = (
        f"{body.listing_type.strip()}"
        + f" "
        + f"{body.verb.strip()}"
        + f" "
        + f"{body.city.strip()}"
    )

    if imported_requests:
        for imported_request in imported_requests:
            listing_category, listing_search_query, province, scraper = [
                i.strip()
                for i in imported_request.split(AppConfig.SEARCH_QUERY_ITEMS_SEPARATOR)
            ]
            if requested_search_query == listing_search_query:
                error_message = f"request {clean_requested_search_query} is imported to site under type of {listing_category}"

    if not_imported_requests:
        for not_imported_request in not_imported_requests:
            listing_category, listing_search_query, province, scraper = [
                i.strip()
                for i in not_imported_request.split(
                    AppConfig.SEARCH_QUERY_ITEMS_SEPARATOR
                )
            ]
            if requested_search_query == listing_search_query:
                error_message = f"request {clean_requested_search_query} is scraped (but not imported to site) under type of {listing_category}"

    if waiting_requests:
        for waiting_request in waiting_requests:
            listing_category, listing_search_query, province = [
                i.strip()
                for i in waiting_request.split(AppConfig.SEARCH_QUERY_ITEMS_SEPARATOR)
            ]
            if requested_search_query == listing_search_query:
                error_message = f"request {clean_requested_search_query} is in queue and is waitin to be scraped under type of {listing_category}"
    if in_processing:
        listing_category, listing_search_query, province = [
            i.strip()
            for i in in_processing.split(
                AppConfig.SEARCH_QUERY_ITEMS_SEPARATOR
            )
        ]
        if requested_search_query == listing_search_query:
            error_message = f"The {clean_requested_search_query} request is being scrapped. under type of {listing_category}"

    if error_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message,
        )

    search_query = (
        f"{body.listing_category.strip()}"
        + f"{AppConfig.SEARCH_QUERY_ITEMS_SEPARATOR.strip()}"
        + f"{requested_search_query}"
        + f"{AppConfig.SEARCH_QUERY_ITEMS_SEPARATOR.strip()}"
        + f"{body.province}"
    )
    redis.rpush(
        RedisConfig.REDIS_REQUESTED_SEARCH_QUERY_QUEUE_NAME, search_query
    )

    return {
        "imported_requests": [
            " ".join(i.split(AppConfig.LISTING_TYPE_ITEMS_SEPARATOR))
            for i in imported_requests
        ]
        if imported_requests
        else [],
        "not_imported_requests": [
            " ".join(i.split(AppConfig.LISTING_TYPE_ITEMS_SEPARATOR))
            for i in not_imported_requests
        ]
        if not_imported_requests
        else [],
        "in_process": in_processing,
        "waiting_to_scrape": [
            " ".join(i.split(AppConfig.LISTING_TYPE_ITEMS_SEPARATOR))
            for i in waiting_requests
        ]
        if waiting_requests
        else [],
    }
