from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class AgentDependencies:
    conversation_id: UUID
