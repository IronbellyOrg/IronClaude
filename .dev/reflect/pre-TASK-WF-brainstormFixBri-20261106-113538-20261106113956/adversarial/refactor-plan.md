# Refactoring Plan: merged reviewer verdict

## Overview
- Base variant: Variant 2 (haiku:qa), combined score 0.897 (V3 0.825, V1 0.788; margin 0.072, no tiebreaker) — `base-selection.md`
- Incorporated variants: V3 (opus:refactorer) for the copy-check mechanism and task-shape checks; V1 (sonnet:analyzer) for the live-check sentence's behaviour (owner notes) and the unverified list
- Orchestrator insertions: Round 2.5 invariant fixes INV-001, INV-002, INV-003 folded into M-01; INV-006 and INV-014 as hardening notes
- Changes planned: 14 (the final finding list M-01..M-14 below), 7 findings dropped by consensus
- Overall risk: Low (the merged artifact is a review verdict; nothing here edits the plan or any repository file)
- The final finding list is decided here so the merge executor does not re-decide it. Every replacement text was tested read-only on 2026-11-06 (see M-01 evidence).

Paths: "plan" = `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/TASK-WF-brainstormFixBri-20261106-113538.md`; "source" = the package's `source.md`; "spec" = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.

## Consolidated verdict
No P1. One P2 (M-01) and twelve P3 items (M-02..M-13), plus one block of owner items carried from the previous review (M-14). The plan copies every brief text byte for byte (E-4) and is executable as written; M-01 adds the acceptance checks the brief's source:34 requires so a mis-copied edit cannot pass.

## Planned Changes

