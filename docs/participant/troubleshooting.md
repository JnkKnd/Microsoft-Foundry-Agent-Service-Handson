# Troubleshooting

If initialization fails, do not proceed to Lab 2; report the error to the administrator.
Do not repeat running operations or share authentication codes, tokens, or keys.

| Symptom | First checks |
|---|---|
| Cannot create an RG | Check account, subscription, and creation permissions. Do not substitute a shared RG |
| Cannot load the template | Verify that you have the administrator-designated `azuredeploy.json` itself; an HTML page cannot be loaded |
| Deployment or initialization fails | Check the RG's **Deployments** and Deployment Scripts **Logs**. Contact the administrator without changing regions or models |
| Cannot find models or connections | Verify that you opened your project from Lab 1's **Outputs > resourceOutputs** |
| Cannot create a Codespace | Check the GitHub account, allowances, and organizational Codespaces policy |
| Kernel is missing | Check **Select Kernel > Jupyter Kernel...**. If still missing, verify post-create completion and the [setup guide](environments/codespaces.md) |
| Notebook output is truncated | Select **scrollable element** under **Output is truncated**. Do not rerun the cell to inspect output |
| Notebook authentication error | Verify Azure CLI sign-in in the container Terminal. Portal sign-in alone is insufficient |
| Setup cannot find a target or finds ambiguous targets | Check subscription ID / RG name and a **Succeeded** deployment. Ask the administrator about multiple candidates; do not guess |
| Setup stops on a connection mismatch | Check the existing `.workshop/context.json` and intended target. Do not overwrite another environment's settings and continue |
| Cannot delete an RG | Check the order in [Lab 9](../../labs/09-observability-cleanup.md) and **Activity log**. Ask the administrator about locks or other obstacles |

## Lab 4 files

Upload Skill ZIPs saved to your PC from the [GitHub links in Lab 4](../../labs/04-tools-toolbox.md).
The ZIP must contain `SKILL.md` at its root; do not select a standalone Markdown file.
In `travel-ops.openapi.json`, replace `servers[0].url` with **Outputs > travelApiBaseUrl**,
then paste the entire JSON into **OpenAPI 3.0+ schema**.
If you see a 404 or HTML, ask the administrator to check the link and saved file.

## Citation links

For Lab 2, check **Search type = Semantic** and **Retrieved documents = 5**
under Azure AI Search **Actions > Parameters**. Compare not just amounts but also
applicability conditions and supporting documents.
If a result URL opens Search itself, ask the administrator to check `source_url`.
Foundry IQ's `mcp://searchindex/...` is an internal citation ID.
Do not open it as a web page; compare the document ID in **Traces** with the workshop policies.
If internal `cite` markers remain visible in a Portal response, record a citation-rendering mismatch
and check retrieved documents in **Traces** against the source material.
Search settings alone may not fix rendering; do not count this as success.

## Evaluation and optimization

Do not resubmit while status is **In progress**. Distinguish 429 errors and timeouts
from an evaluation result of **Fail**.
`content_filter` indicates a safety block. Share the error with the administrator without weakening guardrails.
If **No supported optimization model** appears, ask for a check rather than adding another model.

[Back to setup: Lab 1](../../labs/01-setup.md)
