import logfire
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine


def configure_telemetry(app: FastAPI, engine: AsyncEngine) -> None:
    logfire.configure(
        service_name="chat-api",
        send_to_logfire="if-token-present",
    )
    logfire.instrument_fastapi(app)
    logfire.instrument_pydantic_ai()
    logfire.instrument_sqlalchemy(engine=engine.sync_engine)
