# Document Review Loop Prompts

Prompts for a coordinator that briefs a reviewer or a reviser in a document review loop (`/sc:spec-panel --mode critique`). This file is read on demand and never auto-loaded. `/sc:spec-panel` makes reading it a hard gate before a re-review and before any review or revise brief is written or accepted.

## When to use which prompt

| Situation | Prompt |
|---|---|
| First review of a document | FIRST-REVIEW prompt |
| Any re-review (review 2 or 3) | RE-REVIEW prompt |
| After a review report with open blocking findings, to revise | REVISE prompt |

At `review: 3` with an open blocking finding the loop escalates to the user; no REVISE prompt and no fourth review.

## Values to fill

- `{{CANDIDATE}}`: the revised file under review, the `@file` of the command.
- `{{BASELINE}}`: the `--baseline` file.
- `{{PRIOR}}`: the `--re-review` file.
- `{{N}}`: the number in the prior report's `review: N of 3` header plus 1.
- `{{IDS}}`: the blocking finding ids listed in the report's `Reviser brief`, and only those.

A brief that names the roles differently, or does not name them, does not change them: the table in the re-review core below decides.

## Prompts

### FIRST-REVIEW prompt

Write `review: 1 of 3` once, as the first line of the report.

- First-review brief: "Review the candidate {{CANDIDATE}} (sha256 of the file) against the requirements it states, review 1 of 3. Inspect behavior and the dependencies it touches. Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review; list Medium and minor findings under follow-up candidates. If an input is missing or unreadable, return incomplete. Do not edit the candidate and do not start another review. State what you covered."

### RE-REVIEW prompt

Follow the re-review core below in order (roles, Step 1, review number, self-check), then use this brief.

<!-- core:start -->
| ROLE | FILE VALUE | MEANING |
|---|---|---|
| CANDIDATE | the `@file` of the command | the revised text under review |
| BASELINE | the `--baseline` file | the text as it was before the revision |
| PRIOR | the `--re-review` file | the previous review report |
- **Step 1, the evidence block**, before any finding. Roles are fixed: never infer a role from reading order or from memory. Run `diff -w BASELINE CANDIDATE` and copy the changed lines verbatim under `BEFORE (baseline)` (lines starting `<`) and `AFTER (candidate)` (lines starting `>`). Decide each prior blocking finding marked resolved as resolved or regressed by comparing its defect with the AFTER text only. If the diff is empty, every prior blocking finding stays open.
- **Review number**: N is the number in PRIOR's `review: N of 3` header plus 1. Write `review: N of 3` once, as the first line of the report. Example: a prior `review: 2 of 3` gives `review: 3 of 3`. Use no other header variant.
- **Self-check before the verdict**, when commands can be run: `grep -nF` each quoted AFTER line (without its `>`) in CANDIDATE and each quoted BEFORE line (without its `<`) in BASELINE. If any quote is not found, you swapped roles: redo Step 1. A PASS requires the AFTER text to be consistent with every requirement that depends on it.
<!-- core:end -->

- Re-review brief: "Review the revised candidate {{CANDIDATE}} (sha256 of the file) against {{BASELINE}}, the spec as it was before the revision (sha256 of the file), using prior report {{PRIOR}} (sha256 of the file), review {{N}} of 3, where N is the prior report's review number plus 1. Do Step 1, the evidence block, before any finding. Re-check each prior blocking finding as resolved, open or regressed against the revised candidate. Inspect changed behavior and the dependencies it touches; for inherited text, cite the changed line it depends on. Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review; list Medium and minor findings under follow-up candidates. Record a severe defect you newly discover even if it is older, and say where it came from. If an input is missing or unreadable, return incomplete. Run the self-check before the verdict. Do not edit the candidate and do not start another review. State what you covered."

### REVISE prompt

- Revise brief: "Repair only the blocking findings {{IDS}} in the revised candidate {{CANDIDATE}}. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS."

## Never

Never put "any finding of any severity is FAIL", "assume defects remain", a required number of findings, or "apply all findings" in a brief: a brief may narrow the command's scope but may not widen it or regrade a minor finding as blocking.
