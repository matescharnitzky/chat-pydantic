FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.11.2 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY services/chat-api/pyproject.toml services/chat-api/pyproject.toml
COPY services/chat-api/src services/chat-api/src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --package chat-api

RUN useradd --create-home --uid 10001 appuser
USER appuser

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["uvicorn", "chat_api.app:app", "--host", "0.0.0.0", "--port", "8000"]
