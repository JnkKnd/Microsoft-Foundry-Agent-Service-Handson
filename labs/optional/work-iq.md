# Optional lab — Work IQ (Microsoft 365 connections; fictional prompts only)

## Scope of this document

This lab is **not included in the main workshop duration**.
Work IQ lets Foundry agents call Microsoft 365 Copilot Work IQ, accessing the
**calling user's own Microsoft 365 permissions and data**.
This repository holds/references no real Microsoft 365 tenant data, so this lab
describes **design and connection steps** only.
For practical use, use **your own authorized tenant/account** and fictional prompts only.

> [!WARNING]
> **Public preview**: Work IQ has no SLA and is not recommended for production workloads.
> Connections incur charges beyond model tokens and may send data outside Azure compliance boundaries;
> see the [official Warning](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/work-iq).
>
> All procedures and sample prompts here are **fictional**.
> Do not operate on real colleagues' email, meetings, or files without permission.

## 1. Goal

Add a Work IQ tool to `contoso-travel-assistant` and understand delegation over
Agent-to-Agent (A2A) for natural-language questions about your own fictional Microsoft 365 context,
such as mail addressed to you or your calendar.

## 2. Prerequisites (resource group Owner is insufficient)

> [!IMPORTANT]
> Tenant setup is a one-time **Microsoft Entra Global Administrator** task.
> Main-workshop Owner permissions on an existing RG cannot substitute for it.
> If a Work IQ connection already exists, skip tenant setup and proceed to adding it to the agent.

### 2.1 Commercial requirements by billing route

