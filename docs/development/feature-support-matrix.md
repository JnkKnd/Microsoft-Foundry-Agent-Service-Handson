# Core workshop scope

[Developer guide](README.md) / [Workshop architecture](architecture.md)

This list distinguishes the core workshop's fixed configuration from additional
appendix requirements when changing materials. It describes what this workshop
uses, not the availability of the entire service.

## Environment creation and shared materials

| Item | Core configuration |
|---|---|
| Dedicated RG | The participant manually creates 1 RG in Azure Portal before opening the template. |
| Template | Load `infra/azuredeploy.json` and select Subscription and the existing RG. Use verified release defaults for everything else. |
| Initialization | Deployment Scripts prepare and validate Search data, evaluation data, and rubrics. |
| Success criteria | Verify that the entire deployment succeeds and `workshopContext.setup_status = complete`. |
| Shared materials | GitHub `assets/skills/*.zip` and `assets/openapi/travel-ops.openapi.json`. Change only `servers[0].url` to `travelApiBaseUrl`. |
| Portal exercises | Complete Labs 2–6 in Foundry Portal. |

## Notebooks and authentication

| Item | Core configuration |
|---|---|
| Runtime | GitHub Codespaces by default. Local VS Code / Docker uses the same Dev Container. |
| Dependencies | Post-create processing prepares separate virtual environments outside the checkout. It does not sign in to Azure or create resources. |
| Setup kernel | Python (Foundry Workshop), Python 3.12, `foundry-workshop`. |
| Labs 7–8 kernel | Python (Foundry Hosted Agent), Python 3.13, `foundry-hosted-agent`. |
| Authentication | Before the Notebook, the participant signs in to Azure CLI inside the container. This is separate from GitHub / Portal authentication. |
| Connection information | `00-setup.ipynb` retrieves successful ARM outputs using the subscription ID and RG name and saves `.workshop/context.json`. Schema `2.0`; structure `resource_outputs.<key>.value`. |
| Hosted Agent management | Uses remote source code builds. Deployment and deletion run from the management virtual environment with confirmation input. |

## Services and cleanup

| Item | Core configuration |
|---|---|
| Region and models | Japan East / GlobalStandard. See [administrator model quotas](../../docs/admin/prerequisites.md#model-quotas) for fixed models and capacities. |
| Search | Basic. Uses 2 indexes with initial data. |
| Connections | Search uses an AAD resource connection; MCP and Application Insights use Project Managed Identity. See infrastructure documentation for [connection names and settings](../../infra/README.md#connection-schema-exceptions). |
| Identity and networking | System-assigned identities, a bootstrap-only identity, narrowly scoped RBAC, and public endpoints. Foundry / Search local authentication is disabled. |
| Monitoring and API | Log Analytics / Application Insights and Travel Ops API on Container Apps. |
| Cleanup | Save / export → delete all Hosted Agent versions → stop / delete Codespace → delete dedicated RG in Portal → verify deletion. |

The core workshop does not include environment-specific archive distribution,
Cosmos DB, Agent capability host, ACR, or private networking. It does not automatically
switch regions or models or perform actual bookings, approvals, or payments.
See [administrator prerequisites](../admin/prerequisites.md) for distribution requirements
and [costs and cleanup](../participant/costs-and-cleanup.md) for cleanup.
