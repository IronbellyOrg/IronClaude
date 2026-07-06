# Pre-Execution Best-Practice Audit: TASK-RF-submit-pr-20260611-030241

**Auditor lens:** BEST-PRACTICE COMPLIANCE + RISK SURFACE (UC-1 pre-execution)
**Spec:** `merged-spec.md` at `/config/workspace/IronClaude/.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec.md`
**Tasklist:** `TASK-RF-submit-pr-20260611-030241.md` at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-submit-pr-20260611-030241/TASK-RF-submit-pr-20260611-030241.md`

---

## 1. R1 / DET Gate

**Verdict: COMPLIANT**

**Evidence:**
- Step 2.0 (line 196-197) encodes the R1 probe as a `needs_human_decision` HALT operator item. It explicitly writes PENDING, produces an operator runbook with single-line `--repo IronbellyOrg/IronClaude`-pinned commands, and states "NEVER auto-locks the contract, NEVER hard-guesses `augment_bot_login`".
- Key Constraint (line 136): "R1 DET probe is a `needs_human_decision` HALT (build step-0) ... write PENDING and HALT the lock path, never auto-lock."
- Key Constraint (line 75, Objective 1): "NEVER auto-locks or hard-guessed the bot login."
- `detection.py` item (Step 2.3, line 206) encodes the `locked:false` HALT path at the code level: "raises/HALTs when `locked` is false or absent (the T-210 contract)".
- T-210 test (Step 2.4, line 209) explicitly asserts the skill HALTs when the contract is `locked:false`/absent.

The DET gate is a real build-blocking gate. `locked:false` ships; HALT for human; never auto-guess.

---

## 2. R2 / Loop-Guard (INV-001 single-increment-edge + T-626-OFF-BY-ONE `>=` gate)

**Verdict: COMPLIANT**

**Evidence:**
- Step 8.1 (line 333): `loop-guard.md` ref encodes INV-001 verbatim including "the gate uses `>=` (INV-5) not `>`" and "increment edge is stated as the ONLY increment site".
- Step 8.2 (line 335-336): `loop_guard.py` is a dedicated P0 item. Explicitly encodes: "increments by EXACTLY 1 ONLY on the `S5_AWAITING_REREVIEW -> S2_CLASSIFY` transition", "increments nowhere else", "never decrements (monotonic)", "`should_halt(round_counter, max_rounds)` gate using `round_counter >= max_rounds` (INV-5, `>=` not `>`)". Item calls it "the P0 module -- the off-by-one is the spec's named P0 defect."
- Step 8.5 (line 344-345): `test_loop_guard.py` with T-626-OFF-BY-ONE as canonical, marked `@pytest.mark.p0`, asserts `round_counter==2` exactly at `max_rounds=2`, exactly 2 pushes.
- Key Constraints (line 69): "loop-guard off-by-one is a P0 defect".

The off-by-one surface has a dedicated P0 module, a dedicated P0 test, explicit `>=` encoding, and the single-increment-edge is stated as the ONLY increment site.

---

## 3. R4 / Auto-Push (INV-016 5-predicate G-push conjunction, FR-3.5 verify-before-remediate, VG-1..VG-6 with lint!=format)

**Verdict: COMPLIANT**

**Evidence:**
- **INV-016 conjunction:** Step 4.2 (line 248) encodes all 5 predicates explicitly in `fsm.py`: "`monitor_ordinal>=3` AND `validation_status=="validated"` AND `needs_human_decision==false for all` AND `round_counter<max_rounds` AND `applied_edits>0`" with fail-routing per predicate. Step 7.4 (line 323) extends this to L3 push states.
- **applied_edits > 0 (predicate 5):** Step 4.7 (line 263) T-ZERO-EDIT-NO-PUSH asserts `push_count==0`, `authorized==False`, `predicate_5_applied_edits==0`. Step 8.10 fixture `finding-ungroundable.json` (line 392) represents the `applied_edits==0` path.
- **FR-3.5 verify-before-remediate:** Step 5.2 (line 272-273) `finding-verify.md` with reuse of evidence-validator agent. Step 5.5 (line 281-282) `test_finding_verify.py` with T-341 asserting `round_counter` unchanged and troubleshoot NOT called for unverified.
- **VG-1..VG-6 ordered:** Step 6.2 (line 294-295) `fsm.py` S7_VALIDATING driver "runs VG-1..VG-6 IN ORDER".
- **VG-3 != VG-4 (lint != format split):** Key Constraint (line 137) explicit callout. Step 6.2 "CRITICALLY keeps VG-3 and VG-4 as TWO DISTINCT gate checks". Step 6.4 (line 300-301) T-510 and T-511 are SEPARATE tests. Phase 11 Steps 11.4 and 11.5 are separate items (lines 410-414).
- **Validation-before-push (FR-3.5, spec):** Step 6.2 "sets `validation_status="validated"` only on all-green (the single definition consumed by the INV-016 predicate (2))".

---

## 4. NFR-6 Core Purity

**Verdict: COMPLIANT**

**Evidence:**
- Key Constraint (line 128): "ZERO `gh`/`git` token in `state-machine.md`, `severity-routing.md`, `loop-guard.md` and in the `fsm.py`/`severity_router.py`/`loop_guard.py` Python."
- Step 4.1 (line 245): `state-machine.md` is "CORE-PURE (ZERO `gh`/`git` tokens -- T-N50 static-asserts this)".
- Step 4.2 (line 248): `fsm.py` "contains ZERO `gh`/`git`/`anthropic` tokens (NFR-6/FR-G1)".
- Step 8.1 (line 333): `loop-guard.md` "CORE-PURE (ZERO `gh`/`git` tokens, T-N50)".
- Step 8.2 (line 336): `loop_guard.py` "CORE-PURE (ZERO `gh`/`git`/`anthropic` tokens, T-N50)".
- Step 5.1 (line 270): `severity_router.py` "CORE-PURE (ZERO `gh`/`git` tokens, T-N50)".
- Step 9.5 (line 378-379): `test_static_grep.py` T-N50 "asserts `state-machine.md`, `severity-routing.md`, `loop-guard.md` AND `src/superclaude/submit_pr/{fsm,severity_router,loop_guard}.py` contain ZERO `gh`/`git` tokens".
- Phase Gate A (Step PGA.2, line 228) and Phase Gate B (Step PGB.2, line 429) both have explicit core-purity grep lenses.

The spec's own `gh`/`git` I/O isolation is preserved: poller/dispatcher/helper scripts + SKILL.md VAL validator are the ONLY `gh`/`git` touchers.

---

## 5. Build-Order DAG (DET-first dependency, L5 mechanical gate)

**Verdict: COMPLIANT**

**Evidence:**
- Line 86: "INTERNALLY, the build DAG (spec section 3) is enforced via L5 contract-verdict gates: Phase 2 (detection-contract gate) must produce a PASS verdict before Phase 4+ arming work is authorized."
- Line 174: "BUILD-ORDER DAG (spec section 3) IS MECHANICALLY ENFORCED."
- Step 2.6 (line 214-215): L5 contract-verdict gate -- creates `contract-verdict.md` with VERDICT: PASS or VERDICT: FAIL + "downstream phases BLOCKED".
- Phase 4 header (line 242): "DO NOT begin this phase until `phase-outputs/plans/contract-verdict.md` records 'GATE A: PASS -- Phase 4+ authorized'."
- Phase Gate A (line 217-238): Full 5-lens QA with serialized fix authorization, 3-cycle max, explicit "GATE A: PASS -- Phase 4+ authorized" append.
- Phase Gate B (line 419-451): "DO NOT begin until `phase-outputs/plans/validation-verdict.md` records VERDICT: PASS." 6-lens M3 + 3-lens M4 fidelity, serialized fix, verification rounds.

The DET-first dependency is mechanically enforced via L5 verdict files, not just prose ordering.

---

## 6. Project Conventions

**Verdict: COMPLIANT**

**Evidence:**
- **SoT discipline:** Key Constraint (line 129): "edit `src/superclaude/` -> `make sync-dev` -> `.claude/`; NEVER `git add .claude/*` except `.claude/settings.json`". Step 11.1 (line 402) "NEVER `git add` any `.claude/` path".
- **gh --repo pin:** Key Constraint (line 130): "gh `--repo IronbellyOrg/IronClaude` pin on every `gh`/`gh api` call". Step 7.1 (line 314) "EVERY `gh`/`gh api` call pins `--repo IronbellyOrg/IronClaude`". Step 9.5 T-104 static grep for `gh ` without `--repo`.
- **UV-only:** Step 11.3 uses `uv run pytest`; Step 6.2 uses `uv run ruff format --check`; no `pip install` or `python -m` anywhere.
- **Single-line paste commands:** Step 2.0 explicitly requires "single-line, absolute-path, `--repo IronbellyOrg/IronClaude`-pinned commands" in the runbook.

---

## 7. Execution Safety

**Verdict: COMPLIANT (with one minor gap)**

**Evidence:**
- **Serialized QA fix authorization:** Phase Gate A Steps PGA.3-PGA.5 (lines 231-238): consolidated findings -> single fixer with `fix_authorization: true` -> 2-agent verification round, max 3 fix cycles. Phase Gate B Steps PGB.4-PGB.6 (lines 436-443): same serialized pattern. PGB.7-PGB.8 (lines 445-451): M4 fidelity with same serialization.
- **POST-reflect gate:** Post-completion item (line 463): `/sc:reflect --mode post --remediate --diff <BASE> --tasklist ... --spec ... --depth deep`, with `git add -A` before the gate. Self-run, not human HALT.
- **Mid-execution scope/cost pauses:** The tasklist uses explicit L5 verdict gates (Steps 2.6, 11.6) and Phase Gates A/B with binary PASS/FAIL and HALT-on-failure escalation. No ad-hoc "ask user if we should continue" mid-phase pauses.

**Minor gap:** The tasklist does not explicitly encode a "cost ceiling" or "token budget pause" if a phase runs abnormally long (e.g., 10+ fix cycles across phases). The 3-cycle max per gate is good, but there is no explicit cross-phase escalation if total fix cycles exceed a threshold. This is a WEAK, not MISSING, concern -- the existing gates are sufficient for most scenarios.

---

## TOP 3 RISKS (if executed as-written)

### Risk 1: QA overhead mass could cause context exhaustion before build completion

The tasklist encodes an enormous QA surface: Phase Gate A (5 lens agents + consolidation + fixer + 2 verification = ~9 agent spawns), Phase Gate B M3 (6 lens agents + consolidation + fixer + 2 verification = ~10 spawns), Phase Gate B M4 (3 fidelity agents + consolidation + fixer + 2 verification = ~7 spawns). That is approximately 26+ agent spawns for QA alone, on top of the 11 build phases. For a ~115-test, 30+ file build, this is defensible at Deep tier, but the cumulative context load across session rollovers risks the executor losing thread on earlier phase outputs. The intra-task handoff files mitigate this, but are only as good as the fidelity with which later phases re-read them.

**Severity:** P2 (mitigated by handoff files + explicit re-read instructions in each item)

### Risk 2: Provisional inline payloads in Phase 2 test vs. Phase 10 fixture swap

Step 2.4 (line 209) notes that `test_detection_contract.py` must include "inline minimal payload dicts so the module collects" before Phase 10 lands the real fixtures, then adds "when Phase 10 lands, SWAP the inline dicts for `load_fixture(...)` references rather than keeping both (no duplicate payloads)". This is a deferred correctness debt item embedded in the tasklist. An executor rolling over between Phase 2 and Phase 10 could forget the swap, leaving duplicate payloads. No explicit reminder item or automated verification catches this.

**Severity:** P3 (would cause test maintenance confusion, not a functional defect -- the inline payloads would be superseded, not conflicting)

### Risk 3: No explicit `recovery.py` core-purity enforcement beyond prose

Step 8.4 (line 341-342) creates `recovery.py` and notes "consuming the remote-reachability result as an input" and "keep it core-pure of `gh`/`git`". However, unlike `fsm.py`/`severity_router.py`/`loop_guard.py`, `recovery.py` is NOT listed in the T-N50 static-grep target set (Step 9.5, line 378-379 greps only `fsm,severity_router,loop_guard`). The spec's NFR-6 lists "FSM, router, loop-guard" as the purity set; `recovery.py` and `run_log.py` are not explicitly in that set. This is spec-faithful but leaves a seam where `recovery.py` could acquire a `gh` call (for the remote-reachability query) without T-N50 catching it. The spec intentionally delegates the actual remote query to the SKILL/script, so the risk is bounded -- but the static test does not cover it.

**Severity:** P3 (bounded by spec delegation; a real risk only if an implementor shortcuts the delegation)

---

## Additional Observations

- **Phase 3 is absent.** The tasklist jumps from Phase 2 (Detection Contract Gate) to Phase 4 (FSM Core + Skill Skeleton). This is intentional -- the spec's DAG has no step between DET and FSM skeleton, and Phase Gate A serves as the QA bridge. Not a defect, but worth noting for readers expecting sequential numbering.
- **The `find_symbol` / Serena integration is absent from the reuse surfaces.** The tasklist reuses `severity-rubric.md`, `evidence-validator` agent, and `sc-troubleshoot` dispatch surface, which is correct. The reuse citations are explicit and defensible.
- **Monitor-tool arming reality is correctly framed.** Key Constraint (line 167-168) and Step 4.4 (line 254) both maintain the honest "session close = monitor lost" framing. The SKILL never implies a background daemon.
- **The 5 spec corrections are all encoded in Key Constraints (lines 131-138):** Python core location, `--cov` target, 4-not-5 markers, 33 events, no `--depth quick --fix`. Phase Gate B Step PGB.2 (line 434) explicitly checks these in the actionability lens.

---

## Summary

| Criterion | Verdict | Evidence |
|-----------|---------|----------|
| R1/DET gate | COMPLIANT | Step 2.0 `needs_human_decision` HALT + Key Constraint line 136 + T-210 |
| R2/loop-guard | COMPLIANT | Step 8.2 P0 module + Step 8.5 T-626-OFF-BY-ONE p0 test + `>=` explicit |
| R4/auto-push | COMPLIANT | Step 4.2 5-predicate conjunction + Step 5.2 verify-before-remediate + Step 6.2 VG-1..VG-6 + Step 6.4 T-511 |
| NFR-6 core purity | COMPLIANT | CORE-PURE on all 6 files + T-N50 static test + Phase Gates A/B purity lenses |
| Build-order DAG | COMPLIANT | L5 verdict gates (Steps 2.6, 11.6) + Phase Gate A/B "DO NOT begin" guards |
| Project conventions | COMPLIANT | SoT, gh --repo pin, UV-only, single-line commands all encoded |
| Execution safety | COMPLIANT (minor gap) | Serialized fix auth, POST-reflect gate, no mid-exec cost pauses; missing cross-phase cost ceiling |

**BEST_PRACTICE_GRADE: 4/5**

**TOP_RISKS:**
1. QA overhead mass (~26+ agent spawns) risks context exhaustion across session rollovers
2. Phase 2 inline payload -> Phase 10 fixture swap is deferred debt with no automated catch
3. `recovery.py` not covered by T-N50 static core-purity grep (bounded by spec delegation)

**BLOCKING CONCERNS:** None. The tasklist is well-structured for safe execution of this spec. The DET gate is a genuine HALT, the loop-guard has a dedicated P0 module and test, the 5-predicate G-push conjunction is fully encoded, and the build-order DAG is mechanically enforced via L5 verdict files. Proceed to execution.
