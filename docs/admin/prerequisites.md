# Administrator prerequisites

Before an event, check participants' Azure and development environments and distribute
a verified template. Do not guess model versions, image hashes, or material SHAs;
use published, operationally verified values.

> [!IMPORTANT]
> English source and API image artifacts are [published and pinned](../../infra/README.md#english-release-artifacts).
> Full live verification is still required before participant distribution.
> Translation and publication alone are not release readiness. Operative distribution uses
> `JnkKnd/Microsoft-Foundry-Agent-Service-Handson`; do not reuse an upstream release
> as proof of the English release or use a mutable branch as the bootstrap pin.

## 1. Check permissions and quotas

### Azure permissions and services

- Participants must be able to create and delete a dedicated resource group (RG) in Azure Portal.
- They must have **Owner-equivalent permissions**, including role assignment, within
  that RG. Do not grant the execution managed identity subscription-wide permissions.
- Azure AI Search **Basic**, Container Apps, and Deployment Scripts must be available.
  See [infra/README.md](../../infra/README.md) for runtime requirements.
- Application Insights and Log Analytics collect traces.
  Automatic alerts are outside the exercises, so `Microsoft.AlertsManagement`
  registration is unnecessary. See [automatic alerts](troubleshooting.md#application-insights-automatic-alerts)
  for Azure's default alerts.

### Model quotas

Check the following **Japan East / GlobalStandard** quotas in each participant's subscription.

| Model | Required quota |
|---|---:|
| `gpt-5.6-luna` | 40K TPM |
| `gpt-5.5` | 100K TPM |
| `embedding` / `text-embedding-3-small` | 40K TPM |

> [!NOTE]
> Checking quota does not reserve capacity. If insufficient, investigate the cause
> without changing the region or model.

### Development environment and networking

- Check GitHub Codespaces quotas and organizational policies.
- Ensure connectivity to GitHub, GHCR, and package distribution services.
- Local participants must meet the [Dev Container prerequisites](../participant/environments/local-dev-container.md).

<a id="2-template-and-defaults-to-distribute"></a>

## 2. Check the template and distribution contents

Tell participants which subscription to use. Template and shared material locations
are listed in [participant prerequisites](../participant/prerequisites.md#template-and-shared-materials).

After an approved release is published, participants deploying for themselves select
only **Subscription** and their existing **Resource group**.
All other fields use release defaults; participants do not manually enter model versions or hashes.

### Template defaults

Model defaults pin the **latest available Japan East / GlobalStandard versions verified on 2026-09-12**.

| Parameter | Default / administrator override |
|---|---|
| `location` | `japaneast` |
| `primaryModelVersion` | `2026-07-09` |
| `evaluationModelVersion` | `2026-04-24` |
| `embeddingModelVersion` | `1` |
| `travelApiImageRef` | Verified public English API digest in [release artifacts](../../infra/README.md#english-release-artifacts). Upstream `v1.0.4` is historical provenance, not an English release. |
| `sourceRevision` | Published English source SHA in [release artifacts](../../infra/README.md#english-release-artifacts), pinned to 40 lowercase hexadecimal characters. |
| `participantObjectIdOverride` | Empty for self-deployment. For deployment on behalf of someone else or redeployment by another person, the intended participant's Entra object ID. |
| `bootstrapRunId` | `1`. Change only to intentionally rerun initialization. |
| `enableBootstrapPolicyExclusion` | `true` for approved workshop environments. Set to `false` where exclusions are not used. |

See [template parameters](../../infra/README.md#template-parameters) for all defaults,
their concrete release values, and update instructions. English release values must
not be invented. The existing Bicep guards reject empty or mutable source / image inputs.
For each approved release, synchronize the public JnkKnd source SHA, public GHCR
digest, parameter example, and generated ARM. No additional release flag or parameter
is used. Publication does not replace full live verification.

### When bootstrap policy exclusion is approved

If organizational policy disables shared-key authentication or public networking
for temporary Storage, first check the actual policy definition and the operational
conditions under which an exclusion is permitted.
This workshop defaults **Enable Bootstrap Policy Exclusion** to **true** for
approved workshop environments. Set it to **false** in Lab 1 where
`SecurityControl=Ignore` is not approved or an exclusion is unnecessary.

The exclusion tag is limited to the bootstrap Deployment Script and its automatically
created helper Storage / ACI. Do not add it to the whole RG or shared tags or change
models, region, or existing authentication settings.
Real-environment validation through initialization completion is still required.
See [bootstrap exclusion tags](../../infra/README.md#using-bootstrap-exclusion-tags-in-approved-environments)
for scope and rerun considerations.

### Updating distribution contents

1. First publish shared assets, Notebooks, and source compatible with the new bootstrap.
2. Verify that model versions, image hashes, and material SHAs are published and operationally verified.
3. Set verified values as defaults in `infra/main.bicep`.
4. Use the same public SHA for `sourceRevision` and distributed material references.
5. Synchronize `azuredeploy.parameters.example.json` and related documentation.
6. Regenerate and distribute `azuredeploy.json`.

Distribution links may use the approved English branch in JnkKnd's repository.
For reproducible bootstrap execution, pin to the commit SHA only after confirming
publication. Select the latest release at distribution time; never automatically
resolve `latest` or a branch name at runtime.

> [!IMPORTANT]
> Even with defaults configured, recheck model availability and quotas before the event.

## 3. Verify the complete flow before the event

Before directing participants to the materials, verify the following flow to completion:

1. Follow [Lab 1](../../labs/01-setup.md), **manually creating 1 RG before** opening
   the template. Select the existing RG; do not use **Create new**.
2. Verify that the entire deployment, including Deployment Scripts initialization, is **Succeeded**.
3. Check `workshopContext.setup_status = complete` and `resourceOutputs`.
4. Retrieve [Lab 4](../../labs/04-tools-toolbox.md) GitHub assets and verify OpenAPI
   connectivity using `travelApiBaseUrl`.
5. Open locally the same Dev Container as [Codespaces](../participant/environments/codespaces.md).
   Verify Azure CLI sign-in, `00-setup.ipynb`, both kernels, and representative Notebook operations.
6. Follow [Lab 9](../../labs/09-observability-cleanup.md) through
   **save → delete Hosted Agent / versions → stop / delete Codespace → Delete resource group → verify deletion**.

> [!WARNING]
> Deleting deployment history does not delete resources.
> Use synthetic data only and limit deletion to each participant's dedicated RG.

See [infra/README.md](../../infra/README.md) for architecture, permissions, and initialization details.
