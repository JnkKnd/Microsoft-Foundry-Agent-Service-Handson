---
description: Keep Bicep source, generated ARM, and Deployment Scripts consistent.
applyTo: "infra/**,scripts/bootstrap_custom_template.py,scripts/bootstrap-custom-template.sh,scripts/check_template_artifact.py"
---

# Template and initialization changes

- Read the [infrastructure guide](../../infra/README.md) and
  [AGENTS environment requirements](../../AGENTS.md#environment-creation-requirements)
  before editing. `infra/main.bicep` defines models, capacities, and connections;
  do not duplicate those values in instruction files.
- `infra/azuredeploy.json` is generated. Do not edit it manually. Regenerate with
  `make bicep-build` after Bicep changes and verify equality with `make bicep-validate`.
  Follow the [developer guide](../../docs/development/README.md) for environments
  and the pinned compiler.
- Keep release defaults, the parameter example, administrator documentation, and
  generated ARM synchronized. Verify published source SHAs and image digests;
  never guess unpublished values. Empty English release pins must fail explicitly.
- Separate bootstrap and participant identities. Keep RBAC scoped to intended
  resources in the existing RG. Preserve names, role assignments, and rerun idempotency.
- Surface initialization failures and exhausted retries in deployment results.
  Never publish incomplete connection information as success. Check the
  `resource_outputs` contract and related tests together.
- Compilation and contract tests do not prove deployment success. Keep real
  deployment, permission changes, and deletion out of static validation and follow
  the existing runbook and approved scope.
