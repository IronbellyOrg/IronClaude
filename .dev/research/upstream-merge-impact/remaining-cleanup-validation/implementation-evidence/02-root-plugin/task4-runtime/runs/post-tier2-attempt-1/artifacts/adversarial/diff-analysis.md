# Diff Analysis: Tier-2 Deviation-Audit Reviewer Card Comparison

## Metadata
- Generated: 2026-10-24T19:46:03Z
- Step: 1 (Diff Analysis) only — produced by neutral sc:debate-orchestrator; no debate, no advocacy
- Mode: A (compare) | Depth: standard | Focus: correctness, coverage, deviation-classification
- Variants compared: 2
  - Variant A = `variant-1-original.md` (reviewer 1, sonnet:analyzer, self-reported 0.80)
  - Variant B = `variant-2-original.md` (reviewer 2, haiku:qa, self-reported 0.76)
- Evidence base for factual checks: `runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/` (spec.md, changes.patch, src/greeting.py, tests/test_greeting.py, execution.log, completed.md, `__run_evidence__/{t1-card.md, artifacts/*, verify-logs/invocations.yaml}`); plus fixture `fixtures/project/proposed.md` (read only to test assumption A-006; it is not in the reviewer snapshot)
- Total differences found: 37 (S+C+X+U)
- Categories: structural (8), content (15), contradictions (3), unique (11), shared assumptions (9; promoted [SHARED-ASSUMPTION]: 4)
- Diff points entering debate (S+C+X+promoted A): 30
- Taxonomy distribution (S/C/X/A, 35 tagged points): L1 = 2, L2 = 25, L3 = 8

## Structural Differences

