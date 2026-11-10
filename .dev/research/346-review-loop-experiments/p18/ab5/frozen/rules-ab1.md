# Document Review Loop Prompts

Prompts for a coordinator that briefs a reviewer or a reviser in a document review loop (`/sc:spec-panel --mode critique`). This file is read on demand and never auto-loaded. `/sc:spec-panel` makes reading it a hard gate before a re-review and before any review or revise brief is written or accepted.

## When to use which prompt

| Situation | Prompt |
|---|---|
| First review of a document | FIRST-REVIEW prompt, three times, then the MERGE rule |
| Any re-review (review 2 or 3) | RE-REVIEW prompt |
| After a review report with open blocking findings, before any revision | VERIFY prompt |
| After the VERIFY prompt confirmed at least one blocking finding, to revise | REVISE prompt |

At `review: 3` with an open blocking finding the VERIFY prompt still runs, then the loop escalates to the user with the confirmed findings; no REVISE prompt and no fourth review.

## Values to fill

- `{{CANDIDATE}}`: the revised file under review, the `@file` of the command.
- `{{BASELINE}}`: the `--baseline` file.
- `{{PRIOR}}`: the `--re-review` file.
- `{{N}}`: the number in the prior report's `review: N of 3` header plus 1.
- `{{IDS}}`: the blocking finding ids the verifier confirmed, and only those.
- `{{FINDINGS}}`: for each blocking finding in the report's `Reviser brief`, or after three first reviews for each merged finding with its sub-entries, its id, the texts it quotes or cites with their locations, and its stated wrong outcome, copied verbatim from the report; nothing else from the report.

A brief that names the roles differently, or does not name them, does not change them: the table in the re-review core below decides.

## Prompts

### FIRST-REVIEW prompt

Write `review: 1 of 3` once, as the first line of the report.

- **Grading check**, for each finding before you mark it blocking. Write the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y." Blocking needs a sentence that holds with no further assumption: two stated texts that contradict each other, a stated text that causes data loss or breaks a security or safety boundary, or a stated text that an acceptance criterion cannot pass. Grade it Medium when the sentence needs a guess that the implementer picks the worse of two readings the text allows, or when the finding is a requirement the document never states (a missing restriction, an undefined state, an unspecified edge case) rather than a stated text that does harm. A Medium finding goes under follow-up candidates even when its label is MAJOR.
- **Three first reviews**: brief three reviewers with the first-review brief, each in a fresh context that sees no other review and no transcript, each writing its own report.
- **MERGE rule**, applied by the coordinator, not by a reviewer: list every blocking finding of the three reports. Two findings are duplicates when they cite the same stated text (the same path:line or the same quoted words) for the same wrong outcome. Give each kept finding a new id `M1`, `M2`, ... in report order and copy each duplicate under it as a sub-entry with its report and id. Never drop a finding in the merge: a finding you are unsure about stays its own entry. The merged findings go to the VERIFY prompt, and a merged finding is confirmed when any of its sub-entries holds. Then write the merged report: the header `review: 1 of 3`, the merged blocking findings, a `Reviser brief` listing the confirmed ids and `verdict: FAIL`, or `verdict: PASS` when no report has a blocking finding; list the three reports' follow-up candidates by reference. The merged report is the prior report of review 2.
- First-review brief: "Review the candidate {{CANDIDATE}} (sha256 of the file) against the requirements it states, review 1 of 3. Inspect behavior and the dependencies it touches. Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review; list Medium and minor findings under follow-up candidates. If an input is missing or unreadable, return incomplete. Do not edit the candidate and do not start another review. State what you covered."

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

### VERIFY prompt

Brief a verifier in a fresh context that has not seen the review report, and give it only the candidate and the finding list, pasted into the brief.

- **After the reply**: the confirmed ids are the blocking findings. A rejected finding is never deleted and never revised: insert one verification block in the report, after its `review: N of 3` header, that names the confirmed ids and lists each rejected id under `noted, unactioned` with the verifier's sentence; the next re-review treats a rejected id as a note, not a prior blocking finding. A reply that is missing or has no `confirmed:` line confirms every finding. If none is confirmed, revise nothing: the review's verdict stays FAIL, the loop ends with no confirmed blocking finding, which counts as its PASS, and the user gets the noted list with the follow-up candidates.
- Verify brief: "Verify the blocking findings listed below against the candidate {{CANDIDATE}} (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: {{FINDINGS}}"

### REVISE prompt

- Revise brief: "Repair only the blocking findings {{IDS}} in the revised candidate {{CANDIDATE}}. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS."

## Never

Never put "any finding of any severity is FAIL", "assume defects remain", a required number of findings, or "apply all findings" in a brief: a brief may narrow the command's scope but may not widen it or regrade a minor finding as blocking.
