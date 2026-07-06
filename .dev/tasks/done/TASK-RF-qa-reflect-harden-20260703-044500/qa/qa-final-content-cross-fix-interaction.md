# QA Report — task-qualitative (LENS: cross-fix-interaction)

**Topic:** PR #209 F1–F4 hardening — 5-fix cross-interaction gate-weakening audit
**Date:** 2026-07-03
**Phase:** task-qualitative (scaled I19 agent, cross-fix-interaction lens, 500–1500 net-line band)
**Fix cycle:** N/A (FINAL M3 gate)
**Worktree:** `/config/workspace/IronClaude/.dev/worktrees/pr209-harden`
**fix_authorization:** false (REPORT ONLY)
**Adversarial stance:** ASSUMED two of the five FX interact to weaken a gate; hunted the interaction.

---

## Overall Verdict: PASS

No PAIR of the five FX weakens an existing gate or creates a latent hole that neither
does alone. All four candidate interaction paths were driven to ground with source
reads + a live pytest run and REFUTED. The two "non-gating" mechanisms (FX7, FX1) are
both **visibility-preserving** (they emit observable tokens, they do not silence), and
the two load-bearing **gating** catches for the F1 class (FX2, FX3/FX5) sit on surfaces
that are structurally independent of the non-gating mechanisms — so no combination
demotes a real problem into silence.

---

## The five FX (as applied in worktree HEAD)

| FX | Surface | Gating? | Channel |
|----|---------|---------|---------|
| FX1 | `agents/reflect-reviewer.md` + `refs/deviation-taxonomy.md` | **ADVISORY / non-gating** | `correctness-gaps.yaml` (no-spec residual only) |
| FX2 | `agents/rf-qa-qualitative.md` item 5 (AX-2 cross-symbol input-shape) | **GATING** (rf-qa-qualitative Verdict, sev ≥ IMPORTANT) | task-qualitative FAIL |
| FX3 | `tests/pr_submit/test_setup_questions_resolution.py` | **GATING** (deterministic pytest) | pytest FAIL |
| FX5 | `tests/pr_submit/conftest.py` + `test_gate_helper_{coverage,differentials}.py` | **GATING** (deterministic pytest) | pytest FAIL |
| FX7 | `cli/reflect/{contract,models,ensemble,runner}.py` | **VISIBLE / non-gating** | `degraded_components` token + `reviewers_verified` flag |

---

## Items Reviewed
| # | Check (interaction pair) | axis | Result | Evidence |
|---|--------------------------|------|--------|----------|
| 1 | FX5 conftest hook × FX7 reflect collection | none | PASS | `pytest_generate_tests` is directory-scoped to `tests/pr_submit/` + name-guarded; `tests/cli/reflect/` has own conftest; live run 173 passed/1 xpassed clean |
| 2 | FX7 visible-non-gating × FX1 advisory-non-gating (double-demotion) | none | PASS | Both emit observable tokens; load-bearing gating (FX2/FX3/FX5) independent of reviewer count |
| 3 | FX2 gating × FX1 advisory (same F1 class → downgrade) | none | PASS | Different agents/stages; grep-confirmed neither brief references the other; FX1 spec-anchor-gated |
| 4 | FX3 + FX5 both in `tests/pr_submit/` (collision) | none | PASS | `uv run pytest tests/pr_submit/ -q` → 311 passed, only the 6 known offer-pr-review.sh fails |

<!-- task-qualitative Axis column: closed set {AX-1..AX-5, none}. All four checks PASS
with the five-axis lens applied and no axis-attributable finding surfaced → `none`.
The load-bearing axis for a gate-weakening interaction would be AX-2 (Contradictions);
none fired. drift-axis-inactive is NOT declared — the BUILD_REQUEST GOAL (additively
harden RF QA + /sc:reflect, weaken NO existing gate) is reproduced in research-notes.md
and served as the drift baseline. -->

## Summary
- Checks passed: 4 / 4
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (REPORT ONLY)

## Confidence
- **Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 2 | Grep: 3 | Glob: 0 | Bash: 5
- Every interaction check maps to a specific source read or executed command (below);
  no padding calls.
