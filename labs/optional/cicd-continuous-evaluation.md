# Optional lab: CI/CD and continuous evaluation

## Goal

Learn a design connecting Portal-verified Hosted Agent source and evaluation materials
to GitHub Actions review, deployment, and evaluation approval stages.
Main-workshop resources are managed by Bicep / ARM templates in a manually created RG,
so workflows separate infrastructure deployment from agent deployment.
This appendix does not replace participant RG creation, the custom template, or GitHub shared materials.

## Security prerequisites

- Use GitHub OIDC and workload identity federation, not long-lived client secrets.
- Configure per-environment approvals and least privilege limited to target resources.
- Do not save tokens, device codes, or `.workshop/context.json` in logs/artifacts.
- Do not copy production data into synthetic evaluation datasets.
- Record pinned source revisions and Hosted Agent versions.

## Recommended check and approval order

1. Check Markdown, contract tests, and unit tests.
2. Read-only checks of resource names, project endpoints, model deployments, and connections.
3. Obtain the responsible person's approval.
4. Deploy the Hosted Agent.
5. Evaluate basic behavior using 7 synthetic cases.
6. Inspect errors, reasons, and traces as well as scores.
7. Promote the approved version.

Do not let the pipeline expand template-defined RBAC or resource settings without permission.
Evaluation and deployment incur charges. Avoid duplicate submissions and limit retention/concurrency.

## Cleanup

Inventory Hosted Agent versions, evaluation runs, federated credentials, and
environment secrets/variables created by the workflow; delete those no longer needed.
Main-workshop Lab 9 does not delete extra subscription- or organization-level objects.
