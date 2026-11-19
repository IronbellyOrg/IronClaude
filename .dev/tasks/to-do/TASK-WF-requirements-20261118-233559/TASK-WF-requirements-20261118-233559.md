---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-requirements-20261118-233559
version: "1"
priority: Medium
created_date: "2026-11-18"
---

# Zero-setup issue watcher: status gate, per-status commands, repo threading, config generator and dispatcher loop

Source: ./source.md
Goal: The issue watcher can be switched on in any workspace with no per-user setup: it acts only on the allowed Project statuses, picks its command from the issue's Status and its reach from the Project's Pipeline field, serves every Orca repo through one dispatcher that cron can run, and writes each repo's configuration, approvers and labels itself.

## Constraints

- Scope is the IronClaude repository only. The Coder template work (requirements R1, R6, R9, R10, R17, R20, R21; Coder issues 515 and 516) is not implemented here; Task 19 hands it over with exact values.
- Edit `src/superclaude/`, then run `make sync-dev` and `make verify-sync`. Never edit or stage anything under `.claude/` (only `.claude/settings.json` is tracked).
- Python only through UV (`uv run pytest`, `uv run ruff`). Tests use the faked `gh` and Orca runners already in `tests/issue_watch/conftest.py`; no task runs the watcher against the real GitHub or Orca, except read-only checks named in a task.
- `src/superclaude/cli/issue_watch/github.py` stays read-only: no mutation, no POST to a REST path (security invariant NG-2, `tests/issue_watch/test_security_invariants.py`). Anything that writes to GitHub (creating labels) lives in a new module outside `github.py`.
- The approval label, the allowed Project Status and the "edited after approval" refusal (`predicates.py`) stay the gate. Nothing in this plan removes or auto-satisfies them.
- The term is "coordinator", never "orchestrator". The coordinator branch and worktree are both named `Coordinator`; the session is named `COORD-<RepoName>`.
- Do not switch any real watcher on, claim a real issue, install a real cron entry or start a worker for a real issue. Each generated config starts with `enabled: false` and only the automatic first-run check of Task 13 may turn it on.

## Phase 1: Status gate and Project field reads

## Task 1: Replace the Backlog check with a Status allow-list

In `src/superclaude/cli/issue_watch/predicates.py`, change `project_check` (lines 262 to 271) so an issue passes only when it is the one live item of the configured Project and its Status name is one of `Research`, `Spec`, `Plan` or `Debug` (requirement R22). Every other value, including `Backlog`, `Ready`, `In progress`, `In review`, `Done`, an empty Status and any status added to the board later, returns `project_mismatch`. Keep the reason code `project_mismatch` (it is in `audit.REASON_TABLE`, `audit.py` line 72) so no reason table changes. Name the allowed set as one module constant. The callers `cycle.py` lines 958 (`_examine`) and 1015 (`_revalidate`) keep calling `project_check` unchanged.

Acceptance criteria:
- `project_check` returns `None` for each of `Research`, `Spec`, `Plan` and `Debug`, and `project_mismatch` for `Backlog`, `Ready`, `In progress`, `In review`, `Done`, `None` and an unknown name such as `Triage`.
- `tests/issue_watch/test_predicates.py` has one case per status above, and the old `Backlog`-passes case is replaced, not left alongside.
- `tests/issue_watch/test_cycle.py` and `tests/issue_watch/conftest.py` fixtures that used `Backlog` as the passing status now use an allowed status, and `uv run pytest tests/issue_watch -q` passes.
- `src/superclaude/cli/issue_pipeline/reads.py` (a dependent of `issue_watch/github.py`) still imports and passes its tests: `uv run pytest tests/issue_pipeline -q`.

## Task 2: Update the design and runbook text for the Status rule

Edit `docs/designs/issue-watcher.md` (the lines naming Backlog: 21, 692 and 884) and `docs/designs/issue-watcher-setup.md` (lines 189 and 366) so they state the allow-list of Task 1: Research, Spec, Plan and Debug act; Backlog, Ready, In progress, In review and Done never do; a new status is blocked until added. Add one sentence to `docs/designs/issue-watcher.md` that this reverses the original issue 331 rule ("Issues must be in Backlog status"), by owner decision of 2026-11-18.

Depends on: Task 1

Acceptance criteria:
- `grep -n "Backlog" docs/designs/issue-watcher.md docs/designs/issue-watcher-setup.md` shows no line that says Backlog is the status that allows action.
- Both files list the four allowed statuses by name.
- `uv run pytest tests/docs -q` passes.

