# Gate A change set (Phases 2 and 3)

Files discovered by Glob on 2026-11-07 (__pycache__ build artifacts excluded); line counts from `wc -l`.

| Path | Lines | Created by step |
|---|---|---|
| `src/superclaude/cli/issue_watch/__init__.py` | 0 | 1.6 |
| `src/superclaude/cli/issue_watch/runner.py` | 120 | 2.1 |
| `src/superclaude/cli/issue_watch/predicates.py` | 292 | 2.2 |
| `src/superclaude/cli/issue_watch/audit.py` | 342 | 2.3 |
| `src/superclaude/cli/issue_watch/github.py` | 901 | 3.1a-3.1c |
| `tests/issue_watch/__init__.py` | 0 | 1.7 |
| `tests/issue_watch/conftest.py` | 103 | 2.4 |
| `tests/issue_watch/test_runner.py` | 172 | 2.5 |
| `tests/issue_watch/test_predicates.py` | 629 | 2.6-2.7 |
| `tests/issue_watch/test_audit.py` | 640 | 2.8 |
| `tests/issue_watch/test_github.py` | 1250 | 3.6-3.7 |
| `tests/issue_watch/fixtures/_assumed_shape/gh_api_user_include.json` | 5 | 3.2-3.5 |
| `tests/issue_watch/fixtures/_assumed_shape/gh_graphql_insufficient_scopes.json` | 14 | 3.2-3.5 |
| `tests/issue_watch/fixtures/_assumed_shape/gh_graphql_rate_limited.json` | 14 | 3.2-3.5 |
| `tests/issue_watch/fixtures/_assumed_shape/gh_issue_list.json` | 27 | 3.2-3.5 |
| `tests/issue_watch/fixtures/_assumed_shape/gh_stderr_auth_401.json` | 7 | 3.2-3.5 |
| `tests/issue_watch/fixtures/_assumed_shape/gh_stderr_rate_403.json` | 7 | 3.2-3.5 |
| `tests/issue_watch/fixtures/_assumed_shape/gh_stderr_rate_429.json` | 7 | 3.2-3.5 |
| `tests/issue_watch/fixtures/_assumed_shape/graphql_edits.json` | 37 | 3.2-3.5 |
| `tests/issue_watch/fixtures/_assumed_shape/graphql_project_items.json` | 30 | 3.2-3.5 |
| `tests/issue_watch/fixtures/_assumed_shape/rest_comments_marker.json` | 27 | 3.2-3.5 |
| `tests/issue_watch/fixtures/_assumed_shape/rest_events_page.json` | 42 | 3.2-3.5 |

## Gate commands run in Phases 2 and 3

| Gate | Command | Exit | Result | Source |
|---|---|---|---|---|
| G-1 (P2) | `uv run pytest tests/issue_watch/ -v` | 0 | PASS, 183 passed | test-results/p2-g1-summary.md |
| G-5 (P2) | `uvx --offline ruff@0.15.20 check` and `format --check` on the 9 Phase 2 files | 0 and 0 | PASS | test-results/p2-ruff.txt |
| G-1 (P3) | `uv run pytest tests/issue_watch/ -v` | 0 | PASS, 373 passed | test-results/p3-g1-summary.md |
| G-4 (P3) | `make lint` | 0 | PASS (5 architecture warnings, none in issue_watch) | test-results/p3-g4-summary.md |
| G-5 (P3) | pinned ruff check and format --check on github.py, test_github.py, conftest.py | 0 and 0 | PASS | test-results/p3-ruff.txt |
| G-8 (P3) | `grep -rnE 'shell=True\|os\.system' src/superclaude/cli/issue_watch/` | 1 | NO_MATCH | test-results/p3-g8.txt |

Also: `reviews/p2-leaf-imports.md` (Step 2.9) PASS.

## Decision rows applied

DF-01, DF-02, DF-03, DF-14, DF-16, DF-18, DF-19, DF-21, DF-22, DF-28, DF-30, DF-33, DF-35, DF-37, DF-41, DF-48, DF-55, DF-57.

## Design line ranges implemented

D 218-224, 252-265, 494-505, 537-602, 697-722.
