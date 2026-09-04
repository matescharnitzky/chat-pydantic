from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from chat_api.agent.factory import create_agent
from chat_api.api.conversations import router as conversations_router
from chat_api.api.health import router as health_router
from chat_api.infra.telemetry import configure_telemetry
from chat_api.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()

    engine = create_async_engine(settings.database_url, pool_pre_ping=True)
    try:
        app.state.settings = settings
        app.state.session_factory = async_sessionmaker(engine, expire_on_commit=False)
        app.state.agent = create_agent(settings)
        configure_telemetry(app, engine)
        yield
    finally:
        await engine.dispose()


app = FastAPI(title="Chat API", version="0.1.0", lifespan=lifespan)
app.include_router(health_router)
app.include_router(conversations_router, prefix="/v1")
