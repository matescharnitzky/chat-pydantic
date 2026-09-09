from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from chat_api.repositories.conversation import ConversationRepository
from chat_api.services.chat import ChatService


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    async with request.app.state.session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_chat_service(request: Request, session: SessionDep) -> ChatService:
    settings = request.app.state.settings
    return ChatService(
        repository=ConversationRepository(session),
        agent=request.app.state.agent,
        model_name=settings.model,
        model_configured=settings.openai_api_key is not None,
    )


ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
