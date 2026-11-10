# Local Dev Container — Labs 7–8

Use the **same `.devcontainer`, notebooks, and kernels** as Codespaces.
Installing Python / Conda directly on the host OS is outside this guide.

## Prerequisites for local execution

- Git
- [Visual Studio Code](https://code.visualstudio.com/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Docker able to run containers (running and approved by your organization)
- The same Azure account and authentication method as Lab 1, with the [required permissions](../prerequisites.md)

## Open the environment

1. Clone the workshop and open it in VS Code.

   ```text
   git clone --branch English https://github.com/JnkKnd/Microsoft-Foundry-Agent-Service-Handson.git
   code Microsoft-Foundry-Agent-Service-Handson
   ```

2. In Command Palette, select **Dev Containers: Reopen in Container**.
3. Once container creation and post-create finish, follow the
   [shared steps: Azure CLI sign-in → setup notebook](codespaces.md#shared-steps).

Python 3.12 / 3.13 venvs are created inside the container, outside the checkout.
You do not need to change the host's `.venv` or Python settings.
Save results and follow [Lab 9](../../../labs/09-observability-cleanup.md) when finished.
Local cleanup must target only this workshop's container.