## Task 3: Read the Project Pipeline field with the Status

In `src/superclaude/cli/issue_watch/github.py`, extend `PROJECT_ITEMS_QUERY` (lines 88 to 103) with a second single-select read of the Project field named `Pipeline` (a GraphQL alias next to the existing `fieldValueByName(name: "Status")`), extend `_project_item` (lines 764 to 775) to parse it, and add `pipeline_name: str | None` to the `ProjectItem` dataclass in `src/superclaude/cli/issue_watch/predicates.py` (around lines 113 to 118). The Pipeline values on the board are `None`, `Worktree`, `Full` and `Full Submit`; an absent value is `None` (Python) and is treated as the `None` pipeline by later tasks. The query stays read-only.

Acceptance criteria:
- `tests/issue_watch/test_github.py` parses a fixture with a Pipeline value, a fixture with a null Pipeline and a malformed one (malformed gives the existing `non_json` or `unreadable` outcome, not an exception). The shape fixture `tests/issue_watch/fixtures/_assumed_shape/graphql_project_items.json` is updated.
- `tests/issue_watch/test_security_invariants.py` still passes: the query contains no `mutation`.
- Every other constructor call of `ProjectItem` in `tests/issue_watch/` is updated, and `uv run pytest tests/issue_watch -q` passes.

## Phase 2: Per-status commands

## Task 4: Write the design note for per-status commands

Create `docs/designs/issue-watcher-status-pipelines.md`. It records the owner's mapping of 2026-11-18 (requirement R23) and decides every interface the next tasks implement: Research runs `/sc:research`, Spec runs `/sc:design` when the issue is well defined and `/sc:brainstorm` when it is not, with a handoff to `/sc:design` for high complexity or scope, Plan runs `/sc:workflow`, Debug runs `/sc:troubleshoot --fix`, and Ready and every other status trigger nothing. The Pipeline field (None, Worktree, Full, Full Submit) is the launch level of `/sc:issue --claim --pipeline`, and an empty Pipeline means None (claim only). The note must decide: the exact launch prompt text the watcher sends for each Status and Pipeline pair and the pattern that pins it (today `PROMPT_PATTERN` in `src/superclaude/cli/issue_watch/launch.py` line 33); how the Status reaches the coordinator (which file or store field carries it, since a `--pipeline none` claim creates no worktree record); who judges "well defined" for Spec and where the reason is recorded (the claim's `issue-summary.md`); how the approval record of requirement R19 is created automatically from the approval label (which fields of `dispatch.json` it reads, and whether the watcher or the coordinator writes it); and, for each of the five commands, whether it can run as the coordinator's worker, checked against `src/superclaude/core/WORKER-CONTRACT.md` line 23 (the never-as-worker list) and each command file under `src/superclaude/commands/`.

Acceptance criteria:
- The file exists and has a table with one row per Status (Research, Spec, Plan, Debug, Ready) giving the command, the prompt text, and whether it can run as a worker with the file and line that shows it.
- Every open point listed above has a stated decision; a command that cannot run as a worker has a stated alternative, not a blank.
- The note says which files change in Tasks 5 and 6 by path.

## Task 5: Build the per-status prompt in the watcher

Implement the prompt rules of Task 4 in `src/superclaude/cli/issue_watch/launch.py` (`build_claim_prompt` at line 84, `PROMPT_PATTERN` at line 33, `launch_argv` at line 95, `retry_argv` at line 119) and in `src/superclaude/cli/issue_watch/cycle.py` (`_examine` at line 915 and `_launch` at line 1026), which must carry the examined issue's Status and Pipeline from the `ProjectItem` of Task 3 into the prompt. A Status that triggers nothing is already stopped by Task 1. Keep `ValueError` for any input that does not match, so no other text reaches `--prompt`.

Depends on: Task 1, Task 3, Task 4

Acceptance criteria:
- `tests/issue_watch/test_launch.py` covers the prompt for each allowed Status crossed with each Pipeline value and an empty Pipeline, and rejects an invalid number, an unknown Status and an unknown Pipeline.
- `tests/issue_watch/test_security_invariants.py` and `tests/issue_watch/test_no_shell.py` pass (no new text path, no shell).
- `tests/issue_watch/test_cycle.py` shows the prompt sent for an issue in each allowed Status.
- The `once` dry-run output (`would_launch`) is unchanged in shape.

