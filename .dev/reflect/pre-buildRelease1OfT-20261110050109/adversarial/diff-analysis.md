# Diff Analysis: reviewer-card comparison (pre-build reflect of TASK-WF-buildRelease1OfT-20261110-045742)

## Metadata
- Generated: 2026-11-10T05:12:00Z
- Variants compared: 2
  - Variant 1: `variant-1-original.md` (copy of `reviewer-cards/reviewer-1-card.yaml`; analyzer, haiku; 7 findings: 4 blocking, 3 minor)
  - Variant 2: `variant-2-original.md` (copy of `reviewer-cards/reviewer-2-card.yaml`; qa, opus; 12 findings: 5 blocking, 7 minor)
- Input type warning: both inputs are YAML, copied verbatim under a `.md` name (Mode A naming rule); normalization was not applied, so the copies are byte-identical to the cards.
- Prepared by: the debate-orchestrator itself (no separate analytical agent was spawned for Step 1; recorded as a minor degradation in the return contract).
- Total differences found: 24
- Categories: structural (2), content (3), contradictions (2), unique (13), shared assumptions (4)

## Structural Differences

| # | Area | Variant 1 (R1) | Variant 2 (QA) | Severity |
|---|------|----------------|----------------|----------|
| S-001 | Granularity | 7 findings; mixes design defects (side-call, snapshot timing, constraint wording, dependency order) with coverage gaps | 12 findings; almost all are acceptance-criterion coverage gaps measured against SPEC tests T-nn | Low |
| S-002 | Evidence style | Cites the plan, real source code (`install_user_setup.py:209`) and SNAP (`architecture-options.md`) with single line numbers | Cites SPEC and plan only, often as line ranges (`63-65`, `100-106`, `129-136`) | Low |

## Content Differences (shared topics)

| # | Topic | Variant 1 Approach | Variant 2 Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | 15 s cycle budget not enforced (R1-01 / QA-05) | Blocking. Cites plan:97 only (each call below 15 s, five calls allowed). Fix: monotonic cycle deadline passed into `poll`, per-call timeout = min(timeout, remaining). | Blocking. Cites SPEC:369 (T5 "cycle ends within the 15 s cycle budget"), SPEC:322, plan:104 and plan:106. Fix: same min() rule plus a fake-clock test ending in `cycle overran`. | Low (same claim, same severity; V2 has stronger evidence) |
| C-002 | T33 empty states (R1-06 / QA-02) | Minor. The `empty` fixture exists (plan:75) but no rendering task or criterion carries the T33 text. | Blocking. Neither `no observed items in this source window; not proof none exist` nor `worker-list returned 0 workers in scope=bound` is built or pinned (SPEC:172, SPEC:385). | High (severity disagreement; see X-001) |
| C-003 | PARTIAL disclosure text and `reported T (page k)` (R1-07 / QA-06) | Minor. Carry last-read page and cap-stop reason into the view model; assert in screen and export tests. | Minor. Add the full text and page form to Task 8 COUNTS tokens and assert at view level; adds SPEC:349 (INV-007). | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Severity of the missing T33 empty-state rendering | R1-06: minor | QA-02: blocking | Medium |
| X-002 | Severity rule for "the instruction describes the behaviour but no acceptance criterion pins it" | Treats such gaps as minor (R1-06, R1-07) | Treats several as blocking (QA-03 paging outcomes, QA-04 FAILED (shape)) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V1 | R1-02: `_find_orca()` runs a live `skills list --json` subprocess outside the worker-list-only runner boundary, contradicting the "only live Orca call" constraint (plan:23) and T36 (plan:105) | High |
| U-002 | V1 | R1-03: `--snapshot` is written only after successful cycles (plan:173), so the frozen `source.status` values STALE/ERROR (SNAP:88) are never published | High |
| U-003 | V1 | R1-04: the "never printed" constraint (plan:25) conflicts with displaying and exporting sanitized worker free text (plan:45, plan:157) | Medium |
| U-004 | V1 | R1-05: Task 5's criterion uses the Task 4 `duplicate-out-of-order` variant but Task 5 depends only on Task 3 | Low |
| U-005 | V2 | QA-01: the missing, stale and contradictory golden fixtures are never consumed by a contract test, although SPEC section 7 keeps the R1 gate closed without all four | High |
| U-006 | V2 | QA-03: Task 6 criteria do not pin `PARTIAL (empty page k)`, `changed during read` or `(mismatch)` | Medium |
| U-007 | V2 | QA-04: no criterion maps a missing required field / two envelopes to `FAILED (shape)` end to end (T32) | Medium |
| U-008 | V2 | QA-07: T31 `cost unavailable` / never `$0` is unpinned | Low |
| U-009 | V2 | QA-08: several Task 8 texts are unpinned (`not reobserved`, placeholder, filter text, `scope unknown`, `one Run only`, NOT AVAILABLE / NOT POLLED) | Low |
| U-010 | V2 | QA-09: per-process caps must appear in help and the inspector; the criterion checks option names only | Low |
| U-011 | V2 | QA-10: `read k of N Runs since start` and T45 neither built nor excluded | Low |
| U-012 | V2 | QA-11: STALE `as of HH:MM:SS` qualifier on last-known values not built or rendered | Low |
| U-013 | V2 | QA-12: Task 1 replaces the spec's Textual switch rule with "stop as blocked" and its spike criterion cannot fail | Low |

