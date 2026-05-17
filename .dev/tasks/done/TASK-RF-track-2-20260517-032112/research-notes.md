# Research Notes: PR2 — ruff format sweep

**Date:** 2026-05-17
**Scenario:** A (explicit)
**Depth Tier:** Quick
**Track Count:** 5 (this is track 2)
**Order:** PR1 → PR2 → PR3 → PR4 → PR5

---

## EXISTING_FILES

- `pyproject.toml:159-173` — black config (line-length 88, target py310/311/312); ruff format follows the same line-length.
- `.github/workflows/quick-check.yml:39-41` — runs `ruff format --check src/ tests/` as a hard gate.
- After PR1 merges, the only outstanding ruff-format violations are pure-cosmetic (line wrapping, spacing, quote style normalization). They are independent of PR1's F401/I001/F841 fixes.

Source-of-truth files for this PR:
- `src/superclaude/**/*.py` (entire src tree)
- `tests/**/*.py` (entire tests tree)
- `pyproject.toml` (will read but NOT modify)

## PATTERNS_AND_CONVENTIONS

- Same as PR1.
- `ruff format` is mechanically applied — equivalent to `black` but faster; project ships with both configured.
- `make format` invokes `ruff format` per Makefile target.

## GAPS_AND_QUESTIONS

- **Should PR2 also run `black src/ tests/`?** The project still has `[tool.black]` config in pyproject.toml. Decision: NO — `ruff format` is what CI checks (`quick-check.yml:39`); black is legacy alongside it. Only run `ruff format`.
- **Independence from PR1**: PR2 must not be merged before PR1, because applying format-only changes to files with unused imports (PR1's territory) creates merge-conflict potential. Order dependency documented in frontmatter.

## RECOMMENDED_OUTPUTS

- Branch: `fix/ci-rot-pr2-ruff-format`
- Single task file: `TASK-RF-track-2-20260517-032112.md`
- PR title: `style(lint): ruff format --check now passes`

## SUGGESTED_PHASES

1. Preparation: confirm PR1 merged + branch from updated master + dev-deps install
2. Execute format: `uv run ruff format src/ tests/`
3. Verify: `uv run ruff format --check src/ tests/` exits 0; full test suite still passes
4. Commit + PR

## TEMPLATE_NOTES

- Template 02 (complex) — has prerequisite check (PR1 merged) + execute + verify + completion
- QA_GATE_REQUIREMENTS: FINAL_ONLY
- VALIDATION_REQUIREMENTS: ruff format --check, full test suite, make verify-sync
- TESTING_REQUIREMENTS: UNIT (run existing test suite)

## AMBIGUITIES_FOR_USER

- None. Mechanical operation.

---
**Status:** Complete
