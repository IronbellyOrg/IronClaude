# QA Report — Domain Accuracy (Phase 4: run_log)

**Topic:** pr_submit V1.1 — run-log fold idioms (IDIOM A/B/C) + write-ahead discipline
**Date:** 2026-06-12
**Phase:** doc-qualitative / domain-accuracy lens (Phase 4 run_log)
**Fix authorization:** false (report only — nothing modified)
**Adversarial stance:** assumed ≥5 domain errors; verified every claim by READING + RUNNING source.

---

## Overall Verdict: PASS

All 5 domain claims verified against actual source and live runtime behavior. The
three fold idioms are correct, the write-ahead/fsync discipline is preserved, and the
6th idempotency set is keyed on the `pr_number` scalar (not a comment id). No domain
errors found that rise to a defect; 2 benign observations recorded below (neither
blocks PASS).

---

## Items Reviewed

| # | Claim | Result | Evidence |
|---|-------|--------|----------|
| 1 | IDIOM A (COUNT) for REREVIEW_REQUESTED matches existing ROUND_INCREMENTED count idiom | PASS | run_log.py:172-176 |
| 2 | IDIOM B (ADD-TO-SET) for AUGGIE_FALLBACK_INVOKED matches THREAD_RESOLVED/PUSH_COMPLETED add-to-set idiom (presence-guarded on key) | PASS | run_log.py:177-182, 195-204 |
| 3 | IDIOM C (MONOTONE-MIN) is a one-way non-increasing clamp; None=never-clamped; first clamp seeds; later higher value cannot raise (INV-R3) | PASS | run_log.py:183-194; live trace + test_run_log.py:192-206 |
| 4 | Write-ahead/fsync discipline preserved — new folds are read-side only; append() still fsyncs | PASS | run_log.py:101-123, 146-216; AST scan |
| 5 | 6th set keyed on `pr_number` (per-PR scalar), NOT a comment id | PASS | run_log.py:26-34, 178-182 |

---

## Claim-by-Claim Verification

### Claim 1 — IDIOM A (COUNT fold) parity: PASS

The existing count idiom (ROUND_INCREMENTED) and the new REREVIEW_REQUESTED fold are
structurally identical — both are **unconditional** `+= 1` increments on the matching
event_type, with NO presence guard:

- ROUND_INCREMENTED → `state["round_counter"] += 1` (run_log.py:172-173)
- REREVIEW_REQUESTED → `state["rereview_request_count"] += 1` (run_log.py:174-176)

The seed `"rereview_request_count": 0` is present in the state dict (run_log.py:163,
161-164) mirroring `"round_counter": 0`. Live test confirms two REREVIEW_REQUESTED
events fold to count 2 (test_run_log.py:214-220 → `rereview_request_count == 2`,
passing). MATCH — true mirror of the count idiom.

### Claim 2 — IDIOM B (ADD-TO-SET fold) parity: PASS

The add-to-set idiom is presence-guarded on the key, and the new AUGGIE_FALLBACK_INVOKED
fold follows it:

- THREAD_RESOLVED → guard in the `elif` (`and ev.get("thread_id")`), then
  `sets["resolved_thread_ids"].add(ev["thread_id"])` (run_log.py:203-204).
- PUSH_COMPLETED → guard in the body (`if ev.get("target_sha")`), then
  `sets["pushed_commit_shas"].add(ev["target_sha"])` (run_log.py:195-198).
- AUGGIE_FALLBACK_INVOKED → guard in the `elif`
  (`and ev.get("pr_number") is not None`), then
  `sets["auggie_review_invoked"].add(ev["pr_number"])` (run_log.py:177-182).

The set name `"auggie_review_invoked"` is in IDEMPOTENCY_SETS (run_log.py:33), so it
auto-derives its empty-list seed (run_log.py:164), working set (run_log.py:166), and
sorted serialization (run_log.py:214-215). Live test: two duplicate pr_number=7
AUGGIE events fold to `[7]` (dedup via set semantics) — confirmed. MATCH.

**Benign observation O-1 (NOT a defect):** the guard idiom differs in *kind* between
siblings — THREAD_RESOLVED uses truthiness (`and ev.get("thread_id")`) while AUGGIE
uses explicit identity (`and ev.get("pr_number") is not None`). The brief's own
wording ("presence-guarded on the key") is satisfied by both. The `is not None` form is
in fact the *safer* choice: a hypothetical `pr_number == 0` would be dropped by a
truthiness guard but correctly recorded by `is not None`. PR numbers are never 0, so
the difference is unobservable in practice. No action required; recorded only for
completeness under the adversarial stance.

### Claim 3 — IDIOM C (MONOTONE-MIN fold), INV-R3: PASS — worked trace below

The clamp is implemented at run_log.py:183-194:

```python
elif (
    et == EventType.MAX_ROUNDS_CLAMPED.value
    and ev.get("effective_max_rounds") is not None
):
    prev = state["effective_max_rounds"]
    clamp = ev["effective_max_rounds"]
    state["effective_max_rounds"] = (
        clamp if prev is None else min(prev, clamp)
    )
```

Properties verified:
- **None = never-clamped:** seed `"effective_max_rounds": None` (run_log.py:163);
  no MAX_ROUNDS_CLAMPED event leaves it None.
- **First clamp seeds:** `clamp if prev is None` — the first event sets the value
  outright (no spurious `min(None, x)`).
- **One-way non-increasing:** `min(prev, clamp)` — a later higher value cannot raise it.

