# Diff Analysis: reviewer-card Comparison (sc:reflect Tier 2 merge)

## Metadata
- Generated: 2026-11-13T05:27:00Z
- Variants compared: 3 (variant-1 = reviewer-1 analyzer, 2 findings; variant-2 = reviewer-2 qa, 12 findings; variant-3 = reviewer-3 refactorer, 2 findings)
- Audited artifacts: SPEC `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md`, PLAN `.../TASK-WF-designSpec-20261107-075614.md`
- Total differences found: 18 (excluding the 3 shared assumptions listed separately)
- Categories: structural (1), content (9), contradictions (4), unique (4), shared assumptions (3)
- Focus: correctness, coverage, deviation-classification

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Card layout | header, findings block, self-report, audit notes (6 bullets), rows_observed | same order, notes numbered 1-10 and include process remarks (read the brief under `runs/`, saw two post-execution test file names) | same order, 3 short bullets | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 | Wave 0 bullet vs its own test (plan lines 137-140, spec 241) | F1 MINOR, non-blocking: both texts carry the tension, the test must target gating wording only | F1 MAJOR, blocking: the required behaviour cannot pass its own test | not raised | High |
| C-002 | Cycle-id minting (plan lines 124 and 150, spec 251) | not raised; says dependencies and order look sound | F4 MINOR: no criterion checks that guard, push triad and `rereview_requested` share one `cycle_id` | F1 MAJOR, blocking: Task 8 and Task 10 both direct minting, violating exactly-one-source | High |
| C-003 | Event payload and `idempotency_key` format (spec 182-185) | F2 MINOR: no criterion pins the fields or `guard:<run_id>:<cycle_id>:<to>:a<k>`; Task 8 cites spec sections 3, 4.1, 4.5, 4.6, 5 and omits 4.2 and 4.4 | not raised | not raised | Medium |
| C-004 | Decision-table and fold criteria that never assert a spec item | says no spec row of Tasks 3 and 4 lacks a criterion | F3 `auto_merge_armed` in engage `notes`; F7 `original_is_draft` on a first skip; F6 `RunConfig` unchanged; F10 `--to ready` idempotency; F12 CI-fix engage case | not raised | Medium |
| C-005 | Task 11 scenario criteria | not raised | F2 MINOR: criteria check only that 12 names exist and pytest passes | verified its assigned rows, no finding | Medium |
| C-006 | Docs criteria for Tasks 12 and 13 (plan lines 185, 198) | not raised | F5 MINOR: grep checks match the flag token so they pass without the section, clear command or unverified statement | not raised | Low |
| C-007 | Pinned-sentence and bullet-gating tests (plan lines 150-154) | not raised | F8 start-text constants cannot catch a later change; F9 bullets' L3 and `draft` gating not asserted | not raised | Medium |
| C-008 | PR body states the release gate (spec 326) | not raised | F11 MINOR: no task authors or checks a PR body | not raised | Low |
| C-009 | Task dependency of Task 12 on Tasks 9 and 10 (shared test file) | says task order and dependencies look sound | not raised | F2 MINOR: Task 12 extends the file Tasks 9 and 10 extend without depending on them | Low |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|---|---|---|---|
| X-001 | Severity of the Wave 0 bullet check | V1 F1: MINOR, blocking false | V2 F1: MAJOR, blocking true | High (decides whether the merged verdict has a blocker) |
| X-002 | Whether Tasks 3 and 4 leave spec rows without a criterion | V1 notes: "I found no spec row that Tasks 3 and 4 leave without a criterion" | V2 F3 and F7: `auto_merge_armed` and `original_is_draft` have no assertion | Medium |
| X-003 | Whether task order and dependencies are sound | V1 notes: "Task order and dependencies look sound" | V3 F2: Task 12 lacks a dependency on Tasks 9 and 10 | Low |
| X-004 | Whether Task 11 criteria can fail | V2 F2: stub bodies pass | V3: verified its rows with no finding; plan lines 170-172 assert event order, real recovery calls and forbidden `gh` calls | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | V1 | Task 8 omits spec 4.2 and 4.4 from its sources, so the ref may not carry event fields or the key format | Medium |
| U-002 | V3 | Cycle-id minting appears in two tasks against the spec's one-source rule | Medium |
| U-003 | V2 | Ten acceptance-gap findings (F2 to F12 except F4 overlap with V3) | Medium |
| U-004 | V2 | Process disclosure: it saw two post-execution test file names in a grep and opened neither | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | Line numbers in the cards' citations are accurate | all three cite plan and spec lines | High: V2 cites four lines that do not hold the quoted text (spec 369, 280, 270, 268); citation re-reads decide | UNSTATED, promoted |
| A-002 | /sc:implement runs the plan's tasks in listed order, so a missing `Depends on:` line only matters to a parallel executor | V1 and V3 reasoning about dependencies | Medium: decides the weight of V3 F2 | UNSTATED, promoted |
| A-003 | A gap in an acceptance criterion for a stated plan sentence is a defect of the plan, even when the shipped protocol prose is the impure orchestrator and checked only by wording tests | V2 F3, F6, F7, F9, F10 | Medium | UNSTATED, promoted |

## Summary
- Total structural differences: 1
- Total content differences: 9
- Total contradictions: 4
- Total unique contributions: 4
- Total shared assumptions surfaced: 3 (UNSTATED: 3, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, X-001
