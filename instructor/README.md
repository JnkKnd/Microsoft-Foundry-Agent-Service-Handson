# Instructor guide

The core sequence is **manually create a dedicated RG → custom template /
initialization → Foundry Portal → GitHub Codespaces**.
Local participants use the same Dev Container.

Before the event, review the [runbook](runbook.md),
[reference results](completed-run-assets/README.md),
[administrator prerequisites](../docs/admin/prerequisites.md), and
[costs and cleanup](../docs/participant/costs-and-cleanup.md).
For material changes, see the [developer guide](../docs/development/README.md);
for participant navigation, see the [documentation index](../docs/README.md).

## Schedule planning

The [README schedule](../README.md#schedule-and-preparation) is the source of truth
for time allocations. Treat it as a facilitation estimate excluding Lab 1, not a
measured event duration including Lab 1.
Before the event, follow the runbook on the intended revision / environment and
record initialization, container preparation, evaluation / optimization / deployment
waits, participant operations, and cleanup durations separately.
Keep these records outside the repository, like other execution evidence.

| Event format | Information to provide |
|---|---|
| Complete Lab 1 beforehand | Deadline, success checks, costs / retention until the start time, cleanup owner. At the event, confirm readiness before Lab 2. |
| Complete Lab 1 during the event | Add a preparation slot including initialization waits and measured contingency time to the exercise schedule. Proceed to Lab 2 only after Lab 1 succeeds. |

State the chosen format in the event announcement. When revising the schedule,
update the English-primary README and any explicitly maintained README variant together.
Do not hide omissions or pending execution and present them as completed all-Lab
end-to-end validation. This branch does not promise a Japanese counterpart.

### 60-minute English presentation

Use this variant for an instructor-led English presentation, not a shortened
participant workshop. Announce it as explanation and walkthrough segments;
participants are not expected to create resources or complete the Labs during
the hour. The full workshop schedule above remains unchanged. Optional Labs
are omitted from this presentation.

| Minutes | Segment | Instructor action and reference |
|---|---|---|
| 0–5 | Scope and synthetic-data safety | State the learning goals and distinguish simulation from real bookings, submissions, approvals, and payments. Explain that credentials and personal information must not be shared. |
| 5–12 | Architecture and setup overview | Use the [architecture diagrams](../docs/development/architecture.md#architecture-diagrams) to explain responsibilities and the [Lab 1](../labs/01-setup.md) sequence: manually create 1 dedicated RG, deploy the pinned template, and verify completed initialization. Explain cleanup ownership rather than starting deployment during this slot. |
| 12–27 | Prompt Agent and Foundry IQ | Walk through [Lab 2](../labs/02-prompt-agent.md) direct Search and citations, then [Lab 3](../labs/03-rag-foundry-iq.md) Knowledge base retrieval. Emphasize replacing, not simultaneously enabling, the direct-search path. |
| 27–37 | Toolbox, Skills, and API simulation | Follow [Lab 4](../labs/04-tools-toolbox.md): shared Skill ZIPs, the participant-specific OpenAPI server URL, Tool Search, and actual tool-call traces. Explain that preapproval responses are simulations, not real approval. |
| 37–45 | Evaluation and optimization | Use [Lab 5](../labs/05-evaluation.md) to explain the 7 evaluation rows, evaluator results, and execution errors; use [Lab 6](../labs/06-optimization.md) to explain the 1-candidate baseline comparison and optional promotion. Do not start jobs merely to fit this slot or imply data registration proves job completion. |
| 45–52 | Harness and Hosted Agent | Contrast [Lab 7](../labs/07-agent-framework-harness.md) plan → execute in the same session with [Lab 8](../labs/08-hosted-multi-agent.md) intake → policy → reviewer. Explain local versus Hosted execution, kernel separation, and post-deployment response / trace checks. |
| 52–55 | Summary | Recap grounding, controlled tool use, evaluation, and execution boundaries. Explain [Lab 9](../labs/09-observability-cleanup.md) trace comparison and save → Hosted versions → Codespace → dedicated RG cleanup. |
| 55–60 | Q&A | Answer questions, identify relevant Labs for later practice, and explicitly distinguish demonstrated results from unperformed operations. |

Prepare the linked material and choose explanation-only versus live demonstration
before the session. Live demos may use only a separately released, immutably
pinned English source / API image and an environment that has passed the full
[same-revision acceptance](runbook.md#real-environment-validation-scope).
Obtain any required target, cost, and personal-authentication approvals before
live operations. This agenda records no executed demo or validation result;
English artifacts are [published and pinned](../infra/README.md#english-release-artifacts),
but full live acceptance is incomplete.

If a live demonstration is unavailable or fails, continue with an explanation
of the documented procedure. Label historical screenshots as illustrative and
[simulated reference results](completed-run-assets/README.md) as simulated;
neither proves successful execution. Do not silently substitute off-procedure
repairs or present an unfinished operation as complete.

This shorter lecture does not reduce release acceptance: every core Lab (1–9),
redeployment, and cleanup must still complete at the same revision under the
runbook. Omitting optional Labs from the presentation does not waive any applicable
release checks.

## Checklist

- Participant subscription, dedicated RG name, and create / delete / role assignment permissions
- Fixed-model / Search Basic quotas and a template with verified release defaults
- Open the template only after RG creation completes; select only Subscription / existing RG
- Successful Search / evaluation data preparation and validation; `workshopContext.setup_status = complete`
- Lab 4 GitHub Skill ZIP, shared OpenAPI, and the participant's `travelApiBaseUrl`
- Codespaces / Dev Container preparation, personal Azure CLI sign-in, `00-setup.ipynb`, and both kernels
- Save → Hosted Agent versions → stop / delete Codespace → verify dedicated RG deletion

Explain core safety precautions at the start. Distinguish real UI operation results
from reference materials; never use simulated assets as proof of success.
The English source / API image are published and pinned; full live verification
must precede participant distribution. See the [release evidence](../infra/README.md#english-release-artifacts).
