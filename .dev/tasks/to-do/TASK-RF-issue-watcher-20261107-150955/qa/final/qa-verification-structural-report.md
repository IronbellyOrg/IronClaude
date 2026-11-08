# QA Report: Final gate, structural verification (cycle 1 fixes)

**Topic:** issue-watch implementation (issue 331), Final gate
**Date:** 2026-11-08
**Phase:** fix-cycle verification (structural), `fix_authorization: false`
**Fix cycle:** 1

---

## Overall Verdict: PASS

All ten blocking findings (F-1 to F-10) are FIXED in the repository files, and no new blocking structural issue was found. Everything below was run or read by me; I did not rely on the fix report.

## Per-finding verification

| id | Result | Evidence |
|---|---|---|
| F-1 (detect-secrets) | FIXED | `grep -n "pragma: allowlist secret" tests/issue_watch/*.py` shows the pragma at `test_cli.py:633`, `test_cycle.py:381`, `test_origin_parity.py:55`. `uvx --offline --from detect-secrets detect-secrets-hook` (1.5.0, /tmp copy of `.secrets.baseline` with the version stamp 1.4.0 changed to 1.5.0) over the 49 `.py`/`.json` files of the package and tests plus `main.py` and both design docs: exit 0. Negative control (`secret = "SECRET-PROJECT-VALUE"` in a /tmp file): exit 1. `final-gate-record.md` line 21 no longer claims G-11 covers the hooks; it says G-11 covers only trailing spaces, CR and the final newline, and lists G-12 (detect-secrets) and G-13 (markdownlint). `.secrets.baseline` has no `git diff`. |
| F-2 (`lock_missing` vs `store_missing`) | FIXED | Runbook line 156 (section 5), line 336 (10.1 item 6) and the 10.2 rows at 398-399 now say a new-setup cycle ends `lock_missing` and `store_missing` needs an existing lock. Code agrees: `cycle.py:675-683` takes the lock before `_load` (`cycle.py:695`); `record.py:392-395` raises `lock_missing`; `record.py:357-358` raises `store_missing`; `validate_setup` (`cycle.py:352-358`) never touches `state_dir`; `record.py:773-775` makes `init-state` refuse if either file exists. |
| F-3 (precedence 7 with 5/3) | FIXED | Runbook line 340 states the precedence rule and that a 7 ends the cycle's work. Code agrees: `_cond` is called only from `_fail` (`cycle.py:1002`; callers 1026, 1030) and at 1071 and 1074, all inside `_launch`; `_launch` sets `c.launching` (1009), `_candidates` then sets `self.halt` (814-815) and `_candidates` is the last step of `_steps` (718), so only `_commit` (exit 6) can follow. The "7 with 5 / 7 with 3 occur in practice" sentence is gone. |
| F-4 (stale report statements) | FIXED | `deviation-register.md` DF-05 row (line 13) and Table 3 note (line 60) now point at `final-gate-record.md` line 20, which holds "full suite: CI only" (verified). `final-change-set.md` line 178 quotes the register verbatim. `ac-trace.md` last paragraph says Steps 9.4 to 9.16 were re-run after the docstring edits and that `final-gate-record.md` states it. No "does not exist yet" or "Pending Step 9.19" text remains (Grep). |
| F-5 (Q19 retry only for `unknown`) | FIXED | New `test_status_retry_lists_only_unknown_entries_with_an_id_and_a_cwd__ac9_fr015` (`test_cli.py:885`) with `launched`, `claimed`, `abandoned` and `unknown` entries, JSON and text assertions. I applied mutant Q19 on a /tmp copy: the test fails (KILLED). |
| F-6 (C49/V19 `considered` pruning) | FIXED | New tests `test_cycle.py:3609` (idle cycle) and `:3638` (all `budget_exhausted`). Mutant C49 on a /tmp copy: `test_an_idle_cycle_does_not_prune_the_considered_map__fr023` fails (KILLED). |
| F-7 (V21 `consumed_log` pruning) | FIXED | New `test_cycle.py:3623`. Mutant V21 (`self.doc = doc`): that test fails (KILLED). |
| F-8 (K13 `once` platform) | FIXED | New `test_cli.py:654-668`, parametrized `real` and `dry_run`, asserts exit 2, `platform_unsupported` and no `build_deps` or `run_cycle` call. Mutant K13 (`platform=False`): the `real` case fails (KILLED). |
| F-9 (R4/R20 inode compare) | FIXED | `test_record.py:790-828` has the third `swap` value `rename_aside` (`os.rename` then a fresh file at the path, so `st_nlink` stays 1). Mutant R4 (`if False:` in place of the `(st_dev, st_ino)` compare, `record.py:411`): `...[rename_aside]` fails (KILLED). |
| F-10 (14.1 `once` with `enabled: true`) | FIXED | Runbook line 587 now says to launch the test by hand while `enabled` is `false` and not to run a real `once` with `enabled: true`; `enabled` changes to `true` only in section 8.6 (line 274). Lines 5 and 580 are consistent. No remaining text allows `enabled: true` before the live test (Grep `enabled.{0,40}true`: lines 222, 226, 274, 277, 560 only, all consistent). |

