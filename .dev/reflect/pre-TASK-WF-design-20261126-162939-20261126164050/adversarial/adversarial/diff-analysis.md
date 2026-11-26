# Diff Analysis: Reviewer-card comparison (reflect UC-1, plan vs design)

## Metadata

- Generated: 2026-11-26T17:02:00Z
- Variants compared: 3 (variant-1 = reviewer 1 analyzer/sonnet, 16 rows; variant-2 = reviewer 2 qa/haiku, 10 rows; variant-3 = reviewer 3 refactorer/opus, 15 rows + 1 advisory)
- Subject of all three: the 38-task plan `TASK-WF-design-20261126-162939.md` against its design `source.md`
- Total diff points (S + C + X + A): 37 (structural 3, content 24, contradictions 6, shared assumptions 4); unique contributions U: 12 (not in the denominator)
- Taxonomy level in brackets: L1 surface, L2 structural, L3 state-mechanics
- Variants were not blinded (`--blind` not set); each card names its persona and model class in its header.
- Abbreviations: `PLAN` = the plan file, `DESIGN` = `source.md`, `REQ` = merged requirements.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 [L1] | Layout | 3 H2 sections plus one H3 ("The 29 ids"); Deviations table, adherence summary, notes | 5 H2: adds an "Unmapped IDs checked" table and a "Design sections 3 to 8 and 10" table | 4 H2: adds a separate "Correctness gaps (advisory)" table | Low |
| S-002 [L2] | Category labels | Regression, Drift, "Drift (missing task)", "Regression (internal conflict)" | Regression and Drift only | "Drift (broken plan)", "Drift (missing step)", "Authorized expansion", Regression | Medium |
| S-003 [L2] | Severity vocabulary | Grade (Blocking/Medium/Note) in the cell text plus HIGH/MEDIUM/LOW label, labels mostly agree | All ten rows start with "Blocking" but the label column mixes HIGH and MEDIUM | Grades and labels agree except row 9 ("Blocking (Decision)" with label MEDIUM) | Medium |

## Content Differences

