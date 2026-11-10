# Optional lab — Fabric IQ (expose Contoso travel and expense data in Fabric)

## Scope of this document

This lab is **not included in the main workshop duration**.
As described in the [architecture](../../docs/development/architecture.md), the core custom template
creates no Microsoft Fabric capacity, workspaces, ontologies, or data agents.
This document covers **design and connection steps** for an organization with **separate Fabric
capacity and a workspace** to connect the Contoso travel/expense scenario to Foundry agents through Fabric IQ.
For practical execution, work with a Fabric administrator who meets every prerequisite below.

> [!WARNING]
> **Preview**: Fabric IQ is public preview, without an SLA, and is not recommended for production workloads.
> Connections incur charges beyond model tokens and may send data outside Azure compliance boundaries.
> Users are responsible for this; see the [official Warning](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/fabric-iq).

## 1. Goal

Allow `contoso-travel-assistant` (the Prompt Agent from Labs 2–6) to query
**fictional Contoso travel/expense actuals** through **Fabric IQ**, separately from
the Azure AI Search `contoso-travel-policy` index (policy documents used in Lab 3).
Contrast Lab 3's Foundry IQ agentic retrieval over policy documents with Fabric IQ's
natural-language access to structured Fabric data (ontologies, semantic models, and data agents).

## 2. Prerequisites (all required; resource group Owner is insufficient)

> [!IMPORTANT]
> Main-workshop **Owner** permissions on an existing resource group do **not** prepare Fabric IQ.
> Fabric tenant, capacity, and workspace permissions are separate from Azure RG permissions.
> Assume a separate Fabric administrator has prepared everything below.

### 2.1 Fabric licenses for every caller

