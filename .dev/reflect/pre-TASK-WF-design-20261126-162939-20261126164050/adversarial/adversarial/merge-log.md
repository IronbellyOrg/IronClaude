<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (opus:refactorer) -->
<!-- Merge date: 2026-11-26T17:46:29Z -->

# Merge Log

- Plan executed: `refactor-plan.md` (auto-approved, non-interactive).
- Base: `variant-3-original.md` (reviewer 3, refactorer, opus).
- Sources read: `variant-1-original.md` (V1, analyzer, sonnet), `variant-2-original.md` (V2, qa, haiku), `invariant-probe.md`, `base-selection.md`, `debate/round2-advocate-1.md`, `debate/round2-advocate-2.md`, `debate/round2-advocate-3.md`.
- Output: `merged-output.md`. No other file was modified.
- **Status: complete.** All four validation checks pass (section "Validation"). Two items are escalated for the orchestrator (section "Escalations"); neither blocks the merge.

## Planned changes

### CH-A: replace the base card's 15 rows by the 35 merged rows (Blocking, Medium, Note)

Status: applied. Before: 15 base rows (Blocking 8 by text, labels mixed) plus one advisory correctness-gap row. After: 35 rows M-01 to M-35 in plan order; each row carries an HTML provenance comment in its `#` cell; each Blocking row ends with its repair. The advisory table is folded into M-14 (plan Sources: "V3 advisory").

Category rule used: plain Drift, Regression or Authorized expansion. Where a row has several source rows that disagree, the base (V3) row's category is used, because the plan says to keep the base card's wording where it exists. Probe-only rows have no deviation category and are labelled Drift.

