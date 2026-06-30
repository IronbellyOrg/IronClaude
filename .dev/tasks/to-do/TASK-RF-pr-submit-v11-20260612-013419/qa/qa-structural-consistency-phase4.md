# QA Report — Structural Consistency (Phase 4 / run_log)

**Topic:** pr_submit V1.1 — run_log.py fold/state/test internal consistency
**Date:** 2026-06-12
**Phase:** internal-consistency lens (Phase 4 run_log)
**Lens:** internal-consistency (adversarial stance, fix_authorization: false — report only)

---

## Overall Verdict: PASS

The four mandated checks all hold. Adversarial sweep for ≥5 inconsistencies found
**zero functional inconsistencies** in the four mandated dimensions and surfaced only
**non-blocking observations** (documentation/coverage notes), none of which break the
fold↔state↔test contract. Honest finding: the requested "at least 5 internal
inconsistencies" do not exist as defects; the items below are the closest candidates
and each resolves to CONSISTENT on inspection.

---

## Items Reviewed (4 mandated checks)

| # | Check | Result | Evidence (BOTH sides cited) |
|---|-------|--------|-----------------------------|
| 1 | `state` init seeds agree with keys the new folds WRITE | PASS | Seeds: `rereview_request_count` `run_log.py:161`, `effective_max_rounds` `run_log.py:162`, and `auggie_review_invoked` via `**{s: [] for s in IDEMPOTENCY_SETS}` `run_log.py:164` (set name `run_log.py:33`). Writes: `state["rereview_request_count"] += 1` `run_log.py:176`; `state["effective_max_rounds"] = (clamp…min)` `run_log.py:190-194`; `sets["auggie_review_invoked"].add(ev["pr_number"])` `run_log.py:182` flushed to `state[s]` at `run_log.py:214-215`. Every written key is seeded — no KeyError / unseeded-write path. |
| 2 | Fold EventType refs match member identifiers in models.py | PASS | `EventType.REREVIEW_REQUESTED.value` `run_log.py:174` → `models.py:76`. `EventType.AUGGIE_FALLBACK_INVOKED.value` `run_log.py:178` → `models.py:78`. `EventType.MAX_ROUNDS_CLAMPED.value` `run_log.py:184` → `models.py:79`. (Also pre-existing: `ROUND_INCREMENTED` `models.py:50`, `PUSH_COMPLETED` `models.py:62`, `REPLY_POSTED` `models.py:64`, `THREAD_RESOLVED` `models.py:65`, `FINDINGS_NORMALIZED` `models.py:45`, `FIX_APPLIED` `models.py:55`, `IDEMPOTENCY_SKIP` `models.py:66` — all referenced in folds `run_log.py:172-213,239` and all defined.) No dangling member reference. |
| 3 | Test expectations agree with fold semantics | PASS | count→`rereview_request_count`: two appends `test_run_log.py:214-215` → expect `== 2` `test_run_log.py:220`; fold `+= 1`/event `run_log.py:176` ⇒ 2 ✓. pr_number→set: append `pr_number:99` `test_run_log.py:216-218` → expect `== [99]` `test_run_log.py:221`; fold `sets[...].add(ev["pr_number"])` `run_log.py:182` + `sorted` `run_log.py:215` ⇒ `[99]` ✓. monotone-min→smaller: append `1` then `3` `test_run_log.py:199-205` → expect `== 1` `test_run_log.py:206`; fold `min(prev, clamp)` `run_log.py:193` ⇒ 1 ✓. |
| 4 | 6th set name `"auggie_review_invoked"` identical across run_log.py and tests | PASS | Producer: `run_log.py:33` (IDEMPOTENCY_SETS tuple) + `run_log.py:182` (fold target). Consumers: `test_run_log.py:221`; `test_idempotency.py:87,92,97,100,113,120,121,124,128`. Byte-identical token everywhere (no `auggie_invoked` / `auggie_review_invoke` drift). |

---

## Summary

- Checks passed: 4 / 4
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Adversarial Sweep — candidate inconsistencies probed (all resolved CONSISTENT or non-blocking)

