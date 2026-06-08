# QA Report — Phase-Gate (Phase 5: Tests, Docs, Version)

**Topic:** Auto-Resume as the Default for sprint run / rerun-tasks (v4.3.5)
**Date:** 2026-06-02
**Phase:** phase-gate (Phase 5, items 5.1–5.6; 5.7 pending)
**Fix cycle:** N/A (first pass)
**Stance:** Adversarial, zero-trust. fix_authorization: true.

---

## Overall Verdict: PASS

Phase 5 outputs are valid, non-tautological, and AC-complete. The 9 design §9
tests exist with exact names and assert real production-code behavior; the e2e
tests use the real `claude` shim and assert on real on-disk merged status; docs
and changelog accurately describe the actual `passed = accept_suspect or
validated_last` behavior; version is 4.3.5 in both files. Three in-place
strengthenings were applied (no assertions weakened) and the most important —
a durable test locking the gate's hard-STOP — was **mutation-proven** to have
teeth.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | 5.1 — all 9 design §9 tests exist with EXACT names | PASS | grep on test_resume.py: all 9 present verbatim |
| 2 | 5.1 — each test asserts design behavior (not just output text) | PASS | AC-1 interrupted==3/completed==[1,2]/crash; AC-2 Granularity.TASK+rerun_task_ids==["T03.02"]+roles; AC-3 Granularity.PHASE+boundary_tasks==[]; AC-7 call-counter==0; AC-9 bare==explicit run_rerun_tasks(3,["T03.02"]) |
| 3 | 5.2 — FR-2.5 / DD-2 / INV-001 invariant tests exist & assert | PASS | test_boundary_quarantine_nondestructive, test_haiku_coherence_advisory_only, test_inv001_tier0_exact_hash_match |
| 4 | 5.3 — e2e AC-1/2/3 over the REAL-subprocess harness | PASS | conftest installs fake_claude.py as executable `claude` on $PATH, asserts shutil.which → it (no Popen mock); tests assert real on-disk merged status + real run_log() |
| 5 | 5.3 — AC-3 re-runs the WHOLE phase (all 3 tasks) | PASS | hard-crash test removes result.json+transcripts → PHASE; asserts sorted(run_log)==["T01.01","T01.02","T01.03"] |
| 6 | 5.5 — CHANGELOG: behavior change + `--fresh` opt-out + `--yes`/env CI opt-in | PASS | CHANGELOG.md L9-14 |
| 7 | 5.5 — docs describe detect→print→prompt→proceed | PASS | docs/sprint-cli-deep-dive.md L1664-1681 matches commands.py run() |
| 8 | 5.5 — doc claims match code (passed=accept_suspect or validated_last; partial surfaced-not-blocking) | PASS | doc L1718-1720 byte-matches integrity.py:314 |
| 9 | 5.6 — version 4.3.5 in pyproject.toml AND __init__.py | PASS | pyproject:7, __init__:8, pytest banner "SuperClaude: 4.3.5" |
| 10 | ADV: AC-4/AC-5 fixtures record ORIGINAL baseline → Tier 0 misses, Tier 1 under test | PASS | recorded_body=_P3 in both; verified hash(orig)≠hash(orig+ws); live assess → AC-4 structural/0.9, AC-5 structural/0.3 |
| 11 | ADV: autouse invoke_sonnet stub does not mask the deterministic verdict | PASS | _verdict has no LLM token; advisory runs AFTER verdict (L81>L74); coherence test drives REAL SUSPECT → passed/validated_last unchanged |
| 12 | ADV: AC-7 call-counter truly proves planner NOT called | PASS | --start 1 AND --start 4 → calls==0; bare → calls==1 |
| 13 | ADV: AC mapping completeness | PASS | 9 ACs + FR-2.5 + DD-2 + INV-001 each → one correct test; no cross-wiring |
| 14 | ADV: full module run all-pass | PASS | 36 passed (35→36) |
| 15 | ADV: ruff clean on all three test files | PASS | All checks passed! |
| 16 | ADV: negative-direction (over-claim → hard STOP) durably tested | **FAIL → FIXED** | Module asserted only the True direction; added mutation-proven over-claim test |

