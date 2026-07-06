# QA Report — M4 Source-Document Fidelity Gate (Phase 7 Gate B), Agent 2

**Agent:** FIDELITY-AGENT-2
**Phase:** report-validation / source-fidelity (M4, I21 phantom-coverage detection)
**Assigned scope:** addendum §7-§10 — EC-17..24, AC-16..21, §9 FR→T-ID coverage matrix, §10 preserved constraints
**fix_authorization:** false (verify only)
**Date:** 2026-06-12

---

## Overall Verdict: PASS

Every T-ID in the addendum §9 coverage matrix resolves to a **REAL, collected, passing,
behavior-asserting test** — not a matrix-only row, not a vacuous stub. The full
`tests/pr_submit/` suite collects and passes **176 / 176** (`uv run pytest tests/pr_submit/ -q`,
0 skipped, 0 collection errors). All three prior-gate-flagged items (T-1117, T-1113b,
T-1114/T-1116) now exist and assert their FR/EC/AC behavior. The three V1.1 ref/script
surfaces referenced by the static tests all exist.

One **MINOR (non-blocking) label transposition** found between T-1121 and T-1122 docstrings
vs the §9 matrix's FR mapping — both behaviors are fully tested, so it is a cosmetic
labeling note, not a coverage gap. Documented below.

---

## Phantom-Coverage Detection — per-T-ID matrix verification

Method: `grep -rn "<T-ID>" tests/pr_submit/` for every matrix T-ID, then `Read` the test
body to confirm it ASSERTS the FR/EC/AC behavior (non-vacuous), then ran the suite to
confirm collection + pass.

| Matrix T-ID | Maps to | Real? | Test file:line (the `def`/docstring) | Asserts behavior |
|---|---|---|---|---|
| T-1101 | FR-8.1, AC-16, EC-17 | REAL | test_review_retrigger.py:40 + test_static_grep.py:210 | exactly one re-trigger per push (`len(retriggers)==1`); gh fork-pinned |
| T-1102 | FR-8.2 | REAL | test_review_retrigger.py:58 | deferred increment ticks on `"attributed"` (`round_counter==1`) |
| T-1103 | FR-8.3, AC-18, INV-R1 | REAL | test_review_retrigger.py:98 | `rereview_request_count <= max_rounds(2)` |
| T-1104 | FR-8.4, AC-16, EC-17 | REAL | test_review_retrigger.py:115 | attributed re-review advances cycle (`round_counter==2`) |
| T-1105 | FR-8.5 | REAL | test_review_retrigger.py:131 + test_static_grep.py:230 | core fsm.py holds NO `auggie review` literal; token in script |
| T-1106 | FR-8.6 | REAL | test_review_retrigger.py:146 | S5a skipped when `applied_edits==0` (no push, no re-trigger) |
| T-PUSH-WITHOUT-REREVIEW-NO-TICK | FR-8.2, AC-17, EC-18 | REAL | test_review_retrigger.py:77 | push w/ `"timeout"` → `push_count==1` but `round_counter==0` |
| T-1110 | FR-9.1 | REAL | test_detection_contract.py:193 (+204, +210) | Augment decline (both regexes) → `"declined"` |
| T-1111 | FR-9.1, AC-19 | REAL | test_detection_contract.py:254 | "abnormally large" only (no re-trigger) → NOT decline |
| T-1112 | FR-9.1, AC-19 | REAL | test_detection_contract.py:275 (+296) | re-trigger w/o phrase → NOT decline; non-Augment → NOT decline |
| T-1113 | FR-9.2, AC-19, EC-20 | REAL | test_auggie_fallback.py:73 | decline at S5 poll → fallback; `round_counter==0` frozen |
| T-1113b | FR-9.2, AC-19, EC-19 | REAL | test_auggie_fallback.py:56 | decline at INITIAL S2 poll → fallback (FLAGGED — now resolves) |
| T-1114 | FR-9.3, AC-20 | REAL | test_auggie_fallback.py:94 | fallback INVOKES auggie-review exactly once (FLAGGED — now resolves) |
| T-1115 | FR-9.3 | REAL | test_static_grep.py:246 | byte-exact flag-parity vs auggie-review.md option table |
| T-1116 | FR-9.4, AC-20, EC | REAL | test_auggie_fallback.py:209 | fallback findings re-enter verify-before-remediate (FLAGGED — now resolves) |
| T-1117 | FR-9.5, AC, EC-22 | REAL | test_detection_contract.py:328 | attributed re-review WINS over co-occurring decline (FLAGGED — now exists) |
| T-1118 | FR-9.5, EC-23 | REAL | test_detection_contract.py:313 | stale pre-watermark decline ignored; None watermark accepted |
| T-1120 | FR-10.1, AC-21 | REAL | test_idempotency.py:83 | 6th set; record→True first, False on replay; one `idempotency_skip` |
| T-1121 | FR-10.2 (matrix) | REAL* | test_auggie_fallback.py:191 | asserts `push_count <= max_rounds+1` (see label note) |
| T-1122 | FR-10.3, INV-R3, AC-21 | REAL* | test_auggie_fallback.py:133 | asserts `effective_max_rounds==1` clamp (see label note) |
| T-1123 | FR-10.3 | REAL | test_auggie_fallback.py:147 | single-shot: `fallback_round_counter==1`, one invoke, terminates |
| T-1124 | FR-10.4, AC-21, EC-24 | REAL | test_idempotency.py:103 | strict-once survives resume (rebuild_state folds once) |
| T-1125 | FR-10.5, AC-21, INV-R3 | REAL | test_auggie_fallback.py:171 | `round_counter` frozen at 1; `fallback_round_counter==1` independent |
| T-AUGGIE-AT-MOST-ONCE | FR-10.1, AC-21, INV-R2, EC-21 | REAL | test_idempotency.py:83 + test_auggie_fallback.py:94 | non-vacuous double-entry: 2 declines → invoke fires exactly once |
| T-N50 | §10 NFR-6 / AC-9 | REAL | test_static_grep.py:110 | core-pure file set has ZERO gh/git tokens |

