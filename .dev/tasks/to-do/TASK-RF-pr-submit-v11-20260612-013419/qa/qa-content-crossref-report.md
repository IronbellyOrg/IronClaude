# QA Report — Phase 3 Crossref-Chain Lens (pr_submit V1.1)

**Topic:** pr_submit V1.1 — FR→implementation→test chain integrity
**Date:** 2026-06-12
**Lens:** crossref-chain (content)
**Stance:** Adversarial. fix_authorization: false (report only — nothing modified).

---

## Overall Verdict: FAIL

**Reason:** The two chains I was assigned to trace (FR-9.1 decline, EC-23 watermark) are
**fully intact and live** (14/14 detection-contract tests pass). BUT the explicit secondary
mandate — "verify no Phase-3-scope FR sub-ID is left WITHOUT a verifying test" — surfaces
**massive coverage gaps**: 17 of 21 Phase-3 T-IDs in the §8 coverage matrix have NO
implementing test anywhere in `tests/`, plus a matrix↔test ID-mapping defect. A coverage
matrix that asserts rows backed by tests which do not exist is exactly the phantom-coverage
failure mode the lens exists to catch.

---

## Assigned Chain 1 — FR-9.1 (decline classified, decline-first ordering): PASS

| Link | Location | Evidence |
|------|----------|----------|
| FR-9.1 spec row | `research/06-spec-delta-extraction.md:104` | "`classify()` gains a 4th state `declined` … BOTH `decline_phrase_regex` AND `decline_retrigger_regex` … Test: T-1110, T-1111, T-1112" |
| `STATE_DECLINED` const | `classifier.py:24` | `STATE_DECLINED = "declined"` |
| Decline-first ordering | `classifier.py:124-129` | decline loop runs BEFORE the `if not augment_reviews` polling branch (`classifier.py:131`) and the findings branch (`classifier.py:138`) — a decline is never miscounted as findings/polling |
| `is_decline` predicate (both-regex AND) | `classifier.py:65-97` | phrase regex `classifier.py:89`, retrigger regex `classifier.py:91`; both `re.search` must pass |
| T-1110 (both regexes → declined) | `test_detection_contract.py:192-199` | asserts `classify(...) == "declined"` AND `is_decline(...) is True` via `decline-comment.json` |
| T-1111 (phrase only → NOT decline) | `test_detection_contract.py:209-227` | `is_decline(...) is False`, state stays `"polling"` |
| T-1112 (retrigger only → NOT decline) | `test_detection_contract.py:230-248` | `is_decline(...) is False`, state stays `"polling"` |
| Fixture `decline-comment.json` | `fixtures/decline-comment.json` | real Augment-authored body matching both regexes, `expected.state == "declined"` |

**Live verification:** `uv run pytest tests/pr_submit/test_detection_contract.py -q` → **14 passed**.
The three T-IDs assert the actual FR-9.1 behavior (not stubs): T-1110 exercises the positive
path, T-1111/T-1112 guard each half of the AND. Chain INTACT.

---

## Assigned Chain 2 — EC-23 (stale pre-watermark decline ignored): PASS (with an ID-mapping defect, below)

| Link | Location | Evidence |
|------|----------|----------|
| EC-23 spec row | `research/06-spec-delta-extraction.md:208` | "Stale decline (pre-watermark) at `S5` → ignored; keep polling → Test: T-1118" |
| Watermark comparison in `is_decline` | `classifier.py:93-96` | `if watermark is not None: created = …; if created is None or not (created > watermark): return False` — strict-newer gate |
| Watermark threaded through `classify` | `classifier.py:100,114-115,128` | keyword-only `watermark` passed into `is_decline` |
| EC-23 test | `test_detection_contract.py:268-280` (`test_ec23_stale_pre_watermark_decline_ignored`) | with watermark → `is_decline(...) is False` and `classify(...) != "declined"`; with `None` → `is_decline(...) is True` and `classify(...) == "declined"` |
| Fixture `stale-decline-pre-watermark.json` | `fixtures/stale-decline-pre-watermark.json` | `createdAt 08:00:00Z` < `watermark 09:30:00Z`; `expected.is_decline_with_watermark: false`, `state_without_watermark: "declined"` |

