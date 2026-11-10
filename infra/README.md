# Azure Portal template implementation

[Developer guide](../docs/development/README.md) / [Workshop architecture](../docs/development/architecture.md)

`main.bicep` is the infrastructure source of truth. `azuredeploy.json` is its
compiled ARM template for Portal, not a separately maintained implementation.
Portal environment creation requires no local CLI. Labs 7–8 run in the shared Dev Container.

> [!IMPORTANT]
> The English source release and API image have not yet been published.
> A separately approved publication and verification are required before distributing
> a ready-to-deploy English release. Operative source references use
> `JnkKnd/Microsoft-Foundry-Agent-Service-Handson`. Never invent a SHA / digest or
> substitute a mutable English branch for the bootstrap commit pin.

## Deployment target and operations

1. In Azure Portal **Resource groups > Create**, create 1 dedicated resource group
   (RG) to delete after the workshop.
2. Open **Deploy a custom template > Build your own template in the editor > Load file**
   and load `azuredeploy.json`.
3. Select **Subscription** and the existing **Resource group**, keeping release
   defaults for all other parameters, including the empty participant ID override.
   Do not use **Create new** here.
4. Start with **Review + create > Create** and wait for the entire deployment,
   including the `ds-fdyws-bootstrap-*` Deployment Script, to succeed.
5. Check `workshopContext.setup_status = complete`.
   Materials use shared GitHub files; there are no per-environment downloads or
   participant Blob containers.

The root `targetScope = 'resourceGroup'` reads `resourceGroup()`.
It creates no RG or subscription-scope deployments / role assignments.
Resource names derive from the RG ID and `japaneast`, not the deployment name,
source commit, execution time, or run ID. Role-assignment GUIDs are also deterministic
for the same inputs. This configuration targets a new dedicated RG; it does not
automatically migrate existing resources or local state.

<a id="template-parameters"></a>

## Template parameters

For a published release, all 9 parameters have release defaults in `main.bicep`,
reflected in `azuredeploy.json`. Self-deploying participants select only
**Subscription** and an existing **Resource group**; they need not investigate
model versions, image digests, source SHAs, or their own object ID.
English source / image defaults are empty strings (`""`) in both Bicep and the
parameter example. This branch is unreleased and not deploy-ready: existing
`fail()` guards explicitly reject these empty values. No additional release flag
or parameter is used.

`azuredeploy.parameters.example.json` reflects defaults without invented or
account-specific values. It is an optional administrator reference, not an
additional file participants load.

| Parameter | Default and override conditions |
|---|---|
| `location` | Only `japaneast` is permitted; default `japaneast`. The RG's metadata location does not override it. |
| `primaryModelVersion` | `2026-07-09` for Japan East / GlobalStandard `gpt-5.6-luna`. |
| `evaluationModelVersion` | `2026-04-24` for Japan East / GlobalStandard `gpt-5.5`. |
| `embeddingModelVersion` | `1` for Japan East / GlobalStandard `text-embedding-3-small`. |
| `travelApiImageRef` | Empty string (`""`) pending separately approved English image publication. Set only a verified public GHCR digest reference (`ghcr.io/jnkknd/...@sha256:...`), never a tag, private registry secret, or substitute image. |
| `sourceRevision` | Empty string (`""`) pending separately approved English source publication. Set only a public, 40-character lowercase hexadecimal commit SHA in `JnkKnd/Microsoft-Foundry-Agent-Service-Handson`, never a branch name or another repository. |
| `participantObjectIdOverride` | Empty by default; root `deployer().objectId` identifies the participant. For administrator / automated deployment or redeployment, specify the intended participant's Entra **User** object ID. |
| `bootstrapRunId` | Default `1`. Keep for normal redeployment; change to intentionally rerun initialization. |
| `enableBootstrapPolicyExclusion` | Default `true` for workshop environments where the organization approves `SecurityControl=Ignore`. Set `false` where exclusions are not used. Add the tag only to the bootstrap Deployment Script. |

Model defaults pin the versions verified for the 3 target Japan East /
GlobalStandard models on 2026-09-12. They do not dynamically resolve `latest`.

