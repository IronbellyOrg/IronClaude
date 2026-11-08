# QA Report: Gate B, lens "module-boundaries-and-python-310" (Phases 4 and 5, issue-watch)

**Topic:** issue-watch `record.py` and `launch.py` import boundaries, Python 3.10 compatibility, file hygiene, test isolation
**Date:** 2026-11-07
**Phase:** task-integrity style structural gate (Gate B lens agent 3, Step 5.G4)
**Fix cycle:** N/A (report only, `fix_authorization: false`)
**Scope read:** `gate-b-change-set.md`; `docs/designs/issue-watcher.md` lines 215-260 and 440-450; `record.py` (all 858 lines); `launch.py` (all 348 lines); `conftest.py` lines 160-230; `test_origin_parity.py` lines 1-125; `test_marker_contract.py` (all); `test_record.py` lines 1708-1837 plus targeted greps; `test_launch.py` lines 255-295 and 490-530 plus targeted greps; hygiene and AST checks over every file under `src/superclaude/cli/issue_watch/` and `tests/issue_watch/`.

---

## Overall Verdict: PASS (with minor notes)

Zero blocking findings. The task prompt told me to assume at least 15 errors. I looked for them and did not find 15; I am not padding the table. There are 9 minor notes below. One check could not be run: executing the code on a real Python 3.10 interpreter (see Unverifiable).

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `record` imports only `predicates` and `superclaude.cli.swarm.atomic` (plus stdlib) | PASS | Grep of import lines: `record.py:12-22` stdlib only; `record.py:24` `superclaude.cli.issue_watch.predicates`; `record.py:370` and `record.py:846` lazy `superclaude.cli.swarm.atomic`. No `audit`, `github`, `cycle`, `cli`, `launch`, `runner` import. Runtime check: importing `superclaude.cli.issue_watch.record` loaded only `issue_watch`, `issue_watch.predicates`, `issue_watch.record`. |
| 2 | `swarm.atomic` is imported inside `FileStore.save` only | PASS with note M1 | `record.py:370` is inside `FileStore.save`. A second lazy import exists at `record.py:846` in `save_dry_run` (module function, not `FileStore.save`). See M1. |
| 3 | `launch` imports `runner` and `_ORCA_CLIS` from `superclaude.cli.install_user_setup` only | PASS | `launch.py:13-23`: stdlib, `launch.py:21` `from superclaude.cli.install_user_setup import _ORCA_CLIS`, `launch.py:23` `from .runner import CommandResult, Runner`. `_ORCA_CLIS = ("orca-ide", "orca")` exists at `install_user_setup.py:35`. Runtime check: importing `launch` loaded only `issue_watch`, `issue_watch.launch`, `issue_watch.runner`. |
| 4 | Neither module imports `audit`, `github`, `cycle` or `cli` | PASS | Import grep above (no hit) and the two runtime `sys.modules` listings (no `audit`/`github`/`cycle`/`cli` entry). |
| 5 | `fcntl` imported only inside `lock()` | PASS | Grep `fcntl` in `record.py`: `record.py:387` (`import fcntl` inside `FileStore.lock`), then uses at 405 and 419 inside the same method. No module-level import in any `src/` file under `superclaude` (`^import fcntl` grep over `src/superclaude`: no match). |
| 6 | Only `runner.py` imports `subprocess` | PASS | `grep -rn subprocess src/superclaude/cli/issue_watch` excluding `runner.py`: no output. `runner.py:10` is the only import. |
| 7 | Third-party imports: none in `record`/`launch` | PASS | Import grep: no `click` or other third-party name in either file. |
| 8 | Python 3.10 grep from the prompt, every hit justified | PASS | The one hit over `src/superclaude/cli/issue_watch/` and `tests/issue_watch/` is `predicates.py:30`, a docstring that says "no `fromisoformat`" (DF-35). No `tomllib`, `datetime.UTC`, `StrEnum`, `Self`, `ExceptionGroup`, `except*` or `asyncio.timeout` in code. |
| 9 | `os.O_NOFOLLOW`, `os.O_DIRECTORY`, `fcntl` at import time | PASS (src) / see M3 (tests) | `record.py:309` (`O_DIRECTORY`), `:391` and `:776` (`O_NOFOLLOW`) are all inside function bodies, evaluated at call time. No module-level use in `src/`. `tests/issue_watch/test_record.py:12` has a module-level `import fcntl` (M3). |
| 10 | Other 3.11-only features | PASS | Greps for `contextlib.chdir`, `file_digest`, `Path.walk`, `batched`, `sys.exception`, `add_note`, `LiteralString`, `assert_never`, `getLevelNamesMapping`, `onexc`, possessive quantifiers/atomic groups, `[*x]` subscripts, `type X =`, `def f[T]`: only `launch.py:131` and `test_record.py:1504` match `[*...`, and both are list displays (valid since 3.5), not subscripts. Every one of the 16 `.py` files under the two folders has `from __future__ import annotations` (count grep), so `X \| None` annotations are never evaluated. No `isinstance(x, A \| B)` or runtime `A \| B` alias found. All 31 `.py` and `.json` files parse with `ast.parse(..., feature_version=(3, 10))` (run under 3.11.15). |
| 11 | LF line endings | PASS | AST/hygiene script: no `\r` byte in any of the 31 files checked. |
| 12 | Exactly one trailing newline on every non-empty file | PASS | Same script: every non-empty `.py` and `.json` ends with exactly one `\n`. |
| 13 | No trailing spaces in `.py` and `.json` | PASS | Same script: no line with trailing space or tab. |
| 14 | Zero-byte `__init__.py` | PASS | `src/superclaude/cli/issue_watch/__init__.py` 0 bytes; `tests/issue_watch/__init__.py` 0 bytes. |
| 15 | No name from `superclaude.contracts.__all__` is bound | PASS | Script bound every module-level def, class, assignment, annotated assignment and import name in each `.py` file and intersected with the 10 names in `contracts.__all__`: empty for all files. |
| 16 | Tests use `tmp_path` and never write under the repository | PASS with notes M4, M5 | Writes in `test_record.py` all go through `tmp_path` / `tmp_state` (`conftest.py:179-184` sets HOME and XDG inside `tmp_path`). `test_launch.py`, `test_marker_contract.py` only read. Two caveats: M4 (bytecode cache) and M5 (reads `~/.claude`). |

