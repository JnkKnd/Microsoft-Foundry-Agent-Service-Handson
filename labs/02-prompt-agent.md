# Lab 2 — Prompt Agent and Azure AI Search (20 min)

## Goal

Create the Prompt Agent `contoso-travel-assistant` in Microsoft Foundry Portal,
ready for knowledge and tools in later labs, and connect an Azure AI Search tool to search internal policies.

Microsoft Foundry Agent Service offers two agent types:

- **Prompt Agent**: Configure instructions, a model, and tools to run on Foundry
  without managing code or infrastructure.
- **Hosted Agent**: Implement your own code and framework; Foundry runs it in
  a container with a managed endpoint, scaling, and identity.

Reference: [What is Microsoft Foundry Agent Service? — Agent types](https://learn.microsoft.com/en-us/azure/foundry/agents/overview#agent-types)

In this lab, build a **Prompt Agent** in the Portal and define its role through instructions.
Then connect an Azure AI Search tool to directly search the index of eligibility policies.
In Lab 3, switch to Foundry IQ to broaden retrieval; in Lab 4, add cost calculation.

> [!WARNING]
> Search and model calls incur charges. Use the workshop's synthetic data and example questions.

## Before you begin

Verify that Lab 1's custom template, Deployment Scripts, and validation succeeded,
then open your Foundry project from `foundryPortalUrl`.
Continue enhancing the same `contoso-travel-assistant`; no separate agent is needed for each lab.
Labs 2–6 develop this one Prompt Agent. Labs 7 / 8 reuse the remote resources prepared here
from code rather than rebuilding the same agent.

## Values to use

In Lab 1's deployment **Outputs > resourceOutputs**, find `foundry_project_name`,
`primary_model_deployment_name`, and `search_service_name`. The direct search index is
`contoso-travel-policy`. Use each item's `value`.

## 1. Create a Prompt Agent

1. Open the target project in Microsoft Foundry Portal.
2. Select **Build** at the top, then **Agents** on the left.
3. Select **New agent**.
4. Select **Build an agent**. Do not use **Code an agent** in this lab.
5. Replace the generated **Agent name** with `contoso-travel-assistant`.
6. Select **Create and open playground**.

## 2. Select the deployed model

1. Open **Model** in the configuration pane.
2. Under **Deployments**, select the value of `primary_model_deployment_name`
   (normally `gpt-5.6-luna`).

## 3. Remove automatically added Web search

New agents may include **Web search**. Remove it before asking questions because
this workshop initially uses only the supplied policies and API.

1. In **Tools**, open **Actions for Web search** at the right of the **Web search** row.
2. Select **Remove**.

If Tools has no Web search entry, no action is needed. Leave other settings, such as **Guardrail**, unchanged.

## 4. Set Instructions

Paste this into **Instructions**:

```text
You are Contoso's internal travel and expense assistant.
Answer travel and expense questions concisely in English.

Whenever connected knowledge or tools are available, always use them to verify your answer.
Cite sources for policy-based answers, and do not guess values you cannot verify.
Pass English canonical city names such as Tokyo, Osaka, and New York to Travel Ops tools.
Do not claim to have made bookings or granted approvals; explicitly state that operations are simulations.
```

## 5. Connect an Azure AI Search tool

This workshop uses Search **Basic**. Select the index seeded by Lab 1.
Do not change the Search SKU or substitute another route for direct search.

1. Select **Tools > Add > Add tools**.
2. Under **Configured**, select **Azure AI search**, then **Add tool**.

This uses the **Microsoft Entra ID-authenticated Azure AI Search connection** created in Lab 1,
not an API key.

3. Open **Azure AI Search connection** and select the `search_service_name` value
   (`srch-fdyws-...`). Do not use **Connect to new resource**.
4. Select `contoso-travel-policy` and **Add**.
5. Back in the agent, verify **Select a search index** is `contoso-travel-policy`.
6. Under Azure AI Search **Actions > Parameters**, set **Search type = Semantic**
   and **Retrieved documents = 5**. Close the configuration pane and select **Save**.

The retained screenshots for these steps are historical/illustrative, not English instructions
or current-revision success evidence: [agent list](../docs/images/lab02-agent-list.png),
[model selection](../docs/images/lab02-model-deployment.png),
[Web search removal](../docs/images/lab02-remove-web-search.png),
[Add tools](../docs/images/lab03-add-tools.png),
[Search selection](../docs/images/lab03-select-ai-search.png),
[connection](../docs/images/lab03-search-connection.png),
[index picker](../docs/images/lab03-ai-search-picker.png), and
[attached index](../docs/images/lab03-search-attached.png).

## 6. Check direct search and citations

In **Playground > New chat**, send:

```text
What is the meal per diem for a same-day business trip from Tokyo to Osaka?
```

Check the amount and numbered citations below the answer against the
[per diem and meals policy](../data/policies/04-per-diem-meals.md).
If a citation opens the Search service's top-level URL, see
[citation troubleshooting](../docs/participant/troubleshooting.md#citation-links).

Then select **New chat** again and send this comparison question, whose evidence is split across policies:

```text
I want to book business class on a 12-hour one-way international flight, 2 days before departure.
Summarize the attachment required for a last-minute booking, the business-class approvers and their order,
the feature used to apply, and the standard maximum number of business days from application to completed approval.
```

For each of these four items, record not only whether the answer contains a value but whether
it has a supporting citation. Compare the result with Foundry IQ in Lab 3.

| Item to check | Source document |
|---|---|
| Last-minute booking attachment | [Flight policy](../data/policies/02-flights.md) |
| Approvers and their order | [Approval process policy](../data/policies/09-approval-process.md) |
| Application feature | [Approval process policy](../data/policies/09-approval-process.md) |
| Standard maximum processing time | [Approval process policy](../data/policies/09-approval-process.md) |

`contoso-travel-policy` includes flight policy, while approval process policy is separated into
`contoso-travel-approval`. Only the former is connected now. Even if the answer includes a value,
record it as not retrieved unless the corresponding document supports it.

Do not judge success solely by **AI Quality** scores; compare the four items and their evidence.

## Completion checklist

- `contoso-travel-assistant` appears in the Agents list.
- The agent's model and instructions are saved.
- Tools includes Azure AI Search using `contoso-travel-policy`.
- The meal per diem answer includes an amount and numbered citations, without raw internal markers.
- You recorded evidence coverage for the four comparison items.

Direct search should generally support only the one item in the flight policy.
Next, connect Foundry IQ to search across both indexes.

<details>
<summary>Checks after answering</summary>

The domestic same-day meal per diem is `JPY 1,500`.
For the comparison question, direct search generally supports only 1 of 4 items.
Do not count values in generated text as evidence-backed answers without citations.

</details>

## Next lab

[Lab 3 — Foundry IQ](03-rag-foundry-iq.md)
