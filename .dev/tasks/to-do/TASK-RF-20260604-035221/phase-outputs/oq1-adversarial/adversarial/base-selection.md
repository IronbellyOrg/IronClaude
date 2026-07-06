# Base Selection & Recommendation — OQ-1 Signal B

## Scoring (decision-adapted hybrid, 0.0–1.0; higher = better)

| Dimension | Weight | Opt-1 (minimal) | Opt-2a (localized deeper) | Winner |
|---|---|---|---|---|
| Correctness/safety for the crash-tail scenario | 0.30 | 0.55 — fails closed (SAFE) but the integrity gate provides ZERO validation for recovered seams; always STOPs them | 0.90 — gate validates recovered seams; still fails closed for genuinely-suspect ones | Opt-2a |
| Design-intent alignment | 0.20 | 0.45 — ships a gate whose transcript axis is STRUCTURALLY useless for PASS_RECOVERED; "independence" preserved in form, lost in substance | 0.85 — replaces the structurally-incompatible transcript axis with the executor's recovery evidence (itself transcript-based); 2 independent signals preserved | Opt-2a |
| Feature value (auto-resume headline = crash-tail) | 0.20 | 0.40 — recovered crash-tails (a COMMON case, A-001) always require operator override | 0.90 — recovered crash-tails auto-validate | Opt-2a |
| Blast radius / risk | 0.15 | 0.95 — ~1 line, behavior-neutral, mergeable now | 0.75 — localized to integrity.py; does NOT touch shared `_classify_transcript`; small + guarded | Opt-1 |
| Test burden | 0.15 | 1.00 — zero new tests | 0.80 — one focused regression test (recovered last_completed → validated_last True) + a negative case | Opt-1 |
| **Weighted total** | | **0.61** | **0.85** | **Opt-2a** |

Edge-case-floor: both eligible (both reason about boundary/guard conditions).

## Selected base: **Opt-2a (localized deeper fix)**

Margin 0.85 vs 0.61 (24 pts) — NOT a tiebreaker situation. Opt-2a wins the three highest-weight dimensions (correctness, design-intent, feature-value); Opt-1 wins only the two lowest-weight dimensions (blast-radius, test-burden), which are cost dimensions, not value dimensions.

## Recommendation: choose **Opt-2 (constrained to approach 2a)**

**Why (the load-bearing reason):** Opt-1's `derived.is_success` widening is a *permanent false negative*, not a deferral. `_classify_transcript` can never emit `PASS_RECOVERED` and a recovered task's transcript is an error envelope by design (rerun_tasks.py:547-593), so under Opt-1 Signal B is **structurally guaranteed** to fail for every recovered last_completed — the integrity gate is permanently useless for the exact crash-tail scenario auto-resume exists to handle. Opt-1 does not "leave the door open"; it ships a gate that always STOPs recovered seams.

Opt-2a fixes this with the SAME safety posture and a contained blast radius:
- Trusts the executor's `PASS_RECOVERED` determination for Signal B **only** — and that determination is itself transcript-evidence-based (`detect_error_max_turns` + `_task_completed_before_overrun` require completion evidence before the overrun, executor.py:997-1011 / 2321-2330). So this is NOT "blind trust in persisted status"; it substitutes the only transcript-based check that *can* validate a recovered tail for the one that structurally cannot.
- Preserves a genuine **2-signal double-check** for recovered tasks: persisted-status (Signal A) ∧ artifact-existence (`artifacts_ok`). The persisted claim alone is still insufficient.
- Does **NOT** touch the shared `_classify_transcript` (Opt-2b is rejected — it would spill into `discover_failed_tasks_from_transcripts`, rerun_tasks.py:596-625). Blast radius stays in `integrity.py`.

**Implementation guardrails (both advocates surfaced these — bake into the fix):**
1. Guard the exemption narrowly: `if lc.persisted_status is TaskStatus.PASS_RECOVERED: signal_b_pass = True` — ordinary `PASS` MUST still be transcript-rechecked.
2. Keep Opt-1's `derived is not None and derived.is_success` widening as future-proofing for the non-recovered path.
3. Transparency: set `lc.derived_status = TaskStatus.PASS_RECOVERED` (or annotate) so the report shows Signal B was satisfied by executor-recovery evidence, not a clean PASS transcript.
4. Tests (mandatory): (a) recovered `last_completed` + present artifacts → `validated_last is True`; (b) negative — an over-claimed/missing-artifact recovered seam still STOPs; (c) ordinary false PASS claim still fails Signal B (no over-broad trust).

**Acceptable fallback:** If PR #124 must merge under time pressure, ship Opt-1 now (safe, fails closed) and do Opt-2a as a fast-follow — BUT document explicitly that until then, auto-resume STOPs on every recovered crash-tail and requires operator confirmation. Given Opt-2a is localized + low-risk, doing it directly (in the same PR or a tight follow-up) is preferred over leaving the gate permanently degraded.

## Return contract
```yaml
merged_output_path: null            # decision/recommendation, not a merge
convergence_score: 0.85
artifacts_dir: ".dev/tasks/to-do/TASK-RF-20260604-035221/phase-outputs/oq1-adversarial/adversarial/"
status: "success"
base_variant: "Opt-2a (localized deeper)"
unresolved_conflicts: 0
fallback_mode: false
failure_stage: null
invocation_method: "skill-direct"
unaddressed_invariants: []          # Round 2.5 skipped (depth=quick)
```
