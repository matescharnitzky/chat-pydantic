# chat-pydantic

A staged chatbot monorepo built with FastAPI, the Pydantic AI stack, PostgreSQL,
and Docker Compose.

## Current stage

Stage 1 provides `chat-api`, its PostgreSQL database, Alembic migrations, Pydantic
AI agent, Harness input guardrail, and optional Logfire telemetry. The API starts
without external credentials; calling the chat endpoint requires `OPENAI_API_KEY`.

Compose starts Stage 1 in dependency order: PostgreSQL, the one-shot `init-infra`
job that idempotently creates the chat database and role and applies service-owned
Alembic migrations, and finally the chat API.

## Local development

Requirements: Python 3.12, uv, Docker with Compose, and Bruno CLI for black-box API
tests. On macOS, install the latter with `brew install bruno-cli`.

```bash
cp .env.example .env
make install
make check
make up
```

The chat API is available at <http://localhost:8000>; OpenAPI documentation is at
<http://localhost:8000/docs>.

Run the Bruno collection against the running stack:

```bash
make test-api
```

Pytest covers fast service and agent behavior; the Bruno collection verifies the
live API and its PostgreSQL persistence through Docker Compose.

To make a real model call, set `OPENAI_API_KEY` in `.env`, restart `chat-api`, then:

```bash
curl -X POST http://localhost:8000/v1/conversations \
  -H 'content-type: application/json' \
  -d '{"title":"First conversation"}'

curl -X POST http://localhost:8000/v1/conversations/<conversation-id>/chat \
  -H 'content-type: application/json' \
  -d '{"content":"Hello"}'
```

Set `LOGFIRE_TOKEN` to export telemetry. Without a token, Logfire remains local and
does not prevent startup.

Stop the services and delete the local PostgreSQL data volume:

```bash
make down
```

## Planned stages

1. Chat API and PostgreSQL (implemented).
2. Ingestion API, PDF processing, MinIO, and agent-tool retrieval.
3. Bare-bones first-class evals workspace member.
4. Chat UI (framework and scope TBD).
