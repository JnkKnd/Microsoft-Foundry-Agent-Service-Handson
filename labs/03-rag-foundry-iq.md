# Lab 3 — Foundry IQ (25 min)

## Goal

Lab 2 directly searched one eligibility-policy index using an Azure AI Search tool.
In this lab, create a **Foundry IQ knowledge base** with two source indexes:

- `contoso-travel-policy` for eligibility conditions
- `contoso-travel-approval` for approval procedures

Foundry IQ decomposes questions and retrieves evidence from multiple sources.
For example, it can consult both eligibility for business class and the approvers and their order,
even when they are in separate policies. Connect it to the Prompt Agent, send the same question as
Lab 2, and verify **increased evidence coverage** compared with direct search.

The `contoso-travel-knowledge-lab` created here is a shared remote knowledge base
also used by Lab 7's plain / Harness Agent and Lab 8's Hosted workflow.

> [!WARNING]
> Search and model calls incur charges. Use the workshop's synthetic data and example questions.

## 1. Create a Foundry IQ knowledge base

Create the knowledge base under **Build > Knowledge** before attaching it to the agent.

1. Open **Build > Knowledge** in the left navigation.
2. Set **Connection** to `contoso-travel-search`.
3. Select **Create a knowledge base**.
4. In Lab 1's deployment **Outputs > resourceOutputs**, check `evaluation_model_deployment_name.value`.
5. Set **Basic configuration** as follows:

   | Field | Value |
   |---|---|
   | Name | `contoso-travel-knowledge-lab` |
   | Chat completions model | Value of `evaluation_model_deployment_name` (normally `gpt-5.5`) |
   | Retrieval reasoning effort | **Medium** |
   | Output mode | **Extractive data** |

Select `gpt-5.5` from **Deployments** for **Chat completions model**.
Change **Retrieval reasoning effort** from its default Minimal to **Medium**.
Leave **Description** and **Retrieval instructions** empty for this exercise.

6. Select **Knowledge sources (Foundry IQ) > Add sources > Azure AI Search Index**.
7. Configure the dialog and select **Create**:

   | Field | Value |
   |---|---|
   | Name | `travel-rules-source-lab` |
   | Description | `Policies for travel eligibility, flights, accommodation, per diem, and receipts. Consult a separate source for approval procedures.` |
   | Select search index | `contoso-travel-policy` |

8. Select **Add sources > Azure AI Search Index** again and add:

   | Field | Value |
   |---|---|
   | Name | `approval-workflow-source-lab` |
   | Description | `Policies for the preapproval application feature, approvers and their order, and standard processing days.` |
   | Select search index | `contoso-travel-approval` |

9. Verify both sources appear, then select **Save knowledge base**.
10. Wait for `contoso-travel-knowledge-lab` to show **Active** in the list.

The retained [Knowledge home](../docs/images/lab03-knowledge-home.png),
[basic configuration](../docs/images/lab03-knowledge-base.png),
[source configuration](../docs/images/lab03-knowledge-source.png), and
[save knowledge base](../docs/images/lab03-save-knowledge-base.png) screenshots are
historical/illustrative, not English instructions or success evidence for this revision.

## 2. Connect the knowledge base to the agent

1. Return to **Build > Agents > contoso-travel-assistant**.
2. To keep comparison conditions consistent, select **Actions > Remove** for
   **Azure AI Search** in **Tools**, then **Save**.

This does not delete the Search service or indexes; it only changes the connection method.
The [direct-search removal screenshot](../docs/images/lab03-remove-direct-search.png) is historical/illustrative.

3. Open `contoso-travel-knowledge-lab` from the **Knowledge** list.
4. Select **Use in an agent > contoso-travel-assistant**.
5. Verify the knowledge base appears under the agent's **Knowledge**.
   This may save automatically. Click **Save** if enabled; otherwise continue.

## 3. Check agentic retrieval

Select **New chat** in Playground and send the same question as Lab 2.
Always compare in a new conversation so direct-search answers do not leak in from chat history.

```text
I want to book business class on a 12-hour one-way international flight, 2 days before departure.
Summarize the attachment required for a last-minute booking, the business-class approvers and their order,
the feature used to apply, and the standard maximum number of business days from application to completed approval.
```

Compare the answer and citations against:

| Item to check | Source document |
|---|---|
| Last-minute booking attachment | [Flight policy](../data/policies/02-flights.md) |
| Approvers and their order | [Approval process policy](../data/policies/09-approval-process.md) |
| Application feature | [Approval process policy](../data/policies/09-approval-process.md) |
| Standard maximum processing time | [Approval process policy](../data/policies/09-approval-process.md) |

## 4. Check the evidence behind the answer

Verify that the **Supporting documents** at the end of the answer include flight
and approval process policies, with categories `flights` and `approval_process`.
Additional sources such as FAQs are acceptable.

For Search-index-based Foundry IQ, citations may appear as internal identifiers
such as `mcp://searchindex/...`. These are not ordinary web URLs;
opening them directly in a browser is not a success criterion.
Use the source links in the comparison table above.

1. In **Traces**, open this run's **Trace ID**.
2. Under **Trajectories > Find in trace**, search for `knowledge_base_retrieve`
   and open the matching operation's **Input + Output**.
3. Check the question in **Input** and documents with `flights` / `approval_process` in **Output**.
   Compare retrieved documents with the answer and with the result recorded in Lab 2.

## Completion checklist

- All four items are correct, with more evidence-backed items than direct search.
- Citations and supporting documents include flight and approval process policies.
- `knowledge_base_retrieve` output in Traces includes `flights` and `approval_process` documents.

<details>
<summary>Checks after answering</summary>

The comparison question checks these four items:

| Item | Policy-based answer |
|---|---|
| Last-minute booking attachment | Attach the manager's approval comment in Contoso Expense |
| Approvers and their order | Manager, then department VP |
| Application feature | `Preapproval request` |
| Standard maximum processing time | 4 business days |

The expected comparison is generally 1/4 for direct search and 4/4 for Foundry IQ.
Generated wording may vary, but separating source documents across indexes allows
the same assessment through citation coverage.

</details>

Background: [What is Foundry IQ?](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq),
[Connect Agents to Foundry IQ](https://learn.microsoft.com/azure/foundry/agents/how-to/foundry-iq-connect),
[Retrieval reasoning effort](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-set-retrieval-reasoning-effort),
and [MCP response format](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-retrieve#review-the-mcp-response).

## Next lab

[Lab 4 — Travel Ops API Toolbox](04-tools-toolbox.md)
