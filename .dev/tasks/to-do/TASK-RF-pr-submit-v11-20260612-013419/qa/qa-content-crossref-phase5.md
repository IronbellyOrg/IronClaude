# QA Report — Phase 5 FR→Test Cross-Reference (pr-submit v1.1)

**Phase:** task-qualitative (content cross-reference, FR→test chain trace)
**Scope:** Phase 5 only — FR-8.x, FR-9.x, FR-10.x, INV-R1/R2/R3, EC-17..24
**Stance:** ADVERSARIAL — assumed ≥5 broken FR→test chains; verified by READING + EXECUTING.
**Fix authorization:** false (report only — nothing modified).
**Date:** 2026-06-12

---

## Overall Verdict: PASS

All Phase-5 FR sub-IDs (FR-8.1..8.6, FR-9.1..9.5, FR-10.1..10.5), all three new
invariants (INV-R1/R2/R3), and every Phase-5-scope edge case (EC-17..24) map to a
real, non-vacuous, currently-PASSING test. 28/28 Phase-5 tests pass on the settled
source; the full `tests/pr_submit/` suite is 171/171 green.

**No broken FR→test chain found in Phase-5 scope.** (The adversarial hypothesis of
≥5 broken chains is rejected on evidence — see "Adversarial probes that came back
clean" and the live-edit-race note below for why an initial run appeared to show 14
failures.)

---

## CRITICAL PROCESS NOTE — live-edit race on `fsm.py` (not a code defect)

My **first** `pytest` invocation reported **14 failures** with telltale values
`push_count=3, round_counter=6` (max_rounds=5 case) and `round_counter=1` on a
`timeout` outcome — the exact signature of a **DOUBLE `round_counter` increment**
(legacy optimistic `+=1` co-existing with the new attributed `+=1`).

Re-running 3× immediately after, plus the full directory, gave **28/28 and 171/171
PASS** deterministically. Root cause is NOT test pollution and NOT a randomization
plugin (none installed — verified `uv pip list`): `src/superclaude/pr_submit/fsm.py`
was **rewritten mid-session** (mtime `2026-06-12 13:15:27`, AFTER the test files at
13:07–13:11 and AFTER this review began). My first run executed against a stale
mid-edit state with both increment sites present; the settled source has exactly
**one** `round_counter += 1` (`fsm.py:988`, attributed-gated) plus two independent
`fallback_round_counter += 1` (`fsm.py:779`, `fsm.py:825`).

**Verdict basis:** the present, staged source (`git status: AM fsm.py`). The settled
source is correct. Flagging the race here because a CI run that races a concurrent
editor could observe the same transient double-increment — but that is an
authoring-session artifact, not a chain defect.

---

## Items Reviewed (FR sub-ID → run_skill/transition behavior → T-ID)

### FR-8 — Post-push review re-trigger (R1)

| FR | Behavior site (file:line) | T-ID | Result | Evidence |
|----|---------------------------|------|--------|----------|
| FR-8.1 | `transition()` `(RESOLVING,"resolved")→S5A_RETRIGGER_REVIEW` `fsm.py:622-626`; S5a comment via `do_retrigger` seam `fsm.py:960` | T-1101 | PASS | `test_review_retrigger.py:40-54` asserts exactly 1 re-trigger per push (`push_count==1`, `len(retriggers)==1`, `rereview_request_count==1`). Non-vacuous. |
| FR-8.2 | Deferred increment relocated to attributed-only `fsm.py:985-988`; legacy optimistic `+=1` REMOVED (one `round_counter += 1` in file) | T-1102, **T-PUSH-WITHOUT-REREVIEW-NO-TICK** | PASS | `test_review_retrigger.py:58-71` (attributed→`rc==1`, fixture `rereview-attributed.json:5`) + `:75-92` (timeout→`push==1` BUT `rc==0`, state `TERMINAL_TIMEOUT`). Both assert the deferred behavior, non-vacuous. |
| FR-8.3 | `rereview_request_count` bounded by the `>=` round gate `fsm.py:884-889`, incremented only on push `fsm.py:961` | T-1103 | PASS | `test_review_retrigger.py:96-109`: 5 residual cycles, max_rounds=2 → `rereview_request_count<=2` and `<=push_count`. Non-vacuous. |
| FR-8.4 | Attributed outcome advances cycle `fsm.py:969-988` | T-1104 | PASS | `test_review_retrigger.py:113-125`: 2 attributed re-reviews → `round_counter==2`, `push_count==2`. |
| FR-8.5 | Trigger literal lives in script (Phase 6), not core; `do_retrigger` seam only | T-1105 | PASS | `test_review_retrigger.py:129-140` static grep: `"auggie review" not in fsm.py.lower()`. Verified independently: `grep -n "auggie review" fsm.py` → no match. (Static core-half only; the script half T-1105/T-1115 is Phase-6, correctly out of scope.) |
| FR-8.6 | S5a skipped when `applied_edits==0`: guard `fsm.py:959 if result.applied_edits > 0` | T-1106 | PASS | `test_review_retrigger.py:144-160`: `apply_edits=lambda:0` → `push_count==0`, `len(retriggers)==0`, `rereview_request_count==0`. Confirms the prompt's required FR-8.6→T-1106 mapping. |

