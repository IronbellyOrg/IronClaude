# QA Report — FINAL-PHASE M3 crossref-chain lens (pr_submit V1.1)

**Topic:** pr_submit V1.1 complete change-set — §9 FR→INV→AC→test coverage matrix
**Date:** 2026-06-12
**Phase:** task-qualitative (crossref-chain lens; FINAL completeness check before M4 fidelity gate)
**Fix cycle:** N/A (fix_authorization: false — report only)
**Lens stance:** ADVERSARIAL — assume ≥5 broken FR→test chains; verified by READING + grep + test run.

---

## Overall Verdict: FAIL

The whole §9 matrix is **not** satisfiable as written. Every IMPLEMENTING SYMBOL exists and
all 69 V1.1 tests pass — but **four matrix T-IDs are phantom** (no real test carries the ID
anywhere in the suite), and one of those (T-1117) is backed by **no implementing behavior at
all** (FR-9.5 review-wins arbiter is unimplemented). A push with the matrix taken at face value
would report green coverage for chains that do not exist.

---

## Method (tool engagement)

- **Read** (11): `06-spec-delta-extraction.md` (§9 matrix), all 7 test files, `fsm.py`,
  `classifier.py`, `detection.py`; targeted `sed` reads of `models.py`, `run_log.py`.
- **Grep** (8): every matrix T-ID across `tests/pr_submit/`; repo-wide search for the 4 suspects;
  arbiter search; symbol confirmations in `models.py`/`run_log.py`.
- **Bash** (1): `uv run pytest` over the 7 V1.1 files → **69 passed**.

Confidence: Verified: 31/31 chains traced | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
Tool engagement: Read: 11 | Grep: 8 | Bash: 2 | Glob: 0

---

## FR → symbol → test chain trace (every sub-ID)

Legend: SYM = implementing symbol (real, cited); TST = matrix-named test (real + passing?).

### FR-8 (R1, re-trigger) — all chains REAL

| FR | SYM (file:line) | matrix test | TST real+pass? |
|----|-----------------|-------------|----------------|
| FR-8.1 | `run_skill` S5a post `fsm.py:964-970`; transition edge `fsm.py:622-630` | T-1101 | YES `test_review_retrigger.py:40` + static `test_static_grep.py:210` |
| FR-8.2 | relocated tick `fsm.py:998-1001`; optimistic site REMOVED (no `+=1` post-resolve) | T-1102, T-PUSH-WITHOUT-REREVIEW-NO-TICK | YES `:58`, `:77` |
| FR-8.3 | `rereview_request_count` increment `fsm.py:970`; bound via `should_halt_rounds` | T-1103 | YES `:97` |
| FR-8.4 | outcome `"attributed"` gate `fsm.py:982-1001` | T-1104 | YES `:115` |
| FR-8.5 | token absent from core; lives in `retrigger-review.sh` | T-1105 | YES `:131` + `test_static_grep.py:230` |
| FR-8.6 | S5a skip when `applied_edits == 0` `fsm.py:964` | T-1106 | YES `:146` |

### FR-9 (R2, decline + fallback) — TWO BROKEN CHAINS

| FR | SYM (file:line) | matrix test | TST real+pass? |
|----|-----------------|-------------|----------------|
| FR-9.1 | `is_decline` `classifier.py:65-97`; `STATE_DECLINED` `:24`; decline-FIRST `classifier.py:127-129` | T-1110, T-1111, T-1112 | YES `test_detection_contract.py:193`, `:254`, `:275` |
| FR-9.2 | `(S2_CLASSIFY,"declined")` `fsm.py:640-642`; `(S5_AWAITING_REREVIEW,"declined")` `fsm.py:635-639`; initial-poll `fsm.py:876-881` | T-1113, **T-1113b** | T-1113 YES `test_auggie_fallback.py:71`. **T-1113b PHANTOM — no test carries the ID** |
| FR-9.3 | `invoke_auggie_review` seam `fsm.py:763-765` (core decides; SKILL invokes) | **T-1114**, T-1115 | **T-1114 PHANTOM — no test carries the ID**. T-1115 YES `test_static_grep.py:246` |
| FR-9.4 | verify-before-remediate on fallback findings `fsm.py:778-785` | **T-1116** | **T-1116 PHANTOM — no test carries the ID.** Behavior covered un-named by `test_fallback_findings_pass_verify_before_remediate` `:206` |
| FR-9.5 | watermark in `is_decline` `classifier.py:93-96` (stale-decline half only) | T-1117, T-1118 | T-1118 YES `test_detection_contract.py:312`. **T-1117 PHANTOM AND UNIMPLEMENTED — no review-wins arbiter exists** |

