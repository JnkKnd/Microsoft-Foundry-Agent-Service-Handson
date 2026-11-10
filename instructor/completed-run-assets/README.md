# Simulated execution results and reference materials

## Purpose

These are **reference materials** for instructors to screen-share and explain
"this is the expected shape of a result" when live Lab 5 (evaluation), Lab 6
(Optimizer), or Lab 8 (Hosted Agent deployment) cannot finish during the event
because of preview instability, networking, or quotas.

> [!WARNING]
> JSON files here are **not results from actual Microsoft Foundry execution**.
> Each explicitly uses `"SIMULATED"` or `"REFERENCE"` in `asset_status`, and all
> values (IDs, scores, URLs) are fictional. Never tell participants these are real results.
>
> Identifiers (such as `eval-id`) and URLs intentionally use unrealistic forms
> (`SIMULATED-...`, `.invalid` domains, etc.). They contain no real Azure resource,
> subscription, or tenant IDs and no secrets.

## Label meanings

| `asset_status` | Meaning |
|---|---|
| `SIMULATED` | Fictional values manually created by the instructor from documented / scripted output shapes, never executed in any Foundry environment |
| `REFERENCE` | Reference information explaining field meanings / structure, not an execution result; values are illustrative |

Every file has a `disclaimer_ja` field stating that it is not an actual Foundry
execution result. The schema-compatible field name is retained; its narrative is
English on this branch.

## Files

| File | Lab | Schema |
|---|---|---|
| [evaluation-run.simulated.json](evaluation-run.simulated.json) | [Lab 5](../../labs/05-evaluation.md) | [schemas/evaluation-run.schema.json](schemas/evaluation-run.schema.json) |
| [optimizer-run.simulated.json](optimizer-run.simulated.json) | [Lab 6](../../labs/06-optimization.md) | [schemas/optimizer-run.schema.json](schemas/optimizer-run.schema.json) |
| [hosted-agent-deploy.simulated.json](hosted-agent-deploy.simulated.json) | [Lab 8](../../labs/08-hosted-multi-agent.md) | [schemas/hosted-agent-deploy.schema.json](schemas/hosted-agent-deploy.schema.json) |

`tests/contract/test_completed_run_assets_contract.py` checks schema conformance,
that `asset_status` is `SIMULATED` / `REFERENCE`, that `disclaimer_ja` is nonempty,
and that files contain no apparent secrets (`sk-`, `AccountKey=`, etc.) or realistic
GUID-format IDs.

Do not use these as evidence of custom template / Deployment Scripts success,
GitHub asset retrieval, Codespaces / Notebook UI operation, cleanup, or real Portal E2E.
Record live execution blockers and unperformed scope unchanged.

## Instructor usage

1. Attempt live execution of the relevant Lab.
2. Only if it cannot complete within the time available or errors remain unresolved,
   open and screen-share the relevant file here.
3. Explicitly say "this is a simulation" and explain fields following the relevant
   [runbook.md](../runbook.md) section.
4. Ask participants to attempt actual execution when they have time.

## Related links

- [instructor/README.md](../README.md)
- [instructor/runbook.md](../runbook.md)
