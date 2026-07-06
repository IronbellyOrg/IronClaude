# QA Content Report — DOMAIN-ACCURACY (Phase Gate B)

**Lens:** DOMAIN-ACCURACY (spec-intent vs code behavior, load-bearing invariants)
**document_type:** sc:pr-submit deterministic core + refs
**Date:** 2026-06-11
**fix_authorization:** false (report only)
**Stance:** Adversarial — assumed ≥10 divergence sites; read spec lines and code lines side-by-side.

---

## Method

Read side-by-side:
- Spec `merged-spec.md` §5 (249-340), §9 (592-659), §10 (663-693), §11 (697-744), §12 (748-792), §13 (810-827).
- Code `pr_submit/{fsm,loop_guard,recovery,run_log,severity_router,classifier,detection,models}.py`.
- Ref `skills/sc-pr-submit-protocol/refs/detection-contract.md`.
- Tests `tests/pr_submit/{test_loop_guard,test_crash_recovery,test_edge_cases,test_skill_parse}.py`.

Every judgment below cites BOTH a spec line and a code line.

---

## Invariant-by-Invariant Verdicts

### INV-001 (loop_guard) — PASS

- **Increment edge / `>=` gate.** Spec L604-606 + INV-5 L618-619: gate is `round_counter >= max_rounds` (`>=`, NOT `>`); `max_rounds=N` → exactly N pushes. Code `loop_guard.should_halt` (loop_guard.py:30) `return round_counter >= max_rounds`; `fsm.should_halt_rounds` (fsm.py:142) delegates to the SAME function (single source, no drift). PASS.
- **Off-by-one (T-626 canonical).** Spec L641-644: at `max_rounds=2`, residual×3 → `round_counter==2` NOT 3, exactly 2 pushes. Traced `run_skill` (fsm.py:718-800) with 3 cycles: cycle0 push→counter=1; cycle1 push→counter=2; cycle2 gate `2>=2` True → HALT_MAX_ROUNDS, push_count=2. Matches test_t626 (test_loop_guard.py:45-58). PASS.
- **Monotonicity (INV-4).** Spec L617 / L657-659: a vanished counted re-review does NOT decrement. Code `RoundCounter.vanished_rereview` (loop_guard.py:63-69) is an explicit no-op. PASS.
- **User label.** Spec L606 `round_counter + 1`. Code `user_label` (loop_guard.py:35) `return round_counter + 1`. PASS.
- **Single increment site.** Spec L602-607 "nowhere else". Code: only `RoundCounter.on_rereview` (loop_guard.py:58-59) and `run_skill` line 793 mutate the counter; both model the S5→S2 attributed re-review. PASS.
- **Modeling note (not a defect):** `run_skill` ticks the counter immediately after a push (fsm.py:793) rather than literally at the next-observed re-review. Observable behavior (counter value, push count, gate-at-top-of-cycle timing) is identical to the spec edge and is proven by the fence-post matrix (test_loop_guard.py:74-78). Acceptable simplification.

### INV-007 (recovery) — PASS

- **Push triad order.** Spec L756-763: `push_decision → push_initiated → push_completed`. Code `build_push_triad` (fsm.py:240-260) returns the list in exactly that order. PASS.
- **3-way crash window.** Spec L765-773 + code `resolve_crash_window` (recovery.py:102-135):
  - Branch A (reachable) → append `push_completed{recovered:true}`, resume `S5_AWAITING_REREVIEW` (recovery.py:102-111). PASS.
  - Branch B (not reachable) → append `push_aborted_or_not_landed{recovered:true}`, return `S4_PUSHING` to re-drive the SAME cycle. Comment + code (recovery.py:113-123) explicitly "WITHOUT recomputing the fix". PASS.
  - Branch C (ambiguous tip) → `TERMINAL_HALTED` + `HALT_HUMAN`, carries `observed_remote_sha` + original fields (recovery.py:125-135). PASS.
- **PRE-push idempotency key.** Spec L762-763 `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>` (PRE-push SHA). Code `push_idempotency_key` (fsm.py:207) builds exactly that, keyed on `pre_push_sha`. PASS.
- **No-double-push.** `detect_crash_window` (recovery.py:47-70) matches a dangling `push_initiated` against BOTH `push_completed` AND `push_aborted_or_not_landed` finalizers; Branch A synthesizes the completion without emitting a new `push_initiated` (verified test_crash_recovery.py:236-240). PASS.

### INV-016 (fsm.evaluate_push_decision) — PASS

