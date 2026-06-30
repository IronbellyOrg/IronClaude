---
artifact: adversarial-round-2-rebuttal
role: advocate
variant: variant-3-haiku-qa
persona_lens: qa
round: 2
topic: "PR Review Auto-Remediation Monitor (V1.0)"
created: 2026-06-11
---

# Round 2 — QA Rebuttal (Variant C, speaks third)

## Unresolved IDs

**X-005 fence-post reconciliation (critical):** My T-620..T-629 matrix IS fence-post-correct under `counter >= max_rounds`. Trace for max_rounds=2: counter=0, gate false, push#1, increment→1; gate false, push#2, increment→2; 2>=2 true, HALT. Exactly 2 pushes, matching B's trace. T-626's `counter==2 NOT 3` proves `>=` (not `>`) is required. T-628 (max_rounds=0): 0>=0 true, immediate HALT, 0 pushes. All 10 rows' push_count equals max_rounds. The dual scheme (counter=count, sequence=index list, display=counter+1) resolves the "round 0" ambiguity without changing assertions. Winner: C (dual scheme).

**X-001:** ACCEPT warn compromise. EC-8/T-E08 already assert zero pushes. Add: assert arm-time WARN in JSONL when `--monitor >= 2 && max_rounds == 0`. Winner: C+A.

**X-003:** ACCEPT two-key model. EC-4 update: key fix-dedup on stable finding hash, reply-dedup on comment_id/thread_id. Fixture produces two comments with identical finding body under different comment_ids; assert exactly one fix, one reply. Winner: A-principle + B-substrate.

**X-008:** ACCEPT drop-from-fix + mandatory report retention. Add `finding_dropped: ungroundable` event assertion. Winner: C-scoped + B-retention.

**C-002:** ACCEPT role split. I own proof matrix; A owns SHA predicate; B owns storage.

## Positions changed
- X-005: from mixed representation to explicit count+display separation.
- X-003: from "C simplicity" to two-key model.
- X-008: from pure drop to two-channel drop-from-fix + retain-in-report.

## Verification fixtures for REJECT shared assumptions

**A-003 (session eviction):** `test_kill_session_mid_cycle_resume_idempotency` — kill session after JSONL push journal but before reply; `--resume` must reconstruct idempotency sets; assert reply posted exactly once, total push count == 2, no missing idempotency_skip. Proves resume is survivable, not documented.

**A-007 (validation passes, behavior drifts):** `test_validated_not_verified_behavioral_drift` — fix passes targeted tests + lint but changes a non-targeted assertion; push proceeds with run-log `validation_status: "validated_not_verified"`; after max_rounds=2, HALTs regardless of reviews. Proves validation != behavioral safety; max_rounds caps blast radius.
