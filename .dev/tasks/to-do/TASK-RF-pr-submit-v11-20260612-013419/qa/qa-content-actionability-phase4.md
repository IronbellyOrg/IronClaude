# QA Report — Phase 4 (run_log) Actionability / Test-Correctness Lens

**Topic:** pr_submit V1.1 — Phase 4 run_log test non-vacuity audit
**Date:** 2026-06-12
**Phase:** task-qualitative (actionability / test-correctness lens, adversarial)
**Fix cycle:** N/A
**Fix authorization:** false (report only — nothing modified; all source mutations reverted byte-for-byte)

---

## Overall Verdict: PASS

The four named tests are all **discriminating** — each one was empirically proven to FAIL
under the exact inverse implementation it claims to guard against (mutation testing, not
inspection-only). The adversarial "≥5 vacuous tests" hypothesis is **not supported for the
four target tests**; I ran 5 source mutations and every one was caught. I record one genuine
**MINOR partial-vacuity weakness** in `test_t1124_auggie_strict_once_survives_resume` (its
loaded fixture's "two declines" premise is never exercised — only its `expected` scalar is
read), and several lower-tier observations on the surrounding Phase-4 surface. None rise to
IMPORTANT/CRITICAL; none block the four core guarantees.

---

## Items Reviewed
| # | Check (target test) | Result | Evidence |
|---|---------------------|--------|----------|
| Q1 | `test_max_rounds_clamped_monotone_min_fold_inv_r3` discriminates min-vs-max + None-guard | PASS | Two mutations (min→max; drop None-guard) both fail the test — see Mutation 1 + 2 |
| Q2 | `test_eventtype_is_37_members_with_v11_events` catches count drift | PASS | Removing 1 member → `assert 36 == 37` fails — see Mutation 3 |
| Q3 | `test_t1124_auggie_strict_once_survives_resume` rebuilds a 2nd RunLog from JSONL (not in-memory) | PASS (w/ MINOR note) | Neutering the JSONL→set fold yields `assert 55 in []` on `rl2` — see Mutation 5 |
| Q4 | `test_t1120_auggie_review_invoked_at_most_once` asserts True-then-False + skip event | PASS | Explicit `is True`/`is False`/`len(skips)==1`; broken dedup fails it — see Mutation 4 |

---

## Per-question reasoning (the four key non-vacuity questions)

### Q1 — `test_max_rounds_clamped_monotone_min_fold_inv_r3` (test_run_log.py:192-206)

**Discriminating: YES — on both failure modes asked about.**

The test orders the events correctly to be a real proof: it appends `effective_max_rounds=1`
**first** (line 199-201), then the HIGHER `effective_max_rounds=3` **second** (line 203-205),
then asserts the rebuild yields `1` (line 206). Because the higher value arrives *after* the
lower one, a correct monotone-min fold must refuse to raise the result — exactly the INV-R3
one-way-non-increasing property. It also seeds the invariant by asserting the never-clamped
default is `None` first (line 198).

- **Would it fail if the fold used `max` instead of `min`?** YES. **Mutation 1** changed
  `run_log.py:193` `min(prev, clamp)` → `max(prev, clamp)`. Result:
  `assert 3 == 1` → FAILED. The ordering is what makes this bite: with `max`, the later `3`
  raises the result; the test catches it.
- **Would it fail if the None-safe guard were dropped?** YES. **Mutation 2** replaced
  `clamp if prev is None else min(prev, clamp)` with bare `min(prev, clamp)`. Result:
  `TypeError: '<' not supported between instances of 'int' and 'NoneType'` → FAILED, because
  the *first* clamp folds against the seeded `None`. The test exercises the first-clamp path,
  so it covers the guard.

**Regression caught:** any future edit that makes the `effective_max_rounds` clamp
non-monotone (a later larger ceiling raising the effective cap) or that removes None-seed
safety. This is the load-bearing INV-R3 guarantee.

### Q2 — `test_eventtype_is_37_members_with_v11_events` (test_run_log.py:164-173)

**Discriminating: YES.**

Asserts `len(EventType) == 37` two ways (line 168-169) and pins the 4 V1.1 members to their
exact `identifier == value` strings (line 170-173). I confirmed the live enum is genuinely 37
at runtime (`len(EventType) == 37`), and it is the *closed* set the writer validates against
(`run_log.py:36 _VALID_EVENT_VALUES`, enforced in `append()` lines 108-111).

