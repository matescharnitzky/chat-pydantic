from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ConversationCreate(BaseModel):
    title: str | None = Field(default=None, max_length=200)


class ConversationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str | None
    created_at: datetime
    updated_at: datetime


class ChatRequest(BaseModel):
    content: str = Field(min_length=1, max_length=20_000)


class ChatResponse(BaseModel):
    conversation_id: UUID
    run_id: UUID
    content: str


class AgentRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    conversation_id: UUID
    prompt: str
    output: str
    model_name: str
    created_at: datetime
