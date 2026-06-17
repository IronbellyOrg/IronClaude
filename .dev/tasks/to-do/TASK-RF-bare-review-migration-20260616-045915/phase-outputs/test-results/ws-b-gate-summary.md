# WS-B STRICT Gate Summary (Step 4.5)

**Status: Complete**
**Verdict: PASS**
**Date:** 2026-06-16

## Commands (run in the `mms-m8m9` worktree)
- `uv run pytest tests/swarm/test_bare_review_parity.py -v`
- `uv run pytest tests/swarm/ -q`
- `uv run ruff check tests/swarm/test_bare_review_parity.py`

Raw output: `ws-b-gate.txt`.

## Results

### Rebuilt parity gate — 16 passed, 0 skipped, 0 failed
All 5 invariants × 3 scenarios (15) + the injection-guard suffix test (1):
- `test_cli_bodies_byte_match_frozen_golden[all-success|partial-with-timeout|salvage-promoted]` — **byte-equality CLI-vs-frozen-golden across all 3 scenarios** (sorted normalized `.final.md` multiset).
- `test_cli_contract_aggregate_status[*]` — IMM-5 status from the live CLI contract (success/partial/success).
- `test_cli_contract_per_slot_status_and_counts[*]` — per-slot status set + M/N.
- `test_cli_contract_suspect_and_adversarial_handoff[*]` — `caller_metadata.suspect` + `/sc:adversarial --suspect-source` from the CLI contract.
- `test_cli_contract_output_files_length[*]` — `len(output_files)==3`.
- `test_bare_review_lens_prompt_ends_with_canonical_injection_guard` — injection-guard suffix (NOT full prompt byte-parity, per G-2).

**The gate RAN and PASSED — none skipped.** It does NOT import `t2_normalize.py`/`LEGACY_SCRIPT`/`importlib` and has no `skipif` module guard, so it will keep asserting after WS-C deletes the legacy script (deletion-survivability verified independently at PG4 + WS-C post-deletion gate).

### Full swarm suite — 2217 passed, 27 skipped, 0 failed
Baseline comparison (no new regressions):
| run | passed | skipped | failed |
|-----|--------|---------|--------|
| baseline (Step 1.3, pre-migration) | 2212 | 26 | 0 |
| post-WS-0 (PG2.4) | 2218 | — | 0 |
| **WS-B (now)** | **2217** | **27** | **0** |

Reconciliation (every baseline-passing test still passes; deltas are all intentional):
- WS-0 added e2e CLI tests (`test_quickstart_emits_normalized_artifacts`, `--label`/`--reviewers`/`--target-line-cap`/`--timeout-sec` flag tests, etc.) → +passed over baseline.
- WS-B parity rebuild 17 → 16 tests (`-1` vs post-WS-0 count) — intentional (library-vs-library 7-test file → CLI-vs-golden 16-test file; the `-1` net is the count change, not a regression).
- WS-B regen helper `test_bare_review_golden_regen.py` → **+1 skipped** (env-gated `SWARM_REGEN_GOLDEN`, correctly skips in CI).
- **0 failed at every stage.**

### Ruff (path-scoped) — clean
`uv run ruff check tests/swarm/test_bare_review_parity.py` → All checks passed. `ruff format --check` also clean (both the parity test and the regen helper). No NEW issues on touched files. (Gate uses path-scoped ruff, NOT `make lint`, per Key Constraints.)

## Overall: WS-B PASS
Byte-equality CLI-vs-golden demonstrated across all 3 scenarios with NO reliance on the legacy script's runtime presence; full suite green with no new regressions; touched files ruff-clean.

**Carried forward (HIGH follow-up, see Follow-Up Items):** the FR-028 §7.4 salvage-promotion divergence (live CLI does not promote upstream `parse_error→success`; shared-`recipe_args` root cause). The gate is consistent with the frozen golden; the divergence is for PG4 / POST-reflect to adjudicate.