- **Would it FAIL on count drift?** YES. **Mutation 3** removed one member
  (`MAX_ROUNDS_CLAMPED`) from `models.py`. Result: `assert 36 == 37` → FAILED. A removed member
  or any net count change (add without intent, rename that drops one) trips it. The value-string
  pins additionally catch a silent rename of any of the 4 V1.1 events (e.g.
  `auggie_fallback_invoked` → `auggie_fallback`) even if the count stayed 37.

**Regression caught:** enum-count drift and V1.1-event identifier/value rename — the closed-set
integrity the run-log writer depends on.

### Q3 — `test_t1124_auggie_strict_once_survives_resume` (test_idempotency.py:107-128)

**Discriminating: YES — and it genuinely constructs a SECOND RunLog that rebuilds from the
on-disk JSONL.** (One MINOR partial-vacuity note below.)

The test creates `rl = RunLog(pr, tmp_path)`, records + appends the fallback event, then
creates a **distinct** `rl2 = RunLog(pr, tmp_path)` over the same dir (line 118) and calls
`rl2.rebuild_state()` (line 119). Because `rebuild_state()` reads the authoritative JSONL from
disk (`run_log.py:146-216` → `read_events()` → `jsonl_path.read_text`), `rl2` cannot inherit
`rl`'s in-memory state — its `sets` dict starts empty and is rebuilt purely from the file.

- **Does it really rebuild from disk, not reuse the first instance's memory?** YES, proven by
  **Mutation 5**: I neutered the AUGGIE_FALLBACK_INVOKED→set fold in `rebuild_state`
  (`run_log.py:177-182`). Result: `assert 55 in state["auggie_review_invoked"]` →
  `assert 55 in []` → FAILED. If `rl2` had been silently reusing `rl`'s memory, this mutation
  could not have emptied the set. It did. So the second-instance/JSONL-rebuild path is real.
- The test also asserts post-resume dedup still fires:
  `rl2.record_idempotent(...) is False` (line 128), and the set has exactly one element
  (line 121).

**Regression caught:** a resume/crash-recovery regression where the strict-once gate is lost
across process restart (set not rebuilt from JSONL) — the exact INV-R2 durability property.

**MINOR weakness (partial vacuity):** the test loads `decline-twice.json` whose `cycles`
encode **two** decline observations, and the docstring/comment claims "Even across the two
declines in the fixture, the invoke is recorded once" (line 122-123). But the fixture's
`cycles` are never fed to any FSM/replay — the test manually appends a **single**
`AUGGIE_FALLBACK_INVOKED` event (line 114-116). The only fixture field actually used is the
scalar `fixture["expected"]["auggie_review_invoked_count"]` (== 1) on line 125. So the
"survives two declines" claim is asserted by construction (one manual append vs. a hard-coded
`1`), **not** by exercising the two-decline path. The test still soundly proves *resume
preserves a single recorded invoke*; it does **not** prove *two real declines collapse to one
invoke*. The fixture is decorative for the cross-decline claim. **Severity: MINOR** — the core
resume guarantee is real and mutation-caught; only the stronger "across two declines"
narrative is under-exercised. Recommend either (a) drive the two `cycles` through the FSM and
assert one invoke, or (b) soften the docstring to match what is actually asserted.

### Q4 — `test_t1120_auggie_review_invoked_at_most_once` (test_idempotency.py:83-104)

**Discriminating: YES — asserts True-then-False AND the idempotency_skip event.**

Explicit sequence: `record_idempotent(...) is True` (line 92, first invoke proceeds) →
append the fallback event → `record_idempotent(...) is False` (line 97, replay skips) →
`state["auggie_review_invoked"] == [pr]` (line 100, folded exactly once) →
`len(skips) == 1` (line 104, exactly one `idempotency_skip` emitted). It also pins the set
membership and the 5→6 cardinality (`len(IDEMPOTENCY_SETS) == 6`, line 88), explicitly
rejecting a "4"/reconcile framing.

- **Would it fail if dedup were broken?** YES. **Mutation 4** forced
  `record_idempotent`'s membership test to always-False (never dedups). Result: the second
  call returned `True`, so `assert ... is False` → `assert True is False` → FAILED. The
  True→False transition is genuinely load-bearing, and the skip-event count would also drop to
  0.

**Regression caught:** loss of the strict-once gate within a single run (a second decline
re-invoking the auggie fallback), plus failure to emit the audit `idempotency_skip` event.

---

## Adversarial sweep — the "≥5 vacuous tests" hypothesis

Stance required hunting for ≥5 vacuous/weak tests. Findings across the Phase-4 run_log surface:

