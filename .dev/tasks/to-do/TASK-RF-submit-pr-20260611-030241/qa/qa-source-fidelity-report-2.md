# QA Report — M4 SOURCE-FIDELITY agent 2 (loop-guard + run-log + recovery)

**Phase:** report-validation / source-fidelity (Phase Gate B)
**Date:** 2026-06-11
**Fix authorization:** false (report only)
**Adversarial hypothesis tested:** ≥5 spec-to-code fidelity gaps (off-by-one, 32-vs-33 event drift, missing idempotency set, wrong recovery branch)
**Result of hypothesis:** DISCONFIRMED on all four named defect classes. 0 behavioral fidelity defects; 3 advisory gaps (test-coverage + doc-drift), none falsifying the implementation.

**Spec range:** merged-spec.md FR-6.3/INV-001 (L236) + §9 (L592-659) + §11 (L697-744) + §12 (L748-776)

---

## Overall Verdict: PASS

---

## Element-by-element fidelity matrix (spec line ↔ code line, binary)

### A. INV-001 loop-guard (FR-6.3 L236 / §9.1 L600-622)

| Element | Spec | Code | Result |
|---|---|---|---|
| Single increment edge `S5_AWAITING_REREVIEW→S2_CLASSIFY` on `review_observed ∧ sha_attributed_to_our_push` | L236, L602-603 | loop_guard.py:58-61 (`on_rereview` guards both conds); fsm.py:613 step-edge `rereview_attributed`; fsm.py:792-793 driver | PASS |
| Increments NOWHERE else | L236 "nowhere else" | fsm.py: only ONE `round_counter +=` mutation (audited L720/771/793 — 720 & 771 are reads, 793 is the sole write) | PASS |
| Monotonic — no decrement on vanish | L236, INV-4 L616-617 | loop_guard.py:63-69 `vanished_rereview` = intentional no-op | PASS |
| Gate `>=` NOT `>` | INV-5 L618-619 | loop_guard.py:30 `round_counter >= max_rounds`; fsm.py:135-141 delegates to same fn | PASS |
| User label = counter+1 | L236, L605 | loop_guard.py:33-35 `user_label` = `+1` | PASS |
| `max_rounds=N` → exactly N pushes | L236, L606 | T-626 trace (cycles 0,1 push; cycle 2 gate `2>=2` halts) → 2 pushes; verified by run + test_loop_guard.py:80-84 matrix incl. `(5,9,5,5)` | PASS |
| Default 2, hard cap 5 | L236 | loop_guard.py:19-20; CLI clamp fsm.py:101 `if ns.max_rounds > 5` (T-102) | PASS |
| Canonical off-by-one (T-626): counter==2 NOT 3 at max=2 | §9.3 L641-655 | Traced through fsm.py:718-800; test_loop_guard.py:45-64 asserts `round_counter==2, push_count==2, HALT_MAX_ROUNDS` | PASS |

### B. 33 EventType (§11.3 L724-731 + §12.1 L771)