## Summary
- Checks passed: 16 / 16 (4 with minor notes)
- Checks failed: 0
- Critical issues: 0
- Blocking issues: 0
- Minor notes: 9
- Issues fixed in-place: 0 (report only)

## Issues Found

Blocking: none.

Minor notes (do not fail the gate, are not rechecked in later rounds):

| # | Severity | Location | Note | Suggested follow-up |
|---|----------|----------|------|---------------------|
| M1 | MINOR | `src/superclaude/cli/issue_watch/record.py:846` | `save_dry_run` lazily imports `superclaude.cli.swarm.atomic`. The lens text and design C18 (`issue-watcher.md:99`) say the import is "inside `save`". The module is still within the allowed import set and the lazy-import reason holds, but a Phase 8 boundary test that pins the import to `FileStore.save` would fail. | Decide the rule in Step 8.8: module-level allow-list (current behaviour) or exact function. Update design C18 to say "inside `save` and `save_dry_run`". |
| M2 | MINOR | `record.py:24-29` vs design `issue-watcher.md:239` | The design says `record` imports `predicates` "types only". `record` imports three functions (`format_utc`, `parse_utc`, `valid_issue_number`, defined at `predicates.py:42`, `:27`, `:52`) and one type (`ApprovalResult`, `predicates.py:139`, annotation only). `Entry` holds no `predicates` type. The module-level rule is met; the parenthetical is not. | Amend the design table cell to "pure helpers and types". The Phase 8 test checks module names, so it will not trip. |
| M3 | MINOR | `tests/issue_watch/test_record.py:12` | Module-level `import fcntl` makes collection fail on a platform without `fcntl` (Windows). CI is `ubuntu-latest` on Python 3.10 (`.github/workflows/test.yml:13,22`), so no current failure. | Optional: `pytest.importorskip("fcntl")` or import inside the lock tests. |
| M4 | MINOR | `tests/issue_watch/test_origin_parity.py:62-71` | The `original` fixture runs `exec_module` on `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py`, which lets Python write bytecode into that folder's `__pycache__` (`origin_repo.cpython-311.pyc` is present). Gitignored (`.gitignore:2`), so nothing is committed. Strictly this is a write under the repository. | Optional: read the source and `exec(compile(...))` it, or accept as normal import behaviour. |
| M5 | MINOR | `tests/issue_watch/test_marker_contract.py:22-25,34-39` | Reads `~/.claude/skills/sc-issue-protocol/...` when present. A contributor with an older installed copy that lacks the marker gets a failure the repo cannot fix. Currently passes: both installed files contain the marker (grep count 2 and 1). Documented as intended in the module docstring (DF-21, DF-46). | Accept, or turn a stale installed copy into a skip with a message. |
| M6 | MINOR | `test_record.py:1810-1822` (`..._read_only_parent_is_state_dir_unwritable`) | `chmod 0o500` on the parent gives no failure when the suite runs as root (root ignores mode bits). No `skipif(os.geteuid() == 0)` guard (the only `geteuid` use in the file is the monkeypatch at 682-687). | Add a root skip guard. |
| M7 | MINOR | `record.py:24` vs `launch.py:23` | `record` imports its sibling by absolute path (`superclaude.cli.issue_watch.predicates`); `launch` uses a relative import (`.runner`). Both are legal. The Phase 8 AST walk must resolve both forms or a future change may slip through. | Make the Step 8.8 test handle `ImportFrom` with `level > 0` and with the absolute package prefix. |
| M8 | MINOR | design `issue-watcher.md:221` vs `record.py:620,692,379` | Design 5.2 lists `sweep(store, now)` and `day_cap_count(store, now)` and a `Lock` class. Implementation has `sweep(doc, now)`, `day_cap_count(doc, now)` and `FileStore.lock()` (the Protocol at design 268-274 does define `lock()` on `Store`). The functions are pure over the document, which is consistent with "never reads the clock/runs commands". Doc drift only. | Update the 5.2 `record` row. |
| M9 | MINOR | `tests/issue_watch/__pycache__/test_smoke_x.cpython-311-pytest-9.2.0.pyc` | A bytecode file for a test module (`test_smoke_x`) that no longer exists. Gitignored and never collected; leftover from an earlier session. | Delete locally; no commit impact. |

