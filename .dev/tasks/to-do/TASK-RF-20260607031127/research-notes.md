# Research Notes: Fix PR #140 review comments r3367342586 (low) + r3367342583 (medium)

**Date:** 2026-06-07
**Scenario:** A (explicit — fully diagnosed upstream by /sc:troubleshoot)
**Depth Tier:** Quick
**Track Count:** 1

> Provenance: research was completed and verified during the `/sc:troubleshoot --fix` pass
> that produced `.dev/troubleshoot/prd-spec-review-r140-20260606174115/REPORT.md`. All
> file:line citations below were read directly from `origin/feature/prd-input-spec` (the PR
> branch), not inferred. No researcher fan-out is needed — the codebase facts are established
> and recorded in `research/01-findings.md`.

---

## EXISTING_FILES

- `src/superclaude/cli/prd/executor.py` (origin/feature/prd-input-spec, 1306 lines) — the only source file to change.
  - `_bind_specs(self, parsed: dict) -> dict` (L1196) — builds the `SPECS` array + prepends spec parent dirs to `WHERE`. `spec_files = list(self._config.spec_files or [])` at **L1209**; `for sp in spec_files:` at **L1215** (dedups parent dirs only, NOT spec paths). [CODE-VERIFIED]
  - `_persist_bound_specs(self) -> None` (L1245) — reads `parsed-request.json`, calls `_bind_specs`, re-writes. Durable source of bound `SPECS`. [CODE-VERIFIED]
  - `_warn_spec_degradation(self) -> None` (L1264) — R5 WARN; builds message via `specs = ", ".join(self._config.spec_files)` at **L1274**. [CODE-VERIFIED]
  - R5 gate at **L645**: `if step_id == "scope-discovery" and self._config.spec_files:` inside `_run_subprocess_step`. [CODE-VERIFIED]
- `src/superclaude/cli/prd/commands.py` (origin/feature/prd-input-spec) — `--spec` option declared only on `run` (L47); `resume` (L171) calls `resolve_config(...)` WITHOUT `spec=` (L204-214), so `config.spec_files` is empty on resume. [CODE-VERIFIED]
- `tests/cli/prd/test_spec_flag.py` (origin/feature/prd-input-spec, 447 lines, 27 tests) — existing test module for the `--spec` feature; regression tests go here. [CODE-VERIFIED]

## PATTERNS_AND_CONVENTIONS

- Fail-soft disk reads: `_persist_bound_specs` swallows `OSError`/`json.JSONDecodeError` and returns. New `_bound_spec_paths()` must follow the same fail-closed pattern (return `[]`). [CODE-VERIFIED L1253-1257]
- Order-preserving dedup idiom already present in `_bind_specs` for `parent_dirs` (list + membership check). Reuse the same idiom for spec-path dedup. [CODE-VERIFIED L1233-1237]
- `Path` is already imported in executor.py (used at L1216 `p = Path(sp)`). [CODE-VERIFIED]
- Tests: pytest under UV (`uv run pytest tests/cli/prd/test_spec_flag.py -v`). Tests live in `tests/`, never inline `python -c`.

## GAPS_AND_QUESTIONS

- None blocking. Both fixes and their exact code are specified in the REPORT. The only open design choice (add `--spec` to `resume` vs. read persisted `SPECS`) was resolved in the REPORT's "Alternative Fixes Considered": read persisted `SPECS` (durable source of truth).

## RECOMMENDED_OUTPUTS

- `research/01-findings.md` — the verified findings + exact proposed code (already the deliverable of the troubleshoot pass).

## SUGGESTED_PHASES

- Phase 1 (Fix 1 — low): dedup `spec_files` in `_bind_specs`.
- Phase 2 (Fix 2 — medium): add `_bound_spec_paths()`; route gate (L645) + message (L1274) through it.
- Phase 3 (Tests): add 3 regression tests to `tests/cli/prd/test_spec_flag.py`.
- Phase 4 (Validation): `uv run pytest tests/cli/prd/test_spec_flag.py -v` green; `uv run ruff format --check src/ tests/` + `make lint` clean.

## TEMPLATE_NOTES

- Template 02 (complex): build → test → validate with a conditional fix path. Quick tier (no web agents, no researcher fan-out — research complete).
- QA_GATE_REQUIREMENTS: FINAL_ONLY. VALIDATION_REQUIREMENTS: lint + ruff format check + targeted pytest green. TESTING_REQUIREMENTS: UNIT.

## AMBIGUITIES_FOR_USER

None — intent is clear from the review comments, the codebase, and the upstream diagnosis. The task targets branch `feature/prd-input-spec`; the executor.py path is canonical source (not a `.claude/` mirror), so no `make sync-dev` step applies to it.
