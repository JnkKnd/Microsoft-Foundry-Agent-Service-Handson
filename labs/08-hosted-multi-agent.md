# Lab 8 — Deploy a sequential workflow of ordinary agents as a Hosted Agent (30 min)

## Goal

Create three ordinary Microsoft Agent Framework agents and deploy them to Microsoft Foundry
as a sequential workflow.

The notebook does not use a workshop-specific factory. Directly write `AzureCliCredential`,
`FoundryChatClient`, `MCPStreamableHTTPTool`, instructions for three agents,
`chat_client.as_agent()`, and `SequentialBuilder` to examine construction order.
The deployment source in `src/hosted-agent/` separates the same configuration into reusable modules.

```text
intake_agent -> policy_agent -> reviewer_agent
```

| Agent | Responsibility | Connected capabilities |
|---|---|---|
| `intake_agent` | Organize itinerary and questions | model |
| `policy_agent` | Retrieve internal policies and organize document IDs/sources | model + Foundry IQ |
| `reviewer_agent` | Compare the original request with evidence and produce the final answer | model |

Lab 7's Harness Agent is a separate exercise, not part of this workflow.
Here, examine ordinary-agent roles, handoffs, and Hosted deployment.

> [!WARNING]
> Notebook model / Foundry IQ calls, source remote build, and Hosted Agent runtime incur charges.
> Do not resubmit running cells or Hosted Agent requests.

## 1. Inspect ordinary agents and workflow in the notebook

Complete Lab 1 initialization and Lab 7's shared environment / `notebooks/00-setup.ipynb` first.

1. In Codespaces or local Dev Container VS Code, open
   [`notebooks/08-hosted-agent.ipynb`](../notebooks/08-hosted-agent.ipynb).
2. Choose **Select Kernel > Jupyter Kernel... > Python (Foundry Hosted Agent)**,
   using `foundry-hosted-agent` venv (Python 3.13).
3. Read explanations and run one cell at a time from the top. Do not skip errors.

See the [Codespaces shared steps](../docs/participant/environments/codespaces.md#shared-steps)
and [local Dev Container prerequisites](../docs/participant/environments/local-dev-container.md).

The notebook proceeds through:

1. Reading model, Search, and Foundry IQ connections from `.workshop/context.json` at `resource_outputs.<key>.value`
2. Directly creating Azure CLI credentials, a shared chat client, and a Foundry IQ MCP tool
3. Reading instructions and creating three ordinary agents
4. Fixing execution order with `SequentialBuilder`
5. Displaying the actual graph using `WorkflowViz` and Graphviz
6. Running a synthetic policy question and comparing intermediate answers with the reviewer's final answer
7. Checking that notebook and deployment-source instructions / request match
8. Running contract tests without Azure

With Graphviz available, an SVG shows these three participants connected in order:

```text
intake_agent -> policy_agent -> reviewer_agent
```

Only the notebook uses `intermediate_output_from="all_other"` to display intake/policy intermediate answers.
The deployed workflow returns only the reviewer's final answer.

### Check execution results

The standard synthetic request asks for meal per diem, accommodation cap, and expense submission
deadline for domestic Tokyo–Osaka travel, with evidence. It does not estimate costs or calculate budgets.

Verify:

- Order: `intake_agent` → `policy_agent` → `reviewer_agent`
- Only `policy_agent` executes `knowledge_base_retrieve`
- Policy document IDs, titles, citations or source URLs remain
- The final answer includes **Request summary / Policy findings / Next actions**
- No Toolbox, Skill, `tool_search`, `call_tool`, or Travel Ops API executes
- The answer explicitly states no actual booking, approval, or expense settlement occurred

Lab 7 session, todos, memory, and outputs are not inherited.
If Lab 3's Foundry IQ is ready, Lab 8 can run without Lab 7 agent execution.
The shared Dev Container, Azure CLI sign-in, and `00-setup.ipynb` remain required.

## 2. Deploy the Hosted Agent

After checking the notebook and contract tests, use the same notebook's
**Python (Foundry Hosted Agent)** kernel to run management-command preparation and deploy cells,
entering **DEPLOY** in the confirmation field. Check the displayed subscription / RG before execution.
Cells explicitly invoke the management `foundry-workshop` venv (Python 3.12)
through `WORKSHOP_MANAGEMENT_PYTHON`, avoiding mixed Hosted SDK dependencies.
This does not rerun Lab 1's template.

The script packages `src/hosted-agent/` into a source ZIP, performs Python 3.13 source remote build,
grants required runtime-identity permissions, and checks status.
No manual ZIP preparation or participant ACR is needed; Foundry performs the build.
If authentication expired, return to the [shared sign-in steps](../docs/participant/environments/codespaces.md#shared-steps).
Deployment is complete when this is returned:

```json
{
  "agent_name": "contoso-travel-hosted-planner",
  "status": "active"
}
```

## 3. Run in the Portal

1. In Microsoft Foundry Portal, open **Build > Agents**.
2. Select `contoso-travel-hosted-planner`.
3. In **Details**, verify **Status = Running** and **Responses protocol = Active**.
4. Return to **Playground**, selecting **New chat** if a previous conversation exists.
5. Enter this and select **Send**:

```text
I am traveling from Tokyo to Osaka for an internal review on 2026-09-10 through 2026-09-11, with 1 traveler in economy. Summarize the domestic meal per diem, hotel cap, and reimbursement deadline, with policy document IDs or links. Do not perform cost estimates, bookings, applications, approvals, or reimbursements.
```

Initial Hosted Agent startup takes time. Do not resubmit while Log stream is active.
If only the first call immediately after deployment returns Search `403`,
wait for role assignment propagation and resend the same request; do not create another version.

## Completion checklist

- Hosted Agent returns a complete response.
- Execution order is `intake_agent` → `policy_agent` → `reviewer_agent`.
- `policy_agent` Trace includes `knowledge_base_retrieve`.
- Policy values and sources agree with Foundry IQ results.
- No Toolbox / Skills / Travel Ops API is called.
- No actual booking, approval, or expense settlement is claimed.

Compare Prompt Agent and Hosted workflow Traces in the next lab.

## Delete when finished

After comparing Traces and saving results, check the target in this notebook's delete cell
and enter the displayed **Agent name** (`contoso-travel-hosted-planner`) in the confirmation field.
Deletion also runs in management `foundry-workshop` venv.
Verify the Hosted Agent and all versions are deleted before cleaning up the Codespace and dedicated RG,
in that order. Follow [Lab 9](09-observability-cleanup.md) for detailed steps.

## Next lab

[Lab 9 — Trace comparison and cleanup](09-observability-cleanup.md)
