# QA Report — Content QA: UV-Discipline (doc-qualitative, adversarial)

**Topic:** UV-only discipline across Phase 5 test-results + tests/troubleshoot/backtest/
**Date:** 2026-06-12
**Phase:** doc-qualitative (content QA, adversarial stance)
**Fix cycle:** N/A
**Fix authorization:** false (report-only — NO source files modified)

---

## Overall Verdict: PASS

Adversarial stance assumed at least 2 UV-violating commands existed. After exhaustive
grep + read across every Phase-5 test-results doc and all 20 backtest `.py` source files,
**zero violations were found.** The single `sys.executable` subprocess is the documented
NOTE case and is verified acceptable. The 0-finding outcome is backed by the explicit
verification trail below (every Python/pip/pytest invocation token was grepped and inspected),
not by an absence of looking.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Phase-5 pytest command uses `uv run` | PASS | `pytest-backtest-summary.md:3` `**Command:** \`uv run pytest tests/troubleshoot/backtest/ -v\``; `phase-5-inventory.md:10` raw output is "`uv run pytest ...` (exit 0)" |
| 2 | Phase-5 ruff commands use `uv run` | PASS | `phase-5-inventory.md:27-28` `uv run ruff check` + `uv run ruff format --check`; `pytest-verdict.md` only references the summary, emits no bare command |
| 3 | No `python -m` anywhere in backtest .py | PASS | grep `-E "python -m|python3"` over `tests/troubleshoot/backtest/ --include=*.py` → NO MATCHES |
| 4 | No `pip` / `pip install` invocation | PASS | grep `-E "pip install\|pip3 "` → NO MATCHES; report scripts (`catch_rate.py`, `catch_rate_report.py`, `conftest.py`) grep for `python\|pip` → NO MATCHES |
| 5 | No bare `pytest` shell invocation (CLI/`__main__`) | PASS | grep `-E "__main__\|argparse\|sys.argv"` → NO MATCHES. All `pytest` references are the imported `pytest` module / `pytest.mark` / `pytest.raises` / `pytest.fixture` decorators — library API use, not a shell invocation |
| 6 | git subprocess calls invoke `git`, not Python | PASS | `git_replay.py:78,103,131,146,188,205,218` — every argv list begins with `"git"` (`rev-parse`, `cat-file`, `worktree`); `test_git_replay_integration.py` subprocess.run calls are git probes (lines 24,41,71,79) |
| 7 | The lone Python subprocess does not bypass UV (NOTE) | PASS (NOTE) | `replay_executor.py:228` `[sys.executable, "-c", prelude + snippet]`. `sys` imported stdlib at line 31. `sys.executable` = the exact interpreter `uv run` launched (per `pytest-backtest-output.txt:3` → `.venv/bin/python`). NOT a fresh `python`/`pip` shell-out. Assessment: acceptable, does NOT FAIL — see NOTE below |

---

## Summary
- Checks passed: 7 / 7
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (report-only)

---

## Issues Found

None. No UV-discipline violations of any severity.

---

## NOTE — `sys.executable -c <snippet>` in replay_executor.py:228 (acceptable, NOT a violation)

**Pattern:** `run_prefix_replay_snippet()` runs a pre-fix code snippet in a fresh subprocess via
`_subprocess.run([sys.executable, "-c", prelude + snippet], ...)` (line 228).

**Why it is NOT a UV bypass (verified):**
- `sys.executable` resolves to the SAME interpreter the UV-managed test process is already
  running under. `pytest-backtest-output.txt:3` confirms that interpreter is
  `/config/workspace/.../.venv/bin/python` — i.e. the project venv that `uv run` activates.
  Spawning `sys.executable` therefore re-enters the identical UV environment; it would behave
  identically under `uv run pytest` (which is exactly how it was exercised).
- It is NOT a bare `python` / `python3` / `pip` shell-out (those would resolve via `PATH` and
  could escape the venv). It is the absolute interpreter path of the live process.
- The prelude (`replay_executor.py:220-226`) inserts the parent worktree's `src/` onto
  `sys.path[0]` and purges inherited `superclaude` modules — this is the deliberate mechanism for
  loading PRE-FIX code from the parent tree (per the docstring at lines 207-217, NFR-3). The
  environment (venv, installed deps) stays UV-managed; only the `superclaude` import root is
  redirected. No new Python environment is created.

Conclusion: per the task's own guidance, this is reported as a NOTE and is NOT failed — it does
not bypass the UV environment in any way that would break under `uv run`.

---

## Actions Taken

None — report-only (`fix_authorization: false`). No source file modified.

---

## Self-Audit (INV-019 — Reliance vs Verification)

**(a) Reliance list — items relied on without independent re-derivation:**
- Relied on the Phase-5 summary's GREEN verdict ONLY for the green/skip counts (not for UV
  discipline). The UV-command claims were re-verified independently against the raw docs, not
  taken on the summary's word.

**(b) Independent semantic checks (≥1 required):**
- Verified the literal `uv run` prefix on the pytest command by reading
  `pytest-backtest-summary.md:3` and `phase-5-inventory.md:10` directly (Read tool), not by
  trusting the verdict file.
- Verified the lone Python subprocess is venv-bound by cross-referencing `replay_executor.py:228`
  (`sys.executable`) against `pytest-backtest-output.txt:3` (interpreter = `.venv/bin/python`) —
  two independent files corroborate that `sys.executable` ≠ a PATH `python` shell-out.
- Verified the seven `_subprocess.run` argv lists in `git_replay.py` all begin with `"git"`
  (grep + line citations 78/103/131/146/188/205/218), proving no test shells out to a non-UV
  Python entrypoint.

**Confidence Gate:**
- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: 6 | Glob: 0 | Bash: 8 (grep/find via Bash)
- Tool-engagement summary (web research): none performed — all verification was local-file-bound;
  Tavily not invoked (not required).
- Self-audit question 1: 9 distinct factual claims independently verified against source.
- Self-audit question 2: files read — `pytest-backtest-summary.md`, `ruff-backtest-output.txt`,
  `phase-5-inventory.md`, `pytest-backtest-output.txt`, `pytest-verdict.md`,
  `replay_executor.py` (lines 195-249, 27-31), plus grep across all 20 backtest `.py` files.
- Self-audit question 3: the 0-finding result is trustworthy because every UV-violation token
  class (`python -m`, `python3`, `pip`, `pip3`, bare `pytest` shell invocation, `__main__`,
  `argparse`, `sys.argv`, `os.system`, `popen`) was explicitly grepped and returned NO MATCHES,
  and the one real Python subprocess was traced to the venv interpreter.

---

## Recommendations

- No action required. UV discipline is fully satisfied across the Phase-5 test-results docs and
  the entire `tests/troubleshoot/backtest/` suite.

## QA Complete
