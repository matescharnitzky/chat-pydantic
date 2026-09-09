FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.11.2 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN apt-get update \
    && apt-get install --yes --no-install-recommends postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock README.md ./
COPY services/chat-api/pyproject.toml services/chat-api/pyproject.toml
COPY services/chat-api/src services/chat-api/src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --package chat-api

COPY infra/init.sh /usr/local/bin/init-infra
COPY infra/init.sql /usr/local/share/init-infra.sql
RUN chmod +x /usr/local/bin/init-infra \
    && useradd --create-home --uid 10001 appuser

USER appuser

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["init-infra"]
