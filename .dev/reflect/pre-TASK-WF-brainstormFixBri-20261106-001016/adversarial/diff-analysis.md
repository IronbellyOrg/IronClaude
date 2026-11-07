# Diff Analysis: reviewer-card comparison (plan audit of TASK-WF-brainstormFixBri-20261106-001016)

## Metadata

- Generated: 2026-11-06T00:35Z
- Variants compared: 3 (V1 = reviewer-1 analyzer/sonnet, V2 = reviewer-2 qa/haiku slot, V3 = reviewer-3 refactorer/opus)
- Variant files: `variant-1-original.md`, `variant-2-original.md`, `variant-3-original.md` (this folder)
- Subject of all three cards: the 7-task plan `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md` against its brief `source.md`
- Calibrated confidence per card (blind): V1 0.85, V2 0.82, V3 0.82
- Total differences found: 24 scored points (structural 2, content 13, contradictions 5, shared assumptions 4) plus 6 unique contributions
- Categories: structural (2), content (13), contradictions (5), unique (6), shared assumptions (4)
- Taxonomy levels: L1 surface wording, L2 structural, L3 state and guard mechanics (tag in the Level column)

Facts checked on disk by the orchestrator while writing this file (use them as ground truth in the debate):
- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:187` offers `/sc:analyze` OR `mcp__auggie__codebase-retrieval` as the codebase row; line 198 defines `primary` as "first-choice source ran cleanly"; line 199 defines `fallback_1` and is inside Wave 2A (lines 175-208); line 201 records `enrichment_used: [{source, quality_tier}, ...]`.
- `SKILL.md:195` (the `Under --unattended` paragraph) does NOT contain the string `fallback_1`.
- Spec line 142 is under `### 3.1 Ready with brief constraints (12)` (lines 136-153); `## 6. Phased rollout` starts at line 215.
- The plan (`plan:81`) calls line 142 "the `brainstorm` row of the section 6 table".
- Baseline `git status --porcelain` today has 950 staged `A` entries under `.dev/tasks/done/TASK-WF-p1LivePlanBrief-` (artifacts/diagnostics.txt:3-7).

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Findings count and P1 count | 10 findings, 2 P1 | 8 findings, 2 P1 | 9 findings, 2 P1 | Low |
| S-002 | Use of INFERRED tag | 1 finding (R1-5) | none (all Grounded) | 1 finding (R3-9) | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity | Level |
|---|-------|----|----|----|----------|-------|
| C-001 | Task 7 third acceptance bullet cannot pass on today's tree | R1-2 P1: cannot pass; use a before/after status diff; did not run git | R2-1 P1: also the first clause ("only six files plus package among tracked paths") fails: "doubly unpassable" | not raised | Medium | L3 |
| C-002 | New `fallback_1` assertion in Task 4 passes on the old text | R1-1 P1: also says Task 1's first acceptance clause is vacuous | R2-3 P2: Task 4 AC3 is false for this assertion | R3-3 P2: same, plus Task 1 stays untested | Medium | L2 |
| C-003 | Task 7 omits `tests/skills/test_codegraph_adoption.py` | R1-7 P2 (also names `test_tier2_tavily_consistency.py`) | R2-5 P2 (names both files) | R3-2 P1 | Medium | L2 |
| C-004 | The owner's core rule ("nested analyze directory exists only when /sc:analyze ran; fallback lists no nested contract") is pinned by no test in the primitives | R1-4 P2: add a second exact phrase everywhere | R2-2 P1: unpinned; an implementer can drop it and every check passes | not raised as unpinned; R3-6 proposes one shared short phrase | High | L2 |
| C-005 | Routing-ref pin (`writes no nested directory` at least twice) is file-wide, not one per codebase tier | R1-3 P2: scope the test to the codebase section, one per tier | not raised | R3-3 (second half) P2: same | Low | L2 |
| C-006 | Task 6 placement (spec section 2.1 bullet) | R1-8 P2: defensible, say so, add a pointer from 7.2 step 4 | R2-4 P2: defensible, but the brief's procedure is not evaluated | R3-5 P2: wrong spot; split the general rule (2.1) from the live-check sentence (7.2 step 4 or 7.3) | Medium | L2 |
| C-007 | Task 6 wording "a `primary` or `fallback_1` scan is recorded as the tier used, with no nested folder" | R1-5 P2 INFERRED: an analyze run is also `primary`; say "an auggie scan (tier primary)" | not raised | R3-1 P1 Grounded: a checker following it fails a correct analyze run; decide by the `source` field of `enrichment_used`, not by `quality_tier` | High | L2 |
| C-008 | Task 5 collect-only check has no recorded baseline | R1-6 P2 | R2-7 P2 (baseline 17 is in diagnostics.txt:11) | R3-7 P2 | Low | L1 |
| C-009 | Task 2 says each tier list "ends with its `quality_tier` line"; Tier 2 ends with the Activation bullet (handoff-routing.md:31) | R1-10 (part) P2 | R2-6 P2 | not raised | Low | L1 |
| C-010 | Stale line numbers in the plan (Task 4 "line 37" vs 39; Task 5 "line 286" for the list vs 288) and the brief's line-711 reference | R1-9: line 711 is a synthetic-section mutation, needs no change | R2-8: confirms offsets 39 and 288, and the 711 note | not raised | Low | L1 |
| C-011 | Task 6 says "the `brainstorm` row of the section 6 table (line 142)"; line 142 is in section 3.1 | not raised | not raised | R3-4 P2 | Low | L1 |
| C-012 | Phrase variants "write" (skill) vs "writes" (ref and command): each file is held to its own verb form | not raised | not raised | R3-6 P2: use one shared phrase such as "no nested directory" | Low | L1 |
| C-013 | Extra affected test files and reasoning about the plugin copy | R1-7 names two extra test files | R2-5 names two extra test files | R3-8: `test_codegraph_adoption.py` reads the plugin brainstorm.md, so the plan's "no test requires parity" reasoning is incomplete | Low | L2 |

