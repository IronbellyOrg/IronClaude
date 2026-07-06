# QA Report — Final-Phase M3 Gate: Core-Purity (NFR-6) Domain Lens

**Topic:** pr_submit V1.1 complete change-set — core-purity (NFR-6) verification
**Date:** 2026-06-12
**Phase:** report-validation (domain lens — core-purity)
**Fix authorization:** false (report only — nothing modified)
**Web search:** none (not required; all claims local)

---

## Overall Verdict: PASS

NFR-6 holds across the complete pr_submit V1.1 change-set. Zero EXECUTABLE
`gh`/`git`/`subprocess`/`os.system`/`popen` tokens exist in any `pr_submit/*.py`.
`auggie-fallback.md` carries zero `gh`/`git` word tokens. The gh-bearing
re-trigger surfaces are correctly excluded from `CORE_PURE_FILES` and are
fork-pinned. All 9 `test_static_grep.py` tests pass.

The adversarial hunt found NO NFR-6 violation. Every `gh`/`git`/`token` match in
the core is docstring prose, an NFR-7 credential-*redaction* regex, or a comment —
none is executable.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Zero executable gh/git in `pr_submit/*.py` | PASS | `grep \bgh\b\|\bgit\b` → 6 hits, all docstring/comment/regex prose (see classification table) |
| 2 | Zero subprocess/os.system/popen/Popen executable | PASS | `grep` for import/use → only `import os` (run_log.py:20), used solely for `os.fsync` (line 122), no process exec |
| 3 | auggie-fallback.md ZERO gh/git word tokens | PASS | `grep \bgh\b\|\bgit\b auggie-fallback.md` → EXIT 1 (no match). The 2 broad-grep hits were "zero-token"/"shell token" (the word "token", not gh/git) |
| 4 | 3 core-pure .py files (fsm/severity_router/loop_guard) zero gh/git | PASS | `grep \bgh\b\|\bgit\b` over all 3 → EXIT 1 (none) |
| 5 | review-retrigger.md NOT in CORE_PURE_FILES | PASS | test_static_grep.py:27-40 — `CORE_PURE_FILES` list excludes it; comment 31-35 documents deliberate exclusion |
| 6 | retrigger-review.sh NOT in CORE_PURE_FILES | PASS | Not present in CORE_PURE_FILES list (27-40); covered by T-104/T-1101 fork-pin path instead |
| 7 | retrigger `gh api` fork-pinned | PASS | retrigger-review.sh:35 `repos/IronbellyOrg/IronClaude/issues/${PR}/comments`; review-retrigger.md:25 same fork path. `gh api` takes no `--repo` — path-pin is correct form |
| 8 | Static-grep test suite green | PASS | `uv run pytest tests/pr_submit/test_static_grep.py -q` → 9 passed in 0.03s |

---

## Classification of every gh/git/token match in `pr_submit/*.py`

| file:line | Token | Classification | Verdict |
|-----------|-------|----------------|---------|
| `__init__.py:13` | ``gh``/``git`` | Module docstring asserting purity | Prose — allowed |
| `__init__.py:14` | ``gh``/``git`` I/O | Module docstring | Prose — allowed |
| `run_log.py:9` | token/credential | NFR-7 docstring | Prose — allowed |
| `run_log.py:38` | credential/token | Comment above redaction patterns | Comment — allowed |
| `run_log.py:41` | `gh[pousr]_[A-Za-z0-9]{16,}` | NFR-7 credential-**redaction** regex (scrubs gh PATs *out* of logs — anti-credential) | Regex literal, defensive — allowed |
| `run_log.py:46` | `(password\|...\|token\|...)` | NFR-7 redaction regex | Regex literal, defensive — allowed |
| `run_log.py:60` | credential/token | Docstring of `_redact` | Prose — allowed |
| `classifier.py:30` | ``gh pr view --json reviews`` | Docstring documenting upstream JSON shape (no call) | Prose — allowed |
| `classifier.py:76` | no ``gh``/``git`` tokens | Docstring asserting purity | Prose — allowed |
| `models.py:11` | ZERO ``gh``/``git`` tokens | Module docstring | Prose — allowed |
| `detection.py:77` | token set | Comment (trigger-phrase set) | Comment — allowed |
| `fsm.py:961,978,981` | trigger token / outcome token | Comments (the word "token", not gh/git/credential) | Comment — allowed |

**No executable command, no subprocess spawn, no os.system/popen.** `import os`
(run_log.py:20) is filesystem-only (`os.fsync`, run_log.py:122).

---

## Summary

- Checks passed: 8 / 8
- Checks failed: 0
- Critical issues: 0
- Offender file:line: NONE

## Issues Found

None.

## Recommendations

- None. Core-purity domain is clean for the M3 final gate.
- The `run_log.py:41` `gh[pousr]_` regex is a *defensive* NFR-7 redaction pattern,
  not a purity violation — its presence is correct and required. Do not "fix" it.

---

## Confidence Gate

- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 1 | Grep: 9 | Glob: 0 | Bash: 6 (each grep/bash mapped to a specific check; pytest run = check 8)
- Every checklist item carries direct tool evidence (grep output line, test result, or file:line).

## QA Complete
