from typing import Any
from uuid import UUID

from pydantic_ai import ModelMessage, ModelMessagesTypeAdapter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from chat_api.infra.database.models import AgentRun, Conversation


class ConversationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, title: str | None) -> Conversation:
        conversation = Conversation(title=title)
        self.session.add(conversation)
        await self.session.flush()
        return conversation

    async def get(self, conversation_id: UUID) -> Conversation | None:
        return await self.session.get(Conversation, conversation_id)

    async def list_runs(self, conversation_id: UUID) -> list[AgentRun]:
        result = await self.session.scalars(
            select(AgentRun)
            .where(AgentRun.conversation_id == conversation_id)
            .order_by(AgentRun.created_at, AgentRun.id)
        )
        return list(result)

    async def get_history(self, conversation_id: UUID) -> list[ModelMessage]:
        history: list[ModelMessage] = []
        for run in await self.list_runs(conversation_id):
            history.extend(ModelMessagesTypeAdapter.validate_python(run.messages))
        return history

    async def add_run(
        self,
        *,
        run_id: UUID,
        conversation_id: UUID,
        prompt: str,
        output: str,
        messages: list[dict[str, Any]],
        model_name: str,
    ) -> AgentRun:
        run = AgentRun(
            id=run_id,
            conversation_id=conversation_id,
            prompt=prompt,
            output=output,
            messages=messages,
            model_name=model_name,
        )
        self.session.add(run)
        await self.session.flush()
        return run
