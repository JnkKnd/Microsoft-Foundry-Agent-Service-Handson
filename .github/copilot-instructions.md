# Copilot development instructions

Keep repository-specific AI development rules under `.github/`.
The [developer guide](../docs/development/README.md) and its references are the
source of truth for architecture, design, and development procedures. Read the
relevant guide before changing code, and update it in the same change when a
specification changes. Link to specifications rather than duplicating them here.

## Documentation language and source of truth

- On the **English branch**, English is the source language for README files,
  `AGENTS.md`, `.github/`, `docs/`, `instructor/`, `labs/`, sample data, and
  user-visible runtime text. Preserve official product names, UI labels,
  identifiers, filenames, code, and commands.
- `README.md` is the primary entry point. Keep `README.en.md` consistent as
  an explicit English entry point; do not imply that this branch contains a
  separately maintained Japanese edition.
- Translation does not change policy amounts, JPY, dates, IDs, approval rules,
  service configuration, or safety boundaries.
- Current procedures are in the [README](../README.md) and
  [setup guide](../docs/participant/environments/custom-template.md).
  See [workshop architecture](../docs/development/architecture.md) for structure.
  Update an existing source of truth before creating another document with the same role.
- Label retained old procedures as historical and link to current instructions
  at the beginning. Historical commands and links are not current operating instructions.

## Documentation placement

- Put participant materials in `docs/participant/`, administrator materials in
  `docs/admin/`, exercises in `labs/`, and instructor materials in `instructor/`.
- Keep shared architecture, design, and development knowledge for people and AI
  in `docs/development/`. Keep implementation-adjacent README files in place and
  link to them from the developer guide.
- When creating or moving documents, update audience indexes and relative links
  together. Do not duplicate the source of truth.

## Using development history

- Follow [AI-assisted changes](../docs/development/README.md#working-with-ai-on-changes):
  establish the requested outcome and the scope of changes and verification first.
- History informs decisions; it is neither the current specification nor
  authorization for this operation. Distinguish user decisions, past Agent reports,
  and unverified assumptions, and compare them with current code, documentation, and tests.
- Integrate only recurrence-prevention rules into existing instructions.
  Connect machine-checkable contracts to existing checks. Do not copy entire
  conversations, live environment identifiers, personal absolute paths, or temporary progress.

## Code changes and completion

- Read the implementation, tests, and adjacent README first. Preserve existing
  APIs, dependency direction, and exception handling. Do not move source code
  just to initialize tooling or update rules, or mix in unrelated formatting or redesign.
- Check the shared worktree at the start and before editing or staging. Preserve
  other work. Do not automatically delete or restore historical material; confirm
  the exact file and revision before restoration.
- Use [AI configuration responsibilities](../docs/development/README.md#ai-configuration-responsibilities)
  for path-specific rules. Do not make personal Agents, Skills, or parent-folder
  dependencies a prerequisite for development.
- Maintain the existing `pyproject.toml` and `requirements.txt` dependency manifests.
  Do not install dependencies into global Python or an unrelated virtual environment.
- Update unit and contract tests for changed behavior. Cover normal, failure, and
  boundary cases. New checks must also reject deliberately broken input.
- Follow [change scope and verification](../docs/development/README.md#change-targets-and-checks)
  for validation and submission checks. Report not-run checks, skips, pre-existing
  failures, and failures caused by the change separately.
- Never commit credentials, live connection information, or Notebook authentication
  output. Publication, deployment, permission changes, and deletion require separate
  approval of their targets and effects; do not perform them as part of configuration edits.
- English releases use this fork's published source and API image. Never assign
  an upstream SHA or digest to a different owner or claim unpublished artifacts
  are available. Bootstrap and citations use immutable commits, not branch names.

## Live verification criteria

Verify the full participant journey in the actual Azure Portal, Foundry Portal,
and Codespaces / VS Code Notebook UI. Confirm the target, costs, and personal
authentication before starting. Do not replace documented success with unpublished
API / REST operations or repairs outside the participant procedure.

The [instructor runbook](../instructor/runbook.md) defines acceptance criteria:
verify all Labs (1-9), redeployment, and cleanup at the same revision. After a fix,
restart the complete run at the corrected revision. Dataset registration is not
evaluation or optimization job execution. Verify Harness plan and execute, and
the Hosted Agent's response after deployment.

Distinguish incomplete, not run, and interrupted results from success. Obtain
prior approval before reducing verification scope. CI and simulated fixtures
do not prove live UI success. Update the runbook when Labs change, and keep
execution evidence without account-specific values or secrets outside the repository.