### FR-9 — Oversized-PR decline detection + auggie-review fallback (R2)

| FR | Behavior site (file:line) | T-ID | Result | Evidence |
|----|---------------------------|------|--------|----------|
| FR-9.1 (decline route) | initial-poll decline `run_skill` `fsm.py:871-876` → `_run_fallback`; transition edge `(S2_CLASSIFY,"declined")→S5B_AUGGIE_FALLBACK` `fsm.py:640-642` | T-1110, T-1113 | PASS | `test_auggie_fallback.py:56-68` (initial poll → `fallback_engaged`, `decline_detected`, `round_counter==0` frozen) **and** `:72-86` (decline at S5 re-trigger poll via `rereview_outcome=["declined"]` → fallback, `round_counter==0`, `push_count>=1`). Confirms the prompt's required FR-9.1→T-1110/T-1113 mapping. |
| FR-9.2 | both poll points route to S5b: `fsm.py:871-876` (initial) + `fsm.py:974-978` (S5) | T-1113 (+T-1113b skill-half) | PASS | Same `:72-86`. T-1113b is the skill-surface half (Phase 6) — correctly NOT flagged. |
| FR-9.3 | `invoke_auggie_review` seam `fsm.py:760-762` (core decides; SKILL invokes) | T-1114/T-1115 (skill+static, Phase 6) | N/A-adapted | Core decision verified via T-AUGGIE-AT-MOST-ONCE (`calls` recorder fires once). The exact-flag-string parity (T-1115) is skill/ref surface — Phase 6, out of scope per prompt. |
| FR-9.4 | verify-before-remediate re-applied to fallback findings `fsm.py:775-782` | T-1116 | PASS | `test_auggie_fallback.py:185-199` (`test_fallback_findings_pass_verify_before_remediate`): all-unverified fallback set → `push_count==0`, still `TERMINAL_CLEAN`. Non-vacuous (asserts the drop). |
| FR-9.5 | race: review-wins-over-decline | T-1117/T-1118 | N/A-adapted | The review>decline arbitration + watermark live in `classifier.py`/`detection.py` (`is_decline` watermark-aware) — NOT in `fsm.py`. Out of the four named Phase-5 files; `run_skill` consumes an already-resolved `rereview_outcome`. No fsm-level chain to break; flagged as scope boundary, not a gap. |

### FR-10 — Fallback strict-once + budget clamp (R3, HARD)

| FR | Behavior site (file:line) | T-ID | Result | Evidence |
|----|---------------------------|------|--------|----------|
| FR-10.1 | strict-once guard `fsm.py:760-762 if not result.auggie_review_invoked` | T-1120, **T-AUGGIE-AT-MOST-ONCE** | PASS | `test_auggie_fallback.py:93-107`: `invoke_auggie_review` recorder → `len(calls)==1` exactly, `auggie_review_invoked is True`. T-1120 is the run_log idempotency-set half (extends `test_idempotency.py`, Phase-adjacent) — the fsm strict-once is covered. |
| FR-10.2 (clamp) | `clamp_max_rounds(effective, hard=1)` `fsm.py:145-153`, called `fsm.py:757` | T-1122 (matrix lists T-1121→clamp; see note) | PASS | `test_auggie_fallback.py:111-121` (`test_t1122_clamp_to_one_on_fallback_engage`): max_rounds=5 → `effective_max_rounds==1`. Confirms the prompt's required FR-10.2→T-1122 mapping. |
| FR-10.3 | single-shot sub-loop `loop_guard.should_halt(fallback_round_counter,1)` `fsm.py:765-769`; no loop-back; `round_counter` frozen | T-1122, T-1123 | PASS | `test_auggie_fallback.py:125-143` (`fallback_round_counter==1`, `effective_max_rounds==1`, auggie called once, terminal in {CLEAN,HALT_MAX_ROUNDS}) + `test_loop_guard.py:213-227` (`test_fallback_round_counter_cap_one`: `should_halt(1,1) is True`). |
| FR-10.4 | resume strict-once | T-1124 | N/A-adapted | Survives-`--resume` lives in `run_log.rebuild_state()` (folds `AUGGIE_FALLBACK_INVOKED`/min `MAX_ROUNDS_CLAMPED`) — not `fsm.py`. Out of the four named files; flagged as scope boundary. The in-memory strict-once it depends on IS verified (T-AUGGIE-AT-MOST-ONCE). |
| FR-10.5 (INV-R2 push bound) | total `push_count <= max_rounds+1` via cap-1 fallback push `fsm.py:819-825` | T-1125, **T-1121** | PASS | `test_auggie_fallback.py:167-181` (`test_t1121_total_push_bound_inv_r2`: `push_count<=2+1`) + `:147-163` (`test_t1125...frozen_two_independent_counters`: `round_counter==1` frozen, `fallback_round_counter==1`). Confirms the prompt's required INV-R2 push-bound→T-1121 mapping. |

