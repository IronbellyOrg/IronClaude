# QA Report — Closed-Enum Count Domain Lens (33→37, 5→6)

**Topic:** pr_submit V1.1 Phase 4 — closed-enum count integrity
**Date:** 2026-06-12
**Phase:** task-integrity (count-integrity domain lens)
**Fix authorization:** false (report only — modified nothing)
**Stance:** Adversarial — assumed ≥1 count-integrity error existed; verified by READING + counting + runtime import.

---

## Overall Verdict: PASS

Every count site is exact. Both run_log.py "33"→"37" prose sites are updated (zero
remaining EventType-count "33" in run_log.py). The IDEMPOTENCY_SETS count comment is
updated to "6". Tests assert both `len(EventType)==37` and `len(IDEMPOTENCY_SETS)==6`.
Runtime import confirms 37 / 6 with NO Enum value-aliasing and NO tuple duplicates.

---

## Part 1 — `len(EventType) == 37`

### EventType member count (models.py)

37 enum members, each `NAME = "value"`, spanning lines 33-79. Member-line file:line:

| # | file:line | Member |
|---|-----------|--------|
| 1 | models.py:33 | RUN_STARTED |
| 2 | models.py:34 | ENVIRONMENT_CHECK |
| 3 | models.py:35 | PR_CREATE_ATTEMPTED |
| 4 | models.py:36 | PR_CREATED |
| 5 | models.py:37 | MONITOR_ARMED |
| 6 | models.py:38 | BASELINE_CAPTURED |
| 7 | models.py:40 | POLL_ATTEMPT |
| 8 | models.py:41 | POLL_RESULT |
| 9 | models.py:42 | API_BACKOFF |
| 10 | models.py:43 | CLASSIFIER_UNKNOWN_SHAPE |
| 11 | models.py:44 | REVIEW_DETECTED |
| 12 | models.py:45 | FINDINGS_NORMALIZED |
| 13 | models.py:47 | FINDING_VERIFIED |
| 14 | models.py:48 | FINDING_UNVERIFIED |
| 15 | models.py:50 | ROUND_INCREMENTED |
| 16 | models.py:51 | ROUTE_DECISION |
| 17 | models.py:53 | TROUBLESHOOT_STARTED |
| 18 | models.py:54 | TROUBLESHOOT_COMPLETED |
| 19 | models.py:55 | FIX_APPLIED |
| 20 | models.py:57 | VALIDATION_STARTED |
| 21 | models.py:58 | VALIDATION_COMPLETED |
| 22 | models.py:60 | PUSH_DECISION |
| 23 | models.py:61 | PUSH_INITIATED |
| 24 | models.py:62 | PUSH_COMPLETED |
| 25 | models.py:64 | REPLY_POSTED |
| 26 | models.py:65 | THREAD_RESOLVED |
| 27 | models.py:66 | IDEMPOTENCY_SKIP |
| 28 | models.py:68 | TERMINAL_CLEAN |
| 29 | models.py:69 | TERMINAL_TIMEOUT |
| 30 | models.py:70 | TERMINAL_MAX_ROUNDS |
| 31 | models.py:71 | TERMINAL_HALTED |
| 32 | models.py:72 | TERMINAL_FAILED |
| 33 | models.py:74 | PUSH_ABORTED_OR_NOT_LANDED (the 33rd) |
| 34 | models.py:76 | REREVIEW_REQUESTED (V1.1) |
| 35 | models.py:77 | DECLINE_DETECTED (V1.1) |
| 36 | models.py:78 | AUGGIE_FALLBACK_INVOKED (V1.1) |
| 37 | models.py:79 | MAX_ROUNDS_CLAMPED (V1.1) |

Textual count (grep of member-assignment lines 33-79): **37**.
Runtime import: `len(EventType) == 37`, distinct values == 37 (NO Enum aliasing —
all 37 values are unique, so no member silently collapsed into an alias).

### run_log.py "33"→"37" prose sites (the two required updates)

| Site | file:line | Content | Status |
|------|-----------|---------|--------|
| append() docstring | run_log.py:104 | "...not one of the **37** closed enum values..." | UPDATED to 37 |
| ValueError message | run_log.py:110 | `f"unknown event_type: {event_type!r} (not one of the **37** §11.3 events)"` | UPDATED to 37 |

`grep '33' run_log.py` → **ZERO matches**. No stale EventType-count "33" remains
anywhere in run_log.py. Both required prose sites confirmed at 37.

### Test asserts `len(EventType) == 37`

| Site | file:line | Assertion |
|------|-----------|-----------|
| test_run_log.py | tests/pr_submit/test_run_log.py:167 | `assert len(EventType) == 37` |
| test_run_log.py | tests/pr_submit/test_run_log.py:168 | `assert len(list(EventType)) == 37` |
| test_run_log.py | tests/pr_submit/test_run_log.py:170-173 | asserts all 4 new V1.1 member identifier=value strings |

`test_eventtype_is_37_members_with_v11_events` (test_run_log.py:164) asserts the count
TWICE (`len(EventType)` and `len(list(EventType))`) plus the 4 V1.1 value strings.

