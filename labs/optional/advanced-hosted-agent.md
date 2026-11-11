# Optional lab — Advanced Hosted Agent (container deployment, protocols, Tool Search, and Skills)

## Scope of this document

[Lab 8](../08-hosted-multi-agent.md) deploys the Agent Framework workflow in `src/hosted-agent/`
as a Hosted Agent using **source-code remote build**, the only route used by
`scripts/deploy_hosted_agent.py`. **The main core remains source deployment.**
This lab explores optional extensions based on Lab 8's code and deployment.
Use a separate approved test environment for extra infrastructure.
This is not a replacement for Lab 1 manual RG creation, custom template, GitHub materials, or Codespaces.

> [!IMPORTANT]
> None of these exercises changes existing files in `scripts/deploy_hosted_agent.py`
> or `src/hosted-agent/`. For ACR container deployment, use an **agent name different**
> from the main `contoso-travel-hosted-planner`.
> Although there is no API for overwriting existing versions, separate names prevent cleanup confusion.

## 1. Container/ACR deployment (optional; core remains source deployment)

### 1.1 When to use ACR

Hosted Agents fundamentally run container images built and pushed to Azure Container Registry (ACR)
and pulled by Foundry. Main-workshop source deployment uses `dependency_resolution=REMOTE_BUILD`
(Foundry server-side build), avoiding participant Hosted-image builds and ACR preparation.
Consider container/ACR deployment for:

- **Compliance**: Images must reside in an organization's centrally managed registry.
- **Shared infrastructure**: Multiple agent projects share one ACR.
- **ABAC-mode registries**: An attribute-based access control (ABAC) registry is required.
- **Prebuilt images**: Images are vulnerability-scanned, supply-chain-signed, hardened,
  or already built by another CI pipeline.

### 1.2 Prerequisites

