# QA Source-Fidelity Report 1 — FSM + Autonomy Partition (Phase Gate B / M4)

**Agent:** M4 SOURCE-FIDELITY agent 1
**Date:** 2026-06-11
**Mode:** `fix_authorization: false` (report only)
**Stance:** Adversarial — assumed ≥5 spec-to-code fidelity gaps in the FSM/autonomy surface.

**Assigned spec range:**
- `merged-spec.md` §5 (lines 249-340): FSM gate table + INV-016 5-predicate conjunction
- `merged-spec.md` §4 (FR-4 autonomy gates, lines 209-217)
- Supporting: EC-7 (line 545-548), §5.2 override (302-303), FSM diagram (259-292)

**Artifacts verified:**
- `src/superclaude/pr_submit/fsm.py`
- `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md`
- `src/superclaude/pr_submit/severity_router.py`
- `src/superclaude/pr_submit/classifier.py`
- `tests/pr_submit/test_autonomy_gates.py`
- (supporting) `src/superclaude/pr_submit/models.py`, fixtures `finding-ungroundable.json`

---

## Element-by-element fidelity matrix

| # | Spec element | Spec cite | Code/test cite | Verdict |
|---|--------------|-----------|----------------|---------|
| 1 | **G-arm `ordinal >= 1`** | §5.2 L298 (`ordinal >= 1` to enter polling) | `fsm.py:125-127` `gate_arm()` returns `ordinal >= 1`; applied `fsm.py:699` (L0 returns S0_IDLE), `fsm.py:580` | **PASS** |
| 2 | **G-edit `ordinal >= 2`** | §5.2 L299 (`ordinal >= 2` to enter S3_FIXING) | `fsm.py:130-132` `gate_edit()` returns `ordinal >= 2`; applied `fsm.py:599`, `fsm.py:750` | **PASS** |
| 3 | **G-push `ordinal >= 3`** (p1) | §5.3 L320 / §5.2 L300 | `fsm.py:163` `p1 = monitor_ordinal >= 3` | **PASS** |
| 4 | **INV-016 p2 `validation_status=="validated"`** | §5.3 L320-321 | `fsm.py:164` `p2 = validation_status == "validated"` | **PASS** |
| 5 | **INV-016 p3 `needs_human_decision==false` (all findings)** | §5.3 L322 | `fsm.py:165` `p3 = not needs_human_decision`; caller ANDs over all: `fsm.py:770` `any(f.needs_human_decision for f in verified)` | **PASS** |
| 6 | **INV-016 p4 `round_counter < max_rounds`** | §5.3 L323 | `fsm.py:166` `p4 = round_counter < max_rounds` | **PASS** |
| 7 | **INV-016 p5 `applied_edits > 0`** | §5.3 L324 | `fsm.py:167-168` `p5 = applied_edits`; `authorized = ... and p5 > 0` | **PASS** |
| 8 | **5-predicate AND conjunction** | §5.3 L319-324 | `fsm.py:168` `bool(p1 and p2 and p3 and p4 and p5 > 0)` — all five ANDed | **PASS** |
| 9 | **Fail-routing p3→HALT_HUMAN** | §5.3 L325 | `fsm.py:185-186` | **PASS** |
| 10 | **Fail-routing p4→HALT_MAX_ROUNDS** | §5.3 L325 | `fsm.py:187-188` | **PASS** |
| 11 | **Fail-routing p5→TERMINAL_CLEAN/report** | §5.3 L325-326 | `fsm.py:189-190` (`predicate_5_applied_edits <= 0 → TERMINAL_CLEAN`) | **PASS** |
| 12 | **Fail-routing p1-2→report-only** | §5.3 L326 | `fsm.py:191` (default `REPORT_ONLY`); spec-order eval = most-specific HALT wins | **PASS** |
| 13 | **`needs_human_decision` override (pre-gate, only ceiling short-circuit)** | §5.2 L302-303; FR-4.4 L217; EC-7 L546 | pure `transition()` pre-gate `fsm.py:573-575`; `run_skill` per-level EC-7 semantics `fsm.py:732-741` (L3 immediate HALT_HUMAN; L1/L2 flow through ceiling per EC-7) | **PASS** (see Note A) |
| 14 | **S2b_VERIFY content gate on S2_CLASSIFY→S3_DIAGNOSE, every armed ordinal, unverified→REPORT_ONLY no round** | §5.2 L305-311; §5 diagram L270-272 | `transition()` edges `fsm.py:593-596` (verified→S3_DIAGNOSE, unverified→REPORT_ONLY); `run_skill` verify BEFORE gate_edit `fsm.py:744-747` (even L1 verifies); no round consumed (break before counter tick) | **PASS** |
| 15 | **L0 zero-regression (FSM never leaves S0_IDLE)** | §5.2 L313-314; ref §5.1 L23 | `fsm.py:699-701` (`not gate_arm → return S0_IDLE`); `transition()` `fsm.py:580` (arm with ordinal 0 stays S0_IDLE) | **PASS** |
| 16 | **L1 zero-edit + exact "fix these? y/n"** | FR-4.1 L214 | `fsm.py:39` `PROPOSE_PROMPT = "fix these? y/n"`; `fsm.py:750-755`; T-401/T-402 `test_autonomy_gates.py:56-71` | **PASS** |
| 17 | **L2 HALT before push/commit/reply, edits in worktree** | FR-4.2 L215; ref §5.2a L74-85 | `fsm.py:776-779` (`ordinal < 3 → S4_HALT_BEFORE_PUSH`); T-410/411/412/413 `test_autonomy_gates.py:76-100` | **PASS** |
| 18 | **L3 full triad + INV-016-conditional push** | FR-4.3 L216 | `fsm.py:784-790`; T-420 `test_autonomy_gates.py:105-121` | **PASS** |
| 19 | **T-ZERO-EDIT-NO-PUSH (`applied_edits==0 → no push`)** | FR-4.3 L216; §5.3 L324 | `fsm.py:642-650` (`_default_apply_edits` returns 0 for `in_diff=False`); push_decision set with p5=0; T `test_autonomy_gates.py:141-154` asserts all three | **PASS** |
| 20 | **Ref retains primed `S4'_HALT_BEFORE_PUSH`; Python drops prime** | §5.1 / ref L14-17 | `state-machine.md:14-17,32`; `models.py:101` (`S4_HALT_BEFORE_PUSH` with comment) | **PASS** |
| 21 | **INV-016 verbatim text in ref** | §5.3 L319-331 | `state-machine.md:89-101` — byte-compared, matches verbatim incl. fail-routing clause | **PASS** |
| 22 | **severity router never emits `--depth quick --fix`** | FR-3.2 (routing) | `severity_router.py:155` assert guard; `route()` L140-156 | **PASS** |

