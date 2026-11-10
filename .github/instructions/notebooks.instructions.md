---
description: Preserve participant Notebook kernels, management boundaries, and safe saved content.
applyTo: "notebooks/*.ipynb"
---

# Notebook changes

- Read the [shared Dev Container](../../.devcontainer/README.md) and
  [Hosted Agent README](../../src/hosted-agent/README.md) first.
  Labs 7-8 use **Python (Foundry Hosted Agent)**; explicitly select the
  management interpreter for management operations.
- Reuse `.workshop/context.json` and `scripts/lib/` connection helpers.
  Do not hardcode subscriptions, RGs, or endpoints in cells.
- Put reusable logic in existing `scripts/` or `src/hosted-agent/` modules.
  Keep Notebooks as participant input, operation, and result-checking entry points.
- Never save credentials or environment-specific values in outputs, exceptions,
  or metadata. Avoid unnecessary outputs or execution-count changes and preserve
  unrelated cell IDs and metadata.
- Check the corresponding Lab, kernel selection, Notebook contracts, and Hosted
  tests. Update the [instructor runbook](../../instructor/runbook.md) when
  participant operations or acceptance criteria change.
- Running cells can authenticate, incur charges, deploy, or delete resources.
  Distinguish static checks from live end-to-end execution; saving a Notebook
  alone is not proof of success.