- An initialized Hosted Agent project with `azure.yaml`;
  see [Initialize the project](azd-appendix.md#3-initialize-the-project).
- Foundry extensions (`microsoft.foundry`) installed for `azd`.
- An authenticated `azd auth login` session (**separate from `az login`**).
  Main Hosted execution uses participant Azure CLI authentication in the Dev Container,
  not `azd auth login`; see the [azd appendix](azd-appendix.md).
- Access to an existing ACR and roles required by the chosen build route.

### 1.3 Workflow overview

```bash
# 1. Inspect/select an existing project's ACR connection (prompted for a registry if none exist)
azd ai agent init

# 2. Build locally and push to the selected ACR
azd ai agent build
azd ai agent push --registry <your-acr-name>.azurecr.io

# 3. Deploy to Foundry (combined build, push, registration, identity creation, and RBAC)
azd ai agent deploy
```

For an existing Foundry project, `azd ai agent init` scans ACR connections and presents candidates.
With none, it prompts for an ACR login server such as `myregistry.azurecr.io`.
Leaving it blank lets `azd provision` create a new project-specific ACR.

> [!NOTE]
> Making ACR "private" (network isolation such as `publicNetworkAccess: Disabled`)
> is separate from registry selection. As described in the
> [architecture](../../docs/development/architecture.md), this workshop does not cover
> VNet injection or private endpoints, so private ACR configuration is outside this lab.

### 1.4 Use a prebuilt image directly

Deploy an image already built/pushed by another CI pipeline without rebuilding
(equivalent to `azd ai agent deploy --source <image-ref>`; confirm exact flags
for your azd Foundry extension version).
This fits [CI/CD and continuous evaluation](cicd-continuous-evaluation.md),
separating builds/vulnerability scans and Foundry deployment into different permissions/pipelines.

## 2. Custom packages beyond the main requirements.txt

Main source deployment uses `REMOTE_BUILD` to `pip install` Python packages
listed in `src/hosted-agent/requirements.txt`.
Container builds are more flexible for:

- Libraries needing OS packages such as apt packages
- Compiled binaries or toolchains distributed outside pip
- Multiple languages, such as Python + Node.js, in one container

First establish required dependencies locally with `python main.py`, as in the
main Lab 8 context, then encode them in a `Dockerfile` to isolate remote build failures.

## 3. Multiple protocols (Responses, Invocations, Invocations (WebSocket), A2A, Activity)

Main `src/hosted-agent/main.py` implements only **Responses** (port 8088).
One Hosted Agent version can expose multiple protocols:

| Scenario | Protocol | Reason |
|---|---|---|
| Conversational assistants | **Responses** | Platform manages history, streaming, and sessions |
| Webhooks (GitHub, Stripe, Jira, etc.) | **Invocations** | Senders use custom payloads incompatible with `/responses` |
| Nonconversational classification, extraction, batch | **Invocations** | Structured data rather than chat messages |
| Real-time microphone/audio output | **Invocations (WebSocket)** | Bidirectional streaming over one persistent connection |
| Teams / Microsoft 365 publication | **Responses** + **Activity** | Implement logic with Responses; platform automatically bridges to Activity for channels |
| Delegated calls from other agents | **A2A (preview)** | Agent-to-Agent delegation |

Official guidance recommends starting with **Responses** when unsure.
Invocations endpoints can be added later; see [Hosted agents concepts](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents).
See [A2A, Routines, and Publish](a2a-routines-publish.md) for A2A prerequisites/enablement.

## 4. Tool Search (preview)

Tool Search discovers needed tools when a Toolbox contains many tools,
rather than loading all definitions at once.
Main Lab 4 enables it in Portal Toolbox settings. Use Foundry Toolkit or the SDK for
advanced configuration such as pinning/additional search terms and reproducible automation.
For Hosted Agent Toolboxes combining many tools (such as Fabric IQ, Work IQ,
and Travel Ops API OpenAPI tools), Tool Search avoids embedding all definitions in every prompt,
reducing context size and latency. Preview behavior and latency characteristics may change.

## 5. Skills

In [Lab 4](../04-tools-toolbox.md), upload `travel-estimation` and `preapproval-simulation`
in the Portal and include them in the same Toolbox as Travel Ops API.
Skills are not ordinary API tools; they reside in a separate `skills[]`
and are exposed through MCP `resources/list` / `resources/read`.

A compatible Skill provider is required for Hosted Agent use.
It exposes Skill names/descriptions and progressively discloses bodies only when needed.
Lab 7's Harness factory includes this provider, but Lab 8's ordinary-agent workflow
does not use Skills, reducing token consumption.
Lab 7 verifies Skill loading separately from API calls.
For extensions, consult the
[official Agent Framework Toolbox Skills sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents/agent-framework/foundry-toolbox-mcp-skills)
and [Skills specification](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/skills),
and verify loading separately from API invocation.

## 6. Permission considerations

- **Agent identity**: A dedicated Microsoft Entra ID automatically created per Hosted Agent version.
  It has model inference/session storage access by default.
  Manually assign RBAC for external resources such as your own Azure Storage.
- **Project managed identity**: The Foundry project's system-assigned identity has
  infrastructure permissions such as **Container Registry Repository Reader** to pull ACR images.
  It is not the agent's runtime identity.
- Do not confuse them: agent code uses agent identity; Foundry infrastructure operations use project managed identity.

## 7. Cleanup beyond the main dedicated resource group

- Agents created with names other than `contoso-travel-hosted-planner` are not deleted
  by the default `--agent-name` in `./scripts/delete_hosted_agent.py`.
  Explicitly specify each additional agent name to delete it and its versions.
- Pushed container images remain in ACR repositories.
  The main custom template does not create/manage ACR; see [architecture](../../docs/development/architecture.md).
  For bring-your-own ACR, confirm image ownership/deletion. Do not delete the whole shared registry.

## Official references

- [Hosted agents in Foundry Agent Service](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Deploy a hosted agent with a private Azure Container Registry](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent-private-azure-container-registry)
- [Install the Azure Developer CLI Foundry extensions](https://learn.microsoft.com/azure/foundry/agents/how-to/install-cli-foundry-extensions)
- [Curate intent-based toolbox in Foundry](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/toolbox)

## Related links

- [Optional lab index](README.md)
- [Lab 8 — Deploy an Agent Framework workflow as a Hosted Agent](../08-hosted-multi-agent.md)
- [azd appendix](azd-appendix.md)
- [A2A, Routines, and Publish](a2a-routines-publish.md)
