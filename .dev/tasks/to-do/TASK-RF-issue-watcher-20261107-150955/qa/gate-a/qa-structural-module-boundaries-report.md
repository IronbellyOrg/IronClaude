# QA Report - Gate A, lens "module-boundaries-and-python-310"

**Topic:** issue-watch implementation, Phases 2 and 3 (Gate A)
**Date:** 2026-11-07
**Phase:** task-integrity / structural gate (module boundaries and Python 3.10 compatibility)
**Fix cycle:** N/A (first review; `fix_authorization: false`, no file other than this report was modified)
**Change set read:** `phase-outputs/reports/gate-a-change-set.md` (11 Python files plus 11 JSON fixtures; the inventory matches Glob and `wc -l` exactly)

---

## Overall Verdict: FAIL (1 blocking finding, 9 minor notes)

The module-boundary table, the Python 3.10 checks and the file hygiene rules all hold. The single blocking finding is a false docstring claim about `parse_utc` (finding 1), proven by running the function. The prompt asked me to assume at least 15 errors; I did not find 15 and did not invent any. Every item below was observed with a tool call.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `runner`, `predicates`, `audit` import nothing from the package or from `superclaude` (design 233-237) | PASS | Import grep over `src/superclaude/cli/issue_watch/*.py` (indented imports included) plus an `ast.walk` of every file: runner imports `subprocess, time, dataclasses, typing`; predicates `collections.abc, dataclasses, datetime`; audit `datetime, json, os, socket, sys, pathlib`. No relative or `superclaude` import in any of the three. |
| 2 | `github` may import only `runner` and `predicates` (design 238) | PASS | `github.py:20-33`: `from .predicates import (...)`, `from .runner import CommandResult, Runner`. AST walk lists package imports for github.py as exactly `['.predicates', '.runner']`. Other imports are stdlib only (`json, re, collections.abc, dataclasses, datetime, email.utils, typing`). No third-party import. |
| 3 | Only `runner` may import `subprocess` | PASS | `grep -rlE subprocess` over src and tests lists `runner.py` (import at line 10) and `tests/issue_watch/test_runner.py` (a test, outside the module table). In the other src files the word appears only in docstrings (`runner.py:4`) and the `superclaude` word in `predicates.py:4`; no `importlib` or `__import__` anywhere. |
| 4 | No module is named `select` | PASS | Glob of the package: `__init__, runner, predicates, audit, github`. `git ls-files` for `select*` under `cli/` is empty. |
| 5 | Mandated 3.11-only grep, every hit justified | PASS | Literal `grep -rnE '<pattern>' src/superclaude/cli/issue_watch/ tests/issue_watch/` gives one source hit, `predicates.py:28`, a docstring sentence ("no ``fromisoformat``"), plus binary matches in two gitignored `predicates.cpython-311*.pyc` files (same docstring text; `.gitignore:2 __pycache__/`). No code use of any listed name. |
| 6 | Other 3.11+/3.12+ features (`Self`, `TaskGroup`, `typing.override`, exception notes, `fromisoformat` with `Z`) | PASS | Wide grep (Self, TaskGroup, override, add_note, ReprEnum, possessive and atomic regex, `enterContext`, `file_digest`, `Path.walk`, `is_junction`, `batched`, `delete=`, `UTC`, `type X =`, `def f[T]`, `Never`, `Required`, `LiteralString`) over src and tests: no code hit. `ast.parse(..., feature_version=(3, 10))` accepts all 11 `.py` files; no `Match` or `TryStar` node. Nested-quote f-strings (3.12 only): none. The one f-string with a call (`github.py:61`) reuses no quote. |
| 7 | Date parsing without `fromisoformat` on a trailing `Z` | PASS with finding 1 | `predicates.py:32` uses `strptime(text, "%Y-%m-%dT%H:%M:%SZ")`; `github.py:367` uses `email.utils.parsedate_to_datetime` and catches `TypeError, ValueError, IndexError, OverflowError`, which covers the 3.9/3.10 difference and the naive `-0000` result (`github.py:372` adds UTC). Strictness of `parse_utc` is finding 1. |
| 8 | LF line endings | PASS | `grep -c '\r'` over all `.py` and `.json` under both trees: 0 files. |
| 9 | Exactly one trailing newline on every non-empty file | PASS | Final two bytes of all 17 non-empty files read with `tail -c2`: every file ends `0a` and none ends `0a0a`. |
| 10 | No trailing spaces in `.py` and `.json` | PASS | `[ \t]+$` over both trees: no matches. |
| 11 | Both `__init__.py` files are zero bytes | PASS | `stat` size 0 for `src/superclaude/cli/issue_watch/__init__.py` and `tests/issue_watch/__init__.py` (`EMPTY` in the loop; `wc -l` 0). |
| 12 | No module binds a name from `superclaude.contracts.__all__` | PASS | `contracts/__init__.py:302-313` lists `ID_PATTERNS, CONVERGENCE_THRESHOLDS, GATE_FIELD_NAMES, THRESHOLDS, UnaddressedInvariant, AdversarialReturn, RETURN_CONTRACTS, ROADMAP_ENTITY_ID_FAMILIES, TOOL_WRITE_ROADMAP_ID_FAMILIES, roadmap_ids_pattern`. `arch_lint.py:88` loads exactly `__all__`; its rules are assign, literal and class (164-228). Grep for all ten names in src and tests: no match. |
| 13 | No string literal equals a requirement-id pattern body | PASS | Bodies at `contracts/__init__.py:71-76` (`M\d+-D-?\d+`, `FR-\d+(?:\.\d+)?`, `NFR-...`, `SC-\d+`, `G-\d+`, `D-?\d+`). Grep for `\d+` and `(?:\.` in src and tests: no match; the AST scan reports no `ID BODY LITERAL`. |
| 14 | Change-set inventory is accurate | PASS | Glob of both trees (pycache aside) lists the same 22 files; every `wc -l` count equals the table (0, 120, 292, 342, 901; 0, 103, 172, 629, 640, 1250; 5/14/14/27/7/7/7/37/30/27/42). |
| 15 | Docstring claims about boundaries, clock and I/O | FAIL (finding 1) | True: `predicates.py:3-4` (no I/O, imports nothing from superclaude), `github.py:7` ("reads no clock": no `.now(`, `time.` or `utcnow` in github.py), `runner.py:3-4` (only subprocess importer), `predicates.py:14` (`MARKER_JQ` built from `CLAIM_MARKER`, `github.py:59-62`). False: `predicates.py:28`, finding 1. |
| 16 | Behaviour under a real 3.10 interpreter | UNVERIFIABLE | `uv python list --only-installed` shows only 3.11.15 and 3.13.5; every `.pyc` tag is `cpython-311`. 3.10 compatibility rests on reading, the grammar parse and the greps above, not on a run. |

