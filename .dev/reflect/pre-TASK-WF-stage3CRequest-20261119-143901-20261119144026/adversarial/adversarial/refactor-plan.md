# Refactoring Plan: Merge into Base (Variant 3)

## Overview
- Base: Variant 3 (reviewer card 3, refactorer lens; `variant-3-original.md`)
- Incorporating strengths from: Variant 1 (card 1, analyzer), Variant 2 (card 2, qa), and the Round 2.5 invariant probe (`invariant-probe.md`)
- Planned changes: 13 (Change 13 added after the first merge pass; see its entry)
- Risk level: Medium overall (rows 1-3 are rewritten in place; the grades do not change)
- Target output: ONE merged verdict card at `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/reflect/pre-TASK-WF-stage3CRequest-20261119-143901-20261119144026/adversarial/merged-output.md`, in the reviewer-card shape of `src/superclaude/agents/reflect-reviewer.md` lines 73-99: Deviations table with grade-prefixed "What diverged" cells, Adherence summary, Notes. Two parts are added to that shape: a "Merged verdict" header line, and a "Per-finding agreement" table with the columns finding, cards that raised it, final grade, why.
- Grading rule for every row: `## Review severity rule`, agent:117-123. Blocking only for Decision / Missing / Safety, with the affected action named in the same cell. A real defect that nothing named rests on is Medium. A defect of form only is a Note. HIGH/MEDIUM/LOW is a label, not the grade. A spec-inherited check or wording is not a plan deviation (agent:123 applies the grading to rows of the Deviations table; consensus C-003/X-001 and INV-013).
- Final grades fixed by the debate (do not change them in the merge): row 1 `Blocking (Missing)`; row 2 `Blocking (Missing)`, with Decision also holding; row 3 `Medium:`; row 4 `Note:`; new row 5 `Note:`. Merged verdict: **FAIL**, because two Blocking findings remain open.

## Planned Changes

### Change 1: Merged verdict line, verdict field and Next line (from Variant 2)
- **Source**: Variant 2, header `**Verdict**: FAIL — two blocking omissions` (variant-2:12) and Notes "**Next:** resolve findings 1 and 2 before execution" (variant-2:35)
- **Target**: Base, top of the document (insert) and header block (insert a `**Verdict**:` field); last Notes bullet (append the Next line)
- **Rationale**: S-001, unanimous over both rounds, 95%. agent:120: "Only blocking findings produce FAIL."
- **Integration point**: put the line `**Merged verdict: FAIL** — 2 Blocking (rows 1 and 2), 1 Medium, 2 Note` directly under the H1. The Next line names rows 1 and 2 and the fix wording of Changes 3 and 4.
- **Risk**: Low, additive
- **Concrete anchors preserved**: "FAIL"; "two blocking" → "2 Blocking (rows 1 and 2)"

### Change 2: Grounding header with full paths once, then short cites (from Variant 1)
- **Source**: Variant 1, header lines `Spec:` / `Plan:` with absolute paths (variant-1:13-14)
- **Target**: Base header block (insert after `**Grounding root**`)
- **Rationale**: S-002, unanimous in Round 2, 95% (V2 advocate conceded; agent:86-87 example uses `spec.md:88`).
- **Integration point**: add `Spec:` and `Plan:` lines with the two absolute paths. Add a one-line legend: `plan:N`, `source.md:N`, `agent:N` = `src/superclaude/agents/reflect-reviewer.md`, `matrix:N` = this run's `artifacts/coverage-matrix.md`, `README.md:N` = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md`. Set `**Reviewer persona**` to "merged: analyzer (card 1), qa (card 2), refactorer (card 3, base)". Change the frontmatter-like lines to `persona: merged`, `model_class: sonnet, haiku, opus (cards 1-3)`, `agent_type: reflect-reviewer`.
- **Risk**: Low, additive
- **Concrete anchors preserved**: both absolute paths verbatim from variant-1:13-14

