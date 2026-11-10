# Lab 9 — Trace comparison and cleanup (20 min)

## 1. Compare traces

In Foundry Portal **Build > Agents > Traces**, open the Lab 4 and Lab 8 runs.

- Prompt Agent: inspect `tool_search` → `call_tool` → actual tool calls.
- Hosted Agent: inspect `intake_agent` → `policy_agent` → `reviewer_agent`
  and `policy_agent`'s `knowledge_base_retrieve`.
- Compare responses, duration, and token usage.

## 2. Save results and delete the Hosted Agent

1. Use VS Code **File > Save All**. In Codespaces, export needed notebooks and results
   to your PC using Explorer **Download...**.
2. Open Lab 8's notebook with **Python (Foundry Hosted Agent)**, check the delete-cell target,
   and enter the displayed **Agent name** (`contoso-travel-hosted-planner`).
   The cell performs deletion in management `foundry-workshop` venv.
3. Verify the Hosted Agent and all versions have been deleted or do not exist.

## 3. Stop and delete the Codespace

Find this workshop's Codespace in [Your codespaces](https://github.com/codespaces).

1. Select **… > Stop codespace** and verify it stopped.
2. Reconfirm saving/export is complete, then select **… > Delete**.
3. Verify it disappears from the list. Stopping alone leaves storage.

For local Dev Container execution, save files and stop only this workshop's container.
Do not delete other containers, volumes, or host Python environments.

## 4. Delete the dedicated RG

1. In Azure Portal **Resource groups**, open your RG from Lab 1.
2. Check subscription and RG name, then select **Delete resource group**.
3. Enter the RG name and confirm with **Delete**. Remaining resources are deleted with the RG.
4. Refresh **Resource groups** and verify the RG is gone.

**Deleting deployment history does not delete resources.**
If deletion fails, check **Activity log** and contact the administrator.

> [!IMPORTANT]
> Delete **only your dedicated RG**, after exporting needed results and
> deleting the Hosted Agent and Codespace.