## Task 6: Update the claim command, the coordinator duties and the guard for the new prompts

Apply the rest of Task 4's decisions: `src/superclaude/commands/issue.md` and `src/superclaude/skills/sc-issue-protocol/SKILL.md` and `refs/claim.md` accept the new prompt forms; `src/superclaude/core/WORKER-CONTRACT.md` section "Issue pipeline duties" (line 291 onward) tells the coordinator how to read the Status and Pipeline and which command the worker brief carries, and creates the approval record automatically from the stored approval fields (requirement R19); the worker brief template `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` carries the chosen command. Any hook or test that pins the old fixed prompt `/sc:issue --claim <N> --pipeline none` is updated, among them `tests/hooks/test_launch_level_guard.py`, `tests/skills/test_worker_contract.py` and `tests/issue_watch/test_security_invariants.py` (search for the literal with Grep first and list every hit in the commit). Run `make sync-dev` and `make verify-sync`.

Depends on: Task 4, Task 5

Acceptance criteria:
- `grep -rn -- "--pipeline none" src tests docs` has no hit that still presents it as the only watcher prompt.
- The duties section names the Status-to-command table and the automatic approval record, and `uv run pytest tests/skills/test_worker_contract.py tests/skills tests/hooks -k "launch_level or worker_contract or issue" -q` passes.
- A test creates the approval record from a stored approval (approver id and event id) and shows the row exists once, and a second call does not create a second row.
- `make verify-sync` is clean and no `.claude/` path is staged.

## Phase 3: Thread the repo through the watcher

## Task 7: Pass the repo into the GitHub reads

In `src/superclaude/cli/issue_watch/github.py`, replace the module constant use of `REPO` (line 37; used at lines 187, 208 and 259) and the hard-coded owner and name inside `EDITS_QUERY` (line 74) and `PROJECT_ITEMS_QUERY` (line 88) with a `repo` parameter (`owner/name`) on `argv_discover`, `_argv_rest_page`, `_argv_graphql`, `argv_edits`, `argv_project_items`, `argv_reread` and on the public reads `discover`, `events`, `marker_comments`, `edits`, `project_items` and `reread`. GraphQL queries take `$owner` and `$name` as variables. Keep `REPO` as the default value so `src/superclaude/cli/issue_pipeline/reads.py` and its tests keep working unchanged. Validate the value with a strict `owner/name` pattern and raise `ValueError` before any call for anything else.

Depends on: Task 3

Acceptance criteria:
- `tests/issue_watch/test_github.py` shows each argv carries the passed repo, and rejects `a/b/c`, an empty string, a value with a space or a leading dash.
- `tests/issue_watch/test_security_invariants.py` still passes, including the no-mutation checks on the query constants.
- `uv run pytest tests/issue_pipeline tests/issue_watch -q` passes.

## Task 8: Add the repo to the config and use it for the origin check

In `src/superclaude/cli/issue_watch/cycle.py` add an optional `repo` key to `_TOP_KEYS` (line 58), to `Config` (line 97) and to `load_config` (line 195); when absent it defaults to `IronbellyOrg/IronClaude` so a hand-written config such as `/home/coder/.config/superclaude/issue-watch.json` stays valid. Pass `cfg.repo` from `_Cycle` to every `github.*` call of Task 7. In `src/superclaude/cli/issue_watch/launch.py` change `check_origin` (line 233) and its use (`ORIGIN_REPO` line 50, compared at line 249; called from `cycle.py` `_origin_ok` line 670 and the launch step) to compare against the configured repo, case-insensitively as today.

Depends on: Task 7

Acceptance criteria:
- `tests/issue_watch/test_cycle.py` runs a cycle for a config with `repo` set to another name and shows every `gh` call carries it and the origin check uses it; a worktree whose origin names a different repo ends with `origin_mismatch`.
- `tests/issue_watch/test_origin_parity.py` and `tests/issue_watch/test_launch.py` are updated and pass.
- A config without `repo` behaves as before (existing tests pass unchanged).
- `uv run pytest tests/issue_watch -q` passes.

## Phase 4: Generate each repo's configuration

## Task 9: Read the central defaults file

