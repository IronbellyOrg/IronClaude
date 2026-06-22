# FR-RH2 Definition-of-Done Traceability Matrix

Date: 2026-06-20
Scope: maps every FR-RH2.N and NFR-RH2.N to its implementing Step, verifying
test row id(s), and the captured evidence file. No row is fabricated — every
test id below exists in the named test file.

Test files:
- `tests/cli/reflect/test_ensemble_unit.py` (U1-U9)
- `tests/cli/reflect/test_ensemble_stub_integration.py` (I1-I9)
- `tests/cli/reflect/test_no_nesting_guard.py` (guard)
- existing floor: `test_verdict_mapping.py` (B1), `test_runner_e2e.py` (B2), `test_writeback.py` (B3)

## Functional Requirements

| Req | Implementing Step | Verifying test(s) | Evidence file |
|-----|-------------------|-------------------|---------------|
| FR-RH2.1 (Tier-2 forms via swarm dispatch, not in-process Task fan-out) | 3.1, 4.1 | I1 (real dispatch→reduce→derive), I11 (production `_audit_once`→ensemble route), U3 (per-slot distinct binding), guard `test_layer_b_*` / `test_ensemble_launches_only_via_claudeprocess_no_raw_subprocess` | `phase6-i1-output.txt`, `phase6-integration-full-output.txt`, `phase3-u3u4u5u6u8-output.txt`, `phase7-u7u9-guard-output.txt`, `phase4-reflect-floor-output.txt` |
| FR-RH2.2 (reflect-review lens registered + passes validator + actually drives per-reviewer worker prompt, suspect+/sc:adversarial, default_workers∈[2,4], no hard-coded model) | 2.1, 2.2, 2.3, 3.1 | U1 (registered + validator), U2 (workers + no model literal), I10 (lens brief drives the worker prompt, not `/sc:reflect`) | `phase2-u1u2-output.txt`, `phase3-u3u4u5u6u8-output.txt`, `phase6-integration-full-output.txt` |
| FR-RH2.3 (adversarial Mode-A consumes final_path; no scoring added to merge.py; convergence score recorded) | 3.2 | U8 (merge stays mechanical/scoring-free), I1/I7 (convergence_score recorded on contract), merge boundary `test_merge_loc_ceiling.py`+`test_merge_mechanical_only.py` | `phase3-u3u4u5u6u8-output.txt`, `phase6-i1-output.txt`, `phase6-i7-output.txt`, `phase8-final-floor-output.txt` |
| FR-RH2.4 (t2_model_class_diversity computed over distinct succeeded model_ids, not N slots) | 3.1, 3.3 | U5 (diversity from succeeded model_ids), I3 (2 distinct→full), I4 (2 duplicate→not full) | `phase3-u3u4u5u6u8-output.txt`, `phase6-i3-output.txt`, `phase6-i4-output.txt` |
| FR-RH2.5 (non-mocked --transport stub positive witness, zero network, no canned ClaudeProcess fixture) | 6.1 | I1 | `phase6-i1-output.txt` |
| FR-RH2.6 (1-reviewer negative witness; same assertions FAIL) | 6.2 | I2 | `phase6-i2-output.txt` |
| FR-RH2.7 (derive_verdict + Verdict exit-code map unchanged; return-contract/reflect_post/sidecar shape preserved) | 3.3, 6.7 | U6 (verdict map + ordering byte-identical), I7 (contract shape, MAJOR-1), B1/B2/B3 floor | `phase3-u3u4u5u6u8-output.txt`, `phase6-i7-output.txt`, `phase8-final-floor-output.txt` |
| FR-RH2.8 (no-nesting guard passes incl. new driver; NFR-7 amendment recorded in spec §9 + guard docstring) | 7.1, 7.2, 7.3 | guard `test_layer_b_*`/`test_ensemble_launches_*`, U7 (guard scans ensemble.py), spec §9 CONFIRM | `phase7-u7u9-guard-output.txt`; spec §9 edit |
| FR-RH2.9 ((M,N) divergence: M==0 blocked/2, M==1 degraded/11, M≥2 distinct pass/0, M≥2 dup degraded/11) | 3.1, 6.3-6.6 | I3 (M==2 distinct→pass), I4 (M==2 dup→degraded), I5 (M==1→degraded), I6 (M==0→blocked, slug contract-missing) | `phase6-i3..i6-output.txt` |

## Non-Functional Requirements