### FR-10 (R3, strict-once + clamp) — all chains REAL

| FR | SYM (file:line) | matrix test | TST real+pass? |
|----|-----------------|-------------|----------------|
| FR-10.1 | 6th set `IDEMPOTENCY_SETS` `run_log.py:33`; strict-once guard `fsm.py:763-765` | T-1120, T-AUGGIE-AT-MOST-ONCE | YES `test_idempotency.py:83`, `test_auggie_fallback.py:92` |
| FR-10.2 | `clamp_max_rounds` `fsm.py:145-153`; recorded once `fsm.py:754-760` | T-1121 | YES (clamp asserted by `test_t1122…:130` + `test_t1121…:188` push-bound) |
| FR-10.3 | `fallback_round_counter` cap-1 `fsm.py:768-770`; no loop-back | T-1122, T-1123 | YES `:130`, `:144` |
| FR-10.4 | `rebuild_state` fold `run_log.py:178-182` survives resume | T-1124 | YES `test_idempotency.py:103` |
| FR-10.5 | push-bound `push_count <= max_rounds+1` (one fallback push `fsm.py:822-824`) | T-1125 | YES `test_auggie_fallback.py:167` |

### INV → symbol → test

| INV | SYM (file:line) | matrix test | real+pass? |
|-----|-----------------|-------------|------------|
| INV-R1 (re-trigger boundedness) | `fsm.py:964-970`; monotone-min fold `run_log.py:174-176` | T-1103, EC-17/18 | YES `test_review_retrigger.py:97`, `test_loop_guard.py:175` |
| INV-R2 (auggie strict-once + push bound) | `fsm.py:763-765`, `:822-824` | T-AUGGIE-AT-MOST-ONCE, T-1125 | YES |
| INV-R3 (clamp monotonicity) | `clamp_max_rounds` `fsm.py:145-153`; min-fold `run_log.py:188-193` | T-1121, T-1122 | YES (min-fold `test_run_log.py:192`, counters-independent `test_loop_guard.py:190`) |
| INV-001 (verbatim preserved) | single tick site `fsm.py:998-1001`; `>=` gate `loop_guard.should_halt` | T-626-OFF-BY-ONE et al. | YES `test_loop_guard.py:45` |

### AC → test

| AC | matrix test | real+pass? |
|----|-------------|------------|
| AC-16 | T-1101, T-1104 | YES |
| AC-17 | T-PUSH-WITHOUT-REREVIEW-NO-TICK | YES |
| AC-18 | T-1103 | YES |
| AC-19 | T-1111, T-1112, T-1113, **T-1113b** | PARTIAL — **T-1113b phantom** |
| AC-20 | **T-1114**, **T-1116** | **BROKEN — BOTH cited tests are phantom** |
| AC-21 (HARD) | T-AUGGIE-AT-MOST-ONCE, T-1124, T-1125, T-1122 | YES |

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | FR-8.1..8.6 chains real | none | PASS | all 6 SYM+TST cited above; 7/7 retrigger tests pass |
| 2 | FR-9.1 decline classify | none | PASS | `classifier.py:65-129`; 3 tests pass |
| 3 | FR-9.2 → T-1113b real | AX-5 | FAIL | T-1113b absent from suite (grep: only `T-1110b` exists) |
| 4 | FR-9.3 → T-1114 real | AX-5 | FAIL | T-1114 absent from suite |
| 5 | FR-9.4 → T-1116 real | AX-5 | FAIL | T-1116 absent; behavior present but test un-named |
| 6 | FR-9.5 → T-1117 real + implemented | AX-3 | FAIL | T-1117 absent AND no review-wins arbiter in `fsm.py`/`classifier.py` |
| 7 | FR-10.1..10.5 chains real | none | PASS | all 5 SYM+TST cited; idempotency/clamp tests pass |
| 8 | INV-R1/R2/R3 + INV-001 symbols | none | PASS | symbols cited; monotone folds verified |
| 9 | AC-16..21 → test | AX-3 | FAIL | AC-19 partial, AC-20 fully phantom (T-1114+T-1116) |
| 10 | All implementing SYMBOLs exist | none | PASS | models/classifier/detection/run_log/fsm all confirmed by read |
| 11 | 69 tests actually pass | none | PASS | `uv run pytest` → 69 passed |

(Axis column per task-qualitative phase: closed set {AX-1..AX-5, none}.)