Each row says how each variant treats the topic ("-" = not raised).

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 [L2] | Constraint line 29 ("No code or text uses `--no-verify`...") vs tasks that must write those tokens (PLAN:29 vs 60, 172, 193, 334) | Blocking (Decision), gives rewording | Blocking (Decision), limit to executing or recommending | Blocking (Decision), lists affected tasks 3, 13, 15, 21, 24, 29 | Low (same grade; wording of fix differs) |
| C-002 [L3] | Task 13 path rules omit the `.dev/implement/` exclusion (DESIGN:228, REQ:475) | Medium | Blocking (Missing), HIGH | Blocking (Missing), HIGH | Medium (grade differs) |
| C-003 [L2] | Task 24 acceptance 2: "only file in the repository that runs a branch deletion" | Medium; lists five hit files; says the allow-listed file may not match a text scan | "Blocking (Decision)" but label MEDIUM; cites `tests/worktree_cleanup/test_git_facts.py:217`; REQ:631 says "No new code" | Blocking, HIGH; lists five hit files; notes `worktree_cleanup.py:2642` uses a list-form argv | Medium (grade differs, evidence overlaps) |
| C-004 [L2] | Task 19 sets S23 activation to `sc:git-protocol` and runs the routing test before Task 20 creates `SKILL.md` | Blocking (Decision), HIGH | - (counts T-14 and AC-13 as covered by Tasks 19, 35, 36) | Blocking (Decision), HIGH | High |
| C-005 [L2] | Task 25 acceptance uses `git ls-files` after a plain delete | Blocking (Decision) | - | Blocking (Decision); tracked state UNVERIFIED | Medium |
| C-006 [L3] | DD-11 / open item O1: owner confirmation of the "pending, attempt n+1" reading | Medium | Open decision, not a finding | Medium | Low |
| C-007 [L1] | Incomplete `Depends on:` lines (Tasks 6, 8 to 12, 15) | Note | Checked, "not a blocker" | Note | Low |
| C-008 [L2] | Plugin copies of the implement protocol left to Task 38 while existing tests require byte equality (Tasks 26 to 34) | - | - | Blocking (Decision), HIGH | High |
| C-009 [L3] | Task 31 adds `E-RESUME-NEEDED` reasons that an existing test (`_TRANSIENT`, four reasons) forbids | - (checked only the STOP-table pin at `test_task_workspace_lifecycle.py:778-791`, which holds) | - | Blocking (Missing), HIGH | High |
| C-010 [L3] | Task 9 ledger reader copies seven line patterns, omits `_HEADER` and `_ARCH`, treats an unparseable last line as corrupt | Adherent apart from dependency note | - | Blocking (Decision), Regression | High |
| C-011 [L3] | `skipped` settlement (empty or mixed-authorization boundary) has no action in Task 12's closed list and no acceptance | Blocking (Missing), HIGH | Lists FR-109 as covered by Tasks 11, 12, 14, 17, 29, 30 | - | High |
| C-012 [L3] | Acceptance gaps against required tests (FR-109 list, T-21, T-04, T-16) | Row 11 Medium (FR-109 test list partly missing) | Rows 3, 6, 7 Blocking (Missing) | - | Medium (grade differs) |
| C-013 [L2] | NFR-014 (stop rather than wait on a credential or authentication prompt) | Real gap, Medium (only `timeout=10` and the 600000 ms call exist) | Covered by Tasks 4, 5, 16, 21, 29 | Covered by Tasks 4 and 29 | Medium |
| C-014 [L3] | Archive gate calls `vcs reconcile` without checking `commits.md` (NFR-018: no extra Bash call without the flag and sidecar) | - | Row 7 raises a related no-flag proof gap (executor behavior not testable through a read-only helper) | Blocking (Decision) graded MEDIUM, Task 32 | Medium |
| C-015 [L3] | Allow-list forbids `-A` yet the snapshot method runs `add -A` in a private index | Row 5, Medium | - | Advisory correctness gap 1 | Low |
| C-016 [L2] | `--commit-tasks` "appears only in" check vs Task 37 docs and sync-dev copies | - | - | Medium | Medium |
| C-017 [L2] | SKILL.md net growth cap of 15 lines and the stale line 129 anchor (Tasks 26, 30) | Row 9, Medium (feasibility doubtful) | - | Row 12, Note (stale anchor, `--stat` counts insertions plus deletions) | Medium |
| C-018 [L1] | Task 14 lists seven refusal tokens but says "five" and tests two | Row 7, Medium | - | - | Low |
| C-019 [L2] | Unchanged-file proofs compare to `origin/integration` (Tasks 9, 32, 38) | Row 12, Medium | - | - | Low |
| C-020 [L2] | Design's "test-first order inside each phase" not carried into the plan | - | Row 10, Blocking (Missing) | - | Low |
| C-021 [L3] | Person-only commit authority (invariant I4) has no assertion in Tasks 20, 24 | - | Row 2, Blocking (Missing), HIGH | - | Medium |
| C-022 [L2] | Helper JSON field-level contract (`header_len`, `rule`, `runs`, `segments`) not checked | - | Row 8, Blocking (Missing), MEDIUM | - | Low |
| C-023 [L2] | 40-line refusal-log cap (DESIGN:431) has no explicit instruction or check | - | Row 9, Blocking (Missing), MEDIUM | - | Low |
| C-024 [L1] | Coverage reading of the 29 ids not named in the plan | Not requirements, covered, or real gaps (NFR-013, NFR-014, NFR-015) | Same classification; says 18 are unused or deleted numbers | Checked 10 only | Low |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|---|---|---|---|
| X-001 [L3] | FR-109 / skipped settlement | V1: required behavior absent, Blocking (REQ:551, 576, 580; DESIGN:290-291, 355; PLAN:156) | V2: FR-109 "covered" by Tasks 11, 12, 14, 17, 29, 30 | High: decides whether a task must be added |
| X-002 [L2] | NFR-014 | V1: not covered by any task (PLAN:70, 252, 334 have only timeouts) | V2 and V3: covered by Tasks 4, 5, 16, 21, 29 | Medium |
| X-003 [L2] | Grade of C-002 and C-003 | V1: Medium | V2 and V3: Blocking | Medium: decides which items the repair must fix |
| X-004 [L3] | Task 9 ledger reader | V1: seven copied patterns match the original, no finding beyond dependencies | V3: omission of `_HEADER` and `_ARCH` causes false `LedgerCorrupt` on a header-only ledger | High |
| X-005 [L2] | 40-line refusal-log cap | V2: "no implementation instruction" | PLAN:252 and PLAN:334 cite FR-064 (a range including it); PLAN:19 tells tasks to read the cited FR (calibrator note) | Low |
| X-006 [L2] | Why plugin copies and constraint 24 interact | V3: early plugin copy "would be work the plan reserves for Task 38" | PLAN:24 says keep the plugin copies byte-identical whenever `src` is edited | Medium: the plan's own Constraint already requires the early copy |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | 3 | Plugin-copy timing breaks existing tests before Task 38 (C-008) | High |
| U-002 | 3 | `_TRANSIENT` reason pin for `E-RESUME-NEEDED` (C-009) | High |
| U-003 | 3 | `_HEADER` and `_ARCH` missing from the ledger reader (C-010) | High |
| U-004 | 1 | Missing `skipped` settlement action (C-011) | High |
| U-005 | 2 | Person-authority invariant untested (C-021) | Medium |
| U-006 | 2 | T-21 crash-after-append and double-resume acceptance missing (C-012) | Medium |
| U-007 | 3 | NFR-018 breach by the archive gate (C-014) | Medium |
| U-008 | 3 | "Appears only in" scope check conflicts with docs and sync-dev (C-016) | Medium |
| U-009 | 1 | NFR-014 stop rule missing (C-013) | Medium |
| U-010 | 1 | `origin/integration` comparison fragility (C-019) | Low |
| U-011 | 2 | Test-first order not carried forward (C-020) | Low |
| U-012 | 2 | Helper field-level contract and 40-line cap acceptance gaps (C-022, C-023) | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 [L3] | All cards grade rows "Blocking" | The review-severity rule (changes a decision, a required behavior or an acceptance check) equals what would actually halt `/sc:implement`; the cards never check implement's own blocking model (`refs/qa.md`) except for the quoted-constraint rule | UNSTATED | Yes |
| A-002 [L3] | V1 and V3 verify existing tests; V2 does not | The plan's acceptance universe includes every existing test that reads a file the plan edits (pins, byte-parity tests), not only the tests the plan names | UNSTATED | Yes |
| A-003 [L3] | All cards audit the plan against the design | The design and requirements are correct and complete where the plan follows them; a defect that originates in the design (V3 row 6, DD-8) can be fixed in the plan without editing `source.md` | UNSTATED | Yes |
| A-004 [L3] | V1 and V3 compare against `origin/integration` and repository state | The repository base and the set of existing tests will not move between this review and implementation | UNSTATED | Yes |
| (not promoted) | All cards | Tasks run in source order and `Depends on:` lines are ignored (`SKILL.md:92`, `:110`) | STATED | No |
| (not promoted) | All cards | No test or command was run; every "fails" comes from reading test source | STATED | No |

## Summary

- Total structural differences: 3
- Total content differences: 24 (denominator: S 3 + C 24 + X 6 + A 4 = 37)
- Total contradictions: 6
- Total unique contributions: 12
- Total shared assumptions surfaced: 4 UNSTATED promoted, 2 STATED not promoted, 0 CONTRADICTED
- Highest-severity items: C-004, C-008, C-009, C-010, C-011, X-001, X-004
