---
id: policy-per-diem-001
title: Per Diem and Meals Policy
category: per_diem_meals
effective_date: 2026-04-01
applies_to:
  - all_employees
source_url: "{{WORKSHOP_SOURCE_BASE}}/data/policies/04-per-diem-meals.md"
---

# Per Diem and Meals Policy

## Regional tiers and per diem rates

Meals during business travel are paid as a **fixed per diem**, not reimbursed at actual cost.
Regional tiers match the `tier` field returned by the Travel Ops API `/per-diem` endpoint.

| Regional tier | Example cities | Per diem (per day) | Hotel cap (per night) |
|---|---|---|---|
| domestic_tier1 | Tokyo, Osaka, Nagoya, Yokohama, Fukuoka, Sapporo | JPY 3,000 | JPY 15,000 |
| domestic_tier2 | Other domestic cities | JPY 2,500 | JPY 12,000 |
| international_tier_a | New York, San Francisco, London, Paris | JPY 6,000 | JPY 25,000 |
| international_tier_b | Singapore, Hong Kong, Sydney | JPY 5,000 | JPY 20,000 |
| international_tier_c | Other international cities | JPY 4,000 | JPY 18,000 |

Hotel caps are identical to those in the [Hotel Policy](03-hotels.md).

## Day trips (without an overnight stay)

Meal per diem for day trips is fixed regardless of regional tier:

- Domestic day trip: JPY 1,500 (fixed)
- International day trip: JPY 3,000 (fixed; an uncommon case)

## Counting days for overnight trips

- Pay 100% of the applicable tier's per diem for every day, including departure and return
  days (no proration).
- Per diem includes breakfast, lunch, dinner, and snacks. For days when a conference or
  training provides meals, report a 50% reduction in per diem.

## Per diem is not actual-cost reimbursement

- No receipt is required for per diem.
- If actual meal costs exceed per diem, the difference cannot be reimbursed.
- If actual meal costs are below per diem, no refund is required.
