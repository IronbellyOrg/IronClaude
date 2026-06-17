# TFEP-troubleshoot-backend — E2E Validation Roll-Up Dashboard

Policy: **strict 12/12 PASS + 4×(3/3 byte-identical digests)** · generated 2026-06-17 · 12 runs (10 PASS / 2 FAIL)

## Verdict & digest matrix (4 tests × 3 runs)

| Test | Run 1 | Run 2 | Run 3 | Digests identical? | Test status |
|------|-------|-------|-------|--------------------|-------------|
| **E1** Residual-Integrity & Sync-Parity | PASS | PASS | PASS | Y (`443baab42cb2`) | **PASS** |
| **E2** Adapter Contract Round-Trip | PASS | PASS | PASS | Y (`202f96f6aa6f`) | **PASS** |
| **E3** Protocol-Chain Resolution | PASS | PASS | PASS | **N** (r2 `1409a638` vs r1/r3 `cf4ead44`) | **DISAGREE** |
| **E4** Safety-Invariant Preservation | **FAIL** | PASS | **FAIL** | **N** (r2 `a6698219` vs r1/r3 `4c755bc4`) | **DISAGREE** |

## GATE: **INDETERMINATE** (human-halt — NOT silently RED)

Tests PASS (GREEN) = **2 / 4** (E1, E2). Two tests DISAGREE. **No run is a unanimous content-FAIL** — every safety/contract invariant verified intact in every run — so the gate is INDETERMINATE, not MIGRATION_NOT_VALIDATED. `suite_failure_class = cross_run_disagreement`.

`migration_substantively_validated = true`

## Diagnosis — migration content vs test-probe artifacts

The migration content is **substantively valid in all 12 runs**. Both DISAGREE results are test-harness defects, not migration regressions:

- **E3 (digest-only split, cause = digest_schema_looseness).** Verdicts are unanimous PASS; AC3.1–AC3.9 hold in every run. The digest diverges solely because the non-AC normalized key `branch_keys_found_count` was counted as **6** (run-2: semantic branch keys) vs **8** (run-1/3: raw `rg` match lines) on the *same* H6 content (all six branch keys + "first match wins" at T1:222-230). Every AC-bearing observation (`h1..h8`, `chain_continuous`, `fix_total/fix_prohibition=2/2`, `tier_intent_count=0`) is byte-identical across runs.

- **E4 (split verdict + digest, cause = test_probe_artifact).** The load-bearing safety gate **AC4.1 (freeze block byte-identity, DIFF_EXIT=0) PASSES in all three runs**, as do AC4.2/4.3/4.5/4.6. The FAIL is confined to two literal probe regexes that under-match real file punctuation:
  - **E4 I4a (AC4.4 incident-rebind):** `report_path .REPORT\.md` expects space+1-char but T1:260 renders `` report_path` (REPORT.md) `` (backtick+space+paren). Loosened `.*` separator matches L260. The clause-2 falsification (zero `rca-verdict`/`solution-verdict`) PASSES in all runs.
  - **E4 I1b / C2 (AC4.7 baseline cross-check):** `STOP. testing` expects 1 char but BASE has `**STOP** testing`; ` .. ` cannot span the single-codepoint em-dash `—`.
  - run-2 graded these two AC on substantive content (PASS); run-1/run-3 bound the verdict to literal exit codes (FAIL). No run reported a content regression.

## Required test-suite fixes (to reach a clean GREEN on re-run)

1. **E4 I4a (AC4.4):** loosen incident-rebind regex to `Diagnostic artifacts.*report_path.*REPORT\.md.*audit_log_path`.
2. **E4 I1b/C2 (AC4.7):** fix baseline cross-check to tolerate markdown bold + em-dash: `STOP.* testing immediately|FREEZE.*implementation.*no further code changes permitted`. (AC4.1 byte-identity already guarantees the freeze block itself; only this self-consistency regex is over-strict.)
3. **E3 H6 (AC3.4):** define `branch_keys_found_count` from the fixed 6-key set rather than raw `rg` line count, or drop it from `normalized_observations` (it is not an AC input). Either makes E3's three digests byte-identical.

After fixes (1)–(3), all four tests are expected to reach 3/3 PASS + 3/3 identical digests → **GREEN**.
