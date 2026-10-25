# Diff Analysis: Tier-2 Reflection Reviewer Card Comparison (UC-2 post-execution deviation audit)

## Metadata
- Generated: 2026-10-25T00:00:00Z
- Pipeline: sc:sc-adversarial-protocol Mode A, Step 1 only (--depth standard, --focus correctness,coverage,deviation-classification)
- Variants compared: 3
  - V1 = variant-1-original.md (reviewer-1, analyzer, sonnet, calibrated 0.85)
  - V2 = variant-2-original.md (reviewer-2, qa, haiku-slot, calibrated 0.87)
  - V3 = variant-3-original.md (reviewer-3, refactorer, opus, calibrated 0.82)
- Unit of comparison: top-level YAML keys plus per-finding, per-grounding-gap, per-recommendation and per-advisory-gap entries
- Total differences found: 37 (S 8 + C 10 + X 6 + U 7, with 6 [SHARED-ASSUMPTION] points added separately)
- Categories: structural (8), content (10), contradictions (6), unique (7), shared assumptions (6 promoted)
- total_diff_points (S+C+X+A, convergence denominator): 30
- Orchestrator stance: neutral. No variant is endorsed. Severity ratings describe how much each point affects the final reflection verdict, not which variant is right.

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity | Taxonomy |
|---|------|----|----|----|----------|----------|
| S-001 | Top-level key set | 13 keys. No `advisory_correctness_gaps` | 13 keys. No `advisory_correctness_gaps` | 14 keys. Adds `advisory_correctness_gaps` (CG-1, `gating: false`) | Medium | L2 |
| S-002 | Coverage of findings per task | 3 findings: T-102 (F-1), T-101 (F-2), T-103 (F-3) | 2 findings: T-101 (F-001), T-102 (F-002). T-103 has **no finding** and appears only as grounding gap 1 | 3 findings: T-102 (R3-F1), T-101 (R3-F2), T-103 (R3-F3) | High | L2 |
| S-003 | Finding ID naming convention | `F-1..F-3` | `F-001..F-002` | `R3-F1..R3-F3` | Low | L1 |
| S-004 | Recommendation count and ordering | 2 RECs. Leads with the tier1-card edit (low), then the test run (medium) | 3 RECs. Leads with the test run (high) | 4 RECs. Leads with the test run (high) | Low | L2 |
| S-005 | Formatting of citation fields | `spec_ref` carries the R-ID label ("spec.md:9 (R-002)"). Location is a single ref | `spec_ref` has a bare line number ("spec.md:9") | Bare `spec_ref`. Location can hold several refs ("src/greeting.py:2; changes.patch:7") | Low | L1 |
| S-006 | Calibrator model class | opus | opus | sonnet | Medium | L2 |
| S-007 | Model-slot provenance header | sonnet slot | Header says "model slot haiku -> grok-4.7". `model_class: haiku-slot` | opus slot | Medium | L2 |
| S-008 | `inferred_claims` formatting | 2 claims with **no** `[INFERRED]` prefix | 3 claims, all prefixed `[INFERRED]` | 2 claims, all prefixed `[INFERRED]` | Low | L1 |

## Content Differences

