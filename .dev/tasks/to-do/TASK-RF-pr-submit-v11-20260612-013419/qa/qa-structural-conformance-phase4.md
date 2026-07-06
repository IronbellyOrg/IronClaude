# QA Report — Phase 4 Structural Conformance (run_log integrity)

**Lens:** template-conformance / item-shape
**Topic:** pr_submit V1.1 — Phase 4 (run_log integrity) deltas
**Date:** 2026-06-12
**Phase:** structural-conformance (custom Phase-4 lens)
**Fix authorization:** false (report only)
**Stance:** ADVERSARIAL — assume ≥5 conformance errors; verify by reading the actual files.

---

## Overall Verdict: PASS

All 5 mandated verification points conform. The adversarial sweep surfaced
**0 conformance errors** against the 5 checks and **3 non-blocking observations**
(documented below — none are conformance failures). I held this to zero-tolerance:
each PASS below cites the exact file:line I read.

---

## Items Reviewed (the 5 mandated checks)

| # | Check | Result | Evidence (file:line) |
|---|-------|--------|----------------------|
| 1 | 6th set `auggie_review_invoked` APPENDED (not reordered), keyed on pr_number | PASS | `run_log.py:27-34` |
| 2 | 3 new folds each key on a DISTINCT event_type | PASS | `run_log.py:174,178,184` |
| 3 | Monotone-min fold uses None-safe form | PASS | `run_log.py:190-194` |
| 4 | `:26` comment + rebuild_state docstring read "6 idempotency sets" | PASS | `run_log.py:26`, `run_log.py:150` |
| 5 | 2 new state-init seeds present | PASS | `run_log.py:161-162` |

---

## Detailed Findings

### Check 1 — 6th set appended (NOT reordered), keyed on pr_number — PASS

`run_log.py:27-34`:
```
IDEMPOTENCY_SETS = (
    "processed_review_ids",
    "processed_finding_ids",  # keyed on fix_key
    "replied_comment_ids",
    "resolved_thread_ids",
    "pushed_commit_shas",
    "auggie_review_invoked",  # keyed on pr_number — INV-R2 strict-once fallback gate
)
```
- The 5 prior members are in their original order (verified against the existing
  folds that key on each: `processed_review_ids` ← FINDINGS_NORMALIZED `run_log.py:211`,
  `processed_finding_ids` ← FIX_APPLIED `:213`, `replied_comment_ids` ← REPLY_POSTED
  `:202`, `resolved_thread_ids` ← THREAD_RESOLVED `:204`, `pushed_commit_shas` ←
  PUSH_COMPLETED `:198`). None reordered.
- `auggie_review_invoked` is the **6th and last** element — appended at the tail.
- Inline comment `# keyed on pr_number` matches the fold at `run_log.py:182`
  (`sets["auggie_review_invoked"].add(ev["pr_number"])`). Key axis = pr_number. ✓
- Cross-check: `test_idempotency.py:88` asserts `len(IDEMPOTENCY_SETS) == 6`;
  `:87` asserts membership.

### Check 2 — 3 new folds each on a DISTINCT event_type (one branch per event) — PASS

Three separate `elif` branches, one event_type each:
- `run_log.py:174` — `elif et == EventType.REREVIEW_REQUESTED.value:` →
  `state["rereview_request_count"] += 1` (`:176`). COUNT fold.
- `run_log.py:177-180` — `elif et == EventType.AUGGIE_FALLBACK_INVOKED.value and
  ev.get("pr_number") is not None:` → `sets["auggie_review_invoked"].add(...)` (`:182`).
  ADD-TO-SET fold, presence-guarded.
- `run_log.py:183-186` — `elif et == EventType.MAX_ROUNDS_CLAMPED.value and
  ev.get("effective_max_rounds") is not None:` → MONOTONE-MIN (`:190-194`).

The three event_types (`rereview_requested`, `auggie_fallback_invoked`,
`max_rounds_clamped`) are distinct closed-enum members — verified to exist at
`models.py:76,78,79`. No two folds share an event_type; the `if/elif` chain
makes them mutually exclusive. ✓

### Check 3 — monotone-min fold None-safe form — PASS

`run_log.py:190-194`:
```
prev = state["effective_max_rounds"]
clamp = ev["effective_max_rounds"]
state["effective_max_rounds"] = (
    clamp if prev is None else min(prev, clamp)
)
```
Exactly the required None-safe form: `clamp if prev is None else min(prev, clamp)`.
First clamp seeds (prev is None → take clamp); subsequent clamps take `min`, so a
later HIGHER value can never raise the result. ✓
Behaviorally locked by `test_run_log.py:192-206` (seed→None, then 1, then 3 →
rebuild == 1).

