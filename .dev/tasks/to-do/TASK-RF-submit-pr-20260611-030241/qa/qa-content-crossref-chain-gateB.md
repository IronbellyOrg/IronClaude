# QA Report — Content Lens (CROSSREF-CHAIN / TEST-COVERAGE) — Phase Gate B

**Topic:** sc:pr-submit test suite — spec→test→fixture coverage chain
**Date:** 2026-06-11
**Phase:** doc-qualitative (content lens, Phase Gate B)
**Fix cycle:** N/A (`fix_authorization: false` — report only)
**Lens:** CROSSREF-CHAIN / TEST-COVERAGE
**Adversarial stance:** ACTIVE (assumed ≥10 broken coverage links)

---

## Overall Verdict: FAIL

Suite executes green (131 passed) and the high-risk invariant surface is intact
(T-626-OFF-BY-ONE present + `@pytest.mark.p0`; T-N50 present; all FM-1..12, EC-1..16,
and every named R3 invariant test resolve). **But the spec §6.2 coverage matrix
contains broken chains: 3 spec-declared test IDs have no resolving test function, and
5 of the 18 fixtures are never loaded by any test (dead test data).** Per the
binary all-findings-must-resolve rule, this is a FAIL.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Suite green @ 131 passed | PASS | `uv run pytest tests/pr_submit/ -q` → `131 passed in 0.19s` |
| 2 | T-626-OFF-BY-ONE present + `@pytest.mark.p0` | PASS | `test_loop_guard.py:44` `@pytest.mark.p0`, `:45` `def test_t626_off_by_one_canonical`, `:46` docstring |
| 3 | T-N50 present (NFR-6/AC-9 core purity) | PASS | `test_static_grep.py:99` `def ... "T-N50: the core-pure file set contains ZERO gh/git tokens"` |
| 4 | T-VANISHED-MONO present (INV-001) | PASS | `test_loop_guard.py:93` |
| 5 | T-ZERO-EDIT-NO-PUSH (INV-016/FR-4.3/AC-2) | PASS | `test_autonomy_gates.py` |
| 6 | T-CRASH-WINDOW-NO-DOUBLE-PUSH (INV-007/AC-12) | PASS | `test_crash_recovery.py` |
| 7 | T-VALIDATED-NOT-VERIFIED (INV-015/AC-13) | PASS | `test_validated_not_verified.py` |
| 8 | T-FRESH-COMMENT-NO-DOUBLE-FIX (INV-009/NFR-1) | PASS | `test_idempotency.py` + `test_reply_resolve.py` |
| 9 | FM-1..12 all resolve | PASS | per-ID grep: all 12 ok |
| 10 | EC-1..16 all resolve | PASS | per-ID grep: all 16 ok |
| 11 | 18 fixtures present | PASS | `ls fixtures/` → 18 JSON (10 finding-* + 8 review/seq/crash/drift) |
| 12 | FR-1.3 chain (T-104, **T-105**) | **FAIL** | T-104 at `test_static_grep.py:87`; **T-105 NOT FOUND** anywhere |
| 13 | AC-7 chain (T-104, **T-105**) | **FAIL** | shares the missing T-105 |
| 14 | NFR-4 chain (T-N30, **T-N31**) | **FAIL** | T-N30 at `test_severity_router.py:59`; **T-N31 NOT FOUND** as a test ID |
| 15 | Every fixture referenced by ≥1 test | **FAIL** | 5 fixtures have ZERO references in any test (see Issues) |
| 16 | T-620..T-629 fence-post range | PASS (with note) | parametrized matrix covers 620–625 + 626-OFF-BY-ONE; 627/628/629 are range-label only, not distinct cases — acceptable, the AC-6 behavior (N→exactly N pushes) is fully exercised |

---

