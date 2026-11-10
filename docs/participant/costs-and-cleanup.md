# Costs and cleanup

[Documentation index](../README.md) / [Lab 9 instructions](../../labs/09-observability-cleanup.md)

## Billable usage

- Foundry model inference, evaluation, optimization, and Hosted Agents
- Azure AI Search Basic, Container Apps, Application Insights / Log Analytics
- Deployment Scripts execution
- Tools you use, such as Code Interpreter / Web Search
- Codespaces compute time and storage (depending on account allowances and billing settings)

Closing the browser does not delete Azure resources. Codespace storage remains after stopping.
Administrators should check quotas, budgets, and alerts, and remind participants not to resubmit running operations.
This workshop uses 7 evaluation cases and 1 optimization candidate.

## Cleanup order

1. Save/export notebooks and any results you need.
2. Delete Hosted Agents and all their versions from the notebook.
3. Select **Stop codespace**, then **Delete**. For local execution, stop the workshop container.
4. In Azure Portal, verify your subscription and dedicated RG name.
5. Use **Delete resource group** to delete the RG and remaining workshop resources together.
6. Confirm that the RG no longer appears in **Resource groups**.

**Deleting Deployments history does not delete resources.**
Save your work and clean up Hosted Agents / Codespaces before deleting the RG.
Partial resources from failed deployments may also incur charges.
Other participants' RGs, shared resources, and unrelated local environments are out of scope.

See [Lab 9](../../labs/09-observability-cleanup.md) for UI steps and the
[infrastructure implementation guide](../../infra/README.md) for the initialization runtime.