| # | Topic | V1 Approach | V2 Approach | V3 Approach | Severity | Taxonomy |
|---|-------|-------------|-------------|-------------|----------|----------|
| C-001 | Static-only caveat on R-001/R-002 acceptance | Accepts T-101/T-102 as conformant. No runtime caveat on those two | "Static acceptance only ... Runtime pass unobserved (execution.log:5)". Inferred claim: "R-001 and R-002 hold at runtime; static reading only" | Accepts T-101/T-102 as conformant. No runtime caveat on those two | Medium | L2 |
| C-002 | How the falsy guard's breadth is handled (`if not name` also rejects None/0/False/[]) | Covered in the F-1 rationale. Only follow-up is REC-1: an "optional informational note on non-string falsy rejection" in the tier1 card | REC-2 (low): "optionally amend R-002 or narrow guard and add None/0/whitespace tests" | Separate advisory gap CG-1 (`gating: false`) plus REC-3 (low): "Decide R-002 scope: document falsy/whitespace rejection or narrow guard to name == \"\"" | Medium | L3 |
| C-003 | Whitespace-only input boundary | "Whitespace-only names are accepted, and R-002 does not require rejecting them" | "no criterion requires ... rejection of whitespace". Proposes whitespace tests | Gives the concrete output: whitespace strings "produce 'Hello,    !'" | Low | L3 |
| C-004 | How the package-marker claim was verified (gap 2) | "[INFERRED] No __init__.py/conftest/pytest config visible (from T1 card; **not Globbed**)" | Says "Snapshot contains no src/__init__.py, tests/__init__.py, conftest.py, or pytest/pythonpath config" but does not name the method | "No src/__init__.py, conftest.py, pytest.ini or pyproject.toml in the snapshot (**Glob lists 11 files**)" | High | L2 |
| C-005 | Treatment of completed.md:2 "status done" | Not mentioned | "completed.md:2 status done unverified". REC-1: "do not treat completed.md status done as R-003 acceptance" | "completed.md:2 status done without an executed check" | Medium | L2 |
| C-006 | Priority of the test-run recommendation | REC-2 priority **medium** | REC-1 priority **high** | REC-1 priority **high** | Medium | L2 |
| C-007 | How specific the test-run verifier is | verifier: "pytest" | "Recorded run from project root collecting test_ordinary and test_empty, exit 0 (or captured failure)" | "pytest exit 0 with 2 tests collected" | Low | L2 |
| C-008 | Owner of gap 2 (import resolution) | reviewer | reviewer | orchestrator | Low | L2 |
| C-009 | Gap between self-reported and calibrated confidence, and calibrator dimension spread | 0.82 -> 0.85. risk_surface 0.78 is the lowest | 0.78 -> 0.87 (+0.09, largest upward move) | 0.85 -> 0.82 (only downward move). coverage 0.75 and classification 0.80 are the lowest of any card | Low | L2 |
| C-010 | Next evidence needed for gap 1 (tests) | Either/or: "Run pytest from the project root, **or** include tests/ in the diff scope" | Both: "Include tests/test_greeting.py in the audited diff or scope **and** run the suite" | Run only, with stated pass criteria: "`python -m pytest` from the project root: exit 0 with 2 tests collected". Scope inclusion moves to REC-1 | Medium | L2 |

## Contradictions

| # | Point of Conflict | V1 Position | V2 Position | V3 Position | Impact | Taxonomy |
|---|-------------------|-------------|-------------|-------------|--------|----------|
| X-001 | Is R-003/T-103 accepted, and is the outcome a clean ship? | Verdict: "No deviations. T-101/T-102/T-103 map to conformant changes". F-3: "test_ordinary and test_empty cover both R-003 cases" | Verdict: "R-003 not accepted, not a clean ship: tests exist but are outside changes.patch and never executed -> grounding gap" | Verdict: "T-103 meets R-003 in content but has no execution evidence ... Calling this verified clean would be a false PASS on R-003" | High | L2 |
| X-002 | Can T-103 be classified at all? | F-3 `class: none` ("Absence from changes.patch is an evidence-scope matter, not a deviation"). Note: V1's own gap 1 also carries a `why_not_classifiable` entry, which sits uneasily with F-3 | No T-103 finding. Gap 1: "Evidence-insufficient: diff membership of the required T-103 deliverable cannot be shown from changes.patch, and passing behavior was not observed" | R3-F3 `class: none` ("cover both R-003 cases in content"). Also files gap 1 with `why_not_classifiable` | High | L2 |
| X-003 | Gap 1 `decision_needed_by_user` | `decision_needed_by_user: false` | `decision_needed_by_user: true` | `decision_needed_by_user: false` | High | L2 |
| X-004 | Gap 1 `owner` | `owner: user` | `owner: user` | `owner: orchestrator` | Medium | L2 |
| X-005 | Does running `pytest` from the project root resolve `from src.greeting import greet`? | Gap 2: "Run from the project root, or add pythonpath config". REC-2: "Run pytest from the project root to confirm tests pass and import resolves" | Gap 2: "Run the tests from the project root, or add a pythonpath / package marker". Inferred claim: "resolves only when the project root is on sys.path" | "[INFERRED] Default rootdir-prepend puts tests/ on sys.path; plain pytest may ImportError; python -m pytest from root should work (namespace package)" | Medium | L2 |
| X-006 | Which changes.patch line holds the `return f"Hello, {name}!"` line (src/greeting.py:4)? | F-2 cites "changes.patch:8". F-1 also cites "changes.patch:7-8" for the guard, so line 8 is used for both the guard/raise and the return | F-001 cites the range "changes.patch:6-9" | R3-F2 cites "changes.patch:9". R3-F1 puts the guard at changes.patch:7 | Medium | L2 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V3 | Advisory correctness gap CG-1, kept separate from deviation classes and marked `gating: false`, with the concrete whitespace output 'Hello,    !' | Medium |
| U-002 | V3 | REC-4: replace try/except/return in test_empty with `pytest.raises(ValueError)`. Its verifier, "fails if guard removed", suggests the current test may not catch removal of the guard (not verified by the card) | Medium |
| U-003 | V3 | Separates plain `pytest` (rootdir-prepend, possible ImportError) from `python -m pytest` (namespace package resolves) when collecting from the project root | Medium |
| U-004 | V3 | First-hand file-inventory evidence ("Glob lists 11 files") behind the package-marker claim | Medium |
| U-005 | V1 | REC-1 targets the Tier-1 card itself (`tier1-card.yaml`): remove DEV-1 or reclassify it as none, verifier orchestrator | Low |
| U-006 | V2 | Explicit rule against reading completed.md "status done" as R-003 acceptance. The verifier also accepts "(or captured failure)" as a valid recorded outcome | Medium |
| U-007 | V2 | Hands the T-103 scope/diff-membership decision to the user (`decision_needed_by_user: true`), making R-003 acceptance a user decision | Medium |

