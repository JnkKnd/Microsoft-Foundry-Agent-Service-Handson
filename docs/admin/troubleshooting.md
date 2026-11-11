# Administrator troubleshooting

## Template, quotas, and policies

- Check that the manually created dedicated RG was selected and the actual
  `infra/azuredeploy.json` template was loaded with **Load file**.
- In the RG's **Deployments / Activity log**, check the failed operation, provider
  registration, locks, Policy, fixed Japan East models, and Search Basic quotas.
- Compare Bicep / generated JSON consistency and verified model, image, and source
  defaults with the [distribution guide](prerequisites.md). Do not switch regions or models.

## Initialization

1. In Deployment Scripts **Overview / Logs**, identify the failing stage: source
   retrieval, dependencies, Search seed, evaluation data / rubric preparation, or validation.
2. Check `participantObjectIdOverride`, the intended participant, and role scopes.
   The bootstrap identity and participant are different. Do not bypass 403 errors
   by granting broader permissions.
3. Repair using the same RG and verified inputs. Change `bootstrapRunId` only when
   intentionally rerunning initialization.
4. Verify that the entire deployment is **Succeeded**,
   `workshopContext.setup_status = complete`, and `source_revision` matches.

Failure does not necessarily trigger automatic rollback. Do not treat a previous
success as success for this run; also inspect partial resources.
See [infra/README.md](../../infra/README.md) for log retention, retries, and temporary infrastructure.

## Application Insights automatic alerts

The workshop uses **trace collection and viewing only; automatic alerts are outside
the exercises**. The template creates neither alert rules nor notification targets.
Trace collection uses `Microsoft.Insights` and `Microsoft.OperationalInsights`;
registration of `Microsoft.AlertsManagement` is not a participation requirement.
`admin-preflight.sh` does not check, warn about, or register this provider.

However, this **does not stop Azure from automatically creating default alerts**.
When Application Insights is created, Azure separately creates a Failure Anomalies
alert. If only `Failure-Anomalies-Alert-Rule-Deployment-*` fails with
`MissingSubscriptionRegistration` indicating unregistered `Microsoft.AlertsManagement`,
investigate separately from the workshop deployment.
Check that the main deployment is **Succeeded**, `workshopContext.setup_status = complete`,
and traces needed in Lab 9 can be recorded and viewed.

You do not need to register another provider or recreate alerts for this exercise.
This change does not disable / delete existing alerts or unregister existing providers.
If default alert notifications must also stop, an administrator must identify the
specific rule and disable it separately. Do not erase history to hide failures or
broaden participant / bootstrap identity permissions.

See [creating and managing default alerts (Microsoft Learn)](https://learn.microsoft.com/azure/azure-monitor/alerts/proactive-failure-diagnostics#managing-failure-anomalies-alert-rules).

## GitHub shared materials and Notebooks

| Symptom | Check |
|---|---|
| Cannot retrieve assets | Is the distribution reference public, and are bootstrap / shared material revisions compatible? |
| Cannot register a Skill | Select the ZIP on the PC; check that `SKILL.md` is at its root. |
| OpenAPI calls another API | Does `servers[0].url` match the participant's `travelApiBaseUrl`? |
| Kernel is missing | Check **Select Kernel > Jupyter Kernel...** and post-create success. Do not modify the existing host environment. |
| CLI authentication error | Did the participant sign in to Azure CLI in the same container as the Notebook? |
| Cannot retrieve context | Check subscription / RG, successful schema `2.0` `workshopContext`, and read permissions. |
| Multiple deployment candidates | After confirming the target, an administrator specifies `configure_workshop.py --deployment <name>`. Do not guess. |
| Context targets another environment | Check the current checkout and intended environment without overwriting another environment's settings. |

Use the [shared Codespaces procedure](../participant/environments/codespaces.md#shared-steps).
Do not substitute API keys, manually injected tokens, or shared credentials.

## When deletion fails

Follow [Lab 9](../../labs/09-observability-cleanup.md): verify saving work, deleting
Hosted Agent versions, and stopping / deleting the Codespace before deleting the
participant's dedicated RG in Azure Portal. Do not resubmit during deletion.
On failure, check **Activity log**, locks, and deny assignments.
Verify that the RG disappears from **Resource groups**; deleting deployment history
alone is not completion.

## Handling validation results

For real UI validation, check operation results in Azure Portal, Foundry Portal,
and Codespaces / VS Code. CI, isolated SDK success, and simulated JSON are not
proof that unperformed UI operations succeeded.
Do not store account-specific information or private evidence in the repository.