### Check 4 — count comment + rebuild_state docstring read "6 idempotency sets" — PASS (with note)

- `run_log.py:26`: `# The 6 idempotency sets (§11.4 + V1.1 addendum §6.3).` — reads
  "6 idempotency sets". ✓
- `run_log.py:150` (rebuild_state docstring): `Reconstructs the FSM state,
  ``round_counter``, the 6 idempotency sets, and` — reads "6 idempotency sets". ✓

NOTE (not a failure): the Phase-4 inventory summary
(`phase4-output-summary.md:7`) describes this delta as updating the comment/docstring
`"5→6"`. The task spec for THIS lens (check 4) requires the literal final text to
read **"6 idempotency sets"**, which it does. The inventory's "5→6" is a
description of the *change*, not the *final literal*; both are internally
consistent. No conformance error.

### Check 5 — 2 new state-init seeds present — PASS

`run_log.py:161-162`:
```
"rereview_request_count": 0,
"effective_max_rounds": None,
```
Both seeds present with the correct initial values (count seed = `0`;
monotone-min seed = `None` = never-clamped). Placed in the `state` dict literal
inside `rebuild_state` (`:153-165`), ahead of the per-set seeding at `:164`. ✓
Seed semantics match the inline rationale at `:159-160` and the fold logic.

---

## Adversarial Sweep — non-blocking observations (NOT conformance failures)

These were hunted for under the "find ≥5 errors" mandate. None violate the 5
checks; recorded for completeness so a false PASS is not masked.

| # | Severity | Location | Observation | Why NOT a Check failure |
|---|----------|----------|-------------|--------------------------|
| O-1 | INFO | `test_idempotency.py:107-128` | `decline-twice.json` is loaded but only `expected.auggie_review_invoked_count` is consumed; the `cycles`/`max_rounds`/`effective_max_rounds` fixture keys are NOT exercised by the test body. The fixture's `effective_max_rounds:1` is asserted nowhere. | Outside the 5 mandated checks (fixture-coverage depth, not item-shape). The fixture *exists* and *parses* (`decline-twice.json:1-8`), satisfying the inventory's schema-(c) claim. Flag for the test-coverage lens, not this one. |
| O-2 | INFO | `run_log.py:182` vs `record_idempotent:236` | The set folds the RAW `pr_number` (int) via `.add(ev["pr_number"])`, then `:215` sorts `key=str`; `record_idempotent` compares `str(key)`. Int 55 in the set vs str "55" comparison is reconciled only because `record_idempotent` stringifies BOTH sides (`:236` `{str(k) for k in ...}`). Type is int-in-set, str-on-compare. | Correct by construction — the stringify-both-sides at `:236` makes it sound; `test_t1120` (`:99-100`) proves `state["auggie_review_invoked"] == [pr]` (int). No behavioral defect. Not an item-shape issue. |
| O-3 | INFO | `run_log.py:33` | Inline comment cites "INV-R2 strict-once fallback gate"; the fold comment at `:181` cites "INV-R2 strict-once, keyed on pr_number". Consistent cross-reference; no drift. | Confirms, not contradicts. Recorded to show the cross-ref was checked, not skipped. |

---

## Summary

- Mandated checks passed: **5 / 5**
- Mandated checks failed: **0**
- Conformance errors found: **0** (adversarial target was ≥5; after reading
  `run_log.py`, both test files, `decline-twice.json`, and cross-referencing
  `models.py`, none of the 5 item-shape contracts are violated)
- Non-blocking observations: **3** (all outside this lens's scope; O-1 is the
  most actionable — route to the test-coverage lens)
- Issues fixed in-place: **0** (fix_authorization: false)

## Confidence

**Verified:** 5/5 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%

Every mandated check was verified against a primary-source file read (not against
the inventory summary). The enum-existence dependency for Check 2 was independently
verified in `models.py:76-79` rather than trusted from the fold code.

**Tool engagement:** Read: 6 | Grep: 0 | Glob: 0 | Bash: 0

(6 Reads: phase4-output-summary.md, run_log.py, test_run_log.py, test_idempotency.py,
decline-twice.json, models.py. Read count ≥ 5 mandated checks → engagement
minimum satisfied. No web research required — all claims are local-source.)

---

VERDICT: PASS
