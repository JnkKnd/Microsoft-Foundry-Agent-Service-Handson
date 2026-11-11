# Environment setup guide

> [!WARNING]
> English source and API image artifacts are published and pinned.
> Full live acceptance of all Labs, redeployment, and cleanup is not yet complete;
> see the [release evidence](../../../infra/README.md#english-release-artifacts).
> Mutable `English` branch links are not release-fixed downloads; existing Azure data is not automatically English.

**Follow the steps in [Lab 1](../../../labs/01-setup.md) in order.**

Manually create one dedicated RG → run the template against that existing RG →
verify successful data loading and validation → open Foundry Portal.
Do not proceed until `workshopContext.setup_status` is `complete`.

Select only **Subscription** and the existing **Resource group**, keeping other defaults.
Leave **Participant Object Id Override** empty when deploying for yourself.

The old Cloud Shell / JupyterLab guide is historical material. Use this guide for current provisioning
and Codespaces or the local Dev Container below for Labs 7–8.

| What to check | Reference |
|---|---|
| Before joining | [Prerequisites](../prerequisites.md) |
| UI steps and initialization checks | [Lab 1](../../../labs/01-setup.md) |
| Shared Skill ZIPs and OpenAPI | [Lab 4](../../../labs/04-tools-toolbox.md) |
| Template defaults | [Administrator guide](../../admin/prerequisites.md) |
| Handling errors | [Troubleshooting](../troubleshooting.md) |
| Notebook preparation (standard) | [Codespaces](codespaces.md) |
| Local participation | [Use the same Dev Container](local-dev-container.md) |
| Cleanup | [Lab 9](../../../labs/09-observability-cleanup.md) |
| Detailed architecture and permissions | [infra/README.md](https://github.com/JnkKnd/Microsoft-Foundry-Agent-Service-Handson/blob/English/infra/README.md) |