### models.py docstring derivation note (NOT a stale count)

- models.py:25 contains `"...the **33** prior members — PLUS the 4 V1.1"`. This is
  CORRECT historical-derivation arithmetic (33 + 4 = 37), NOT a stale EventType-count
  claim. The authoritative count statements (models.py:3 "exactly 37 members",
  models.py:21 "EXACTLY 37 members", models.py:75 "the 34th-37th") all read 37.
  No action required — this "33" is load-bearing provenance, not a drifted count.

---

## Part 2 — `len(IDEMPOTENCY_SETS) == 6`

### Tuple member count (run_log.py:27-34)

6 string members. file:line:

| # | file:line | Member |
|---|-----------|--------|
| 1 | run_log.py:28 | "processed_review_ids" |
| 2 | run_log.py:29 | "processed_finding_ids" |
| 3 | run_log.py:30 | "replied_comment_ids" |
| 4 | run_log.py:31 | "resolved_thread_ids" |
| 5 | run_log.py:32 | "pushed_commit_shas" |
| 6 | run_log.py:33 | "auggie_review_invoked" (the 6th appended — INV-R2) |

Textual count (grep of `"member",` tuple lines): **6**.
Runtime import: `len(IDEMPOTENCY_SETS) == 6`, distinct members == 6 (no tuple dupes).

### Count comment updated (the ":26" site)

| Site | file:line | Content | Status |
|------|-----------|---------|--------|
| IDEMPOTENCY_SETS header comment | run_log.py:26 | `# The **6** idempotency sets (§11.4 + V1.1 addendum §6.3).` | UPDATED to 6 |

`grep '26' run_log.py` → ZERO matches for any stale numeric "26" count. (The only line
*at* line 26 is the comment itself, which now reads "6 idempotency sets" — correct.)

### Test asserts membership + `len == 6`

| Site | file:line | Assertion |
|------|-----------|-----------|
| test_idempotency.py | tests/pr_submit/test_idempotency.py:87 | `assert "auggie_review_invoked" in IDEMPOTENCY_SETS` |
| test_idempotency.py | tests/pr_submit/test_idempotency.py:88 | `assert len(IDEMPOTENCY_SETS) == 6  # 5→6, NOT a "4"/reconcile framing` |

`test_t1120_auggie_review_invoked_at_most_once` (test_idempotency.py:83) asserts BOTH
membership of the 6th set AND `len == 6`. Note: this assertion lives in
test_idempotency.py (imports `IDEMPOTENCY_SETS` at line 12), not in the test_run_log.py
file named in my read list — but it IS a valid, present test site satisfying the
requirement. test_run_log.py additionally exercises the 6th set's fold behavior at
test_run_log.py:221 (`assert state["auggie_review_invoked"] == [99]`).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `len(EventType) == 37` (member count) | PASS | 37 member lines models.py:33-79; runtime `len(EventType)==37`, 37 distinct values |
| 2 | run_log append() docstring "33"→"37" | PASS | run_log.py:104 reads "37 closed enum values" |
| 3 | run_log ValueError "33"→"37" | PASS | run_log.py:110 reads "not one of the 37 §11.3 events" |
| 4 | NO stale EventType "33" in run_log.py | PASS | `grep '33' run_log.py` → 0 matches |
| 5 | Test asserts `len(EventType)==37` | PASS | test_run_log.py:167-168 |
| 6 | `len(IDEMPOTENCY_SETS) == 6` (member count) | PASS | 6 members run_log.py:28-33; runtime `len==6`, 6 distinct |
| 7 | `:26` count comment updated to "6" | PASS | run_log.py:26 "The 6 idempotency sets"; no stale "26" |
| 8 | Test asserts IDEMPOTENCY_SETS membership/`len==6` | PASS | test_idempotency.py:87-88 |
| 9 | Enum value-aliasing check (adversarial) | PASS | runtime: 37 distinct values == 37 members (no silent alias collapse) |
| 10 | Tuple-duplicate check (adversarial) | PASS | runtime: 6 distinct == 6 members (no dup string) |

## Summary

- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: N/A (fix_authorization: false)

## Adversarial findings

Hunted specifically for a count-integrity error. Probed three failure classes a
textual-only count would miss:
1. **Enum value-aliasing** — runtime confirms 37 distinct `.value` strings == 37
   members, so no member silently aliased away. NOT found.
2. **Tuple string-duplication** — runtime confirms 6 distinct == 6 members. NOT found.
3. **Stale residual count prose** — the only surviving "33" (models.py:25) is correct
   derivation arithmetic (33+4=37), not a drifted EventType count; run_log.py has zero
   "33" and zero stale "26". NOT a defect.

No count-integrity error exists. The "≥1 error" prior is not borne out by the evidence.

## Confidence

Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement

Read: 3 | Grep: 4 | Glob: 0 | Bash: 5 (4 grep/sed sweeps + 1 runtime import)
(Tool calls 12 >= 10 checklist items — engagement minimum satisfied; each call mapped
to a specific count site, no padding.)

## QA Complete

VERDICT: PASS