**Worked two-event trace (brief requirement)** — live execution, pr_number=7:
| Step | Event | prev | clamp | result |
|------|-------|------|-------|--------|
| seed | (none) | — | — | `None` |
| 1 | MAX_ROUNDS_CLAMPED max=5 | None | 5 | `5` (first clamp seeds) |
| 2 | MAX_ROUNDS_CLAMPED max=2 | 5 | 2 | `2` (min — decreases) |
| 3 | MAX_ROUNDS_CLAMPED max=9 | 2 | 9 | `2` (higher value does NOT raise — INV-R3) |

The repo test orders the higher value AFTER the lower precisely to prove non-increase:
clamp 1 then clamp 3 → result 1 (test_run_log.py:192-206, passing). MATCH — INV-R3
holds. No in-repo precedent existed for this idiom (research §4.3); the authored form
is correct.

### Claim 4 — Write-ahead / fsync discipline preserved: PASS

- `append()` retains the durability triad: `fh.write(... + "\n"); fh.flush();
  os.fsync(fh.fileno())` (run_log.py:119-122). Unchanged by V1.1.
- `write_ahead()` remains a thin alias of `append()` with identical durability
  (run_log.py:125-131).
- The new folds live entirely inside `rebuild_state()` (run_log.py:146-216), which is
  **read-side only**. AST/source scan of `rebuild_state` confirms ZERO occurrences of
  `fsync`, `flush`, `.write`, `append(`, or `open(`; its only I/O is `read_events()`
  (read-only, run_log.py:135-144). The three new folds mutate in-memory `state`/`sets`
  dicts only — they do not write to the JSONL.

The crash-safety primitive (fsync-before-side-effect) is untouched; rebuild is a pure
read-time fold. MATCH.

### Claim 5 — 6th set keyed on `pr_number` (per-PR scalar), NOT comment id: PASS

- IDEMPOTENCY_SETS declares the 6th set with an explicit comment:
  `"auggie_review_invoked",  # keyed on pr_number — INV-R2 strict-once fallback gate`
  (run_log.py:33).
- The fold adds `ev["pr_number"]` (a per-PR scalar), never a comment_id
  (run_log.py:182).
- Contrast with comment-id-keyed sets: `replied_comment_ids` folds `ev["comment_id"]`
  (run_log.py:199-202) and `resolved_thread_ids` folds `ev["thread_id"]`
  (run_log.py:203-204). `auggie_review_invoked` deliberately does NOT key on either —
  it keys on the PR scalar, giving strict-once-per-PR semantics (INV-R2). Live test:
  two AUGGIE events with the same pr_number collapse to a single-element set. MATCH.

**Benign observation O-2 (NOT a defect):** because the set keys on a single per-PR
scalar (`self.pr_number` is fixed for the whole run-log), this "set" will hold at most
one element in normal operation. That is exactly the intended INV-R2 strict-once
fallback gate — the set machinery is reused for idempotent membership semantics, not
for cardinality. Consistent with the brief; no action.

---

## Adversarial Sweep — errors hunted, NOT found

Per the ≥5-errors stance, I specifically probed for these failure modes and confirmed
each is absent:

1. **Count fold accidentally guarded / double-counted** — checked ROUND vs REREVIEW
   are both unconditional single `+= 1`; no double-increment, no stray guard. CLEAN.
2. **Add-to-set folding the wrong field** (e.g. comment_id into the pr_number set) —
   confirmed `ev["pr_number"]`, not comment_id. CLEAN.
3. **Monotone-min raising on a later higher value** (the classic INV-R3 break) —
   live-traced None→5→2→2; higher 9 did not raise. CLEAN.
4. **`min(None, x)` TypeError on first clamp** — the `prev is None` branch avoids the
   comparison; first clamp seeds outright. CLEAN.
5. **rebuild_state leaking a write/fsync** (breaking the read-side-only invariant) —
   AST scan: no write/fsync/append/open in rebuild_state. CLEAN.
6. **append() losing its fsync under V1.1** — fsync still present at run_log.py:122.
   CLEAN.
7. **6th set not auto-derived** (missing seed / serialization) — IDEMPOTENCY_SETS
   membership gives it seed + working-set + sorted serialize automatically. CLEAN.
8. **each event_type in >1 elif branch** (overlapping folds) — single if/elif chain
   keyed on `et`; each new event in exactly one branch. CLEAN.

The 2 observations above (O-1 guard-form divergence, O-2 single-element set) are the
only deviations from a hypothetical "perfectly uniform" implementation, and both are
correct-by-design, not errors.

---

## Self-Audit

**(a) Reliance list — items NOT independently re-verified (structural, owned elsewhere):**
- Relied on prior Phase structural QA for the EventType "EXACTLY 37" docstring/count
  drift across models.py + run_log.py ValueError message (this lens is fold-domain, not
  count-string-sync) — but note I still independently confirmed `len(EventType) == 37`
  passes (test_run_log.py:164-168).

**(b) Independent semantic checks (≥1 required):**
- Monotone-min INV-R3 semantics — verified by LIVE EXECUTION of a 3-event clamp trace
  (None→5→2→2) via `uv run python`, not by reading the test assertion alone.
- Read-side-only invariant — verified by AST/source scan of `rebuild_state` for
  write/fsync/append/open tokens (all absent), not by trusting the docstring.
- Add-to-set dedup on duplicate pr_number — verified by live double-append of
  pr_number=7 folding to `[7]`.

**Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 4 | Grep: 1 | Glob: 1 | Bash: 4 (incl. live test run + 2 runtime traces)

---

## Issues Found

None of any severity. Two benign, correct-by-design observations (O-1, O-2) recorded
above for completeness; neither is a defect and neither blocks PASS.

---

VERDICT: PASS
