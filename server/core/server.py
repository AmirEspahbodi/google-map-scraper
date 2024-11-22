from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from apis import root_api_router
from core.config.app import AppConfig


def init_routers(app_: FastAPI) -> None:
    app_.include_router(root_api_router)


def init_cors(app_: FastAPI) -> None:
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app() -> FastAPI:
    # init app
    _app = FastAPI(
        title=AppConfig.APP_NAME,
        description=AppConfig.APP_DESCRIPTION,
        version=AppConfig.APP_VERSION,
        docs_url=None if AppConfig.ENVIRONMENT == "production" else "/docs",
        redoc_url=None,
    )
    init_cors(app_=_app)
    init_routers(app_=_app)

    return _app


app = create_app()