### Change 3: Row 1 (branch) facts and fix route (base row 1, modified; from debate Round 2 and INV-001, INV-002, INV-003)
- **Source**: Base row 1 (variant-3:17); r2-v3 New evidence 1; invariant-probe INV-001, INV-002, INV-003; orchestrator spot-check (debate-transcript Round 2.5)
- **Target**: Base Deviations row 1 (modify, in place)
- **Rationale**: C-001 and A-001 (both 95%). INV-003 is the only HIGH UNADDRESSED invariant. The cards' claim that added plan text alone fixes the row ("No task steps need to change", variant-1:47) is false on the in-place route. The row's fix text must name the route.
- **Integration point**: keep the cell's opening `Blocking (Missing):` and the affected action, "choosing the branch that Task 1's two edits and the later PR land on". Keep the base's sentence that every acceptance line still passes on the current branch. Add these:
  - The checkout `feature/blocker-classification-stage3b` is 5 commits ahead of and 49 behind `origin/master`. The check is against the local ref `a0dd57777`, with no fetch.
  - Fix: add a constraint beside the owner-go condition at plan:19: run on a fresh branch made from `origin/master`. Name the route:
    - (a) A new Orca worktree from `origin/master`. The package folder (untracked), the staged `stage3c-request.md` and the uncommitted ledger edit (README.md:22) must be carried into it and staged there. `/sc:implement` needs the plan inside the current checkout (INV-002).
    - (b) Switching this worktree in place. Delete the stale `.claude/` dev copies before `make sync-dev`. `origin/master` deletes 53 source primitives whose gitignored `.claude/` copies would remain (for example `.claude/skills/prd`, `.claude/commands/sc/build.md`). `make sync-dev` never deletes. `make verify-sync` exits 1 on any `.claude` skill with no `src` source (Makefile:188-200, :348-352). So plan:59 "`make verify-sync` passes" would fail on a correct edit (INV-003).
  - Evidence cell: add `INF-001 (matrix:32-35)`. Keep `source.md:3` and the plan-has-no-branch text.
- **Risk**: Medium, modifies the base row; the grade is unchanged
- **Concrete anchors preserved**: `origin/master`; `feature/blocker-classification-stage3b`; "5 ahead / 49 behind"; `a0dd57777`; 53 deleted primitives; plan:19; plan:59; Makefile:188-200, :348-352; INF-001

### Change 4: Row 2 (known limits) wording, unit ids and fix (base row 2, modified; from Variants 1 and 2 and INV-011, INV-014)
- **Source**: Base row 2 (variant-3:18). Variant 2 row 2 limit-3 wording "a judgment affecting digits and apostrophes rather than lowercase letters" (variant-2:19). Variant 1 row 2 "where source.md:69 calls one of them a judgment" (variant-1:21). Variant 2 Notes on INF-036 (variant-2:32). invariant-probe INV-011, INV-014, INV-015, INV-017.
- **Target**: Base Deviations row 2 (modify, in place)
- **Rationale**: C-002 and X-003 (90%). Calibration 2's Medium objection (reviewer-2-calibration.yaml) was rejected in both rounds: Missing has no consequence test (agent:119), and the calibrator's own "fix before the owner's go" names the step that rests on the text. Decision also holds, because plan:21 calls "two real gaps" a fact for findings of which one is a judgment (source.md:69). The other finding was ruled a Blocker by the owner (README.md:28, INV-014).
- **Integration point**: start the cell with `Blocking (Missing):`. Add "Decision also holds:" and the plan:21 sentence, worded "one of the two" (V1). Use V2's wording for limit 3: "it changes the order of digits and apostrophes, not of lowercase letters" (source.md:69). Keep the base's affected action: "the owner's go decision and the owner's later reading of the B/E re-runs". Note that the plan is the only carrier, since README.md:64 cut per-stage owner summaries (A-002, INF-015). Fix text, which must have both parts (INV-011):
  - (a) Add the three limits from source.md:67-69 to the plan's summary, its Goal and "Why this package exists" bullets (plan:15, :21-22).
  - (b) Reword plan:21 so that "two real gaps" no longer states the codepoint-order finding as fact.
  - Evidence cell: add `INF-034, INF-036, INF-037, INF-038 (matrix:83-86)`. Add the V2 point that the INF-036 containment match is not semantic coverage.