Create `src/superclaude/cli/issue_watch/defaults.py`. It reads `~/.config/superclaude/issue-watch-defaults.json` (the file the Coder template saves, requirement R1) and returns the fixed approver logins, the two label names, and an optional map from `owner/name` to a Project node id. When the file is absent it returns built-in values: approver logins `ironbelly` and `clayphi`, labels `issue-watch:trigger` and `issue-watch:approved`, an empty map. Unknown keys, a wrong type or a bad login are rejected with the existing `ConfigError` style (`cycle.py` line 81). The module is pure: it reads one file and runs no command.

Acceptance criteria:
- New `tests/issue_watch/test_defaults.py` covers: file absent, a valid file, an unknown key, a bad login such as `-x`, and a map entry whose id does not match `PVT_`.
- `tests/issue_watch/test_module_boundaries.py` passes with the new module.

## Task 10: List and filter the Orca repos

Create `src/superclaude/cli/issue_watch/repos.py` with a function that runs `orca repo list` through the `Runner` of `src/superclaude/cli/issue_watch/runner.py` and returns one record per usable repo: Orca id, name, local path, and `owner/name` read from the path's git `origin`. A failed or timed-out `orca repo list`, or output that cannot be read, raises an error (requirement R15), never an empty list. Skip, and report with a reason, a repo whose path is under `/tmp`, whose origin is not on github.com, or whose origin owner is not in the allowed owners (default `IronbellyOrg`, taken from the defaults of Task 9). Parse the real format: one line per repo, `<id>  <name>  <path>` (checked on 2026-11-18).

Depends on: Task 9

Acceptance criteria:
- New `tests/issue_watch/test_repos.py` uses the fake runner and covers: six repos with one in `/tmp` skipped, a non-GitHub origin skipped, a foreign owner skipped, a failed list raising, a timed-out list raising, an empty but successful list returning no repos.
- The module uses no shell and passes `tests/issue_watch/test_no_shell.py` and `test_module_boundaries.py`.

## Task 11: Generate one repo's configuration, approvers file and state directory

Create `src/superclaude/cli/issue_watch/generate.py` with `ensure_config(repo_record, defaults, runner)`. For a repo that has no file at `~/.config/superclaude/issue-watch.d/<name>.json` it: reads the account id with `gh api user` (requirement R2); finds the Project with the GraphQL query `repository(owner, name){ projectsV2(first:10){ nodes{ id number title } } }` (R3): zero Projects gives a skip with reason `no_project`, several use the id from the defaults map or give the skip reason `project_ambiguous`; reads maintainers with `gh api "repos/<owner>/<name>/collaborators?permission=maintain"` and adds them to the fixed approvers' account ids (R4; fixed logins are turned into ids with `gh api users/<login>`); writes `~/.config/superclaude/issue-watch.d/<name>-approvers.txt` (mode 600, one id per line) and the config JSON (mode 600) with absolute `worktree` (`/home/coder/workspaces/worktrees/<name>/Coordinator`), `approvers_file`, an explicit absolute `state_dir` of `~/.local/state/superclaude/issue-watch/<name>` (R12), the `repo`, the Project id, the account id and `enabled: false`. The result is validated with `cycle.load_config` and `cycle.validate_approvers` before it is kept; a file that exists is never overwritten.

Depends on: Task 8, Task 9, Task 10

Acceptance criteria:
- New `tests/issue_watch/test_generate.py` covers: a repo with one Project, none, several with and without a defaults entry, a failed account read, maintainers added, an existing config left untouched, file modes 600, and two repos getting two different `state_dir` values.
- A generated config passes `cycle.load_config` in the test, and `uv run pytest tests/issue_watch -q` passes.
- The module issues only read calls to GitHub (`gh api user`, `gh api users/<login>`, the Project query, the collaborators call).

## Task 12: Create the two labels on a repo when missing

Create `src/superclaude/cli/issue_watch/repo_init.py` with a function that lists the repo's labels (`gh label list --repo <owner/name>`) and creates `issue-watch:trigger` and `issue-watch:approved` with `gh label create --repo <owner/name>` when absent (requirement R11). This is the only place in the watcher package that writes to GitHub, so it is a separate module and `github.py` stays read-only. It is idempotent and reports `created`, `present` or `failed` per label.

Depends on: Task 9

Acceptance criteria:
- New `tests/issue_watch/test_repo_init.py` covers: both labels missing, one present, both present (no create call), a failed create.
- `tests/issue_watch/test_security_invariants.py` still passes, and its NG-2 scope is documented as `github.py` and the cycle, with this module named as the one allowed writer.
- The label names come from the defaults of Task 9, not from literals in the module.