## Summary
- Chains traced: 31 (18 FR + 4 INV + 6 AC + 3 structural)
- Chains PASS: 26 | Chains FAIL: 5
- CRITICAL: 1 | IMPORTANT: 3 | MINOR: 1
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | matrix §8 `FR-9.5 → T-1117`; `fsm.py:982-996`, `classifier.py:127-129` | **FR-9.5 "review wins over decline" is half-built.** Matrix names T-1117 (EC-22: re-review AND decline in same poll → review wins). No test T-1117 exists, AND no implementing arbiter exists: `run_skill` consumes a single pre-resolved `rereview_outcome` token (cannot model both-present), and `classifier.py` implements the OPPOSITE precedence (decline-FIRST over findings). The watermark half (T-1118) is real; the review-wins half is absent. Phantom coverage on a HARD race requirement. | Implement an S5 arbiter: when an attributed re-review AND a watermarked decline co-occur, the re-review wins (route to S2_CLASSIFY, tick round_counter), decline ignored. Add a real `test_t1117_review_wins_over_cooccurring_decline` that feeds BOTH and asserts `round_counter` advanced + `fallback_engaged is False`. Then the matrix chain is real. |
| 2 | IMPORTANT | matrix §8 `FR-9.3 → T-1114`; AC-20 | **T-1114 phantom.** No test carries the ID. The core decide-to-invoke behavior IS exercised (by T-AUGGIE-AT-MOST-ONCE's `calls` recorder, `test_auggie_fallback.py:92-126`), so this is a naming/matrix gap, not a behavior gap — but AC-20 cites T-1114 as one of its two verifications, so AC-20's evidence trail is broken. | Either rename/add a `test_t1114_*` asserting the single core invoke decision, or correct the matrix + AC-20 to cite T-AUGGIE-AT-MOST-ONCE (`:92`). Matrix↔test must be bijective. |
| 3 | IMPORTANT | matrix §8 `FR-9.4 → T-1116`; AC-20 | **T-1116 phantom.** Behavior is real and covered by `test_fallback_findings_pass_verify_before_remediate` (`test_auggie_fallback.py:206`, non-vacuous: all-unverified → `push_count==0`, `TERMINAL_CLEAN`), but that test carries no T-1116 ID. AC-20's second verification thus points at a non-existent ID. | Add the `T-1116` ID to that test's name/docstring (or update matrix + AC-20 to cite `test_fallback_findings_pass_verify_before_remediate`). |
| 4 | IMPORTANT | matrix §8 `FR-9.2 → T-1113b`; AC-19; EC-19 | **T-1113b phantom.** No test carries `T-1113b`. The "decline at initial S2 poll" behavior IS covered by real tests — `test_t1110b_decline_from_initial_poll` (`test_detection_contract.py:203`, classifier half) and `test_t1110_decline_at_initial_poll_routes_to_fallback` (`test_auggie_fallback.py:55`, FSM half) — but under DIFFERENT IDs (T-1110b / unlabeled). AC-19 and EC-19 both cite T-1113b. | Reconcile IDs: either rename one initial-poll test to T-1113b, or update matrix/AC-19/EC-19 to cite T-1110b + the FSM test. |
| 5 | MINOR | matrix §8 internal `T-ID` consistency | Matrix maps `FR-10.2 → T-1121` (clamp) but the test named `test_t1121_*` (`:188`) asserts the **push-bound** (FR-10.5/INV-R2), while the **clamp** is asserted by `test_t1122_clamp_to_one*` (`:130`). The FR-10.2 / FR-10.5 ↔ T-1121 / T-1125 / T-1122 labels are internally scrambled vs the test names. Behavior for both is covered; only the ID↔intent mapping drifts. | Re-align matrix rows FR-10.2/10.3/10.5 with the actual `test_t112x` names so each cited ID asserts the FR it is mapped to. |

## Actions Taken
None — fix_authorization: false. All findings documented; no files modified.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` block was supplied in the spawn prompt (standalone
crossref-chain lens). Fell back to independent verification: every chain link was traced by
reading the actual symbol AND grepping/running the actual test. No rf-qa PASS items were relied
upon; all 31 chains independently verified with tool evidence (Read + Grep + a full pytest run).

## Recommendations
1. **Issue #1 is the blocking one for M4 fidelity:** FR-9.5's review-wins arbiter is a genuine
   capability gap, not just a label gap. The matrix claims a chain that the code cannot satisfy.
   Build the arbiter + T-1117, or the §9 matrix overstates coverage of a HARD requirement.
2. Issues #2–#4 are matrix↔test bijection breaks (behavior present, IDs phantom). They will make
   the M4 phantom-coverage detector (I21) fire: each cited T-ID must resolve to a real test. Add
   the four IDs (T-1113b, T-1114, T-1116) and reconcile T-1117 before the fidelity gate.
3. Issue #5 (FR-10.x label scramble) is cosmetic but will confuse the next reader of the matrix.

VERDICT: FAIL
