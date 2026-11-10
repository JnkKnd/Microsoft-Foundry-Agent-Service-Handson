"""Shared Agent Framework wiring for the Contoso travel workshop."""

from __future__ import annotations

import asyncio
import os
import threading
import time
from collections.abc import Awaitable, Callable, Generator
from pathlib import Path
from typing import Any

import httpx
from agent_framework import (
    Agent,
    AgentModeProvider,
    ChatContext,
    ChatMiddleware,
    FileSystemAgentFileStore,
    InMemoryHistoryProvider,
    MCPStreamableHTTPTool,
    create_harness_agent,
    todos_remaining,
    todos_remaining_message,
)
from agent_framework.foundry import FoundryChatClient, FoundryToolbox
from azure.core.credentials import TokenCredential
from azure.identity import AzureCliCredential, DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

FOUNDRY_PROJECT_ENDPOINT_ENV = "FOUNDRY_PROJECT_ENDPOINT"
FOUNDRY_MODEL_ENV = "FOUNDRY_MODEL"
SEARCH_SERVICE_ENDPOINT_ENV = "AZURE_AI_SEARCH_SERVICE_ENDPOINT"
KNOWLEDGE_BASE_NAME_ENV = "AZURE_AI_SEARCH_KNOWLEDGE_BASE_NAME"
TOOLBOX_NAME_ENV = "TOOLBOX_NAME"
CREDENTIAL_MODE_ENV = "WORKSHOP_CREDENTIAL_MODE"

DEFAULT_KNOWLEDGE_BASE_NAME = "contoso-travel-knowledge-lab"
DEFAULT_TOOLBOX_NAME = "contoso-travel-toolbox"
# Luna is supported by the August API (Microsoft Learn, retrieved 2026-09-10).
FOUNDRY_IQ_API_VERSION = "2026-08-01-preview"
SEARCH_TOKEN_SCOPE = "https://search.azure.com/.default"
CHAT_REQUEST_INTERVAL_SECONDS = 20.0
HARNESS_MAX_OUTPUT_TOKENS = 4_096

HARNESS_AGENT_NAME = "travel_harness_agent"
HARNESS_AGENT_DESCRIPTION = (
    "Plans a travel request, retrieves Contoso policy, loads Toolbox Skills, "
    "and uses Tool Search to select the required travel tools."
)
HARNESS_AGENT_INSTRUCTIONS = """
You are Contoso's internal travel and expense Harness Agent.

Break complex requests into todos and complete each todo before preparing the final answer.
Do not confuse the roles of information sources and capabilities.
In plan mode, create only the plan and todos. Do not execute Foundry IQ, Skills, Toolbox tools,
or Web Search. Execute them only after the user approves the plan and switches to execute mode.

- Use Foundry IQ to retrieve internal policy and approval-process evidence, and cite it.
- If operational guidance is needed, load the Toolbox Skill and follow its instructions.
- For Toolbox tools, discover via Tool Search's tool_search; execute with call_tool.
- For tool_search query, use one English tool name matching the task, not descriptive prose.
  Use createTripEstimate for estimates, getPerDiem for per diem, createPreapproval for an explicitly
  requested approval simulation, code_interpreter for numerical calculations, and web_search for
  explicitly requested public-information searches. Check the returned official name and inputSchema
  before calling call_tool; do not guess undiscovered tools.
- Use Travel Ops API results for costs, per diem, and approval simulations; do not invent values.
- Use Code Interpreter for ratios and comparisons across multiple results.
- Use Web Search only when the user explicitly requests current public information;
  show retrieval time and sources.

Do not make bookings or grant actual approvals. Run a preapproval simulation only when explicitly
requested by the user, and distinguish it from actual approval. If required information is missing,
list the questions to clarify rather than guessing.
""".strip()

STANDARD_AGENT_INSTRUCTIONS = """
You are Contoso's internal travel and expense assistant.
Use Foundry IQ to research internal policy questions and support your answers with evidence.
Do not guess unverified values. If search finds no information, say it was not found.
This Agent does not yet have cost-calculation or approval-simulation tools.
""".strip()


class AzureTokenCredentialAuth(httpx.Auth):
    """Attach a fresh Azure bearer token to every HTTP request."""

    def __init__(self, credential: TokenCredential, scope: str) -> None:
        self._credential = credential
        self._scope = scope

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response]:
        request.headers["Authorization"] = f"Bearer {self._credential.get_token(self._scope).token}"
        yield request


class ChatRequestPacer(ChatMiddleware):
    """Space model calls so the workshop's default 40K TPM deployment can recover."""

    def __init__(
        self,
        interval_seconds: float = CHAT_REQUEST_INTERVAL_SECONDS,
        *,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ) -> None:
        if interval_seconds < 0:
            raise ValueError("interval_seconds must be non-negative")
        self._interval_seconds = interval_seconds
        self._clock = clock
        self._sleep = sleep
        self._reservation_lock = threading.Lock()
        self._next_start_at = 0.0

    async def process(
        self,
        context: ChatContext,
        call_next: Callable[[], Awaitable[None]],
    ) -> None:
        del context
        with self._reservation_lock:
            now = self._clock()
            start_at = max(now, self._next_start_at)
            self._next_start_at = start_at + self._interval_seconds
        if start_at > now:
            await self._sleep(start_at - now)
        await call_next()


CHAT_REQUEST_PACER = ChatRequestPacer()


