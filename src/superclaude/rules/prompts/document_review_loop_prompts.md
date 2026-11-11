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

- **Grading check**, for each finding before you mark it blocking. Write the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y." Blocking needs a sentence that holds with no further assumption: two stated texts that contradict each other, a stated text that causes data loss or breaks a security or safety boundary, or a stated text that an acceptance criterion cannot pass. Grade it Medium when the sentence needs a guess that the implementer picks the worse of two readings the text allows, or when the finding is a requirement the document never states (a missing restriction, an undefined state, an unspecified edge case) rather than a stated text that does harm. A Medium finding goes under follow-up candidates even when its label is MAJOR.
- First-review brief: "Review the candidate {{CANDIDATE}} (sha256 of the file) against the requirements it states, review 1 of 3. Inspect behavior and the dependencies it touches. Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review; list Medium and minor findings under follow-up candidates. If an input is missing or unreadable, return incomplete. Do not edit the candidate and do not start another review. State what you covered."
- **Findings block**: end the report with the findings block described under "Findings block" below, one line per finding, blocking or not.

### RE-REVIEW prompt

Follow the re-review core below in order (roles, Step 1, review number, self-check), then use this brief.

| ROLE | FILE VALUE | MEANING |
|---|---|---|
| CANDIDATE | the `@file` of the command | the revised text under review |
| BASELINE | the `--baseline` file | the text as it was before the revision |
| PRIOR | the `--re-review` file | the previous review report |
- **Step 1, the evidence block**, before any finding. Roles are fixed: never infer a role from reading order or from memory. Run `diff -w BASELINE CANDIDATE` and copy the changed lines verbatim under `BEFORE (baseline)` (lines starting `<`) and `AFTER (candidate)` (lines starting `>`). Decide each prior blocking finding marked resolved as resolved or regressed by comparing its defect with the AFTER text only. If the diff is empty, every prior blocking finding stays open.
- **Review number**: N is the number in PRIOR's `review: N of 3` header plus 1. Write `review: N of 3` once, as the first line of the report. Example: a prior `review: 2 of 3` gives `review: 3 of 3`. Use no other header variant.
- **Self-check before the verdict**, when commands can be run: `grep -nF` each quoted AFTER line (without its `>`) in CANDIDATE and each quoted BEFORE line (without its `<`) in BASELINE. If any quote is not found, you swapped roles: redo Step 1. A PASS requires the AFTER text to be consistent with every requirement that depends on it.

- Re-review brief: "Review the revised candidate {{CANDIDATE}} (sha256 of the file) against {{BASELINE}}, the spec as it was before the revision (sha256 of the file), using prior report {{PRIOR}} (sha256 of the file), review {{N}} of 3, where N is the prior report's review number plus 1. Do Step 1, the evidence block, before any finding. Re-check each prior blocking finding as resolved, open or regressed against the revised candidate. Inspect changed behavior and the dependencies it touches; for inherited text, cite the changed line it depends on. Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review; list Medium and minor findings under follow-up candidates. Record a severe defect you newly discover even if it is older, and say where it came from. If an input is missing or unreadable, return incomplete. Run the self-check before the verdict. Do not edit the candidate and do not start another review. State what you covered."
- **Findings block**: end the report with the findings block described under "Findings block" below: one line per finding you report and one prior line per prior blocking finding.

### REVISE prompt

- Revise brief: "Repair only the blocking findings {{IDS}} in the revised candidate {{CANDIDATE}}. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS."
- **Fix map**: end your output with the fix map described under "Fix map" below.

### Findings block

The last section of every review report is `## Findings block`: one fenced code block whose info string is `findings-v1`, holding one JSON object per line and nothing else. A report with no finding has an empty block.

- Finding line: `{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "<text copied exactly from the candidate>", "anchor2": "<optional second exact quote>", "refs": ["AC-0.4"], "claim": "<one sentence naming the wrong outcome>"}`. `severity` is CRITICAL, MAJOR or MINOR. `blocking` is true only for a finding that passes the grading check. `category` is one of contradiction, unpassable-check, data-loss, safety, missing-requirement, other. `anchor` is 12 to 200 characters copied exactly from the candidate: the text that is wrong; for a contradiction `anchor2` is the other side. `refs` lists the requirement ids and section numbers the finding rests on.
- Prior line, re-reviews only: `{"prior": "L3", "status": "resolved"}`, with status resolved, open or regressed, one line per prior blocking finding id.
- The block restates the findings discussed above it and adds none. The verdict line stays the reviewer's verdict.

### Fix map

The reviser ends its output with `## Fix map`: one fenced code block whose info string is `fixmap-v1`, one JSON object per line, `{"id": "L3", "action": "applied", "reason": "<one sentence>"}`, with action applied or rejected, one line per blocking id in the brief.

### Review panel

Run each review with the reviewers that `superclaude review panel resolve --run-id <loop id> --kind <first or re-review>` prints (a panel for a first review, one reviewer for a re-review by default): each in a fresh context with the same brief, none seeing another's report or transcript. Merge the reports with `superclaude review merge`, also for a single reviewer; its merged report and the ledger it keeps give the verdict and the Reviser brief ids, and only that script changes a finding's status. If the `superclaude` command is not installed, run one reviewer and say so in the loop summary.

## Never

Never put "any finding of any severity is FAIL", "assume defects remain", a required number of findings, or "apply all findings" in a brief: a brief may narrow the command's scope but may not widen it or regrade a minor finding as blocking.