| Element | Spec | Code | Result |
|---|---|---|---|
| §11.3 list count | L724-731 = **32** event types (the 33rd line in the fence block is the ```` ``` ```` close, not an event) | — | confirmed 32 |
| 33rd event `push_aborted_or_not_landed` | §12.1 L771 | models.py:70 | PASS |
| Total EventType members | 32 + 1 = 33 | models.py:29-70 → counted 33 | PASS |
| Exact set equality (no drift) | — | `comm -23/-13` diff code↔spec: **0 in code-not-spec, 0 in spec-not-code** | PASS — no 32-vs-33 drift |
| Run-log validates against closed set | §11.3 | run_log.py:35,107-110 raises on unknown event_type | PASS |
| Ref doc inline list | loop-guard.md:51-58 | counted 33, 0 diff vs code enum | PASS |

### C. 5 idempotency sets (§11.4 L735-744)

| Set | Spec | Code | Result |
|---|---|---|---|
| `processed_review_ids` | L739 | run_log.py:28 | PASS |
| `processed_finding_ids` keyed on `fix_key=sha256(path+line+finding_body)` | L740-741 | run_log.py:29 + fix_key fn L53-55 (`sha256(path\nline\nbody)`); Finding.fix_key models.py:152-162 identical; cross-checked equal by test_idempotency.py:64-68 | PASS |
| `replied_comment_ids` | L742 | run_log.py:30 | PASS |
| `resolved_thread_ids` | L743 | run_log.py:31 | PASS |
| `pushed_commit_shas` (the INV-001 attribution set) | L744 | run_log.py:32; populated from `push_completed.target_sha` (rebuild L171-172) | PASS |
| Count | exactly 5 | IDEMPOTENCY_SETS tuple has 5 members | PASS — no missing set |

### D. INV-007 push triad + crash-window 3-way (§12.1 L754-776)

| Element | Spec | Code | Result |
|---|---|---|---|
| Triad ORDER `push_decision→push_initiated→push_completed` | L756-760 | fsm.py:240-260 `build_push_triad` returns list in that exact order | PASS |
| `push_initiated` fsynced BEFORE `git push` | L759 | run_log.py:124-130 `write_ahead` = append+fsync; doc L223-225 | PASS |
| PRE-push idempotency key `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>` | L762-763 | fsm.py:199-207 `push_idempotency_key` — exact format, PRE-push SHA | PASS |
| Branch A landed → `push_completed{recovered}`, resume S5 | L768-770 | recovery.py:102-111 → `(BRANCH_A_LANDED, S5_AWAITING_REREVIEW)` | PASS |
| Branch B not-landed → `push_aborted_or_not_landed{recovered}`, re-drive SAME cycle WITHOUT recomputing fix | L770-772 | recovery.py:113-123 → emits the event, returns `S4_PUSHING` (pre-push path), docstring "without recomputing the fix" | PASS |
| Branch C ambiguous → HALT_HUMAN with original fields + observed SHA | L773 | recovery.py:125-135 → `terminal_halted` + observed_remote_sha + common fields → HALT_HUMAN | PASS |
| Crash window = dangling `push_initiated` no matching `push_completed` | L765-767 | recovery.py:47-70 `detect_crash_window` matches on idempotency_key | PASS |
| MUST NOT double-push | L766 | test_crash_recovery.py:254-257 asserts `initiated_after == initiated_before` | PASS |

---

## Summary
- Fidelity elements checked: 31 / 31
- Behavioral spec-to-code defects (CRITICAL): **0**
- Advisory gaps: 3 (1 IMPORTANT test-coverage, 2 MINOR)
- Tests: 31/31 pass (`uv run pytest tests/pr_submit/{test_loop_guard,test_run_log,test_crash_recovery,test_idempotency}.py`)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | IMPORTANT | tests/pr_submit/test_crash_recovery.py | INV-007 3-way crash-window: **only Branch A** (`remote_reachable=True`) is integration-tested (L240). **Branch B** (`remote_reachable=False` → not-landed re-drive, S4_PUSHING) and **Branch C** (`remote_reachable=None` → ambiguous → HALT_HUMAN) have NO dedicated test anywhere (grep across tests/pr_submit confirms 0 hits for `BRANCH_B`/`BRANCH_C`/`remote_reachable=False`/`=None`). recovery.py:113-135 implements both correctly but they are unverified. The prompt's "wrong recovery branch" hypothesis is the exact surface this leaves unguarded. | Add `resolve_crash_window(..., remote_reachable=False)` asserting `BRANCH_B_NOT_LANDED` + `S4_PUSHING` + a `push_aborted_or_not_landed` event with `recovered=True` and NO fix recompute; and `remote_reachable=None` asserting `BRANCH_C_AMBIGUOUS` + `HALT_HUMAN` + `terminal_halted{observed_remote_sha}`. |
| 2 | MINOR | tests/pr_submit/test_loop_guard.py:71-78 | Parametrize comment-to-spec-ID labels are misattributed: row `(1,3,1,1)` is commented "T-620" but spec T-620 is `max_rounds=2,rounds=1`; the spec ID for `--max-rounds 1` is T-627 (§9.2 L635). Docstring claims "T-620..T-629" but the matrix covers 6 of those 10 IDs and the per-row labels don't line up. Assertions are correct — only the ID comments drift from §9.2. | Re-map the inline comments to the matching §9.2 test IDs (or drop the per-row ID comments). |
| 3 | MINOR | run_log.py:179-183 | `processed_review_ids` is populated from `FINDINGS_NORMALIZED.review_id`, whereas spec §11.4 L739 frames it as "prevents re-processing the same Augment **review emission**" (more naturally keyed at `review_detected`). Behaviorally adequate (a review that normalizes findings is recorded), and FM-8 test passes, but the keying event differs from the spec's emission-level intent. Not a defect — flag for reviewer awareness. | Confirm with spec owner whether review-emission dedup should key on `review_detected` vs `findings_normalized`; no change if findings-level dedup is intended. |

## Adversarial probe outcomes (the 5 the prompt asked me to hunt)
1. **Off-by-one** — DISCONFIRMED. `>=` gate (loop_guard.py:30); T-626 traces to counter==2/2 pushes; tested.
2. **32-vs-33 event drift** — DISCONFIRMED. Exact set equality, 0 symmetric-difference; §11.3=32 + §12.1=1 = 33 = enum count.
3. **Missing idempotency set** — DISCONFIRMED. All 5 present (run_log.py:27-33), fix_key correct and cross-validated.
4. **Wrong recovery branch** — DISCONFIRMED on implementation (recovery.py:102-135 all 3 branches correct); but Branch B/C are **untested** (Issue #1).
5. **Increment-elsewhere leak** — DISCONFIRMED. fsm.py has exactly ONE `round_counter +=` write site (L793); INV-001 "nowhere else" holds.

## Confidence
Verified: 31/31 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

(Note on the attribution seam: `run_skill` (fsm.py:793) increments inline and pre-assumes `rereview_findings` are SHA-attributed, bypassing the `RoundCounter.on_rereview` `sha_attributed_to_our_push` guard; the guard IS present at the unit level (loop_guard.py:58, tested test_loop_guard.py:107-109) and the `step_transition` edge (fsm.py:613) is correctly named `rereview_attributed`. No `run_skill`-level negative test exists for a non-attributed re-review, but every spec-required assertion is independently verified, so this is folded into Issue #1's coverage advisory rather than an Unchecked item.)

## Tool engagement
Read: 8 | Grep: 6 | Glob: 0 | Bash: 9 (incl. 1 `uv run pytest`)

## QA Complete

## VERDICT: PASS
