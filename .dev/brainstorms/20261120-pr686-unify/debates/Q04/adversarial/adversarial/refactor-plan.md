# Refactoring Plan

## Overview
- Base: Variant 1 (`/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/adversarial/adversarial/variant-1-original.md`)
- Incorporated from: Variant 2 (`variant-2-original.md`, same folder)
- Planned changes: 7; changes not made: 4
- Overall risk: Low to Medium (text only; no code is touched)
- Merged output path: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/adversarial/merged-output.md`

## Planned Changes

### Change #1: Rewrite the Claim and Mechanism so fix-round pushes are covered by the run line (resolves X-001; C-002; C-001)
- Source: Variant 2, Claim and Mechanism 2; Variant 1 Risks bullet 1
- Target: Variant 1 "Claim" and "Mechanism" items 1, 2, 3
- Approach: replace
- Rationale: both advocates agreed (Round 1, C-002 Hybrid 90%, X-001 Hybrid 85%): the typed `/sc:pr-submit --monitor 3` line, or the Full Submit field for that issue, is the person's go for that one run's first push, PR and fix-round fast-forward pushes. Sha-bind only where the commit exists when the go is given: a push after a rebase (old and new sha), and the merge.
- Risk: Medium (changes the central rule)

### Change #2: Add the end of a go (C-004)
- Source: Variant 1 Mechanism 3; Variant 2 "What it costs" (no end event)
- Target: Variant 1 "Mechanism" item 3
- Approach: replace
- Rationale: C-004 Hybrid 80%. A run-level go ends at the run's terminal status, when the PR is merged or closed, or when the branch head moves outside the run; PR 368 is the reason (memory `pr-submit-check-pr-open-before-push`, not re-verified).
- Risk: Low

### Change #3: Add the mechanical fence as the stated condition of the run go (U-006)
- Source: Variant 2 cited facts 3 and 4; `SKILL.md:262, 342-348`; `pr-submit.md:121`
- Target: new "Mechanism" item after item 1
- Approach: insert
- Rationale: the run go is not a blank check: one fix commit per cycle, `push_range_mismatch` halt, fast-forward only, no force push, no push to the default or protected branch, `push_count <= max_rounds + 1` (hard cap 5). A test can check each of these.
- Risk: Low

### Change #4: State the classes outside the run (C-003, U-002)
- Source: Variant 1 Mechanism 2 and Risks
- Target: new "Mechanism" item
- Approach: insert
- Rationale: first push without `/sc:pr-submit` (a manual or coordinator push), a revert, a rebase (a force push), a new run on the same PR, and a merge each need a new typed go; the tool itself never rebases or force-pushes.
- Risk: Low

### Change #5: Narrow Full Submit and keep the worker route closed (C-005, C-007, X-002, A-003)
- Source: Variant 1 cited facts 2 and 9; Variant 2 U-008
- Target: Variant 1 "Mechanism" item 4 and "Cited facts"
- Approach: replace
- Rationale: the Full Submit field value (Pipeline = Full Submit plus the `Approved` field) is the person's go for that issue's first push, PR and the loop pushes of the one `/sc:pr-submit --monitor 3` run it starts, in a top-level session; it never covers a merge, force push, branch deletion or any other push. ADD1's worker route stays rejected (D06 item 5; WC:23, WC:244). The amendment of WC:245 must be worded so it is not an "earlier pre-authorization" (U-008).
- Risk: Medium

### Change #6: Replace "What it costs" and "What it risks" with the agreed accounting (C-008, X-003, U-004, U-005, U-007)
- Source: Variant 1 and Variant 2 costs and risks
- Target: "What it costs", "What it risks"
- Approach: restructure
- Rationale: cost now one go per run (not per push), up to 5 prompts removed; risks now: a script can type the run line (A-001, D06 INV-003); a worker script's own push is covered by no go (SEC-13, D:117); head moved outside the run (A-005); sha-bound push is OURS extended and not in D06 or Q01 (X-003); a bad fix push is caught only at the merge go, so the merge go stays sha-bound (U-007).
- Risk: Low

### Change #7: Add the testable one-sentence rule and the rows to change (the topic's deliverable)
- Source: both variants; debate outcome
- Target: new final section "Resulting rule and rows"
- Approach: append
- Rationale: both rubrics scored NOT MET on success criteria. The rule must be checkable. Name rows: SPEC section 8 rules and the flow sentence at line 124 ("a typed go precedes every push and merge"), FR-32, SEC-15 (the WC:245 amendment text), 13.2 guard probe row, SEC-01 untouched, and add a new row for the end of a run go.
- Risk: Medium

## Changes NOT Being Made

| Diff point | Non-base approach | Why the base approach stands |
|---|---|---|
| C-001/C-004 (sha-bound fix pushes) | Variant 1 base says each fix push needs a sha-bound go | The base is replaced here; the sha pin stays only for rebase and merge. (Listed so a reader sees the base text was changed on purpose.) |
| C-003 | Variant 2: a go until merge also covers revert and rebase | Rejected: changes the commit set the person approved; both advocates agreed (C-003 Variant 1, 90%) |
| C-007, X-002 | Variant 2: ADD1 worker runs `/sc:pr-submit` | Rejected: WC:23, WC:244, D06 item 5; Variant 2's advocate conceded |
| C-004 | Variant 2: the go lasts "until merge" | Rejected: no end event, PR 368; Variant 2's advocate conceded |

## Risk Summary

| Change | Risk | Impact if wrong | Rollback |
|---|---|---|---|
| #1 | Medium | Run line read as a standing grant | Restore Variant 1 Mechanism 2 text |
| #5 | Medium | WC:245 amendment read as pre-authorization | Reword per U-008 |
| #7 | Medium | A row named wrongly | Fix the row id in the verdict |
| #2, #3, #4, #6 | Low | Wording only | Edit text |

## Review Status
Auto-approved (non-interactive, `--unattended`). Timestamp 2026-11-20.