## Summary

- Checks passed: 14 / 16 (items 7 and 15 carry finding 1; item 16 is unverifiable)
- Checks failed: 1 (item 15)
- Critical issues: 0; blocking (IMPORTANT) issues: 1; minor notes: 9
- Issues fixed in-place: 0 (report only)

## Issues Found

### Blocking

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT (blocking: false claim) | `src/superclaude/cli/issue_watch/predicates.py:25-32` (`parse_utc`); tests `tests/issue_watch/test_predicates.py:541-553` | The docstring says "Raises ``ValueError`` for any other input". Running the function gave: `2026-11-07T12:00:00z` (lowercase z) parses; `2026-1-5T1:2:3Z` (unpadded fields) parses to `2026-01-05T01:02:03+00:00`; `٢٠٢٦-11-07T12:00:00Z` (Arabic-Indic digits) parses. `strptime` is lenient, so the "any other input" claim is false. Only four rejected shapes are pinned by tests (missing Z, numeric offset, space separator, empty). Impact is low because GitHub emits the canonical form, but a false claim is blocking under the severity rule. | Either narrow the docstring to the shapes the tests pin (and say `strptime` accepts unpadded fields), or add a strict ASCII `re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", text)` guard before `strptime` and add parametrized rows for `z`, unpadded and non-ASCII digits. |

### Minor notes (recorded, not rechecked, do not fail the gate)

