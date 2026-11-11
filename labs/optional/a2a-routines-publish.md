# Optional lab — A2A, Routines, and Teams/M365 publishing (preview)

## Scope of this document

This lab covers three independent preview capabilities: calling Foundry agents externally,
automatically triggering them, and publishing to Teams or Microsoft 365.
None is part of the main workshop; **all are preview**.
For safety, external-agent communication uses a local simulated mock within this lab,
not real external services or secrets.

> [!WARNING]
> These examples do not register real Microsoft Entra applications, create real Bot Service
> resources, or publish to real Teams environments. They explain future configuration
> and show simulated local interactions. Obtain organizational security/compliance approval
> before implementing them.

## 1. Incoming A2A (external agent access, preview)

### 1.1 Prerequisites

| Item | Requirement |
|---|---|
| Protocol | Agent implements **Responses**; see [Advanced Hosted Agent](advanced-hosted-agent.md). Prompt agents support Responses by default |
| Azure role | **Foundry User** |
| Network | Project public network access enabled; otherwise use REST API and separate networking procedures, not A2A |
| Targets | Prompt agents and Hosted Agents implementing Responses |

> [!NOTE]
> A2A is unnecessary for delegation **between Foundry agents**.
> Within one Foundry project, use Microsoft Agent Framework workflows as in
> [Lab 8](../08-hosted-multi-agent.md), or prompt-agent connected agents.
> A2A is a preview interoperability protocol for **agents outside Foundry**,
> including other platforms/vendors.

### 1.2 Conceptual enablement flow

1. In Foundry Portal or the SDK, enable A2A for the agent to expose
   (for example, `contoso-travel-assistant`).
2. Foundry generates an **agent card**, metadata describing capabilities, endpoint, and authentication.
3. The external caller retrieves the card, then sends a request.

### 1.3 Safe simulated external agent (lab only, no actual communication)

This **illustrative pseudocode** shows the shape of an external agent's A2A request.
`https://example-invalid.contoso-lab.invalid` is deliberately a **nonresolving fictional domain**,
not a real destination. Real A2A connections must use the endpoint and credentials
obtained from your Foundry project's agent card.

```python
# Illustrative pseudocode. No external request is sent.
SIMULATED_EXTERNAL_AGENT_CARD = {
    "name": "contoso-partner-demo-agent",
    "endpoint": "https://example-invalid.contoso-lab.invalid/a2a",
    "protocolVersion": "1.0",
    "note": "This is a fictional agent card for lab illustration only.",
}


def simulated_a2a_call(prompt: str) -> dict:
    """Illustrate an A2A request to an external agent without sending it."""
    return {
        "request_would_be_sent_to": SIMULATED_EXTERNAL_AGENT_CARD["endpoint"],
        "headers": {"A2A-Version": "1.0"},
        "body_preview": {"input": prompt},
        "status": "SIMULATED — no network call performed",
    }
```

### 1.4 Versions

A2A supports v1.0 (recommended; send `A2A-Version: 1.0`) and v0.3
(default when the header is omitted). Explicit v1.0 is recommended for new implementations.

## 2. Routines (preview)

### 2.1 Overview

A Routine associates **one trigger with one action**.
Unlike workflows (Agent Framework in Lab 8), which handle complex branching and
multi-agent orchestration, Routines suit simple automation:

| Trigger | Example |
|---|---|
| One-time timer | Once tomorrow at 9:00, summarize and post pending travel requests |
| Recurring schedule | Every Monday at 9:00, generate last week's Contoso travel expense summary |
| Event | When a GitHub issue is created, summarize it in a comment |

### 2.2 Fictional Contoso scenario

```text
Trigger: Every Friday at 17:00 (recurring schedule)
Action: Invoke contoso-travel-assistant with:
  "Summarize the count and total amount of Contoso travel requests approved this week."
```

This is a **fictional configuration**, not an operation on real data.
Execution results are available in Foundry Portal run history.
Supported trigger/action types may change during preview.

### 2.3 Choosing between them

- Use **Routines** for one fixed prompt at a fixed time or one action on an event.
- Continue using **Agent Framework workflows** ([Lab 8](../08-hosted-multi-agent.md))
  for multiple agents, conditional branches, or human approval steps.

## 3. Publish to Teams and Microsoft 365 (preview)

### 3.1 Prerequisites

| Item | Requirement |
|---|---|
| Protocol | Agent implements Responses (automatically bridged to Activity) |
| Azure role (RG scope) | **Azure Bot Service Contributor**, including `Microsoft.BotService/botServices/write` and `channels/write`; Contributor or Owner also suffices |
| Foundry role | **Foundry User** |
| Network | Project public network access enabled |
| Organization-wide publication | **Organizational administrator approval** by Microsoft 365 / Teams administrators through Teams admin center |

> [!IMPORTANT]
> Personal testing (only you can install) and organization-wide availability are different.
> The latter requires Microsoft 365 / Teams administrator approval.
> Workshop participant RG Owner permissions alone do not authorize organization-wide publication.

### 3.2 Conceptual flow

1. Select the agent in Foundry Portal, then Teams / M365 Copilot under **Channels**,
   creating a bot registration (requires Azure Bot Service Contributor).
2. For personal testing, sideload the generated Teams app manifest.
3. For organization-wide distribution, request approval through Teams admin center.

This lab does not create actual bot registrations or publish Teams apps.
Its purpose is understanding which roles approve each operation.

## 4. Data and security considerations

- All three capabilities are **preview**, without SLA coverage.
- Code/configuration examples do not make real external calls or create Azure resources.
- Before enabling them, check both [costs and cleanup](../../docs/participant/costs-and-cleanup.md)
  and organizational data governance policies.

## Official references

- [Enable incoming Agent-to-Agent (A2A) requests](https://learn.microsoft.com/azure/foundry/agents/how-to/enable-agent-to-agent-endpoint)
- [Routines in Foundry Agent Service (preview)](https://learn.microsoft.com/azure/foundry/agents/concepts/routines)
- [Publish an agent to Microsoft 365 Copilot and Microsoft Teams](https://learn.microsoft.com/azure/foundry/agents/how-to/publish-copilot)
- [Hosted agents in Foundry Agent Service](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)

## Related links

- [Optional lab index](README.md)
- [Advanced Hosted Agent](advanced-hosted-agent.md) (Responses/Activity details)
- [Work IQ](work-iq.md) (an example using A2A + OBO)
- [Lab 8 — Agent Framework workflow](../08-hosted-multi-agent.md)
