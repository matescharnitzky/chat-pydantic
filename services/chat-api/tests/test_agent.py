from uuid import uuid4

from chat_api.agent.dependencies import AgentDependencies
from chat_api.agent.factory import create_agent
from chat_api.settings import Settings
from pydantic_ai.models.test import TestModel


def test_blank_openai_key_is_not_configured() -> None:
    settings = Settings(_env_file=None, OPENAI_API_KEY="")

    assert settings.openai_api_key is None


async def test_agent_can_run_without_paid_model_calls() -> None:
    agent = create_agent(
        Settings(_env_file=None),
        model=TestModel(custom_output_text="Hello from the test model"),
    )

    result = await agent.run(
        "Hello",
        deps=AgentDependencies(conversation_id=uuid4()),
    )

    assert result.output == "Hello from the test model"
