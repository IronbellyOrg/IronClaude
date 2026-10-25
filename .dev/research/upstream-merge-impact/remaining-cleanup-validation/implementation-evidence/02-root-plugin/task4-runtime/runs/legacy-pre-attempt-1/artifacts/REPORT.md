# sc:reflect — FINAL — Pre-execution (UC-1) audit: proposed greeting plan vs spec

```yaml
contract_version: 1.8.0
status: partial            # grounding-gaps.yaml non-empty (§10.6) -> needs_human_decision: true
mode: pre
tier_reached: 1
confidence_calibrated: 0.93
citations_total: 9
citations_revalidated: 9
citations_dropped: 0       # sc:evidence-validator verified 9/9 (zero-drop-flag audited)
citations_inferred: 5
citation_budget_policy: full_reread
coverage_degraded: null
```

Path legend: `SPEC` = /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/fixtures/project/spec.md ; `PLAN` = /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/fixtures/project/proposed.md

## Evidence

Coverage matrix (Pass 1 exact ID match; Pass 2 inference emitted 0 rows — all MUST bodies sit inside parsed spans):

| Req | Spec citation | Task | Plan citation | ID match | Semantic verdict |
|---|---|---|---|---|---|
| R-001 | `SPEC:6` — "The greet function MUST return the exact string Hello, Ada! for Ada." | T-101 | `PLAN:4` — "Implement greet(name) returning the required greeting." | exact | partial |
| R-002 | `SPEC:9` — "The greet function MUST reject an empty name with ValueError." | T-102 | `PLAN:7` — "Reject an empty name using ValueError." | exact | covered |
| R-003 | `SPEC:12` — "Tests MUST exercise the ordinary greeting and empty-input rejection." | T-103 | `PLAN:10` — "Add ordinary and empty-name test cases." | exact | partial |

ID traceability anchors: `PLAN:3` — "## T-101 R-001"; `PLAN:6` — "## T-102 R-002"; `PLAN:9` — "## T-103 R-003".

- coverage_pct = 1.0 (3/3), coverage_pct_union = 1.0, unmapped_requirements = [], S_scope 3, S_domains 2, S_dev_density 0.0.
- best_practice_grade: 3/5.

## Deviations

### Deviation D-1: T-101 does not restate the exact required output string
- **Location:** PLAN:4
- **Mapped tasklist item:** T-101
- **Spec section:** R-001 (SPEC:6)
- **Evidence:** "Implement greet(name) returning the required greeting." (PLAN:4)
- **Classification:** drift
- **Classification rationale:** Under-specification of an exact-string MUST; does not contradict R-001, so not regression.
- **Default remediation:** Amend T-101 to state `greet('Ada') == 'Hello, Ada!'` (exact match) as acceptance.
- **[INFERRED] notes:** [INFERRED] An implementer could choose a different format and still claim T-101 is done.

### Deviation D-2: T-103 does not define test assertions or a run/pass step
- **Location:** PLAN:10
- **Mapped tasklist item:** T-103
- **Spec section:** R-003 (SPEC:12)
- **Evidence:** "Add ordinary and empty-name test cases." (PLAN:10)
- **Classification:** drift
- **Classification rationale:** Tests could exist without asserting the exact string or ValueError; under-specification, not contradiction.
- **Default remediation:** Require assertions on `'Hello, Ada!'` and `ValueError` plus a final passing test run.
- **[INFERRED] notes:** [INFERRED] No test-run/exit step appears anywhere in the plan.

No regression (no planned task contradicts a spec MUST); no authorized/necessary deviations; no out-of-spec scope.

## Grounding Gaps

### Gap G-1
- **Hunk ref:** SPEC:9
- **Evidence missing:** Spec says only "reject an empty name"; whitespace-only, None and non-string input unaddressed.
- **Why not classifiable:** No spec intent stated, so the plan's silence is neither drift nor covered.
- **Next evidence needed:** User/spec-owner decision on whether "empty" includes whitespace-only and None.

