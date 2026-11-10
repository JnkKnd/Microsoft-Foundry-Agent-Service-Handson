# Lab 1 — Create the environment and verify initialization

Use Azure Portal. This lab does not use a CLI or notebooks.

> [!WARNING]
> **Live acceptance is not yet complete.** Published English source and API image defaults
> are pinned; see the [release evidence](../infra/README.md#english-release-artifacts).
> Administrators must verify all Labs, redeployment, and cleanup before participant distribution.
> Branch download links are mutable, not release pins.
> Existing Azure environments are not automatically English.

## Overall flow

Participants create a dedicated RG, load and run the custom template, and check completion in Azure Portal.
Azure then provisions resources, prepares data, validates the environment, and outputs connections.
Verify success of the entire process, including data preparation and validation, before continuing.

The existing [deployment flow diagram](../docs/images/azure-architecture-02.png)
has English labels and illustrates the procedure; it is not current-revision success evidence.

## Before you begin

- Check the [prerequisites](../docs/participant/prerequisites.md).
- Obtain the designated subscription from the administrator. Create your own dedicated RG in step 1.
  See the [administrator guide](../docs/admin/prerequisites.md#2-template-and-defaults-to-distribute) for template defaults.
- Save the administrator-designated
  [azuredeploy.json](https://github.com/JnkKnd/Microsoft-Foundry-Agent-Service-Handson/blob/English/infra/azuredeploy.json)
  to your PC. Save the JSON itself, not the web page.

For a distributed release, model versions, image hashes, and the workshop source SHA must be preconfigured.
Use that release's defaults; do not guess values or bypass the unreleased branch's fail guards.

## 1. Manually create one dedicated RG

1. In [Azure Portal](https://portal.azure.com), verify your account and subscription.
2. Open **Resource groups > Create**.
3. Set **Subscription** to the designated subscription, **Resource group** to your own dedicated name,
   and **Region** to **Japan East**.
4. Select **Review + create > Create**.
5. Once creation finishes, check the RG name in **Resource groups**.

**Wait for RG creation to finish before proceeding.**

## 2. Run the template against the existing RG

1. In Azure Portal, search for and open **Deploy a custom template**.
2. Select **Build your own template in the editor > Load file**.
3. Load the saved `azuredeploy.json` and select **Save**.
4. For **Subscription** and **Resource group**, select the existing RG from step 1.
   Do not use **Create new**.
5. Keep other fields **at their defaults**. You are deploying for yourself, so leave
   **Participant Object Id Override** empty and **Bootstrap Run Id** at `1`.
   **Enable Bootstrap Policy Exclusion** defaults to **true**.
   This is for workshop environments where the organization's administrator has approved
   the initialization exclusion tag. Set it to **false** where approval is absent or exclusion is unnecessary.
   Check the [administrator applicability conditions](../docs/admin/prerequisites.md#when-bootstrap-policy-exclusion-is-approved).
6. Select **Review + create > Create**.

## 3. Wait for successful initialization

1. In the RG's **Deployments**, wait until the **entire deployment, including Deployment Scripts initialization**,
   shows **Succeeded**.
2. Open `workshopContext` in **Outputs** and verify `setup_status = complete`.
   Initialization includes Search data loading, evaluation dataset/rubric preparation, and validation.
   Resource creation alone does not mean setup is complete.

The existing [deployment completion screenshot](../docs/images/lab01-template-succeeded.png)
is a historical UI illustration, not evidence that this revision has been verified.
Use the status and output checks above rather than the screenshot to determine success.

If it fails, do not continue; see [troubleshooting](../docs/participant/troubleshooting.md).
Do not resubmit running operations or switch regions or models.

## 4. Open Foundry Portal

Check these in the same **Outputs**:

| Output | Purpose |
|---|---|
| `foundryPortalUrl` | Open it and select the Foundry resource in `resourceOutputs` and project `contoso-travel` |
| `resourceOutputs` | Names used in Labs 2–6; use each item's `value` |
| `travelApiBaseUrl` | Your API URL to insert into the shared OpenAPI in Lab 4 |

Lab 1 is complete. There is no environment-specific bundle to download.
Obtain shared files from GitHub in [Lab 4](04-tools-toolbox.md) and prepare Codespaces in
[Lab 7](07-agent-framework-harness.md).

## Next lab

[Lab 2 — Prompt Agent](02-prompt-agent.md)
