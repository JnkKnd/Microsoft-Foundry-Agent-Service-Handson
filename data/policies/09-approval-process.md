---
id: policy-approval-process-001
title: Approval Process Policy
category: approval_process
effective_date: 2026-04-01
applies_to:
  - all_employees
  - managers
  - department_vps
source_url: "{{WORKSHOP_SOURCE_BASE}}/data/policies/09-approval-process.md"
---

# Approval Process Policy

## When preapproval is required

| Condition | Required approval |
|---|---|
| All international trips | Manager preapproval before booking |
| Domestic trip with total estimate at or below JPY 100,000 | No preapproval (post-trip review only) |
| Domestic trip with total estimate above JPY 100,000 | Manager preapproval before booking |
| Business class | Manager and department VP preapproval (both required) |
| First class | Generally prohibited. Only exceptions under [Accessibility and Exceptions](08-accessibility-exceptions.md) may receive three-party approval from HR, Travel Ops, and the department VP |
| Hotel cap exceeded | Manager preapproval before booking |
| High-risk destination | Preapproval from Travel Ops and Contoso Travel Safety Desk |

The total estimate is the sum of estimated flights, hotels, and per diem.
Use `total_estimate` returned by Travel Ops API `POST /trip-estimates`.

## Requesting preapproval

- Use the Preapproval Request feature in Contoso Travel Portal. This workshop
  simulates that submission flow through the `POST /preapprovals` endpoint.
- **Important**: `POST /preapprovals` in this workshop is an educational simulation
  with no actual approval authority. For real travel, always obtain formal approval
  through Contoso Travel Portal.

## Approval SLA

- Manager approval: A decision within 2 business days of submission.
- Department VP approval: A decision within 2 business days after manager approval.
- These 2 stages are sequential, so the standard maximum time from submission
  to department VP approval is 4 business days.
- If no decision is made within the SLA, you may escalate to Travel Ops.

## Changes after approval

- If trip details (seat class, hotel city, or dates) change after approval,
  reapproval is required when the total estimate increases by 10% or more.