### Gap G-2
- **Hunk ref:** PLAN:4, PLAN:10
- **Evidence missing:** No greet module path, test file location or test framework named in spec or plan.
- **Why not classifiable:** Spec is silent; omission cannot be judged a deviation.
- **Next evidence needed:** Project convention or user decision on module/test layout.

## Risks
- RISK-1 (medium): token-only traceability shows 1.0 coverage while R-001/R-003 are semantically partial.
- RISK-2 (medium): [INFERRED] a differently formatted greeting would satisfy T-101 text but violate R-001.
- RISK-3 (medium): [INFERRED] tests lacking assertions would satisfy T-103 but not R-003.
- RISK-4 (low): no dependency/ordering fields or per-task acceptance criteria (PLAN:3, PLAN:6, PLAN:9 headings carry only IDs).
- RISK-5 (low): [INFERRED] S_dev_density 0.0 can read as "no deviation" despite two drift items.

## Inferred-claim audit
- `citations_inferred: 5`
- Inferred-fraction: 5 / 9 = 0.56 (WARN not triggered: citations_total <= 20)

## Recommendations

### Recommendation R-1: Pin the exact greeting in T-101
- **File:** PLAN (proposed.md)
- **Change:** Replace "the required greeting" at line 4 with acceptance `greet('Ada') == 'Hello, Ada!'` (exact).
- **Verifier:** Grep proposed.md T-101 section for literal `Hello, Ada!`; then re-run `/sc:sc-reflect --mode pre --spec spec.md --tasklist proposed.md --tier 1 --no-promote`.
- **Linked deviation(s):** D-1
- **Priority:** P1

### Recommendation R-2: Specify assertions and a run step in T-103
- **File:** PLAN (proposed.md)
- **Change:** At line 10, require asserting `'Hello, Ada!'` and `pytest.raises(ValueError)` for empty name, plus a final step "test suite runs and passes". (`pytest.raises` is illustrative — the test framework is unconfirmed, see G-2 [UNVERIFIED].)
- **Verifier:** Grep T-103 section for `ValueError`, `Hello, Ada!` and a run/pass statement.
- **Linked deviation(s):** D-2
- **Priority:** P1

### Recommendation R-3: Add acceptance lines, ordering and file paths
- **File:** PLAN (proposed.md)
- **Change:** Add per-task Acceptance lines, mark T-103 depends-on T-101/T-102, and name module/test file paths.
- **Verifier:** Read proposed.md; each task has Acceptance, T-103 lists dependencies, paths named.
- **Linked deviation(s):** none (G-2, RISK-4)
- **Priority:** P2

### Recommendation R-4: Decide the empty-name boundary policy (user decision)
- **File:** SPEC (spec.md)
- **Change:** Only with user approval, state in R-002 whether whitespace-only/None counts as empty.
- **Verifier:** Read R-002 section; boundary policy explicit.
- **Linked deviation(s):** none (G-1)
- **Priority:** P2

## Audit provenance
- Coverage: sc:sc-requirements-analyst (sonnet slot) → artifacts/coverage-matrix.yaml
- Card: sc:sc-root-cause-analyst (sonnet slot) → reflection-card.yaml
- Calibration: sc:confidence-calibrator (opus slot, disjoint from card author; calibrator_diversity full) → calibration/tier1-calibration.md, C = 0.93 (self-reported 0.85, delta +0.08)
- Tier: 1 (explicit `--tier 1`; shadow rubric rule 2 agrees) → artifacts/tier_decision.yaml. No Tier 2 / adversarial merge run.
- Evidence gate: sc:evidence-validator (haiku slot) → evidence-validation.md, 9/9 verified, 0 dropped
- Recommendation check: sc:confidence-check → recommendation-scrutiny.yaml (0.80: present with alternatives; R-3/R-4 need user input)
- Degraded: Serena/Auggie/Context7 MCP not exposed (native Read/Grep fallback; think_about_* checkpoints skipped); vendor diversity single (warn-only, T2 not reached); no external best-practice lookup performed.
- Promotion: suppressed (`--no-promote`; UC-1 has nothing to promote). No repository mutation.
