# Before you join

> [!WARNING]
> The English release is not yet deployment-ready. Source and API image artifacts have not
> been published. The administrator must pin a published English source SHA and GHCR image
> digest before distributing the template. `English` branch links are mutable references,
> not release pins; existing Azure environments are not automatically translated.

## Accounts and PC

- The Azure account and subscription designated by the administrator.
- Permission to create and delete a dedicated RG, and **Owner-equivalent permissions**
  to assign roles within that RG.
- Only if using Codespaces for Labs 7–8: a GitHub account with access and available
  usage allowance for [GitHub Codespaces](https://github.com/codespaces).

The standard Codespaces route requires no CLI, Docker, or Python installation on your PC.
Ask the administrator to check Azure quotas and organizational policies, and,
if applicable, Codespaces allowances and organizational policies.

## Template and shared materials

Check the files and references you will use.

- **Lab 1**: Save the [preconfigured `azuredeploy.json`](https://github.com/JnkKnd/Microsoft-Foundry-Agent-Service-Handson/blob/English/infra/azuredeploy.json)
  to your PC. You do not need to look up and enter model versions or hashes yourself.
  See the [administrator guide](../admin/prerequisites.md) for default values.
- **Lab 4**: Obtain Skill ZIPs and OpenAPI from the [shared materials](../../assets/README.md).
  Lab 4 explains how to download and use them.

## Get started

Follow [Lab 1](../../labs/01-setup.md): **manually create exactly one RG** in Azure Portal,
then run the template against that existing RG. Keep all defaults except
**Subscription** and **Resource group**. Prepare notebooks in Lab 7 using the
[Codespaces guide](environments/codespaces.md).

| Interface | Purpose |
|---|---|
| [Azure Portal](https://portal.azure.com) | Provisioning, initialization checks, and RG deletion |
| [Microsoft Foundry Portal](https://ai.azure.com) | Labs 2–6 |
| GitHub / Codespaces | Shared materials and notebooks for Labs 7–8 |

For local execution, check the [Dev Container prerequisites](environments/local-dev-container.md).
See the [README](../../README.md) for safety guidance and [Lab 9](../../labs/09-observability-cleanup.md)
for cleanup.
