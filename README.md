**English** | [English compatibility entry](README.en.md)

# Microsoft Foundry Agent Service Hands-on

Build a travel and expense assistant for the fictional company Contoso in nine labs.
Explore retrieval, tools, evaluation, optimization, and Hosted Agents.

> [!WARNING]
> **This English branch is not yet deployment-ready.** English source and API image artifacts
> have not been published. An administrator must publish and pin an English source SHA and
> GHCR image digest before distributing a release. Links to the `English` branch are mutable
> browsing/download links, not release pins. Existing Azure environments are not automatically
> converted to English. The lab steps below describe the future pinned release.

[**Start with Lab 1**](labs/01-setup.md) ·
[Prerequisites](docs/participant/prerequisites.md) ·
[Setup guide](docs/participant/environments/custom-template.md)

The template provisions the foundation. In Labs 2–4, you connect Foundry Agent Service,
Azure AI Search, Foundry IQ, and the Travel Ops API through Toolbox.
See [architecture and communication paths](docs/development/architecture.md).
The existing [architecture PNG](docs/images/azure-architecture-01.png),
[editable PowerPoint (2 slides)](docs/diagrams/azure-architecture.pptx), and
[deployment and initialization diagram](docs/images/azure-architecture-02.png)
are historical/illustrative assets, not English instructions or evidence of success on this revision.

## Workshop flow

1. **Lab 1**: In Azure Portal, manually create one dedicated resource group (RG).
   Then use the template provided by the administrator to deploy the environment into that RG.
2. **Labs 2–6**: Create an agent in Microsoft Foundry Portal and enhance it with
   Foundry IQ and Toolbox. Learn the continuous improvement cycle through evaluation and optimization.
3. **Labs 7–8**: Use Agent Framework to create agents in code in
   [GitHub Codespaces](docs/participant/environments/codespaces.md) or the
   [local Dev Container](docs/participant/environments/local-dev-container.md).
   In Lab 7, run and compare Plain Agent and Harness Agent inside the Dev Container.
   In Lab 8, build a separate sequential workflow and deploy it as a Hosted Agent.
4. **Lab 9**: Compare Prompt Agent and Hosted Agent traces to examine execution flow
   and performance differences. Save your results, clean up Hosted Agents and the
   development environment you used, and then delete the dedicated RG.

The notebooks and Python source are already in the repository; no manual folder upload is needed.
The browser-based Codespaces route requires no local Docker or Python installation.

## Agenda

| Lab | Topic | Estimate |
|---|---|---:|
| [Lab 1](labs/01-setup.md) | Create the environment and verify initialization | [Check the event schedule](#schedule-and-preparation) |
| [Lab 2](labs/02-prompt-agent.md) | Prompt Agent and Azure AI Search | 20 min |
| [Lab 3](labs/03-rag-foundry-iq.md) | Foundry IQ | 25 min |
| — | Break | 10 min |
| [Lab 4](labs/04-tools-toolbox.md) | Toolbox, OpenAPI, Skills, and Tool Search | 30 min |
| [Lab 5](labs/05-evaluation.md) | Agent evaluation | 15 min |
| [Lab 6](labs/06-optimization.md) | Agent Optimizer | 20 min |
| [Lab 7](labs/07-agent-framework-harness.md) | Codespaces setup, Agent Framework, and Harness Agent | 50 min |
| [Lab 8](labs/08-hosted-multi-agent.md) | Hosted Agent workflow | 30 min |
| [Lab 9](labs/09-observability-cleanup.md) | Trace comparison and cleanup | 20 min |

## Schedule and preparation

The estimates total **220 minutes (3 hours 40 minutes), including the break and excluding Lab 1**.
These are planning estimates, not measured event timings.
Lab 1 is treated as not measured here; its provisioning time is excluded from that total.
Evaluation, optimization, deployment waits, and troubleshooting can change the actual finish time.

Check the event announcement to learn whether Lab 1 is performed in advance or on the day.
Complete Lab 1's initialization checks before starting Lab 2.
Organizers should use a live rehearsal to budget setup time and contingency,
and communicate costs, retention, and cleanup ownership for advance provisioning.
See the [instructor scheduling guide](instructor/README.md#schedule-planning).

## Documentation by audience

| Audience | References |
|---|---|
| Participants | [Documentation index](docs/README.md), [troubleshooting](docs/participant/troubleshooting.md), [costs and cleanup](docs/participant/costs-and-cleanup.md) |
| Administrators and instructors | [Prerequisites and models](docs/admin/prerequisites.md), [instructor guide](instructor/README.md) |
| Workshop developers | [Developer guide](docs/development/README.md), [architecture](docs/development/architecture.md) |

English is the source language on this branch. [README.en.md](README.en.md) is a compatibility entry.

> [!IMPORTANT]
> Use synthetic data only; never share or save credentials or tokens.
> Azure and Codespaces usage may incur charges.
> Follow Lab 9 to delete **only your dedicated RG** and verify that deletion completed.
