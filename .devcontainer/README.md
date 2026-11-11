# Shared development container

[Developer guide](../docs/development/README.md) / [Shared participant procedure](../docs/participant/environments/codespaces.md#shared-steps)

Codespaces and local **Dev Containers: Reopen in Container** share this configuration.
The host Python environment, credentials directory, and Docker socket are not mounted.
It does not start a Jupyter server or automatically forward ports.

## Python environments and kernels

| Runtime | Interpreter passed to Terminal and Notebook | Kernel |
|---|---|---|
| Python 3.12 | `WORKSHOP_MANAGEMENT_PYTHON=/home/vscode/.venvs/foundry-workshop/bin/python` | Python (Foundry Workshop) |
| Python 3.13 | `WORKSHOP_HOSTED_PYTHON=/home/vscode/.venvs/foundry-hosted-agent/bin/python` | Python (Foundry Hosted Agent) |

Variables are defined in `containerEnv`, so both VS Code and `devcontainer exec`
inherit them. They do not depend on a Terminal activation script.

## Post-create processing and recovery

Post-create processing runs `python3.12 scripts/setup_dev_environment.py`.
It checks both `python3.12` and `python3.13`, installs isolated dependencies and
development tools, then runs `pip check`, checks SDK versions, and registers two
user kernels. It does not sign in to Azure or operate on resources.

If dependency downloads fail, rerun the same command. Preparation can continue
for partially created virtual environments managed by this process.
Unmanaged or incompatible environments and kernels cause an error; they are not
deleted or overwritten. To change their locations, explicitly set both variables
to absolute paths outside the checkout. Each must end in its corresponding
`<kernel-name>/bin/python`.

## Updating images and dependencies

Use `3.2.3-3.13-bookworm` from the
[official Python image definition](https://github.com/devcontainers/images/blob/main/src/python/manifest.json)
on Linux amd64 / arm64. The
[Python Feature](https://github.com/devcontainers/features/blob/main/src/python/devcontainer-feature.json)
adds pinned Python 3.12 under `/usr/local/python` and preserves the image's
`/usr/local/bin/python3.13`. Use only options defined by the Feature.

Images, Features, Azure CLI, Graphviz, and development tools are pinned to release
versions. Existing project definitions are the source of truth for Python dependency
ranges; these are not lockfiles pinning transitive dependencies.
Update pins together and verify a full container build on both architectures before
releasing the materials.

## First use

After signing in yourself in the container Terminal, run `notebooks/00-setup.ipynb`
with the management kernel. Switch to the Hosted kernel for Labs 7–8.
