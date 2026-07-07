# QA Report — Step 6.G7 crossref-chain lens (AC #1–12 traceability)

**Task:** TASK-RF-t2-fallback-ladder-20260706-050832
**Phase:** task-qualitative (crossref-chain lens, report-only)
**Date:** 2026-07-07
**Fix authorization:** false (report-only)
**Scope:** trace each acceptance criterion AC #1–12 end-to-end
(requirement → design section → implementing code → proving test) and verify every link exists.

---

## Overall Verdict: PASS (with 1 IMPORTANT + 2 MINOR coverage findings)

All 12 AC chains are **complete and green**: every requirement maps to a design
section, an implementing code surface, and at least one proving test that
actually executes and passes. I ran the proving tests directly — **86 reflect
fallback/verdict tests + 50 swarm T1/read_env_for_pool tests all pass**. No
chain is broken (no missing code, no phantom test, no citation drift).

The verdict is PASS on the crossref question ("does every link exist"). It is
**not clean**: AC #6's wall-clock half is proven only at the pure-planner level;
the impure controller's wall-clock behavior is untested (F1, IMPORTANT). This
should be closed before the task is marked Done.

Adversarial note: the spawn framing assumed ≥5 broken AC→code→test chains. I
looked hard (ran the suites, reversed-ladder binding test, counter-case, F6
first-match) and did not find broken chains — the implementation and its tests
are unusually tightly coupled to the design. The honest finding is a
**coverage-depth** gap on one AC sub-path, not a severed chain.

---

## Per-AC Coverage Table

| AC | Requirement (merged-requirements.md:633–644) | Design § | Implementing code | Proving test | axis | Result |
|----|----------------------------------------------|----------|-------------------|--------------|------|--------|
| 1 | single terminal primary failure repaired by T1Model01 | §8, §11 row1 | `plan_next_attempt` dispatch branch (fallback.py:204–214); `run_fallback_ladder` loop | `test_fallback_plan::test_dispatches_first_ladder_slot_when_quorum_unmet`; `test_ensemble_fallback_stub::test_incident_replay_certifies_tier2_with_fallback` (2-fail superset a fortiori) | none | PASS |
| 2 | multiple terminal failures escalate to T1Model02 | §4.2 ordering invariant, §11 row2 | next-unattempted-slot logic (fallback.py:204); ordering invariant keeps T1Model01 first | `test_fallback_plan::test_first_pass_with_multiple_primary_failures_still_dispatches_t1model01` (asserts T1Model01 first) + `test_ensemble_fallback_stub::test_counter_case…` (2 fails → T1Model01→T1Model02) | none | PASS |
| 3 | T1Model01 terminal failure escalates to T1Model02 | §11 row3 | failed fb not counted in `evaluate_quorum` successes; next slot dispatched (fallback.py:435–475) | `test_fallback_plan::test_second_attempt_dispatches_t1model02_not_t1model01_again`; counter-case (T1Model01 proxy_error → T1Model02) | none | PASS |
| 4 | T1Model01 success but diversity-short → T1Model02 | §11 row4 | quorum.satisfies_tier2 False on single-vendor → eligible_failures still non-empty → next slot (fallback.py:157–214) | `test_fallback_plan::test_later_pass_can_escalate_when_t1model01_success_did_not_repair_diversity` | none | PASS |
| 5 | fallback never before retry+salvage | §2 seam (post-normalize_wave2) | ensemble.py:343–373 seam: `run_fallback_ladder` called AFTER `normalize_wave2`; salvaged parse_error arrives as success (not eligible) | `test_fallback_classify::test_salvaged_parse_error_arrives_as_success_and_is_not_eligible`; `test_ensemble_fallback_engage` (real `run_tier2_ensemble` seam, ON+OFF) | none | PASS |
| 6 | bounded by attempt count AND wall-clock | §7.4 (F4), §11 row6 | attempts: `while len(attempts_made) < max_attempts` (fallback.py:435). wall-clock: `_wall_clock_ok` + clamp (fallback.py:288–299,438,457–458); deadline captured ensemble.py:322 | attempts: counter-case + `test_ladder_exhaustion_reports_pool_exhausted`. **wall-clock: ONLY `test_fallback_plan::test_wall_clock_exhaustion_stops_before_dispatch` (pure planner, flag passed directly)** | AX-3 | **PASS (weak — see F1)** |
| 7 | original primary failures visible | §11 row7 | `primary_failures_preserved` + full-primaries ledger (fallback.py:427,513–521,559) | `test_contract_fallback_metadata::test_primary_failures_are_preserved…`; `test_ensemble_fallback_stub::test_incident_replay…` (exact list) | none | PASS |
| 8 | fallback uses same normalize contract | §11 row8 | injected `normalize=normalize_wave2` + same `prompt`; `_REFLECT_REVIEW_RECIPE="passthrough"` (fallback.py:44,387–395) | F2 stamp→normalize stable final_path in `test_ensemble_fallback_stub` + `test_ensemble_fallback_engage` (real seam) | AX-1 | PASS (see F2 drift note) |
| 9 | Tier-2 still needs 2 heterogeneous successes | §11 row9 | unchanged `evaluate_quorum` (count≥2 ∧ mcd=full ∧ vendor) + `build_reflect_contract` tier gate (fallback.py:157–167; ensemble.py:731–737) | `test_fallback_select` suite; incident replay tier_reached=2; counter-case tier_reached=1 | none | PASS |
| 10 | genuine failure stays degraded/exit 11 | §6/§8 counter-case | short contributing set → existing first-match `degraded-tier1` (T6) fires; fallback block explanatory only | `test_ensemble_fallback_stub::test_counter_case…` (DEGRADED/11); `test_contract_fallback_metadata::test_degraded_with_fallback_metadata_keeps_real_verdict_reason` (F6); `test_verdict_mapping::test_degraded_tier1_first_match_precedes_single_reviewer_fallback` | none | PASS |
| 11 | metadata distinguishes primary-only vs fallback | §11 row11 | `certified_with_fallback` + `original_primary_pool_fully_succeeded` + `tier2_certification_basis` (fallback.py:118–137) | `test_contract_fallback_metadata::test_tier2_certification_basis_distinguishes…` | none | PASS |
| 12 | no proxy keys emitted | §7.3, §11 row12 | creds live only in `build_transport` closure (ensemble.py:269–278); ledger emits only model_id/vendor/status | `test_contract_fallback_metadata::test_contract_metadata_does_not_leak_proxy_secret_names_or_urls` (forbids ProxyUrl/ProxyKey/api_key/base_url/http/https/:4000/cli) | none | PASS |

