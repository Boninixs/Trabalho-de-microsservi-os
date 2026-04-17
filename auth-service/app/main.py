from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import RequestLoggingMiddleware, configure_logging, get_logger

settings = get_settings()
configure_logging(service_name=settings.service_name, log_level=settings.log_level)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("service_starting")
    yield
    logger.info("service_stopping")


app = FastAPI(
    title=settings.service_name,
    description="Authentication and authorization service.",
    version=settings.service_version,
    lifespan=lifespan,
)
app.add_middleware(RequestLoggingMiddleware)
app.include_router(api_router)