| # | Area | Variant A | Variant B | Severity | Level |
|---|------|-----------|-----------|----------|-------|
| S-001 | Top-level card sections | No coverage section; per_task, deviations, grounding_gaps, risks, recommendations, confidence | Adds a `coverage_audit` section (spec-span coverage statement) in addition to the same sections | Medium | L2 |
| S-002 | D-1 deviation record schema | Includes a `severity: LOW` field | No severity field on D-1 | Medium | L2 |
| S-003 | Per-task verdict vocabulary | Free-text wording ("implemented (static only)", "implemented on disk, unrun, outside supplied diff") | snake_case token naming convention (`statically_met`, `statically_met_with_drift`, `static_cases_present_runtime_unproven`) | Low | L1 |
| S-004 | grounding_gaps `hunk_ref` | Concrete file refs (`tests/test_greeting.py:1`, `tests/test_greeting.py (outside changes.patch)`) | `none` for all three gaps | Low | L2 |
| S-005 | grounding_gaps `decision_needed_by_user` type (interface of the gap record) | String stating the decision question | Boolean (`true` / `false` / `false`) | Medium | L2 |
| S-006 | Grounding-gap organization / granularity | 2 gaps: (1) no execution + no packaging config folded together, (2) tests-file provenance | 3 gaps: (1) tests-file diff omission, (2) no runner output, (3) packaging/import | Medium | L2 |
| S-007 | Citation path formatting | Mixed: `__run_evidence__/verify-logs/invocations.yaml:2` once, bare filenames elsewhere | Bare filenames throughout (`invocations.yaml:2`, `t1-card.md:19-20`) | Low | L1 |
| S-008 | Recommendation set organization | 3 items targeting t1-card.md, src/greeting.py, tests/test_greeting.py | 4 items targeting src/greeting.py, tests/test_greeting.py (x2), changes.patch | Low | L2 |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity | Level |
|---|-------|-------------------|-------------------|----------|-------|
| C-001 | T-101 (R-001) per-task verdict | "implemented (static only)"; evidence greeting.py:4, changes.patch:9, tests:4-5, invocations.yaml:2 | "statically_met"; same evidence plus spec.md:6 and execution.log:5 (no-run disclaimer). Substantively equivalent | Low | L2 |
| C-002 | T-102 (R-002) per-task verdict vs D-1 guard | "implemented (static only)" — verdict does not carry the D-1 guard finding even though D-1 maps to T-102 | "statically_met_with_drift" — verdict explicitly links the guard broadening (D-1) | Medium | L3 |
| C-003 | T-103 (R-003) per-task verdict and completion claim | "implemented on disk, unrun, outside supplied diff"; does not challenge completed.md:8 `[x]` | "static_cases_present_runtime_unproven"; asserts completed.md:8 `[x]` and `tasklist_completion_pct 1.0` (task-to-work-map.yaml:33) "overclaim acceptance"; also says T1 G-2 is "too broad: exercise is statically visible" (note: this sits in tension with B's own "R-003 not accepted absent execution") | High | L2 |
| C-004 | D-1 classification and hedging (`if not name` guard) | `drift`, severity LOW, with explicit counter-view: "`not name` is a common idiom for 'empty' and could be read as adherent/no deviation; either way not 'authorized'" | `drift`, unhedged: "unstated broadening with no rationale -> Drift"; no no-deviation alternative offered | High | L3 |
| C-005 | D-1 "Necessary deviation" elimination test for the guard | "no documented forcing constraint (Necessary fails)" | "no inline rationale and `name == \"\"` would have sufficed -> not Necessary" (counterfactual-alternative argument) | Medium | L3 |
| C-006 | Grounding gap: tests file absent from supplied diff | Gap 2; "no HEAD baseline (task-to-work-map.yaml:35-36)"; decision: "whether omission from supplied diff is acceptable" | Gap 1; "no git history"; next evidence: diff incl. tests or widened scope `src/,tests/`; decision_needed_by_user: true. Both agree user decision is required | Low | L2 |
| C-007 | Grounding gap: no test execution (runtime) | Folded into gap 1 with the import question; decision_needed_by_user: "whether static presence suffices for T-103 done" | Separate gap 2; "pass/fail not observable; unrun != contradiction"; flags T1 G-2 citation defect ("execution.log:5 does not prove tool unavailability"); decision_needed_by_user: false | High | L2 |
| C-008 | Grounding gap: packaging / import of `src.greeting` module | Gap 1 (shared with execution) + separate [INFERRED] risk of ModuleNotFoundError; cites absence of src/__init__.py / conftest | Gap 3; [INFERRED] plain-pytest import failure not observed; decision_needed_by_user: false | Low | L2 |
| C-009 | Risks: boundary inputs at the guard | "extra falsy handling untested"; "test_empty ... only exercises ''" | Whitespace input returns a greeting (greeting.py:2,4) [INFERRED blank-vs-empty]; non-string truthy input interpolated (greeting.py:4); test accepts any ValueError, message unchecked | Medium | L3 |
| C-010 | Risks: verification / acceptance | "Verification triangle did not run (invocations.yaml:2-3); all verdicts static" | "R-003 not accepted absent execution; completion 1.0 is not an acceptance pass"; "interaction-effects coverage is static only; must not become runtime clearance" | Medium | L2 |
| C-011 | Risks: shared-component coupling T-101/T-102 | Explicit risk: shared-function coupling (cites interaction-effects.yaml:14-21) | Not raised as coupling; only notes interaction-effects is static-only | Low | L2 |
| C-012 | Recommendations: D-1 guard remediation | (a) reclassify T1 D-1 "authorized -> Drift (LOW) or no-deviation"; (b) narrow guard to `name == ""` OR record rationale/spec amendment; verifier greet('') raises, greet('Ada') == 'Hello, Ada!' | Narrow line 2 to empty-string check OR "stop calling falsy broadening authorized"; verifier = re-read greeting.py:2-3 vs spec.md:9 and tests:10 | Medium | L3 |
| C-013 | Recommendations: test / evidence remediation | Single item: run suite with real pytest, attach log under verify-logs | Three items: replace try/except (tests:8-13) with explicit ValueError assertion; regenerate changes.patch incl. tests or widen scope; make src importable (root conftest.py / pythonpath) | Medium | L2 |
| C-014 | Citation accuracy (re-read against snapshot) | All per-task/D-1/gap citations resolve; **defect**: `interaction-effects.yaml:14-21` — file has only 13 lines (relevant content is :4-12) | All checked citations resolve (spec.md:6/9/12, t1-card.md:19-20 and the G-2 text at :33-34, task-to-work-map.yaml:30-31/:33, invocations.yaml:2-4). Its G-2 critique is accurate about execution.log:5 but does not mention invocations.yaml:3, which does record `verification_skip_reason: tool-unavailable` (with note that Bash was deliberately not substituted) | Medium | L2 |
| C-015 | Self-reported confidence | 0.80 (prerequisites.md records calibrated 0.82) | 0.76 (prerequisites.md records calibrated 0.84) — calibration ordering inverts self-report ordering | Low | L2 |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact | Level |
|---|-------------------|-------------------|-------------------|--------|-------|
| X-001 | Is T-103 / R-003 done on static evidence? | Verdict "implemented on disk, unrun, outside supplied diff"; leaves it open: decision_needed_by_user "whether static presence suffices for T-103 done" | "completed.md:8 [x] and tasklist_completion_pct 1.0 (task-to-work-map.yaml:33) overclaim acceptance"; risk "R-003 not accepted absent execution" | High | L2 |
| X-002 | Does the runtime-execution gap require a user decision? | Gap 1 decision_needed_by_user: "whether static presence suffices for T-103 done" | Gap 2 (no runner output) `decision_needed_by_user: false`; Gap 3 (import) `false` | Medium | L2 |
| X-003 | Is "no deviation" an admissible outcome for the `if not name` guard? | "could be read as adherent/no deviation"; recommendation "Reclassify D-1 authorized -> Drift (LOW) or no-deviation" | "unstated broadening with no rationale -> Drift"; "`name == \"\"` would have sufficed -> not Necessary" — Drift is the only outcome offered | High | L3 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | B | `coverage_audit`: no requirement-bearing spec span missing from slice; spec.md:1-3 non-normative (verified: spec.md:3 "synthetic audit input") | Medium |
| U-002 | B | Flags tasklist completion overclaim: completed.md:8 `[x]` and task-to-work-map.yaml:33 `tasklist_completion_pct: 1.0` vs unrun tests | High |
| U-003 | B | Critiques T1 card G-2: execution.log:5 cited as proof of tool unavailability (t1-card.md:33) is a citation defect; G-2 "cannot confirm tests exercise the code" (t1-card.md:34) is over-broad | Medium |
| U-004 | B | Whitespace-only and non-string input risks (greeting.py:2,4) — carried forward from t1-card.md:38-39 | Low |
| U-005 | B | test_empty accepts any ValueError; message unchecked (and notes spec does not require message) | Low |
| U-006 | B | Concrete remediation for tests/diff: explicit ValueError assertion, regenerate diff / widen scope, root conftest.py or pythonpath (mirrors t1-card.md:45-47) | Medium |
| U-007 | A | Shared-function coupling risk T-101/T-102 from interaction-effects (citation line range defective, see C-014) | Low |
| U-008 | A | Assigns D-1 a severity (LOW) | Low |
| U-009 | A | Counter-view that `if not name` may be adherent / no deviation (feeds X-003 and A-001/A-002) | High |
| U-010 | A | Recommendation aimed at the T1 card itself with a rule-level verifier: "every 'authorized' item cites an explicit approving artifact" | Medium |
| U-011 | A | Alternative remediation path: keep broad guard but "record rationale/spec amendment for rejecting all falsy input" | Medium |

## Shared Assumptions

Agreement points scanned: both classify D-1 as Drift and reject T1's "authorized"; both treat all verdicts as static-only; both credit T-103 as implemented-on-disk; both treat greeting.py and changes.patch as interchangeable evidence; both search for an approving artifact and find none; both carry the [INFERRED] plain-pytest import risk.

| # | Agreement Source | Assumption | Classification | Promoted | Level |
|---|------------------|-----------|----------------|----------|-------|
| A-001 | C-004 (both: D-1 = Drift) | The `if not name` guard broadening is a deviation from R-002 at all (spec.md:9 only requires that empty input be rejected; greet('') does raise) | STATED (Variant A counter-view raises "adherent/no deviation"; Variant B does not) | No — flagged for debate via X-003 | L3 |
| A-002 | C-004, C-005 (both treat broadening as substantive) | For `str` input, `not name` is equivalent to `name == ""`; the broadening only bites for non-str falsy values (None, 0, [], False), where the spec is silent and `greet` has no type contract. Both variants treat it as a behavioural divergence within the spec's domain (B: "`name == \"\"` would have sufficed") without stating this equivalence | UNSTATED | Yes — [SHARED-ASSUMPTION] | L3 |
| A-003 | C-001..C-003, C-010 (both: static-only) | Static evidence is the only evidence available; no runtime evidence exists | STATED (A: invocations.yaml:2-3; B: invocations.yaml:2-4). Note invocations.yaml:3 shows the skip was an orchestrator surface choice ("did not substitute Bash"), not proof that execution was impossible | No | L2 |
| A-004 | C-006 (both: provenance gap) | Provenance of tests/test_greeting.py is unverified (untracked file, git init only — task-to-work-map.yaml:35-36) | STATED (both raise it as a grounding gap) | No | L2 |
| A-005 | C-003 (both credit T-103 as executor work) | The omitted test file was genuinely authored by the executor as T-103 work. Both per-task T-103 verdicts credit it on the sole basis of the executor's self-report (execution.log:4) and are not conditioned on the provenance gap they themselves raise (A-004) | UNSTATED | Yes — [SHARED-ASSUMPTION] | L2 |
| A-006 | C-004 (both: "no approving artifact") | The reviewer snapshot is complete for the authorization search (no approving artifact exists outside it). The snapshot omits fixtures/project/proposed.md; on read, proposed.md:7 ("Reject an empty name using ValueError.") does not authorize falsy broadening, so the assumption holds in fact but neither variant states its search scope | UNSTATED | Yes — [SHARED-ASSUMPTION] | L2 |
| A-007 | C-001, C-002 (both cite greeting.py and changes.patch interchangeably) | On-disk src/greeting.py is identical to the changes.patch hunk (verified identical by re-read: changes.patch:6-9 = greeting.py:1-4) | UNSTATED | Yes — [SHARED-ASSUMPTION] | L2 |
| A-008 | C-008 (both: [INFERRED] import risk) | Plain `pytest` would fail to import `src.greeting` module (no conftest/ini/`__init__.py`); inherited from t1-card.md:40 | STATED (both mark [INFERRED]) | No | L2 |
| A-009 | C-004, C-012 (both reject T1 "authorized") | Authorized expansion requires an explicit approving artifact; mapping a change to a task is insufficient (contrary to t1-card.md:20) | STATED (A verifier: "every 'authorized' item cites an explicit approving artifact"; B: "No approving artifact ... -> not Authorized") | No | L2 |

### Promoted [SHARED-ASSUMPTION] Points

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|-----------|------------------|--------|--------|
| A-002 | `not name` == `name == ""` for str input; broadening affects only non-str falsy values outside the spec's stated domain | C-004, C-005 | High — could downgrade D-1 to no-deviation or to an unspecified-input note; directly bears on X-003 | UNSTATED, open for debate |
| A-005 | T-103 credit assumes executor authorship of an untracked, out-of-diff test file | C-003 | Medium — affects T-103 verdict and X-001 | UNSTATED, open for debate |
| A-006 | Snapshot is the complete authorization search space | C-004 | Low — verified to hold (proposed.md does not authorize) | UNSTATED, open for debate (likely ACCEPT) |
| A-007 | On-disk source equals the supplied diff | C-001, C-002 | Low — verified to hold | UNSTATED, open for debate (likely ACCEPT) |

## Summary
- Total structural differences: 8
- Total content differences: 15
- Total contradictions: 3
- Total unique contributions: 11
- Total shared assumptions surfaced: 9 (UNSTATED: 4, STATED: 5, CONTRADICTED: 0)
- Highest-severity items: C-003, C-004, C-007, X-001, X-003, U-002, U-009, A-002
- Taxonomy coverage: L1 = 2 (S-003, S-007); L2 = 25; L3 = 8 (C-002, C-004, C-005, C-009, C-012, X-003, A-001, A-002). All three levels covered.
- Factual check notes for debaters: Variant A has one out-of-range citation (interaction-effects.yaml:14-21; file is 13 lines). Variant B's G-2 critique is accurate re execution.log:5 but omits invocations.yaml:3. Variant B carries an internal tension (C-003: "exercise is statically visible" vs "R-003 not accepted absent execution").

## Similarity Check
- Comparable items: 23 (3 per-task verdicts, 6 D-1 fields, 3 grounding-gap slots, 5 risk slots, 4 recommendation slots, coverage section, confidence)
- Items differing materially: 18 of 23 (~78%); identical or substantively equivalent: D-1 class, D-1 location/mapped_task/spec_section, T-101 verdict substance
- Threshold: < 10% => substantially identical
- Verdict: **NOT substantially identical** — debate (Steps 2-3) proceeds.