After the mutation runs `diff -r` of the real `src/` and the /tmp copy printed no difference (the copy was restored, and the repository was never mutated).

## Structural checks run by me

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | `uv run pytest tests/issue_watch/ -v -rs` (uid 1000, non-root) | PASS | 2635 passed, no skipped line, no failures |
| 2 | `uv run --offline --with "pytest-xdist>=3.5,<4" pytest -n auto -rs tests/issue_watch/` | PASS | 2635 passed, zero skips |
| 3 | Real CPython 3.10.20 (`uv venv --python 3.10` in /tmp, pytest, click and pure-Python libs, `superclaude/src` on a `.pth`, a stub `jsonschema`), whole `tests/issue_watch/` with `-p no:cacheprovider` | PASS | 2635 passed, including the three subprocess e2e tests |
| 4 | Python 3.11+ API grep over package and tests | PASS | One hit, the docstring at `predicates.py:30` ("no ``fromisoformat``"); no call |
| 5 | `make lint` | PASS | "All checks passed!", 0 errors, 5 pre-existing warnings |
| 6 | `uvx --offline ruff@0.15.20 check` on `src/superclaude/cli/issue_watch`, `tests/issue_watch`, `main.py` | PASS | All checks passed |
| 7 | `uvx --offline ruff@0.15.20 format --check` on the same paths, and on `src/ tests/` | PASS | 31 files and 1234 files already formatted |
| 8 | `uv run superclaude issue-watch --help` | PASS | Lists exactly check-config, init-state, once, reset, status |
| 9 | G-2 command (issue_watch plus five registration test files) | PASS | 2665 passed, 1 skipped (`tests/swarm/test_cli_registration.py:127`, pre-existing) |
| 10 | markdownlint 0.38.0 (`~/.cache/pre-commit`) with the repo `.markdownlint.json` on /tmp copies of `issue-watcher-setup.md` and `issue-watcher.md` | PASS | exit 0 |
| 11 | Imports against design lines 233-242 | PASS | Read of every import line in the package: `runner`, `predicates`, `audit` import nothing from `superclaude`; `github`, `launch`, `cycle`, `cli` import only the listed modules; `record` imports `predicates` and `swarm.atomic` lazily (the known minor note F-25, unchanged); `test_module_boundaries.py` passes |
| 12 | File hygiene over 57 package, test, design and report files | PASS | No CR, no BOM, every file ends with exactly one newline. Trailing spaces only in `.md` reports under `.dev/` (`final-change-set.md`, `gate-c-change-set.md`), which the pre-commit `trailing-whitespace` hook (`.md` excluded) and `markdownlint` (`\.dev/.*` excluded) skip |
| 13 | `git status`: nothing outside the allowed set | PASS | Tracked change is only `src/superclaude/cli/main.py` (the two registration lines) plus the task file; untracked are `src/superclaude/cli/issue_watch/`, `tests/issue_watch/`, `docs/designs/issue-watcher*.md`, `.dev/...`. No change to `pyproject.toml`, `Makefile`, `.github/`, `.claude/`, `uv.lock`. No staged `.claude/` path. `docs/designs/issue-watcher.md` mtime (2026-11-07 15:08) predates the fix. No `.pyc` untracked |

## New blocking findings

None.

## Minor notes (not rechecked, do not fail the gate)

- `.secrets.baseline` has a newer mtime than the consolidated findings but no content difference (`git diff` is empty). Probably the fix agent's run against the repo copy rewrote the version stamp and restored it. No action.
- `final-change-set.md` and `gate-c-change-set.md` hold whitespace-only lines; both hooks that would care exclude them.
- The 3.10.20 run needed a stub `jsonschema` and a `.pth` to the repo `src` (a harness detail, same as Gate D); the e2e tests need `superclaude` importable from the interpreter's own site.

## Confidence

**Confidence:** Verified: 23/23 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (10 finding rows plus 13 structural checks)
**Tool engagement:** Read: 14 | Grep: 8 | Glob: 0 | Bash: 31

## QA Complete