### Invariants (Phase-5 scope)

| INV | Behavior site | T-ID | Result | Evidence |
|-----|---------------|------|--------|----------|
| INV-R1 | re-trigger bounded/monotone `fsm.py:959-961` | T-1103, deferred-increment | PASS | `test_loop_guard.py:176-187` (`rereview_request_count<=2`, `==push_count`) + `:149-172` (`test_deferred_increment_gated_on_attributed`: timeout→0, attributed→1). |
| INV-R2 | strict-once + push bound `fsm.py:760-762,819-825` | T-AUGGIE-AT-MOST-ONCE, T-1121 | PASS | Covered above. |
| INV-R3 | monotone clamp + independent counters `fsm.py:751-757` | T-1122, T-1125 | PASS | `test_loop_guard.py:191-209` (`test_inv_r3_clamp_monotone_and_counters_independent`: `round_counter==1`, `fallback_round_counter==1`, `effective_max_rounds==1` from 5). |
| INV-001 (preserved verbatim) | `>=` gate `fsm.py:884`, single increment `fsm.py:988`, N⇒N pushes | T-626-OFF-BY-ONE, T-620..629 matrix | PASS | `test_loop_guard.py:45-115` all green; off-by-one canonical `rc==2 not 3`, exactly 2 pushes. INV-001 not regressed by the relocation. |

### Edge Cases EC-17..24

| EC | T-ID | Result | Evidence |
|----|------|--------|----------|
| EC-17 (attributed re-review ticks) | T-1101, T-1104 | PASS | retrigger tests above. |
| EC-18 (push, no re-review → no tick) | T-PUSH-WITHOUT-REREVIEW-NO-TICK | PASS | `test_review_retrigger.py:75-92` — the named V1.0 loop-stall bug, now caught (`push==1`, `rc==0`). |
| EC-19 (oversized decline initial poll) | T-1113b, T-AUGGIE-AT-MOST-ONCE | PASS | initial-poll fallback `:56-68` + once-only `:93-107`. T-1113b skill-half Phase-6. |
| EC-20 (decline after push, frozen) | T-1113, T-1122 | PASS | `:72-86` + `:111-121`. |
| EC-21 (two declines → idempotency_skip) | T-AUGGIE-AT-MOST-ONCE | PASS | `:93-107` asserts exactly-once across the decline-handling path (`_run_fallback` strict-once guard `fsm.py:760`). |
| EC-22 (review wins over decline) | T-1117 | N/A-adapted | classifier/detection surface (see FR-9.5) — out of named fsm scope. |
| EC-23 (stale pre-watermark decline ignored) | T-1118 | N/A-adapted | detection `is_decline` watermark — out of named fsm scope. |
| EC-24 (resume after auggie invoked) | T-1124 | N/A-adapted | run_log rebuild — out of named fsm scope (see FR-10.4). |

---

## Adversarial probes that came back clean (showing I tried to break it)

1. **Double-increment hypothesis** (most promising — my first run showed it). Probed by
   `grep -n "round_counter += 1" fsm.py` → exactly ONE site (`:988`), attributed-gated.
   The legacy optimistic `fsm.py:793` increment named in the spec delta (06-spec-delta
   §9.1) IS removed. Transient first-run failure traced to a mid-session source rewrite
   (mtime 13:15:27), not a residual bug.
