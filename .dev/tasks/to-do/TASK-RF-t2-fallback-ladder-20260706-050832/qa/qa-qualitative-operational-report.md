# QA Report — Task File Qualitative Review (Operational Correctness)

**Topic:** Reflect Tier-2 fallback model ladder
**Date:** 2026-07-06
**Phase:** task-qualitative
**Lens:** operational-correctness
**Fix cycle:** N/A (first pass)
**Fix authorization:** true

---

## Overall Verdict: FAIL — 2 issues found, BOTH FIXED IN-PLACE (no unfixable issues remain)

Two IMPORTANT operational defects were found and remediated in the task file
directly (fix_authorization: true, scoped to the task document under review).
After the fixes, no blocking operational defect remains. A re-verification pass
over the two edited items is recommended but not required to proceed.

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | `uv run pytest tests/cli/reflect/...`, scoped `ruff check`/`format --check`, `make verify-sync`, POST wrapper — all preconditions satisfied by earlier items; UV-only honored; ruff scoped to changed files only (matches worktree-drift memory) |
| 2 | Project convention compliance | none | PASS | All edits target `src/superclaude/cli/**` (source of truth); reflect tests → `tests/cli/reflect/` (verified dir exists w/ conftest+fixtures); swarm tests → `tests/swarm/` NOT `tests/cli/swarm/` (Step 4.5/4.6 correct); `.claude/` never staged; verify-sync noted as required though CLI files don't trigger sync-dev |
| 3 | Intra-phase execution order | AX-2 | FAIL→FIXED | Step 3.4 (controller terminal_reason) contradicted Step 3.7 (counter-case assertion) — see Issue #1 |
| 4 | Function signature verification | none | PASS | `run_tier2_ensemble` HAS `env` param (ensemble.py:179); `build_reflect_contract` at ensemble.py:553 takes the described kw-only params, `t2_fallback` append is additive; `_stamp_worker_paths` IS in ensemble.py:691; `read_env` IS T2-bound via T2_* constants (openai_compat.py:159); `_resolve_run_transport_factory(kind,*,models,env,workers_requested)` matches Step 4.3; `dispatch_wave1` sig matches; `ModelPoolTooSmallError` at swarm/commands.py:589 |
| 5 | Module context analysis | AX-3 | FAIL→FIXED | Moved private helper `_vendor_from_model_id` has an out-of-change-set consumer + ruff-F401 severing risk — see Issue #2 |
| 6 | Downstream consumer analysis | AX-3 | FAIL→FIXED | `test_ensemble_unit.py` imports `_vendor_from_model_id`/`compute_model_class_diversity` from `ensemble` — Issue #2 |
| 7 | Test validity | none | PASS | Tests build real `WorkerResult`s / inject `dispatch`/`normalize`/`stamp` stubs / `httpx.MockTransport` / env dicts; no stub-of-stub; F1/F2/F4/F6 load-bearing assertions concrete |
| 8 | Test coverage of primary use case | none | PASS | §8 incident + counter-case replayed end-to-end through real controller+contract path (Step 3.7); full `-k "reflect or swarm"` at Step 6.2 |
| 9 | Error path coverage | none | PASS | `TransportEnvError`/`ModelPoolTooSmallError` → `fallback_config_missing`; wall-clock → `fallback_wall_clock_exhausted`; missing-T1-env raises; enum tokens validated w/ `ValueError` |
| 10 | Runtime failure path trace | AX-2 | FAIL→FIXED | Data flow normalize→controller→build_reflect_contract sound (seam 225→226 verified); terminal_reason break at counter-case — Issue #1 |
| 11 | Completion scope honesty | none | PASS | Phase-5 Open Question is a REAL needs_human_decision HALT: PENDING write + `status: ⚪ Blocked` + stop, no auto-default to T2-reuse; Steps 5.2/5.3 gate on confirmation |
| 12 | Ambient dependency completeness | AX-3 | FAIL→FIXED | Import/`__all__`/re-export touchpoint for `_vendor_from_model_id` — Issue #2 |
| 13 | Kwarg sequencing red flags | none | PASS | `t2_fallback` param added (Step 2.2) before its use (Step 3.6); `_T1_PROXY_BINDING` sentinel declared Step 3.5 → structure Step 4.4 → enabled Step 5.2; `stamp` required-no-default correctly injected at Step 3.6 call site |
| 14 | Function existence claims | none | PASS | All grep-verified: `degraded-tier1`@contract.py:272 precedes `single-reviewer-fallback`@288 (F6 ✓); `_LOAD_BEARING_BOOL_FIELDS`@48; fixtures `pass.yaml`+`degraded_tier1.yaml` exist; conftest `temp_tasklist`/`patch_git`/`FIXTURES_DIR`/`_load` exist; `test_openai_compat.py` w/ `read_env` regression body exists |
| 15 | Cross-reference accuracy | none | PASS | design §6 enum, §8 counter-case, §5 ledger, §7.2 config, §10 change-map all match cited item content; anchor line-drift noted in items as "±a few lines, match on symbol" |