| # | Location | Note |
|---|----------|------|
| 2 | `gate-a-change-set.md:39` | The G-8 command is shown as `shell=True\|os\.system`. Read literally with `-E`, `\|` is a literal pipe and the search would be vacuous. The evidence file `phase-outputs/test-results/p3-g8.txt` records the correct `shell=True|os\.system`, and my own run of that command printed nothing and exited 1. Citation-format only. |
| 3 | `audit.py:98` | `os.O_DIRECTORY` is POSIX-only. It is resolved at call time, so the module still imports elsewhere; the `platform_unsupported` reason in `REASON_TABLE` covers the intent. |
| 4 | `audit.py:105,117,199` | The module-level function `line` is shadowed by parameters named `line` in `_encode` and `AuditLog.append`. Style only. |
| 5 | `audit.py:331-332` | `stderr_fallback` accepts any `REASONS` member, including entry and note reasons such as `claimed` and `re-approved`, although it writes a `cycle` line. `line()` documents the same membership-only rule (`audit.py:202-204`), so this is consistent but loose. No spec line checked. |
| 6 | `runner.py:78-91` | A NUL byte in an argv item or in `cwd` makes `subprocess.run` raise `ValueError: embedded null byte` (probed: both cases raised). It is neither converted to `spawn_error` nor listed in the docstring, which names only `TypeError`. Callers pass labels and logins from config and `gh` output, so a validated cycle should not reach it; worth a test or a docstring line. |
| 7 | `github.py:1-3` | "Every argv is built here from module constants" is slightly wide: `argv_discover(trigger, login)` and the cursor argument add caller-supplied strings. The sentence two lines later is accurate. |
| 8 | `github.py:375-388` | `rate_limit_wait` documents that `now` must be timezone-aware but does not enforce it; a naive `now` would make `now.timestamp()` use local time. |
| 9 | `tests/issue_watch/test_audit.py:31`, `test_github.py:30` | Tests import helpers from `.conftest` instead of a plain helper module. It works because `tests/issue_watch/__init__.py` exists; only a pytest convention nit. |
| 10 | `tests/issue_watch/test_runner.py:51` | The fixture patches `subprocess.run` on the shared `subprocess` module object (through `runner_mod.subprocess`), so the patch is process-wide for the test's duration. `monkeypatch` restores it; no leak found. |

Not defects, checked and cleared: the added `cwd` keyword on `Runner.run` differs from the design signature at `docs/designs/issue-watcher.md:265` but is authorised by decision row DF-01 (`research/06-gap-fill-decisions.md:24`) and by design line 625; `tests/issue_watch/test_module_boundaries.py` does not exist yet because the task file creates it at Step 8.8, so boundary enforcement is by reading at this gate; `tests/issue_watch/test_predicates.py:14` imports `audit.REASONS`, which is a test and outside the module table.

## Actions Taken

None. Report only. No file other than this report was written. Probes ran in `-I -B` / `-B` mode with `PYTHONPATH` set only for read-only imports; no bytecode or cache was written by them.

## Recommendations

- Fix finding 1 (docstring or strict guard plus tests), then re-review only that item.
- If a 3.10 interpreter becomes available, run `uv run --python 3.10 pytest tests/issue_watch/` once; item 16 stays unverifiable until then.

## Confidence Gate

- **Confidence:** Verified: 15/16 | Unverifiable: 1 | Unchecked: 0 | Confidence: 100.0% (15 / (16 - 1)); the one unverifiable item is a real 3.10 run. The verdict is FAIL because of finding 1, not because of the confidence threshold.
- **Tool engagement:** Read: 17 | Grep: 25 | Glob: 5 | Bash: 8 (no web research; no Tavily or fallback calls)
- **Coverage limits, stated openly:** runner.py, predicates.py, audit.py, github.py, conftest.py and test_runner.py were read in full. test_predicates.py (lines 528-597 only), test_audit.py and test_github.py were checked for 3.11-only APIs by grep and by a 3.10-grammar AST parse, not read line by line.
- **UNVERIFIABLE:** item 16 (no CPython 3.10 interpreter installed; only 3.11 and 3.13).

## QA Complete