Legend: axis `none` = five-axis lens applied, nothing fired on this row.

---

## Findings

| # | Severity | Location | Issue | Recommended fix |
|---|----------|----------|-------|-----------------|
| F1 | IMPORTANT | AC #6 wall-clock proving link; `fallback.py:288–299,438,457–458` (`_wall_clock_ok`, clamp, sub-floor stop) | The wall-clock half of AC #6 is proven **only** at the pure-planner level (`test_fallback_plan::test_wall_clock_exhaustion_stops_before_dispatch` passes `wall_clock_ok=False` directly). The impure controller's `deadline_monotonic → _wall_clock_ok` computation, the `remaining > _FALLBACK_WALL_CLOCK_FLOOR_SEC` (1.0s) stop, and the `timeout_sec = min(config.timeout_seconds, remaining)` clamp are **untested** — all 3 `run_fallback_ladder` stub calls pass `deadline_monotonic=None`, and `test_ensemble_fallback_engage` uses a far-future deadline (default 3600s). A sign error or floor-comparison bug in `_wall_clock_ok` would ship silently, yet §7.4/F4 elevated wall-clock to a load-bearing "decided, not deferred" bound. | Add one `run_fallback_ladder` test with `deadline_monotonic=time.monotonic() - 5` (or `+0.5`, below the 1.0s floor) asserting `terminal_reason == "fallback_wall_clock_exhausted"`, `engaged`/`fallback_attempt_count == 0`, and no dispatch occurred; plus one with a mid-range remaining asserting the attempt timeout is clamped. |
| F2 | MINOR | AC #8; `fallback.py:44` vs `ensemble.py:80` | The reviewer normalize recipe is duplicated as two independent string literals (`_REFLECT_REVIEW_RECIPE = "passthrough"` in fallback.py, `REFLECT_REVIEW_RECIPE = "passthrough"` in ensemble.py). Design-sanctioned to avoid the ensemble↔fallback import cycle, and commented as such — but if ensemble's recipe ever changes off `"passthrough"`, the fallback path silently diverges and AC #8's "same normalization contract" quietly breaks with no failing test. | Optional: host the recipe constant in the leaf `reflect/_diversity.py` (or another cycle-free module) and import into both; or add an assertion test `fallback._REFLECT_REVIEW_RECIPE == ensemble.REFLECT_REVIEW_RECIPE` to pin the equivalence. |
| F3 | MINOR (observation) | AC #2 literal wording | The requirement's literal "multiple failures escalate to T1Model02" is satisfied **indirectly**: the implementation is failure-count-agnostic (next-unattempted-slot), so T1Model02 is reached only after T1Model01 has run and quorum is still unmet — never as a direct multi-failure jump. This is intentional and correctly documented in design §4.2 (ordering invariant) with a mandated first-T1Model01 test. No action required; recorded so a future reader does not mistake the next-slot logic for a bug against AC #2's phrasing. | None. |

---

## Summary
- AC chains traced: 12 / 12 — all links (requirement → design → code → test) exist.
- Chains broken: 0
- Proving tests executed green: 86 (reflect) + 50 (swarm) = 136
- Findings: IMPORTANT 1 (F1 wall-clock controller coverage), MINOR 2 (F2 recipe-literal drift, F3 wording observation)

## Confidence
Verified: 12/12 AC chains | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
Tool engagement: Read 17 | Grep/Bash 6 | pytest runs 2 (136 tests green)

## Recommendations (before marking task Done)
1. Close F1: add controller-level wall-clock tests to `test_ensemble_fallback_stub.py` (exhausted-deadline stop + timeout clamp). Without it, AC #6's wall-clock guarantee rests on inspection, not proof.
2. Consider F2: pin recipe-name equivalence so AC #8 cannot silently regress.
3. F3 needs no action.

## QA Complete
