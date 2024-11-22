from fastapi import APIRouter
from .status.router import status_router
from .scrap_req.router import scrap_req_router

root_api_router = APIRouter()
root_api_router.include_router(status_router)
root_api_router.include_router(scrap_req_router)

__all__ = ["root_api_router"]