## Task 13: Run the first-run check and enable a repo

Create `src/superclaude/cli/issue_watch/first_run.py` (requirements R7 and R18). For a freshly generated config it runs, in order: config validation (`check-config` logic), `init-state`, and one dry-run cycle (`once --dry-run` logic). All pass: it rewrites the config with `enabled: true`. Any fails: the config stays `enabled: false` and a one-line reason is written to `~/.local/state/superclaude/issue-watch/<name>/first-run.txt`. It is idempotent: a repo whose state already exists is not re-initialised and a repo already enabled is left alone.

Depends on: Task 11, Task 12

Acceptance criteria:
- New `tests/issue_watch/test_first_run.py` covers: all pass gives `enabled: true`; a worktree that does not exist gives `enabled: false` with `worktree_invalid` in the report; a dry-run failure keeps it false; a second run changes nothing.
- No real `gh`, Orca or network call is made in the tests.

## Phase 5: The dispatcher loop

## Task 14: Print the launched issue from `once`

In `src/superclaude/cli/issue_watch/cli.py` `once_command` (line 118) currently prints `cycle: <reason>` and `exit: <code>`, and prints `would_launch` only in a dry run. Also print `launched: <issue number>` when the cycle launched an issue (`CycleResult.launched_issue`, `cycle.py` line 455), so the dispatcher can read it from a child's output.

Acceptance criteria:
- `tests/issue_watch/test_cli.py` shows `launched: 12` appears after a launch and is absent otherwise, and the existing outputs are unchanged.
- `tests/issue_watch/test_no_text.py` still passes (the line contains a number only).

## Task 15: Write the dispatcher core

Create `src/superclaude/cli/issue_watch/dispatch.py` with the loop of requirements R5, R15 and R16. It lists repos (Task 10), calls `ensure_config` and `first_run` (Tasks 11 and 13) for any repo without a config, then starts `superclaude issue-watch once --config <file>` as a child process per repo, one after another. Rules: total loop cap 270 seconds; each child is killed after 255 seconds, longer than the cycle's own 240 second deadline (`DEADLINE_TOTAL_S`, `cycle.py` line 41); repos not reached are skipped and reported; the repo order rotates each sweep (the next start index is kept in a small file under `~/.local/state/superclaude/issue-watch/`); the loop stops starting children after the first child whose output has a `launched:` line; `DAY_CAP` stays per repo. Use the `Runner` interface so tests use fakes, and pass absolute paths because cron has no PATH.

Depends on: Task 10, Task 11, Task 13, Task 14

Acceptance criteria:
- New `tests/issue_watch/test_dispatch.py` covers: rotation across three sweeps, a stop after the first launch, the 270 second cap with unreached repos reported, a child killed after 255 seconds and recorded as failed while later repos still run, a repo with no config being generated first, and a failed `orca repo list` giving an error result rather than a clean one.
- A child timeout never kills the loop, and each child's exit code and reason are kept for Task 17.

## Task 16: Add the loop-level account rate wait and the pre-child checks

Extend `src/superclaude/cli/issue_watch/dispatch.py`. Rate wait (requirement R5): when a child's cycle reason is plain `rate_limited` (not the 3600 second clamp reason, `github.py` `rate_limit_wait` line 418), the loop writes one file `~/.local/state/superclaude/issue-watch/account-rate-wait.json` holding the child's `next_permitted_at` and starts no further child until that time; children never write each other's stores. Pre-child checks (R14), each reported rather than silent: the repo's `Coordinator` worktree exists, is a git checkout and its `origin` names the repo; both labels exist (read-only `gh label list`, creating them through `repo_init.py` when missing); the Project count is exactly one (Task 11 rule). A failing check skips that repo and records the reason.

Depends on: Task 12, Task 15

Acceptance criteria:
- `tests/issue_watch/test_dispatch.py` adds cases: a `rate_limited` child stops later children until the stored time and a restart of the loop honours the file; a `rate_limit_clamped` child does not write it; a missing `Coordinator` worktree, a wrong origin and missing labels each give a distinct skip reason; an expired wait file is ignored.
- All reasons used are written in the audit reason vocabulary (`src/superclaude/cli/issue_watch/audit.py` `REASON_TABLE`, line 26) or a new documented table in `dispatch.py`.

## Task 17: Add the `run-all` command