## Summary
- Checks passed: 16 / 16 (after fix)
- Checks failed (pre-fix): 1 (item 16 — coverage gap)
- Critical issues: 0
- Issues fixed in-place: 3 strengthenings (1 coverage gap closed + 2 anti-tautology locks)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | test_resume.py — gate coverage | The durable Phase-5 suite asserted ONLY the `validated_last/passed == True` direction. The gate verdict `_verdict = accept_suspect or validated_last` could regress to an always-True no-op and EVERY test would still pass. The hard-STOP (FR-2.4) — the gate's reason to exist — was not test-locked durably (P3's "55+ assertions" were throwaway inline traces, not CI-durable per item 13). | Added `test_gate_hard_stops_on_last_completed_overclaim` driving a missing-deliverable over-claim → asserts validated_last False, passed False, blocking_reasons present, lc suspect, and accept_suspect override → passed True. **Mutation-proven**: with `_verdict` forced to always-True the test FAILS (`assert True is False`); reverts to green. |
| 2 | MINOR | test_resume.py:250 (AC-4) | `assert confidence >= 0.8` could not distinguish a vacuous Tier-0 hash match (1.0) from the intended Tier-1 cosmetic path (0.9). If the hash fn ever normalized whitespace, AC-4's real path would silently stop being exercised. | Added `assert drift.tier != "hash"` + `assert drift.cosmetic_only is True` to lock the Tier-1 path. |
| 3 | MINOR | test_resume.py:261 (AC-5) | `assert confidence < 0.8` could be satisfied by the corrupt/empty-file guard (also 0.3) rather than the intended removed-completed-task path. | Verified material body parses to non-empty {T03.02,T03.09}; added `assert "T03.01" in drift.explanation` + `cosmetic_only is False` to lock the removed-completed path. |

## Actions Taken
- Strengthened AC-4 test (`test_drift_trailing_whitespace_high_conf`): added `tier != "hash"` and `cosmetic_only is True` — proves Tier 1 ran, not a vacuous Tier-0 pass. Verified via direct hash comparison that Tier 0 genuinely misses on trailing whitespace.
- Strengthened AC-5 test (`test_drift_material_edit_low_conf`): added `"T03.01" in explanation` and `cosmetic_only is False` — proves the removed-completed-task path, not the corrupt-file guard. Verified the material body parses to a non-empty ID set.
- Added `test_gate_hard_stops_on_last_completed_overclaim` (reuses existing `_build_gate_fixture(lc_deliverable_exists=False)`) — closes the negative-direction coverage gap. Verified the live behavior (validated_last/passed False + blocking_reasons + accept_suspect override) before locking it, then mutation-tested it (always-True `_verdict` → FAIL) and reverted integrity.py byte-identical (no MUTANT residue; line 314 intact; git shows no modification — only the expected new-file `??`).
- Re-ran the full 3-module set after every change: 36 passed; ruff clean on all three files.

## Verification Independence Notes
- e2e harness is genuinely real-subprocess: `claude_shim` copies `fake_claude.py` to an executable `claude` on `$PATH` and asserts `shutil.which("claude")` resolves to it — the executor's real `subprocess.Popen` spawns it; only desktop-toast / post-merge verify-checkpoints / advisory `invoke_sonnet` are patched (all environmental noise, never the spawn chain or the deterministic gate).
- Docs/changelog verified against code, not against each other: the load-bearing claim `passed = accept_suspect or validated_last` in docs L1718 byte-matches `integrity.py:314`. No doc claim contradicts the code.

## Recommendations
- None blocking. Phase 5 (5.1–5.6) is complete and verified. Item 5.7 (mark Done) may proceed.
- The two PRE-EXISTING breakages noted in the task's Follow-Up (the `invoke_haiku` ImportError family and the `FakePopen.stdin` integration-lifecycle failure) are NOT this task's regressions (stash-proven in the task log) and are correctly out of scope for this phase gate. They do block the unconditional "full suite green" claim and should be triaged separately.

## Confidence

**Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 8 | Grep: 4 | Glob: 1 | Bash: 9

- No UNCHECKED items.
- No UNVERIFIABLE items.
- No web research performed (all claims are local-source-truth; no external URL/standard/third-party-API lookup required).
- Tool calls (Read+Grep+Glob+Bash ≈ 22) exceed the 16-item checklist minimum; each maps to a specific check (file reads of all 6 output surfaces + production modules, grep for test names/versions/doc claims, live behavior verification, mutation test).

## QA Complete

VERDICT: PASS
