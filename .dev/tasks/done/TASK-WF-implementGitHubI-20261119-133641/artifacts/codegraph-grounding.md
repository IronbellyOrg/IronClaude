# Codegraph grounding: TASK-WF-implementGitHubI-20261119-133641

## Run state

- index_state: fresh
- checked_at: 2026-11-19T13:38:11Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-669
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-669
- access: mcp (`codegraph_status`, `codegraph_search`, `codegraph_node`, `codegraph_callers` listed)
- tokens: none. Note: an index build (`codegraph init --yes`, started by the session hook) was running when the check began; the check waited for it to end (under 60 seconds) and then `codegraph_status` reported 0 added, 0 modified, 0 removed.
- Re-check note: this run writes only files under `.dev/tasks/` (not indexed: markdown). Rows about files the plan will change are leads only.

## Resolved symbols

The plan adds new files; it changes no existing symbol. What the source names, resolved:

| Source names | Resolved to | How |
|---|---|---|
| `src/superclaude/cli/install_skills.py:88-115` | `install_all_skills` (function, `install_skills.py:62`), loop over `available` skills at lines 83-115; `_has_corresponding_command` (`:40`), `skill_activation_targets` (`:35`), `list_installed_skills` (`:153`) | `codegraph_node` symbolsOnly, then Read lines 80-120 |
| `src/superclaude/cli/main.py:197-251` | calls `install_all_skills(force=force)` at line 206 and `install_all_skills(force=True)` at line 402 (inside `install` at line 46 and `update` at line 356 per the caller rows) | Grep on `main.py` |
| install code reading repo-root `scripts/` | none. `install_hooks.py:32-33, 548-550, 594-596` read `src/superclaude/scripts/` and `src/superclaude/hooks/scripts/` (package paths), never the repo-root `scripts/` | Grep on `src/superclaude/cli/install*.py` |
| `scripts/` (repo root) | exists: 19 entries (`README.md`, `ab_test_workflows.py`, `reflect_*.py`, `verify_deps.py`, ...). `scripts/README.md` describes build and version scripts only | Read, shell listing |
| `tests/` | `testpaths = ["tests"]`, `python_files = ["test_*.py"]`, `--strict-markers` (`pyproject.toml:107-117`). Subfolders carry `__init__.py` (for example `tests/issue_pipeline/`, `tests/pr_submit/`). Recorded responses live in `fixtures/` folders (for example `tests/issue_pipeline/fixtures/recorded/*.json`, `tests/pr_submit/fixtures/*.json`) | Glob, Grep |
| how a test loads a repo-root script | `tests/review/test_reflect_cluster_pairs.py:14-16`: `SCRIPT = ROOT / "scripts" / "<name>.py"` then `importlib.util.spec_from_file_location(...)` and `module_from_spec` | Grep |
| ruff scope | line length 88, `target-version py310`, rules `E,F,I,N,W,TID` (`pyproject.toml:174-190`); `scripts/` and `tests/` are linted | Grep |
| name collision for `merged_pr_log` | none in `scripts/`, `src/`, `tests/` (only `.dev/issues/669/` files mention it) | Grep |
| Jay's generator `build-fleet-daily-digest.py` | stdlib-only, REST through `urllib.request`: `token` (:72), `gh_get` (:82), `gh_list` (:96), `parse_iso` (:119), `to_local_day` (:128), `fetch_merged_prs` (:132), `fetch_issue_churn` (:171, drop), `bucket_all` (:204), `day_summary_title` (:230, drop), `build_markdown` (:838), `build_html` (:913), `build_daily_ics` (:1265, drop), `main` (:1311); agent-from-title code `extract_agents_and_clean` (:622) and the `_AGENT_*` patterns, `AGENT_LOGO`, `agent_icons_html` etc. (drop); imports `select_public_repos`, `PUBLIC_REPOS` (public allowlist, drop). Config by environment: `DIGEST_LOOKBACK_DAYS` 21, `DIGEST_TZ` America/Chicago, token from `FLEET_GITHUB_TOKEN` or `GITHUB_TOKEN`. UNVERIFIED line numbers: read through a summarizing fetch of the raw file, not opened directly | WebFetch of the raw file |
| ClickUp write | `PUT /v3/workspaces/{workspace_id}/docs/{doc_id}/pages/{page_id}`, body `content`, `content_format` `text/md`, `content_edit_mode` `replace` (hosting research). The path needs a Doc id as well as the page id | Read of the hosting research |
| first attempt (reference only) | `tools/merged_pr_log/credit.py` credits the PR author and treats `[bot]` and `app/` logins as bots; the new rule replaces that logic | Read |

## Dependents

Nothing in the plan edits an existing symbol, so there is no blast radius to size tasks by. The install path must stay exactly as it is. Its dependents, which must keep working unchanged:

| Symbol | Dependent | Resolution |
|---|---|---|
| `install_all_skills` | `src/superclaude/cli/main.py` line 206 (`install`) and line 402 (`update`) | call-site-verified (Grep) |
| `install_all_skills` | `tests/unit/test_cli_install.py:683, :713, :787, :942` | def-line (leads) |
| `install_all_skills` | `tests/unit/test_cli_doctor.py:73` | def-line (lead) |
| `install_all_skills` | `tests/troubleshoot/test_diagnostic_worker_contract.py:411` | def-line (lead) |

shown/total: 10/10 caller rows (the two import rows are file rows). The new script has no dependents; no file imports it.

## Pre-check

Checked 2026-11-19 after the gate passed (Bash `test -e`, Read, Grep; no new readiness check). The plan was not edited.

| Task | Named item | Result |
|---|---|---|
| Constraints, Task 1, 6 | `src/superclaude/cli/install_skills.py`, `src/superclaude/cli/main.py`, the 15 `src/superclaude/cli/install_*.py` modules | exist; none reads the repo-root `scripts/` folder (only `src/superclaude/scripts/` and `src/superclaude/hooks/scripts/`) |
| Task 1 | `tests/review/test_reflect_cluster_pairs.py` lines 14-16 | exist and match the quoted loading pattern (`ROOT / "scripts" / ...`, `spec_from_file_location`, `module_from_spec`, `exec_module`) |
| Task 1 to 6 | new paths `scripts/merged_pr_log.py`, `scripts/merged_pr_log_orca_automation.md`, `tests/merged_pr_log/` | all free (do not exist yet) |
| Task 6 | `sys.stdlib_module_names` | present on the project's Python (3.10.20, `hasattr` true); the project floor is 3.10 |
| Task 1, 3, 4 | Jay's functions (`token`, `gh_get`, `gh_list`, `fetch_merged_prs`, `bucket_all`, `build_markdown`, `build_html`, `main`, and the drop list) | UNVERIFIED line numbers and names: taken from a summarizing fetch, not an opened file; Task 1's Constraints line tells the executor to read the original first |
| Task 5 | Orca automation file format | not confirmed in this repo (no automation definitions exist; Orca commands are blocked in this session's launch level), so the definition lists the fields a person enters |

Dependents of touched symbols not named by any task: none. No existing symbol is changed. The Orca automation format and the ClickUp plan are open items for the human steps, not graph findings.

Count: 6 tasks checked, 0 failed, 2 UNVERIFIED notes.
