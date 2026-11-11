# GitHub Codespaces — Prepare for Labs 7–8

This is the standard browser-based route. No local Docker or Python installation is needed.
Complete initialization in [Lab 1](../../../labs/01-setup.md) and have a GitHub account with Codespaces access.

## 1. Create a Codespace

1. Open the [workshop repository](https://github.com/JnkKnd/Microsoft-Foundry-Agent-Service-Handson/tree/English)
   and verify that the branch is `English`.
2. Open **Code > Codespaces** and select the creation button
   (**Create codespace on English** or **＋**).
3. Wait for browser-based VS Code to open, the Dev Container to be created, and `postCreateCommand` to finish.
4. Verify that Explorer contains `notebooks/`, `scripts/`, and `src/`.
   No folder upload or individual code downloads are needed.

To resume the same Codespace, open it from [Your codespaces](https://github.com/codespaces).
For local execution, open the [local Dev Container](local-dev-container.md), then continue below.

## Shared steps

### 2. Sign in to Azure in the container

In VS Code, select **Terminal > New Terminal** and run this **once**, before running notebooks:

```bash
az login --use-device-code
```

Follow the displayed instructions and select your Azure account and the subscription used in Lab 1.
**GitHub and Azure Portal sign-in are separate from Azure CLI sign-in inside the container.**
Run this again only if authentication expires; do not paste codes or tokens into notebooks.

### 3. Retrieve connections in the setup notebook

1. Open [`notebooks/00-setup.ipynb`](../../../notebooks/00-setup.ipynb).
2. At the top right, select **Select Kernel > Jupyter Kernel... > Python (Foundry Workshop)**.
   If only recent choices appear, use **Select Another Kernel...**.
   Choose this notebook's specified kernel, not merely a recommended one.
3. Enter the **subscription ID** and **RG name** used in Lab 1, then run cells from top to bottom.
4. Setup is complete when `.workshop/context.json` exists and shows the intended RG and `setup_status = complete`.

The notebook uses `scripts/configure_workshop.py` to read `workshopContext` from a successful ARM deployment.
Connections are saved in schema `2.0` as `resource_outputs.<key>.value`; no model or endpoint transcription is needed.
If it stops because the deployment is ambiguous, targets a different environment, or initialization is incomplete,
see [troubleshooting](../troubleshooting.md).

### 4. Select the lab kernel

Dev Container post-create prepares separate environments in `~/.venvs/`, outside the checkout.

| Purpose | Kernel display name | Kernel name / Python |
|---|---|---|
| Initial setup and management | **Python (Foundry Workshop)** | `foundry-workshop` / 3.12 |
| Labs 7–8 | **Python (Foundry Hosted Agent)** | `foundry-hosted-agent` / 3.13 |

Use the specified kernel for each notebook without mixing dependencies. Post-create does not authenticate to or deploy to Azure.
VS Code notebooks require no additional Jupyter server or public port.
If output says **Output is truncated**, select its **scrollable element**.
Do not resubmit a cell just to inspect its output.

Continue to [Lab 7](../../../labs/07-agent-framework-harness.md).
When finished, save and delete resources in the order in [Lab 9](../../../labs/09-observability-cleanup.md).
