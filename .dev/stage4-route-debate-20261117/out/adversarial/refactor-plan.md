# Refactoring Plan (base: variant 2, Route B)

## Overview
- Base: variant 2. Incorporated from variant 1: 5 changes. Rejected: 2. Overall risk: Low (additive text to a position paper).
- Approval: auto-approved (non-interactive).

## Planned Changes

| # | Change | Source | Target in base | Approach | Rationale | Risk |
|---|---|---|---|---|---|---|
| 1 | Add a precondition: the owner decides the Task 1 gate (waive, hold, rollback) before any edit | A-001, A-002 (both advocates QUALIFY) | Top of "The route" | insert | Both advocates answered the same; README.md:9 says generate only after the owner's go | Low |
| 2 | Edit the request file and `source.md` together, byte-identical | V1 reward 4, C-004 (B conceded) | Route step 2 | replace | Removes B's source/plan divergence risk | Low |
| 3 | Make the contract and review concrete: new slug in folder, file name and plan front matter; contract 1.1 with the same slug; run `/sc:reflect --mode pre`, read it, write its result into the contract | V2 U-003, C-001, C-002 | Route step 3 | replace | Detection checks 1 to 4 (managed-workspace.md:9-12); stage 3 shows the cost of skipping | Low |
| 4 | Record the departure from the ledger rule (README.md:3, "generated with /sc:workflow") as an owner-approved exception | U-001 | Risks | append | The rule is the owner's; B departs from it | Low |
| 5 | Add a switch-over condition: if the carrier task changes more than one existing task, or the review finds more than one blocking defect, regenerate with Route A | X-002 (unresolved) | ROI claim | append | X-002 stayed unresolved; this converts it into a testable trigger | Low |

## Changes NOT Being Made
- Route A's "re-grounded by construction": withdrawn by its own advocate (X-001).
- Making Route A the default: it loses on C-003 and C-005 (70% each) and its only unique hard reward (valid contract) is reachable by hand.

## Risk Summary
All changes add text to a short document; rollback is deleting the lines.

## Review Status
auto-approved