### Change #1 (M-01, P2): whole-text acceptance checks for Tasks 1, 2, 3 and 6
- **Source**: V3 R3-2 (corrected in Round 2, section 3.3), merged with V1 R1-F1 and V2 R2-01; debate C-001 (V3 95%), X-002 (V3 93%); invariant fixes INV-001, INV-002, INV-003
- **Target**: verdict finding M-01; plan Tasks 1 (after plan:46), 2 (after plan:61), 3 (after plan:77), 6 (after plan:145)
- **Rationale**: source:34 says each task's acceptance criteria "must contain a check equivalent to its verifier"; the F-1 verifier (source:45) and the F-3 verifier (source:71) are byte-for-byte checks. Every current AC is a substring pin or a diff shape. E-3 (the per-task reviewer reads explicit instructions) lowers the chance of a paraphrase passing but does not satisfy source:34.
- **Exact AC texts** (one shell, run from the repository root, `S` = this package's `source.md`; INV-001 one path base, INV-014 no hard-coded `to-do/` path):
  - Task 1: "With `S` set to this package's `source.md` and the command run from the repository root, `X=$(sed -n '231s/.*with: "\(.*\)" Task 1 AC.*/\1/p' "$S")` is non-empty, `grep -cxF -- "$X"` on this plan prints 1, and `grep -cF -- "$X" src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` prints 1."
  - Task 2: "With `S` as in Task 1, `X=$(sed -n '232s/.*31): "\(.*\)" .grep.*/\1/p' "$S")` is non-empty, `grep -cxF -- "$X"` on this plan prints 1, and `grep -cxF -- "$X" src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` prints 2."
  - Task 3: "With `S` as in Task 1, `X=$(sed -n '233s/.*bullet: "\(.*\)" Leave.*/\1/p' "$S")` is non-empty, `grep -cxF -- "$X"` on this plan prints 1, and `grep -cF -- "$X" src/superclaude/commands/brainstorm.md` prints 1."
  - Task 6: "With `S` as in Task 1, `X=$(sed -n 223p "$S")` and `Y=$(sed -n 219p "$S")` are non-empty, `grep -cxF` on this plan prints 1 for each, and `grep -cF` against `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` prints 1 for each."
  - Task 6 body, appended to the Necessary-deviation paragraph (plan:131): "The whole-text check in the acceptance criteria is required by the brief's rule that each correction's verifier has an equivalent check; it is not one of the pins correction F-7 lists."
- **Evidence (run read-only 2026-11-06 from the repository root)**: extraction lengths 412, 261, 361, 450, 1210; `grep -cxF` on the plan prints 1 for each; each target prints 0 today, so every new AC fails before the edit. The Task 2 regex uses `.grep` instead of a backtick (INV-003). An empty extraction fails loudly (INV-005); the non-empty and plan-line self-check catches a moved source line (INV-002).
- **Risk**: Low (additive ACs). Rollback: drop the four ACs.

### Change #2 (M-02, P3): copy residual risks 1, 2 and 4 verbatim
- **Source**: V2 R2-05; debate C-005 (V2 95%), X-001 (V2 93%), C-012 (V2 93%)
- **Target**: plan:134, :135, :137
- **Change**: replace each bullet's text with the brief's text after its number: plan:134 with source:240 ("A `/sc:analyze` call made without the nested `--report-dir` (a broken propagation, itself a defect) is not seen, so its missing folder passes. Related: INV-022 (no live check can force the analyze route)."), plan:135 with source:241, plan:137 with source:243. Plan bullets stay "- " bullets (the workflow gate forbids numbered lines).
- **Verifier**: for N in 240, 241, 243, the text of source line N after "N. " occurs in the plan (`grep -cF` prints 1); plan:136 and :138 already equal source:242 and :244 after the number.
- **Risk**: Low.

### Change #3 (M-03, P3): record the extra negative pin as a deviation, keep it
- **Source**: V2 R2-02 (detection), V1 and V3 (keep it); debate C-002 (V2 90%)
- **Target**: plan:131 (Task 6 Necessary-deviation paragraph)
- **Change**: append "Task 6's second acceptance criterion also checks that the old trigger wording ``a `Skill`, `Agent` or `Task` tool call`` is gone; this goes beyond the pins correction F-7 lists, on purpose, because the positive pins are shared by the old and the amended sentence."
- **Verifier**: plan:131 names the extra check and its reason; plan:144 is unchanged.

### Change #4 (M-04, P3): F-14 absence check without the literal
- **Source**: V2 R2-04 (detection), V1 Round 2 fix; debate C-004 (V2 85%)
- **Target**: plan:45
- **Change**: replace `and does not contain "only for a nested command that ran".` with ``and a regular-expression search for `only for a nested command that r[a]n` finds nothing in it.``
- **Verifier**: Task 1 no longer contains the literal "only for a nested command that ran" (`grep -cF` on plan:31-47 prints 0) and still carries the absence check. Tested: the regex `only for a nested command that r[a]n` matches the old literal.

### Change #5 (M-05, P3): Task 3 diff-shape AC
- **Source**: V3 R3-3; debate C-014 (V3 85%)
- **Target**: Task 3 ACs (after plan:77)
- **Change**: add "`git diff --stat -- src/superclaude/commands/brainstorm.md` shows one line changed (one insertion, one deletion)."

### Change #6 (M-06, P3): Task 5 HEAD guard and Task 4 claim
- **Source**: V3 R3-4; debate C-015 (V3 88%)
- **Target**: plan:111 and plan:95
- **Change**: plan:111 append ", and `git cat-file -e HEAD:src/superclaude/commands/brainstorm.md` exits 0"; plan:95 replace "which shows the pins fail on the pre-change text" with "which shows the shared directory pins fail on the pre-change text".

### Change #7 (M-07, P3): exit status in the Task 7 logs
- **Source**: V3 R3-5 narrowed; debate C-010 (V3 88%)
- **Target**: plan:153
- **Change**: after "save the output of `git status --porcelain` to `./artifacts/status-after.txt`." insert "Append the line `exit=<status>` after each command's output in its log."
- **Note**: the lint-baseline half is dropped: `make lint` exits 0 today (E-2).

### Change #8 (M-08, P3, review artifact): verifier rows in the coverage matrix
- **Source**: V2 R2-06; debate C-006 (V2 90%)
- **Target**: this review's report, not the plan
- **Change**: the report carries V2's per-correction table (F-1..F-17: 14 literal pass, 3 literal fail, all three fails explained by M-03, M-04 and M-12) as the verifier-level coverage record.

### Change #9 (M-09, P3, owner item, top of the owner list): step 5 condition 2 scope
- **Source**: V1 R1-F6; debate C-011 (V1 92%), X-003 (V1 88%)
- **Claim**: the amended sentence accepts the analyze `Skill` call "in one of its subagent files" (plan:128); the skill runs enrichment sources "in parallel via `Task` agents" (SKILL.md:183); spec 7.2 step 5 condition 2 requires the command call to be a top-level message (spec:296), and the lc10 record applied condition 2 to nested calls (lc10-result.md:13). A checker that follows lc10 fails a correct run whose nested analyze call sits in a subagent.
- **Owner action**: decide that condition 2 applies to the command under test only, and record it for the P2 live-plan author (and, if wanted, as residual risk 6 in brief Part 4). No plan or spec edit in this plan.

### Change #10 (M-10, P3, owner item): refusal has no recorded marker
- **Source**: V1 R1-F3; debate C-008 (V1 88%), X-003
- **Claim**: `/sc:analyze` prints a refused directory "in chat only" (`src/superclaude/commands/analyze.md:97`), so the "did not refuse that directory" clause is judged from chat text; a checker that misses it requires a folder that was never written. With M-09 this qualifies the brief's "no known false FAIL on a correct run" (source:239, plan:133). The `--report-dir` match is literal (a relative path or a missing trailing slash is not matched: false PASS).
- **Owner action**: decide whether brief Part 4 gains residual risks 6 and 7 (these two paths) and a narrowed lead-in; the plan copies Part 4 and cannot change it alone.

### Change #11 (M-11, P3, owner item): "only when" reads as a necessary condition
- **Source**: V1 R1-F2; debate C-007 (V1 92%)
- **Claim**: "a `nested/analyze-<n>/` directory is required ... only when ..." (source:219) does not say the folder is required when every condition holds; the intended reading is "exactly when".
- **Owner action**: optional wording change in brief Part 4 ("exactly when"); otherwise none.

### Change #12 (M-12, P3, owner item): F-12 verifier contradicts F-3
- **Source**: V2 R2-03; debate C-003 (V2 93%)
- **Claim**: F-12's verifier says every pin added under F-3 contains `no nested directory and no nested contract` (source:161), but F-3 also requires the separate ``only by a `/sc:analyze` call`` pin (source:63). The plan correctly keeps both pins.
- **Owner action**: none needed for this plan; note for future briefs.

### Change #13 (M-13, P3, hardening notes on M-01)
- **Source**: invariant probe INV-006, INV-014
- **Notes**: `grep -c` counts lines, not occurrences (a text pasted twice on one line still prints 1; the per-task reviewer sees the diff); do not hard-code `.dev/tasks/to-do/` in an AC, because the package moves to `done/` after the final review.

### Change #14 (M-14, P3, carried owner items from the previous review)
- **Source**: Tier 1 card F-4; previous report M-12, M-13, M-14, INV-020, INV-021
- **Items**: research enrichment from P2 stays an open conflict (plan:26); no pointer for the P2 author to the new 7.2 step 4 sentence (INV-020); the routing bullet's "with this tier's `quality_tier`" against a timeout's `skipped` (plan:54); the 2.1 companion sentence's installed twin `WORKER-CONTRACT.md` is not edited.

## Base weaknesses addressed
| Issue | Better variant | Fix |
|---|---|---|
| V2 tests presence, not behaviour of the live-check sentence | V1 | M-09, M-10, M-11 |
| V2's R2-01 had no runnable mechanism | V3 | M-01 (corrected mechanism plus INV fixes) |
| V2's R2-02 and R2-04 fixes would remove regression guards | V1, V3 | M-03 keeps the pin; M-04 keeps the check with a regex class |

## Changes NOT Being Made (with rationale)
| Diff point / finding | Proposal | Rationale |
|---|---|---|
| C-009: R1-F4, R3-6 | Guard that the six files are clean before Task 1 | Void today (E-1); plan:33 records the start state; a dirty file would make a diff-shape AC fail loudly |
| C-010 half: R1-F5, R3-5 baseline | Lint baseline / outside-six-files waiver | `make lint` exits 0 today (E-2) |
| C-012: R1-F7, R3-8 | Narrow residual risk 4 | Risk 4 is conditioned on a missing or ambiguous session file and spec:300 then blocks PASS; it is true as written |
| C-013: R3-1 | Widen Task 7's status exemption | Void: E-1 meets the finding's own void condition |
| C-016: R3-7 | Reword the Task 7 "writes only the logs" sentence | source:169 mandates it and source:171 verifies it; plan:153 already names the exceptions |
| A-001 | "QA checks only the AC" | Refuted by E-3; M-01 rests on source:34 instead |

## Risk Summary
| Change | Risk | Impact | Rollback |
|---|---|---|---|
| M-01 | Low | Four added ACs; fails red before the edit, green after an exact copy | Drop the ACs |
| M-02..M-07 | Low | Wording and check hardening | Revert the line |
| M-08..M-14 | None | Notes only | n/a |

## Review Status
- Approval: auto-approved (non-interactive)
- Timestamp: 2026-11-06T12:24:00Z