| Connection route | Requirement type | Requirement |
|---|---|---|
| Work IQ API through A2A, REST, or MCP | **Usage-based billing** | Enable [Copilot Credits usage-based billing](https://learn.microsoft.com/microsoft-365-copilot/usage-based-billing-overview-copilot-credits); no connector license required |
| Connector-based Microsoft 365 tools (Teams, Word, Outlook Calendar/Mail, SharePoint, OneDrive, etc.) | **Connector licenses** | Check each selected connector's prerequisites; each caller may need a [Microsoft 365 Copilot license](https://www.microsoft.com/microsoft-365-copilot/pricing/individuals) |

Distinguish billing/licensing for **Work IQ Chat** (A2A endpoint) from individual
connectors (Copilot Chat, Teams, Word, Outlook Calendar/Mail, Microsoft 365 user profile,
SharePoint, OneDrive).

### 2.2 Azure RBAC roles (Foundry)

| Role | Assigned to | Purpose |
|---|---|---|
| **Foundry User** | Developer, agent runtime identity, OAuth user identities | Create/run agents using Work IQ |
| **Foundry Project Manager** | Connection creator | Create Foundry connections to Work IQ endpoints |

### 2.3 Tenant setup (once, by Global Administrator)

Before the organization's first Work IQ connection, the Global Administrator:

1. Provisions the Work IQ service principal in the tenant.
2. Grants **tenant-wide admin consent** to delegated permission `WorkIQAgent.Ask`.

> [!NOTE]
> Activate Global Administrator **just in time** for this setup through
> [Microsoft Entra Privileged Identity Management (PIM)](https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-configure),
> then **deactivate** it. Ordinary Work IQ users do not need this role.

After setup, developers with Foundry User + Foundry Project Manager can create
Work IQ connections and add them to agents.

### 2.4 Delegated user context and On-Behalf-Of (OBO)

Requests run only within **the calling user's Microsoft 365 permissions**.
Foundry forwards them over A2A using **On-Behalf-Of (OBO)** authentication,
not the agent's own identity. Work IQ can access only mail, meetings, files,
and chats visible to the signed-in user.

### 2.5 Foundry Toolkit / Node.js prerequisites

- **Foundry Toolkit**: Install [Visual Studio Code](https://code.visualstudio.com/) and
  [Foundry Toolkit for Visual Studio Code](https://code.visualstudio.com/docs/intelligentapps/overview#_install-and-setup)
  for the Toolbox UI route.
- **JavaScript SDK**: Node.js **22 or later**, `@azure/ai-projects` **2.4.0 or later**,
  and `@azure/identity`. For Python, `azure-ai-projects>=2.3.0` suffices.

### 2.6 Direct A2A calls

Work IQ supports A2A **v1.0** and **v0.3**.
New implementations should send `A2A-Version: 1.0` and use v1 method names;
omitting the header uses v0.3.
Include location metadata for time-related requests and always use delegated user authentication.

## 3. Important data and compliance warnings

> [!WARNING]
> - Work IQ incurs charges and may send data outside Azure compliance boundaries.
>   Users must assess compliance/geographic boundaries and obtain necessary permissions/approvals.
> - Use only fictional, business-appropriate prompts within **your own actual authorized access**.
>   Do not summarize or quote others' mail, meetings, or files without their consent.
> - Contoso `data/` is synthetic policy, expense, and itinerary data unrelated to Microsoft 365.
>   It does not appear in Work IQ responses, which use only Microsoft 365 tenant data.

## 4. Contoso scenario (fictional prompt examples)

Because Work IQ accesses real data, prompts are limited to **general operation examples**
against your own mail/calendar, with fictional Contoso travel-request context:

- "Summarize recent emails about my Contoso travel request."
- "Are there meetings this week awaiting travel approval?"

These are usage templates; execution results depend on the actual signed-in user's Microsoft 365 data.
Use your own test account or an explicitly authorized account.

## 5. Add to an agent

### 5.1 Foundry Toolkit (recommended)

1. In Foundry Toolkit **My Resources > Tools**, select **+ Add Toolbox**.
2. Under **Build a Custom Toolbox**, enter a Toolbox name and description.
3. Select **Add tools > Work IQ**.
4. In **Add the Work IQ Tool**, select the Microsoft 365 Copilot data to use.
   **Work IQ Chat** uses A2A; the others (Copilot Chat, Teams, Word,
   Outlook Calendar/Mail, Microsoft 365 user profile, SharePoint, OneDrive) use MCP.
5. For each option, select an existing connection or **Create new connection**.
6. Select **Add > Publish**.

### 5.2 SDK inspection (reference; do not change main scripts)

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, WorkIQPreviewTool
from azure.identity import DefaultAzureCredential

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=FOUNDRY_PROJECT_ENDPOINT, credential=credential) as project_client,
):
    tool_payload = WorkIQPreviewTool(project_connection_id=WORK_IQ_PROJECT_CONNECTION_ID)
    agent = project_client.agents.create_version(
        agent_name="contoso-travel-assistant-workiq-demo",
        definition=PromptAgentDefinition(
            model=PRIMARY_MODEL_DEPLOYMENT_NAME,
            instructions="Use Work IQ to answer questions about the user's own Microsoft 365 context.",
            tools=[tool_payload],
        ),
    )
```

This is a **reference implementation**, not an addition to `scripts/`.
`WORK_IQ_PROJECT_CONNECTION_ID` is the full resource ID of the connection created by
the Foundry Project Manager after Global Administrator tenant setup.

## 6. Cleanup outside the main dedicated resource group

- Work IQ agent versions and Foundry connections are project objects; delete them in
  Foundry Portal or the SDK (`project_client.agents.delete_version(...)`).
- The tenant-wide Work IQ service principal and admin consent are organizational settings.
  Individual participants must not delete them; defer to tenant administrators.

## Official references

- [Connect agents to Microsoft 365 with Work IQ (preview)](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/work-iq)
- [Work IQ API overview](https://learn.microsoft.com/microsoft-365/copilot/extensibility/work-iq-api-overview)
- [Usage-based billing overview (Copilot Credits)](https://learn.microsoft.com/microsoft-365-copilot/usage-based-billing-overview-copilot-credits)
- [Microsoft Entra Privileged Identity Management](https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-configure)
- [Curate intent-based toolbox in Foundry](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/toolbox)

## Related links

- [Optional lab index](README.md)
- [A2A, Routines, and Publish](a2a-routines-publish.md) (A2A protocol details)
- [Lab 4 — Tools and Toolbox](../04-tools-toolbox.md)
