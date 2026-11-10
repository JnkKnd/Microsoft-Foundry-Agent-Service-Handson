# Instructor runbook

## Before the event

1. Follow [administrator prerequisites](../docs/admin/prerequisites.md) to check
   permissions, fixed Japan East models, Search Basic, and Codespaces quotas / policies.
2. Distribute template / material references only after the same guide's publication
   checks, and identify the subscription to use. Do not ask participants to manually
   enter model versions, image digests, or source SHAs.
   English artifacts are [published and pinned](../infra/README.md#english-release-artifacts);
   full live acceptance is still required before distribution.
3. Give local participants the [Dev Container prerequisites](../docs/participant/environments/local-dev-container.md).
4. Assign budget / alert and cleanup owners and failure contacts.

## Real-environment validation scope

Pre-event end-to-end validation covers every participant Lab (1–9), redeployment,
and cleanup. Before creating Azure / Codespaces environments, confirm targets,
costs, personal authentication, and execution environments.
The following are acceptance criteria, not completed results.

At the start, fix the material / template revision and maximum wait for each operation.
If anything is changed during validation, restart from the beginning at the same
corrected revision and verify that no off-procedure rescue operations are needed.
Record Codespaces and local Dev Container results separately; success in one does
not verify the other. Do not omit Labs from all-Lab validation even when participant
instructions permit skipping them.

Record results and unperformed scope outside the repository.
CI and simulated JSON are preliminary checks, distinct from real UI success.
Obtain approval in advance for scope changes caused by cost, permissions,
authentication, or similar constraints, and report them as limited validation.
Add images only from publishable portions verified in the real UI.

### Lab 1

Follow [Lab 1](../labs/01-setup.md) from environment creation through initialization.

1. In Azure Portal **Resource groups > Create**, **manually create 1 dedicated RG**
   and verify completion.
2. Use **Deploy a custom template > Build your own template in the editor > Load file**
   to load `infra/azuredeploy.json`; after **Save**, select the existing RG.
3. Keep defaults except Subscription / RG. For self-deployment, leave
   **Participant Object Id Override** empty and **Bootstrap Run Id** at `1`,
   then **Review + create > Create**.
   **Enable Bootstrap Policy Exclusion** defaults to **true** for approved workshop
   environments. Set **false** where unapproved or unnecessary, and record enabled /
   disabled runs separately. When enabled, verify that the tag reaches the Deployment
   Script and helper Storage / ACI but not the RG, Foundry, Search, or other resources.
4. Verify the entire deployment, including Search seed, evaluation data / rubric,
   and validation, is **Succeeded** and `workshopContext.setup_status = complete`.
5. Check that `resourceOutputs`, `travelApiBaseUrl`, and `foundryPortalUrl` target
   the participant's own environment.
6. Verify redeployment with the same RG / participant and an intentional
   `bootstrapRunId` update. Check that duplicate data does not grow and failures are explicit.

### Labs 2–6

Extend the same Prompt Agent. In Lab 4, upload GitHub's shared Skill ZIP from the PC
and change only `servers[0].url` in the shared OpenAPI to the participant's `travelApiBaseUrl`.

| Lab | Required execution and checks |
|---|---|
| [Lab 2](../labs/02-prompt-agent.md) | Call Search from the Prompt Agent and check answers and citations. |
| [Lab 3](../labs/03-rag-foundry-iq.md) | Connect Foundry IQ and check retrieval results and answer grounding. |
| [Lab 4](../labs/04-tools-toolbox.md) | Register / publish OpenAPI and Skills; use Trace to verify Tool Search through actual tool execution. |
| [Lab 5](../labs/05-evaluation.md) | Run all 7 evaluation rows; inspect each evaluator's results, reason, Error, and traces for tool-using rows. |
| [Lab 6](../labs/06-optimization.md) | Run optimization with 1 candidate; after completion, compare scores, changes, and rubric details against the baseline. |

In Lab 2, verify the [automatic-toolbox opt-out and Web search removal](../labs/02-prompt-agent.md#3-remove-automatically-added-web-search)
when the current Portal creates an agent-managed toolbox. Direct tool configuration
on the Prompt Agent is separate from Lab 4's published Toolbox and its server-side Tool Search.

Registration of evaluation data or rubrics alone does not complete Labs 5 / 6.
For **Partial** evaluations, record unscorable rows and causes.
Distinguish protection-triggered blocks / answer Fail results from unresolved
execution errors; remaining execution errors mean incomplete.
Do not resubmit running operations; check status and progress.

Lab 6 is complete if comparison is performed, even without an adoptable improvement.
Use **Promote candidate** only when adopting an improvement, then recheck connection /
safety constraints and Lab 3 / 4 behavior.

### Labs 7–8

For [Lab 7](../labs/07-agent-framework-harness.md) and
[Lab 8](../labs/08-hosted-multi-agent.md), verify Notebook execution and Hosted responses separately.

1. Create from **Code > Codespaces** using the
   [Codespaces guide](../docs/participant/environments/codespaces.md);
   check post-create processing and material placement.
2. Have the participant sign in to Azure CLI in the container Terminal.
   Explain that this is separate from GitHub / Portal login.
3. Run `notebooks/00-setup.ipynb` with **Python (Foundry Workshop)**.
   Verify that subscription ID / RG name produce schema `2.0` `.workshop/context.json`.
4. Run Labs 7 / 8 with **Python (Foundry Hosted Agent)**.
   Lab 7 uses plain / Harness; Lab 8 uses the intake / policy / reviewer sequential workflow.
   In Lab 7, proceed from plan to execute in the same session, check Skills, Tool Search,
   and actual tool results, and continue until no unfinished todos remain.
   Plan success alone is not completion.
5. In Lab 8, run the workflow in the Notebook, then deploy with confirmation input
   through the management venv. Once the Hosted Agent is active, invoke it from Portal,
   verify a complete response, and check `policy_agent` retrieval and all 3 Agents'
   execution order in Trace.
6. Verify that deletion after trace comparison / saving requires confirmation input
   and runs through the management venv.
7. Locally, also verify clone → **Dev Containers: Reopen in Container** → the same
   shared procedure. Record this separately from Codespaces.

Lab 8 does not depend on Lab 7 session state, but environment preparation is required.

### Lab 9 and completion criteria

In [Lab 9](../labs/09-observability-cleanup.md), compare Prompt Agent and Hosted Agent
traces, responses, duration, and token usage before saving results and proceeding
to cleanup below.

Record results by Lab and runtime.

| Result | Criteria |
|---|---|
| Complete | Required operations and result checks are finished, with no unresolved execution errors. |
| Incomplete | Executed but acceptance criteria not met. Record failure location, confidence in the cause, and recheck items. |
| Not performed | Not executed because of costs, permissions, personal authentication, etc. Record required approval / prerequisites. |
| Interrupted | Verification stopped at the wait limit or because responses stopped. Record the last successful point and resumption conditions. |

Distinguish an SDK-reported timeout from an interruption where the validator stopped waiting.
Report end-to-end completion only when every Lab, redeployment, and cleanup completes
at the same revision. If cost control or safety requires early cleanup, perform it
first and preserve incomplete / unperformed results. Successful cleanup does not
turn remaining validation items into completed ones.

## Failure response boundaries

- On initialization failure, do not advance to the next Lab; diagnose / repair the same RG.
- For 403 errors, check bootstrap and participant identities / role scopes separately.
- For quota / Policy failures, do not change models, region, or security baseline.
- If authentication requires personal action, hand over to the participant.
  Do not share codes / tokens or save them on someone else's behalf.
- See [administrator troubleshooting](../docs/admin/troubleshooting.md).

## Cleanup checks

For each participant, follow [Lab 9](../labs/09-observability-cleanup.md):

1. Save / export Notebooks and results.
2. Verify deletion of the Hosted Agent and all versions.
3. Stop / delete the Codespace. Locally, stop only the workshop container.
4. In Azure Portal, verify the participant's subscription / dedicated RG name.
5. Execute **Delete resource group** and verify that the RG disappears from the list.

Deleting deployment history does not delete resources.
Other people's and shared environments are out of scope.
