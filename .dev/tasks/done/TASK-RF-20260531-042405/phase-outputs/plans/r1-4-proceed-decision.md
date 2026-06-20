# R1.4 → R1.5 Proceed Decision (PG9.2)

**Authored:** 2026-06-02. **Gate:** Phase 9 (R1.4) Quality Verification.
**PG9.1 rf-qa-qualitative verdict:** **PASS** (`phase-outputs/reviews/r1-4-rf-qa-qualitative.md`).

## Decision: PROCEED to Phase 10 (R1.5 — `verify-implementation` terminal step)

PG9.1 release-validation passed all 8 acceptance criteria (a)–(h) + 4 adversarial deep-checks,
with 2 MINOR findings fixed in-place (fix cycle 1; HALT-precedence not triggered):
- **F1:** `extraction_mode` schema enum was narrower than the markdown gate's `chunked*`
  acceptance → relaxed to `pattern:"^(standard|chunked.*)$"` in both extract schemas + regression
  test cross-checking the real gate function (restored dual-write interchangeability).
- **F2:** added a guard test proving multi-agent `reflect-{agent}` / `adversarial-merge` ids
  bypass the tool-write hook.
Re-verification after fixes: **full `tests/roadmap/` 1950 passed / 12 skipped / 0 failed**, ruff
clean, `make lint-architecture` 0 errors.

## R1.4 outcome recorded

- **11 genuine LLM tool-write migrations** implemented in DUAL-WRITE mode (flags default False;
  markdown is the production default): extract, extract_tdd, generate, diff, debate, score, merge,
  spec_fidelity, test_strategy, certify, validate_reflect.
- **wiring_verification — deterministic-EXEMPT:** already static analysis (no LLM/markdown path);
  no schema/template; not a missing artifact (Step 9.10).
- **remediate — parity-only:** prompt `tool_write` param + `--tool-write-remediate` flag + flag=False
  byte-identity; no schema/template/render (file-edit prompt, no roadmap-ID artifact, Contract #3 N/A).
- **Cutover DEFERRED:** `.dev/migrations/r1-4-cutover-counters.yaml` all `release_marker_count: 0`,
  `cutover_eligible: false`. Markdown remains production default until ≥3 release cycles per step
  (Vector A); markdown-path deletion is an R1.6 / release-cycle-hook action, NOT done in R1.4.
- **Contracts:** #3 (phantom-ID) LIVE at generate + merge (generation-time rejection, neither .md
  nor .json written); #8 (thresholds) score + spec_fidelity sourced from `CONVERGENCE_THRESHOLDS`.
- **PRESERVE:** convergence.py / semantic_layer.py / structural_checkers.py byte-unchanged vs
  90a8fa67; commands.py additive `--tool-write-*` flags only; R1.3 dispatch-reachability preserved.

## ⚠ CARRY-FORWARD CONSTRAINT into Phase 10 (H2 — sc:reflect, load-bearing)

**Phase 10 (R1.5 `verify-implementation`) MUST NOT ship before R1.6 Step 11.4** (deletion of the
`fidelity_checker.py:287-303` fail-open default). If `verify-implementation` lands in production
while the legacy fail-open default still exists, an error path falls through to `found=True` — the
exact fail-open behavior the new step is designed to eliminate.

**Acceptable orderings (task preamble §Phase 10 prerequisite):**
- (A) ship Step 11.4 before Phase 10's first step lands in production (preferred: R1.6.4 → R1.5.1); OR
- (B) ship Phase 10 + Phase 11 atomically in one merge (no fail-open window).
- NOT acceptable: Phase 10 in production while Phase 11 is in progress.

The executing agent MUST verify Step 11.4 is complete (or lands in the same merge) before opening
any PR that includes Phase 10's `verify-implementation` wiring.

## Provenance note

R1.4 was committed during this gate (HEAD `44f78a01` ← `b0bc0fe1` ← `c542b6bf`), resolving the
earlier untracked-files carry-forward. A concurrent session that produced those commits (and a
"Phases 9-13 adversarial pre-validation" note) was stopped per user direction; this session owns
the task. The QA F1/F2 fixes are in the working tree on top of `44f78a01` (uncommitted at authoring).
Phase 10+ checkbox state should be re-reconciled before execution (the concurrent session may have
touched Phases 10–13).
