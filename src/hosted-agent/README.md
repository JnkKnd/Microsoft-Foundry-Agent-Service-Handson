# Contoso Travel Hosted Agent

[Developer guide](../../docs/development/README.md) / [Lab 8](../../labs/08-hosted-multi-agent.md)

The sequential Microsoft Agent Framework workflow used in Lab 8:

```text
intake_agent -> policy_agent -> reviewer_agent
```

Only `policy_agent` searches the synthetic policies through Foundry IQ.
The deployed workflow does not include Lab 7's Harness, Toolbox, Skills, or Travel Ops API.
It performs no real bookings, submissions, approvals, or expense settlements.

## Running in Notebook

1. After Lab 1 initialization, open [Codespaces](../../docs/participant/environments/codespaces.md)
   or the [local Dev Container](../../docs/participant/environments/local-dev-container.md).
2. Sign in to Azure CLI in the container Terminal and run
   `notebooks/00-setup.ipynb` with **Python (Foundry Workshop)**.
   This creates `.workshop/context.json` from the subscription ID / RG name.
3. Run [`notebooks/08-hosted-agent.ipynb`](../../notebooks/08-hosted-agent.ipynb)
   with **Python (Foundry Hosted Agent)**. Settings are read from `resource_outputs.<key>.value`.

Use the Notebook, source code, and scripts from the same repository.
Management uses the Python 3.12 `foundry-workshop` venv; Hosted uses the Python 3.13
`foundry-hosted-agent` venv. Both are prepared inside the container, outside the checkout.

## Deployment and cleanup

After **DEPLOY** confirmation in the Notebook, a source code ZIP is generated and
submitted to Foundry's remote source code build.
Deployment and deletion invoke the management interpreter from the Hosted kernel
(`WORKSHOP_MANAGEMENT_PYTHON`, defaulting to `~/.venvs/foundry-workshop/bin/python` when unset).

Save your work, check the target in the deletion cell, and enter the displayed **Agent name**.
After deleting the Hosted Agent / versions, stop and delete the Codespace, then
delete your dedicated RG in Azure Portal. See [Lab 9](../../labs/09-observability-cleanup.md).
Deleting deployment history alone does not delete resources.
