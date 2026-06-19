# QA Report — Synthesis Gate (Phase 6, lens: evidence-quality / test-coverage)

**Topic:** P5 Tier Calibration Advisory (RETAINED advisory-only)
**Date:** 2026-06-19
**Phase:** report-validation (P6 lens-based QA gate, evidence-quality lens)
**Fix authorization:** false (REPORT-ONLY)
**Fix cycle:** N/A

---

## Overall Verdict: PASS

The two P5 tests are non-vacuous, assert against source-of-truth `src/superclaude/...`,
correctly target the SCORED-TIER SLICE only (the R-9 whole-bundle `==` trap is AVOIDED),
and would FAIL if the advisory mutated a scored tier or if the section/threshold were
removed. Zero regressions (92 passed). Verdict is PASS on the five mandated VERIFY items.

Three test-COVERAGE gaps were found (documented invariants with NO asserting test). All
are IMPORTANT/MINOR, none invalidate the PASS: the verify mandate covered the scored-tier
slice + non-mutation + non-vacuity + regressions, all of which hold. The gaps are
under-coverage of the *advisory* side, not a defect in what is tested. Recorded below for
the orchestrator merge.

## Items Reviewed (the 5 mandated VERIFY items)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Tests assert against source-of-truth `src/superclaude/...` | PASS | Fixture `tasklist_skill_text` (test_tasklist_cli.py:44-46) reads `TASKLIST_SKILL_PATH = _REPO_ROOT/src/superclaude/skills/sc-tasklist-protocol/SKILL.md` where `_REPO_ROOT = Path(__file__).resolve().parents[2]` (line 35-39) = repo root. NOT the `.claude/` mirror. Header comment lines 28-33 explicitly state source-of-truth. |
| 2 | Determinism test asserts SCORED-TIER SLICE only — R-9 trap AVOIDED | PASS | `test_p5_advisory_does_not_mutate_scored_tiers` (599-614) asserts §5.3 pure-function invariant strings only (`"scored tiers are a **pure function of the roadmap text**"`, `"NO calibration/feedback input"`, `"MUST NOT read \`feedback-log.md\`"`, `"never feeds back into"`, `"same roadmap → same scored tiers"`). NO whole-bundle `==` / byte-equality assertion across differing feedback logs (grep for `==` in 599-615 returns only the python `assert ... in text` membership form). Test docstring 600-605 explicitly states the slice-only design. |
| 3 | Each asserted advisory marker exists in edited source | PASS | All 16 asserted strings grep-confirmed present in `src/.../SKILL.md` (counts all ≥1). Section at :866-885 (`## Tier Calibration Advisory`), §5.3 fence at :569, exact spec table at :880. |
| 4 | Tests would FAIL if advisory mutated a scored tier OR section/threshold removed (non-vacuous) | PASS | 4 live source mutations each turned a P5 test RED, then restored byte-identical (see Mutation Evidence). |
| 5 | Zero regressions (92 passed) | PASS | `uv run pytest tests/tasklist/ -q` → `92 passed in 0.20s`. P5 subset → `2 passed`. Matches p5-pytest-summary.md (92, +2 new, 0 regressions; prior baseline 90). |

## Mutation Evidence (non-vacuity, item 4)

Each mutation applied to `src/.../SKILL.md`, test re-run, source restored:

| Mutation | Target test | Result |
|----------|-------------|--------|
| `only when ≥2 matching overrides exist` → drop `≥2` | shape | FAILED (RED) ✓ |
| `MUST NOT mutate` → `MAY mutate` | shape | FAILED (RED) ✓ |
| `scored tiers are a **pure function of the roadmap text**` → `... depend on ...` | determinism | FAILED (RED) ✓ |
| `never feeds back into` → `feeds back into` | determinism | FAILED (RED) ✓ |

Post-restore: `diff` reports RESTORED-IDENTICAL; both P5 tests `2 passed`. The tests are
NOT vacuous — removing the section/threshold or weakening the non-mutation / pure-function
guarantee each breaks the gate.

## Issues Found (test-coverage gaps — adversarial pass)