## Actions Taken
None. Only this report file was written. No source, test or fixture file was modified. Python checks ran with `-B -I` and `PYTHONDONTWRITEBYTECODE=1`, so they created no new bytecode files.

## Recommendations
- Proceed. No blocking finding for this lens.
- Carry M1, M2 and M7 into Step 8.8 (`test_module_boundaries.py`) so the AST walk and the design table say the same thing.
- Run the suite once on a real Python 3.10 interpreter before merge (CI does this at `.github/workflows/test.yml:22`); this review could only prove 3.10 compatibility statically.

## Confidence Gate
- **Confidence:** Verified: 15/16 | Unverifiable: 1 | Unchecked: 0 | Confidence: 100.0% (15 / (16 - 1))
- Unverifiable item (counted in the 16 above as the runtime half of check 10): executing `record.py`, `launch.py` and the tests on a real CPython 3.10. Blocker: no 3.10 interpreter is installed (`/usr/bin/python3.10` absent; `uv python list` shows 3.10 only as "download available"), and `uv run --python 3.10` would rebuild the repo `.venv`, which this read-only review must not do. Static evidence (3.10 AST parse, feature greps, future-annotations count) stands in for it. Undetected-issue scenarios that remain: a runtime-only 3.11 stdlib behaviour change inside a call I did not recognise by name (for example a changed default of a stdlib function).
- **Tool engagement:** Read: 15 | Grep: 21 | Glob: 1 | Bash: 3 (one AST/hygiene script via stdin heredoc, one batch of read-only checks, one runtime import-graph check)
- Tool calls (37) >= checklist items (16): no engagement flag.

## QA Complete
