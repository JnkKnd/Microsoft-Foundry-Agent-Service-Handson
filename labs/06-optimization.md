# Lab 6 — Agent Optimizer (20 min)

## Goal

Generate candidate Prompt Agent configurations using the same evaluation data as Lab 5,
and apply only a candidate that improves on baseline.

Compare the original **baseline** and generated **candidate** using the same questions
and scoring criteria, and decide whether to adopt the changes based on their content and results.

> [!WARNING]
> The agent and tools run repeatedly for dataset rows, incurring model and external tool charges.

## 1. Open the optimization wizard

1. Open **Build > Agents > contoso-travel-assistant**.
2. Select the **Optimize** tab.
3. Select **Optimize my agent** initially, or **Create optimization run** on later runs.

## 2. Set Target

In Lab 1's deployment **Outputs > resourceOutputs**, check
`optimizer_model_deployment_name` and `evaluation_model_deployment_name`.
Both are `gpt-5.5` in this workshop.

In **Target**, set:

| Field | Value |
|---|---|
| Version | Latest version with changes saved through Lab 4 |
| Optimization model | `optimizer_model_deployment_name` (`gpt-5.5`) |
| Max candidates | `1` |
| Evaluation model | `evaluation_model_deployment_name` (`gpt-5.5`) |
| Compare across models | Off |

Choose **gpt-5.5** for both models, not `gpt-5.6-luna` or `embedding`.
Limit candidates to **1** to reduce token usage.
Check settings and select **Next**.

## 3. Select the dataset

1. Under **Data**, select **Select dataset and criteria**.
   Do not use the initial **Generate data** selection; no new question set is needed.
2. Check the `contoso-travel-optimizer-live-subset` row on the right.
   Do not choose `skill_...` data.
3. Select **Next**.

This dataset contains the same 7 questions as Lab 5, with the optimizer-required
reference answer (`ground_truth`) populated on every row.

## 4. Select Criteria

1. Under **Criteria**, select **[Contoso Travel Rubric](../docs/participant/contoso-travel-rubric.md)**
   registered by Lab 1.
2. Add no other evaluators; select **Next**.

This evaluator scores policy compliance, citations, tool use, and scope/safety.
Inspect actual selected tools and their arguments/outputs in each candidate's Conversation / Trace.

The retained [Target settings](../docs/images/lab06-target-settings.png),
[existing dataset](../docs/images/lab06-existing-data.png), and
[custom rubric selection](../docs/images/lab06-optimizer-criteria.png) screenshots
are historical/illustrative, not English instructions or success evidence for this revision.

## 5. Check Cost estimate and run

In **Review**, check the agent, dataset, models, candidate count, evaluator, and **Estimated cost**,
then select **Submit**. The estimate's **Maximum** is not a billing cap.

## 6. Compare candidates

Wait until Run detail status is **Succeeded**. Do not resubmit the same run.

1. Compare **Improvement**, **Baseline**, and **Best score**.
2. Under **Candidate results > View changes**, inspect before/after changes and select **Close**.
3. Open the `evalrun_...` link in **Score details** at the table's far right
   for the candidate you want to inspect.

With **Max candidates = 1**, two rows may appear: one generated candidate plus baseline.

Read `system_prompt` changes and responses, checking:

- Instructions to clarify missing information and avoid claims of actual booking/approval remain.
- Policy amounts, approval conditions, and processing days are not copied into instructions in a way that overrides retrieval.
- Questions previously answered correctly do not gain unnecessary clarification questions.
- The candidate does not invent unconsulted sources or results of unexecuted tools.
- Changes do not hide either `tool_search` / `call_tool` or downstream operations.
- Estimate requests do not unnecessarily invoke `createPreapproval`, Web Search, or Code Interpreter.

In the Evaluation run, select **View rubric details** beside scores in **Detailed metrics result**.
Inspect criterion weights, scores, and reasons; select **Done** to return to comparison.
This is a small question set. Do not adopt a higher-scoring candidate if content or safety deteriorated,
and do not infer improvement from a small score difference alone.

Completing the comparison meets this lab's goal even if no candidate is worth adopting.
In that case, skip promotion and proceed to Lab 7.

## 7. Promote an improved candidate

Do this only if a candidate clearly improves on baseline.

1. Select **Promote candidate**.
2. Recheck the score difference between best candidate and baseline, and the changes.
3. In the confirmation dialog, select **Promote to agent version**.

Verify **Promoted**. Return to the agent and verify model `gpt-5.6-luna`
and the Knowledge/Toolbox connections remain.
In Toolbox, verify Code Interpreter, Web Search, both Skills, existing policies/guardrail,
and Tool Search On remain. Maintain Skill registration/publication for Lab 7,
but regard Prompt Agent Skill use as proven only by `load_skill` or `resources/read` in Trace.
Lab 7's Harness Agent loads Skills through the Skill provider and verifies execution records.

In **New chat**, retry Lab 3 / 4 questions and verify policy retrieval and
`tool_search → call_tool → createTripEstimate` still work.

Details: [Quickstart: Optimize a prompt agent](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-optimize-prompt-agent).

## Next lab

[Lab 7 — Build an Agent and Harness Agent with Agent Framework](07-agent-framework-harness.md)
