# Developer guide

For contributors changing the workshop materials, code, or environment configuration.
See the [workshop README](../../README.md) to participate and the
[instructor guide](../../instructor/README.md) to prepare an event.

## Getting started with development

### 1. Open the shared Dev Container

For local development, meet the [Dev Container prerequisites](../../docs/participant/environments/local-dev-container.md),
clone the repository, open its root in VS Code, and run
**Dev Containers: Reopen in Container**. For Codespaces, select the target branch
and create a Codespace from **Code > Codespaces**.
In either environment, run the following commands in Bash inside the container,
from the repository root.

Wait for `postCreateCommand` to prepare dependencies and both kernels.
Rerun downloads with `make setup` if they fail.
For management / compatibility errors involving existing environments, follow the
[shared development container](../../.devcontainer/README.md#post-create-processing-and-recovery)
instead of deleting them to bypass the error.
Azure sign-in and Lab 1 environment creation are unnecessary at this stage.

### 2. Check management and Hosted environments

```bash
"$WORKSHOP_MANAGEMENT_PYTHON" -c "import sys, azure.ai.projects, travel_api; assert sys.version_info[:2] == (3, 12)"
"$WORKSHOP_HOSTED_PYTHON" -c "import sys, agent_framework, agent_framework_foundry_hosting; assert sys.version_info[:2] == (3, 13)"
"$WORKSHOP_MANAGEMENT_PYTHON" -m jupyter kernelspec list
```

Verify that the first 2 commands exit with code 0 and the final list includes
`foundry-workshop` and `foundry-hosted-agent`. Do not substitute Hosted Python for management operations.

### 3. Run local validation before changing anything

```bash
make lint
make test
make test-hosted
make assets-check
make shell-validate
```

These checks do not create Azure resources or authenticate to Azure.
`make test` uses the management environment; `make test-hosted` uses the Hosted environment.
Record failures and skips caused by missing dependencies as the pre-change baseline;
do not count them as success.

To check ARM / Bicep consistency, prepare the same compiler as CI.
Initial installation contacts its distribution service.

```bash
az bicep install --version v0.46.1
make bicep-validate
```

After preparation, `make validate` runs the checks above together.
Also check the [CI workflow](../../.github/workflows/validate.yml) for validation not
included in local `make validate`, such as container image builds and startup checks.

### 4. Perform required real-environment validation separately

To verify participant operations, connectivity, or deployment behavior, obtain
approval for the target, costs, and personal authentication, then follow the
[instructor runbook](../../instructor/runbook.md) acceptance criteria.
Local tests or CI success do not replace pre-release verification of every Lab.

## Architecture and change policy

| Document | What to check |
|---|---|
| [Workshop architecture](architecture.md) | Service responsibilities, communication paths, authentication, and transfer of materials / connection information |
| [Core workshop scope](feature-support-matrix.md) | Fixed core configuration and features separated into appendices |
| [AI development instructions](../../.github/copilot-instructions.md) | English-primary policy on this branch, sources of truth, and real-environment validation criteria |
| [Development agent guide](../../AGENTS.md) | Implementation responsibilities, environment / service constraints, and safety requirements |

English is the primary source on this branch; no Japanese counterpart is promised.

## Component documentation

| Document | What to check |
|---|---|
| [Infrastructure implementation guide](../../infra/README.md) | Bicep, generated ARM, initialization, permissions, reruns, and deletion |
| [Shared development container](../../.devcontainer/README.md) | Python environments / kernels, post-create processing, and dependencies |
| [Travel Ops API](../../src/travel-api/README.md) | API contract, local execution, tests, and container publication |
| [Hosted Agent](../../src/hosted-agent/README.md) | Workflow, Notebooks, deployment, and deletion |
| [Shared materials](../../assets/README.md) | Skill ZIP / OpenAPI sources of truth, regeneration, and validation |

Keep implementation-adjacent READMEs in place. Consolidate cross-cutting architecture,
design, and development knowledge in `docs/development/` so humans and AI use the same
sources of truth. Put short, always-applicable AI rules in `.github/copilot-instructions.md`.
Participant / administrator procedures belong in `docs/participant/` / `docs/admin/`;
event and instructor validation procedures belong in `instructor/`.

## AI configuration responsibilities

| Configuration | Role |
|---|---|
| [AGENTS.md](../../AGENTS.md) | Directory map, validation entry points, fixed environment / service constraints |
| [Shared Instructions](../../.github/copilot-instructions.md) | Documentation sources of truth, changes, testing, safety, and completion criteria |
| [Python](../../.github/instructions/python.instructions.md) | Management / API / Hosted runtimes, typing, dependency direction, and I/O boundaries |
| [Testing](../../.github/instructions/testing.instructions.md) | Unit / contract / runtime validation and separation from external I/O |
| [CI](../../.github/instructions/ci.instructions.md) | Workflow / Makefile consistency and separation of validation / publication permissions |
| [Infrastructure](../../.github/instructions/infra.instructions.md) | Conditions for changing Bicep, generated ARM, and initialization |
| [Notebooks](../../.github/instructions/notebooks.instructions.md) | Kernels, management operations, saved contents, and Lab consistency |
| [Documentation and images](../../.github/instructions/documentation.instructions.md) | Inputs / success criteria, real screenshots / architecture diagrams, provenance, editing sources, and published images |
| [GitHub Copilot app](../../.github/github-app.yml) | Links to these sources of truth. No automatically executed scripts are configured. |

Path-specific Instructions apply to changes matching each file's `applyTo`.
GitHub Copilot app configuration is not applied until its contents are reviewed
and approved. Open this Git repository as the project, not its parent directory.
Distinguish a configuration file's existence from confirmation that each client / session loaded it.

Reuse existing pytest, Ruff, container validation, and Bicep artifact checks.
The current Makefile / CI has no dedicated static type checker. Do not report type
annotations or Ruff checks as substitutes for static type checking.
To avoid adding independent responsibilities, do not add Custom Agents,
repository-specific Skills, Hooks / MCP, or duplicate design documents.

## Working with AI on changes

Scope AI requests to changes within this Git repository.
Local development history can reveal omissions and reasoning, but is not the source
of truth for current specifications or validation results.

1. **Define the destination.** Confirm purpose, scope / exclusions, and whether completion
   means local or real-environment validation. Read the current branch and uncommitted
   changes to protect shared work and ongoing edits. Do not add parent-directory work
   files or switch branches without a request.
2. **Cross-check evidence.** Read the relevant implementation, tests, and current documentation.
   When consulting history, distinguish user decisions from contemporary Agent reports
   and check for reversals by later decisions. Do not turn unverified product behavior
   or past success reports directly into current requirements / support claims.
3. **Connect the changes.** Use [change targets and checks](#change-targets-and-checks)
   to select documentation, generated artifacts, and tests to update together.
   For example, cross-check Python support against dependencies, CI, and containers;
   verify model support by use case. Reuse adequate existing checks; new checks also
   need tests rejecting intentionally broken inputs.
4. **Separate results.** Start with the smallest relevant checks and expand to required
   full validation. Distinguish runtime, commands, target revision, counts, skips,
   and unperformed scope. Use the [runbook](../../instructor/runbook.md#real-environment-validation-scope)
   for real environments. Do not confuse stopping a wait with an SDK timeout or
   unilaterally reduce the requested scope.
5. **Keep only recurrence prevention.** Put implementation-verified rules in the
   relevant Instructions, design rationale in existing architecture documents, and
   testable invariants in tests. Do not copy conversation logs or generalize a single
   failure into new prohibitions. Keep evidence outside the repository, without
   secrets / personal information, and share only lasting knowledge future developers need.

Past approval for costs, authentication, deployment, deletion, push, or merge does
not authorize those operations now. Follow [submission and completion criteria](#submission-and-completion-criteria).

## Change targets and checks

Include sources of truth and related documentation / generated artifacts in the
same change according to its type. The checks below are for development; before
submission, check `make validate` and CI results.

| Change target | Source of truth | Update / check together | Development validation |
|---|---|---|---|
| Documentation, placement, navigation | Existing Markdown for the intended reader | README, documentation index, relative links, explicit English README. Update runbook when Lab acceptance criteria change. | Management Python: `tests/contract/test_labs_links_contract.py` and `tests/contract/test_optional_labs_links_contract.py` |
| AI instructions | `AGENTS.md`, shared / path-specific Instructions | This guide's list, applicability, and links. Cross-check current implementation, not conversation history. | Management Python: `tests/contract/test_labs_links_contract.py`. Also verify detection / applicability in the client used. |
| Architecture diagrams and screenshots | [Diagram editing sources](architecture.md#editing-architecture-diagrams), real UI | Editing files, published PNGs, README files, related Labs, [attribution](../images/ATTRIBUTION.md). Do not restore historical diagrams as current sources. | Management Python: `tests/contract/test_architecture_diagrams_contract.py` and documentation link checks. Visually inspect published images and editing files separately. |
| Models, permissions, initialization, template | [main.bicep](../../infra/main.bicep), [initialization script](../../scripts/bootstrap_custom_template.py), [wrapper](../../scripts/bootstrap-custom-template.sh) | Parameter example, generated ARM, [infrastructure documentation](../../infra/README.md), [administrator distribution requirements](../../docs/admin/prerequisites.md). First verify public source / image releases. | `make bicep-build` → `make bicep-validate`. Management Python: `tests/contract/test_custom_template_contract.py` and `tests/unit/test_bootstrap*` |
| API, policies, shared materials | [API source guide](../../src/travel-api/README.md), [policy data example](../../data/policies/01-general-policy.md), [Skill source example](../../data/skills/travel-estimation/SKILL.md) | Shared ZIP / OpenAPI from the [generator](../../scripts/build_common_assets.py), related Labs, public image digest | Management Python: `tests/unit/travel_api`, `tests/contract/travel_api`, `tests/unit/data`, `tests/contract/data`. `make assets` → `make assets-check` |
| Notebooks, Harness, Hosted workflow | [Lab 8 Notebook](../../notebooks/08-hosted-agent.ipynb), [Hosted source guide](../../src/hosted-agent/README.md) | Labs 7–8, kernel selection, runbook, and published source revision where needed | `make test-hosted`. Management Python: `tests/contract/test_notebooks_contract.py` |
| Dev Container, dependencies | [Container configuration](../../.devcontainer/devcontainer.json), [environment setup script](../../scripts/setup_dev_environment.py), component dependency definitions | Container README, participant environment guides, CI runtime | Management Python: `tests/unit/test_setup_dev_environment.py` and `tests/contract/test_devcontainer_contract.py`. CI container build and both kernels. |

For example, after documentation changes, run inside the container:

```bash
"$WORKSHOP_MANAGEMENT_PYTHON" -m ruff check .
"$WORKSHOP_MANAGEMENT_PYTHON" -m ruff format --check .
"$WORKSHOP_MANAGEMENT_PYTHON" -m pytest -q tests/contract/test_labs_links_contract.py tests/contract/test_optional_labs_links_contract.py
```

Formatting checks cover the entire repository, including Markdown code examples,
not only changed Python files. Only historical `cloud-shell.md` is excluded from
Ruff automatic formatting in [pyproject.toml](../../pyproject.toml) to preserve its
original text. Retain formatting checks for current documents / code and checks
of the historical document's opening link to current procedures.
Documentation link checks include relative links and Markdown headings in shared /
path-specific Instructions. They also check path-specific YAML frontmatter and
navigation from this guide. They do not prove client detection / application of
instructions or product behavior described in prose.

Bicep is the source of truth for fixed model names, capacities, and connection names.
Maintain human-readable numeric lists in infrastructure documentation and administrator
distribution requirements; link there from AGENTS, architecture overviews, and scope documents.
The [Makefile](../../Makefile) is the source of truth for validation commands;
the [validation workflow](../../.github/workflows/validate.yml) is the source for automation.

See the [instructor runbook](../../instructor/runbook.md) for real-environment acceptance
criteria and all-Lab end-to-end validation. Report static validation success,
real-environment results, and unperformed scope separately.

## Submission and completion criteria

Check the request and existing workflow for branches, submission destination, and PR use.
Commit, push, PR creation, merge, and publication are separate operations; updating
AI configuration alone does not authorize them. Reread shared files immediately
before staging and exclude unrelated changes.

| Stage | Required evidence |
|---|---|
| Local changes | Target diff, validation environment, commands, and counts. Do not count dependency-related skips, unperformed checks, or failures as success. |
| PR / remote CI | Target head SHA and corresponding run, successful required jobs / steps in the [validation workflow](../../.github/workflows/validate.yml), required reviews. Another revision's success or skips after failed installation do not substitute. |
| Merge / distribution | Post-merge SHA, distributed source / image revisions, and publication results. API publication follows the [dedicated workflow](../../.github/workflows/publish-travel-api.yml) and approved scope. |
| Real-environment / end-to-end validation | Results by Lab / runtime, redeployment, and cleanup at one revision. Historical images, registered data, simulated fixtures, and CI success do not prove completion. |

When using PRs, check branch rules, required checks, and review requirements; merge
only when approved. If rules cannot be read, mark them unknown; adding this document
or CI files does not establish that rules are configured.
Distinguish local edits, local commits, and remote updates in reports.
Later stages outside the request are out of scope; requested stages that cannot
be performed are incomplete, with necessary checks identified.

The English source SHA and API image are [published and pinned](../../infra/README.md#english-release-artifacts).
Full live acceptance remains incomplete. Future publication requires separate
approval; do not invent pins or replace the bootstrap commit pin with a mutable branch.
