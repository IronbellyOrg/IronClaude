# QA Report — Step 6.G3 Internal-Consistency / Anchor-Fidelity Lens

**Topic:** reflect Tier-2 fallback model ladder — final structural consistency
**Date:** 2026-07-07
**Phase:** report-validation (structural-consistency lens, report-only)
**Fix cycle:** N/A (fix_authorization: false)
**Change set:** `src/superclaude/cli/reflect/{fallback,ensemble,config,models,_diversity,commands}.py` + `src/superclaude/cli/swarm/{config,commands,transports/openai_compat}.py`

---

## Overall Verdict: FAIL

All load-bearing anchor invariants the spawn prompt enumerated **PASS**. The FAIL
is driven by **one IMPORTANT internal-consistency defect** (a false module-integration
claim in `_resolve_run_transport_factory` + an unexercised F3 parameterization that
duplicates the T1 pool-read mechanism) plus **one MINOR anchor-enumeration gap**.
No runtime-correctness defect was found; every changed module imports and the wiring
is functionally sound. The failure is a documentation/consistency reconciliation.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Controller seam is post-`normalize_wave2`, pre-`succeeded_final_paths` | PASS | ensemble.py: normalize L343-351 → fallback block L357-375 → `succeeded_final_paths` L376-380. Seam exact (research/01 §1 = "between L225/L226" pre-edit). |
| 2 | F4 run-deadline captured once, before primary dispatch | PASS | ensemble.py L322-324 `deadline = time.monotonic()+timeout if timeout else None`; precedes preflight L326 + `dispatch_wave1` L336. Passed as `deadline_monotonic=deadline` L371. |
| 3 | Additive `t2_fallback=` is the LAST defaulted kwarg | PASS | `build_reflect_contract` signature L704-721 ends `swarm_status`, `adversarial_status`, `t2_fallback: dict\|None=None`. Call site L490 last kwarg. Conditionally added to dict L791-792 (never overwrites). |
| 4 | Slot-NAME factory binding (`ladder[i]→pool[i]`, not positional slot_index) | PASS | `make_fallback_slot_factory` fallback.py L251-272 binds `slot_to_model[ladder[i]]=pool[i]`; keyed by NAME. `resolve_t1_fallback_factory` openai arm L280-282 feeds it. F1 root cause (research/02 §4) avoided. |
| 5 | Config/flag threading (3 fields → resolve_config → `--no-tier2-fallback` → tmux inner) | PASS | models.py L115-117 (3 defaulted fields, after last prior default `reachability` L109). config.py param L261, stub-OFF derivation L334, construction L389. commands.py option L320-329, run param L348, forward L381, tmux inner reinvocation L501-503. |
| 6 | No dangling references | PASS | `t1-proxy-binding-decision.md` exists (2869B). All 9 changed modules import cleanly (uv run import probe). Only `ensemble.py` imports `fallback` (grep). |
| 7 | `resolve_t1_fallback_factory` signature == call site | PASS | def `(transport, *, ladder, env=None)` L201-206; call `(config.transport, ladder=..., env=env)` L359-363. Exact. |
| 8 | `_T1_PROXY_BINDING` non-None dict of NAME strings, consistent w/ Phase 5 CONFIRMED | PASS | ensemble.py L193-198 non-None dict `{model_prefix,proxy_url_env,proxy_key_env,max_slots}`; consumed at L260-264. decision file Verdict: CONFIRMED (2026-07-07). Comment L186-192 matches. (max_slots is an int by design, read as `binding["max_slots"]`.) |
| 9 | `run_fallback_ladder`/`fallback.py` never imports `reflect.ensemble` | PASS | fallback.py imports L15-37 = swarm.* + `._diversity` + TYPE_CHECKING `reflect.models`. No `reflect.ensemble`. `stamp` is a required-no-default param (L406) injected by caller — module-boundary invariant honored. |
| 10 | `read_env_for_pool` call shape matches def | PASS | openai_compat def `(*, model_prefix, max_slots, proxy_url_env, proxy_key_env, env=None)` L160-166; ensemble lazy call L259-265 matches. T1 constants `T1_MODEL_ENV_PREFIX="T1Model0"`/`T1_MODEL_MAX_SLOTS=9` (swarm/config L72-73), imported ensemble L42. |
| 11 | `_resolve_run_transport_factory` F3 parameterization integration claim | **FAIL** | swarm/commands.py docstring L666 + comment L698 assert the reflect fallback resolver reads its pool "through the SAME builder" / "passes the T1 names to read its own pool" — but `ensemble.resolve_t1_fallback_factory` BYPASSES it (calls `read_env_for_pool`+`make_fallback_slot_factory` directly). Claim false; parameterization unexercised by T1. |
| 12 | fallback.py import allowlist vs Key Objective 1 enumeration | PASS (MINOR deviation) | Task L78 enumerates swarm.dispatch/normalize/models/transports/commands + reflect._diversity/models. fallback.py ALSO imports `swarm.preflight` (L26) + `swarm.transports.openai_compat` (L28), not enumerated. Verified `swarm.preflight` does NOT import reflect (no cycle). Load-bearing invariant (never import ensemble) holds. |
| 13 | "Additive-only, verdict-gate-preserving" (contract.py unchanged) | PASS | build_reflect_contract adds only the conditional `t2_fallback` key; no `_LOAD_BEARING_BOOL_FIELDS` member, no WorkerStatus/WorkerResult change (research/01 §4, research/02 §5). When `tier2_fallback_enabled` False the whole block is skipped → `t2_fallback=None` → byte-equivalent (ensemble L356). |