---

## Summary
- Checks passed: 15 / 15 (after in-place fixes; 3 checks were FAIL→FIXED)
- Checks failed (unremediated): 0
- Critical issues: 0
- Important issues: 2 (both FIXED in-place)
- Minor issues: 0
- Issues fixed in-place: 2

---

## Issues Found

| # | Severity | Location | Issue | Fix Applied |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Step 3.4 vs Step 3.7 (`terminal_reason`) | **Internal contradiction (AX-2) guaranteeing a Phase-3 test failure.** Step 3.4's M6 rule assigns `fallback_attempts_failed` to "the ladder DID dispatch its slots but none yielded a contributing success" — i.e. the both-fallbacks-failed terminal state. But Step 3.7's counter-case asserts `t2_fallback.terminal_reason == fallback_pool_exhausted` for "both fallbacks fail," which matches the AUTHORITATIVE design §8 (design.md:650) and the enum comment "both slots attempted, still short" (design.md:450). With the default `ladder=("T1Model01","T1Model02")` + `max_attempts=2`, both slots are walked, so the counter-case terminal state satisfies BOTH of Step 3.4's descriptions — the wording made the two tokens indistinguishable at the terminal state and inverted the design's choice. If implemented per Step 3.4's literal M6 wording, `test_ensemble_fallback_stub.py` counter-case (Step 3.7 / Step 3.9) FAILS. | Edited Step 3.4 to add an explicit **precedence rule** aligning with design §8/§6 + Step 3.7: when all ladder slot NAMES are attempted and quorum is still unmet, `terminal_reason = fallback_pool_exhausted` (even if all attempts failed); `fallback_attempts_failed` is reserved for the narrower `max_attempts < len(ladder)` truncation case (unused slot name remains). Keeps the M6 producer branch reachable without colliding with the §8 counter-case. |
| 2 | IMPORTANT | Step 1.4 + `ensemble.py`/`test_ensemble_unit.py` | **Ambient-dependency / downstream-consumer gap (AX-3) with a ruff-F401 severing hazard.** Step 1.4 moves `_vendor_from_model_id` from `ensemble.py` to `_diversity.py`, keeping a re-import in `ensemble.py`. After the move, `compute_model_class_diversity`/`compute_vendor_diversity` stay USED at ensemble.py:615-616 (re-import safe), but `_vendor_from_model_id`'s only callers moved out (ensemble.py:665,672), so its re-import is UNUSED → ruff F401. The out-of-change-set test `tests/cli/reflect/test_ensemble_unit.py:17-24` imports `_vendor_from_model_id` AND `compute_model_class_diversity` FROM `superclaude.cli.reflect.ensemble`. Step 1.16's scoped `ruff check`/`--fix` would flag/remove the unused re-import, silently severing that test's import. Invisible in Phase 1 (Step 1.15 runs only the 4 new files), surfaces as a collection ImportError at Phase 6 Step 6.2 (`-k "reflect or swarm"`), then risks a ruff-vs-test deadlock. Neither Step 1.4 nor any later item accounts for it. | Edited Step 1.4 to add an **anti-orphaning / ruff-F401 guard**: MUST preserve the `ensemble._vendor_from_model_id` re-export via `__all__`/`# noqa: F401`, OR re-point `test_ensemble_unit.py`'s import to `._diversity` (and add that file to Step 1.15/1.16 scoped lint/test set). Explicitly forbids letting `ruff --fix` drop the re-import unguarded. |

---

## Actions Taken
- **Fixed Issue #1** in Step 3.4 by inserting a `terminal_reason` precedence rule
  binding `fallback_pool_exhausted` to the all-slots-attempted terminal state
  (per authoritative design.md:650 + enum design.md:450 + Step 3.7), reserving
  `fallback_attempts_failed` for the `max_attempts < len(ladder)` truncation case.
  Makes Step 3.4 ⇔ Step 3.7 ⇔ design §8 mutually consistent.
- **Fixed Issue #2** in Step 1.4 by adding an anti-orphaning / ruff-F401 guard that
  preserves the `ensemble._vendor_from_model_id` re-export (or re-points the
  external test import), preventing the Phase-6 collection ImportError + ruff/test
  deadlock. Verified via grep that `test_ensemble_unit.py:18` imports
  `_vendor_from_model_id` from `ensemble` and that it has no remaining in-`ensemble`
  caller after the planned move.