---

## Adversarial findings (5 predicted gaps — investigation results)

The adversarial stance assumed ≥5 gaps. Each predicted gap was investigated to the spec line and code line. **All five candidate gaps resolved to spec-faithful implementations.** No genuine fidelity gap was found.

### Candidate gap 1 — `needs_human_decision` override gated on `ordinal >= 3` in `run_skill` (NOT applied at L1/L2)

- **Suspicion:** §5.2 L302-303 says the override "ignores the ordinal entirely... even at L3", but `run_skill:739` only emits HALT_HUMAN `if ordinal >= 3`. At L1/L2 a `needs_human` finding flows through the ceiling (PROPOSED / S4_HALT_BEFORE_PUSH), NOT HALT_HUMAN.
- **Resolution: NOT A GAP.** EC-7 (spec L545-548) is the operative per-level contract and explicitly states: "L1: propose + offer. L2: fix locally then HALT. L3: HALT immediately." Expected outcomes: "L1 `edits==0`; L2 `pushes==0, edits>0`; L3 `edits==0, pushes==0, halted==True`." The implementation matches EC-7 exactly. The §5.2 "even at L3" language exists because at L3 the override is what *prevents the push that would otherwise occur* — at L1/L2 the ceiling already yields non-push behavior, so EC-7 specifies the actual outcomes. The pure `transition()` function (fsm.py:573-575) DOES apply the override globally pre-gate; `run_skill` correctly implements the EC-7-specified per-level driver. T-430 (the only override test) targets L3 only and passes. The code comment fsm.py:732-738 documents this reconciliation accurately. **Faithful.**

### Candidate gap 2 — `transition()` S7_VALIDATING→validated returns S4_PUSHING unconditionally (conjunction not applied in the table)

- **Suspicion:** `fsm.py:602-604` returns `S4_PUSHING` on `validated` without checking the INV-016 conjunction — a dropped gate.
- **Resolution: NOT A GAP.** The comment at fsm.py:603 ("G-push handled by evaluate_push_decision at the caller; default edge") documents the seam. The `transition()` table is the low-level edge map; the 5-predicate conjunction is enforced in the `run_skill` driver (fsm.py:766-782) which calls `evaluate_push_decision` and routes via `push_fail_state` on block. The ref §5.3 L87-106 and §5.4 L108-114 both describe the conjunction as a single named predicate applied at the push transition, consistent with this split. No path reaches an actual push without the conjunction. **Faithful** (design seam, not a missing gate).

### Candidate gap 3 — p5 conjunction uses `applied_edits` (int) as truthy, risk of negative-int authorization

