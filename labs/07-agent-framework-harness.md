# Lab 7 — Build an Agent and Harness Agent with Agent Framework (45 min)

## Goal

Use the same information sources as the Portal-built `contoso-travel-assistant`
from Microsoft Agent Framework agents created in Python.

Build these in order in the notebook:

1. **Plain Agent**: Connect only Lab 3's Foundry IQ to learn the minimal code-based agent configuration.
2. **Harness Agent**: Retain Foundry IQ and add Lab 4's Toolbox tools and Skills,
   decomposing complex requests into plan / todos / execute.

This lab does not use a workshop-specific agent factory. Directly import and construct
`AzureCliCredential`, `FoundryChatClient`, `MCPStreamableHTTPTool`, `Agent`,
`FoundryToolbox`, and `create_harness_agent` in the notebook to inspect each argument's role.

Skills published in Lab 4 are first loaded here through `load_skill`.
Use execution records to distinguish registration in Toolbox from actual agent use.

> [!WARNING]
> Agents run in the notebook container, but model, Foundry IQ, and Toolbox tools
> call billable Azure services. Do not rerun cells that are waiting for results.

## Plain Agent and Harness Agent

Both run through `run()` as ordinary Agent Framework `Agent` instances.
Their difference is the execution-support features added during construction.

| Configuration | What this lab examines |
|---|---|
| `Agent(...)` | Minimal configuration with explicit client, instructions, and tools |
| `create_harness_agent(...)` | Factory combining an ordinary agent with mode, todos, memory, Skills, and a loop |

`create_harness_agent` is not a decorator, separate Azure resource, or multi-agent workflow.
It manages complex work within one agent. Lab 8 explicitly connects multiple ordinary agents.

## 1. Prepare Codespaces and open the notebook

1. Follow [Codespaces setup](../docs/participant/environments/codespaces.md) and sign in to
   Azure CLI in the container Terminal. Local participants use the
   [same Dev Container](../docs/participant/environments/local-dev-container.md).
2. Run `notebooks/00-setup.ipynb` with **Python (Foundry Workshop)**,
   creating `.workshop/context.json` from the subscription ID and RG name.
3. In VS Code Explorer, open
   [`notebooks/07-agent-framework-harness.ipynb`](../notebooks/07-agent-framework-harness.ipynb).
4. Under **Select Kernel > Jupyter Kernel...**, choose
   **Python (Foundry Hosted Agent)** (`foundry-hosted-agent`, Python 3.13).
5. Read the explanations and run one cell at a time from the top. Do not skip errors.

Notebooks, source, and scripts are already in the repository; no manual collection/upload is needed.
The notebook reads `.workshop/context.json` at `resource_outputs.<key>.value`,
so no manual connection or model deployment entry is needed.
Saving the notebook does not persist the running session, todos, or memory.
After a kernel restart, rerun required cells from connection setup in order and recheck the plan.

## 2. Plain Agent with Foundry IQ

The first half constructs:

```text
FoundryChatClient
  + instructions
  + Foundry IQ MCP tool
  = travel_policy_agent
```

- `FoundryChatClient`: client that sends questions to the model
- `instructions`: agent role and response policy
- `MCPStreamableHTTPTool`: connection to Lab 3's knowledge base
- `Agent`: combines these components into a runnable unit with `run()`

Send Lab 3's multi-policy question and check `knowledge_base_retrieve` and citations.
Toolbox is not supplied yet, so cost calculation and Web Search are unavailable.

## 3. Harness Agent with Toolbox and Skills

The second half adds these to the same Foundry IQ:

```text
Foundry IQ
  + Lab 4 Toolbox
      - tool_search / call_tool
      - Travel Ops OpenAPI
      - Code Interpreter
      - Web Search
      - travel-estimation Skill
      - preapproval-simulation Skill
  + plan / execute mode
  + todos / bounded loop
  = travel_harness_agent
```

`FoundryToolbox` loads Toolbox tools over MCP.
`toolbox.as_skills_provider()` exposes Skill names/descriptions and lazily loads
only the needed Skill body with `load_skill`, rather than including every body in every prompt.

Disable Web Search automatically added by Harness Agent, so every Lab 4 callable tool,
including Web Search, goes through Toolbox Tool Search.

## 4. Decompose a complex request in plan mode

The notebook's synthetic request includes policy checks, cost estimation, budget comparison,
current public information, and a preapproval simulation.

The initial run uses **plan mode**. Rather than immediately producing a final answer,
it breaks work into smaller tasks with `todos_add` and presents a plan.

Read the plan and verify:

- Foundry IQ retrieves internal policies and approval procedures.
- The `travel-estimation` Skill is loaded to check estimate tool usage.
- Travel Ops API returns a deterministic cost estimate.
- Code Interpreter computes budget difference and utilization.
- Web Search retrieves only explicitly requested current information.
- The `preapproval-simulation` Skill is loaded for a synthetic approval simulation.

Ensure the plan includes no unnecessary work or actual bookings/approvals.

## 5. Complete todos in execute mode

In the cell after plan review, switch the same `AgentSession` to **execute mode**.
Do not recreate the session; keep the todos from plan mode.

Execute mode reruns the Harness Agent only while todos remain incomplete.
Iterations are bounded, and tool errors are not treated as success.

Verify at least these in the notebook execution records:

1. `knowledge_base_retrieve` retrieves internal policies.
2. `load_skill` retrieves the relevant Skill body.
3. `tool_search` discovers the needed tool schema.
4. `call_tool` executes the selected tool.
5. Travel Ops / Code Interpreter / Web Search results are reflected in individual todos.
6. `todos_complete` leaves no incomplete items.

Tool Search does not decompose complex requests; it discovers candidate tools on demand to save context.
Harness mode, TodoProvider, session, and loop handle decomposition and progress.

## Completion checklist

- Built ordinary `Agent(...)` from client / instructions / tools and verified Foundry IQ answers.
- Can explain that `create_harness_agent(...)` is a factory returning an ordinary Agent.
- Plain Agent has only Foundry IQ; Harness Agent has Foundry IQ + Toolbox + Skills.
- Plan mode decomposed the request into todos; after review, the same session switched to execute mode.
- Verified `load_skill` and Skill resource loading.
- Verified `tool_search`, `call_tool`, and the selected actual tool in order.
- No todos remain incomplete, and failed tools were not counted as success.
- The final answer distinguishes internal policies, API results, and current external information with sources and retrieval times.
- The answer explicitly states that no actual booking/approval occurred.

## Skipping Lab 7 execution and proceeding to Lab 8

Lab 8 does not inherit this notebook's session, todos, memory, or output.
It uses a sequential workflow of ordinary `intake_agent`, `policy_agent`, and `reviewer_agent`.
Experienced participants may skip Lab 7 agent execution if Lab 3's Foundry IQ is ready.
However, the shared Dev Container, Azure CLI sign-in, and `00-setup.ipynb` preparation remain mandatory.

When taking the labs consecutively, observe the single-agent mechanisms here,
then compare them with role separation across multiple ordinary agents in Lab 8.

## References

- [Microsoft Agent Framework — Agent Harness](https://learn.microsoft.com/agent-framework/concepts/harness)
- [Microsoft Agent Framework — Agent Skills](https://learn.microsoft.com/agent-framework/agents/skills)
- [Microsoft Agent Framework — Microsoft Foundry Toolbox](https://learn.microsoft.com/agent-framework/integrations/by-component/tools/foundry-toolbox)
- [Microsoft Foundry — Foundry IQ](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)

## Next lab

[Lab 8 — Sequential workflow of ordinary agents](08-hosted-multi-agent.md)
