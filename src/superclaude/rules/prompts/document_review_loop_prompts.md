# Document Review Loop Prompts

Prompts for a coordinator that briefs a reviewer or a reviser in a document review loop (`/sc:spec-panel --mode critique`). This file is read on demand and never auto-loaded. `/sc:spec-panel` makes reading it a hard gate before a re-review and before any review or revise brief is written or accepted.

## When to use which prompt

| Situation | Prompt |
|---|---|
| First review of a document | R1 |
| Any re-review (review 2 or 3) | R2 |
| After a review report with open blocking findings, to revise | V1 |

At `review: 3` with an open blocking finding the loop escalates to the user; no V1 and no fourth review.

## Roles (fixed)

- `{{CANDIDATE}}`: the revised file under review, the `@file` of the command.
- `{{BASELINE}}`: the spec as it was before the revision, the `--baseline` file.
- `{{PRIOR}}`: the previous review's report, the `--re-review` file.
- `{{N}}`: the prior report's `review: N of 3` number plus 1.
- `{{IDS}}`: the blocking finding ids listed in the report's `Reviser brief`, and only those.

In a re-review the `@file` is the revised candidate, `--baseline` is the saved copy of the spec as it was before the revision, and `--re-review` is the prior report. A brief that names these differently, or does not name them, does not change the roles.

## Prompts

### Prompt R1 (first review)

- First-review brief: "Review the candidate {{CANDIDATE}} (sha256 of the file) against the requirements it states, review 1 of 3. Inspect behavior and the dependencies it touches. Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review; list Medium and minor findings under follow-up candidates. If an input is missing or unreadable, return incomplete. Do not edit the candidate and do not start another review. State what you covered."

### Prompt R2 (re-review)

- Re-review brief: "Review the revised candidate {{CANDIDATE}} (sha256 of the file) against {{BASELINE}}, the spec as it was before the revision (sha256 of the file), using prior report {{PRIOR}} (sha256 of the file), review {{N}} of 3, where N is the prior report's review number plus 1. Re-check each prior blocking finding as resolved, open or regressed against the revised candidate. Inspect changed behavior and the dependencies it touches; for inherited text, cite the changed line it depends on. Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review; list Medium and minor findings under follow-up candidates. Record a severe defect you newly discover even if it is older, and say where it came from. If an input is missing or unreadable, return incomplete. Do not edit the candidate and do not start another review. State what you covered."

### Prompt V1 (revise)

- Revise brief: "Repair only the blocking findings {{IDS}} in the revised candidate {{CANDIDATE}}. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS."

## Never

Never put "any finding of any severity is FAIL", "assume defects remain", a required number of findings, or "apply all findings" in a brief: a brief may narrow the command's scope but may not widen it or regrade a minor finding as blocking.
