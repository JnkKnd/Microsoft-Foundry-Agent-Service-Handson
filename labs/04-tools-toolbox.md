# Lab 4 — Create a Toolbox and Skills (30 min)

## Goal

In Microsoft Foundry, group the Travel Ops API, Code Interpreter, Web Search,
and procedural Skills into `contoso-travel-toolbox`, enable **Tool Search**, and publish it.

Keep Lab 3's policy retrieval, adding API-based cost calculation and shared procedures through Skills.

| Component | Role |
|---|---|
| Foundry IQ (Lab 3 Knowledge) | Search internal policies and cite evidence. Do not move it into Toolbox |
| Travel Ops API (one OpenAPI entry) | Expose `getHealth` / `getPerDiem` / `createTripEstimate` / `createPreapproval` for deterministic queries, calculations, and simulations |
| Code Interpreter | Only compare, aggregate, and format numerical API results into tables. Do not invent policies or input values |
| Web Search | Only search current public travel information explicitly requested by the user |
| `travel-estimation` Skill | Clarify missing information, choose query/estimate APIs, and explain cost breakdowns |
| `preapproval-simulation` Skill | Confirm intent to execute and distinguish synthetic approval results from actual approval |

## What is Toolbox?

Toolbox centrally manages and shares tools and Skills used by agents.
A tool defines an operation an agent can execute; a Skill defines when and how to use it.

A published Toolbox is reusable across agents through one MCP-compatible endpoint.
Authentication, access control, guardrails, observability, and versions can also be managed per Toolbox.

This lab publishes one Toolbox containing the Travel Ops API OpenAPI tool, two built-in tools,
and two Skills for estimates and approval simulations.
With Tool Search, the model does not receive every tool definition up front.
It discovers needed definitions with `tool_search` and executes a selected tool with `call_tool`.

> [!IMPORTANT]
> Never send secrets, credentials, customer data, or personal data to Web Search.
> Treat results as untrusted external input. Use it here only for explicit requests containing public information.
> Foundry IQ is authoritative for internal policies; Travel Ops API is authoritative for cost calculations.

## 1. Prepare files to paste and upload

**Save these shared files to your PC** from GitHub.
Links point to file content. Upload ZIPs without extracting them.