In `src/superclaude/cli/issue_watch/cli.py` add a `run-all` command to `issue_watch_group` (line 94) that runs the dispatcher of Tasks 15 and 16 and prints one line per repo (repo, result, reason) and an overall line. Exit codes follow the existing set (`_EXIT_*`, lines 34 to 38): 0 for a clean sweep, 2 for a configuration problem in the loop itself, 75 when another sweep holds the loop lock. It takes a `--dry-run` flag that lists repos and decisions but writes no config, creates no label and starts no child. A second sweep started while one runs exits 75 through a lock file in the state directory (`flock`-style, like `record.py` line 381).

Depends on: Task 16

Acceptance criteria:
- `tests/issue_watch/test_cli.py` covers `run-all` output for a clean sweep, a skipped repo, a held lock (exit 75) and `--dry-run` (nothing written; assert the temp directory is unchanged).
- `uv run superclaude issue-watch run-all --help` exits 0 and `uv run superclaude issue-watch --help` lists `run-all`.
- `uv run pytest tests/issue_watch -q` passes.

## Phase 6: Documentation, the Coder handoff and the requirements record

## Task 18: Document the dispatcher in the watcher design and runbook

Update `docs/designs/issue-watcher.md` and `docs/designs/issue-watcher-setup.md` for: the `run-all` loop and its caps, the config folder `~/.config/superclaude/issue-watch.d/`, the defaults file, the generator and first-run check, the label creation module as the single writer, the `repo` config key, the per-status commands and the Pipeline field (pointing to `docs/designs/issue-watcher-status-pipelines.md`), the `Coordinator` worktree path, and a new section replacing the hand setup steps of the runbook (sections 2 to 5) with the automatic path while keeping the manual commands as a fallback.

Depends on: Task 17

Acceptance criteria:
- Both files mention `run-all`, `issue-watch.d`, `Coordinator`, `Pipeline` and the allowed statuses, checked with `grep -c`.
- `uv run pytest tests/docs -q` passes.

## Task 19: Write the Coder handoff document

Create `docs/designs/issue-watcher-zero-setup-coder-handoff.md` for the Coder template maintainers (requirements R1, R6, R9, R10, R17, R20, R21; Coder issues 515 and 516). It contains: the exact crontab line to install, built from verified values (`*/5 * * * *`, an explicit `PATH`, `flock -n` on a lock under `~/.aidev/`, full path `/usr/local/bin/superclaude issue-watch run-all`, output appended to `~/.aidev/logs/issue-watch.log`), with the tool locations checked on 2026-11-18 (`/home/coder/.config/orca/linux-orca-cli-shim/orca`, `/home/coder/.local/bin/gh`, `/usr/local/bin/superclaude`, `/usr/local/bin/uv`); the content of the central defaults file of Task 9 for the template to save; the `Coordinator` branch and worktree rules (switch to the remote branch when it exists, create it otherwise, path `/home/coder/workspaces/worktrees/<repo>/Coordinator`, origin equal to the repo); the session name `COORD-<RepoName>` and the standing launch-prompt text that gives the coordinator the issue-pipeline duties; and the open Orca question that `orca worktree create --branch` suffixes a taken name. Before writing the cron line, run `env -i HOME=$HOME PATH=/usr/bin:/bin /home/coder/.local/bin/gh auth status` and record whether `gh` stays logged in under cron's environment, and record the result in the file.

Depends on: Task 17

Acceptance criteria:
- The file lists each of R1, R6, R9, R10, R17, R20 and R21 with the Coder issue number where one exists and the exact value or text the template must use.
- It records the result of the `gh auth status` check under a cron-like environment, whichever way it came out.
- The cron line in the file contains an absolute `PATH`, `flock -n`, the log path and `run-all`.

## Task 20: Record the built and tested results in the requirements file

Update `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`: set each row that Tasks 1 to 19 implemented to `built` with the date and the test evidence (the test files and the passing count from the last full run of `uv run pytest tests/issue_watch tests/issue_pipeline tests/hooks tests/skills -q`), add a row to "Built and tested" for each task, move any decision still open (R20, R21 and the four confirmations of R23) under "Open decisions", and state which rows stay with the Coder repository.

Depends on: Task 19

Acceptance criteria:
- Every row R1 to R23 has a status of `built`, `decided (Coder repo)` or `open`, and none is left as the earlier `decided (not built)` when its task is done.
- The "Built and tested" table has an entry per task with a test file name and a count.
- `make verify-sync` is clean.
