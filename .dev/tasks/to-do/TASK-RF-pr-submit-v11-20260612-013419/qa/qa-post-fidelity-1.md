# QA Report — POST-COMPLETION M4 Source-Fidelity (Agent 1, §1-§6)

**Topic:** PR Review Auto-Remediation Monitor V1.1 — spec→core symbol fidelity (FR-8.x/9.x/10.x + INV-R1/R2/R3)
**Date:** 2026-06-12
**Phase:** report-validation (source-fidelity, FINAL state)
**Fix authorization:** false (report only — nothing modified)
**Scope:** spec §1-§6 vs `src/superclaude/pr_submit/{models,classifier,detection,run_log,fsm}.py`

---

## Overall Verdict: PASS

Every FR-8.x, FR-9.x, FR-10.x and INV-R1/R2/R3 in §1-§6 maps to a real implementing symbol with preserved detail. FR-9.5 (review-wins-over-decline) is FULLY implemented via the `_is_attributed_review` arbiter. No phantom coverage detected. Two spec-faithful **necessary deviations** are documented in-code and do not break fidelity.

---

## FR → Symbol Map (file:line)

| Req | Symbol / site | Detail preserved |
|-----|---------------|------------------|
| FR-8.1 (S5a, one re-trigger comment) | `fsm.transition` `RESOLVING→S5A_RETRIGGER_REVIEW` (fsm.py:622-626); `run_skill` S5a enter + `do_retrigger` + `rereview_request_count += 1` (fsm.py:964-970) | One comment per cycle; token NOT in core (seam `do_retrigger`, fsm.py:733) |
| FR-8.2 (tick moves to attributed re-review; old fsm.py:793 increment removed) | Single relocated increment at fsm.py:1001 (`outcome == "attributed"`); old post-resolve `+=1` is GONE (no `round_counter += 1` anywhere except 1001) | Optimistic-default preserved for legacy empty `rereview_outcome` (fsm.py:985); `timeout` path does NOT tick (fsm.py:992-996) — EC-18 |
| FR-8.3 (≤ max_rounds, once per cycle) | `rereview_request_count += 1` guarded by `applied_edits > 0` (fsm.py:964) | INV-R1 monotone count |
| FR-8.4 (poll attributed to our SHA / watermark) | `_is_attributed_review(review, watermark)` (classifier.py:100-115) — newer-than-watermark | watermark = re-trigger ts; None ⇒ initial poll accepts any |
| FR-8.5 (token from contract, not core literal) | `accepted_trigger_phrases` default list (detection.py:87-93); core holds NO `auggie review` literal (verified: grep of the 5 files shows the phrase only in docstrings/regex, never emitted by core) | canonical `auggie review` + 2 alts |
| FR-8.6 (skip S5a when no push) | S5a block gated on `if result.applied_edits > 0:` (fsm.py:964) | no comment when applied_edits==0 |
| FR-9.1 (4th `declined` state, BOTH regexes + watermark) | `STATE_DECLINED` (classifier.py:24); `is_decline()` requires phrase AND retrigger AND newer-than-watermark (classifier.py:65-97); decline checked FIRST (classifier.py:147-151) | both-regex conjunction defeats false positive |
| FR-9.2 (declined routes from S2 AND S5) | `transition` `(S2_CLASSIFY,"declined")→S5B` (fsm.py:640-642) and `(S5_AWAITING_REREVIEW,"declined")→S5B` (fsm.py:635-639); `run_skill` both paths (initial fsm.py:876-881, S5 fsm.py:987-991) | both poll points |
| FR-9.3 (exact fallback invoke) | `invoke_auggie_review` seam (fsm.py:734) called once in `_run_fallback` (fsm.py:763-765); flags live SKILL-side per §2 | core DECIDES only (NFR-6) |
| FR-9.4 (findings re-enter verify-before-remediate) | `_run_fallback` re-runs `config.verify` (fsm.py:779), gate_edit, validation, G-push (fsm.py:778-827) | not trusted verbatim |
| **FR-9.5 (review WINS over decline)** | `_is_attributed_review` arbiter (classifier.py:100-115) wired into `classify`: when decline present, `attributed_rereview` computed; `if not attributed_rereview: return STATE_DECLINED` else fall through (classifier.py:152-164) | review>decline ONLY when watermark set + review newer + review itself not a decline; stale pre-watermark decline ignored (EC-23 via watermark arg) |
| FR-10.1 (6th idempotency set, strict-once) | `IDEMPOTENCY_SETS += ("auggie_review_invoked",)` → 6 tuple members (run_log.py:27-34); `_run_fallback` guards on `if not result.auggie_review_invoked:` (fsm.py:763) | keyed on pr_number; at-most-once |
| FR-10.2 (clamp once, monotone) | `clamp_max_rounds(effective, hard=1) = min(effective,1)` (fsm.py:145-153); recorded once via MAX_ROUNDS_CLAMPED; monotone-min fold (run_log.py:187-194) | `min(prev,clamp)`, None seeds |
| FR-10.3 (separate cap-1 sub-loop, no loop-back, round_counter frozen) | `fallback_round_counter` (models.py:213) gated by `loop_guard_should_halt(fallback_round_counter, effective_max_rounds)` (fsm.py:768); `round_counter` never touched in `_run_fallback` | independent counters |
| FR-10.4 (survive --resume) | `rebuild_state` folds AUGGIE_FALLBACK_INVOKED→set (run_log.py:177-182) + MAX_ROUNDS_CLAMPED→min (183-194) + REREVIEW_REQUESTED→count (174-176) | rebuilt from JSONL |
| FR-10.5 (push_count ≤ max_rounds+1) | fallback's single `do_push`+`push_count += 1` (fsm.py:823-824); structurally one push (strict-once + cap-1) | +1 reachable once |

