# Diff Analysis: decision comparison (D-P2-22, workflow.md wording)

## Metadata
- Generated: 2026-11-07
- Variants compared: 2 (Variant 1 = option A "two-line exemption", Variant 2 = option B "keep stale Contract line, delete only Nested line" with sub-variant B2 "zero deletions")
- Mode: A (compare existing files), depth quick (Round 1 only)
- Total differences found: 10 diff points in the convergence denominator (structural 2, content 4, contradictions 2, shared assumptions 2); unique contributions 2 (not in the denominator)
- Categories: structural (2), content (4), contradictions (2), unique (2), shared assumptions (2)

Evidence read in the working tree before this analysis (verified, not recalled):
- `src/superclaude/commands/workflow.md:72,75` (the working-tree text; `git diff HEAD -U0` shows exactly 2 added and 2 deleted lines, at lines 72 and 75).
- `tests/skills/test_worker_contract.py:1679-1712` (`_check_workflow_reflect_wording` and `test_workflow_section_passes_the_nested_reflect_directory`).
- `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` lines 62 (nested propagation rule), 72 (WC-4), 211 (SA-4), 222 (P2 row), 271 (AC-C5).
- `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c5.txt:18` (workflow row: `vs HEAD [2 2] (named exemption: exactly 2 deleted lines)`).
- `src/superclaude/commands/reflect.md:101` (default `--output` is `.dev/reflect/<mode>-<slug>-<ts>/`) and `:263` (under `--unattended` exactly one of `--output` or `--report-dir`).

## Structural Differences

| # | Area | Variant 1 (A) | Variant 2 (B / B2) | Severity |
|---|------|---------------|--------------------|----------|
| S-001 | Deleted lines in workflow.md | 2 (lines 72 and 75), matches the working tree and `ac-c5.txt:18` | B: 1 (line 75 only); B2: 0 | Medium |
| S-002 | Where the correction lives | In place: each false sentence is replaced by its true version | B: new line added after the stale Contract line; B2: two override lines added beside two stale lines | High |

## Content Differences

| # | Topic | Variant 1 (A) Approach | Variant 2 (B / B2) Approach | Severity |
|---|-------|------------------------|-----------------------------|----------|
| C-001 | Truth of the `## Unattended mode` section under `--unattended` | Every sentence true; the Contract line names `<report-dir>/nested/reflect-<n>/` | B: Contract line still says reflect files are in `.dev/reflect/` (false under the new call), correction placed in a separate line; B2: also keeps "runs as today, without `--unattended`" | High |
| C-002 | Spec fit: nested propagation rule (spec line 62), WC-4 / WC-11 (files inside the report dir) | Matches: reflect gets `--unattended` plus its own nested directory; contract lists it | B: stale line still points a coordinator to a path outside the report dir; B2: stale Nested line says the opposite of spec line 62 | High |
| C-003 | Test and tooling impact | The test at `test_worker_contract.py:1679-1712` already pins A's wording and asserts the old wording is absent; the AC-C5 row already records the 2-line exemption | B/B2 would fail `_check_workflow_reflect_wording` (old Contract wording must be absent) and need the test, its mutation checks and `ac-c5.txt` rewritten | Medium |
| C-004 | Presentation of change history | History stays in git | History "visible" in the file as stale plus correcting text | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | B2 (and B for the Contract line) leaves a sentence that contradicts its neighbour | No contradicting sentence remains (workflow.md:72 and :75 as edited) | B2: "runs as today, without `--unattended`" beside "receives `--unattended`"; B: `.dev/reflect/` beside `nested/reflect-<n>/` | High |
| X-002 | Whether the additive check is actually satisfied | Not satisfied for 2 lines; a named exemption is recorded (`ac-c5.txt:18`) | B still needs an exemption (1 line); only B2 satisfies the literal check | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | Variant 1 | A single, already-recorded and already-tested end state (exemption row in `ac-c5.txt`, pinned test with mutation checks) | High |
| U-002 | Variant 2 (B2) | Literal zero-deletion compliance with SA-4 / AC-C5 with no exemption | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | A worker reads the whole `## Unattended mode` section as normative and has no rule for ranking a later correcting line over an earlier stale one (UNSTATED) | Both options assume the section is read as a whole | High: decides whether B/B2 contradictions are harmless | Promoted [SHARED-ASSUMPTION] |
| A-002 | Standalone (person) runs are unaffected by either option because the section applies only when `--unattended` is a standalone token (`workflow.md:70`) (UNSTATED in both options; true in the file) | Both options leave SA-1 out of the argument | Medium: removes SA-1 as a differentiator | Promoted [SHARED-ASSUMPTION] |

## Summary
- Total structural differences: 2
- Total content differences: 4
- Total contradictions: 2
- Total unique contributions: 2
- Total shared assumptions surfaced: 2 (UNSTATED: 2, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: S-002, C-001, C-002, X-001, A-001

## Taxonomy tags (AD-5)
| Point | Level | Reason |
|-------|-------|--------|
| S-001 | L2 | organization / component boundary of the edit |
| S-002 | L2 | organization of the section |
| C-001 | L3 | invariant: every statement in the section must hold when `--unattended` is set |
| C-002 | L3 | guard / boundary: files must stay inside the report directory (WC-4, WC-11) |
| C-003 | L2 | module / interface of the pinned test |
| C-004 | L1 | presentation / wording |
| X-001 | L3 | invariant (contradicting statements) |
| X-002 | L2 | dependency on the check rule |
| A-001 | L3 | state of what the reader holds (shared-assumption rule: A-NNN with state terms tag L3) |
| A-002 | L3 | guard condition (the `--unattended` token guard) |
