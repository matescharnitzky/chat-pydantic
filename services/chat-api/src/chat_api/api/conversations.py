from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from chat_api.api.schemas import (
    AgentRunRead,
    ChatRequest,
    ChatResponse,
    ConversationCreate,
    ConversationRead,
)
from chat_api.dependencies import ChatServiceDep
from chat_api.services.chat import ConversationNotFoundError, ModelNotConfiguredError

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("", response_model=ConversationRead, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    body: ConversationCreate,
    service: ChatServiceDep,
) -> ConversationRead:
    return ConversationRead.model_validate(await service.create_conversation(body.title))


@router.get("/{conversation_id}", response_model=ConversationRead)
async def get_conversation(
    conversation_id: UUID,
    service: ChatServiceDep,
) -> ConversationRead:
    try:
        return ConversationRead.model_validate(await service.get_conversation(conversation_id))
    except ConversationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="conversation not found"
        ) from exc


@router.get("/{conversation_id}/runs", response_model=list[AgentRunRead])
async def list_runs(
    conversation_id: UUID,
    service: ChatServiceDep,
) -> list[AgentRunRead]:
    try:
        return [
            AgentRunRead.model_validate(run) for run in await service.list_runs(conversation_id)
        ]
    except ConversationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="conversation not found"
        ) from exc


@router.post("/{conversation_id}/chat", response_model=ChatResponse)
async def chat(
    conversation_id: UUID,
    body: ChatRequest,
    service: ChatServiceDep,
) -> ChatResponse:
    try:
        result = await service.respond(conversation_id, body.content)
        return ChatResponse(
            conversation_id=result.conversation_id,
            run_id=result.run_id,
            content=result.content,
        )
    except ConversationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="conversation not found"
        ) from exc
    except ModelNotConfiguredError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OPENAI_API_KEY is not configured",
        ) from exc