- **Risk**: Medium, modifies the base row; the grade is unchanged
- **Concrete anchors preserved**: source.md:65-69 (three limits, verbatim content: examples stay and B result does not depend on them; one sonnet model, three reviewers per arm, one scorer, no second reader, coverage hints in the briefs; codepoint-order judgment); plan:15, :19, :21, :22; README.md:28, :64; INF-034/036/037/038

### Change 5: Row 3 (byte identity) scope, impact and fix (base row 3, modified; from Variant 1 U-001 and INV-005, INV-006, INV-010)
- **Source**: Base row 3 (variant-3:19); Variant 1 row 3 sub-claim U-001 (variant-1:22); r2-v3 New evidence 3; invariant-probe INV-005, INV-006, INV-010
- **Target**: Base Deviations row 3 (modify, in place)
- **Rationale**: C-003 and X-001 (85%). It is a deviation only because the plan dropped the spec's sha256 (INF-008; matrix:39, :87). The partial greps (plan:44 = source.md:39-41) and "passes with the two new needles" (plan:46 = source.md:43) are inherited word for word, so they only explain the impact. It is Medium because restoring the hash changes no named acceptance check (agent:120).
- **Integration point**:
  - Start the cell with `Medium:`.
  - Replace "the plan drops the spec's way of checking byte identity" (V3 conceded the overstatement at r2-v3.md:20) with "plan:22 keeps 'copied byte for byte ... never retype it' but drops the spec's sha256 `7696a2b21601ff914d7651085125ef4188238640998c0599907555c760ec0ed8` (source.md:24)".
  - Impact: the inherited greps pin only the opening, the last sentence and the join. `grep -c` counts lines, and the whole bullet is one line (agent:122). So a wrong token in the middle, or the passage inserted twice on that line, still prints 1 (INV-005). The inherited "passes with the two new needles" does not check that the needles were added, because the tuple at `tests/skills/test_review_severity_rule.py:216-227` holds the ten existing needles and pytest passes either way (U-001, INV-006).
  - Fix: add a whole-file `sha256sum` check against the hash above. It is valid only while the base agent still equals `origin/master`'s, base hash `ed911b7c…d183312c6`; otherwise fall back to the plan:45 diff check (INV-010). Add one `grep -c` per new needle in the test file.
  - Name the variant path `.dev/stage3c-variants/brainstorm/reflect-reviewer.md` as where the hash comes from, not as a check, because `.dev/stage3c-variants/` is not tracked on `origin/master` (INV-002).
  - Keep the base's verified sentence that the variant's line 122 equals the agent's line 122 with the passage inserted.
- **Risk**: Medium, modifies the base row; the grade is unchanged
- **Concrete anchors preserved**: full sha256 from source.md:24; base hash `ed911b7c…d183312c6` (truncated, as given in r2-v3.md:31); agent:122; test:216-227 (10 needles); plan:22, :44, :45, :46; source.md:24, :39-43; INF-008

### Change 6: Keep row 4 (Authorized expansion, Note) unchanged (base original)
- **Source**: Base row 4 (variant-3:20)
- **Target**: Base Deviations row 4 (preserve)
- **Rationale**: U-004. Calibration 3 agrees. INV-004 checked the plan:61 guard against the `tests/` edit and Task 2, and the guard holds.
- **Integration point**: none. Add `INV-004` to the evidence cell only.
- **Risk**: Low
- **Concrete anchors preserved**: plan:61, :37, :60; agent:5-8; Makefile:109-163 / :126-130

### Change 7: New row 5, the plan-added "83 tests" claim, Note (from base Notes, reworded with Variant 2's and the debate's evidence)
- **Source**: Base Notes "Not verified" (variant-3:37); r1-v2 / r2-v1 / r2-v3 evidence; INV-008; INV-013
- **Target**: Base Deviations table, new row 5 (insert). Remove the matching phrase from Notes.
- **Rationale**: C-006 (90%). INV-013: plan:39 is plan-added text, not inherited, so it is a plan-side row. It is a wrong citation on a true statement, so a Note (agent:120).
- **Integration point**: set Category Drift and label LOW. The cell starts `Note:`: "plan:39 says the four test files passed, 83 tests, with the passage swapped in. The only 83-passed record (`.dev/stage3c-variants/brainstorm-deep/DESIGN.md:1-3, :24`) is for the carry-scope variant. The chosen variant's `TEST-PLAN.md:5` says pytest was not run. On `origin/master` the severity test file collects at least 6 fewer cases. No acceptance line uses 83 (plan:46-47, :60), so do not compare the observed count with it."
- **Risk**: Low, additive
- **Concrete anchors preserved**: "83"; DESIGN.md:1-3, :24; TEST-PLAN.md:5; "at least 6 fewer cases"

