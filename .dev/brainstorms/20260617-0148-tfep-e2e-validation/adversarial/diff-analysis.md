# Diff Analysis — 3 Variants (opus:qa, sonnet:analyzer, haiku:devops)

**Date:** 2026-06-17 · **Depth:** standard · **Convergence target:** 0.75

## Structural convergence (HIGH)

All three independently produced the SAME 4-test decomposition mapped 1:1 to the seed brief's
4 desired-outcome dimensions, and the SAME strict 12/12 verdict policy:

| Dimension | A (opus:qa) | B (sonnet:analyzer) | C (haiku:devops) | Agree? |
|-----------|-------------|---------------------|------------------|--------|
| 1 Residual + sync parity | E1-residual-sync | E2E-B1 | TEST-01 | ✅ |
| 2 Adapter contract round-trip | E2-contract-roundtrip | E2E-B2 | TEST-02 | ✅ |
| 3 E2E protocol chain | E3-chain-trace | E2E-B3 | TEST-03 | ✅ |
| 4 Safety invariants | E4-safety-invariants | E2E-B4 | TEST-04 | ✅ |
| Verdict policy | strict 12/12 (split→INDETERMINATE) | strict 12/12 (split→DISAGREE→FAIL) | strict 12/12 (split→RED) | ✅ |
| Read-only / non-mutating | ✅ | ✅ | ✅ | ✅ |
| Embedded delegable prompt per test | ✅ | ✅ | ✅ | ✅ |
| Per-test/per-run evidence dir + aggregator | ✅ (AGGREGATE.md) | ✅ (aggregate-verdict.yaml) | ✅ (roll-up.yaml + dashboard.md) | ✅ |
| Falsification / negative check per test | ✅ (explicit, named) | ✅ (per-test) | ✅ (per-test "NEGATIVE CHECK") | ✅ |

Estimated convergence: **0.88** (structure ~95% identical; remaining deltas are complementary, not contradictory).

## Complementary divergences (each adds value, none conflicts)

| Aspect | A | B | C | Resolution |
|--------|---|---|---|------------|
| Verdict anchoring | falsification tripwire per test; every criterion → shell exit code | DETERMINISTIC vs JUDGMENT class label + judgment-fraction; only 2 judgment criteria across suite | deterministic-probes-first, LLM trace anchored to probe output | **Merge all 3**: keep A's falsification, adopt B's class label + judgment-minimization, keep C's "deterministic first" ordering |
| Cross-run agreement | verdict-level (run1==run2==run3) | **observation-level**: normalized_observation_digest must match across 3 runs (stronger) | verdict-level (cross_run_agreement bool) | **Adopt B's digest** as the stronger reproducibility gate + DISAGREE status |
| Determinism hygiene | implicit | **explicit**: `LC_ALL=C`, `--sort path`, sha256 of stdout/stderr, volatile-field exclusion | timeout + fail-fast + token budget | **Merge**: B's locale/sort/sha256 + C's timeout/fail-fast/budget |
| Evidence files per run | single `run-N.md` | `verdict.yaml` + `evidence.md` | `verdict.yaml` + `findings.md` | **Adopt the 2-file split** (machine + human); name them `verdict.yaml` + `findings.md` |
| `--fix` falsification | **FIX_TOTAL == FIX_PROHIBITION** (the subtle, correct check) | exact-line dispatch has no `--fix` (B4-AC4) | "--fix absent from dispatch strings" | **Adopt A's count-equality** (most robust) + B's exact-line check as a second probe |
| Orchestration | independence stated, no spawn plan | run layout + aggregator prompt | **explicit 4-batch spawn plan + aggregator subagent + dashboard.md** | **Adopt C's orchestration** wholesale |
| Suite failure taxonomy | INDETERMINATE vs NOT_VALIDATED | **`suite_failure_class` enum** (missing_artifact/schema_invalid/run_failed/cross_run_disagreement) | GREEN/RED | **Adopt B's failure-class enum** + C's GREEN/RED + dashboard |
| Extra coverage in test 4 | freeze byte-diff, no-backend-token-in-freeze | **+ incident-rebound to report_path/audit.log, report-template asymmetric rendering rules** | + conditional `## TFEP Consumer` preamble | **Union all** into the merged E4 |

## No irreconcilable conflicts

There is no point where adopting one variant's choice forces rejecting another's; the deltas layer
cleanly. The only "tension" is verbosity vs. concision (A is the most exhaustive, C the most operational)
— resolved by taking A's rigor as the spec body and C's orchestration as the execution wrapper.