- **Four target tests: NOT vacuous.** 5 mutations applied, 5 caught (1:1, no survivors among
  the inverse implementations asked about).
- **1 genuine partial-vacuity weakness found** (MINOR): t1124's fixture `cycles` are unused
  (detailed in Q3). This is the strongest "vacuity" signal in the set, and it is partial — the
  test's primary assertion is sound.
- The hypothesis of **5 fully vacuous tests is not supported** for this file set. I did not
  manufacture findings to hit a quota; the adversarial mutations actively *tried* to slip past
  each test and could not. Reporting honestly: 1 MINOR + lower-tier observations below, not 5
  CRITICALs.

---

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | test_idempotency.py:107-126 | `decline-twice.json` `cycles` are loaded but never exercised; the "survives two declines" claim rests on a single manual append vs a hard-coded `1`. Partial vacuity of the cross-decline narrative (core resume assertion is sound). | Drive the two fixture `cycles` through the FSM/replay and assert one invoke, OR soften the docstring (line 122-123) to "a single recorded invoke survives resume". |
| 2 | MINOR (observation) | test_run_log.py:164-173 | `test_eventtype_is_37_members` pins count + the 4 V1.1 members, but does NOT pin the other 33 identifier→value strings, so a silent rename of a non-V1.1 member (e.g. `push_completed`→`push_done`) that keeps count 37 would pass here. | Acceptable as-scoped (count + V1.1 focus). If broader rename-protection is desired, add a frozenset equality of all 37 value strings. Not blocking. |
| 3 | MINOR (observation) | test_run_log.py:192-206 | INV-R3 test covers first-clamp (None seed) and later-higher. It does NOT assert later-LOWER actually lowers further (e.g. 3 then 1 → 1 in the opposite order). The `min` direction is already proven by Mutation 1, so this is completeness, not a gap. | Optional: add a `[3, then 1] → 1` ordering case for symmetric coverage. Not blocking. |

---

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source code?** All load-bearing
   ones: EventType count (runtime `len(EventType)==37`), the `min`+None-guard fold
   (`run_log.py:190-194`), the JSONL-rebuild path (`run_log.py:135-216`), `record_idempotent`
   dedup (`run_log.py:226-245`), `IDEMPOTENCY_SETS` cardinality 6 (`run_log.py:27-34`), the
   `load_fixture` fixture (`conftest.py:20-27`), and `decline-twice.json` contents. Plus **5
   source mutations** executed and reverted, each empirically confirming a test fails under the
   inverse implementation.
2. **Specific files read:** `src/superclaude/pr_submit/run_log.py`,
   `src/superclaude/pr_submit/models.py`, `tests/pr_submit/test_run_log.py`,
   `tests/pr_submit/test_idempotency.py`, `tests/pr_submit/conftest.py`,
   `tests/pr_submit/fixtures/decline-twice.json`.
3. **If 0 issues, why trust the check?** I did NOT report 0 — I found 1 MINOR partial-vacuity
   + 2 lower-tier observations. More importantly, the trust here rests on **execution evidence,
   not inspection**: 5 mutations, 5 catches, with literal pytest failure output quoted
   (`assert 3 == 1`, `assert 36 == 37`, `assert 55 in []`, `assert True is False`,
   `TypeError ... NoneType`). A reader can re-run the same mutations.
4. **Web research?** None performed; no external lookup required (all checks are local-source
   bound). Tavily-first precedence therefore not triggered.

**Source-restoration integrity:** after every mutation I restored from `/tmp` backups and
verified `diff -q` shows the live `run_log.py` and `models.py` are byte-identical to their
pre-mutation state, and re-ran all 4 target tests green. Nothing was left modified
(fix_authorization: false honored).

---

## Confidence Gate

- **Confidence:** Verified: 4/4 target tests | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- **Tool engagement:** Read: 6 | Grep: 4 | Glob: 0 | Bash: 7 (5 mutation runs + 1 baseline run + 1 restore-verify)
- Tool calls (≈17) exceed the 4-item checklist minimum; each Bash mutation directly tested one
  specific non-vacuity claim.

---

## Recommendations
- **Non-blocking:** address Issue #1 (t1124 fixture either exercised or docstring softened)
  in a follow-up; the four core Phase-4 guarantees (INV-R3 monotone-min, 37-member closed
  enum, INV-R2 strict-once across resume, at-most-once within run) are all genuinely guarded.
- Optionally tighten Issues #2/#3 for symmetric/rename coverage; both are completeness nits,
  not correctness gaps.

## QA Complete

VERDICT: PASS
