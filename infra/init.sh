#!/bin/sh
set -eu

: "${PGHOST:?PGHOST is required}"
: "${PGUSER:?PGUSER is required}"
: "${PGPASSWORD:?PGPASSWORD is required}"
: "${CHAT_DB_NAME:?CHAT_DB_NAME is required}"
: "${CHAT_DB_USER:?CHAT_DB_USER is required}"
: "${CHAT_DB_PASSWORD:?CHAT_DB_PASSWORD is required}"
: "${CHAT_DATABASE_URL:?CHAT_DATABASE_URL is required}"

psql \
  --dbname postgres \
  --set ON_ERROR_STOP=1 \
  --set chat_db_name="$CHAT_DB_NAME" \
  --set chat_db_user="$CHAT_DB_USER" \
  --set chat_db_password="$CHAT_DB_PASSWORD" \
  --file /usr/local/share/init-infra.sql

alembic \
  -c services/chat-api/src/chat_api/infra/database/alembic.ini \
  upgrade head
