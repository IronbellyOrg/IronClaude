# QA Report - Gate C, lens "module-boundaries-and-python-310" (structural)

**Topic:** issue-watch implementation, Phases 6 and 7 (cycle.py, cli.py, main.py registry edit, conftest part 4, three test files)
**Date:** 2026-11-08
**Phase:** task-integrity / structural gate (report only, `fix_authorization: false`)
**Fix cycle:** 1 (first review of Gate C)
**Change set read:** `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/reports/gate-c-change-set.md`

---

## Overall Verdict: PASS (0 blocking findings, 8 minor notes)

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `cycle` imports only runner, github, predicates, record, launch, audit from the package and nothing else from superclaude | PASS | Grep of every `import`/`from` line (indented ones included) in `cycle.py`: lines 12-31 are stdlib plus `from . import audit, github, launch, predicates, record`, `.launch`, `.predicates`, `.record`, `.runner`. No indented (lazy) import exists in cycle.py. No `superclaude.*` import at all. |
| 2 | `cli` imports only cycle, record, audit, launch, runner plus click | PASS | `cli.py:12-29`: stdlib, `click`, `from . import audit, cycle, record`, `.launch` (MAX_ISSUE_NUMBER, OrcaLauncher), `.record`, `.runner`. No github or predicates import (but see M2: `cycle.format_utc` at `cli.py:310`). |
| 3 | Other modules obey the design 5.3 table (runner/predicates/audit none; github runner+predicates; record predicates + lazy `swarm.atomic`; launch runner + `install_user_setup._ORCA_CLIS`) | PASS | Import grep over all 9 files. `record.py:23` predicates; lazy `swarm.atomic` at `record.py:372` and `:853`; `launch.py:22,24`; `github.py:22,35`; `runner/predicates/audit` import only stdlib. Only three indented imports exist in the package (`record.py:372,389,853`). |
| 4 | Nothing imports `subprocess` except `runner.py` | PASS | Grep `subprocess\|os.system\|os.popen\|os.exec\|os.spawn\|Popen` over src and tests: the only `import subprocess` in src is `runner.py:10`; `cli.py:7` and `cycle.py:5,1161` mention it in docstrings that say it is never imported. Tests: `test_runner.py:5` imports it to fake `subprocess.run`; no test starts a real process (`test_cli.py:53-66` turns any real call into a failure). |
| 5 | No module is named `select` | PASS | Glob of `src/superclaude/cli/issue_watch/` shows 9 modules (`__init__, runner, github, audit, predicates, launch, record, cycle, cli`); Grep `\bselect\b` over src and tests has no hit. |
| 6 | Python 3.10: the lens grep (`tomllib`, `datetime.UTC`, `UTC` import, `StrEnum`, `Self`, `ExceptionGroup`, `except*`, `asyncio.timeout`, `fromisoformat`) | PASS | Exactly one hit: `predicates.py:30`, a docstring sentence "DF-35: no ``fromisoformat``" stating the module avoids it. Justified. `parse_utc` uses a fixed-format parser, not `fromisoformat`. |
| 7 | Python 3.10: other 3.11/3.12-only features | PASS | Grep for `NotRequired, Required, LiteralString, Never, assert_never, Unpack, override, batched, .walk(, is_junction, contextlib.chdir, add_note, sys.exception, file_digest, getLevelNamesMapping, cbrt, exp2, case_sensitive, (?>, possessive quantifiers, TaskGroup, PEP 695 type statements`: no real hit (only the word "Required" in docstrings and `str.removesuffix`, which is 3.9+). `ast.parse(..., feature_version=(3, 10))` accepted all 24 `.py` files (9 source, 14 test, `main.py`). `pyproject.toml:16` `requires-python = ">=3.10"`, `:175` ruff `target-version = "py310"`. |
| 8 | Python 3.10 runtime proof | PASS | Python 3.10.20 is installed under uv. In a throwaway env (`UV_PROJECT_ENVIRONMENT=/tmp/...`, removed afterwards; `uv.lock` and `pyproject.toml` untouched): import of `cycle`, `cli` and `superclaude.cli.main` works and the group lists `['check-config','init-state','once','reset','status']`; `pytest tests/issue_watch/ -q -p no:cacheprovider -W error::DeprecationWarning` gave `2194 passed`. `email.utils.parsedate_to_datetime` (the one stdlib call whose error type changed across versions) raises `ValueError` on 3.10.20 and `github.py:410-411` catches `(TypeError, ValueError, IndexError, OverflowError)`. |
| 9 | No `/proc` or `fcntl` use at import time | PASS | `cycle.py:77` is a string constant; the read is inside `_read_mountinfo` (`cycle.py:178-184`). `fcntl` is imported inside the lock method (`record.py:389`, comment "not at module level"). `os.O_NOFOLLOW`/`O_DIRECTORY` are used only inside functions (`cycle.py:321`, `audit.py:105`, `record.py:311,393,783`). |
| 10 | File hygiene: LF endings | PASS | Byte scan of 41 files under `src/.../issue_watch`, `tests/issue_watch` (fixtures included) and `main.py`: no `\r` in any file, no BOM. |
| 11 | File hygiene: exactly one trailing newline on non-empty files | PASS | Same scan: every non-empty file ends with `\n` and none with `\n\n`. The two empty files are `src/.../issue_watch/__init__.py` and `tests/issue_watch/__init__.py` (0 bytes; design 751 and 761 call them package markers). |
| 12 | File hygiene: no trailing spaces in `.py` and `.json` | PASS | Same scan: zero trailing-whitespace lines in all `.py` and `.json` files; no tab characters in any `.py`. |
| 13 | No name from `superclaude.contracts.__all__` is bound; no string literal equals an ID-pattern body | PASS | `contracts.__all__` = AdversarialReturn, CONVERGENCE_THRESHOLDS, GATE_FIELD_NAMES, ID_PATTERNS, RETURN_CONTRACTS, ROADMAP_ENTITY_ID_FAMILIES, THRESHOLDS, TOOL_WRITE_ROADMAP_ID_FAMILIES, UnaddressedInvariant, roadmap_ids_pattern. An AST scan of src and tests for any def, class, arg, Name, Attribute, import alias or string constant equal to one of them: 0 hits. `arch_lint.check_paths` over `src/superclaude/cli/issue_watch` and `tests/issue_watch`: `violations: 0`. Module constants in `cycle.py` (lines 34-78, 443-444, 468-469, 1171-1172) include no contract name. |
| 14 | main.py edit: exactly the import line with its noqa suffix plus the `add_command` line, nothing else; `superclaude --help` works | PASS | `git diff HEAD -- src/superclaude/cli/main.py`: `1 file changed, 4 insertions(+)`, hunk `@@ -560,6 +560,10 @@`, lines 563-565 are the `from superclaude.cli.issue_watch.cli import issue_watch_group  # noqa: E402,I001  # intentional: ...` line, a blank line and `main.add_command(issue_watch_group, name="issue-watch")`. The noqa suffix is byte-identical to the reflect line above it (`main.py:559`). Matches the change-set diff. `uv run superclaude --help` printed a Commands list containing `issue-watch    Poll GitHub for approved issues and start one Orca claim...` and no traceback. Each of the 8 modules imports cleanly as the first import of a fresh process (no import cycle through `superclaude.cli.__init__` -> `main`). |
| 15 | Click commands are exactly five, hyphenated names registered explicitly | PASS | `cli.py:93` `@click.group("issue-watch")`; `@issue_watch_group.command("once")` (110), `"status"` (155), `"check-config"` (176), `"init-state"` (192), `"reset"` (273): five names, each passed as an explicit string. `uv run superclaude issue-watch --help` lists exactly check-config, init-state, once, reset, status. Registered in main as `name="issue-watch"`. |
| 16 | Scope: nothing from `.claude/` and no test-collection collision caused by the new package | PASS | `git status --short` shows no `.claude/` path. `pytest tests/issue_watch/test_cli.py tests/cli_portify/test_cli.py --collect-only` collects 119 tests with no error (both folders have `__init__.py`). |