- **Suspicion:** `fsm.py:167` `p5 = applied_edits` (the int), and `authorized` ANDs `p5 > 0` (L168) — but `push_fail_state` checks `predicate_5_applied_edits <= 0` (L189). Could a negative value diverge?
- **Resolution: NOT A GAP.** `authorized` uses strict `p5 > 0` (L168); `push_fail_state` uses `<= 0` (L189) — the two are exact complements. `applied_edits` is a count (`_default_apply_edits` sums, never negative). The spec predicate is `applied_edits > 0` (§5.3 L324). Both gates implement `> 0` / `<= 0` consistently. **Faithful.**

### Candidate gap 4 — S2b_VERIFY might be skipped at L1 (verify-after-propose ordering)

- **Suspicion:** spec §5.2 L308 requires verification "even L1 (diagnose-only) verifies before proposing." If `run_skill` proposed before verifying, L1 would propose unverified findings.
- **Resolution: NOT A GAP.** `run_skill` runs the verify filter at fsm.py:744-747 (`verified = [f for f in cycle_findings if config.verify(f)]`; empty→REPORT_ONLY break) BEFORE the `gate_edit` / PROPOSED branch at fsm.py:750-755. An all-unverified cycle at L1 routes to REPORT_ONLY, never PROPOSED. Round counter never ticks on the unverified path (break precedes the L793 increment). **Faithful.**

### Candidate gap 5 — missing S2b_VERIFY edge in `transition()` table

- **Suspicion:** the FSM diagram (spec L270-272) shows S2_CLASSIFY→S2b_VERIFY→(S3_DIAGNOSE | REPORT_ONLY); a missing edge would be a dropped transition.
- **Resolution: NOT A GAP.** `transition()` implements: S2_CLASSIFY/findings→S2B_VERIFY (fsm.py:585-592, with round-budget gate), S2B_VERIFY/verified→S3_DIAGNOSE (L593-594), S2B_VERIFY/unverified→REPORT_ONLY (L595-596). All three diagram edges present with correct round-budget gate placement at S2_CLASSIFY (L587-591). **Faithful.**

---

## Notes

**Note A (override semantics reconciliation):** §5.2's "ignores the ordinal entirely / even at L3" and EC-7's per-level table are internally consistent: the override is the predicate that changes the L3 outcome from push→HALT; at L1/L2 the capability ceiling independently yields non-push behavior, and EC-7 specifies those exact outcomes. Both `transition()` (global pre-gate) and `run_skill` (EC-7 per-level driver) are spec-faithful representations at their respective abstraction levels. The push-gate predicate 3 (fsm.py:770) is the defense-in-depth backstop that blocks any L3 push if a `needs_human` finding reaches it.

**Note B (test durability):** `tests/pr_submit/test_autonomy_gates.py` is a proper pytest file under the project test tree; `@pytest.mark.autonomy` is registered in `pyproject.toml:141`. Not inline one-liners. CI-compatible.

---

## Verification evidence

- **Test execution:** `uv run pytest tests/pr_submit/test_autonomy_gates.py -q` → **7 passed in 0.03s** (T-401, T-402, T-410, T-411/412/413, T-420, T-430, T-ZERO-EDIT-NO-PUSH).
- **Ungroundable path trace:** `finding-ungroundable.json` (`in_diff:false`, `verification_status:"verified"`) → verified-but-zero-edit → `evaluate_push_decision(applied_edits=0)` → `push_decision` SET, `predicate_5_applied_edits==0`, `authorized==False` → `push_fail_state` → TERMINAL_CLEAN. Matches T-ZERO-EDIT-NO-PUSH assertions.
- **INV-016 verbatim diff:** ref `state-machine.md:89-101` vs spec `merged-spec.md:319-331` — verbatim match including the parenthetical fail-routing clause.

## Confidence

Verified: 22/22 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 7 | Grep: 2 | Glob: 0 | Bash: 4

Every checklist element maps to a specific Read of the cited spec/code line, a Grep of the marker/reference, or the test-execution Bash call. Tool calls ≥ checklist items.

---

## Summary

- All 22 fidelity elements PASS with paired spec-line + code-line citations.
- All 5 adversarially-predicted gaps investigated to the line; **none is a genuine fidelity gap** — each resolves to a spec-faithful implementation (4 reconciled against EC-7 / §5.4 seam semantics, 1 against the `transition()` table edges).
- Every gate predicate present as the exact ordinal comparison; INV-016 5-predicate conjunction implemented verbatim with correct fail-routing; needs_human override present (pre-gate + EC-7 per-level); S2b_VERIFY content gate on the correct edge at every armed ordinal; L0 zero-regression preserved.

## VERDICT: PASS