Any `English` branch links are mutable browsing/download references, not release pins.
The published English artifacts below are pinned to a fixed source SHA matching the
[API release](../infra/README.md#english-release-artifacts).
Full live acceptance is still required before participant distribution.

| File | Purpose |
|---|---|
| [travel-estimation.zip](https://raw.githubusercontent.com/JnkKnd/Microsoft-Foundry-Agent-Service-Handson/0900bcbad443b055d6c4b7aefc0cfb55420ceaaa/assets/skills/travel-estimation.zip) | Estimate Skill |
| [preapproval-simulation.zip](https://raw.githubusercontent.com/JnkKnd/Microsoft-Foundry-Agent-Service-Handson/0900bcbad443b055d6c4b7aefc0cfb55420ceaaa/assets/skills/preapproval-simulation.zip) | Approval simulation Skill |
| [travel-ops.openapi.json](https://raw.githubusercontent.com/JnkKnd/Microsoft-Foundry-Agent-Service-Handson/0900bcbad443b055d6c4b7aefc0cfb55420ceaaa/assets/openapi/travel-ops.openapi.json) | Shared OpenAPI definition |

Each Skill ZIP contains `SKILL.md` at its root. Choose the ZIP, not the standalone `SKILL.md`.
The browser file picker reads your local PC.

Open the OpenAPI file in a text editor on your PC. Replace **only**
`https://replace-with-your-travel-api.example.invalid` in `servers[0].url` with
Lab 1's Azure Portal **Deployments > target deployment > Outputs > travelApiBaseUrl**.
Paste the entire modified JSON into **OpenAPI 3.0+ schema** later; that field is not a file upload.

The readable Skill sources are in `data/skills/`:

- [`travel-estimation/SKILL.md`](../data/skills/travel-estimation/SKILL.md)
- [`preapproval-simulation/SKILL.md`](../data/skills/preapproval-simulation/SKILL.md)

## 2. Open Toolbox creation in the Portal

1. In your project, open **Build > Tools**.
2. Select the **Toolboxes** tab, then **Create toolbox**.
3. Enter `contoso-travel-toolbox` for **Name**.
4. Enter this **Description**:

```text
Contoso Travel Ops API, Code Interpreter for numerical comparisons, Web Search for explicitly requested current information,
and two Skills describing cost estimates and preapproval simulations.
```

If `FoundryMCPServerpreview` was added automatically, remove it using **Actions > Remove**
at the right. It is outside this lab, and management operations must not enter Tool Search candidates.
Do not delete other organization-added tools without checking with the administrator.
Leave **Guardrail** at its default. Follow organizational requirements and do not remove existing guardrails.

## 3. Add an OpenAPI tool

1. Select **Included > + Add > Add tool**.
2. Select **Select a tool > Custom > OpenAPI tool**.
3. Select **Create** at the bottom of the dialog.

Set **Create an OpenAPI tool** as follows:

| Field | Input |
|---|---|
| **Name** | `travel_ops_api` |
| **Description** | `Travel Ops API for Contoso per diem queries, cost estimates, and preapproval simulations.` |
| **Authentication method** | `Anonymous` |
| **Connection** | Create `contoso-travel-ops-api` with **Anonymous** authentication and the same Lab 1 API endpoint |
| **OpenAPI 3.0+ schema** | Entire `travel-ops.openapi.json` with the modified `servers[0].url` |

The current Portal requires a project connection even for Anonymous authentication.
Use only the synthetic workshop API endpoint; do not enter credentials.
Select **Create tool** and verify it appears in Included.
Then set **Tool search** to **On**.

Included shows one `travel_ops_api` tool containing four operations.
Tool Search treats each operation as a separate tool. Together with Code Interpreter
and Web Search, these six tools are searchable:

| Type | Official candidate name | Purpose |
|---|---|---|
| OpenAPI | `travel_ops_api.getHealth` | Check API availability |
| OpenAPI | `travel_ops_api.getPerDiem` | Query city-specific per diem and accommodation caps |
| OpenAPI | `travel_ops_api.createTripEstimate` | Estimate travel costs |
| OpenAPI | `travel_ops_api.createPreapproval` | Simulate preapproval |
| Built-in | `code_interpreter` | Compare, aggregate, and format numbers into tables |
| Built-in | `web_search` | Search current public travel information |

The agent discovers a needed tool through `tool_search` and executes it through `call_tool`.
These two are discovery/execution meta-tools, not part of the six above.
The two Skills are MCP Resources, not tools, and are not Tool Search candidates.

> [!NOTE]
> `Anonymous` is the authentication method for the public mock API containing only synthetic data.
> **It does not mean authentication from the agent to Foundry Toolbox is Anonymous.**
> Toolbox uses Microsoft Entra ID/RBAC.

## 3.1 Check and add Code Interpreter and Web Search

1. Keep **Code Interpreter** if already in Included; otherwise add it using **+ Add > Add tool**.
2. Do the same for **Web Search**. Do not create an external connection or duplicate a tool type.
3. Verify Tool Search remains **On**.

If Code Interpreter opens an optional **Upload files** dialog, select **Attach**
without adding files. No participant files are needed for this exercise.

Limit Code Interpreter to comparing, aggregating, and tabulating numbers returned by Travel Ops.
Use Web Search only for explicit requests for current public travel information,
and include source URLs and retrieval time in the answer.
Neither should run for ordinary policy questions or estimates.

## 4. Upload two Skills

1. Select **Included > + Add > Add skill**.
2. Under **Select a skill > Configured**, select **Add skill**.
3. Select **Upload skill** from the menu.
4. Select **Browse**, then the `travel-estimation.zip` saved on your PC.
5. Verify the filename and **Name = travel-estimation**, then select **Upload**
   (**Create** in earlier Portal versions).
   Name and Description are read from `SKILL.md` inside the ZIP.
6. Return to Toolbox and verify the Skill appears in Included.
7. Repeat **Add skill > Upload skill** with `preapproval-simulation.zip`.
   Verify **Name = preapproval-simulation** and select **Upload**.

Uploaded Skills enter Included automatically. To use an already registered Skill,
select it from **Configured** in the same project and select **Add**.

Read `SKILL.md` before and after upload to check this separation of responsibilities:

- `description` defines **when to use it**, distinguishing per diem/estimates from approval simulations.
- The body defines **how to use it**: input checks, API selection, and result explanations.
- Do not duplicate policy amounts or approval conditions; use Foundry IQ and the API as sources.
- Do not run an approval simulation for an estimate-only request.

> [!NOTE]
> Guardrail applies responsible AI (RAI) content filtering to Toolbox tool inputs and outputs.
> It operates at the Toolbox layer independently of model-side content filters.
> This workshop does not create, configure, or validate Guardrails; leave displayed defaults unchanged.
> Preserve any Guardrail required by your organization.

## 5. Publish the Toolbox

1. Verify Included contains **travel_ops_api / Code Interpreter / Web Search /
   travel-estimation / preapproval-simulation** and Tool search is **On**.
2. Select **Create** at the top right (**Publish** in earlier Portal versions).
3. Reopen the saved Toolbox and verify the five entries, Tool search On,
   version, and MCP endpoint. A versioned endpoint, not the button label alone,
   is the checkpoint for the next step.

## 6. Connect the Prompt Agent using Microsoft Entra

Agents call Toolbox through the common MCP protocol.
**Do not delete Lab 3's Knowledge.**

1. In the published Toolbox, use **Call this toolbox > Endpoint > Copy endpoint**.
2. Open **Build > Agents > contoso-travel-assistant**.
3. Under **Tools**, select **Add > Add tools** (not Add under Knowledge).
4. Select **Custom > Model Context Protocol (MCP)**, then **Create**.
5. Set:

| Field | Value |
|---|---|
| Name | `contoso-travel-toolbox-mcp` |
| Remote MCP Server endpoint | Endpoint copied from the published Toolbox |
| Authentication | **Microsoft Entra** |
| Type | **Project Managed Identity** |
| Audience | `https://ai.azure.com/` |

6. Check each field and select **Connect**.
7. Verify the connection appears in Tools and `contoso-travel-knowledge-lab` remains in Knowledge,
   then select **Save**.

The current Portal can display the connection as a native
**contoso-travel-toolbox v...** group instead of the entered MCP connection name.
Record the displayed Toolbox and agent versions.
If either Skill shows **Needs configuration**, open its **Configure** dialog.
An **Auto-provisioned container** environment incurs additional charges: obtain
approval before selecting it and saving. Do not upload files or change the
agent's Harness or Guardrail to bypass configuration. Saving these settings
can create another Toolbox version; recheck both versions after **Save**.
Configuration alone does not prove that the Skill was loaded or executed.

Do not use API keys or manually obtained bearer tokens.

Keep the existing agent instructions (Lab 3 policy retrieval) and append these boundaries, then **Save**:

```text
- Retrieve internal policies and evidence from Foundry IQ Knowledge.
- Use deterministic Travel Ops API results for per diem, travel estimates, and preapproval simulations.
- When a Toolbox tool is needed, discover candidates with tool_search and execute the selected tool with call_tool.
- For tool_search query, use one English tool name matching the purpose, not a descriptive sentence:
  createTripEstimate for estimates, getPerDiem for per diem, createPreapproval for explicitly requested approval simulations,
  code_interpreter for numerical calculations, and web_search for explicitly requested public-information searches.
  Check the discovered tool's official name and inputSchema before call_tool; do not guess undiscovered tools.
- Use Code Interpreter only to compare, aggregate, and tabulate numerical API results; do not invent policy values or itineraries.
- Use Web Search only when the user explicitly requests current public travel information; include source URLs and retrieval time.
  Do not send secrets, credentials, personal information, or customer data to search.
- Do not call createPreapproval for estimate-only requests. Run a synthetic preapproval simulation only after confirming
  explicit intent to execute, and state clearly that it is not an actual approval or booking.
```

If **Microsoft Entra** is absent under **Authentication**, or **Project Managed Identity**
is absent under **Type**, do not create the connection. Check that Lab 1 managed identity
and RBAC validation succeeded, and inform the instructor.
Do not switch to API keys or manual bearer tokens.

The retained [Toolboxes tab](../docs/images/lab04-toolboxes-tab.png),
[OpenAPI form](../docs/images/lab04-openapi-form.png), and
[MCP connection](../docs/images/lab04-connect-toolbox.png) screenshots are historical/illustrative,
not English instructions or success evidence for this revision. Endpoint values are environment-specific.

## 7. Auto-approve tools on the workshop MCP connection

Auto-approve tools on `contoso-travel-toolbox-mcp` so calls do not show confirmation dialogs,
allowing this lab's checks and Lab 5 / 6 automated evaluations to run without interruption.

Apply this only to the workshop-specific MCP connection using synthetic data.
Do not apply it to general business APIs or pre-added management tools.

1. In the agent's Tools, open **contoso-travel-toolbox-mcp > Actions > Configure**.
2. Under **Approval setting for tools in this MCP server for this agent**, select
   **Always auto-approve all tools**.
3. Select **Apply**, then **Save** on the agent.

If the native Toolbox group does not expose this scoped setting, stop before
Labs 5 / 6. Do not assume the chat menu's **Always approve all tools** has the
same scope. For a diagnostic estimate only, inspect the displayed operation
and arguments and use **Approve once**. This verifies that invocation, not
persistent auto-approval or unattended evaluation readiness.

The [approval setting screenshot](../docs/images/lab04-batch-approval-setting.png) is historical/illustrative.
This controls confirmation when the model calls tools. It neither disables Microsoft Entra
authentication/RBAC nor grants actual travel approval.

## 8. Verify Tool Search and actual tool execution in Trace

Create a **New chat** in Playground, enter this, and select **Send**:

```text
Estimate costs for a business trip from Tokyo to New York, 2026-07-10 through 2026-07-15,
for 1 traveler in business class. Do not make a booking or run an approval simulation.
```

Verify a final answer with a cost breakdown and total.
If a confirmation dialog appears, persistent auto-approval has not been verified;
follow section 7 rather than starting unattended evaluation or optimization.

After the answer, inspect tool calls in **Traces**:

1. Select **Traces** below the Playground answer to open **Conversations view**.
   If unavailable, open **Build > Agents > contoso-travel-assistant > Traces**.
2. Open the `conv_...` (Conversation) corresponding to your submission time.
   IDs differ for each run.
3. In **Trajectories**, expand `invoke_agent contoso-travel-assistant` and check this order:
   - `tool_search` discovers the estimate tool.
   - `call_tool` selects it.
   - Toolbox executes `travel_ops_api___createTripEstimate`.
4. In the executed tool's **Input + Output**, check the cities, dates, seat class,
   traveler count, and output `total_estimate`. It must match the Playground answer's total.
5. Verify that `getHealth`, `getPerDiem`, `createPreapproval`, Code Interpreter, and Web Search
   did not execute. Appearing as a Tool Search candidate is not execution.

Depending on the Portal version, the actual tool may appear inside `call_tool`,
at another level, or as `execute_tool`. Check the tool name in **Input + Output**,
not just the display name.
If only the downstream operation appears, record the API invocation separately:
Tool search **On** and a correct API answer do not prove the
`tool_search` / `call_tool` sequence. Do not report the complete checklist as passed.

### Optional: Check purpose-specific tool selection

These two cases verify selection of different capabilities according to the request.

#### Aggregate the estimate

Return to the same Playground chat containing the section 8 estimate and send:

```text
Use Code Interpreter to calculate the proportions of airfare, accommodation, and per diem
in the previous estimate and format them as a table. Do not assume new policy values or itineraries.
```

Verify in Trace that `code_interpreter` executed using only API-returned amounts.

#### Check costs and approval procedures together

In **New chat**, send:

```text
I am traveling from Tokyo to New York, 2026-07-10 through 2026-07-15, with 1 traveler in business class.
Estimate the cost and summarize the business-class approvers and approval order, the application feature,
and the standard maximum business days from application to completed approval, with policy evidence.
Do not make a booking or run an approval simulation.
```

This question does not specify which capabilities to use. Verify that the agent chooses them
according to the content and records both in Trace:

- Toolbox: `travel_ops_api___createTripEstimate`
- Foundry IQ: `knowledge_base_retrieve`

## Completion checklist

- Published a Toolbox with OpenAPI, Code Interpreter, Web Search, two Skills, and Tool Search On.
- Confirmed `tool_search → call_tool → createTripEstimate` in Trace.
- Confirmed an estimate request does not call unrelated tools or `createPreapproval`.
- Both Skills are registered and published in Toolbox.

> [!NOTE]
> This lab verifies registration and publication of both Skills only.
> Portal Prompt Agents do not expose verification of loading Skills published as MCP Resources.
> Do not equate registration with use. Verify actual loading in Lab 7 using `load_skill` / `resources/read`.

## Optional: Inspect Toolbox through the SDK

[`notebooks/04-create-toolbox.ipynb`](../notebooks/04-create-toolbox.ipynb) is supplementary material
for inspecting/updating the Portal-created Toolbox through the SDK, not required for main-lab completion.

To run it, complete Lab 7's [shared environment setup](../docs/participant/environments/codespaces.md)
and `notebooks/00-setup.ipynb`, then choose **Python (Foundry Workshop)**.
The notebook supports:

- Updating OpenAPI while preserving existing Skills, tools, guardrail, and Tool Search
- Adding missing built-in tools and Tool Search
- Calling the Prompt Agent and inspecting tool Input / Output

Use this lab's Portal steps for Skill upload.

Official documentation: [Toolbox](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/toolbox) /
[Skills](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/skills).
See [Toolbox troubleshooting](../docs/participant/troubleshooting.md#lab-4-files) if needed.

## Next lab

[Lab 5 — Agent evaluation in the Portal](05-evaluation.md)