## Contradictions

| # | Point of Conflict | V1 Position | V2 Position | V3 Position | Impact |
|---|-------------------|-------------|-------------|-------------|--------|
| X-001 | Is Task 1's first acceptance clause ("the Wave 2A paragraph ... contains `fallback_1`") vacuous on the old text? | Yes (R1-1 says Task 1's clause also passes) | Says only Task 4's assertion is vacuous | Says Task 1's clause "stays untested" | Medium: `plan:33` scopes Task 1's clause to the one `Under --unattended` paragraph (SKILL.md:195), which lacks `fallback_1`, so for Task 1 it is NOT vacuous |
| X-002 | Severity of the missing `test_codegraph_adoption.py` run | P2 | P2 | P1 (calibrator 3: adding a bullet inside Tier 2 would not break that test) | Medium |
| X-003 | Is the `primary`/analyze wording problem real and how serious? | P2 INFERRED | silent | P1 Grounded | High |
| X-004 | Is the section 2.1 placement of the live-check wording acceptable? | defensible | defensible, unevaluated | wrong spot | Medium |
| X-005 | Does Task 7's third bullet fail once or twice on today's tree? | cannot pass (the `.dev/tasks/done/` clause) | fails in both its first clause and its `done/` clause | silent | Medium: staged `A` entries are tracked paths (first clause fails); whether staged `A` counts as "modified" (second clause) depends on how "modified" is read |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V2 | R2-2: the core owner rule has no pin in any primitive | High |
| U-002 | V3 | R3-1: decide by the `source` field, not `quality_tier` | High |
| U-003 | V3 | R3-4: wrong section label for spec line 142 | Medium |
| U-004 | V1 | R1-3 / V3 R3-3: scope the routing-ref test to the codebase section, one bullet per tier | Medium |
| U-005 | V3 | R3-9 INFERRED: the command-file addition repeats the skill text and omits the "nested contract listed in `artifacts` only for a nested command that ran" clause | Low |
| U-006 | V1 | R1-10: Task 7 says "do not edit any file" but saves logs under `./artifacts/` | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|------------|------------------|----------------|--------|--------|
| A-001 | Adding the new bullets and sentences leaves `test_codegraph_adoption.py` and `test_tier2_tavily_consistency.py` passing. No card ran either test; all three reason from reading the source | C-003, C-013 | UNSTATED | If false, Task 7 misses a break; if true, the P1 rating of C-003 is too high. This is an invariant of the edited Tier 2 block. | Promoted |
| A-002 | `/sc:implement` judges each acceptance bullet literally (a pass/fail check), so an unpassable bullet blocks completion; a semantic reader would let it pass | C-001, X-005 | UNSTATED | Decides whether the C-001 finding is a blocker (P1) or a wording nit (P2). This is a guard-condition (validation rule) question. | Promoted |
| A-003 | Exact-substring tests are the right way to pin the new wording | C-002, C-004, C-005, C-012 | STATED | All three cards accept it; it sets the remedy shape (add a phrase) rather than challenging it | Not promoted |
| A-004 | The tree state at execution time equals today's state (the staged P1 archive stays; no other session changes `.dev/tasks/done/` or the six files in between). A state change would alter every baseline-dependent check | C-001, C-008, X-005 | UNSTATED | Baseline-dependent checks (status diff, collect-only count) only hold if this state persists | Promoted |

## Summary

- Total structural differences: 2
- Total content differences: 13
- Total contradictions: 5
- Total unique contributions: 6
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-004, C-007, X-003
- Scored diff points (denominator for convergence): S 2 + C 13 + X 5 + A 4 = 24
