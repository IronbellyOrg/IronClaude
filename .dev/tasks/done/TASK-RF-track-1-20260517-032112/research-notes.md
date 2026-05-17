# Research Notes: PR1 — ruff auto-fix sweep (F401 unused imports + I001 import order + F841 unused locals)

**Date:** 2026-05-17
**Scenario:** A (explicit)
**Depth Tier:** Quick
**Track Count:** 5 (this is track 1)
**Order:** PR1 → PR2 → PR3 → PR4 → PR5

---

## EXISTING_FILES

CI evidence from PR #35 run `25979540639` (job `76365604439`, base commit `71b1b1f`, re-validated after closeout merge `f64ea62`):

- Total ruff errors on master: 1036
- F401 (unused imports): 646 — **auto-fixable**
- I001 (un-sorted/un-formatted imports): 242 — **auto-fixable**
- F841 (unused local vars): 46 — **auto-fixable**
- Affected directories (8): `src/superclaude/cli/{audit,cleanup_audit,cli_portify,pipeline,prd,roadmap,sprint,tasklist}/`
- 291 unique `.py` files with at least one violation

Source-of-truth files for this PR:
- `pyproject.toml:175-182` — ruff config: `select = ["E","F","I","N","W"]`, `ignore = ["E501"]`, `exclude = ["docs/"]`, line-length 88
- `.github/workflows/test.yml:46-48` — runs `pytest -v` (no audit filter); `quick-check.yml:35-37` runs `ruff check src/ tests/`
- `Makefile` — defines `make lint` (ruff check) and `make format` (ruff format)
- Local `.venv` is missing the dev dependencies (ruff not on PATH); `make dev` or `uv pip install -e ".[dev]"` is required before running ruff locally

## PATTERNS_AND_CONVENTIONS

- Source-of-truth is `src/superclaude/`; tests live under `tests/`. `.claude/` is a synced copy and must NEVER be edited directly (`make sync-dev` enforces).
- Branch convention: `feat/*`, `fix/*`, `chore/*`, `docs/*`. PR target is `master` (NOT `main` — relevant to PR5).
- Commit convention: conventional commits with `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>` trailer.
- Recent merges (`71b1b1f`, `cd4c9e0`, `f64ea62`) used squash-merge via `gh pr merge --squash --delete-branch`.

## GAPS_AND_QUESTIONS

- **Scope-vs-AC mismatch (user intent inference)**: BUILD_REQUEST says "across src/superclaude/cli/audit/ + tests/audit/" but AC1 requires `ruff check src/ tests/` exits 0 globally. The narrow scope cannot satisfy AC1. **Resolution applied**: widen scope to whole src/ + tests/ tree. Document this in task Open Questions; proceed.
- **F841 inclusion**: BUILD_REQUEST mentions only F401+I001 for PR1; F841 (46 violations) is also auto-fixable by `ruff --fix`. **Resolution applied**: include F841 in PR1 because it's mechanically identical and would otherwise need a separate auto-fix PR.
- **N806/N811/F811 status**: 25 total violations not in the brainstorm spec. These are manual fixes; routed to PR3 alongside E741.

## RECOMMENDED_OUTPUTS

- Branch: `fix/ci-rot-pr1-ruff-autofix`
- Single task file: `TASK-RF-track-1-20260517-032112.md`
- PR title: `fix(lint): ruff --fix sweep — F401 unused imports + I001 import order + F841 unused locals`

## SUGGESTED_PHASES

Orchestrator-as-researcher (no parallel researchers spawned — Quick tier, Scenario A, scope fully known from CI logs and BUILD_REQUEST). Builder receives this notes file directly.

Suggested task phases:
1. Preparation: branch + dev-deps install + baseline lint
2. Execute auto-fix: `uv run ruff check src/ tests/ --fix --select F401,I001,F841`
3. Verify: re-run ruff check (expect F401/I001/F841 gone); run full test suite to confirm no behavioral regression
4. Commit + PR

## TEMPLATE_NOTES

- Template 02 (complex) — has a discovery (baseline) phase + execute + verify + completion
- QA_GATE_REQUIREMENTS: FINAL_ONLY (one verification phase at end is sufficient — work is mechanical)
- VALIDATION_REQUIREMENTS: ruff check (auto-fix targets only), full test suite, make verify-sync
- TESTING_REQUIREMENTS: UNIT (run existing test suite; no new tests written)

## AMBIGUITIES_FOR_USER

- Wider scope (whole src/+tests/ vs only audit/) — flagged as Open Question in the task file; default action is wider scope to satisfy AC1.

---
**Status:** Complete
