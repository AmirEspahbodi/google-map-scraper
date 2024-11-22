import uvicorn
from core.config.app import AppConfig


if __name__ == "__main__":
    uvicorn.run(
        app="core.server:app",
        host=AppConfig.HOST,
        port=AppConfig.PORT,
        reload=True if AppConfig.ENVIRONMENT != "production" else False,
        workers=AppConfig.WORKER,
    )
