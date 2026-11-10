# Appendix — Deploy a Hosted Agent with azd (Azure Developer CLI)

## Scope of this document

The main workshop uses only **source-code remote build** through `scripts/deploy_hosted_agent.py`
and never uses `azd`. This appendix describes an alternative route using the azd Foundry extensions,
which **requires separate authentication and an approved test environment**.
It is not needed for [Lab 8](../08-hosted-multi-agent.md), manual RG creation / custom template in Lab 1,
or GitHub shared materials / Codespaces. Do not modify the main source directory or fixed infrastructure.

> [!IMPORTANT]
> **`azd auth login` is separate from `az login`.** Main-workshop Hosted execution
> uses the participant's Azure CLI authentication in the Dev Container.
> To try this appendix, run **`azd auth login` separately**, in addition to `az login`.
> This does not change the main design; it is an extra step only for the separate azd tool.

## 1. Prerequisites

| Item | Requirement |
|---|---|
| Azure Developer CLI (azd) | **1.25.2 or later** |
| Runtime | Python 3.10 or later, or .NET 8 or later (required by the Foundry extensions) |
| Azure role (RG scope) | **Contributor** for provisioning; also **Foundry Owner** when creating a new Foundry project |
| Authentication | `azd auth login` (required separately from `az login`) |

## 2. Install Foundry extensions

```bash
azd version   # Verify 1.25.2 or later
azd auth login

azd extension install microsoft.foundry
```

`microsoft.foundry` is a metapackage installing these extensions together:

| Extension | Purpose |
|---|---|
| `azure.ai.agents` | Agent creation/deployment |
| `azure.ai.connections` | Manage Foundry connections (ACR, Fabric, Work IQ, etc.) |
| `azure.ai.inspector` | Local debugging and trace inspection |
| `azure.ai.projects` | Manage Foundry projects |
| `azure.ai.routines` | Manage Routines (preview); see [A2A, Routines, and Publish](a2a-routines-publish.md) |
| `azure.ai.skills` | Manage Skills; see [Advanced Hosted Agent](advanced-hosted-agent.md) |

## 3. Initialize the project

Run `azd ai agent init` in a separately prepared, independent agent project directory,
not the main workshop's `src/hosted-agent/`.

The command interactively asks for:

- A different approved Foundry project. Do not provision extra infrastructure into
  the project in the main `.workshop/context.json`.
- An ACR destination for container images. If unspecified, `azd provision` creates
  a new project-specific ACR; see [Advanced Hosted Agent](advanced-hosted-agent.md).

`azd ai agent init` generates `azure.yaml` and `next-steps.md` (standard azd project metadata).
These are separate from `.workshop/context.json`; main-workshop scripts do not read/write them.

## 4. Deploy

```bash
azd ai agent deploy
```

This builds the container, pushes to ACR, registers the version with Foundry,
creates an agent Microsoft Entra identity, and assigns required RBAC.
For separate stages, use `azd ai agent build` → `azd ai agent push` → `azd ai agent deploy`;
see [Advanced Hosted Agent](advanced-hosted-agent.md).

## 5. Differences from the main workshop

| Aspect | Main core (`scripts/deploy_hosted_agent.py`) | This appendix (`azd ai agent`) |
|---|---|---|
| Authentication | Participant Azure CLI authentication in the Dev Container | `az login` + `azd auth login` |
| Deployment | source ZIP + `REMOTE_BUILD` (Foundry server-side build) | Local container build → push to ACR |
| Extra infrastructure | None beyond main custom template resources | ACR in a separate environment (existing or created by `azd provision`) |
| Audience | All participants (required main lab) | Optional route for azd-experienced participants |
| Idempotency/cleanup | Covered by `scripts/delete_hosted_agent.py` and Lab 9 | azd-specific state and ACR images need separate cleanup; see [Advanced Hosted Agent](advanced-hosted-agent.md#7-cleanup-beyond-the-main-dedicated-resource-group) |

## 6. If you do not use this appendix

Lab 8 completes without any `azd` use. This appendix is entirely optional;
skipping it does not affect the rest of the workshop.

## Official references

- [Install the Azure Developer CLI Foundry extensions](https://learn.microsoft.com/azure/foundry/agents/how-to/install-cli-foundry-extensions)
- [Deploy a hosted agent with a private Azure Container Registry](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent-private-azure-container-registry)
- [Azure Developer CLI overview](https://learn.microsoft.com/azure/developer/azure-developer-cli/overview)

## Related links

- [Optional lab index](README.md)
- [Advanced Hosted Agent](advanced-hosted-agent.md)
- [Lab 8 — Deploy an Agent Framework workflow as a Hosted Agent](../08-hosted-multi-agent.md)
