# Diff Analysis: reviewer-card Comparison

Subject: three Tier 2 reviewer cards on plan `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/TASK-WF-brainstormFixBri-20261106-113538.md` ("plan") against its brief (the package's `source.md`).
Variants: V1 = `variant-1-original.md` (sonnet:analyzer, calibrated 0.74), V2 = `variant-2-original.md` (haiku:qa, calibrated 0.81), V3 = `variant-3-original.md` (opus:refactorer, calibrated 0.81).
Mode A, `--depth standard`, focus: correctness, coverage, deviation-classification. Prepared by the orchestrator (the analytical step was run inline; no separate agent).

## Metadata
- Generated: 2026-11-06T11:55:00Z
- Variants compared: 3
- Total differences found: 22 scored points (2 structural, 16 content, 3 contradictions, 1 shared assumption) plus 9 unique contributions
- Categories: structural (2), content (16), contradictions (3), unique (9), shared assumptions (1)

Orchestrator evidence gathered before the debate (read-only commands, recorded so advocates argue from the same facts):
- E-1: `git status --porcelain -- .dev/tasks` (2026-11-06T11:50Z) prints only `A`/`R` lines plus `?? .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/`; none of the six plan files is modified.
- E-2: `make lint` exits 0 today ("All checks passed!", architecture policy PASS with 5 warnings); `uv run ruff format --check` on the two edited test files and the two unrelated dirty files prints "4 files already formatted", exit 0.
- E-3: `/sc:implement`'s per-task reviewer receives "the task brief (Ti text + AC ids + global constraints) and the diff" (`~/.claude/skills/sc-implement-protocol/refs/qa.md:9`) and compares the diff to the task's AC, the parent constraints and "explicit instructions on the task" (`qa.md:13-17`); "Missing" = "AC/instruction not in the diff" (`qa.md:21`).

## Structural Differences

| # | Area | V1 (analyzer) | V2 (qa) | V3 (refactorer) | Severity |
|---|------|---------------|---------|-----------------|----------|
| S-001 | Per-correction verifier table | None; correctness probes per sentence clause | Full F-1..F-17 table with pass/fail and plan lines, plus Part 4 / Part 5 checks | None; checked_clean list cites F-2, F-13, F-16, F-17 only | Medium |
| S-002 | Unverified / limits section | Explicit `unverified` list (git, make lint, session encoding) | Folded into one checked_clean row | Folded into the closing note | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | No whole-text copy check for the fenced texts (Task 6 spec sentences; Tasks 1-3 applied texts) | R1-F1 P2: Task 6 only; add `grep -cF` for four decision-clause fragments or the whole sentence | R2-01 P2: Tasks 1-3 and 6; add exact-equality ACs; keep the F-7 pin set | R3-2 P2: Tasks 1-3 and 6; save fenced texts to `./artifacts/` and `grep -cF -f` | Medium |
| C-002 | Extra negative pin in Task 6 AC vs F-7 "exactly these pins" (plan:144) | Treats the negative pin as legitimate; asks to record any addition next to it | R2-02 P3: literal F-7 verifier fails; move to a note or get authorization | Silent | Low |
| C-003 | F-12 verifier quantifier contradicts F-3 (source.md:161 vs :63) | Silent | R2-03 P2: record the brief contradiction | Silent (checked the pins clean) | Low |
| C-004 | F-14 literal absence vs negative AC quoting the phrase (plan:45) | Silent | R2-04 P3 | Silent | Low |
| C-005 | Residual-risk notes paraphrased (plan:134-138 vs source.md:240-244) | R1-F7 P3: narrow risk 4 further (opposite direction) | R2-05 P3: copy all five verbatim | R3-8 P3 owner note: risk 4 claims a spec mechanism step 4 lacks | Medium |
| C-006 | Coverage matrix omits the 17 Verifier lines (review artifact) | Silent | R2-06 P2 | Silent | Low |
| C-007 | "required ... only when" states a necessary condition, not "exactly when" (plan:128) | R1-F2 P3 owner note | Silent | Silent | Medium |
| C-008 | Refusal clause has no recorded marker; literal `--report-dir` match; "returns no tool error" weak (plan:128) | R1-F3 P3: a missed refusal is a false FAIL, contradicting plan:133 | Silent (calls the qualifications retained) | Silent | Medium |
| C-009 | Start-state guard: six files clean before Task 1 (plan:44) | R1-F4 P3 | Silent | R3-6 P3 | Low |
| C-010 | Whole-repo `make lint` with unrelated dirty files; no baseline, no exit codes in logs (plan:153, :157) | R1-F5 P3 | Silent | R3-5 P3 | Low |
| C-011 | Spec 7.2 step 5 condition 2 (top-level command call) vs a nested analyze Skill call inside a `Task` subagent | R1-F6 P3 owner note | Silent | Silent | Medium |
| C-012 | Risk 4's "the spec then blocks a PASS" vs spec:300's scope (step 5 conditions 1, 2, 4, 5) | R1-F7 (partial: says risk 4 already conditioned) | Silent (wants risk 4 copied verbatim) | R3-8 P3 owner note | Medium |
| C-013 | Task 7 bullet 3 exemption for other `.dev/tasks` paths | Silent | Silent | R3-1 P2 (void per E-1) | Low |
| C-014 | Task 3 has no diff-shape AC | Silent | Silent | R3-3 P3 | Low |
| C-015 | Pre-change HEAD checks: Task 5 lacks the `git cat-file -e` guard; only one pin checked against HEAD | Silent | Silent | R3-4 P3 | Low |
| C-016 | Task 7 body: "writes only the logs" then "the one non-log file" (plan:153) | Silent | Silent (marked F-13 pass) | R3-7 P3 | Low |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|-------------------|----|----|----|--------|
| X-001 | What the plan should do with residual risk 4 | Narrow its wording (R1-F7) | Copy the brief's text verbatim, including "spec:300 then blocks a PASS" (R2-05) | Narrow it, or have the owner amend Part 4, because spec:300 does not cover step 4 (R3-8) | Medium |
| X-002 | Whether a whole-text check conflicts with F-7's "exactly these pins" | It is an addition to the pin list; record it (R1-F1) | Preserve the prescribed pin set; the extra negative pin already fails F-7 (R2-01, R2-02) | A byte check is not a pin, so no conflict (R3-2) | Medium |
| X-003 | Whether the amended sentence still has a known false-FAIL path (plan:133 "no known false FAIL") | Yes: a refusal the checker misses, and a nested analyze call failed by step 5 condition 2 (R1-F3, R1-F6) | No: the trigger and the timeout, refusal, tool-error and not-verifiable qualifications are retained (V2 checked_clean) | Not probed; anchors and slices clean | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V2 | Literal per-correction verifier table F-1..F-17 (14 pass, 3 fail) | High |
| U-002 | V1 | "only when" is necessary-not-sufficient (C-007) | Medium |
| U-003 | V1 | Step 5 condition 2 interaction with a nested analyze Skill call in a subagent (C-011) | Medium |
| U-004 | V1 | Refusal clause has no recorded marker (C-008) | Medium |
| U-005 | V2 | F-12 vs F-3 contradiction in the brief (C-003) | Low |
| U-006 | V2 | Coverage matrix lacks Verifier rows (C-006) | Medium |
| U-007 | V3 | Task 3 diff-shape AC (C-014) | Low |
| U-008 | V3 | Task 5 HEAD-check guard and one-pin scope (C-015) | Low |
| U-009 | V3 | Task 7 self-contradicting sentence (C-016) | Low |

## Shared Assumptions

Agreement points: all three cards find no P1; all three confirm the amended trigger removes the lc10 Task-prompt false FAIL; all three rate the missing whole-text check P2.

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | `/sc:implement`'s per-task QA checks only the acceptance criteria, so a paraphrase of a fenced "copy character for character" text would pass unless an AC compares the whole text | C-001 (all three rate it P2) | Decides P2 vs P3 for C-001 | UNSTATED; E-3 suggests it is CONTRADICTED (the reviewer gets the task text and compares the diff to "explicit instructions on the task", qa.md:9, :17, :21) |

## Summary
- Total structural differences: 2
- Total content differences: 16
- Total contradictions: 3
- Total unique contributions: 9
- Total shared assumptions surfaced: 1 (UNSTATED: 1, STATED: 0, CONTRADICTED: 0 as classified by the variants; the orchestrator's E-3 evidence bears on it)
- Highest-severity items: X-003 (High); C-001, C-005, C-007, C-008, C-011, C-012, X-001, X-002, S-001 (Medium)
- Taxonomy pre-tags: L3 (state/guard/boundary/validation): C-001, C-008, C-009, C-011, C-013, C-015, X-003, A-001; L2 (structure): S-001, C-005, C-006, C-007, C-010, C-012, C-014, X-001, X-002; L1 (wording): S-002, C-002, C-003, C-004, C-016
- Similarity check: 22 scored points across three cards with largely disjoint findings; well above the 10% threshold, so the debate runs.