- **5-predicate conjunction.** Spec L319-331 verbatim vs code (fsm.py:163-168):
  - p1 `monitor_ordinal >= 3` (fsm.py:163) ✓
  - p2 `validation_status == "validated"` (fsm.py:164) ✓ literal matches spec L322 + L667
  - p3 `not needs_human_decision` (fsm.py:165) ✓
  - p4 `round_counter < max_rounds` (fsm.py:166) ✓ (strict `<`, correct — distinct from the loop gate's `>=`)
  - p5 `applied_edits > 0` (fsm.py:167-168) ✓ closes the zero-edit hole (spec L324-325, L333-334)
  - `authorized = bool(p1 and p2 and p3 and p4 and p5 > 0)` (fsm.py:168) — full conjunction. PASS.
- **Fail-routing.** Spec L325-326: (3)→HALT_HUMAN, (4)→HALT_MAX_ROUNDS, (5)→TERMINAL_CLEAN/report, (1)-(2)→report-only. Code `push_fail_state` (fsm.py:185-191) routes in that precedence order. PASS.
- **Write-ahead audit record.** Spec L327-329 "mandatory at L3". Code `build_push_triad` emits `push_decision` first (fsm.py:241-253) naming each predicate. PASS.

### FSM gate table = ordinal comparisons, not nested ifs (§5.4) — PASS

- Spec L336-340 + §5.2 table L296-303. Code: `gate_arm` `ordinal >= 1` (fsm.py:127), `gate_edit` `ordinal >= 2` (fsm.py:132), G-push `ordinal >= 3` predicate-1 (fsm.py:163). `transition()` (fsm.py:560-619) is an edge-lookup table applying the three one-line ordinal gates at their edges, plus the `needs_human_decision` pre-gate override evaluated FIRST (fsm.py:574-575, matches spec L302-303). PASS.

### R1 probe HALTs, never auto-locks; ref ships `locked:false` — PASS

- **Ships `locked:false`.** detection-contract.md:24 `locked: false`. PASS.
- **HALT on unlocked.** `DetectionContract.load(require_locked=True)` raises `DetectionContractLocked` (detection.py:100-105) — the T-210 gate. Absent/unparseable contract also raises (detection.py:88-98). PASS.
- **Never auto-locks.** `poll_augment_review` with no contract uses a neutral UNLOCKED placeholder `DetectionContract()` with `augment_bot_login=None` (detection.py:154); the classifier matches no entries for any payload (classifier.py:41-43 `_augment_entries` returns `[]` when `bot_login` falsy) → fail-safe `"polling"` (classifier.py:75-77). No login guessed, nothing locked. PASS.

---

## Findings

| # | Severity | Location | Spec ref | Issue |
|---|----------|----------|----------|-------|
| 1 | IMPORTANT | `fsm.py:103-104` (`parse_args`) | spec L550-554 (EC-8) | **CLI parser rejects `--max-rounds 0`, which the spec mandates as a valid "monitor-but-never-remediate" configuration.** `parse_args` raises `ValueError("--max-rounds must be >= 1")` for `max_rounds < 1`. But EC-8 (spec L550-554) specifies `--max-rounds=0` as supported behavior: gate `0>=0` True → HALT before any fix; "Poll fires, findings reported, zero rounds." The deterministic core HONORS this — `run_skill(RunConfig(max_rounds=0))` correctly returns HALT_MAX_ROUNDS / round_counter==0 (proven by test_edge_cases.py:98-103). The contradiction is that the test reaches the behavior by constructing `RunConfig` directly, bypassing the CLI parser. A real user typing `/sc:pr-submit --monitor 3 --max-rounds 0` would be rejected at parse time, so the spec's EC-8 contract is unreachable through the documented CLI surface. Either the parser must accept `0` (and rely on the `0>=0` gate) or EC-8 must be amended. This is a parser-vs-spec divergence, not a counter defect. |

### Sub-threshold observations (not gating; recorded for completeness)

- **O-1 (seam, MINOR).** `transition()` S7_VALIDATING→"validated" edge returns `S4_PUSHING` unconditionally (fsm.py:602-604); the 5-predicate G-push conjunction is enforced only in `run_skill` (fsm.py:767-782), never in the raw table. Spec §5.3 explicitly defines G-push as a runtime conjunction "immediately before git push" (L319-320), and no test drives `transition()` for the push edge — all autonomy gating flows through `run_skill` (test_autonomy_gates.py:80,100). Acceptable per the spec's own framing, but `transition()` is not self-sufficient for push authorization; a future caller using the bare table would bypass G-push. Worth a docstring caution.
- **O-2 (seam, MINOR).** `is_groundable` (fsm.py:271-279) implements the EC-9 structural drop (empty path / non-positive line) but is NOT wired into `run_skill`'s default pipeline — `_default_apply_edits` (fsm.py:642-650) filters only on `in_diff` + `verification_status`, not groundability. Defensible because the spec puts finding normalization/drop in the SKILL layer (the FSM "consumes already-classified data", fsm.py:11-13), and test_ec9 exercises the helper directly. No invariant in scope is violated, but the integration driver does not defend against an ungroundable finding reaching `apply_edits`.

---

## Self-Audit

**(a) Reliance list — items relied on from prior structural QA:**
- Relied on the manifest's structural counts (33 EventType members, 5 idempotency sets, file line counts) without re-counting every enum line.

**(b) Independent semantic checks (≥1 required):**
- Independently traced the T-626 off-by-one through `run_skill`'s loop arithmetic (fsm.py:718-800) rather than trusting the test name — confirmed counter==2 / push==2 by hand-execution against `_run(2,2)`.
- Independently cross-checked the `validated` literal in p2 (fsm.py:164) against BOTH spec L322 and the §10 definition L667 — confirmed single consistent string.
- Independently verified the EC-8 contradiction by reading `parse_args` (fsm.py:103-104) AND `test_ec8` (test_edge_cases.py:98-103) AND the spec EC-8 prose (L550-554) — the three disagree on whether `--max-rounds 0` is acceptable at the CLI.
- Independently confirmed `detect_crash_window` treats `push_aborted_or_not_landed` as a finalizer (recovery.py:62-66), closing the Branch-B re-drive loop against a double-detection.

**Tool engagement:** Read: 11 | Grep/Bash: 4 | Glob: 0

**Confidence:** Verified: 5/5 in-scope invariants traced to code+spec lines | Unverifiable: 0 | Unchecked: 0 | Confidence: 100% on the 5 named invariants. Found 1 IMPORTANT divergence + 2 MINOR seam observations against the adversarial ≥10 target — the core 5 invariants are faithfully implemented; the divergence is at the CLI-parser boundary, not the deterministic core.

---

## VERDICT: FAIL
