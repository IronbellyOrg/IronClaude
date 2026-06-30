# QA Report — Phase 4 Content Cross-Reference (run_log / idempotency)

**Topic:** pr-submit v11 — Phase 4 FR→test chain verification
**Date:** 2026-06-12
**Phase:** task-qualitative (FR→test cross-reference, Phase 4 scope only)
**Fix cycle:** N/A (fix_authorization: false — report only)

**Scope:** FR-10.1 / 10.2 / 10.4, INV-R1 / R2 / R3 (run_log + idempotency). Phase 5/6
T-IDs (retrigger/fallback/fsm/skill) explicitly out of scope and NOT flagged.

---

## Overall Verdict: PASS

Adversarial stance applied: I assumed >=5 broken FR→test chains existed and tried to
break each link by reading the actual source + tests AND executing the suite. Every
Phase-4-scope FR sub-ID resolves to a verifying test whose assertions exercise the real
behavior. The 15 Phase-4 tests pass live (`15 passed in 0.06s`). No broken chains found
within the Phase-4 scope.

---

## Link-by-Link Trace (each link cited)

### Link 1 — FR-10.1: 6th idempotency set + `record_idempotent` strict-once → T-1120 / T-AUGGIE-AT-MOST-ONCE

**Source side:**
- 6th set member declared: `run_log.py:33` — `"auggie_review_invoked"` is the 6th tuple
  member of `IDEMPOTENCY_SETS` (`run_log.py:27-34`), commented `INV-R2 strict-once
  fallback gate`. The set has exactly 6 members.
- `record_idempotent` strict-once: `run_log.py:226-245`. It rebuilds state
  (`run_log.py:235`), checks membership against the rebuilt set (`run_log.py:236`),
  appends an `idempotency_skip` and returns `False` if present (`run_log.py:237-244`),
  else returns `True`. This is the strict-once primitive.
- Fold that makes the set durable: `run_log.py:177-182` — `AUGGIE_FALLBACK_INVOKED`
  with non-null `pr_number` adds `pr_number` to `auggie_review_invoked` (IDIOM B).

**Test side:** `test_idempotency.py:83-104` (`test_t1120_auggie_review_invoked_at_most_once`).
- Asserts membership + cardinality: `test_idempotency.py:87-88`
  (`"auggie_review_invoked" in IDEMPOTENCY_SETS`; `len(IDEMPOTENCY_SETS) == 6` — and the
  comment explicitly rejects the "4"/reconcile framing).
- Strict-once behavior: first call `True` (`:92`), replay `False` (`:97`), set folds the
  pr exactly once (`:99-100`), exactly one `idempotency_skip` (`:101-104`).

**Verdict: VERIFIED.** Live: passes. The docstring carries both T-IDs (`T-1120 /
T-AUGGIE-AT-MOST-ONCE`, `:83-86`), so both label forms map to this single test.

---

### Link 2 — FR-10.2 / INV-R3: clamp → `MAX_ROUNDS_CLAMPED` monotone-min fold → clamp test

**Source side:** `run_log.py:183-194` (IDIOM C, monotone-min fold). `MAX_ROUNDS_CLAMPED`
with non-null `effective_max_rounds`: `None` (never-clamped) is seeded by the first clamp;
otherwise `min(prev, clamp)` (`run_log.py:192-194`). A later higher value can never raise
the rebuilt value — the one-way non-increasing INV-R3 property. Default seed `None` set at
`run_log.py:163`.

**Test side:** `test_run_log.py:192-206`
(`test_max_rounds_clamped_monotone_min_fold_inv_r3`).
- Seeds default `None`: `:198`.
- Appends clamp=1 then a LATER, HIGHER clamp=3 (`:199-205`) — ordering chosen specifically
  to prove the higher later value never raises the result.
- Asserts rebuild == 1 (the smaller): `:206`.

**Verdict: VERIFIED.** This is the strongest possible adversarial ordering (higher-after-
lower) and it passes. INV-R3 monotone non-increasing is genuinely exercised, not stubbed.

---

### Link 3 — FR-10.4: resume strict-once → `rebuild_state` folds the set → T-1124

**Source side:** Resume path is `RunLog.__init__` continuing `event_id` from an existing
JSONL (`run_log.py:84-85`) + `rebuild_state` folding the authoritative JSONL into the
6 sets (`run_log.py:146-216`), specifically the `auggie_review_invoked` fold at
`run_log.py:177-182`. A fresh `RunLog` over the same dir reconstructs the set from the
JSONL (NFR-6 rebuild-is-authoritative).

**Test side:** `test_idempotency.py:107-128` (`test_t1124_auggie_strict_once_survives_resume`).
- First invoke recorded + event appended: `:113-116`.
- Fresh `RunLog` over the same `tmp_path` rebuilds (`:118-119`) — the resume simulation.
- pr present, cardinality 1 after rebuild: `:120-121`.
- Cross-checked against the fixture's expected count: `:123-126`
  (`decline-twice.json` → `expected.auggie_review_invoked_count == 1`, fixture
  verified at `tests/pr_submit/fixtures/decline-twice.json:7`).
- Dedup still fires post-resume: `:128` (`record_idempotent(...) is False`).

