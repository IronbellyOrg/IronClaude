---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-requirements-20261119-012839
version: "1"
priority: Medium
created_date: "2026-11-19"
---

# Zero-setup issue watcher v3: status gate, approval provenance, per-status commands and launch levels, coordinator-only completion update, repo threading, config generator and dispatcher loop

Source: ./source.md
Goal: The issue watcher can be switched on in any workspace with no per-user setup. It acts only on the allowed Project statuses and only on an approval given after the issue's last Project change, picks its command from the issue's Status and its launch level from the Project's Pipeline field (None, Worktree, Full, Full Submit), serves every Orca repo through one dispatcher that cron can run, writes each repo's configuration, approvers and labels itself, and, when the work is finished, has the coordinator comment on the issue and move its Status to In review.

## Constraints

- Scope is the IronClaude repository only. The Coder template work (requirements R1, R6, R9, R10, R17, R20, R21; Coder issues 515 and 516) is not implemented here; Task 23 hands it over with exact values.
- Edit `src/superclaude/`, then run `make sync-dev` and `make verify-sync`. Never edit or stage anything under `.claude/` (only `.claude/settings.json` is tracked). The tracked plugin mirror `plugins/superclaude/hooks/scripts/launch-level-guard.sh` is changed together with its source.
- Python only through UV (`uv run pytest`, `uv run ruff`). Tests use the faked `gh` and Orca runners already in `tests/issue_watch/conftest.py`; no task runs the watcher against the real GitHub or Orca, except the read-only schema check Task 3 names.
- `src/superclaude/cli/issue_watch/github.py` stays read-only: no mutation, no POST to a REST path (security invariant NG-2, `tests/issue_watch/test_security_invariants.py`). The only modules that write to GitHub are two new ones outside `github.py`: `src/superclaude/cli/issue_pipeline/complete.py` (Task 9: result comment and Status move, run only by the coordinator) and `src/superclaude/cli/issue_watch/repo_init.py` (Task 16: labels).
- Only the coordinator writes to an issue or its Project item (owner decision of 2026-11-19; `src/superclaude/core/WORKER-CONTRACT.md` lines 241 to 243 and 300), and only under that issue's grant row. An agent launched at Worktree, Full or Full Submit, and every worker, never runs `issue-pipeline complete`, never posts an issue comment and never changes a Project field; it reports through its result file `.dev/issues/<N>/result.md`. The launch-level guard keeps refusing issue comments and `gh api` writes at those levels.
- The approval label, the allowed Project Status, the approval-void rule of Task 4 and the "edited after approval" refusal (`predicates.py`) stay the gate. Nothing in this plan removes or auto-satisfies them. The plan-hash approval row (`src/superclaude/cli/issue_pipeline/approval_record.py`) is created only from a worker's `ask` that carries the plan hash (`WORKER-CONTRACT.md`, WC-17), never from claim-time fields.
- The cron watcher may launch every Pipeline level: None, Worktree, Full and Full Submit (owner, 2026-11-19). Full Submit commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`; it never merges. For an issue the owner has put at Full Submit and approved with the approval label after the last Project change, that setting is the person's go for that issue's push and pull request, and nothing else is pushed.
- The term is "coordinator", never "orchestrator". The coordinator branch and worktree are both named `Coordinator`; the session is named `COORD-<RepoName>`.
- Every new module that writes under the user's home takes an injectable base directory, and its tests run with every path inside `tmp_path` and assert nothing was written under the real home.
- Do not switch any real watcher on, claim a real issue, install a real cron entry, move a real issue's Status or start a worker for a real issue. Each generated config starts with `enabled: false` and only the automatic first-run check of Task 17 may turn it on.

## Phase 1: Status gate, field reads and approval provenance

## Task 1: Replace the Backlog check with a Status allow-list

In `src/superclaude/cli/issue_watch/predicates.py`, change `project_check` (lines 262 to 271) so an issue passes only when it is the one live item of the configured Project and its Status name is one of `Research`, `Spec`, `Plan` or `Debug` (requirement R22). Every other value, including `Backlog`, `Ready`, `In progress`, `In review`, `Done`, an empty Status and any status added to the board later, returns `project_mismatch`. Keep the reason code `project_mismatch` (it is in `audit.REASON_TABLE`, `audit.py` line 72) so no reason table changes. Name the allowed set as one module constant. The callers `cycle.py` lines 958 (`_examine`) and 1015 (`_revalidate`) keep calling `project_check` unchanged.

Acceptance criteria:
- `project_check` returns `None` for each of `Research`, `Spec`, `Plan` and `Debug`, and `project_mismatch` for `Backlog`, `Ready`, `In progress`, `In review`, `Done`, `None` and an unknown name such as `Triage`.
- `tests/issue_watch/test_predicates.py` has one case per status above, and the old `Backlog`-passes case is replaced, not left alongside.
- `tests/issue_watch/test_cycle.py` and `tests/issue_watch/conftest.py` fixtures that used `Backlog` as the passing status now use an allowed status, and `uv run pytest tests/issue_watch -q` passes.
- `src/superclaude/cli/issue_pipeline/reads.py` (a dependent of `issue_watch/github.py`) still imports and passes its tests: `uv run pytest tests/issue_pipeline -q`.

## Task 2: Update the design and runbook text for the Status rule

Edit `docs/designs/issue-watcher.md` (the lines naming Backlog: 15, 21, 692 and 884) and `docs/designs/issue-watcher-setup.md` (lines 189 and 366) so they state the allow-list of Task 1: Research, Spec, Plan and Debug act; Backlog, Ready, In progress, In review and Done never do; a new status is blocked until added. Line 15 of `issue-watcher.md` says the cycle finds issues "in the Project's Backlog column"; it is rewritten with the others. Add one sentence to `docs/designs/issue-watcher.md` that this reverses the original issue 331 rule ("Issues must be in Backlog status"), by owner decision of 2026-11-18.

Depends on: Task 1

Acceptance criteria:
- `grep -n "Backlog" docs/designs/issue-watcher.md docs/designs/issue-watcher-setup.md` shows no line that says Backlog is the status that allows action, line 15 included.
- Both files list the four allowed statuses by name.
- `uv run pytest tests/docs -q` passes.

## Task 3: Read the Pipeline field and the Project item's update time

In `src/superclaude/cli/issue_watch/github.py`, extend `PROJECT_ITEMS_QUERY` (lines 88 to 103) with a second single-select read of the Project field named `Pipeline` (a GraphQL alias next to the existing `fieldValueByName(name: "Status")`) and with the Project item's `updatedAt`. Extend `_project_item` (lines 764 to 775) to parse both, and add `pipeline_name: str | None` and `updated_at: datetime | None` to the `ProjectItem` dataclass in `src/superclaude/cli/issue_watch/predicates.py` (around lines 113 to 118). The Pipeline values on the board are `None`, `Worktree`, `Full` and `Full Submit`; an absent value is Python `None` and later tasks treat it as the `None` pipeline. The query stays read-only. Requirement R31 relies on `updatedAt`: before relying on it, run one read-only GraphQL schema query for the type `ProjectV2Item` (`gh api graphql -f query='query { __type(name: "ProjectV2Item") { fields { name } } }'`) and save its output to `./artifacts/t3-projectv2item-fields.txt`; if `updatedAt` is not listed, stop and return the fallback of R31 (a level-specific approval label) to the owner.

Acceptance criteria:
- `./artifacts/t3-projectv2item-fields.txt` exists and lists `updatedAt` (or the task stops with the R31 fallback reported).
- `tests/issue_watch/test_github.py` parses a fixture with a Pipeline value and an update time, a fixture with a null Pipeline and a malformed one (malformed gives the existing `non_json` or `unreadable` outcome, not an exception). The shape fixture `tests/issue_watch/fixtures/_assumed_shape/graphql_project_items.json` is updated.
- `tests/issue_watch/test_security_invariants.py` still passes: the query contains no `mutation`.
- Every other constructor call of `ProjectItem` in `tests/issue_watch/` is updated, and `uv run pytest tests/issue_watch -q` passes.

## Task 4: Void an approval when the Project item changed after it

Implement requirement R31 in `src/superclaude/cli/issue_watch/predicates.py` and `src/superclaude/cli/issue_watch/cycle.py`. Add a predicate next to `edited_after_approval` (line 258) that returns the existing reason `edited_after_approval` when the live Project item's `updated_at` is at or after the approval's time (an equal time counts as changed, as in `unchanged_since`; an unreadable `updated_at` also refuses). Call it in `_examine` (line 915) and again in `_revalidate` (line 979) with the reread item, so a Pipeline or Status changed after the approval label cannot launch. Reuse the reason code so no reason table changes.

Depends on: Task 3

Acceptance criteria:
- `tests/issue_watch/test_predicates.py` covers: item updated before approval passes, at the same instant refuses, after approval refuses, a missing `updated_at` refuses.
- `tests/issue_watch/test_cycle.py` shows a Pipeline raised from None to Full Submit after approval ends with `edited_after_approval` and no launch, both at examine time and between examine and launch.
- `tests/issue_watch/test_security_invariants.py` passes and `uv run pytest tests/issue_watch -q` passes.

## Phase 2: Design decisions for per-status commands, launch levels and completion

## Task 5: Write the design note for per-status commands, launch levels and completion

Create `docs/designs/issue-watcher-status-pipelines.md`. It records the owner's decisions of 2026-11-18 and 2026-11-19 (requirements R23, R24, R25, R29, R31, R32) and decides every interface the later tasks implement. Research runs `/sc:research`; Spec runs `/sc:design` when the issue is well defined and `/sc:brainstorm` when it is not, with a handoff to `/sc:design` for high complexity or scope; Plan runs `/sc:workflow`; Debug runs `/sc:troubleshoot --fix`; Ready and every other status trigger nothing. The Pipeline field maps to the claim command as None or empty = `--pipeline none`, Worktree = `--pipeline worktree`, Full = `--pipeline full`, Full Submit = `--pipeline full --submit` (`src/superclaude/commands/issue.md` lines 43, 44 and 56 accept only worktree, full and none plus the `--submit` flag).

The note must decide, each with a stated reason:
- The exact launch prompt text the watcher sends for each Status and Pipeline pair, and the pattern that pins it (today `PROMPT_PATTERN`, `src/superclaude/cli/issue_watch/launch.py` line 33, with the prompt built at line 92). The launch-level guard has no prompt allow-list, so the pattern in `launch.py` is the only pin.
- A table of Status by launch level: whether the command runs, runs in a limited form or is refused, and the end Status of each pair. Default to decide against: `/sc:troubleshoot --fix` edits code, so at Worktree ("propose next steps, halt") it runs without `--fix` and at Full and Full Submit with `--fix`.
- Which session runs the Status command at each level: at `none` the coordinator starts a worker from the brief template; at `worktree`, `full` and `full submit` the agent that `/sc:issue --claim` launches runs it from its launch prompt. State how the Status command enters `launch-prompt.md` and the worker brief.
- How the Status and Pipeline reach the coordinator (which stored field or file), since a `--pipeline none` claim creates no worktree record.
- Who judges "well defined" for Spec and where the reason is recorded (the claim's `issue-summary.md`).
- Which record the "automatic approval record" of R19 means: the claim-time approval already kept in `dispatch.json` plus the adoption row, versus the plan-hash approval row, which only a worker's `ask` carrying the plan hash may create (R29).
- The completion update (R24), coordinator only: how the coordinator learns a launched agent has finished (the result file `.dev/issues/<N>/result.md` in the issue's worktree and the `/sc:sweep` report), the closed format of that result file (outcome word, artifact paths, pull request number), what the result comment holds, that only a succeeded outcome moves the Status, that the end Status is held in one named table (all four Status pipelines end at `In review`; the owner has not yet named exceptions), idempotency, and what a failed, blocked or partial outcome does (comment only).
- The Full Submit push rule: the wording that replaces the push sentence in `src/superclaude/core/WORKER-CONTRACT.md` (line 245) so the owner's Pipeline setting plus an approval given after the last Project change (Task 4) is the person's go for that issue only.
- For each of the five commands, whether it can run as the coordinator's worker, checked against `src/superclaude/core/WORKER-CONTRACT.md` line 23 (the never-as-worker list) and each command file under `src/superclaude/commands/`, with an alternative where it cannot.

Acceptance criteria:
- The file exists and has a table with one row per Status (Research, Spec, Plan, Debug, Ready) giving the command, the prompt text for each of the four Pipeline values, the end Status per level, and whether it can run as a worker with the file and line that shows it.
- Every decision listed above has a stated decision; a command that cannot run as a worker has a stated alternative, not a blank.
- The note says which files change in Tasks 6 to 10 by path.

Depends on: Task 1, Task 3, Task 4

## Phase 3: Per-status prompts and launch levels

## Task 6: Build the per-status prompt from the revalidated item

Implement the prompt rules of Task 5 in `src/superclaude/cli/issue_watch/launch.py` (`build_claim_prompt` at line 84, `PROMPT_PATTERN` at line 33, `launch_argv` at line 95, `retry_argv` at line 119) and in `src/superclaude/cli/issue_watch/cycle.py` (`_examine` at line 915, `_revalidate` at line 979 and `_launch` at line 1026). Today `_launch` builds the prompt at line 1054 and only then calls `_revalidate` (line 1058), which rereads the project items (lines 1012 to 1016) but checks only `project_check` (requirement R27). Change the order so the prompt is built from the item that `_revalidate` rereads, and refuse the launch with the existing `revalidation_failed` reason when the reread Status or Pipeline differs from the one examined. Add a small helper next to `project_check` in `predicates.py` that returns the one live item. `status_report` (`cycle.py` line 1270) builds a retry command with `build_claim_prompt`; it must keep printing a valid command for every allowed Status and Pipeline. Keep `ValueError` for any input that does not match, so no other text reaches `--prompt`.

Depends on: Task 1, Task 3, Task 4, Task 5

Acceptance criteria:
- `tests/issue_watch/test_launch.py` covers the prompt for each allowed Status crossed with each Pipeline value and an empty Pipeline, and rejects an invalid number, an unknown Status and an unknown Pipeline.
- `tests/issue_watch/test_cycle.py` shows the prompt sent for an issue in each allowed Status, and shows two refusals: Status changed from Research to Debug between examine and launch, and Pipeline lowered from Full Submit to None between examine and launch. Both end with `revalidation_failed` and no launch call.
- `tests/issue_watch/test_security_invariants.py` and `tests/issue_watch/test_no_shell.py` pass (no new text path, no shell).
- The `once` dry-run output (`would_launch`) keeps its shape, and the `status_report` retry command is valid in a test for each Status.

## Task 7: Update the claim command, the skill, the result file and the tests for the new prompts

Apply the prompt decisions of Task 5 to the claim surface: `src/superclaude/commands/issue.md`, `src/superclaude/skills/sc-issue-protocol/SKILL.md`, `src/superclaude/skills/sc-issue-protocol/refs/claim.md` and `src/superclaude/skills/sc-issue-protocol/templates/next-steps.md` accept the new prompt forms, carry the Status command into the launch prompt, and make the last step of a launched agent's prompt the writing of its result file `.dev/issues/<N>/result.md` in the closed format of Task 5 (no GitHub write). The launch-level guard `src/superclaude/hooks/scripts/launch-level-guard.sh` has no prompt allow-list and is not changed here. Update every test and document that pins the old fixed prompt `/sc:issue --claim <N> --pipeline none`. The files that hold the literal today (checked with Grep on 2026-11-19) are `src/superclaude/cli/issue_watch/launch.py`, `src/superclaude/commands/issue.md`, `src/superclaude/core/WORKER-CONTRACT.md`, the three skill files named above, `tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py`, `tests/issue_watch/test_cli.py`, `test_cli_e2e.py`, `test_crash_injection.py`, `test_cycle.py`, `test_launch.py`, `test_no_text.py`, `test_security_invariants.py`, `docs/user-guide/commands.md`, `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` and `docs/designs/` files `issue-pipeline-fu1.md`, `issue-watcher-setup.md`, `issue-watcher.md`, `sc-issue-claim-pipeline-flag.md`, `sc-issue-command.md`, `sc-issue-launch-level-hook.md`. Run the Grep again before editing and list every hit in the commit message. Run `make sync-dev` and `make verify-sync`.

Depends on: Task 5, Task 6

Acceptance criteria:
- `grep -rn -- "--pipeline none" src tests docs plugins` has no hit that still presents it as the only watcher prompt.
- `tests/commands/test_issue_command.py` and `tests/skills/test_issue_protocol.py` show each allowed prompt form is accepted, a prompt with extra text, an unknown level or `--submit` without `--pipeline full` is refused, and the launch prompt ends with the result-file step and contains no `gh` write or `issue-pipeline complete` call.
- `uv run pytest tests/commands tests/skills tests/hooks -q` passes.
- `make verify-sync` is clean and no `.claude/` path is staged.

## Task 8: Update the coordinator duties, the worker brief and the push rule

Apply the remaining decisions of Task 5 to `src/superclaude/core/WORKER-CONTRACT.md` section "Issue pipeline duties" (line 291 onward) and to the rule that a push needs the person's go (line 245). The duties section names the Status-to-command table, says how the coordinator reads the Status and Pipeline, covers claims at every level (today it covers only `--pipeline none`, line 293), and names which stored record is the automatic approval record (R29): the claim-time approval in `dispatch.json` and the adoption row, never the plan-hash row. Update the worker brief template `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` and `src/superclaude/cli/issue_pipeline/brief.py` so the brief carries the Command for the issue's Status, keeping the closed-set checks (no issue text reaches the brief). Update `tests/skills/test_worker_contract.py` and `tests/issue_pipeline/test_brief.py` for the new text and rows. Run `make sync-dev` and `make verify-sync`.

Depends on: Task 5, Task 6

Acceptance criteria:
- A test in `tests/issue_pipeline/test_approval_record.py` shows a plan-hash approval row cannot be created from the claim-time approver id and event id alone: the call is refused without a plan hash, and a claim-time event is refused as plan approval.
- `tests/issue_pipeline/test_brief.py` shows one brief row per allowed Status, the limited form of `/sc:troubleshoot` at Worktree and the `--fix` form at Full and Full Submit (Task 5 table), and that a bad Status, issue number or nonce is refused with a closed reason.
- A test shows the Spec judgment: a well-defined issue yields the `/sc:design` row, an issue that is not yields the `/sc:brainstorm` row with the handoff to `/sc:design` for high complexity, and the reason is recorded in `issue-summary.md`.
- The duties section and the push rule carry the text Task 5 decided; `uv run pytest tests/skills tests/issue_pipeline -q` passes.
- `make verify-sync` is clean and no `.claude/` path is staged.

## Phase 4: Completion update, coordinator only

## Task 9: Write the result comment and move the Status to In review

Create `src/superclaude/cli/issue_pipeline/complete.py` (requirement R24). A function takes the repo, the issue number, an outcome word (`succeeded`, `failed`, `blocked` or `partial`), a pointer to the result summary file and a Runner from `src/superclaude/cli/issue_watch/runner.py`. It posts one result comment through `gh api --method POST repos/<owner>/<name>/issues/<N>/comments` carrying a marker line, and a second call finds only the marker comments written by the watcher's own login and posts no second comment. For `succeeded` only, it reads with its own read-only GraphQL query (variables `$owner`, `$name` and the issue number) the issue's Project item id and the Project's `Status` field id and `In review` option id, then sets the Status with the GraphQL mutation `updateProjectV2ItemFieldValue`; a second call still retries the Status move when the first call's move failed. The end Status comes from one named table keyed by the allowed Status (all four map to `In review`), so an exception is a one-line change. A failed, blocked or partial outcome posts the comment and does not move the Status. Result words are closed and no issue or comment text is echoed. The module lives outside `github.py`, which stays read-only.

Depends on: Task 3, Task 5

Acceptance criteria:
- New `tests/issue_pipeline/test_complete.py` uses the fake runner and covers: succeeded posts one comment and one Status mutation to the `In review` option; failed, blocked and partial post a comment and no mutation; a second call with the watcher's own marker present posts no comment; a marker posted by another login does not suppress the comment; a failed first move is retried on the second call; an unknown outcome word, a bad issue number and a bad repo are refused before any call; a failed mutation reports a closed failure word and leaves the comment in place.
- `tests/issue_watch/test_security_invariants.py` is updated so its NG-2 scope and header (line 10) read `github.py` and the cycle, name `complete.py` and `repo_init.py` as the only allowed writers, and the argv scan (lines 712 to 730) also covers the read calls of the new modules; the test still proves `github.py` has no mutation.
- `tests/issue_watch/test_module_boundaries.py` passes with the new module.

## Task 10: Add the coordinator-only `complete` verb and make the coordinator call it

In `src/superclaude/cli/issue_pipeline/cli.py` add an `issue-pipeline complete` verb (next to `release-worker` at line 200 and `stage-status` at line 335) that calls Task 9 and prints one closed result word. Add the verb to the coordinator-only pattern of the launch-level guard `src/superclaude/hooks/scripts/launch-level-guard.sh` (the TAMPER case at line 444 that already names `adopt-`, `record-` and `release-worker`) and to its plugin mirror, so a bound worker or a launched session that runs it is refused. Update `src/superclaude/core/WORKER-CONTRACT.md` section "Issue pipeline duties" so the coordinator runs the verb under the issue's grant row after it has read a worker's `worker_done` contract (level None) or a launched agent's result file (other levels), per Task 5. Run `make sync-dev` and `make verify-sync`.

Depends on: Task 7, Task 8, Task 9

Acceptance criteria:
- A new `tests/issue_pipeline/test_complete_cli.py` covers the verb: a succeeded call prints the closed success word, a refused call prints a `refused:` word and exits 1, and no verb output holds issue text.
- The guard tests (`tests/hooks/test_launch_level_guard_worker.py` and `tests/hooks/test_launch_level_guard.py`) show a bound worker and a launched session at each level are refused when they run `issue-pipeline complete`, and the existing classes still refuse `gh issue comment` at Worktree and Full and `gh api` writes at every level.
- The duties section names the verb, the grant-row rule and the rule that a failed outcome never moves the Status; `uv run pytest tests/hooks tests/skills tests/issue_pipeline -q` passes.
- `make verify-sync` is clean and no `.claude/` path is staged.

## Phase 5: Thread the repo through the watcher

## Task 11: Pass the repo into the GitHub reads

In `src/superclaude/cli/issue_watch/github.py`, replace the module constant use of `REPO` (line 37; used at lines 187, 208 and 259) and the hard-coded owner and name inside `EDITS_QUERY` (line 74) and `PROJECT_ITEMS_QUERY` (line 88) with a `repo` parameter (`owner/name`) on `argv_discover`, `_argv_rest_page`, `argv_events` (line 218), `argv_comments` (line 223), `_argv_graphql`, `argv_edits`, `argv_project_items`, `argv_reread` and on the public reads `discover`, `events`, `marker_comments`, `edits`, `project_items` and `reread`. GraphQL queries take `$owner` and `$name` as variables. Keep `REPO` as the default value so `src/superclaude/cli/issue_pipeline/reads.py` and its tests keep working unchanged. Validate the value with a strict `owner/name` pattern and raise `ValueError` before any call for anything else. The test `tests/issue_watch/test_security_invariants.py` lines 911 to 919 asserts the old literal `repository(owner: "IronbellyOrg", name: "IronClaude")` and the absence of `$owner` and `$name`; rewrite it to assert the variable form, `$owner` and `$name` present, no `mutation` and no `subscription`.

Depends on: Task 3

Acceptance criteria:
- `tests/issue_watch/test_github.py` shows each argv, `argv_events` and `argv_comments` included, carries the passed repo, and rejects `a/b/c`, an empty string, a value with a space or a leading dash.
- `tests/issue_watch/test_security_invariants.py` lines 911 to 919 are rewritten for the variable form and pass, and the no-mutation checks on the query constants still pass.
- `uv run pytest tests/issue_pipeline tests/issue_watch -q` passes.

## Task 12: Add the repo to the config and use it for the origin check

In `src/superclaude/cli/issue_watch/cycle.py` add an optional `repo` key to `_TOP_KEYS` (line 58), to `Config` (line 97) and to `load_config` (line 195); when absent it defaults to `IronbellyOrg/IronClaude` so a hand-written config such as `/home/coder/.config/superclaude/issue-watch.json` stays valid. Pass `cfg.repo` from the cycle to every `github.*` call of Task 11. In `src/superclaude/cli/issue_watch/launch.py` change `check_origin` (line 233) and its use (`ORIGIN_REPO` line 50, compared at line 249; called from `cycle.py` `_origin_ok` line 670 and the launch step) to compare against the configured repo, case-insensitively as today.

Depends on: Task 6, Task 11

Acceptance criteria:
- `tests/issue_watch/test_cycle.py` runs a cycle for a config with `repo` set to another name and shows every `gh` call carries it and the origin check uses it; a worktree whose origin names a different repo ends with `origin_mismatch`.
- `tests/issue_watch/test_origin_parity.py` and `tests/issue_watch/test_launch.py` are updated and pass.
- A config without `repo` behaves as before (existing tests pass unchanged).
- `uv run pytest tests/issue_watch -q` passes.

## Phase 6: Generate each repo's configuration

## Task 13: Read the central defaults file

Create `src/superclaude/cli/issue_watch/defaults.py`. It reads `issue-watch-defaults.json` from a config directory passed in (default `~/.config/superclaude`; the file the Coder template saves, requirement R1) and returns the fixed approver logins, the two label names, the allowed repo owners and an optional map from `owner/name` to a Project node id. When the file is absent it returns built-in values: approver logins `ironbelly` and `clayphi`, labels `issue-watch:trigger` and `issue-watch:approved`, allowed owner `IronbellyOrg`, an empty map. Unknown keys, a wrong type or a bad login are rejected with the existing `ConfigError` style (`cycle.py` line 81). The module is pure: it reads one file and runs no command.

Acceptance criteria:
- New `tests/issue_watch/test_defaults.py` covers: file absent, a valid file, an unknown key, a bad login such as `-x`, and a map entry whose id does not match `PVT_`; every path is under `tmp_path`.
- `tests/issue_watch/test_module_boundaries.py` passes with the new module.

## Task 14: List and filter the Orca repos

Create `src/superclaude/cli/issue_watch/repos.py` with a function that runs `orca repo list` through the `Runner` of `src/superclaude/cli/issue_watch/runner.py` and returns one record per usable repo: Orca id, name, local path, and `owner/name` read from the path's git `origin`. A failed or timed-out `orca repo list`, or output that cannot be read, raises an error (requirement R15), never an empty list. Skip, and report with a reason, a repo whose path is under `/tmp`, whose origin is not on github.com, or whose origin owner is not in the allowed owners of Task 13. Parse the real format: one line per repo, `<id>  <name>  <path>` (checked on 2026-11-18).

Depends on: Task 13

Acceptance criteria:
- New `tests/issue_watch/test_repos.py` uses the fake runner and covers: six repos with one in `/tmp` skipped, a non-GitHub origin skipped, a foreign owner skipped, a failed list raising, a timed-out list raising, an empty but successful list returning no repos.
- The module uses no shell and passes `tests/issue_watch/test_no_shell.py` and `test_module_boundaries.py`.

## Task 15: Generate one repo's configuration, approvers file and state directory

Create `src/superclaude/cli/issue_watch/generate.py` with `ensure_config(repo_record, defaults, runner, base)` where `base` holds the config directory and the state directory (defaults `~/.config/superclaude` and `~/.local/state/superclaude`). For a repo that has no file at `<config dir>/issue-watch.d/<name>.json` it: reads the account id with `gh api user` (requirement R2); finds the Project with the GraphQL query `repository(owner, name){ projectsV2(first:10){ nodes{ id number title } } }` (R3): zero Projects gives a skip with reason `no_project`, several use the id from the defaults map or give the skip reason `project_ambiguous`; reads maintainers with `gh api "repos/<owner>/<name>/collaborators?permission=maintain"` and adds them to the fixed approvers' account ids (R4; fixed logins are turned into ids with `gh api users/<login>`); writes `<config dir>/issue-watch.d/<name>-approvers.txt` (mode 600, one id per line) and the config JSON (mode 600) with absolute `worktree` (`/home/coder/workspaces/worktrees/<name>/Coordinator`), `approvers_file`, an explicit absolute `state_dir` of `<state dir>/issue-watch/<name>` (R12), the `repo`, the Project id, the account id and `enabled: false`. The result is validated with `cycle.load_config` and `cycle.validate_approvers` before it is kept; a file that exists is never overwritten.

Depends on: Task 12, Task 13, Task 14

Acceptance criteria:
- New `tests/issue_watch/test_generate.py` covers: a repo with one Project, none, several with and without a defaults entry, a failed account read, maintainers added, an existing config left untouched, file modes 600, and two repos getting two different `state_dir` values; every path is under `tmp_path` and the test asserts nothing was written under the real home.
- A generated config passes `cycle.load_config` in the test, and `uv run pytest tests/issue_watch -q` passes.
- The module issues only read calls to GitHub (`gh api user`, `gh api users/<login>`, the Project query, the collaborators call), each REST call with `--method GET`, and its argv builders are covered by the scan Task 9 extends.

## Task 16: Create the two labels on a repo when missing

Create `src/superclaude/cli/issue_watch/repo_init.py` with a function that lists the repo's labels (`gh label list --repo <owner/name>`) and creates `issue-watch:trigger` and `issue-watch:approved` with `gh label create --repo <owner/name>` when absent (requirement R11). It is idempotent and reports `created`, `present` or `failed` per label. The label names come from Task 13. Only the per-repo first run (Task 17) calls the creating function; the loop of Tasks 19 and 20 only reports a missing label (R14).

Depends on: Task 9, Task 13

Acceptance criteria:
- New `tests/issue_watch/test_repo_init.py` covers: both labels missing, one present, both present (no create call), a failed create.
- `tests/issue_watch/test_security_invariants.py` still passes with `repo_init.py` named as an allowed writer (Task 9 documents the scope).
- The label names are read from the defaults of Task 13, not written as literals in the module.

## Task 17: Run the first-run check and enable a repo

Create `src/superclaude/cli/issue_watch/first_run.py` (requirements R7, R18 and R28). For a freshly generated config it runs, in order: config validation (`check-config` logic), label creation through Task 16, `init-state`, one dry-run cycle (`once --dry-run` logic), the lock test (a second run while the lock is held ends with exit 75, using the store lock of `src/superclaude/cli/issue_watch/record.py`) and the restart test (the state document reloads and a second dry run changes nothing). All pass: it rewrites the config with `enabled: true`. Any fails: the config stays `enabled: false` and a one-line reason is written to `<state dir>/issue-watch/<name>/first-run.txt`. It is idempotent: a repo whose state already exists is not re-initialised and a repo already enabled is left alone. It takes the same injectable base directories as Task 15. The live-test record of the runbook stays an owner check and is not part of this task.

Depends on: Task 15, Task 16

Acceptance criteria:
- New `tests/issue_watch/test_first_run.py` covers: all pass gives `enabled: true`; a worktree that does not exist gives `enabled: false` with `worktree_invalid` in the report; a dry-run failure keeps it false; a held lock is detected by the lock test; a state document that does not reload fails the restart test; a second run changes nothing.
- No real `gh`, Orca or network call is made in the tests, and nothing is written under the real home.

## Phase 7: The dispatcher loop

## Task 18: Print the launched and attempted issue from `once`

In `src/superclaude/cli/issue_watch/cli.py` `once_command` (line 118) currently prints `cycle: <reason>` and `exit: <code>`, and prints `would_launch` only in a dry run. Also print `launched: <issue number>` when the cycle launched an issue (`CycleResult.launched_issue`, `cycle.py` line 455) and `attempted: <issue number>` when a launch ended with an unknown outcome (requirement R26). Today `cycle.py` lines 1106 to 1109 return `launch_unknown` without setting `launched_issue`; add an `attempted_issue` field to `CycleResult`, set there. Print each line only once, and only the number, so the dispatcher can read it from a child's output.

Depends on: Task 6

Acceptance criteria:
- `tests/issue_watch/test_cli.py` shows `launched: 12` appears after a confirmed launch, `attempted: 12` appears after an unknown outcome and neither appears otherwise; the existing outputs are unchanged.
- `tests/issue_watch/test_cycle.py` shows `attempted_issue` is set for `launch_unknown` and for no other result.
- `tests/issue_watch/test_no_text.py` still passes (each line contains a number only).

## Task 19: Write the dispatcher core

Create `src/superclaude/cli/issue_watch/dispatch.py` with the loop of requirements R5, R15, R16, R26 and R32. It lists repos (Task 14), calls `ensure_config` and `first_run` (Tasks 15 and 17) for any repo without a config, then starts `superclaude issue-watch once --config <file>` as a child process per repo, one after another. Rules: total loop cap 270 seconds; each child is killed after 255 seconds, longer than the cycle's own 240 second deadline (`DEADLINE_TOTAL_S`, `cycle.py` line 41); repos not reached are skipped and reported; the repo order rotates each sweep (the next start index is kept in a small file under the state directory); the loop stops starting children after the first child whose output has a `launched:` or an `attempted:` line; a child killed or timed out counts as a launch attempt and stops the loop too, unless the repo's `dispatch.json` store (read through `record.py`, read-only) shows no pending or launched entry created during this sweep; `DAY_CAP` stays per repo. Use the `Runner` interface so tests use fakes, pass absolute paths because cron has no PATH, and take the injectable base directories of Task 15.

Depends on: Task 14, Task 15, Task 17, Task 18

Acceptance criteria:
- New `tests/issue_watch/test_dispatch.py` covers: rotation across three sweeps, a stop after the first `launched:` line, a stop after an `attempted:` line, a child killed after 255 seconds with a pending store entry stopping the loop, the same kill with no pending entry letting later repos run, the 270 second cap with unreached repos reported, a repo with no config being generated first, and a failed `orca repo list` giving an error result rather than a clean one.
- A child timeout never kills the loop, and each child's exit code and reason are kept for Task 21.

## Task 20: Add the loop-level account rate wait and the pre-child checks

Extend `src/superclaude/cli/issue_watch/dispatch.py`. Rate wait (requirement R5): when a child's cycle reason is plain `rate_limited` (not the 3600 second clamp reason, `github.py` `rate_limit_wait` line 418), the loop writes one file `<state dir>/issue-watch/account-rate-wait.json` holding the child's `next_permitted_at` and starts no further child until that time; children never write each other's stores. Pre-child checks (R14), each reported rather than silent: the repo's `Coordinator` worktree exists, is a git checkout and its `origin` names the repo; both labels exist (a read-only `gh label list`; a missing label is reported and the repo is skipped, never created by the loop); the Project count is exactly one (Task 15 rule). A failing check skips that repo and records the reason.

Depends on: Task 16, Task 19

Acceptance criteria:
- `tests/issue_watch/test_dispatch.py` adds cases: a `rate_limited` child stops later children until the stored time and a restart of the loop honours the file; a `rate_limit_clamped` child does not write it; a missing `Coordinator` worktree, a wrong origin and missing labels each give a distinct skip reason and no label is created; an expired wait file is ignored.
- All reasons used are written in the audit reason vocabulary (`src/superclaude/cli/issue_watch/audit.py` `REASON_TABLE`, line 26) or a new documented table in `dispatch.py`.

## Task 21: Add the `run-all` command

In `src/superclaude/cli/issue_watch/cli.py` add a `run-all` command to `issue_watch_group` (decorator at line 94, definition at line 95) that runs the dispatcher of Tasks 19 and 20 and prints one line per repo (repo, result, reason) and an overall line. Exit codes follow the existing set (`_EXIT_*`, lines 34 to 38): 0 for a clean sweep, 2 for a configuration problem in the loop itself, 75 when another sweep holds the loop lock. A second sweep started while one runs exits 75 through a lock file in the state directory (`flock`-style, like `record.py` line 382). It takes a `--dry-run` flag that lists repos and decisions but takes no lock, writes no config, no rotation file and no label and starts no child.

Depends on: Task 20

Acceptance criteria:
- `tests/issue_watch/test_cli.py` covers `run-all` output for a clean sweep, a skipped repo, a held lock (exit 75) and `--dry-run` (no lock taken and nothing written; assert a snapshot of the temp directory, lock file included, is unchanged).
- `uv run superclaude issue-watch run-all --help` exits 0 and `uv run superclaude issue-watch --help` lists `run-all`.
- `uv run pytest tests/issue_watch -q` passes.

## Phase 8: Documentation, the Coder handoff and the requirements record

## Task 22: Document the dispatcher, the launch levels and the completion update

Update `docs/designs/issue-watcher.md` and `docs/designs/issue-watcher-setup.md` for: the `run-all` loop and its caps, the config folder `~/.config/superclaude/issue-watch.d/`, the defaults file, the generator and first-run check (lock test and restart test included), the label creation module as one of two allowed writers beside `complete.py`, the `repo` config key, the per-status commands, the Pipeline field and its four levels (pointing to `docs/designs/issue-watcher-status-pipelines.md`), the approval-void rule, the coordinator-only completion update to `In review`, the `Coordinator` worktree path, and a new section replacing the hand setup steps of the runbook (sections 2 to 5) with the automatic path while keeping the manual commands as a fallback.

Depends on: Task 2, Task 5, Task 7, Task 8, Task 10, Task 21

Acceptance criteria:
- Both files mention `run-all`, `issue-watch.d`, `Coordinator`, `Pipeline`, `In review` and the allowed statuses, checked with `grep -c`.
- `uv run pytest tests/docs -q` passes.

## Task 23: Write the Coder handoff document

Create `docs/designs/issue-watcher-zero-setup-coder-handoff.md` for the Coder template maintainers (requirements R1, R6, R9, R10, R17, R20, R21; Coder issues 515 and 516). It contains: the exact crontab line to install, built from verified values (`*/5 * * * *`, an explicit `PATH`, `flock -n` on a lock under `~/.aidev/`, full path `/usr/local/bin/superclaude issue-watch run-all`, output appended to `~/.aidev/logs/issue-watch.log`), with the tool locations checked on 2026-11-18 (`/home/coder/.config/orca/linux-orca-cli-shim/orca`, `/home/coder/.local/bin/gh`, `/usr/local/bin/superclaude`, `/usr/local/bin/uv`); the content of the central defaults file of Task 13 for the template to save; the `Coordinator` branch and worktree rules (switch to the remote branch when it exists, create it otherwise, path `/home/coder/workspaces/worktrees/<repo>/Coordinator`, origin equal to the repo); the session name `COORD-<RepoName>` and the standing launch-prompt text that gives the coordinator the issue-pipeline duties, including the coordinator-only completion update and the Full Submit push rule; and the open Orca question that `orca worktree create --branch` suffixes a taken name, recorded as open with the reproduction step (R20 is a Coder row and is not verified here). Before writing the cron line, run `env -i HOME=$HOME PATH=/usr/bin:/bin /home/coder/.local/bin/gh auth status` and record whether `gh` stays logged in under cron's environment, and record the result in the file.

Depends on: Task 8, Task 10, Task 21

Acceptance criteria:
- The file lists each of R1, R6, R9, R10, R17, R20 and R21 with the Coder issue number where one exists and the value or text the template must use, or for R20 that it is open with its reproduction step.
- It records the result of the `gh auth status` check under a cron-like environment, whichever way it came out.
- The cron line in the file contains an absolute `PATH`, `flock -n`, the log path and `run-all`.

## Task 24: Record the built and tested results in the requirements file

Update `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`: set each row that Tasks 1 to 23 implemented to `built` with the date and the test evidence (the test files and the passing count from the last full run of `uv run pytest tests/issue_watch tests/issue_pipeline tests/hooks tests/skills tests/commands tests/docs -q`), add a row to "Built and tested" for each task, move any decision still open (R20, R21 and the pipelines that should not end at `In review`) under "Open decisions", and state which rows stay with the Coder repository.

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 11, Task 12, Task 13, Task 14, Task 15, Task 16, Task 17, Task 18, Task 19, Task 20, Task 21, Task 22, Task 23

Acceptance criteria:
- Every row R1 to R32 has a status of `built`, `decided (Coder repo)` or `open`, and none is left as an earlier `decided (not built)` or `open` when its task is done.
- The "Built and tested" table has an entry per task with a test file name and a count.
- `make verify-sync` is clean.
