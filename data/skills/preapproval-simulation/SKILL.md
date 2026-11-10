---
name: preapproval-simulation
description: Use when explicitly asked to simulate Contoso travel preapproval or interpret its results. Do not start a simulation for estimate-only or policy-only questions.
---

# Preapproval simulation

Simulate Contoso preapproval using the Travel Ops API with synthetic data only.
This feature does not save applications, grant actual approvals, or make bookings.

## Confirm intent and inputs

1. Confirm that the user wants a simulation.
   Do not execute for "Give me an estimate" or "Is approval required?" alone.
   For "Book it" or "Approve it", explain the limits and ask whether a simulation is acceptable.
   Do not repeat confirmation if the user already explicitly requested a simulation.
2. Check origin, destination, departure date, return date, and seat class.
   Only when traveler count is omitted, explicitly state the assumption of 1 traveler.
   Ask about missing information rather than guessing.
3. Normalize city names, dates, and seat classes to the same schema forms as `travel-estimation`.
   Do not include personal information in optional `justification`. For exercises requiring
   `requester_alias`, use only synthetic aliases such as `employee-001`; do not request real names or email addresses.

## Call the API

Choose the actual published name corresponding to operationId `createPreapproval` from
the Toolbox definitions and pass the confirmed itinerary. If the API fails, explain the failure;
do not invent successful results or approval numbers.
The API also returns an estimate, so a duplicate estimate API call is unnecessary unless comparison is needed.

## Explain results

Use "Simulation result", "Cost breakdown", and "Where to check next", in that order.
Check that `simulation` is `true`. Do not remove the `simulated_` prefix from `decision`
or present the result as an actual approval.

| API decision | Meaning |
|---|---|
| `simulated_auto_eligible` | Eligible for automatic processing in the simulation, not actual approval |
| `simulated_pending_manager_review` | Manager review required in the simulation |
| `simulated_pending_vp_review` | VP review required in the simulation |

Do not interpret an unknown decision or a result whose `simulation` is not `true` as approval;
ask the instructor to clarify.
Use the `trip_estimate` breakdown and total; do not recalculate approval conditions or prices in this Skill.
Explain that `reference_id` is a synthetic reference, not a saved application number.
Do not omit the API's `disclaimer`. Explicitly state: "This is not an actual booking or approval."