## Summary
- Checks passed: 16 / 16
- Checks failed: 0
- Blocking issues: 0 (CRITICAL 0, IMPORTANT 0)
- Minor notes: 8
- Issues fixed in-place: 0 (report only)

## Issues Found

No blocking finding. Numbered table of every finding, all minor:

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| M1 | MINOR | `cycle.py:1208,1211` (`_retry_orca`) | `cycle` reads `launch._ORCA_CLIS`, a private name that exists in `launch` only because `launch.py:22` imports it from `superclaude.cli.install_user_setup`. The AST import rule is met (no import statement), but `cycle` now depends in effect on a superclaude name the design 5.3 table gives `cycle` none of ("May import from elsewhere: none"), through another module's private re-import. A change to the import form in `launch` (a lazy or `as` import) would break `status` retry output. | Expose a public name in `launch` (for example `ORCA_CLI_NAMES = _ORCA_CLIS`) and use that, or move the "first resolvable orca" helper into `launch`. Not required to pass. |
| M2 | MINOR | `cli.py:310` | `cli` calls `cycle.format_utc`, which is `predicates.format_utc` re-imported by `cycle.py:29`. Design 5.3 does not list `predicates` for `cli`. No import rule is broken, but the dependency on `predicates` is hidden behind a re-export. | Use `audit` or `cycle` helper that formats the stamp, or add `format_utc` to the documented `cycle` surface. |
| M3 | MINOR | `cycle.py:1216` | The parameter `audit` of `status_report` shadows the imported module `audit` inside that function (the body does not use the module, so there is no bug). `Deps.audit` (`cycle.py:423`) has the same name as the module. | Nit; leave or rename the parameter. |
| M4 | MINOR | `record.py:23` versus `cycle.py:27`, `cli.py:26` | `record.py` imports with the absolute form `superclaude.cli.issue_watch.predicates`; every other module uses relative imports. The `tests/issue_watch/test_module_boundaries.py` AST walker planned in Step 8.8 must resolve both forms. | Note for Step 8.8; no change needed now. |
| M5 | MINOR | `tests/issue_watch/__pycache__/` | Stale bytecode of deleted scratch tests: `test_smoke_x`, `test_zz_scratch_world`, `test_tmp_orig`, `test_dbg_tmp` (Glob). No source exists for them, `.gitignore:2` ignores `__pycache__/`, and sourceless pyc files in `__pycache__` are not collected, so nothing runs or ships. | None; optionally delete the stale files. |
| M6 | MINOR (cross-lens, for the citation-evidence lens) | `docs/designs/issue-watcher.md:95` and `:244` | Line 95 (C14) says `tests/cli_portify/test_cli.py` makes same-basename test files collide; `tests/cli_portify/__init__.py` exists and collection of both files succeeds (119 tests), so the stated reason is false (the `__init__.py` in `tests/issue_watch/` is still harmless). Line 244 says `cli.py` is imported lazily from `main.py`; `main.py:563` is a module-level import that runs on every `superclaude` start. The design file is not in `src/` or `tests/`, and no source or test text repeats either claim (Grep for `lazy`, `collid`, `cli_portify` in src and tests: one hit, `test_record.py:666`, about the genuine lazy `swarm.atomic` import). | Correct the design text if the design is meant to stay accurate. |
| M7 | MINOR (process) | git status | `src/superclaude/cli/issue_watch/`, `tests/issue_watch/`, `docs/designs/issue-watcher.md` and the new `.dev/` folders (`phase-outputs/`, `qa/gate-a/`, `qa/gate-b/`, `qa/gate-c/`) are untracked (`??`). Project rule: `.dev/tasks/` is always staged (`git add .dev/tasks`). Nothing is committed here, as no commit was requested. | Stage `.dev/tasks` and the new source and test folders when committing. |
| M8 | MINOR | design 5.3 / 8.8 | `tests/issue_watch/test_module_boundaries.py` does not exist yet (it is Step 8.8, a later phase), so the import rules for `cycle` and `cli` are not mechanically enforced at this gate. This report checked them by reading and grep. | None for this gate; Step 8.8 must add the test. |

## Actions Taken
None. No file was modified except this report. A throwaway virtual environment under `/tmp` was created for the 3.10 runs and removed afterwards; no bytecode was written into the repository (`PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`).

## Recommendations
- Proceed. No blocking finding in this lens.
- Optional before merge: M1 (public name in `launch`) and the design text of M6.

## Confidence
- **Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 22 | Glob: 2 | Bash: 10
- Self-audit: the claim "0 blocking" rests on the AST scans, the arch-lint run, the git diff of `main.py`, the `--help` output and the 2194-pass run on Python 3.10.20 listed above. The task prompt expected at least 15 errors; this lens found none that is blocking. The strongest candidates (M1, M2) were weighed against the severity rule: both are correct behaviour with a hidden dependency, so they are minor.

## QA Complete