| Row | Status | Before (base card) | After (merged) | Provenance tag | Validation |
|---|---|---|---|---|---|
| M-01 | applied | row 4 (Drift, Blocking Decision) | Blocking (Decision), Drift, HIGH; affected tasks widened to 3, 13, 15, 21, 24, 29, 34 (union of V3 and V1); repair added | V3 r4; V1 r2; V2 r1 | grade and label match the plan; V2 r1 said Regression, base Drift kept |
| M-02 | applied | row 2 (Drift, Blocking Decision) | adds the INV-011 point (S23 still `self-contained` fails at `:489-490`) and the lint-architecture note; repair moves the edit AND the test run | V3 r2; V1 r1; INV-011 | ok; V1 r1 said Regression, base Drift kept |
| M-03 | applied | row 7 (Drift, Blocking Decision) | adds V2's `test_git_facts.py:217` hit, PLAN:41, REQ:631 and the prose-vs-AC scope point; notes V1 and V2 graded Medium | V3 r7; V1 r10; V2 r5 | ok |
| M-04 | applied | row 5 (Drift, Blocking Decision) | adds V1's "count 20 only if all tracked" point; repair added | V3 r5; V1 r3 | ok; V1 r3 said Regression, base Drift kept |
| M-05 | applied | row 1 (Drift, Blocking Decision) | corrected per CH-C (see below); adds PLAN:429 (debate), the `test_implement_saved_prompt_rule.py` selection point (advocate 3), Tasks 28 and 29 (INV-012); notes advocate 2 graded Note | V3 r1; debate X-006; INV-012 | ok |
| M-06 | applied | row 3 (Drift, Blocking Missing) | adds the T-16 / NFR-005 conflict (REQ:679, from the probe) and the repair | V3 r3 | ok |
| M-07 | applied | none (new) | new Blocking (Decision) row from INV-014; Decision because the repair changes the acceptance checks of Tasks 26, 30, 31, 32 | INV-014 | ok |
| M-08 | applied | row 6 (Regression, Blocking Decision) | adds INV-006 (nine patterns, AC "seven", `ledger_builder` forms); repair records the DD-8 override | V3 r6; INV-006 | ok; Regression kept from the source row |
| M-09 | applied | none (new) | new Blocking (Missing) row; notes X-001 rejection | V1 r4 | ok |
| M-10 | applied | none (new) | new Blocking (Missing) row: T-04 (V2 r6), T-21 (V2 r3), FR-109 test list (V1 r11, including V1's note that Task 16 covers `gc`); notes advocate 1 graded Medium | V2 r3, r6; V1 r11 | ok |
| M-11 | applied | row 8 (Drift, Blocking Missing) | regraded to Blocking (Safety) as instructed; notes V1 graded Medium | V3 r8; V1 r8; V2 r4 | ok |
| M-12 | applied | none (new) | Medium; adds INV-005 (inherited `GIT_*`, `GIT_TERMINAL_PROMPT=0`) and X-002; minority note from the plan | V1 r13; INV-005 | ok |
| M-13 | applied | row 9 (Drift, "Blocking (Decision)" text, MEDIUM label) | grade text changed to "Medium:"; label MEDIUM (CH-C) | V3 r9 | ok |
| M-14 | applied | advisory correctness gap 1 (no category) | Medium; category Regression from V1 r5 ("Regression (internal conflict)") | V1 r5; V3 advisory | ok; see Escalation 2 |
| M-15 | applied | row 10 (Drift, Medium) | unchanged substance; notes advocate 1 argued Note | V3 r10 | ok |
| M-16 | applied | row 12, budget part (Note) | Medium (net-growth budget shared by Tasks 26 and 30); notes V2 graded Blocking | V1 r9; V3 r12 | ok |
| M-17 | applied | none (new) | Medium; notes advocate 2 argued Blocking | V1 r7 | ok |
| M-18 | applied | none (new) | Medium; adds INV-002 facts (merge base `862384852`, `origin/integration` `4ce9f14`, row moved 293 to 298, rebase collision); `HOW-WE-WORK.md:293` cited as the working-tree line from V3's Notes, not the upstream 298 | V1 r12; INV-002 | ok |
| M-19 | applied | none (new) | Medium; notes V2 graded Blocking | V2 r2 | ok |
| M-20 | applied | none (new) | Medium; minority note from the plan | V2 r10 | ok |
| M-21 | applied | none (new) | Medium | INV-001 | ok |
| M-22 | applied | none (new) | Medium | INV-004 | ok |
| M-23 | applied | none (new) | Medium; V1's Notes item on re-keying the row is cited in the provenance tag | INV-013; V1 Notes | ok |
| M-24 | applied | none (new) | Medium | INV-015 | ok |
| M-25 | applied | row 11 (Drift, Medium) | adds V1's FR-108 point and DESIGN:134, REQ:579, 587; "owner decision, no plan edit" | V3 r11; V1 r6 | ok |
| M-26 | applied | row 15 (Drift, Note) | adds V1's Task 15 / `hook_emulator` item and PLAN:196 | V3 r15; V1 r16 | ok (plan line names only C-007; V3 r15 and V1 r16 are the card rows for it) |
| M-27 | applied | none (new) | Note; NFR-013 and NFR-015 gaps folded in per CH-E | V2 r8; V1 coverage | ok |
| M-28 | applied | none (new) | Note; "no implementation instruction" withdrawn per X-005 | V2 r9 | ok |
| M-29 | applied | none (new) | Note | INV-003 | ok |
| M-30 | applied | none (new) | Note | INV-007 | ok |
| M-31 | applied | none (new) | Note | INV-008 | ok |
| M-32 | applied | none (new) | Note | INV-009 | ok |
| M-33 | applied | none (new) | Note | INV-010 | ok |
| M-34 | applied | rows 12 (anchor part) and 14 (Note) | Note, both stale anchors in one row | V3 r12, r14 | ok |
| M-35 | applied | row 13 (Authorized expansion, Note) | adds V1's `core.autocrlf` point; V1's claim that the preflight list also lacks `hooks_path` is left out, because `base-selection.md` lists it as shown false | V3 r13; V1 r14 | ok; the only Authorized expansion row |

### CH-B: Adherence summary counts

Status: applied. Before: "Spec units audited: 38 tasks plus the Constraints block"; "Fully adherent: 20 (...)"; "Authorized expansion 1, Necessary 0, Drift 13 (8 Blocking), Regression 1". After: 38 tasks plus Constraints plus the 29 coverage ids; Blocking 11, Medium 14, Note 10; Blocking by kind Decision 7, Missing 3, Safety 1; Authorized expansion 1 (M-35), Necessary deviation 0, Drift 32, Regression 2 (M-08, M-14). "Fully adherent 20" dropped. Validation: the counts were recomputed from the table by script (Drift 32, Regression 2, Authorized expansion 1).

### CH-C: correct two base-card errors

Status: applied.
- Base row 1 (now M-05): Task 27 removed from the affected list ("Task 27 runs no tests"); the `refs/qa.md:52` "early copy is a breach" premise is stated as withdrawn (X-006, Constraint 24 requires the copy). The repair still has Task 27 copy `commit-step.md`, as the plan's repair column and advocate 1's X-006 fix say.
- Base row 9 (now M-13): "Blocking (Decision)" text with a MEDIUM label replaced by "Medium:" with label MEDIUM. The plan's CH-C wording ("label HIGH, not MEDIUM, now that it is Blocking-free") reads as garbled; its stated result, "it becomes M-13 Medium", and the Medium table were followed.

### CH-D: `## Repairs` section

Status: applied. Eleven numbered lines (M-01 to M-11), each naming the tasks to change and the plan's repair text; then `### Medium repairs (not applied by the plan repair step; follow-up candidates)` with M-12 to M-25 and their plan notes. The base card's "Reviewer's recommended action" Notes line is replaced by a pointer to this section.

### CH-E: `## Coverage` section

Status: applied, with a count discrepancy flagged (Escalation 1). The inactive ids, the covered-by-task list (from V1's "The 29 ids" section), the three real gaps and the rejected coverage claims (from the plan's "Changes NOT Being Made") are written. The base card's Notes line "NFR-014 by Tasks 4, 29" is replaced by a pointer to this section, because X-002 rejected it.

### CH-F: `## Unresolved` section

Status: applied. Two bullets: INV-014 UNADDRESSED HIGH at Round 2.5, now M-07; the Category 6 sufficiency challenge (13 original repairs falsified by INV-014 and INV-011), so the repair set is M-01 to M-11.

### Changes NOT being made (plan list)

All respected: V2's Blocking grades for M-12, M-16, M-20, M-27, M-28 appear only as minority notes; V1's Medium grades for M-03, M-11 appear only as minority notes; V3's `qa.md:52` breach premise is withdrawn; V2's FR-109 and NFR-014 coverage claims are listed as rejected; the 16 inactive FR ids are not treated as missing; no edit to `source.md` is proposed, and the DD-8 and T-16 / NFR-005 overrides are recorded in the plan-side repairs.

## Validation

| Check | Result | How |
|---|---|---|
| (a) Heading structure has no level gaps | pass | Script listed the headings: H1 title; H2 Deviations, Adherence summary, Notes, Repairs, Coverage, Unresolved; H3 only under Repairs. No gap. |
| (b) Every row M-01 to M-35 present exactly once | pass | Script: 35 rows, 35 unique, in order M-01 to M-35. |
| (c) Every file:line citation appears in a source card, the probe or the plan table | pass | Script: 70 distinct `file:line` citations, 83 PLAN, 27 DESIGN (incl. `source.md`), 19 REQ line numbers; none missing from V1, V2, V3, `invariant-probe.md` or `refactor-plan.md`. Relative continuations (`:61`) were not checked separately; they follow a checked file name. Spot-check below. |
| (d) No new contradiction with the debate's final grades | pass | Script: every row's grade prefix and Severity label match the plan (M-01 to M-11 Blocking/HIGH, M-12 to M-25 Medium/MEDIUM, M-26 to M-35 Note/LOW); M-11 is "Blocking (Safety):"; Authorized expansion only on M-35. Minority grades appear only as notes. |

### Spot-check of cited lines (check c)

12 citations were read in the live tree at the cited line. All match; no evidence text was changed.

| # | Citation (row) | What the line holds | Match |
|---|---|---|---|
| 1 | PLAN:29 (M-01) | "No code or text uses `--no-verify`, `-n` on commit, `SKIP=`, `commit-tree` or `--amend`." | yes |
| 2 | `tests/recommend/test_routing_refresh.py:483-496` (M-02) | `test_case_activation_matches_command_source`; `self-contained` asserts no Activation section at 489-490; skill must exist at 495-496 | yes |
| 3 | `tests/commands/test_workflow_command.py:204-220` (M-05) | compares src and plugin `sc-implement-protocol` by file set (218) and bytes (220) | yes |
| 4 | `tests/skills/test_task_workspace_lifecycle.py:682-688` (M-06) | transient list exactly four reasons; 686-688 scan only `refs/retry.md`, `refs/ledger.md`, `SKILL.md` | yes |
| 5 | `tests/skills/test_implement_severity_static.py:420-434` (M-07) | `test_ac11_every_halt_stop_ruling_site_is_classified`; each site must match exactly one `_ALLOW` entry | yes |
| 6 | `refs/retry.md:437` (M-21) | "At `complete`, delete the Q0 pin and the task's checkpoint refs" | yes |
| 7 | `scripts/worktree_cleanup.py:2642` (M-03) | `runner.run(["git", "branch", "-d", branch], ...)`, a list-form argv | yes |
| 8 | REQ:475 (M-11) | excluded paths include "paths under `.dev/implement/`" | yes |
| 9 | `refs/managed-workspace.md:50-52` (M-13) | archive gate heading (50) and step 1 (52) | yes |
| 10 | `tests/worktree_cleanup/conftest.py:146-151` (M-12) | `git_in` sets `GIT_TERMINAL_PROMPT="0"` | yes |
| 11 | `archive_workspace.py:44-67` (M-08) | `_HEADER` at 44-46 through `_ARCH` at 67 | yes |
| 12 | `src/superclaude/commands/README.md:9` (M-34) | "(parity tests check these four)" | yes |

## Escalations (for the orchestrator; merge not blocked)

1. **CH-E count.** The plan says 18 of the 29 ids are not active requirements, but the ids it lists (FR-024 to FR-029, FR-083 to FR-089, FR-119, FR-068, FR-069) number 16. The 18 looks carried over from V2's list, which also counted FR-037 and FR-055; FR-055 is not among the 29, and V1 shows FR-037 covered by Task 5. `merged-output.md` keeps the plan's list, states both numbers and puts FR-037 under "covered". Please confirm or correct the plan.
2. **Category choices not set by the plan.** M-14 is labelled Regression because its only categorized source row (V1 row 5) says "Regression (internal conflict)"; advocate 1 conceded a "Regression label stretch" in Round 1 without naming rows, so this may be meant as Drift. In M-01, M-02 and M-04, V2 or V1 said Regression and the base said Drift; the base label was kept. Probe-only rows (M-07, M-21 to M-24, M-29 to M-33) are Drift by default. None of this changes a grade.

## Source rows not carried (not named in the plan's Sources; not added)

- V1 row 15 (Note): Task 4's `--ignore-submodules=all` is stated for every read, but only `status` and `diff` accept it (PLAN:70; DESIGN:184).
- V2 row 7 (V2 graded Blocking (Missing), label MEDIUM): the no-flag regression check runs through `vcs reconcile --flag off` and cannot prove that the executor adds no Bash calls or files when no sidecar exists (PLAN:384; DESIGN:365). Advocate 2 argued for it under C-012, but the plan's M-10 Sources name only V2 rows 3 and 6.

Neither was added, because the merge executor adds only what the plan names. If either should be kept, the plan needs a row for it.