Both fixes are scoped to the task file itself (the artifact under review) — in
scope per the fix-authorization rules; no source code was modified.

---

## Self-Audit (reliance vs. independent verification, INV-019)

**(a) Inherited Structural Verdict PASS items relied on (structural re-check skipped):**
- Relied on rf-qa A.10 PASS for: item structure / frontmatter shape / section
  numbering / B2 5-field bodies / TB-Add-* structural checks / stamp
  circular-import CRITICAL fix / "7 new reflect" count / handoff-path
  consistency / anti-orphaning (structural) / A.10.25 research-alignment.

**(b) Independent semantic checks where structural PASS was INSUFFICIENT and my own tool work was required (≥1, INV-019):**
- **terminal_reason semantic contradiction (Issue #1):** structural QA confirms the
  items exist and reference §6/§8; it does NOT execute the semantics. I Read
  design.md:444-455 (enum) and :647-653 (counter-case) and cross-read Step 3.4 vs
  Step 3.7 to find they assert incompatible `terminal_reason` for the same runtime
  scenario — invisible to a structural pass.
- **ruff-F401 / out-of-change-set consumer (Issue #2):** structural anti-orphaning
  covers the task's own references; it did not catch that `_vendor_from_model_id`
  becomes unused-in-`ensemble` post-move and that `test_ensemble_unit.py:17-24`
  imports it via the ensemble namespace. I grepped both importer and remaining-usage
  set to prove the F401 severing hazard.
- **Signature/anchor liveness:** independently Read ensemble.py (env@179,
  build_reflect_contract@553, _stamp_worker_paths@691), openai_compat.py
  (read_env T2-bound@159), swarm/config.py (T2 constants + _collect_t2_models),
  swarm/commands.py (_resolve_run_transport_factory + ModelPoolTooSmallError@589),
  contract.py (F6 order 272<288), fixtures/conftest existence — value-level facts a
  structural verdict does not guarantee.

---

## Confidence Gate
- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 9 | Grep(via Bash): 6 | Glob: 0 | Bash: 6 | Edit: 2
  (Tool calls exceed the 15-item minimum — no padding; each targeted a specific
  claim: ensemble/openai_compat/config/models source, design §6/§8, contract order,
  fixtures, conftest, dispatch sig, importer grep.)
- No UNCHECKED items. No UNVERIFIABLE items.

### Tavily / web-research note
No external web lookup required — all verification local-file-bound (task file,
design, source, tests). Tavily-first precedence not triggered.

---

## Answers to Lens-Focus Questions
1. **Signatures match?** YES — `run_tier2_ensemble` has `env` (fwd to
   `resolve_t1_fallback_factory` OK); `build_reflect_contract` takes the described
   kw-only params (additive `t2_fallback` OK); `_stamp_worker_paths` in ensemble.py;
   `read_env` T2-bound via constants.
2. **Phase ordering works at runtime?** YES — `_diversity.py` extracted before
   `fallback.py` imports it; pure helpers before controller wiring; stub arm before
   real dispatch; seam 225→226 is post-`normalize_wave2`, pre-`succeeded_final_paths`.
3. **Tests exercise REAL artifacts?** YES — real `WorkerResult`, injected
   dispatch/normalize/stamp, `httpx.MockTransport`, env dicts; cited fixtures +
   conftest fixtures all exist.
4. **Commands' preconditions satisfied?** YES — UV-only, scoped ruff, verify-sync,
   `-k "reflect or swarm"` all reachable; no always-fail gate.
5. **needs_human_decision HALT real?** YES — PENDING write + `status: ⚪ Blocked` +
   stop; no silent T2-reuse auto-default; downstream items gate on confirmation.
6. **VALIDATION/TESTING/QA_GATE encoded as items?** YES — PER_PHASE QA gates, UNIT
   (Phase 1) + INTEGRATION (Phase 3/5) tests, final 7-agent aggregate gate,
   full-suite + scoped-lint + verify-sync + POST reflect wrapper.

---

## VERDICT: FAIL — 2 IMPORTANT issues found, BOTH FIXED IN-PLACE

No unfixable issues remain. The two remediated items (Step 3.4 terminal_reason
precedence; Step 1.4 ruff-F401 anti-orphaning guard) now make the plan
operationally executable without the identified Phase-3 test failure and Phase-6
import/lint deadlock. Recommend a light re-verification of the two edited items
before execution.

## QA Complete