### Change 8: Keep the spec-inherited items in Notes as non-deviations (base Notes (a) and (b), modified; INV-013, INV-009)
- **Source**: Base Notes (a) and (b) (variant-3:38); Variant 1 row 4 and its Note paragraph (variant-1:23, :25); INV-009, INV-013
- **Target**: Base Notes (modify)
- **Rationale**: C-004, C-005, X-002 (Note, 90-95%). INV-013 says the C-003 rule must apply to all inherited items. plan:41 = source.md:34 and plan:44 = source.md:39 (with the same escaped backticks), so neither is a plan deviation and neither goes in the table.
- **Integration point**: label both bullets "Note, spec-inherited, not a plan deviation". In (b) keep the six extra files. Add from INV-009 that the two extra test files mention the agent only as text (`tests/skills/test_worker_contract.py:2923`, `tests/unit/test_cli_install.py:63`), and that `git grep -l` names the same 13 files on `origin/master`.
- **Risk**: Low
- **Concrete anchors preserved**: plan:41, :44; source.md:34, :39; the 4 YAML fixture paths; test_worker_contract.py:2923; test_cli_install.py:63; 13 files

### Change 9: Coverage-matrix inventory Note (from Variant 2)
- **Source**: Variant 2 Notes first bullet (variant-2:31)
- **Target**: Base Notes (append)
- **Rationale**: U-002 (Low value, but uncontested). It is a Note about this run's coverage matrix, not about the plan, and it consumes no unit.
- **Integration point**: append it as "Note, non-gating", keeping V2's citations source.md:3, matrix:32-35 and plan:20.
- **Risk**: Low, additive
- **Concrete anchors preserved**: source.md:3; matrix:32-35; plan:20

### Change 10: Update "Not verified" and close U-005 and PR #605 (base Notes, modified; from the debate)
- **Source**: Base Notes "Not verified" (variant-3:37); r2-v3 Response 3 and 4; INV-001; INV-016
- **Target**: Base Notes (modify)
- **Rationale**: Round 2 verified both items that the base left open.
- **Integration point**: in "Checked with no finding", replace the U-005 item with these facts:
  - `git diff --stat origin/master -- src/superclaude/agents/reflect-reviewer.md` is empty.
  - The variant differs from the agent only at `122c122`.
  - The variant's sha256 equals source.md:24.
  - So the anchor and the hash hold on a fresh branch from the local `origin/master`.

  Replace "Whether PR #605 is merged" with "PR #605 is merged: `e3e9d636a` on `origin/master`", and note that the stage 3b package is in the done folder on `origin/master` (INV-016). Keep "no tests were run". Add "git checks are against the local ref `a0dd57777`, not fetched". State where the merged card's facts come from: the cards, then the debate rounds, then the invariant probe.
- **Risk**: Low
- **Concrete anchors preserved**: `e3e9d636a`; `a0dd57777`; `122c122`; source.md:24 hash

### Change 11: Adherence summary recount (from Variant 2's INF-id method, corrected in Round 2; INV-007)
- **Source**: Variant 2 Adherence summary (variant-2:23-27); r2-v2 and r2-v3 S-003; INV-007
- **Target**: Base Adherence summary (replace)
- **Rationale**: S-003 (90%). Units are counted by coverage-matrix id, so each fix can be checked unit by unit.
- **Integration point**:
  - "Spec units audited: 43 (coverage-matrix INF-001 to INF-043, matrix:14)".
  - "Fully adherent: 37".
  - "Not carried: INF-001 (row 1); INF-034, INF-036, INF-037, INF-038 (row 2); INF-008 (row 3; its semantic note is filed under INF-009 at matrix:87)".
  - "Authorized expansion: 1 | Necessary deviation: 0 | Drift: 4 (rows 1, 2, 3, 5) | Regression: 0".
  - "Rows 4 and 5 consume no unit".
  - Set the header to `**Total deviations**: 5 (2 Blocking, 1 Medium, 2 Note)`.