**Verdict: VERIFIED.** The fixture exists, `load_fixture` exists
(`conftest.py:21-22`), and the resume-survives strict-once chain is exercised end-to-end.

---

## INV-R1 / R2 coverage (Phase-4 idempotency-set scope)

These are in-scope as the run_log fold idioms (INV-R1/R2/R3 were named in scope):

- **INV-R1** (re-trigger count, IDIOM A): source `run_log.py:172-176`
  (`REREVIEW_REQUESTED` → `rereview_request_count += 1`); test
  `test_run_log.py:209-221` asserts count == 2 (`:214-215, :220`). VERIFIED.
- **INV-R2** (strict-once, IDIOM B): source `run_log.py:177-182`; tested by Link 1
  (T-1120) and Link 3 (T-1124). VERIFIED.
- **INV-R3** (monotone-min clamp, IDIOM C): Link 2. VERIFIED.

All three V1.1 fold idioms (A/B/C) have dedicated verifying tests.

---

## Supporting-substrate cross-checks (would-have-broken-the-chain probes)

- **37-member closed enum** the folds depend on: source `models.py:45-79` (all 12 probed
  members present incl. the 4 V1.1 events at `models.py:76-79`); live count == 37
  (`uv run python -c "len(list(EventType))"` → 37); test
  `test_run_log.py:164-173` asserts `len(EventType) == 37` + the 4 exact value strings.
  VERIFIED. (If the count had drifted, the AUGGIE/CLAMP folds would silently never match
  — this guard is real.)
- **`fix_key` comment_id-independence** (underpins the 2nd set `processed_finding_ids`):
  property `models.py:163-171` = `sha256(path+line+body)`, no comment_id; module-level
  `fix_key` `run_log.py:54-56` identical formula. Test `test_idempotency.py:45-77`
  proves two findings with different `comment_id` (100 vs 999) hash identically and
  produce exactly one fix. VERIFIED.
- **closed-enum append validation** (the folds can't ingest a typo event): source
  `run_log.py:107-111`; test `test_run_log.py:176-189`. VERIFIED.

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | FR-10.1 6th set + strict-once → T-1120 | none | PASS | run_log.py:33,226-245 ↔ test_idempotency.py:83-104 |
| 2 | FR-10.2/INV-R3 monotone-min clamp → clamp test | none | PASS | run_log.py:183-194 ↔ test_run_log.py:192-206 |
| 3 | FR-10.4 resume strict-once → T-1124 | none | PASS | run_log.py:146-216 ↔ test_idempotency.py:107-128 + fixture:7 |
| 4 | INV-R1 re-trigger count fold | none | PASS | run_log.py:172-176 ↔ test_run_log.py:209-221 |
| 5 | INV-R2 strict-once fold (B) | none | PASS | run_log.py:177-182 ↔ T-1120 + T-1124 |
| 6 | 37-enum guard the folds rely on | none | PASS | models.py:45-79 (live 37) ↔ test_run_log.py:164-173 |
| 7 | fix_key comment_id-independence | none | PASS | models.py:163-171 ↔ test_idempotency.py:45-77 |
| 8 | record_idempotent test validity (not stub) | none | PASS | exercises real RunLog over tmp_path, real JSONL rebuild |
| 9 | Live suite execution | none | PASS | 15 passed in 0.06s |

(Axis column: this is a focused FR→test cross-reference rather than a full task-file
review; the five-axis lens was applied — no drift/contradiction/omission/weakened-criteria/
invented-content surfaced within Phase-4 scope.)

## Summary
- Checks passed: 9 / 9
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found
None within Phase-4 scope.

### Adversarial probes that did NOT yield a finding (evidence the search was real)
- Probed whether `record_idempotent` was a no-op stub: it is not — it rebuilds from
  JSONL and gates on the rebuilt set (`run_log.py:235-236`).
- Probed whether the clamp test used a trivial same-value ordering (would not prove
  monotonicity): it deliberately orders higher-AFTER-lower (`test_run_log.py:199-205`).
- Probed whether T-1124's fixture existed / matched the asserted count: it exists and
  `expected.auggie_review_invoked_count == 1` matches (`fixture:7` ↔ `test:123-126`).
- Probed whether `len(IDEMPOTENCY_SETS) == 6` was asserted (not a stale "5"/"4"): it is
  (`test_idempotency.py:88`).
- Probed whether the EventType count guard could silently drift: live count is 37 and the
  test pins it (`test_run_log.py:168`).

## Self-Audit
1. **Factual claims verified against source:** 9 distinct links, each traced to specific
   source line ranges AND test line ranges; plus the live EventType count (37) and a live
   test run (15 passed).
2. **Files read to verify:** `run_log.py` (full), `test_run_log.py` (full),
   `test_idempotency.py` (full), `models.py:45-79` + `:142-171`,
   `tests/pr_submit/fixtures/decline-twice.json` (full), `conftest.py:21-22` (load_fixture).
3. **Why trust the PASS:** Each link cites both a source location and a test location, the
   suite was executed (not merely read), and five named adversarial probes were run and
   documented as not-yielding — the search for breakage was active, not confirmatory.
4. **Web research:** none performed (out of scope per prompt); no Tavily/fallback needed.

## Confidence
Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 5 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 4

## QA Complete

VERDICT: PASS