These do NOT change the PASS verdict (the 5 mandated VERIFY items all hold). They are
under-coverage findings: documented invariants in the edited source that NO P5 test asserts.
A future source-side regression deleting any of these would NOT be caught by the suite.

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | SKILL.md:885 vs test 599-614 | R-9 has TWO clauses. Clause (a) "same roadmap → same scored tiers" IS tested. Clause (b) — "same roadmap + same feedback-log → identical advisory" — is documented at SKILL.md:885 (`The whole section is a pure function of \`(roadmap, feedback-log.md)\` — same inputs → byte-identical section`) but NO test asserts it. R-9 explicitly required: "Separately assert 'same roadmap + same feedback-log → identical advisory'." That assertion is absent. Marker grep `byte-identical section` in tests = 0 hits. | Add to `test_p5_advisory_does_not_mutate_scored_tiers` (or a sibling): `assert "same inputs → byte-identical section" in text` (advisory-determinism clause). |
| 2 | IMPORTANT | SKILL.md:871 vs P5 tests | First-run robustness ("the file may be absent on the first run — when absent, the whole section is omitted, no error") is documented at SKILL.md:871 but NO P5 test asserts the absent-feedback-log graceful-omit behavior. (The :400/:404 absent-form assertions belong to the Execution Context References-only test, an unrelated surface.) phase-6 summary acceptance criterion #5 (first-run robustness) is therefore unverified by test. | Add `assert "absent on the first run" in text` (or the omit-no-error phrase) to the shape test. |
| 3 | MINOR | index-template.md:132-134 vs P5 tests | R-14 mirror: `templates/index-template.md` carries the advisory placeholder at :132 (`### Tier Calibration Advisory (P5 — RETAINED advisory-only)` / :134 `## Tier Calibration Advisory`). NO P5 test reads `index_template_text` to confirm the mirror — both P5 tests only consume `tasklist_skill_text` (SKILL.md). The sole `index_template_text` test (test_execution_context_block_not_in_index, :410) asserts ABSENCE of a different section. Mirror-drift in the index template would pass the suite. | Add a P5 test asserting `"## Tier Calibration Advisory" in index_template_text` (and the advisory-only marker), paralleling the SKILL.md shape test. |
| 4 | MINOR | test 581 marker non-uniqueness | The shape test asserts `assert "## Tier Calibration Advisory" in text`. That literal appears 4× in SKILL.md (heading, fence reference :569, body :868/:878). The assertion would still pass if the actual emitted-output block (:868/:878) were deleted but a stray mention survived. Lower-risk because the table-column + threshold + ⚠ markers (uniquely in the block) backstop it, but the heading assertion alone is not block-anchored. | Optional: anchor on the more specific `#### Tier Calibration Advisory (P5 — RETAINED advisory-only)` heading or rely on the (already-unique) table/threshold markers. No action strictly required. |
| 5 | MINOR | test design (both P5 tests) | Both tests are pure source-string content gates — there is no executable generator (R-9 notes the logic is prose, which is legitimate). Consequence: the tests verify the SPEC TEXT is present, not that any generator HONORS it. This is the correct ceiling given no callable Python exists, but it means "the advisory cannot mutate a scored tier" is asserted as documented-intent, not as runtime behavior. Acceptable per R-9; flagged so the merge does not over-claim runtime enforcement. | None — inherent to the prose-generator design. Document the limitation in any downstream claim of "provably read-only." |

## Self-Audit

If I told the user I found 0 issues, would they believe me? No — and correctly so. An
adversarial pass on a 2-test, 16-assertion gate that is REQUIRED to satisfy a 2-clause R-9
contract should expect to find the under-tested clause. I found it (gap #1: advisory
determinism clause documented but untested), plus first-run (gap #2) and mirror (gap #3).
Evidence I actually checked: 4 RED mutations + restore, 16 marker greps, fixture-path
resolution read, and a `==`-absence grep over the determinism test body.

## Confidence Gate

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
  (the 5 mandated VERIFY items; all carry tool evidence). The 5 coverage gaps are findings,
  not unchecked items — each is itself tool-verified (grep counts, source line citations).
- **Tool engagement:** Read: 6 | Grep: 5 | Glob: 0 | Bash: 6 (greps + 2 pytest runs + 4 mutation cycles)
- **No UNCHECKED items.** No UNVERIFIABLE items.
- Tool calls (17) ≥ verification surface (5 mandated + 5 gap probes) — not suspect.

## Summary

- Mandated VERIFY checks passed: 5 / 5
- Coverage gaps found: 5 (IMPORTANT: 2, MINOR: 3)
- Critical issues: 0
- Issues fixed in-place: 0 (REPORT-ONLY — fix_authorization: false)
- Regressions: 0 (92 passed)

## Recommendations

- VERDICT: PASS. The P5 tests satisfy all five mandated VERIFY items. The R-9 whole-bundle
  `==` trap is provably AVOIDED; the determinism test is on the scored-tier slice only.
- Before final sign-off, the orchestrator SHOULD merge gaps #1 (R-9 advisory-determinism
  clause, IMPORTANT) and #2 (first-run robustness, IMPORTANT) into a follow-up. R-9
  literally mandated the advisory-determinism assertion ("Separately assert..."); it is the
  one part of the cited research pin not landed in test code. Gap #3 (mirror) is MINOR but
  cheap to close given `index_template_text` fixture already exists.
- These are additive test-coverage improvements; they do NOT block P6 since the source
  invariants themselves are correct and present — only their test guards are partial.

## QA Complete
