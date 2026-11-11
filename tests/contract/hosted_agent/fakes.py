"""Network-free chat client used by the sequential workflow tests."""

from __future__ import annotations

from typing import Any

from agent_framework import Agent
from workflow import (
    INTAKE_AGENT_INSTRUCTIONS,
    POLICY_AGENT_INSTRUCTIONS,
    REVIEWER_AGENT_INSTRUCTIONS,
    SIMULATION_NOTICE,
)

INTAKE_RESPONSE = (
    "Intake summary: Tokyo to Osaka, 2026-09-10 through 2026-09-11, 1 traveler, economy."
)
POLICY_RESPONSE = (
    "Policy findings: Domestic Tier 1 meal per diem is JPY 3,000 per day, "
    "with a hotel cap of JPY 15,000 per night. "
    "Submit reimbursement within 30 days after the trip ends. "
    "Sources: policy-per-diem-001, policy-hotels-001, policy-general-001."
)
REVIEWER_RESPONSE = (
    "Request summary: An internal review trip from Tokyo to Osaka.\n"
    "Policy findings: Verified per diem, hotel cap, reimbursement deadline, and document IDs.\n"
    f"Next actions: Check the original policies before applying.\n{SIMULATION_NOTICE}"
)


class ScriptedChatClient:
    """Implements the same ``as_agent`` boundary as ``FoundryChatClient``."""

    def __init__(self) -> None:
        self.created_agents: list[str] = []
        self.created_agent_tools: dict[str, list[Any]] = {}
        self.calls: list[dict[str, Any]] = []
        self.include_policy_tool_events = False

    def as_agent(
        self,
        *,
        name: str,
        instructions: str,
        tools: list[Any] | None = None,
    ) -> Agent:
        self.created_agents.append(name)
        self.created_agent_tools[name] = list(tools or [])
        return Agent(client=self, name=name, instructions=instructions, tools=tools)

    def get_response(
        self,
        messages: Any = None,
        *,
        stream: bool = False,
        options: Any = None,
        **_: Any,
    ) -> Any:
        options = options or {}
        instructions = options.get("instructions") or ""
        message_texts = [message.text for message in (messages or [])]
        self.calls.append(
            {
                "instructions": instructions,
                "messages": message_texts,
            }
        )
        text = self._response_for(instructions)

        if stream:
            from agent_framework import ChatResponseUpdate, Content, ResponseStream

            async def _stream() -> Any:
                if self.include_policy_tool_events and instructions == POLICY_AGENT_INSTRUCTIONS:
                    yield ChatResponseUpdate(
                        contents=[
                            Content(
                                type="text",
                                text="",
                                name="knowledge_base_retrieve",
                            )
                        ],
                        role="assistant",
                    )
                midpoint = len(text) // 2
                for chunk in (text[:midpoint], text[midpoint:]):
                    yield ChatResponseUpdate(
                        contents=[Content.from_text(chunk)],
                        role="assistant",
                    )

            return ResponseStream(_stream())

        async def _response() -> Any:
            from agent_framework import ChatResponse, Message

            return ChatResponse(messages=[Message(role="assistant", contents=[text])])

        return _response()

    @staticmethod
    def _response_for(instructions: str) -> str:
        if instructions == INTAKE_AGENT_INSTRUCTIONS:
            return INTAKE_RESPONSE
        if instructions == POLICY_AGENT_INSTRUCTIONS:
            return POLICY_RESPONSE
        if instructions == REVIEWER_AGENT_INSTRUCTIONS:
            return REVIEWER_RESPONSE
        raise AssertionError(f"Unexpected agent instructions: {instructions}")
