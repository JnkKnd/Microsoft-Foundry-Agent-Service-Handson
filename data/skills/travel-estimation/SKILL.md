---
name: travel-estimation
description: Use for Contoso travel cost estimates, per diem and hotel cap inquiries, or travel requests with missing information. Check inputs, choose the Travel Ops API operation, and explain results without inventing prices.
---

# Travel cost estimation

Answer in English using the Travel Ops API for fictional Contoso trips.
This Skill describes API operations, not the travel policy itself.
Do not duplicate amounts or approval conditions here. Use API results and, when connected,
policies retrieved through Foundry IQ.

## Check inputs

- For per diem and hotel-cap inquiries only, check the city and date.
- For a full-trip estimate, check origin, destination, departure date, return date, and seat class.
  Only when traveler count is omitted, use the API default of 1 and explicitly state that assumption.
- Do not guess dates or cities. Ask the user about missing or ambiguous required values before calling the API.
- When meaning is unambiguous, normalize city names to schema forms such as `Tokyo`, `Osaka`,
  and `New York`, dates to `YYYY-MM-DD`, and business class to `business`.
  Never silently substitute another city for an unsupported city or route.

## Choose the operation

Check the actual published tool name and arguments corresponding to each operationId
in the Toolbox tool definitions. Published names may have a prefix such as `travel_ops_api___`.

| Request | operationId | Inputs |
|---|---|---|
| Per diem and hotel cap | `getPerDiem` | `city`, `date` |
| Full-trip estimate | `createTripEstimate` | `origin_city`, `destination_city`, `start_date`, `end_date`, `cabin_class`, `traveler_count` |

The estimate API already calculates per diem; calling `getPerDiem` first is not always necessary.
Do not call `createPreapproval` for an estimate-only request. Use the `preapproval-simulation`
Skill only if the user also explicitly requests a preapproval simulation.

## Explain results

Use the sections "Assumptions", "Cost breakdown", and "Items to confirm", in that order.
For a full-trip estimate, use the API's `flight_cost`, `lodging_cost`, `meal_cost`,
`total_estimate`, and `currency` unchanged. Distinguish daily rates from nightly rates in per diem inquiries.
Do not invent prices or add per diem to the API total a second time.

An API indication that approval is required does not mean approval has been obtained.
For policy evidence, use Foundry IQ and cite only sources actually retrieved.
If policies and the API disagree, show both and ask the instructor to clarify.
If the API fails, explain the error and missing information; do not present a successful estimate.

End with: "This is an estimate based on synthetic data, not an actual booking or approval."
Do not enter or request real personal, customer, or booking information.