## Shared Assumptions

Agreement points: both cards agree the cycle budget is unenforced (C-001), that T33 text is unbuilt (C-002) and that the PARTIAL disclosure is incomplete (C-003); neither card challenges the plan's authorization, export source or task ordering.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | C-002, U-008, U-011 | Every SPEC section 10 test that the plan does not explicitly exclude is in release-1 scope (some are R2 placeholders or B-view-only: T7, T10-T12, T19, T46, T47, T50, T51) | UNSTATED | Yes |
| A-002 | absence from X-NNN | The plan's authorization (plan:22, owner message 2026-11-10 plus owner-decisions items 1 and 5) clears the DIRECTION-SELECTED and production-integration gates, so live calls and CLI registration are in scope | UNSTATED | Yes |
| A-003 | absence from X-NNN | `export_text(view)` / `export_json(view)` export every collected row, even though the same view model hides historical rows by default and applies the local filter | UNSTATED | Yes |
| A-004 | U-004 | Tasks run in numeric order, so a missing `Depends on` entry is harmless | UNSTATED | Yes |
| A-005 | C-001 | The 15 s cycle budget is a hard ceiling (SPEC:369 T5) | STATED (QA-05) | No |

### Promoted [SHARED-ASSUMPTION] diff points

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | All non-excluded SPEC tests are release-1 scope | C-002, U-008, U-011 | Decides whether unpinned B-view items are findings at all | Open |
| A-002 | Plan authorization clears the gates | absence of contradiction | If false, Tasks 6 and 11 are out of scope | Open |
| A-003 | Exports carry every collected row regardless of view state | absence of contradiction | If false, the snapshot can silently drop hidden or filtered rows (SPEC:189 says historical rows are never deleted from the snapshot) | Open |
| A-004 | Numeric task order makes dependency gaps harmless | U-004 | Decides the severity of R1-05 and any similar gap | Open |

## Taxonomy tags (for the coverage gate)

| Point | Level | Signal |
|-------|-------|--------|
| S-001 | L1 | presentation |
| S-002 | L1 | style choice |
| C-001 | L3 | boundary, guard (deadline) |
| C-002 | L3 | boundary (empty collection) |
| C-003 | L2 | component wording of a paging boundary; no state change |
| X-001 | L2 | organization (severity) |
| X-002 | L2 | organization (severity rule) |
| A-001 | L2 | dependency (scope) |
| A-002 | L2 | dependency (gate) |
| A-003 | L3 | state, guard (view state vs export) |
| A-004 | L2 | dependency |

## Summary
- Total structural differences: 2
- Total content differences: 3
- Total contradictions: 2
- Total unique contributions: 13
- Total shared assumptions surfaced: 5 (UNSTATED: 4, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-002, U-001, U-002, U-005
- Similarity check: differences well above 10%; debate proceeds.
- Convergence denominator: S (2) + C (3) + X (2) + A (4) = 11 diff points.