- **Risk**: Medium, replaces a base section
- **Concrete anchors preserved**: 43; 37; the six INF ids; matrix:14, :39, :87, :91

### Change 12: Per-finding agreement table (new section; requested by the caller)
- **Source**: diff-analysis C/X/U points, debate-transcript Scoring Matrix, calibrations
- **Target**: new H2 `## Per-finding agreement`, placed after Adherence summary and before Notes
- **Rationale**: the caller's output contract
- **Integration point**: columns Finding | Raised by (card 1 / card 2 / card 3) | Final grade | Why. Rows:
  1. Branch (cards 1, 2, 3).
  2. Known limits (cards 1, 2, 3; calibration 2 dissent recorded).
  3. Dropped sha256 (cards 1, 3; card 2 said "not a deviation", conceded).
  4. Authorized expansion (card 3).
  5. "83 tests" (card 3; cards 1 and 2 left it not verified).
  6. Test-discovery wording (card 1 Medium, card 3 Note; final Note, spec-inherited, Notes only).
  7. Backtick rendering (cards 1, 3; Note, spec-inherited, Notes only).
  8. Coverage-matrix inventory (card 2; Note).
  9. In-place fix route / verify-sync (none of the cards; invariant probe INV-003; folded into row 1's fix, not a separate row).
  10. origin/master line 122 risk (card 3, unverified; closed, not a finding).
- **Risk**: Low, additive

### Change 13: Keep card 1's check of the plan's B and E numbers (from Variant 1; added after the first merge pass flagged it as an unplanned dropped anchor)
- **Source**: Variant 1 Notes, "The plan's B and E numbers (3 of 3 and 2 of 3; master 1 of 3 and 0 of 3) match source.md:13" (variant-1:38)
- **Target**: Base Notes, "Checked with no finding" list (append one bullet)
- **Rationale**: Anchor-level rule. It is a verified quoted number that the plan's stated evidence rests on (plan:21), and it is uncontested. The orchestrator re-checked it: plan:21 gives E 3 of 3 for both target findings (master 1 of 3 and 0 of 3), and B 3 of 3 and 2 of 3 (master 0 of 3 each), which matches source.md:12-13.
- **Integration point**: append the bullet "**Scores.** The plan's B and E numbers at plan:21 match source.md:12-13: E 3 of 3 on both target findings (master 1 of 3 and 0 of 3); B 3 of 3 and 2 of 3 (master 0 of 3 each)."
- **Risk**: Low, additive
- **Concrete anchors preserved**: 3 of 3; 2 of 3; 1 of 3; 0 of 3; plan:21; source.md:12-13

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| X-002 / C-004 | Variant 1 row 4 grades the test-discovery wording `Medium:` (variant-1:23) | Conceded by the V1 advocate in Round 2. The wording is spec-inherited (source.md:34) and changes no value (agent:120). Calibration 1: "at most a Note". |
| X-001 / C-003 | Variant 2: "their limited automated coverage is **not** an additional plan deviation" (variant-2:33) | Conceded by the V2 advocate. The plan dropped the spec's sha256 (INF-008), so there is a plan-side divergence. |
| X-003 | Calibration 2: known-limits finding Medium | Rejected in both rounds. Missing has no consequence test (agent:119), and Decision also holds via plan:21. |
| S-002 | Variant 2 full absolute paths in every cell | Conceded by the V2 advocate. Full paths are given once in the header instead (Change 2). |
| (labels) | Variant 2 labels the two Blocking rows MEDIUM | The base labels HIGH are kept. Labels are information (agent:122), and HIGH matches agent:71 for these rows. |
| A-001 | Variant 1 fix "No task steps need to change" (variant-1:47) | Refuted by INV-003: the in-place route breaks plan:59. Change 3 names the route instead. |
| C-003 | Variant 1 / spec: variant path `.dev/stage3c-variants/brainstorm/reflect-reviewer.md` as part of the check | Not tracked on `origin/master` (INV-002). It is kept as provenance for the hash, not as a check (Change 5). |
| S-004 | Variant 1's Note paragraph outside the table (variant-1:25); Variant 2's Notes-only layout | Plan-side Medium and Note deviations go in the table (agent:122). Inherited items go in Notes (INV-013). |
| S-003 | Variant 2's 45 units and 40 adherent (two hand-added units) | Corrected to the matrix's 43 and 37 (r2-v2, r2-v3, INV-007). The two package-writing units are covered by the coverage-matrix Note (Change 9). |
| S-003 | Variant 1's 22 units, list summing to 23; Variant 3's 30 units | Replaced by the INF-id count. Both per-kind counts are dropped, and each omitted unit is covered by an INF id. |

Anchor-level omissions (no anchor is dropped silently):

| Source variant | Anchor type | Anchor text or ID | Reason for omission | Evidence from debate |
|----------------|-------------|-------------------|---------------------|----------------------|
| V1 | count | "Spec units audited: 22", "Fully adherent: 18" | Internal miscount (list sums to 23); replaced by INF-id count 43/37 | base-selection IC; r2 S-003 |
| V2 | count | "45", "40", "5 non-adherent" | Two hand-added units; replaced by 43/37/6 | r2-v2 S-003 |
| V3 | count | "30", "25", "3 rows covering 5 units" | Replaced by INF-id count | r2 S-003 (unanimous V2 method) |
| V1 | named statement | "I rely on the T1 card's simulation, which found the same sha256" (variant-1:44) | Superseded by direct verification (Change 10) | r2-v3 Response 3 |
| V1 | named statement | "Codegraph was stale, so I used Read and Grep only" (variant-1:45) | Kept as a method note in Notes; the merge-executor must preserve it | none (uncontested) |
| V2 | named statement | "The brief supplied a live grounding root rather than an isolated snapshot" (variant-2:34) | Kept in Notes; the merge-executor must preserve it | A-004 (STATED) |

## Threshold preservation

| Source variant | Value | Target disposition |
|----------------|-------|--------------------|
| spec via V1/V3 | sha256 `7696a2b21601ff914d7651085125ef4188238640998c0599907555c760ec0ed8` | preserved-exact, written in full (V1 and V3 truncated it) |
| debate (r2-v3) | base agent hash `ed911b7c…d183312c6` | preserved as given (truncated in the source) |
| plan/spec via cards | E: 3 of 3 and 2 of 3 vs master 1 of 3 and 0 of 3; B: 3 of 3 and 2 of 3 vs 0 of 3 each | preserved-exact where quoted |
| debate | 5 ahead / 49 behind `origin/master`; local ref `a0dd57777` | preserved-exact |
| probe | 53 deleted source primitives on `origin/master` | preserved-exact |
| V2 (corrected) | 43 units, 37 fully adherent | modified-with-rationale (from 45/40) |
| V3 | 13 files named by `git grep`; 4 YAML fixtures; 2 extra test files | preserved-exact |
| probe | 10 needles in the tuple at test:216-227 | preserved-exact |
| plan | "83 tests" | preserved-exact as the quoted claim in row 5 |
| debate | "at least 6 fewer cases" on `origin/master` | preserved-exact |
| cards | line 122 (agent), line 214 (test) | preserved-exact |
| debate | PR #605 = `e3e9d636a` | preserved-exact |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1, 2, 7, 9, 12 | Low | Additive; no conflicts | Remove the inserted text |
| 3, 4, 5 | Medium | A mis-merge could change a grade or drop a fix part (INV-003 route, INV-011 plan:21 rewording, INV-010 hash condition) | Revert to the base row text and re-apply |
| 6, 8, 10 | Low | Wording only | Revert to base Notes |
| 11 | Medium | Counts could disagree with the table | Recount from matrix:14, :91 |

## Review Status
- [x] Auto-approved (default; non-interactive)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-19T16:05:00Z
