from dataclasses import dataclass
from uuid import UUID, uuid4

from pydantic_core import to_jsonable_python

from chat_api.agent.dependencies import AgentDependencies
from chat_api.infra.database.models import AgentRun, Conversation
from chat_api.repositories.conversation import ConversationRepository


class ConversationNotFoundError(Exception):
    pass


class ModelNotConfiguredError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class ChatResult:
    conversation_id: UUID
    run_id: UUID
    content: str


class ChatService:
    def __init__(
        self,
        *,
        repository: ConversationRepository,
        agent: object,
        model_name: str,
        model_configured: bool,
    ) -> None:
        self.repository = repository
        self.agent = agent
        self.model_name = model_name
        self.model_configured = model_configured

    async def create_conversation(self, title: str | None) -> Conversation:
        conversation = await self.repository.create(title)
        await self.repository.session.commit()
        await self.repository.session.refresh(conversation)
        return conversation

    async def get_conversation(self, conversation_id: UUID) -> Conversation:
        conversation = await self.repository.get(conversation_id)
        if conversation is None:
            raise ConversationNotFoundError
        return conversation

    async def list_runs(self, conversation_id: UUID) -> list[AgentRun]:
        await self.get_conversation(conversation_id)
        return await self.repository.list_runs(conversation_id)

    async def respond(self, conversation_id: UUID, content: str) -> ChatResult:
        await self.get_conversation(conversation_id)
        if not self.model_configured:
            raise ModelNotConfiguredError

        history = await self.repository.get_history(conversation_id)
        run_id = uuid4()
        result = await self.agent.run(
            content,
            deps=AgentDependencies(conversation_id=conversation_id),
            message_history=history,
            conversation_id=str(conversation_id),
            run_id=str(run_id),
        )
        await self.repository.add_run(
            run_id=run_id,
            conversation_id=conversation_id,
            prompt=content,
            output=result.output,
            messages=to_jsonable_python(result.new_messages()),
            model_name=self.model_name,
        )
        await self.repository.session.commit()
        return ChatResult(
            conversation_id=conversation_id,
            run_id=run_id,
            content=result.output,
        )