\* See "Issues Found" — T-1121/T-1122 docstring↔matrix FR-label transposition (cosmetic).

**Phantom count: 0.** No matrix T-ID is a row without a backing test.

---

## EC-17..24 coverage (via mapped T-IDs)

| EC | Mapped T-ID(s) | Status |
|---|---|---|
| EC-17 | T-1101, T-1104 | COVERED (both real) |
| EC-18 | T-PUSH-WITHOUT-REREVIEW-NO-TICK | COVERED (named in test_review_retrigger.py:78) |
| EC-19 | T-1113b, T-AUGGIE-AT-MOST-ONCE | COVERED (named in test_auggie_fallback.py:57) |
| EC-20 | T-1113, T-1122 | COVERED (both real) |
| EC-21 | T-AUGGIE-AT-MOST-ONCE | COVERED (non-vacuous double-decline) |
| EC-22 | T-1117 | COVERED (named in test_detection_contract.py:329) |
| EC-23 | T-1118 | COVERED (named in test_detection_contract.py:313) |
| EC-24 | T-1124 | COVERED (resume strict-once) |

All 8 ECs map to real tests. (EC labels are sparsely cited by name in docstrings — EC-17/20/21/24
are covered transitively through their mapped T-IDs, which is the matrix's contract.)

## AC-16..21 coverage (via mapped T-IDs)

| AC | Mapped T-ID(s) | Status |
|---|---|---|
| AC-16 | T-1101, T-1104 | COVERED |
| AC-17 | T-PUSH-WITHOUT-REREVIEW-NO-TICK | COVERED |
| AC-18 | T-1103 | COVERED |
| AC-19 | T-1111, T-1112, T-1113, T-1113b | COVERED |
| AC-20 | T-1114, T-1116 | COVERED |
| AC-21 (HARD) | T-AUGGIE-AT-MOST-ONCE, T-1124, T-1125, T-1122 | COVERED |

All 6 ACs map to real, passing tests. AC labels are not cited verbatim in test code, but
every backing T-ID is verified real — fidelity holds at the T-ID granularity the matrix defines.

---

## §10 Preserved-constraints spot-check

- **NFR-6 core purity (no gh/git in core):** T-N50 (test_static_grep.py:110) REAL — scans the
  core-pure set for zero gh/git tokens. Re-trigger gh surfaces correctly excluded to the
  fork-pin path (T-1101 static, test_static_grep.py:210). PASS.
- **INV-001 verbatim:** transition() S5→S2-on-attributed edge asserted byte-identical
  (test_auggie_fallback.py:243); deferred increment relocated, ticks only on `"attributed"`
  (T-1102, T-PUSH-...NO-TICK). PASS.
- **6th idempotency set follows existing pattern:** `len(IDEMPOTENCY_SETS)==6` + record/rebuild
  pattern (T-1120). PASS.
- **Two independent monotone counters / no loop-back:** T-1125 (frozen round_counter) +
  T-1123 (single-shot, terminates). PASS.

---

## Prior-gate flagged items — re-check

| Item | Prior status | Now | Evidence |
|---|---|---|---|
| T-1117 (FR-9.5 review-wins) | flagged "should now exist" | EXISTS, REAL | test_detection_contract.py:328 — asserts review>decline both findings & clean cases |
| T-1113b | flagged "should resolve" | RESOLVES, REAL | test_auggie_fallback.py:56 — initial-S2-poll decline → fallback |
| T-1114 | flagged "should resolve" | RESOLVES, REAL | test_auggie_fallback.py:94 — non-vacuous exactly-once invoke |
| T-1116 | flagged "should resolve" | RESOLVES, REAL | test_auggie_fallback.py:209 — unverified fallback finding dropped, no push |

All four prior flags are cleared.

---

## Issues Found

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| 1 | MINOR (non-blocking) | test_auggie_fallback.py:133 (T-1122) & :191 (T-1121) | Docstring↔matrix FR-label transposition. §9 matrix maps T-1121→FR-10.2 (clamp/`max_rounds_clamped`) and T-1122→FR-10.3 (single-shot/freeze). In the test file, T-1121's body asserts the **push-bound** (`push_count <= max_rounds+1`, an INV-R2/FR-10.5 property) and T-1122's body asserts the **clamp** (`effective_max_rounds==1`, the FR-10.2 property). The two test labels are swapped relative to the matrix's FR assignment. | No behavior gap — both the clamp and the push-bound are asserted by real tests (just under transposed T-IDs). Optional: swap the two docstring labels (or the matrix rows) so T-1121↔clamp / T-1122↔single-shot align. Verify-only gate: documented, not fixed (`fix_authorization:false`). |

No CRITICAL or IMPORTANT issues. No phantom coverage. No missing tests.

---

## Confidence

**Verified: 26/26 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**

(26 matrix T-IDs, all confirmed real via grep + body Read + suite execution. EC-17..24 and
AC-16..21 verified transitively through their mapped T-IDs per the matrix contract.)

**Tool engagement:** Read: 5 | Grep: 3 | Glob: 0 | Bash: 4

No web research performed (external lookup not required; gate is source-truth-local).

---

## QA Complete

VERDICT: PASS