Historical upstream release provenance, **not an English release pin or readiness claim**:
Travel API `v1.0.4` was published as
`ghcr.io/matayuuu/travel-ops-api@sha256:173f7e954cd284057bf2a2fe10d53efae83547a060ec2ac23172dd5458816dcf`,
with source [05bd80776c0091ae03d8cfae9312a14b0db00b5f](https://github.com/matayuuu/Microsoft-Foundry-Agent-Service-Handson/commit/05bd80776c0091ae03d8cfae9312a14b0db00b5f).
Do not treat these historical values as published JnkKnd English artifacts.

For a new release, administrators verify model availability / quotas and, with
separate publication approval, publish
compatible source and a public image first. Update defaults in `main.bicep`,
the parameter example, and documentation together, then regenerate ARM as below.
The source SHA must be public but need not contain the template itself.
Do not ask participants to guess values or change regions / models after deployment failure.

Resolve the participant ID once at the root and pass it to every participant role
and the canonical connection information. Do not infer it from a UPN, script ID,
or Microsoft Graph signed-in-user lookup. Preserve the intended participant ID
when another operator redeploys.

Model names, SKUs, and capacities are fixed.

| Deployment name | Model | SKU | Capacity (K TPM) |
|---|---|---|---|
| `gpt-5.6-luna` | `gpt-5.6-luna` | GlobalStandard | 40 |
| `gpt-5.5` | `gpt-5.5` | GlobalStandard | 100 |
| `embedding` | `text-embedding-3-small` | GlobalStandard | 40 |

Evaluation and optimization outputs alias the same `gpt-5.5` deployment.
Quotas, model availability, policies, and image / source publication are administrator
prerequisites, not availability guarantees from the template.
Stop on insufficient capacity; do not switch regions or models.
ARM string parameters do not support regex constraints, so character / length
checks and `fail()` reject unpinned image / source inputs before use.

## Resources and authentication

- Foundry AIServices account and `contoso-travel` project with system-assigned identity.
  Uses Basic Agent Setup and disables local authentication.
  Child resources are created in order: **project → primary → evaluation → embedding → connections**.
- Dedicated Search **Basic** with 1 replica and 1 partition, free semantic search,
  system-assigned identity, public endpoint, and `disableLocalAuth: true`.
  Do not specify incompatible `authOptions`.
- Log Analytics uses `PerGB2018` and 30-day retention.
  Workspace-based Application Insights disables local authentication and preserves
  existing monitoring permissions.
- Travel Ops API on Container Apps uses port 8080, HTTPS ingress,
  0.25 vCPU / 0.5 GiB, and scale 0–1. It anonymously pulls the specified public GHCR digest.
  Policy citations use the same fixed `sourceRevision` as initialization.
- Codespaces and local VS Code use the same Dev Container.
  The template creates no Azure ML workspace, Compute, or permanent workshop Storage / Key Vault.
- Cosmos DB, capability host, ACR, and virtual networks are outside the core workshop.

Monitoring collects telemetry and displays traces; it does not provide workshop alerts.
The template creates no alert rules or notification action groups.
`Microsoft.Insights` and `Microsoft.OperationalInsights` are required, but
`Microsoft.AlertsManagement` is not a prerequisite and `admin-preflight.sh` neither
queries nor registers it. This does not suppress Azure's separately created default
Failure Anomalies alert or disable existing rules.
See [automatic alerts](../docs/admin/troubleshooting.md#application-insights-automatic-alerts).

The 6 participant role assignments and Foundry project / Search identities retain
resource-scoped access. Do not leave role assignments for removed execution /
distribution resources. The bootstrap identity needs no storage data role.

### Connection schema exceptions

Foundry account / project / model deployments and the `CognitiveSearch` / `AAD`
connection use `2026-05-01`. The 2 Project Managed Identity connections retain
the existing `2026-05-15-preview` wire format.

| Connection | Preserved configuration |
|---|---|
| `contoso-travel-search` | `CognitiveSearch`, `AAD`, Search resource ID and location metadata. |
| `contoso-travel-knowledge-lab-mcp` | `RemoteTool`, `ProjectManagedIdentity`, `useWorkspaceManagedIdentity: true`, audience `https://search.azure.com`, knowledge base MCP URL using `2026-08-01-preview`. |
| `contoso-travel-appinsights` | `AppInsights`, `ProjectManagedIdentity`, Application Insights resource ID, internal connection-string routing metadata. |

All connections are project-scoped (`isSharedToAll: false`).
The [official Preview definition](https://learn.microsoft.com/azure/templates/microsoft.cognitiveservices/2026-05-15-preview/accounts/projects/connections)
consulted for this implementation omits the `ProjectManagedIdentity` discriminator
and MCP `audience`. Bicep 0.46.1 reports **BCP036** for `authType` on these 2 connections.
Suppress only those 2 warnings and check entire generated connection objects with
static contract tests. Do not suppress diagnostics globally or cast with `any()`.
Do not substitute `ManagedIdentity`, whose credential contract differs.
Verify Preview operations through the real Portal before release distribution.

Application Insights connection-string metadata and Container Apps Log Analytics
shared-key integration are only for internal resource connections. Do not copy
them into bootstrap environment variables, connection information, or participant outputs.

## Managed identity initialization

Use the `AzureCLI` form of `Microsoft.Resources/deploymentScripts@2023-08-01`,
embedding the actual `scripts/bootstrap-custom-template.sh` with `loadTextContent`.
Download only the fixed repository at the specified SHA, prepare an isolated Python
environment, and run `scripts/bootstrap_custom_template.py`.
Deployment Scripts signs in with managed identity; adapters use `AzureCliCredential`.
Source extraction, virtual environments, and package builds use the container's
`/tmp`, not the Azure Files script directory. Only service-output JSON crosses this
temporary filesystem boundary.

Azure CLI is pinned to **2.87.0**, the Azure Linux release preceding CLI 2.88's
embedded Python 3.14 change. See [Microsoft Artifact Registry](https://mcr.microsoft.com/v2/azure-cli/tags/list)
and [CLI release notes](https://learn.microsoft.com/cli/azure/release-notes-azure-cli).
CI creates an isolated environment in the same CLI image and imports bootstrap
dependencies without Azure authentication. This does not replace checking current
regional Deployment Scripts support or Portal end-to-end validation.

Before release, verify that the service accepts the pinned version and that the
runtime provides Python 3.10–3.13, `venv`, `ensurepip`, TLS, and the ability to install
bootstrap dependencies. The wrapper explicitly fails when prerequisites are missing.
Do not change Azure CLI's own interpreter or assume the service accepts arbitrary
GHCR initialization images.
Recompile `azuredeploy.json` after shell changes.
The template normalizes CRLF to LF before Linux execution; also save source with LF for reproducibility.

The bootstrap-only user-assigned managed identity (UAMI) receives:

| Scope | Role |
|---|---|
| Foundry account | Foundry User for required data operations. |
| Search service | Search Service Contributor and Search Index Data Contributor. |
| Existing dedicated RG | Reader for resource validation and ARM role-assignment reads. |

Do not grant this identity Owner, role-assignment write access, subscription-wide
permissions, storage-account-wide data permissions, or permission to create deployment
resources. The deployer, not the script identity, must be able to create declared
resources, roles, UAMI associations, and helper ACI / Storage.
Participants need permission to read RG deployments so the setup Notebook can
retrieve secret-free connection information after their own Azure CLI sign-in.

The script depends on required resources, all connections, and all role assignments.
The template supplies 2 environment variables:

- `WORKSHOP_SOURCE_REVISION`: verified source commit.
- `WORKSHOP_CONTEXT_JSON`: canonical secret-free connection information serialized as JSON.

Connection information contains `schema_version: "2.0"`,
`provisioning_method: "azure-custom-template"`, `setup_status: "infrastructure-ready"`,
subscription, RG, location, source URL / revision, participant ID, and
24 `resource_outputs.<key>.value` entries.
Initialization prepares 2 Search indexes, Lab 5 evaluation data, Lab 6 Agent Optimizer
data, and shared rubrics, then validates the environment.
Only after all stages succeed does it save `status: complete` and `source_revision`
to `AZ_SCRIPTS_OUTPUT_PATH`. It does not build materials, create participant ZIPs,
or read / write Blob Storage.

ARM exposes these 4 secret-free outputs:

| Output | Purpose |
|---|---|
| `workshopContext` | Completed schema 2.0 connection information, returned only after successful initialization. |
| `resourceOutputs` | Canonical resource-name / endpoint mapping. |
| `travelApiBaseUrl` | Replacement for `servers[0].url` in shared OpenAPI JSON. |
| `foundryPortalUrl` | URL opening the workshop project in Foundry. |

After `az login --use-device-code` inside the Dev Container,
`scripts/configure_workshop.py --subscription <id> --resource-group <name>` reads
deployments and saves `.workshop/context.json`. It validates deployment state,
scope, schema, and endpoints and rejects ambiguous candidates.
It does not overwrite another project's connection information.
Use `--deployment <name>` to explicitly identify a target.
Never publish credentials, SAS links, or participant-specific settings to GitHub.

### Using bootstrap exclusion tags in approved environments

`enableBootstrapPolicyExclusion` defaults to `true` for approved workshop environments.
First verify that organizational policy treats `SecurityControl=Ignore` as an
exclusion condition and approves its use. Set `false` where unapproved or unnecessary.
The tag itself cannot disable arbitrary Azure Policy.

When enabled, add `SecurityControl=Ignore` only to `bootstrap`'s existing tags.
Do not change common tags or tags on the RG, Foundry, Search, bootstrap identity,
or other resources. Deployment Scripts also propagates tags to automatically
created helper Storage and ACI. Add no permanent Storage, policy assignments,
or Policy Exemption resources.

Create a new deployment with the approved settings; check helper Storage tags,
required authentication / network settings, overall `Succeeded`, and
`workshopContext.setup_status = complete`.
This option does not restore existing Storage settings already changed by policy.
It neither ignores initialization failure nor relaxes success criteria or cleanup.
Record enabled / disabled results separately in the target tenant.

- Reference: [Deployment Scripts tags and helper resources](https://learn.microsoft.com/azure/azure-resource-manager/templates/deployment-script-template)

### Retries, helper resources, and cleanup

`forceUpdateTag = guid(sourceRevision, bootstrapRunId)` is deterministic for the
same inputs. Changing commit or run ID reruns initialization without renaming
workshop resources. Script changes or redeployment after retention expiry may also
rerun it, so initialization must remain idempotent.

The service automatically creates independent temporary ACI and helper Storage
for Azure Files. `storageAccountSettings` is deliberately omitted.
Provider registration, policy, and quota must allow Microsoft.Resources Deployment
Scripts, Microsoft.ManagedIdentity, Microsoft.ContainerInstance, Microsoft.Storage,
and helper Azure Files / shared-key access.

`timeout: PT1H`, `cleanupPreference: OnSuccess`, and `retentionInterval: P1D` limit
execution and failed-run retention. Helper resources are cleaned up on success;
diagnostics remain only for the configured retention on failure.
Retain the UAMI and narrowly scoped permissions for reruns until dedicated RG deletion.
Retained resources incur charges, so verify their actual deletion.

Deployment failure is not a transactional rollback; created resources and seeded
data may remain. Inspect deployment / script errors, correct inputs or prerequisites,
and redeploy with the same RG / participant ID.
Change `bootstrapRunId` to force a rerun. Do not treat partial initialization as complete.

At the end, save results, delete Hosted Agent versions, stop / delete the Codespace,
then delete the dedicated RG in Azure Portal and verify completion.
Deleting deployment history alone does not delete resources.
Do not delete unrelated resources, existing local state, or caches.

## Developer regeneration and validation

Use the shared Dev Container and run from the repository root:

```bash
az bicep build --file infra/main.bicep --outfile infra/azuredeploy.json
python -m pytest tests/contract/test_custom_template_contract.py -q
```

Bicep CLI is pinned to **v0.46.1 (545b338e2c)**, recorded as **0.46.1.21595** in
generated ARM metadata. No compiler upgrade is required for this template.
Use the same compiler / source for byte-for-byte reproduction.
Compiler upgrades may change generated metadata; review it with the artifacts.

Static tests check ARM structure, dependency graph, fixed-input expressions,
RBAC scopes, connection payloads, embedded shell, outputs, and connection information.
They do not guarantee Azure runtime availability or real Portal end-to-end success.

## Official references

- [Deployer identity](https://learn.microsoft.com/azure/azure-resource-manager/bicep/bicep-functions-deployment#deployer)
- [Deployment Scripts API](https://learn.microsoft.com/azure/templates/microsoft.resources/2023-08-01/deploymentscripts)
- [Runtime, identity, and cleanup](https://learn.microsoft.com/azure/azure-resource-manager/bicep/deployment-script-develop)
- [Foundry account](https://learn.microsoft.com/azure/templates/microsoft.cognitiveservices/2026-05-01/accounts)
- [Search Basic and authentication](https://learn.microsoft.com/azure/templates/microsoft.search/2025-05-01/searchservices)