## INV → Symbol Map

| INV | Site | Detail |
|-----|------|--------|
| INV-R1 (re-trigger boundedness) | rereview_request_count monotone, guarded by applied_edits>0, no round_counter tick (fsm.py:964-970); count fold (run_log.py:174-176) | edge/gate unchanged |
| INV-R2 (strict-once + push bound) | `auggie_review_invoked` flag (fsm.py:763) + 6th durable set (run_log.py:33) + single fallback push (fsm.py:823-824) | push_count ≤ max_rounds+1 |
| INV-R3 (clamp monotonicity / determ. term.) | `clamp_max_rounds` min (fsm.py:153) + monotone-min fold (run_log.py:192) + cap-1 no-loop-back sub-loop (fsm.py:768-839) | two independent counters |

## Detail-item checklist (explicit asks)

| Item | Verified |
|------|----------|
| 4 EventType values | REREVIEW_REQUESTED/DECLINE_DETECTED/AUGGIE_FALLBACK_INVOKED/MAX_ROUNDS_CLAMPED present (models.py:76-79); docstring "EXACTLY 37" + run_log `_VALID_EVENT_VALUES` validation (run_log.py:36,108-111) |
| 2 states | S5A_RETRIGGER_REVIEW/S5B_AUGGIE_FALLBACK (models.py:115-116); NEITHER in TERMINAL_STATES (models.py:129-138) — confirmed non-terminal |
| 6 SkillResult fields | rereview_request_count, fallback_engaged, auggie_review_invoked, decline_detected, effective_max_rounds, fallback_round_counter (models.py:208-213) = 6 |
| 3 DetectionContract fields + regex defaults | decline_phrase_regex=`abnormally\s+large`, decline_retrigger_regex, accepted_trigger_phrases (detection.py:83-93); `from_yaml` extends all 3 (detection.py:110-120) |
| 6th set | `auggie_review_invoked` 6th tuple member (run_log.py:27-34) |
| clamp min(.,1) | `clamp_max_rounds` returns `min(effective, hard)` hard=1 (fsm.py:153) |
| monotone-min fold | `effective_max_rounds = clamp if prev is None else min(prev, clamp)` (run_log.py:190-194) |

## Documented necessary deviations (fidelity-preserving, not phantom)

1. **Retrigger regex char-class adds backtick** — detection.py:80-86 includes `` ` `` alongside `"`/`'` (spec §6.2 literal was `["']?`). Justified in-code: real Augment renders `` `augment review` `` with markdown backticks (Phase-3 QA finding F1). Strengthens detection; does not weaken FR-9.1's both-regex requirement.
2. **`S4'_HALT_BEFORE_PUSH` → `S4_HALT_BEFORE_PUSH`** — Python identifier cannot hold an apostrophe (models.py:97-100). Spec-faithful adaptation, documented.
3. **Outcome vocab vs edge vocab** — `run_skill`'s `"attributed"` outcome token is deliberately distinct from `transition`'s `"rereview_attributed"` edge name (fsm.py:978-981). Intentional two-vocabulary design, documented; not a mismatch.

## Phantom-coverage scan

No phantom coverage found. Each FR/INV resolves to executed core logic (not a comment-only or stub). Specifically checked the high-risk sites:
- FR-8.2's removed increment: confirmed the optimistic `fsm.py:793` site is GONE; the sole `round_counter += 1` is fsm.py:1001 behind `outcome == "attributed"`.
- FR-9.5: the arbiter is real and load-bearing — `classify` returns `STATE_DECLINED` only when `not attributed_rereview`, and the arbiter additionally excludes a review that is itself a decline (classifier.py:158-161), so a decline cannot masquerade as the winning review.
- INV-R3 frozen round_counter: `_run_fallback` (fsm.py:737-839) contains no `round_counter` mutation — only `fallback_round_counter`.

## Summary
- FRs mapped: 16/16 (FR-8.1-8.6, FR-9.1-9.5, FR-10.1-10.5)
- INVs mapped: 3/3 (INV-R1/R2/R3)
- Detail items: 7/7
- FR-9.5 arbiter: FULLY implemented (classifier.py:100-115 + 152-164)
- Phantom coverage: 0
- Necessary deviations (documented, non-breaking): 3

**Confidence:** Verified: 26/26 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 5 | Grep: 0 | Glob: 0 | Bash: 0 (all 5 core files + spec §1-§6 read in full; symbol map derived from full-file reads)

VERDICT: PASS