**Every user** calling Fabric IQ through a Foundry agent, including end users, not just developers,
needs a [Microsoft Fabric license](https://www.microsoft.com/microsoft-fabric) allowing access to the target item.
Fabric access is controlled using the caller's credentials; an agent does not bypass missing licenses.

### 2.2 Paid Fabric F2+ or Power BI Premium P1+

Fabric data agents must be published on **paid Fabric F2 or higher capacity**, or
**Power BI Premium P1 or higher capacity with Microsoft Fabric enabled**.
Free Fabric trial capacity and Power BI capacity without Fabric do not work.

### 2.3 Regions: unavailable in Power BI-only regions

Fabric IQ is unavailable where **Power BI is the only Fabric workload offered**.
The workspace must be in a region offering the full Fabric stack (lakehouse, eventhouse, OneLake, etc.).
Check [Microsoft Fabric region availability](https://learn.microsoft.com/fabric/admin/region-availability#power-bi).

### 2.4 Published Fabric item (ontology, data agent, or Power BI semantic model)

The target must be one of these, **published in advance**:

| Fabric item | Purpose | Additional requirements |
|---|---|---|
| **Ontology** | Questions based on entities, properties, and relationships | — |
| **Power BI semantic model** | Analytical questions based on measures/hierarchies | Uses the same `gpt-5.6-luna` as other LLM operations in this environment |
| **Fabric data agent** | Conversational Q&A and long-running queries | Published on paid F2+ or Power BI Premium P1+ capacity; enable tenant cross-geo processing/storage where required; data agent and its sources must use capacity in the **same region** |

The calling user or service principal also needs Fabric-side **read access**
to the item and each data source.

### 2.5 Azure RBAC roles (Foundry)

| Role | Assigned to | Purpose |
|---|---|---|
| **Foundry User** | Developer, agent runtime identity, user identities involved in OAuth | Create/run agents using Fabric IQ |
| **Foundry Project Manager** | Connection creator | Create Foundry connections to Fabric IQ endpoints |

These are roles on the same Foundry project as Labs 4/5, but the main template
does not manage extra Fabric IQ connection permissions.
Fabric and Foundry project administrators must assign roles individually for this lab.

### 2.6 Authentication: managed OAuth, BYO Entra apps, and admin consent

Authentication depends on the item:

| Fabric item | Authentication available for the initial query |
|---|---|
| Ontology | Delegated user authentication through a BYO Entra app or managed OAuth connection |
| Power BI semantic model | Same as above |
| Fabric data agent | BYO Entra app or managed OAuth through Foundry connections; user/service-principal tokens are also available only for clients accessing the data agent MCP endpoint **directly** |

- **Managed OAuth**: Foundry manages Entra app registration and consent flow.
  Setup is faster, but tenant policy may need to allow consent to multitenant applications.
- **BYO Entra app**: The organization registers its own Entra app and delegated permissions,
  and a tenant administrator explicitly grants **admin consent**. Choose this for organizational app governance.

Either approach may require tenant administrator consent or checking tenant user-consent policy during setup.
Resource group Owner does not substitute for consent.

### 2.7 Foundry Toolkit (VS Code extension)

Installing [Visual Studio Code](https://code.visualstudio.com/) and
[Foundry Toolkit for Visual Studio Code](https://code.visualstudio.com/docs/intelligentapps/overview#_install-and-setup)
provides the Toolbox UI route for adding Fabric IQ below.
This optional Toolkit route is not required by the main Dev Container.
If needed, confirm an approved, extension-compatible VS Code environment with the administrator.

## 3. Contoso scenario (fictional; not provisioned by this repository)

Assume a Fabric administrator has already prepared the following fictional data,
manually created in Fabric separately from this repository's `data/`:

- Workspace `contoso-travel-fabric-ws` in a full-Fabric-stack region on paid F2+ capacity.
- Ontology `ContosoTravelOntology`, binding `Employee`, `Trip`, and `ExpenseReport`
  entities and relationships (such as one Employee having multiple Trips) to a OneLake lakehouse.
- Published data agent `contoso-expense-fabric-agent`, a conversational Q&A endpoint based on that ontology.

Example **fictional prompts** from `contoso-travel-assistant`:

- "How many Trips submitted last week exceeded the expense policy per diem cap?"
- "Aggregate this quarter's pending expense requests by department."

These concern synthetic Contoso data only, with no real employee or expense information.

## 4. Connection steps (conceptual; work with a Fabric administrator)

### 4.1 Find the Fabric IQ server URL

MCP endpoint patterns vary by item:

| Fabric item | `server_url` pattern |
|---|---|
| Power BI semantic model | `https://api.fabric.microsoft.com/v1/mcp/fabricaihub/integrations/m365` |
| Ontology | `https://api.fabric.microsoft.com/v1/mcp/dataPlane/workspaces/{workspaceId}/items/{itemId}/ontologyEndpoint` |
| Fabric data agent | `https://api.fabric.microsoft.com/v1/mcp/workspaces/{workspaceId}/dataagents/{dataAgentId}/agent` |

Obtain `{workspaceId}`, `{itemId}`, and `{dataAgentId}` from the browser URL when opening the item in Fabric Portal.

### 4.2 Add through Toolbox in Foundry Toolkit (recommended)

As in Lab 4, add Fabric IQ **through Toolbox rather than directly to the agent**
for reuse across agents and centralized credentials, versions, and policies;
see the [official Tip](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/fabric-iq).

1. In Foundry Toolkit **My Resources > Tools**, create/open a Toolbox.
2. Select **Add tools > Configured > Fabric IQ (OneLake Catalog)**.
   Fabric IQ connections themselves, such as ontology OAuth connections, cannot be created
   directly in Toolkit. Create the connection in Foundry Portal first, then return to Toolkit.
3. Select **Publish** for a new Toolbox or **Save Changes** for an existing one.

### 4.3 SDK inspection (reference; do not change main scripts)

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FabricIQPreviewTool
from azure.identity import DefaultAzureCredential

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=FOUNDRY_PROJECT_ENDPOINT, credential=credential) as project_client,
):
    tool_payload = FabricIQPreviewTool(
        project_connection_id=FABRIC_IQ_PROJECT_CONNECTION_ID,
        require_approval="never",
    )
    agent = project_client.agents.create_version(
        agent_name="contoso-travel-assistant-fabriciq-demo",
        definition=PromptAgentDefinition(
            model=PRIMARY_MODEL_DEPLOYMENT_NAME,  # primary_model_deployment_name from .workshop/context.json
            instructions="Use Fabric IQ to answer questions about Contoso travel and expense actuals.",
            tools=[tool_payload],
        ),
    )
```

`FABRIC_IQ_PROJECT_CONNECTION_ID` is the full resource ID of the connection prepared by
the Fabric administrator and Foundry Project Manager.
It is absent from the main `.workshop/context.json` because the template creates no Fabric connections.
This is a **reference implementation**, not an addition to `scripts/`; save your own scratch file if executing it.

## 5. Validate

1. As a user with item access, send the fictional prompts in Playground.
   Verify questions using ontology terms such as `Trip` and `ExpenseReport`
   receive answers grounded in Fabric data.
2. Repeat as a user **without** item access and verify results are withheld or access denied.
   This demonstrates Fabric permission enforcement, not custom access control built in Foundry.

## 6. Cleanup outside the main dedicated resource group

- Fabric IQ Foundry connections and agent versions are project objects; delete them through
  Foundry Portal or the SDK (`project_client.agents.delete_version(...)`), as in the main workshop.
- The Fabric administrator must separately delete or suspend Fabric-side ontologies,
  data agents, and capacity in Fabric Portal. Lab 9 does not manage Fabric resources.

## 7. Recheck data boundaries and costs

> [!WARNING]
> Fabric IQ incurs charges and may send data outside Azure compliance boundaries.
> Users must assess crossed boundaries and effects on organizational compliance/geographic boundaries,
> obtaining required permissions and approvals; see the
> [official Warning](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/fabric-iq).
> Only fictional Contoso-scenario prompts are allowed in this lab.

## Official references

- [Connect agents to Microsoft Fabric with Fabric IQ (preview)](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/fabric-iq)
- [Fabric IQ overview](https://learn.microsoft.com/fabric/iq/overview)
- [Ontology overview](https://learn.microsoft.com/fabric/iq/ontology/overview)
- [Fabric data agent concept](https://learn.microsoft.com/fabric/data-science/concept-data-agent)
- [Microsoft Fabric region availability](https://learn.microsoft.com/fabric/admin/region-availability#power-bi)
- [Curate intent-based toolbox in Foundry](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/toolbox)

## Related links

- [Optional lab index](README.md)
- [Lab 3 — Foundry IQ](../03-rag-foundry-iq.md) (comparison with Foundry IQ)
- [Lab 4 — Tools and Toolbox](../04-tools-toolbox.md)
