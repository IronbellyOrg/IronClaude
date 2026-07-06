# BUILD_REQUEST

## GOAL
Apply both fixes diagnosed in `.dev/troubleshoot/prd-spec-review-r140-20260606174115/REPORT.md` for PR #140 review comments r3367342586 (low) and r3367342583 (medium), and add regression tests.

## WHY
Two confirmed correctness defects in the `--spec` deterministic-ingestion feature:
1. `_bind_specs()` does not dedup input `spec_files`, so duplicate `--spec FILE` produces duplicate `SPECS` entries and repeated `--file` attachments downstream (violates the method's own idempotency docstring). Severity: low.
2. The R5 "make silent degradation loud" WARN is gated on `self._config.spec_files`, which is ALWAYS empty on a `prd resume` run (`--spec` is declared only on `prd run`; `resume` → `resolve_config` omits `spec=`). Bound `SPECS` persist in `parsed-request.json`, so the warning can never fire on the resume path. Severity: medium.

## WHERE
- **Branch to target: `feature/prd-input-spec`** (NOT the current checkout `feature/prd-spec-flag`). The PR code (`_bind_specs`, `_persist_bound_specs`, `_warn_spec_degradation`, the `--spec` option) exists only on this branch.
- `src/superclaude/cli/prd/executor.py` — the only source file changed:
  - `_bind_specs()` (~lines 1196-1243): insert order-preserving dedup of `spec_files` keyed on `str(Path(sp))` immediately after the empty-guard, before the `for sp in spec_files` loop.
  - Add new method `_bound_spec_paths(self) -> list[str]`: return `list(self._config.spec_files)` when set, else read `SPECS` from `<task_dir>/parsed-request.json` and return each `s["path"]`; fail closed (return `[]`) on missing/corrupt JSON (`OSError`/`json.JSONDecodeError`).
  - Gate at `executor.py:645`: change `if step_id == "scope-discovery" and self._config.spec_files:` → `... and self._bound_spec_paths():`.
  - Message in `_warn_spec_degradation` at `executor.py:1274`: change `", ".join(self._config.spec_files)` → `", ".join(self._bound_spec_paths())`.
- `tests/cli/prd/test_spec_flag.py` (447 lines, 27 tests) — add regression tests:
  - Duplicate `--spec foo.md --spec foo.md` ⇒ exactly one `SPECS` entry for foo.md (and idempotent `WHERE`).
  - On a simulated resume (empty `config.spec_files` + a `parsed-request.json` containing a non-empty `SPECS` array), a STANDARD scope-discovery gate failure triggers `_warn_spec_degradation` and the emitted message lists the persisted spec path(s).
  - `_bound_spec_paths()` returns `[]` when `parsed-request.json` is missing or corrupt.

## CONSTRAINTS
- Source-of-truth: `src/superclaude/cli/prd/executor.py` is canonical Python (not a `.claude/` mirror); no `make sync-dev` needed for it.
- Use UV for all test runs: `uv run pytest tests/cli/prd/test_spec_flag.py -v`.
- Do not add `--spec` to the `resume` command — the durable `SPECS` array is the chosen gate input (see REPORT "Alternative Fixes Considered").
- Preserve fail-soft behavior on every disk read (no new crash paths).
- Run `uv run ruff format --check src/ tests/` and `make lint` before declaring done (CI runs format check separately from lint).

## TEMPLATE
01 (generic) — single source file + one test file, < 2 hours, low coupling.

## REFERENCE
Full diagnosis, evidence (file:line), and proposed code in:
`.dev/troubleshoot/prd-spec-review-r140-20260606174115/REPORT.md`