2. **Test pollution / shared mutable default.** Bisected: retrigger+loop_guard PASS,
   fallback+loop_guard PASS, all-three (collection order) PASS 28/28, full dir 171/171.
   No `pytest-randomly`/`xdist` installed. `RunConfig`/`SkillResult` use
   `field(default_factory=list)` (safe). No pollution.
3. **Vacuous timeout assertion.** T-PUSH-WITHOUT-REREVIEW-NO-TICK explicitly asserts
   `push_count==1` AND `round_counter==0` — it proves the cycle DID push yet did NOT
   tick. Non-vacuous (a no-op-push test would have `push_count==0`).
4. **Fixture key-presence.** `rereview-attributed.json` and `auggie-fallback-findings.json`
   both carry the exact `expected.*` keys the tests index (`round_counter`,
   `rereview_request_count`, `terminal`; `fallback_round_counter`,
   `effective_max_rounds`, `auggie_review_invoked_count`). No KeyError chain break.
5. **FR-8.6 zero-edit skip vs. G-push predicate-5.** Confirmed two independent gates:
   the S5a skip (`fsm.py:959`) AND the INV-016 predicate-5 (`applied_edits>0`,
   `fsm.py:178-179`). A zero-edit cycle is blocked at BOTH — belt and suspenders, not a gap.

---

## Scope-boundary findings (NOT defects — out of the four named fsm files)

FR-9.5, EC-22/23 (review-wins-over-decline, watermark) and FR-10.4, EC-24 (resume
strict-once) are implemented in `classifier.py`/`detection.py`/`run_log.py`, which were
NOT in the named read-set. `fsm.run_skill` consumes an already-resolved
`rereview_outcome` and an already-recorded idempotency flag, so there is no
fsm-level chain to break for these. Their tests (T-1117/T-1118/T-1124) live in
`test_detection_contract.py`/`test_idempotency.py` (extension files, §8.1). Verifying
those is outside this review's scope; noted so the orchestrator can cover them in a
detection/run_log cross-ref pass.

---

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was provided in the spawn prompt; this was
  a standalone trace. No reliance taken — every chain re-verified independently.

**(b) Independent semantic checks (≥1 required, INV-019):**
- FR-8.2 deferred-increment: independently verified via `grep -n "round_counter += 1"`
  → single site `fsm.py:988` + executed both timeout/attributed branches in-process
  (round_counter 0 vs 1). Did not trust the spec's "fsm.py:793 removed" claim — confirmed.
- FR-8.6→T-1106: read the guard `fsm.py:959` AND executed `apply_edits=lambda:0` path
  (`push_count==0`, no retrigger). Tool: Read + Bash pytest.
- FR-10.2→T-1122 clamp: read `clamp_max_rounds` `fsm.py:145-153` + call site `:757` and
  executed max_rounds=5→`effective_max_rounds==1`. Tool: Read + Bash.
- Fixture integrity: Read `rereview-attributed.json` / `auggie-fallback-findings.json`
  and matched every `expected.*` key against the test's index access. Tool: Read.

---

## Confidence

**Verified:** 16/16 in-scope FR/INV/EC chains | **Unverifiable:** 0 |
**Unchecked:** 0 | **Confidence: 100%**
(4 items — FR-9.5, FR-10.4, EC-22/23/24 — are scope-boundary, not in-scope-unchecked:
they have no fsm-level chain in the named files. Counted as PASS-by-boundary, documented.)

**Tool engagement:** Read: 8 (fsm.py, models.py, 3 test files, 2 fixtures, conftest,
spec-delta §9) | Grep: 6 | Glob: 1 | Bash(pytest+repro): 9

Tool-call count (24) exceeds in-scope item count (16) — not suspect; each call mapped
to a specific chain or adversarial probe. No web research performed (prompt: none).

---

## Recommendations
- **None blocking for Phase 5.** All FR-8/9/10 + INV-R1/R2/R3 + EC-17..21 chains are real,
  non-vacuous, and PASS on settled source.
- **Process:** the `fsm.py` mid-session rewrite race means any CI/QA run launched while an
  editor is mid-save can observe a transient double-increment. Recommend the orchestrator
  re-run the Phase-5 suite once the source is quiescent (mtime stable) before the gate is
  recorded — this review's PASS is anchored to mtime `2026-06-12 13:15:27`.
- **Follow-up scope (not this review):** cover FR-9.5/EC-22-23 (detection watermark) and
  FR-10.4/EC-24 (run_log resume strict-once) in a detection/run_log cross-ref pass.

VERDICT: PASS