| Req | Implementing Step | Verifying test(s) | Evidence file |
|-----|-------------------|-------------------|---------------|
| NFR-RH2.1 (no Task(/subagent_type in runner.py/ensemble.py) | 3.1, 4.1, 7.1 | guard `test_layer_b_wrapper_module_has_no_agent_imports` (loops runner.py+ensemble.py), U7 | `phase7-u7u9-guard-output.txt` |
| NFR-RH2.2 (thinness: no sprint/roadmap import, no async/await, no raw subprocess in reflect pkg) | 3.1, 4.1 | guard `test_no_sprint_or_roadmap_import_*`, `test_no_async_await_*`, `test_apply_remediation_*`, `test_ensemble_launches_only_via_claudeprocess_no_raw_subprocess` | `phase7-u7u9-guard-output.txt` |
| NFR-RH2.3 (ensemble proof non-vacuous: positive + falsifying witnesses) | 6.1, 6.2, 6.4, 6.5, 6.6 | I1 (holds) vs I2/I4/I5/I6 (`_i1_positive_holds` False) | `phase6-integration-full-output.txt` |
| NFR-RH2.4 (credit-free CI: stub run, no network I/O) | 6.1 | I1 (StubTransport; I1 patches ClaudeProcess to raise → no inference child) | `phase6-i1-output.txt` |
| NFR-RH2.5 (model-class diversity over survivors) | 3.1 | U5, I3, I4 | `phase3-u3u4u5u6u8-output.txt`, `phase6-i3-output.txt`, `phase6-i4-output.txt` |
| NFR-RH2.6 (existing reflect tests pass unchanged) | 4.1, 4.2, 8.1 | B1/B2/B3 + `test_fix_loop.py` + `test_marker_suppression.py` UNCHANGED (`git diff` empty — confirmed by the backward-compat lens) and whole `tests/cli/reflect` green. NOTE: `test_no_nesting_guard.py` was intentionally EXTENDED per Step 7.1/FR-RH2.8 — it is the guard being extended, NOT a backward-compat floor test. | `phase4-reflect-floor-output.txt`, `phase8-final-floor-output.txt` |
| NFR-RH2.7 (headless run pollable via done.json) | 3.1, 6.9 | I9 (DM-017 done.json shape) | `phase6-i9-output.txt` |
| NFR-RH2.8 (no forbidden host/port/path literal in executable code) | 3.1 | U9 (AST scan: no :4000/v1, :8317, /cli) | `phase7-u7u9-guard-output.txt` |

## Open-Item / OI rows

| Item | Resolution | Evidence |
|------|-----------|----------|
| Q1 / OI-1 (swarm→reflect contract correspondence table) | Validated Phase 0.1; ensemble.py mapping matches 6 DERIVED + 2 MAPPED + 12 SYNTHESIZED | `phase-outputs/discovery/oi1-mapping-table-validated.md` |
| Q6 (M==0 reason-slug) | Option B working default — `contract-missing` (NOT absent `ensemble-empty`); derive_verdict unchanged | `phase-outputs/decisions/q6-mzero-slug-decision.md`; I6 |
| Adversarial-seam (OI-4) | Option (b) — second top-level ClaudeProcess /sc:adversarial Mode A, launch site ensemble.py, fallback null-convergence | `phase-outputs/decisions/adversarial-seam-decision.md`; Step 3.2 |
| OI-2/Q2 (NFR-7 confirm/amend) | CONFIRM (no scope amendment); guard coverage extended to ensemble.py | spec §9 edit; Step 7.2 |
| OI-3 (--transport stub CI selection) | Explicit opt-in; CI passes `--transport stub` deliberately (not env-auto) | Step 5.3; I1-I9 pass `transport="stub"` |
| Q7 (`_resolve_run_transport_factory` is private) | Imported cross-package; flagged. Follow-up: pin a swarm contract test on signature stability or promote to public post-FR-RH2 | Follow-Up below |

## Spec §8.3 manual/live validation (Release-Criteria check)

| Scenario | Status |
|----------|--------|
| Live proxy Tier-2 ensemble (real `T2Model0N` openai_compat fan-out, real `/sc:adversarial` child) | **Manual Follow-Up / Out-of-scope for this automated task.** The automated proof is credit-free (stub transport + injected adversarial score). A live-proxy smoke run with `--transport openai_compat` against `~/.aienv` is required before production rollout to exercise the real HTTP path + real adversarial child. NFR-RH2.7 rollout coverage is NOT silently implied. |
| Original `claude -p` regression check (confirm the broken single-child fan-out no longer runs at Tier 2) | **Manual Follow-Up.** Covered structurally by the guard + I1 (no ClaudeProcess in the ensemble formation path) but a live before/after `merge_method`/`tier_reached` comparison on a real run is a rollout step. |

## Gaps & Follow-Ups

- **[Medium] Repo-wide ruff/format pre-existing drift** (125 ruff errors, 102 format files) outside this task's touched surface — needs a separate formatting-sweep PR before the repo-wide CI format gate is green. None are this task's files.
- **[Low] Live-proxy + claude -p regression smoke** (spec §8.3) — manual rollout validation, out-of-scope for this automated task.
- **[Low] Q7 private-symbol coupling** — `ensemble.py` imports module-private `_resolve_run_transport_factory`; pin a swarm signature-stability contract test or promote to public API post-FR-RH2.

All FR-RH2.1..FR-RH2.9 and NFR-RH2.1..NFR-RH2.8 have at least one verifying test with a real evidence file. No automated-coverage gaps remain; the only non-automated items are the spec §8.3 live/manual rollout scenarios, explicitly marked as follow-ups.