## Summary
- Checks passed: 13 / 16
- Checks failed: 3
- Critical issues: 0
- Important issues: 3 (one missing-test pair counts as the FR + AC chain it breaks)
- Total distinct findings: **8 broken links** (2 missing test IDs counted once each across their chains + 1 missing test ID + 5 orphan fixtures)
- Issues fixed in-place: 0 (report-only)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | spec §6.2 `FR-1.3 → T-104, T-105`; `AC-7 → T-104, T-105` | **T-105 has no resolving test function.** Grep across `tests/pr_submit/**/*.py` returns zero hits. FR-1.3 and AC-7 are both half-covered (only T-104 resolves, in `test_static_grep.py:87`). | Add `test_t105_*` to `test_skill_parse.py` (spec §6.3 layout assigns T-101..T-103, T-111..T-113 there and the FR-1.3 "choices" surface belongs with flag parsing), OR strike T-105 from the matrix if T-104 alone satisfies FR-1.3/AC-7. Do not leave the matrix asserting a test that does not exist. |
| 2 | IMPORTANT | spec §6.2 `NFR-4 → T-N30, T-N31`; spec §15.4 + §8 risk-row R9 also cite T-N31 | **T-N31 has no test function bearing that ID.** Spec describes it precisely (`github-actions[bot]` → ignored, stays "polling"). The *behavior* is covered (FM-4 `test_crash_recovery.py:67`, EC-10 `test_edge_cases.py:117`, both tagged NFR-4), but no test carries the `T-N31` ID the matrix + §15.4 + R9 reference. The chain is unresolvable by ID. | Either (a) add a `T-N31` non-Augment-bot stays-polling test to `test_detection_contract.py` (where T-211 already lives — the natural home), or (b) re-point the matrix/§15.4/R9 T-N31 references at the existing FM-4/EC-10 coverage. Currently three spec locations cite an ID with no test. |
| 3 | IMPORTANT | `fixtures/finding-empty.json` | **Orphan fixture — 0 references.** EC-1 (empty findings → clean) at `test_edge_cases.py:39` builds its data inline; never calls `load_fixture("finding-empty.json")`. | Wire EC-1 to load this fixture, or delete the fixture. Manifest claims "every fixture referenced" — this breaks it. |
| 4 | IMPORTANT | `fixtures/finding-malformed.json` | **Orphan fixture — 0 references.** EC-9 (malformed missing file:line → structural drop) at `test_edge_cases.py:106` builds data inline; fixture unused. | Wire EC-9 to the fixture, or delete it. |
| 5 | IMPORTANT | `fixtures/finding-max.json` | **Orphan fixture — 0 references.** This is the largest fixture (12 KB) — presumably the boundary/max-findings case — yet no test loads it. A bounds case that exists as data but is never exercised is a silent coverage gap. | Add the max-findings boundary test that loads it (likely an EC bound), or delete. |
| 6 | IMPORTANT | `fixtures/finding-needs-human.json` | **Orphan fixture — 0 references.** T-430 (`test_autonomy_gates.py:127`), EC-7, and FM-10 all exercise `needs_human_decision` but each sets `f.needs_human_decision = True` inline; none load this fixture. | Wire one of T-430/EC-7/FM-10 to the fixture, or delete it. |
| 7 | IMPORTANT | `fixtures/round-sequence-2.json` | **Orphan fixture — 0 references.** The fence-post matrix is fully parametrized inline (`test_loop_guard.py:66-71`); only `round-sequence-residual-x3.json` is even mentioned (and that only in a docstring "mirrors" comment, not loaded). `round-sequence-2.json` is dead data. | Delete, or wire into the T-622/T-626 path. |
| 8 | MINOR | `fixtures/round-sequence-residual-x3.json`, `behavioral-drift.json`, `crash-after-push-before-completed.json` | **Comment-only references — loaded by no test.** Each is named only in a docstring ("Scenario mirrors X.json" / "Mirrors X.json"); the tests reconstruct the scenario inline. Not strictly orphaned (the docstring documents provenance) but the fixture file is not actually exercised, so a drift between fixture and inline data would go undetected. | Prefer `load_fixture(...)` over inline reconstruction so the fixture is the single source of truth, OR accept as documentation-only and note it. Distinct from #3-7 (those have zero mentions at all). |

