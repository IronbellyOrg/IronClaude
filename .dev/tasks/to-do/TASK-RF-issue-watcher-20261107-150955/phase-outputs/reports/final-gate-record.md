# Final gate record (date: 2026-11-08)

All results below were produced after the Final-gate fix cycle (the p9-* files were overwritten by the re-run). The detect-secrets hook (cached offline in ~/.cache/pre-commit, run by the Final-gate verifiers) and markdownlint 0.38.0 on the runbook also exit 0.

| Gate | Command | Exit | Verdict |
|---|---|---|---|
| G-1 | `uv run pytest tests/issue_watch/ -v` | 0 (2635 passed, 0 skipped) | PASS |
| G-2 | `uv run pytest tests/issue_watch/ tests/skills/test_model_alias_policy.py tests/docs/test_retired_docs_absent.py tests/cli/test_cli_registration.py tests/swarm/test_cli_registration.py tests/recommend/test_cli_registration.py -v -rs` | 0 (2665 passed, 1 pre-existing skip outside this change set) | PASS |
| G-3 | `uv run --offline --with "pytest-xdist>=3.5,<4" pytest -n auto tests/issue_watch/` | 0 (2635 passed, 0 skipped) | PASS |
| G-4 | `make lint` | 0 (5 pre-existing warnings, none in issue_watch) | PASS |
| G-5 | `uvx --offline ruff@0.15.20 check` and `format --check` on the package, main.py and tests, then `format --check src/ tests/` | 0, 0, 0 (31 and 1234 files already formatted) | PASS |
| G-6 | `make verify-deps`; `make sync-dev` (preparation); `make verify-sync` | 0, 0, 0 (all components in sync; nothing under src/superclaude/{skills,agents,commands,hooks,templates} changed) | PASS |
| G-7 | grep of Python 3.11+ APIs over the package and tests | 1 hit, a docstring (predicates.py:30), justified in p9-g7.txt | PASS |
| G-8 | `grep -rnE 'shell=True\|os\.system' src/superclaude/cli/issue_watch/` | 1 (NO_MATCH) | PASS |
| G-9 | `uv run superclaude issue-watch --help` | 0 (exactly check-config, init-state, once, reset, status) | PASS |
| G-10 | `git diff --exit-code pyproject.toml Makefile`; `git diff --exit-code -- .github/`; staged `.claude/` paths | 0, 0, 0 staged .claude/ paths | PASS |
| G-11 | trailing-space, CR and final-newline checks (48 files) | no hit, 0 problems | PASS |

Statements required by the plan:
- full suite: CI only (the whole `make test` run is left to CI, decision DF-05).
- pre-commit hooks are not run as a whole locally. G-11 covers only trailing spaces, CR and the final newline; it is not a stand-in for the secret scan or markdownlint. Those two were run by hand, offline, in the Final-gate fix pass (see "Final-gate fix pass" below); the other hooks are covered by the fixture JSON parse test and the runbook reading (decisions DF-32 and DF-58).

## Final-gate fix pass (cycle 1, findings F-1 to F-10)

The Final gate found that the first version of this record overstated the hook coverage. After the fixes, these were run again:

| Gate | Command | Exit | Verdict |
|---|---|---|---|
| G-1 | `uv run pytest tests/issue_watch/ -q` | 0 (2635 passed, 0 skipped; 2628 before plus 7 new cases) | PASS |
| G-2 | the G-2 command above | 0 (2665 passed, 1 pre-existing skip outside this change set) | PASS |
| G-3 | the xdist command above | 0 (2635 passed) | PASS |
| G-4 | `make lint` | 0 (0 errors, 5 pre-existing warnings) | PASS |
| G-5 | `uvx --offline ruff@0.15.20 check` and `format --check` on `src/superclaude/cli/issue_watch`, `tests/issue_watch`, `main.py`; `format --check src/ tests/` | 0, 0, 0 (31 and 1234 files already formatted) | PASS |
| G-12 | `detect-secrets-hook` 1.5.0 (offline, `uvx --offline --from detect-secrets`) with a /tmp copy of `.secrets.baseline` (only its version stamp 1.4.0 changed to 1.5.0), over the 49 `.py`/`.json` files of the package and tests plus `main.py` and the two design documents | 0 (before the fix: exit 1, three hits: `test_cli.py`, `test_cycle.py`, `test_origin_parity.py`) | PASS |
| G-13 | markdownlint 0.38.0 from `~/.cache/pre-commit` with the repo `.markdownlint.json`, on a /tmp copy of `docs/designs/issue-watcher-setup.md` (no `--fix`) | 0 | PASS |

The three secret-scanner hits were test strings (`secret = "..."` twice, a `user:token@` URL once); each now carries the repo's own `# pragma: allowlist secret` convention. `.secrets.baseline` is unchanged.

Additional facts: a real Python 3.10.20 interpreter was found during Gate D and the whole tests/issue_watch suite passed on it (2635 passed); the plan text saying none exists is stale. The Python floor was therefore verified by running, not only by grep.