## Shared Assumptions

### Agreement points (all three variants converge)
- AG-1: DEV-1 is reclassified from Drift to `none` because the change maps to T-102 (completed.md:7) and implements R-002.
- AG-2: T-101/R-001 conforms (f-string returns exactly "Hello, Ada!").
- AG-3: `deviation_count_by_class` is 0/0/0/0 and `regression_present: false`.
- AG-4: tests/test_greeting.py exists on disk, is outside changes.patch, covers both R-003 cases in content, and was never executed (execution.log:5).
- AG-5: Import resolution of `src.greeting` is a grounding gap, not a deviation or regression. Every card recommends running the tests from the project root as closing evidence.
- AG-6: The falsy-guard breadth is low priority and does not gate.
- AG-7: All calibrations carry `spot_check_not_performed`.

### Precondition enumeration

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| P-01 | AG-1 | Drift requires a change that maps to no tasklist item | STATED (all three) | No |
| P-02 | AG-1 | completed.md is an authoritative, faithful proxy for the planned tasklist, so mapping to completed.md:7 equals mapping to the planned T-102 | UNSTATED | A-001 |
| P-03 | AG-1 / AG-6 | A mapped change whose guard rejects more inputs than the spec literally requires is class `none`, not Authorized expansion (the cards never consider the expansion class) | UNSTATED | A-002 |
| P-04 | AG-1 | spec.md:9 is the full text of R-002 | STATED ("R-002 is silent", "no criterion requires") | No |
| P-05 | AG-2 / AG-3 | spec.md lists the complete requirement set (R-001..R-003) and there is no implicit invariant or type contract on `name` | UNSTATED | A-003 |
| P-06 | AG-2 / AG-3 | Static reading is enough for a `none` class without execution | STATED (V2 caveat, V1/V3 inferred_claims for tests) | No |
| P-07 | AG-3 | A regression needs an observed broken criterion; unobserved failure is not a regression | STATED (V2 gap 2: "failure not observed, so not a regression") | No |
| P-08 | AG-4 | execution.log:5 is a complete record (no out-of-band test run took place) | STATED (all cite execution.log:5) | No |
| P-09 | AG-4 | tests/test_greeting.py on disk is the T-103 deliverable produced by this execution, not a pre-existing or externally modified file | UNSTATED (V2 questions diff membership but not provenance) | A-004 |
| P-10 | AG-1..AG-4 | The reviewer snapshot's file contents match the audited post-execution working tree byte for byte (the header only says it "mirrors the fixture project paths") | UNSTATED | A-005 |
| P-11 | AG-5 | Running from the project root is enough for import resolution | CONTRADICTED (V3 inference that plain pytest may ImportError conflicts with V1/V2; see X-005) | No (flagged for debate) |
| P-12 | AG-6 | No caller of greet() passes non-string values or relies on non-ValueError behavior for falsy non-strings, so the guard's breadth is safe to leave non-gating | UNSTATED | A-006 |
| P-13 | AG-7 | Calibrated confidence without a spot check is good enough for weighting | STATED (notes field) | No |