### Note on the "missing off-by-one test" hypothesis (from the prompt)
The adversarial brief specifically flagged a *possible* missing off-by-one test. **It is NOT
missing** — `T-626-OFF-BY-ONE` is present, is the canonical `>=`-gate-at-counter==2 case, is
`@pytest.mark.p0`, and is backed by `round-sequence-residual-x3.json`. The off-by-one surface
is the strongest-covered part of the suite. This hypothesis is REFUTED with evidence.

### Note on T-627 / T-628 (range-label IDs)
The matrix writes `FR-6.3 → T-620..T-629`. The implementation parametrizes T-620–T-625 plus the
named T-626-OFF-BY-ONE. T-627/T-628/T-629 do not exist as distinct functions, but the AC-6
property they would assert (max_rounds=N → exactly N pushes, counter==N) is fully covered by the
parametrized matrix and the hard-cap-5 case (`(5, 9, 5, 5)  # T-625`). This is a labeling
convention, not a coverage gap — PASS with note (item 16). Not counted as a finding.

## Actions Taken
None. `fix_authorization: false` — report only.

## Self-Audit
**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on the PGB.1 full-suite summary's "131 passed / 85% coverage" only as a starting
  claim — I independently re-ran the suite rather than trusting it.

**(b) Independent semantic checks (≥1 required):**
- Re-ran `uv run pytest tests/pr_submit/ -q` → confirmed `131 passed` with my own tool call (not relied on the manifest's claim).
- Grepped every spec §6.2 test ID against `tests/pr_submit/**/*.py` and confirmed three (T-105, T-N31, and the range-label T-627/628) — verified T-105/T-N31 are genuinely absent, not renamed, by searching ID fragments and behavior keywords.
- Distinguished *real* `load_fixture("...")` calls from *comment-only* fixture mentions (`grep load_fixture("` vs raw filename grep) — this is what exposed the 5 orphan + 3 comment-only fixtures that a naive filename grep marked "ok".
- Read `conftest.py` in full to confirm there is NO glob/iterdir dynamic fixture discovery — fixtures are loaded only by explicit string name, so zero-reference == truly dead.

**Self-audit questions:**
1. Factual claims independently verified against source: ~25 (suite run, p0 markers, every FM/EC ID, every flagged fixture's reference status, conftest loader mechanism, fence-post parametrize).
2. Files read: `conftest.py` (full), `merged-spec.md` §6.1/§6.2/§6.3 + NFR-4/§15.4/R9 rows, plus targeted grep/sed over all 21 test modules + 18 fixtures.
3. Why trust this found real issues: the findings are reproducible by `grep -rn "T-105" tests/pr_submit/` (empty) and the fixture-reference loop — not judgment calls.
4. Web research: none performed (lens is fully local-file-bound); Tavily not required.

**Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 3 | Grep/Bash: 9 | Glob: 0 | Bash(pytest): 1

## Recommendations
- Resolve all 8 findings before Gate B sign-off. Findings #1-#2 are matrix↔test contract breaks
  (spec asserts tests that don't exist by ID); #3-#7 are dead fixtures the manifest explicitly
  claims are all referenced; #8 is a provenance-drift risk.
- Cheapest correct path for #1/#2: add the two missing tests (T-105 in `test_skill_parse.py`,
  T-N31 in `test_detection_contract.py` next to T-211) so the matrix becomes truthful; this also
  bumps the count past 131 (toward the spec §6.1 "115 tests" floor, already exceeded).
- For #3-#7: prefer wiring the fixtures into their behavior-twin tests (EC-1/EC-9/EC-7, a
  max-bound test, T-622) so the JSON becomes the single source of truth, rather than deleting —
  inline data + unused fixtures is exactly the drift the fixtures were created to prevent.

## VERDICT: FAIL