class FoundryIQTool(MCPStreamableHTTPTool):
    """MCP tool that owns its authenticated Azure AI Search HTTP client."""

    def __init__(
        self,
        credential: TokenCredential,
        *,
        search_endpoint: str,
        knowledge_base_name: str = DEFAULT_KNOWLEDGE_BASE_NAME,
    ) -> None:
        endpoint = (
            f"{search_endpoint.rstrip('/')}/knowledgebases/{knowledge_base_name}"
            f"/mcp?api-version={FOUNDRY_IQ_API_VERSION}"
        )
        self._owned_http_client = httpx.AsyncClient(
            auth=AzureTokenCredentialAuth(credential, SEARCH_TOKEN_SCOPE),
            timeout=120.0,
        )
        super().__init__(
            name="contoso-travel-knowledge",
            url=endpoint,
            http_client=self._owned_http_client,
            allowed_tools=["knowledge_base_retrieve"],
            load_prompts=False,
            approval_mode="never_require",
        )

    async def close(self) -> None:
        try:
            await super().close()
        finally:
            await self._owned_http_client.aclose()


def create_credential() -> TokenCredential:
    """Select Azure CLI only when a local notebook explicitly opts in.

    The deployed Hosted Agent does not set ``WORKSHOP_CREDENTIAL_MODE`` and
    therefore retains ``DefaultAzureCredential`` managed-identity behavior.
    """
    mode = os.environ.get(CREDENTIAL_MODE_ENV)
    if mode == "azure-cli":
        return AzureCliCredential()
    if mode not in (None, "", "default"):
        raise ValueError(
            f"{CREDENTIAL_MODE_ENV} must be 'azure-cli', 'default', or unset; got {mode!r}"
        )
    return DefaultAzureCredential()


def create_chat_client(
    credential: TokenCredential,
    *,
    project_endpoint: str | None = None,
    model: str | None = None,
) -> FoundryChatClient:
    """Create the single Foundry chat client shared by workshop agents."""
    return FoundryChatClient(
        project_endpoint=project_endpoint or os.environ[FOUNDRY_PROJECT_ENDPOINT_ENV],
        model=model or os.environ[FOUNDRY_MODEL_ENV],
        credential=credential,
        middleware=[CHAT_REQUEST_PACER],
    )


def create_foundry_iq_tool(
    credential: TokenCredential,
    *,
    search_endpoint: str | None = None,
    knowledge_base_name: str | None = None,
) -> FoundryIQTool:
    """Create the Foundry IQ MCP adapter from explicit values or environment."""
    return FoundryIQTool(
        credential,
        search_endpoint=search_endpoint or os.environ[SEARCH_SERVICE_ENDPOINT_ENV],
        knowledge_base_name=(
            knowledge_base_name
            or os.environ.get(KNOWLEDGE_BASE_NAME_ENV, DEFAULT_KNOWLEDGE_BASE_NAME)
        ),
    )


def create_toolbox(
    credential: TokenCredential,
    *,
    toolbox_name: str | None = None,
    toolbox_endpoint: str | None = None,
) -> FoundryToolbox:
    """Create the authenticated Toolbox MCP adapter used by tools and Skills."""
    resolved_name = toolbox_name or os.environ.get(TOOLBOX_NAME_ENV, DEFAULT_TOOLBOX_NAME)
    return FoundryToolbox(
        credential,
        name=resolved_name,
        url=toolbox_endpoint,
        load_tools=True,
        approval_mode="never_require",
    )


def build_standard_travel_agent(
    *,
    chat_client: Any,
    foundry_iq_tool: Any,
) -> Agent[Any]:
    """Build the standard Agent that has one Foundry IQ tool."""
    return Agent(
        client=chat_client,
        name="travel_policy_agent",
        description="Answers Contoso travel-policy questions with Foundry IQ.",
        instructions=STANDARD_AGENT_INSTRUCTIONS,
        tools=[foundry_iq_tool],
    )


def build_harness_travel_agent(
    *,
    chat_client: Any,
    foundry_iq_tool: Any,
    toolbox: Any,
    default_mode: str = "plan",
    history_provider: Any | None = None,
    file_memory_store: Any | None = None,
    default_options: dict[str, Any] | None = None,
) -> Agent[Any]:
    """Build the Lab 7 Harness Agent."""
    skills_provider = toolbox.as_skills_provider(
        disable_load_skill_approval=True,
        disable_read_skill_resource_approval=True,
    )
    memory_store = (
        file_memory_store
        if file_memory_store is not None
        else FileSystemAgentFileStore(
            str(Path(os.environ.get("HOME") or os.getcwd()) / "agent-file-memory")
        )
    )
    return create_harness_agent(
        client=chat_client,
        name=HARNESS_AGENT_NAME,
        description=HARNESS_AGENT_DESCRIPTION,
        agent_instructions=HARNESS_AGENT_INSTRUCTIONS,
        tools=[foundry_iq_tool, toolbox],
        history_provider=(
            history_provider if history_provider is not None else InMemoryHistoryProvider()
        ),
        max_context_window_tokens=128_000,
        max_output_tokens=HARNESS_MAX_OUTPUT_TOKENS,
        file_memory_store=memory_store,
        skills_provider=skills_provider,
        mode_provider=AgentModeProvider(default_mode=default_mode),
        disable_web_search=True,
        disable_tool_auto_approval=True,
        loop_should_continue=todos_remaining(looping_modes=["execute"]),
        loop_next_message=todos_remaining_message,
        loop_max_iterations=6,
        default_options=default_options,
    )