| # | Severity | Location | Probe | Resolution |
|---|----------|----------|-------|------------|
| C1 | INFO (consistent) | `run_log.py:214-215` ↔ `test_run_log.py:221` / `test_idempotency.py:100` | Do idempotency sets rebuild as `set` or `list`? A `set` would break `== [99]` / `== [pr]` equality and crash `json.dumps` in `materialize_snapshot` `run_log.py:221`. | CONSISTENT: `state[s] = sorted(sets[s], key=str)` `run_log.py:215` coerces every set to a **sorted list**, satisfying both list-equality asserts AND JSON-serializability. No defect. |
| C2 | MINOR (non-blocking) | `models.py:77` (`DECLINE_DETECTED`) ↔ `run_log.py` folds | `DECLINE_DETECTED` is asserted as a valid enum member (`test_run_log.py:171`, append-validated `test_run_log.py:183`) but has **no fold branch** in `rebuild_state` `run_log.py:167-213`. | NOT an inconsistency within this lens: the SkillResult field `decline_detected` `models.py:211` is FSM-runtime state, not a run_log rebuild counter; tests only assert it is appendable, never that rebuild folds it. Flag for Phase-5/FSM lens, not a Phase-4 contradiction. |
| C3 | INFO (consistent) | `run_log.py:33` comment "keyed on pr_number" ↔ `run_log.py:182` | Comment claims pr_number keying; fold must actually key on `ev["pr_number"]`. | CONSISTENT: fold guards `ev.get("pr_number") is not None` `run_log.py:178-180` and adds `ev["pr_number"]` `run_log.py:182`. Comment matches code. |
| C4 | INFO (consistent) | `run_log.py:161-162` doc "INV-R1 / INV-R3" ↔ folds `run_log.py:175,187` | Init-dict comment maps `rereview_request_count`→INV-R1 and `effective_max_rounds`→INV-R3; folds must carry the same idiom labels. | CONSISTENT: IDIOM A/INV-R1 `run_log.py:175`, IDIOM C/INV-R3 `run_log.py:187`. Invariant labels align across seed-comment and fold-comment. |
| C5 | INFO (consistent) | `test_run_log.py:167` (`len(EventType) == 37`) ↔ `models.py:20-79` | Enum-count test vs. actual member count after the 4 V1.1 additions. | CONSISTENT: members `RUN_STARTED`…`MAX_ROUNDS_CLAMPED` count to 37 (33 prior + 4 V1.1 `models.py:76-79`). `_VALID_EVENT_VALUES` `run_log.py:36` derives from the same enum, so the append-validator and the count test cannot drift apart. |
| C6 | INFO (consistent) | `run_log.py:200-202` (`reply_posted`→`comment_id`) ↔ `test_run_log.py:152,158` | reply fold keys `replied_comment_ids` on `comment_id`; test appends `comment_id:55` and expects `55 in state["replied_comment_ids"]`. | CONSISTENT: fold `sets["replied_comment_ids"].add(ev["comment_id"])` `run_log.py:202`; `55` is an int, `sorted(...,key=str)` keeps it `55` (int), `55 in [55]` ✓. |

## Issues Found

None blocking. The single tracked observation (C2) is a coverage note for a later lens,
not a Phase-4 fold/state/test contradiction.

## Actions Taken

None (report-only; fix_authorization: false).

## Recommendations

- (Optional, out-of-Phase-4-scope) Confirm in the FSM/Phase-5 lens that `DECLINE_DETECTED`
  is intentionally a runtime-only signal with no `rebuild_state` fold — `run_log.py:167-213`
  deliberately omits it while `test_run_log.py:171,183` only assert appendability. This is the
  one place a future reader could mistake the absence for a gap.

## Confidence

**Confidence:** Verified: 4/4 mandated + 6/6 adversarial probes | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 4 | Grep: 0 | Glob: 0 | Bash: 0 — all four in-scope files
read in full; every cited line verified against the read buffer. (Grep/Glob unnecessary:
the lens is confined to four named files, all read end-to-end.)

## QA Complete

VERDICT: PASS