## Summary
- Checks passed: 12 / 13
- Checks failed: 1
- Critical issues: 0
- Important issues: 1
- Minor issues: 1
- Issues fixed in-place: 0 (report-only; fix_authorization: false)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `swarm/commands.py` `_resolve_run_transport_factory` docstring L666 + comment L698; vs `ensemble.py` `resolve_t1_fallback_factory` L251-286 | The builder's docstring/comment claim the reflect T1 fallback resolver reads its pool "through the SAME builder without forking". It does NOT: `resolve_t1_fallback_factory`'s openai_compat arm calls `read_env_for_pool` + `make_fallback_slot_factory` directly (necessarily — the builder returns a positional `(slot_index)->Transport`, unusable for slot-NAME binding). The F3 parameterization (`model_prefix`/`max_slots`/`proxy_url_env`/`proxy_key_env`) is therefore UNEXERCISED by the T1 path, and two parallel T1-pool-read mechanisms now exist. Also deviates from task Phase-4 item (file L362) which prescribed routing the T1 arm through `_resolve_run_transport_factory`. | Either (a) correct the L666/L698 docstring+comment to describe the direct `read_env_for_pool` design and drop the unused T1-purpose parameterization claim (keep params only if a real caller needs them), OR (b) reconcile the task Phase-4 item text so the "route through the builder" prescription no longer contradicts the shipped direct-read design. No code-behavior change needed. |
| 2 | MINOR | Task file Key Objective 1 (L78) vs `fallback.py` imports L26, L28 | The stated module-boundary allowlist omits `swarm.preflight` (imported for `PreflightResult`) and does not explicitly name the `swarm.transports.openai_compat` submodule (`TransportEnvError`). Both are leaf swarm modules (verified no back-import of reflect → no cycle), so the load-bearing invariant holds, but the enumeration is inaccurate. | Add `swarm.preflight` and `swarm.transports.openai_compat` to the Key Objective 1 allowlist enumeration for anchor fidelity. |

## Notes (verified NON-issues — checked and cleared)
- **"Augmented set" vs "smallest contributing set":** Task Overview (L70) / Objective 1 say fallback successes are "appended … recompute over the augmented set." The controller instead sets `normalized_workers = ladder_outcome.contributing_workers` where `select_contributing_set` returns the *smallest* Tier-2-satisfying set (fallback.py L217-248), which can reduce `reviewer_count` from 3→2 even when all primaries succeed on the default openai_compat path. This is NOT a defect: design.md is authoritative and explicitly specifies "smallest set satisfying count + model-class + vendor diversity" (§4 L270) and "reviewer_count == contributing not attempt count" (§4 L388-392, test L683). Implementation is faithful to the authoritative spec; the "augmented" intro language is loose in BOTH the task and design intros.
- **`_T1_PROXY_BINDING is None` gated arm (ensemble L230-235) is dead** given the CONFIRMED non-None binding — harmless defensive fallback, not an inconsistency.
- **Frontmatter `reflect_pre.note` (L28) still describes needs_human_decision as an open HALT** while Phase 5 CONFIRMED it — expected: `reflect_pre` is a frozen PRE-execution snapshot; the runtime comment (ensemble L186-192) correctly reads "CONFIRMED and enabled in Phase 5."
- **Per-fallback stamp→normalize order** (fallback.py `_dispatch_one_fallback` L372-396: dispatch→stamp→normalize) mirrors the primary seam (ensemble L336-351), and each attempt stamps into a distinct `fallback-<slot>` subdir → no `final_path` collision despite all 1-worker dispatches carrying `index==0`. F2 honored.
- **Terminal-reason / certification-basis closed vocabularies** (fallback.py L49-63) are exhaustive over every value `run_fallback_ladder` can emit; `build_fallback_metadata` validates membership (L111-116). Consistent.

## Confidence
Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Every check cites a specific file:line or tool result; the two defects were themselves verified by Read + grep (docstring L666/L698, import L26/L28, cycle-absence probe on swarm/preflight).

## Tool engagement
Read: 11 | Grep: 4 | Glob: 0 | Bash: 5 (incl. uv import probe of all 9 modules, decision-file listing, design.md semantics grep, cycle check)
No web research performed (all claims are source-truth-local; nothing external to verify).

## Recommendations
1. Resolve Issue #1 before marking the task Done: reconcile the `_resolve_run_transport_factory` docstring/comment with the shipped direct-`read_env_for_pool` T1 design (or wire the T1 arm through the builder per task L362). This is the only blocking finding.
2. Patch the Key Objective 1 import allowlist enumeration (Issue #2).
3. No changes required to the controller seam, F4 capture, kwarg placement, slot-NAME factory, config/flag threading, `_T1_PROXY_BINDING`, or the import boundary — all verified consistent.

## QA Complete