**The behavior is correct and tested both directions** (watermark active → ignored; watermark
None → accepted). Chain INTACT. However the **T-ID label is broken** — see Issue #2.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | `research/…/06-spec-delta-extraction.md:228-238` (§8 matrix) vs `tests/pr_submit/` | **17 of 21 Phase-3 matrix T-IDs have NO implementing test anywhere in `tests/`.** Missing: T-1101, T-1102, T-1103, T-1104, T-1105, T-1106, T-1113, T-1114, T-1115, T-1116, T-1117, T-1118, T-1120, T-1121, T-1122, T-1123, T-1124, T-1125, plus named T-PUSH-WITHOUT-REREVIEW-NO-TICK and T-AUGGIE-AT-MOST-ONCE. The matrix asserts these rows; `grep -rn` across `tests/` returns zero hits for each. The two NEW test files §8.1 promises (`test_review_retrigger.py`, `test_auggie_fallback.py`) and four fixtures (`rereview-attributed.json`, `rereview-then-decline.json`, `decline-twice.json`, `auggie-fallback-findings.json`) do NOT exist. This is phantom coverage: every matrix row whose T-ID has no real test is unbacked. | Either (a) build the Phase-3 FSM/SKILL/run_log work + these test files so each matrix T-ID resolves to a real assertion, OR (b) if this lens runs mid-Phase-3 with only the classifier slice built, the matrix must be annotated to scope which rows are landed vs pending so it does not over-claim. A matrix row without a real implementing test is a contract violation regardless. |
| 2 | IMPORTANT | `06-spec-delta-extraction.md:208,234` vs `test_detection_contract.py:269` | **EC-23 / T-1118 ID-mapping defect.** §6 EC table (line 208) and §8 matrix (line 234, `FR-9.5 → T-1117, T-1118`) name the stale-decline test **T-1118**. The actual test is named `test_ec23_stale_pre_watermark_decline_ignored` and carries **no T-1118 marker** — `grep -rn "T-1118\|t1118" tests/` returns nothing. The behavior IS implemented and IS tested, but it is filed under the EC-ID `ec23`, not the matrix's T-ID `T-1118`. A phantom-coverage auditor keying on the matrix T-ID would mark FR-9.5's T-1118 as uncovered. | Add the `T-1118` token to the test docstring/name (e.g. `T-1118 / EC-23`) so the matrix row resolves, OR correct the matrix to map FR-9.5/EC-23 → `test_ec23_…`. Pick one canonical ID and make matrix + test agree. |
| 3 | IMPORTANT | `06-spec-delta-extraction.md:234` (`FR-9.5 → T-1117, T-1118`) | **T-1117 (review-wins-over-decline race) has no test and is NOT classifier-scope.** FR-9.5 (line 108) requires a genuine attributed re-review to WIN over a same-window decline at `S5_AWAITING_REREVIEW`. That tiebreak is FSM poll-window logic (fsm.py `S5`), not `classify()`. The classifier supplies only the watermark half (T-1118/EC-23). T-1117 has zero test and zero implementation. So even the "decline" FR family is only HALF covered by the landed classifier slice — FR-9.5's review-wins half is entirely absent. | Build the `S5` race-resolution edge in fsm.py and T-1117 (review present + decline present in one poll → proceed as attributed re-review, EC-22). Until then FR-9.5 is a partially-broken chain: predicate exists, ordering arbiter does not. |
| 4 | MINOR | `test_detection_contract.py:202-206` (`test_t1110b…`) & `:252-265` (`test_t1112b…`) | **Two real tests carry T-IDs absent from the matrix** (`T-1110b` decline-from-initial-poll, `T-1112b` non-Augment-author-ignored). `grep` of §8 matrix for `1110b`/`1112b` → none. These are GOOD extra tests (T-1110b duplicates the FR-9.2 "decline before any push" intent the matrix files under T-1113b; T-1112b is a T-211 sibling) but they are orphaned from the coverage matrix — the reverse of phantom coverage (test exists, matrix row doesn't). | Add T-1110b / T-1112b rows to the matrix (or fold T-1110b under the FR-9.2 / T-1113b decline-at-initial-poll row it actually satisfies) so matrix↔test is bijective. |

---

## Phantom-coverage sweep — every Phase-3 matrix T-ID

`grep -rln "t<id>\|T-<id>" tests/` across the full `tests/` tree:

```
LANDED (real test, assigned-chain scope):
  T-1110  → test_detection_contract.py:192   (FR-9.1)  REAL
  T-1111  → test_detection_contract.py:209   (FR-9.1)  REAL
  T-1112  → test_detection_contract.py:230   (FR-9.1)  REAL
  EC-23   → test_detection_contract.py:268   (watermark) REAL — but labeled ec23, not T-1118 (Issue #2)

MISSING (matrix asserts, no test exists anywhere):
  T-1101 T-1102 T-1103 T-1104 T-1105 T-1106     (FR-8.* re-trigger — fsm/skill scope)
  T-1113 T-1114 T-1115 T-1116 T-1117 T-1118     (FR-9.2..9.5 fallback/route/race)
  T-1120 T-1121 T-1122 T-1123 T-1124 T-1125     (FR-10.* strict-once/clamp/resume)
  T-PUSH-WITHOUT-REREVIEW-NO-TICK               (FR-8.2 / AC-17 — the headline V1.0 bug)
  T-AUGGIE-AT-MOST-ONCE                         (FR-10.1 / AC-21 HARD safety constraint)

ORPHAN (test exists, no matrix row):
  T-1110b → test_detection_contract.py:202
  T-1112b → test_detection_contract.py:252
```

**Within my two assigned chains: both PASS.** The FAIL verdict is driven entirely by the
secondary mandate (no Phase-3 FR sub-ID without a verifying test) — which 17 T-IDs violate.
If this lens is scoped ONLY to the landed classifier slice, escalate Issue #1 to the
orchestrator for a scope ruling; the matrix still over-claims as written.

---

## Self-Audit

**(a) Reliance list — structural items I did NOT re-derive:**
- Relied on the matrix's transcription of FR text being verbatim (§3 claims "TRANSCRIBED verbatim"); I did not re-open the addendum spec — out of crossref-chain scope.

**(b) Independent semantic checks (tool-verified, ≥1 required):**
- Decline-first ORDERING is real, not just present — read `classifier.py:124-142` and confirmed the decline loop precedes both the polling return (`:131`) and findings return (`:138`). rf-qa structural presence of `STATE_DECLINED` is insufficient; I verified the control-flow position that makes FR-9.1 "checked FIRST" true.
- Watermark gate is strict-newer and bidirectional — read `classifier.py:93-96` (`not (created > watermark)`) and cross-checked against `stale-decline-pre-watermark.json` timestamps (08:00 < 09:30) + the test's both-direction assertions (`:276-280`). Verified the EC-23 behavior, not just the param's existence.
- Tests are not stubs — ran `uv run pytest tests/pr_submit/test_detection_contract.py -q` → 14 passed; T-1110/1111/1112/ec23 assert real `classify`/`is_decline` returns, not placeholders.
- Missing-test claims are grep-verified — looped all 21 Phase-3 T-IDs through `grep -rln` over `tests/`; confirmed file absence of `test_review_retrigger.py` / `test_auggie_fallback.py` and 4 fixtures via `ls`.

**Confidence:** Verified: 21/21 matrix T-IDs traced | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 3 | Grep/Bash: 8 | Glob: 0

---

## Recommendations

1. **Scope ruling needed (Issue #1):** confirm whether this lens runs on the full Phase-3 build
   or only the landed classifier slice. As-written, the §8 matrix over-claims 17 unbacked rows.
2. **Fix the T-1118 label (Issue #2)** so EC-23's real test resolves under the matrix's T-ID.
3. **FR-9.5 is half-built (Issue #3):** the review-wins-over-decline arbiter (T-1117) and its
   fixture do not exist — the decline FR family is not fully closed even within "detection."
4. **Reconcile orphan T-IDs (Issue #4)** T-1110b / T-1112b into the matrix.

VERDICT: FAIL
