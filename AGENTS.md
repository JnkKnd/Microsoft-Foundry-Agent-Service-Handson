# Development agent guide

## Project overview

This is the English edition of the Microsoft Foundry Agent Service workshop.
Environment creation uses Azure Portal custom templates. Codespaces and local
development share the same Dev Container. Preserve official English UI labels.

## AI development guidance

Follow the [Copilot development instructions](.github/copilot-instructions.md)
for documentation language and live verification criteria.
The [developer guide](docs/development/README.md) links to architecture, design,
and implementation documentation. Start with
[AI-assisted changes](docs/development/README.md#working-with-ai-on-changes) to reconcile
history with current specifications and agree on scope, verification, and delivery.

## Directories and validation entry points

The work root is the Git repository containing this `AGENTS.md` and `Makefile`.
Do not treat working files or dependencies in parent directories as project components.

| Location | Responsibility |
|---|---|
| `src/travel-api/` | Python 3.12 FastAPI; HTTP adapter → application → domain |
| `src/hosted-agent/` | Python 3.13 Hosted Agent startup and workflow |
| `scripts/`, `scripts/lib/` | Administration, initialization, shared connection and runtime helpers |
| `notebooks/` | Participant entry points; separate SDK execution from management operations |
| `infra/` | Bicep source of truth, generated ARM, parameter example |
| `data/`, `assets/` | Synthetic materials, schemas, Skill sources, generated ZIP / OpenAPI |
| `tests/unit/`, `tests/contract/`, `tests/runtime/` | Unit and contract checks; bootstrap image verification |
| `.devcontainer/`, `.github/workflows/` | Shared development environment, validation CI, API image publication |
| `docs/`, `labs/`, `instructor/` | Audience-specific materials, exercises, instructor acceptance criteria |

Use the [developer quickstart](docs/development/README.md#getting-started-with-development)
for setup and validation environments. `make` commands run in Bash inside the
Dev Container. Windows host Python and a repository-local `.venv` are not the
management and Hosted environments. See
[AI configuration responsibilities](docs/development/README.md#ai-configuration-responsibilities)
for path-specific rules.

## Responsibility boundaries

- In Azure Portal, participants manually create exactly one dedicated resource
  group (RG) before running the template, then select that existing RG.
- Bicep / ARM manages the Foundry account and project, pinned models, Search,
  monitoring, Container Apps API, and narrowly scoped RBAC and connections.
  It does not create an RG, Azure ML workspace, or permanent workshop Storage / Key Vault.
- Deployment Scripts uses a dedicated user-assigned identity to initialize and
  verify Search data and evaluation materials, then returns non-secret ARM outputs.
- GitHub stores shared Skill ZIPs, the OpenAPI template, Notebooks, and Python source.
- Foundry Portal is used for Prompt Agents, Foundry IQ, Toolbox, evaluation,
  optimization, and traces.
- Codespaces / local Dev Container runs the Labs 7-8 Notebooks and Hosted operations.
- The canonical connection key is `resource_outputs` in `.workshop/context.json`.

## Environment creation requirements

- Bicep is authoritative; commit the generated Portal ARM JSON as well.
- Released templates have verified defaults for every parameter, so participants
  select only subscription and existing RG. Leave the participant override empty
  for personal deployments. Unpublished English source/image pins remain empty
  and fail explicitly until an approved release supplies verified defaults.
- Do not add Terraform / Cloud Shell environment creation, cleanup, or substitutes.
- Use administrator-verified model versions and immutable source/image references.
  Update Bicep defaults, the parameter example, and documentation together for a release.
  Stop on capacity or policy errors; do not switch regions or models automatically.
- Pass the intended participant object ID to RBAC and verification. The bootstrap
  managed identity is not the participant. Do not look up the signed-in user
  through Microsoft Graph during bootstrap.
- Initialization must be idempotent, retries bounded, and failures visible in deployment results.
- Do not add environment-specific participant ZIPs or Blob handoffs.
  Shared Skill ZIPs and Hosted source archives are required by their respective APIs.
- Publish complete, non-secret connection information only after initialization succeeds.
- Clean up temporary Deployment Scripts ACI / Storage on success and bound retention
  on failure. Retain the bootstrap identity and scoped permissions until the workshop is deleted.

## Development environment requirements

- Use the same Dev Container in Codespaces and local VS Code / Docker.
- Separate Python 3.12 management from Python 3.13 Hosted SDK environments.
- Store container virtual environments outside the repository; do not overwrite the host `.venv`.
- Post-create prepares dependencies and kernels only; no Azure authentication or provisioning.
- After personal Azure CLI sign-in, `notebooks/00-setup.ipynb` reads the successful
  deployment using subscription ID and RG name and saves `.workshop/context.json`.
- Labs 7-8 use **Python (Foundry Hosted Agent)**.
- Invoke management operations with the management interpreter explicitly, not the Hosted SDK.
- Replace only the shared OpenAPI server URL with the participant's API endpoint.

## Fixed service requirements

- The Foundry project is `contoso-travel`, using Basic Agent Setup.
- [Bicep](infra/main.bicep) defines model names, capacities, and connections.
  See [administrator model capacity](docs/admin/prerequisites.md#model-quotas)
  for numbers and [connection schema exceptions](infra/README.md#connection-schema-exceptions)
  for connection names and authentication. Do not guess replacements; synchronize release artifacts.
- Use public endpoints, system-assigned identities, and scoped RBAC. Disable local
  authentication for Foundry / Search.
- The dedicated user-assigned identity is used only for deployment-time initialization.
- Cosmos DB, Agent capability hosts, ACR, and private networking are outside the core workshop.

## Safety and cleanup

Use synthetic data only. Never publish credentials, tokens, device codes, or state files.
Save Notebooks, delete Hosted Agent versions, and stop/delete the verification
Codespace before deleting the dedicated RG in Azure Portal and verifying completion.
Deleting deployment history does not delete resources. Unrelated local containers,
data, and environments are not cleanup targets.

When retiring old implementation files, preserve existing user state, caches,
and unrelated Azure resources. Keep credential/state exclusions after old tools
are removed. Do not add quota adjustment procedures to participant documentation.
