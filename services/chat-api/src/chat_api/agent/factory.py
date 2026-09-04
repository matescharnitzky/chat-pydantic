from pydantic_ai import Agent
from pydantic_ai.models import Model
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai_harness import InputGuardrail
from pydantic_ai_harness.guardrails.detectors import redact_secrets

from chat_api.agent.dependencies import AgentDependencies
from chat_api.settings import Settings


def create_agent(settings: Settings, model: Model | None = None) -> Agent[AgentDependencies, str]:
    configured_model: Model | str
    if model is not None:
        configured_model = model
    elif settings.openai_api_key is not None:
        configured_model = OpenAIResponsesModel(
            settings.model.removeprefix("openai:"),
            provider=OpenAIProvider(api_key=settings.openai_api_key.get_secret_value()),
        )
    else:
        configured_model = settings.model

    return Agent(
        configured_model,
        deps_type=AgentDependencies,
        output_type=str,
        instructions="Be concise, helpful, and honest about uncertainty.",
        capabilities=[InputGuardrail(guard=redact_secrets)],
        defer_model_check=settings.openai_api_key is None and model is None,
    )