### Promoted [SHARED-ASSUMPTION] diff points

| A-NNN | Assumption | Source Agreement | Impact | Status | Taxonomy |
|-------|-----------|------------------|--------|--------|----------|
| A-001 | [SHARED-ASSUMPTION] completed.md is an authoritative, faithful proxy for the planned tasklist, so a change mapped to completed.md:7 is mapped to the planned T-102 | AG-1 | Medium | UNSTATED, promoted | L2 |
| A-002 | [SHARED-ASSUMPTION] A mapped change whose guard rejects a wider input set (None/0/False/[]) than the spec literally requires is class `none` rather than Authorized expansion. The taxonomy boundary between "conformant" and "expansion" is assumed, never argued | AG-1, AG-6 | Medium | UNSTATED, promoted | L3 |
| A-003 | [SHARED-ASSUMPTION] spec.md lists the complete requirement set (R-001..R-003) and there is no implicit invariant or type contract on `name` that the falsy guard could violate | AG-2, AG-3 | Medium | UNSTATED, promoted | L3 |
| A-004 | [SHARED-ASSUMPTION] tests/test_greeting.py on disk is the T-103 deliverable produced by this execution, not a pre-existing or externally modified file, even though it is outside changes.patch | AG-4 | High | UNSTATED, promoted | L2 |
| A-005 | [SHARED-ASSUMPTION] The reviewer snapshot's file contents are byte-identical to the audited post-execution working-tree state (the header only claims path mirroring) | AG-1..AG-4 | Medium | UNSTATED, promoted | L3 |
| A-006 | [SHARED-ASSUMPTION] No caller of greet() passes non-string values or relies on non-ValueError behavior for falsy non-strings, so the guard's breadth can stay non-gating | AG-6 | Low | UNSTATED, promoted | L3 |

CONTRADICTED precondition flagged for debate: P-11 (overlaps X-005).

## Taxonomy Tagging Summary
- L1 surface: S-003, S-005, S-008
- L2 structural: S-001, S-002, S-004, S-006, S-007, C-001, C-004, C-005, C-006, C-007, C-008, C-009, C-010, X-001, X-002, X-003, X-004, X-005, X-006, A-001, A-004
- L3 state-mechanics: C-002, C-003, A-002, A-003, A-005, A-006
- Rule applied: guard/boundary/validation/invariant/state signal terms -> L3; L3 > L2 > L1; default L2. Every point carries exactly one level. L3 coverage is non-empty, so state-mechanics debate cannot be bypassed.

## Similarity Check
- Comparable items counted: 37 (14 top-level keys, 3 per-task finding slots, 2 grounding gaps x 6 fields = 12, 6 distinct recommendation intents, 2 calibration fields: model and calibrated value).
- Differences on those items (S + C + X): 24, about 65%.
- Threshold: <10%. **Not met. The variants are not substantially identical. Debate should proceed (Steps 2-3).**

## Load-bearing points for the final reflection verdict (orchestrator note, neutral)
- X-001 / X-002: whether R-003 is "satisfied in content" (V1, V3) or "not accepted / unclassifiable" (V2). V3 sits in between ("meets in content", but "false PASS" if called verified clean).
- X-003 / X-004: gap 1 `decision_needed_by_user` (V2 true; V1, V3 false) and `owner` (user vs orchestrator). This decides whether the final report needs a user decision.
- C-004: first-hand verification of the package-marker claim. V1 states it did not Glob and relied on the T1 card. V3 Globbed (11 files). V2 asserts contents without naming a method.
- S-001 / U-001: the advisory correctness gap (CG-1) appears only in V3. C-002 shows that V1 and V2 relegate the same guard-breadth observation to low-priority REC text.
- C-010: whether closing evidence for gap 1 is "run OR scope" (V1), "scope AND run" (V2), or "run with explicit pass criteria" (V3).

## Summary
- Total structural differences: 8
- Total content differences: 10
- Total contradictions: 6
- Total unique contributions: 7
- Total shared assumptions surfaced: 13 preconditions (UNSTATED: 6 promoted as A-001..A-006, STATED: 6, CONTRADICTED: 1)
- total_diff_points (S+C+X+A): 30
- Highest-severity items: S-002, C-004, X-001, X-002, X-003, A-004
- Similarity verdict: ~65% differing (> 10%), so debate proceeds
