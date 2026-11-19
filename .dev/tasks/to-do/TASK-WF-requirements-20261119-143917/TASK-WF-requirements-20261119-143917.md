---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-requirements-20261119-143917
version: "1"
priority: Medium
created_date: "2026-11-19"
---

# Zero-setup issue watcher v5: status gate, approval provenance, per-status commands, closed ship gate, coordinator-only completion update, hardened launch-level guard, repo threading, config generator and dispatcher loop

Source: ./source.md
Goal: The issue watcher can be switched on in any workspace with no per-user setup. It acts only on the allowed Project statuses and only on an approval given after the issue's last Project change, picks its command from the issue's Status and its launch level from the Project's Pipeline field (None, Worktree, Full, Full Submit), launches only Pipeline None until a reviewed commit opens the ship gate, serves every Orca repo through one dispatcher that cron can run, writes each repo's configuration, approvers and labels itself, and, when the work is finished, has the coordinator comment on the issue and move its Status to In review. A launched agent can never write to an issue, a label or a Project at any level.

## Constraints

- Scope is the IronClaude repository only. The Coder template work (requirements R1, R6, R9, R10, R17, R20, R21; Coder issues 515 and 516) is not implemented here; Task 27 hands it over with exact values.
- This plan applies requirement R33, which adopts the remediation proposal `.dev/remediation/watcher-plan-v3/remediation-proposal.md` with the owner's answers of 2026-11-19: the ship gate stays closed, the `updatedAt` observation is run, self-approval is warn-only, `~/.config/superclaude` joins the guard's tamper tokens, all four pipelines end at In review, and the extra guard refusals are confirmed. It also applies requirement R34, the five blocking corrections of the fourth review (P4-1 to P4-5): the coordinator's approval read names its repo (Tasks 15 and 16), an empty Pipeline has no time to compare (Tasks 3 and 5), the claim-time approval refusal is tested where it is enforced (Task 11), the guard pattern for `issue-pipeline complete` is anchored on the verb word (Task 13), and the worker brief is tested at level `none` only (Tasks 6, 10 and 11).
- Edit `src/superclaude/`, then run `make sync-dev` and `make verify-sync`. Never edit or stage anything under `.claude/` (only `.claude/settings.json` is tracked). The tracked plugin mirror `plugins/superclaude/hooks/scripts/launch-level-guard.sh` is changed together with its source.
- Python only through UV (`uv run pytest`, `uv run ruff`). Tests use the faked `gh` and Orca runners already in `tests/issue_watch/conftest.py`; no task runs the watcher against the real GitHub or Orca, except the read-only schema check of Task 3 and the read-only reads of Task 4.
- `src/superclaude/cli/issue_watch/github.py` stays read-only: no mutation, no POST to a REST path (security invariant NG-2, `tests/issue_watch/test_security_invariants.py`). The only modules that write to GitHub are two new ones outside `github.py`: `src/superclaude/cli/issue_pipeline/complete.py` (Task 12: result comment and Status move, run only by the coordinator) and `src/superclaude/cli/issue_watch/repo_init.py` (Task 20: labels).
- Only the coordinator writes to an issue, a label or a Project item (owner decision of 2026-11-19; `src/superclaude/core/WORKER-CONTRACT.md` lines 241 to 243 and 300), and only under that issue's grant row. An agent launched at Worktree, Full or Full Submit, and every worker, never runs `issue-pipeline complete`, never posts an issue comment and never changes a label or a Project field; it reports through its result file `.dev/issues/<N>/result.md`. The launch-level guard refuses every `gh issue`, `gh label` and `gh project` write at every level, Full Submit included (Task 13), and every `gh api` write at every level. This is a text check on `gh` commands only: a script or another HTTP client is not seen. The complete control is a token with no issues or projects write for launched agents (a Coder row, owner decision). This is the one place the plan goes beyond issue verbs.
- Governed means a session with a record in the launch-level store: the agents launched at Worktree, Full and Full Submit, and bound workers. Not governed: the watcher-launched `--pipeline none` claim session and the coordinator. The claim session's two marked comments are allowed by design, and it reads untrusted issue text under the launch login.
- The approval label, the allowed Project Status, the approval-void rule of Task 5 and the "edited after approval" refusal (`predicates.py`) stay the gate. Nothing in this plan removes or auto-satisfies them. The plan-hash approval row (`src/superclaude/cli/issue_pipeline/approval_record.py`) is created only from a worker's `ask` that carries the plan hash (`WORKER-CONTRACT.md`, WC-17), never from claim-time fields. Approval by the launch account is accepted unless the owner sets the exclusion key `approval_excluded_ids` (Task 9, warn-first).
- The cron watcher may launch every Pipeline level as a capability (owner, 2026-11-19), but the ship gate of Task 8 is closed: until a reviewed commit flips `GOVERNED_LEVELS_ALLOWED` and un-skips the launch-level observations (`tests/hooks/test_launch_level_observations.py`), only Pipeline None launches and every other level ends `level_gated`. Full Submit commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`; it never merges. For an issue the owner has put at Full Submit and approved with the approval label after the last Project change, that setting is the person's go for that issue's push and pull request, and nothing else is pushed.
- `~/.config/superclaude` was not in the guard's tamper tokens (guard line 764); Task 13 adds it. Until that lands, the exclusion key and any future config key are as writable as the approvers file, so the exclusion limits an honest but injected session, not a hostile one.
- The term is "coordinator", never "orchestrator". The coordinator branch and worktree are both named `Coordinator`; the session is named `COORD-<RepoName>`.
- Tasks that edit the same file run in plan order, never in parallel: `cycle.py` (Tasks 5, 7, 8, 9, 16, 22), `launch.py` (Tasks 7, 8, 16), `github.py` (Tasks 3, 15), `predicates.py` (Tasks 1, 3, 5, 7, 9), `audit.py` (Task 8), `launch-level-guard.sh` (Task 13), `WORKER-CONTRACT.md` (Tasks 11, 14), `issue_pipeline/cli.py` (Tasks 14, 15, 16), `issue_pipeline/reads.py` (Task 15), `test_security_invariants.py` (Tasks 3, 7, 12, 15). Task 1 leaves `cycle.py` unchanged.
- Every new module that writes under the user's home takes an injectable base directory, and its tests run with every path inside `tmp_path` and assert nothing was written under the real home.
- Do not switch any real watcher on, claim a real issue, install a real cron entry, move a real issue's Status or start a worker for a real issue. Each generated config starts with `enabled: false` and only the automatic first-run check of Task 21 may turn it on.

## Phase 1: Status gate, field reads and approval provenance

## Task 1: Replace the Backlog check with a Status allow-list

In `src/superclaude/cli/issue_watch/predicates.py`, change `project_check` (lines 262 to 271) so an issue passes only when it is the one live item of the configured Project and its Status name is one of `Research`, `Spec`, `Plan` or `Debug` (requirement R22). Every other value, including `Backlog`, `Ready`, `In progress`, `In review`, `Done`, an empty Status and any status added to the board later, returns `project_mismatch`. Keep the reason code `project_mismatch` (it is in `audit.REASON_TABLE`, `audit.py` line 72) so no reason table changes. Name the allowed set as one module constant, which Task 12 imports instead of copying the four words. The callers `cycle.py` lines 958 (`_examine`) and 1015 (`_revalidate`) keep calling `project_check` unchanged.

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

## Task 3: Read the Pipeline field and the Status and Pipeline value times

Depends on: Task 1

In `src/superclaude/cli/issue_watch/github.py`, extend `PROJECT_ITEMS_QUERY` (lines 88 to 103). Today it reads only the Status `name`. Change it to two aliased single-select reads, `status: fieldValueByName(name: "Status")` and `pipeline: fieldValueByName(name: "Pipeline")`, each `... on ProjectV2ItemFieldSingleSelectValue { name createdAt updatedAt }`. Extend `_project_item` (lines 764 to 775) to parse them, and add `pipeline_name: str | None`, `status_changed_at: datetime | None` and `pipeline_changed_at: datetime | None` to the `ProjectItem` dataclass in `src/superclaude/cli/issue_watch/predicates.py` (around lines 113 to 118). The item-level `updatedAt` is not read (a label or a comment may move it; owner decision R33). The Pipeline values on the board are `None`, `Worktree`, `Full` and `Full Submit`; an absent Pipeline value is `pipeline_name = None` and `pipeline_changed_at = None`, which means the Pipeline has no value and so no time (it is the `None` pipeline); it is not an unreadable time. A Status or Pipeline value object that is present but carries no `createdAt` or `updatedAt`, or a time that does not parse, fails the whole read with the existing `unreadable` outcome. The query stays read-only. Requirement R31 relies on the value times: before relying on them, run one read-only GraphQL schema query for the type `ProjectV2ItemFieldSingleSelectValue` (`gh api graphql -f query='query { __type(name: "ProjectV2ItemFieldSingleSelectValue") { fields { name } } }'`) and save its output to `./artifacts/t3-single-select-value-fields.txt`. If either `createdAt` or `updatedAt` is not listed, stop and return the fallback of R31 (a level-specific approval label) to the owner.

Acceptance criteria:
- `./artifacts/t3-single-select-value-fields.txt` exists and lists both `createdAt` and `updatedAt` (or the task stops with the R31 fallback reported).
- `tests/issue_watch/test_github.py` parses a fixture with a Pipeline value and value times, a fixture with a null Pipeline (it parses to `pipeline_name = None` and `pipeline_changed_at = None`, not an error) and a malformed one (a present value with a missing or unparseable time gives the existing `non_json` or `unreadable` outcome, not an exception). The shape fixture `tests/issue_watch/fixtures/_assumed_shape/graphql_project_items.json` is updated.
- `tests/issue_watch/test_security_invariants.py` still passes: the query contains no `mutation`.
- Every other constructor call of `ProjectItem` in `tests/issue_watch/` is updated, and `uv run pytest tests/issue_watch -q` passes.

## Task 4: Record the owner's observation of the value times

Depends on: Task 3

This task needs the owner's hands: a field change is a GitHub write, which no agent may run (Constraints). The owner changes the Pipeline, then the Status, then applies the approval label, in this order, on one throwaway issue in a test Project. After each owner step, the executor runs the read-only query of Task 3 for that issue's Project item and records the Status and Pipeline value times in `./artifacts/t4-updatedat-observation.md`: before any change, after the Pipeline change, after the Status change and after the label. The task asks the owner in chat for each step and does not continue until the owner answers. The file ends with an outcome line. Field change moves the matching value time and the label moves neither: rule R31 stands as written. A field change that moves no time: the rule would fail open, so the task stops and returns the level-specific approval label (the R31 fallback) to the owner. A label that moves a value time: every approval would be voided, so the task stops with the same fallback.

Acceptance criteria:
- `./artifacts/t4-updatedat-observation.md` exists, holds the four recorded reads with their timestamps and ends with exactly one outcome line naming one of the three outcomes above.
- When the outcome is not "rule stands", no later task that reads the value times starts, and the fallback is reported to the owner in chat.
- No real issue, Status or label is changed by the executor, and the throwaway issue and Project are named in the file.

## Task 5: Void an approval when the Status or Pipeline value changed after it

Depends on: Task 1, Task 3, Task 4

Implement requirement R31 in `src/superclaude/cli/issue_watch/predicates.py` and `src/superclaude/cli/issue_watch/cycle.py`. Add a predicate next to `edited_after_approval` (line 258) that returns the existing reason `edited_after_approval` when the later of the value times that exist is at or after the approval's time: the Status value time, and the Pipeline value time only when the Pipeline has a value. An absent Pipeline value contributes no time, so an issue whose Pipeline is empty (the `None` pipeline, the only level the closed ship gate lets launch) is judged on its Status time alone; a Pipeline cleared after the approval reads the same way and launches at `None`, the lowest level, so it raises no authority. An equal time counts as changed, as in `unchanged_since` (one-second resolution, line 257), and a Status name with no Status time also refuses (Task 3's read layer already rejects a present value with a missing or unparseable time). In `_examine` (line 915) call it after `unchanged_since` (lines 949 to 956) and before `project_check` (lines 957 to 960). In `_revalidate` (line 979) call it after the approval reread (lines 1007 to 1011) and the items reread (lines 1012 to 1014), and before `project_check`, so a Pipeline or Status changed after the approval label cannot launch and the specific reason wins. Reuse the reason code so no reason table changes.

Acceptance criteria:
- `tests/issue_watch/test_predicates.py` covers: value times before approval pass, at the same instant refuse, after approval refuse, a Status name with no Status time refuses, a value an hour older than the approval passes, an empty Pipeline with a Status time before the approval passes, a Pipeline cleared after the approval passes at the `None` pipeline, and a Pipeline value changed after the approval refuses.
- `tests/issue_watch/test_cycle.py` shows a Pipeline raised from None to Full Submit after approval ends with `edited_after_approval` and no launch call, both at examine time and between examine and launch, and shows an approved issue whose Pipeline is empty and whose Status time is before the approval launches with `--pipeline none` (it is not refused as edited after approval).
- `tests/issue_watch/test_security_invariants.py` passes and `uv run pytest tests/issue_watch -q` passes.

## Phase 2: Design decisions for per-status commands, launch levels and completion

## Task 6: Write the design note for per-status commands, launch levels and completion

Create `docs/designs/issue-watcher-status-pipelines.md`. It records the owner's decisions of 2026-11-18 and 2026-11-19 (requirements R23, R24, R25, R29, R31, R32, R33, R34) and decides every interface the later tasks implement. Research runs `/sc:research`; Spec runs `/sc:design` when the issue is well defined and `/sc:brainstorm` when it is not, with a handoff to `/sc:design` for high complexity or scope; Plan runs `/sc:workflow`; Debug runs `/sc:troubleshoot --fix`; Ready and every other status trigger nothing. The Pipeline field maps to the claim command as None or empty = `--pipeline none`, Worktree = `--pipeline worktree`, Full = `--pipeline full`, Full Submit = `--pipeline full --submit` (`src/superclaude/commands/issue.md` lines 43, 44 and 56 accept only worktree, full and none plus the `--submit` flag).

Depends on: Task 1, Task 3, Task 5

The note must decide, each with a stated reason:
- The exact launch prompt text the watcher sends for each Status and Pipeline pair, and the pattern that pins it (today `PROMPT_PATTERN`, `src/superclaude/cli/issue_watch/launch.py` line 33, with the prompt built at line 92). The launch-level guard has no prompt allow-list, so the pattern in `launch.py` is the only pin.
- A table of Status by launch level: whether the command runs, runs in a limited form or is refused, and the end Status of each pair. Default to decide against: `/sc:troubleshoot --fix` edits code, so at Worktree ("propose next steps, halt") it runs without `--fix` and at Full and Full Submit with `--fix`.
- Debug at level `none`: the coordinator's worker runs `/sc:troubleshoot` without `--fix`, because a level `none` worker stops before any code change and code edits start only at Full and Full Submit. The worker brief is used only at level `none`; at the other levels the launched agent runs the command from its launch prompt, so the brief has no level slot.
- Which session runs the Status command at each level: at `none` the coordinator starts a worker from the brief template; at `worktree`, `full` and `full submit` the agent that `/sc:issue --claim` launches runs it from its launch prompt. State how the Status command enters `launch-prompt.md` and the worker brief.
- How the Status and Pipeline reach the coordinator (which stored field or file), since a `--pipeline none` claim creates no worktree record.
- Who judges "well defined" for Spec and where the reason is recorded (the claim's `issue-summary.md`).
- Which record the "automatic approval record" of R19 means: the claim-time approval already kept in `dispatch.json` plus the adoption row, versus the plan-hash approval row, which only a worker's `ask` carrying the plan hash may create (R29); and where a claim-time event is refused as plan approval: in `stage_predicates.py` (`label-before-plan`, lines 161 to 170) through `stage-status`, because `approval_record.record_create` cannot tell the two events apart and is not changed.
- The completion update (R24), coordinator only: how the coordinator learns a launched agent has finished (the result file `.dev/issues/<N>/result.md` in the issue's worktree and the `/sc:sweep` report), the closed format of that result file (outcome word, artifact paths, pull request number), what the result comment holds, that only a succeeded outcome moves the Status, that the end Status is held in one named table (all four Status pipelines end at `In review`; the owner confirmed this on 2026-11-19), the per-run marker `<!-- sc:issue:result issue=<N> run=<approval_event_id> -->` and why the approval event id is its key (each relaunch needs a fresh approval), the compare-and-set rule (the Status moves only from Research, Spec, Plan or Debug, otherwise the comment is posted with `status_moved_by_person`), idempotency, and what a failed, blocked or partial outcome does (comment only).
- That the coordinator's own comment never voids an approval (comments by the watcher's own login are skipped by `unchanged_since`, `predicates.py` lines 253 to 255), while its move to In review changes the Status value time and so voids the approval by design: a retry or relaunch needs a fresh approval label, and In review fails `project_check`, so the owner moves the Status back first.
- The Full Submit push rule: the wording that replaces the push sentence in `src/superclaude/core/WORKER-CONTRACT.md` (line 245): "At Full Submit the launched agent pushes only its own feature branch to origin and opens the pull request through /sc:pr-submit; the owner's Pipeline value plus an approval later than the last Project change is the go for that issue only. The coordinator never pushes worker commits on that basis; for every other push the rule above stands."
- For each of the five commands, whether it can run as the coordinator's worker, checked against `src/superclaude/core/WORKER-CONTRACT.md` line 23 (the never-as-worker list) and each command file under `src/superclaude/commands/`, with an alternative where it cannot.
- Which sessions the guard governs and that the counted marker login is the workspace's single `gh` login, shared by the watcher, the coordinator and launched agents.

Acceptance criteria:
- The file exists and has a table with one row per Status (Research, Spec, Plan, Debug, Ready) giving the command, the prompt text for each of the four Pipeline values, the end Status per level, and whether it can run as a worker with the file and line that shows it.
- Every decision listed above has a stated decision; a command that cannot run as a worker has a stated alternative, not a blank.
- The note says which files change in Tasks 7 to 14 by path.

## Phase 3: Per-status prompts, ship gate and launch levels

## Task 7: Build the per-status prompt from the revalidated item

Depends on: Task 1, Task 3, Task 5, Task 6

Implement the prompt rules of Task 6 in `src/superclaude/cli/issue_watch/launch.py` (`build_claim_prompt` at line 84, `PROMPT_PATTERN` at line 33, `launch_argv` at line 95, `retry_argv` at line 119) and in `src/superclaude/cli/issue_watch/cycle.py` (`_examine` at line 915, `_revalidate` at line 979 and `_launch` at line 1026). Today `_launch` builds the prompt at line 1054 and only then calls `_revalidate` (line 1058), which rereads the project items (lines 1012 to 1016) but checks only `project_check` (requirement R27). Change the order so the prompt is built from the item that `_revalidate` rereads. The order inside `_revalidate` is fixed: the approval reread (lines 1007 to 1011, `revalidation_failed`), then the value-time rule of Task 5 (`edited_after_approval`), then `project_check` and the comparison of the examined Status and Pipeline with the reread ones (both `revalidation_failed`). Add a small helper next to `project_check` in `predicates.py` that returns the one live item. `status_report` (`cycle.py` line 1270) builds a retry command with `build_claim_prompt`; it must keep printing a valid command for every allowed Status and Pipeline. Keep `ValueError` for any input that does not match, so no other text reaches `--prompt`.

The seven test files that pin the old prompt move into this task because `launch_argv` rejects any prompt that does not fullmatch `PROMPT_PATTERN` (`launch.py` line 101) and the tree would be red until a later task: `tests/issue_watch/test_cli.py`, `test_cli_e2e.py`, `test_crash_injection.py`, `test_cycle.py`, `test_launch.py`, `test_no_text.py` and `test_security_invariants.py` (45 lines hold `--pipeline none`, counted by the remediation debate; recount with Grep before editing). The new `_PROMPT_RE` in `test_security_invariants.py` is written out in the test, not imported from `launch.py`, so the test pins the closed set instead of mirroring it. Its docstring (lines 5 to 6), `_PROMPT_RE` (line 67), the malformed list and the prompt assertions are rewritten.

Acceptance criteria:
- `tests/issue_watch/test_launch.py` covers the prompt for each allowed Status crossed with each Pipeline value and an empty Pipeline, and rejects an invalid number, an unknown Status, an unknown Pipeline, extra text and `--submit` without `full`.
- `tests/issue_watch/test_cycle.py` shows the prompt sent for an issue in each allowed Status, and shows two refusals with every value time kept before the approval: Status changed from Research to Debug between examine and launch, and Pipeline lowered from Full Submit to None between examine and launch. Both end with `revalidation_failed` and no launch call. It also shows the overlap case: a Pipeline lowered with a value time after the approval ends `edited_after_approval`.
- `uv run pytest tests/issue_watch -q` passes with all seven files updated, and `tests/issue_watch/test_no_shell.py` passes (no new text path, no shell).
- The `once` dry-run output (`would_launch`) keeps its shape, and the `status_report` retry command is valid in a test for each Status.

## Task 8: Add the closed ship gate

Depends on: Task 7

Add `GOVERNED_LEVELS_ALLOWED = False` to `src/superclaude/cli/issue_watch/launch.py`. In `_examine` (`cycle.py` line 915), before `_launch` is reached (`_launch` is at line 1026 and sets `c.launching` at line 1028, and its dry run returns at lines 1029 to 1035, so the check must sit before it to keep `would_launch` honest), raise `_Skip("level_gated")` for any Pipeline other than None while the constant is False. Add one row `"level_gated": ("skip", 0)` to `REASON_TABLE` in `src/superclaude/cli/issue_watch/audit.py` (line 26, next to the rows at lines 71 to 80). No config key or environment variable is the switch: the config directory is not tamper-protected, so such a switch would be as writable as the approvers file. Add a coupling test in `tests/hooks/test_launch_level_observations.py` beside `_PENDING` (line 79): when the constant is True, none of `OB-H1 item 1`, `OB-H1 item 5`, `OB-H2` and `OB-H3` appears in `_PENDING`, so the gate opens only in the commit that un-skips the observations. Record in the design note that `refs/claim.md` line 133 (an observation of item 1 before any governed claim) and `docs/designs/sc-issue-launch-level-hook.md` line 201 (item 1 only for `full` and `--submit`) disagree, that one boolean follows the stricter text, and that a per-level split stays an owner option.

Acceptance criteria:
- `tests/issue_watch/test_cycle.py` shows an issue at Worktree, Full and Full Submit ends `level_gated` with no launch call and no store write, an issue at None launches, and a dry run shows no `would_launch` for a gated level.
- `tests/issue_watch/test_audit.py` (or the test that counts `REASON_TABLE` rows) is updated for the new row and passes.
- The coupling test passes with the constant False and would fail if the constant were True with the four observations still in `_PENDING`.
- `uv run pytest tests/issue_watch tests/hooks -q` passes.

## Task 9: Add the warn-only self-approval exclusion

Depends on: Task 7

In `src/superclaude/cli/issue_watch/predicates.py` add a keyword `excluded_ids: Collection[int] = ()` to `approval_of` (line 185); an approval whose `actor_id` is in that set returns `not_approved`, checked next to the approver test (lines 216 to 223). In `src/superclaude/cli/issue_watch/cycle.py` add one closed-set key `approval_excluded_ids` (a list of integers, default empty) to `_TOP_KEYS` (line 58), `Config` and `load_config`, and pass it at both call sites of `approval_of` (`_approve`, line 883, and `_revalidate`, line 998). With the default empty list nothing changes. In `src/superclaude/cli/issue_watch/cli.py` make `check-config` (lines 185 to 198, which prints only "configuration is valid" and three info lines today) print one warning line `approver_is_launch_account` when the approvers file holds the config's own account id (`self.account_id`, `cycle.py` lines 767 to 768). The hand-written config for this host lists account 7361222 both as the account and as an approver, so the warning shows there. The Task 19 generator never writes the account id into a generated approvers file, and the Task 21 first-run report prints the same warning (those tasks name it).

Acceptance criteria:
- `tests/issue_watch/test_predicates.py` shows an approval by an excluded id returns `not_approved` and the same event by another approver passes.
- `tests/issue_watch/test_cycle.py` shows a launch-account approval at examine time gives no launch when the key lists that account, and none when the approval appears between examine and launch; with the default empty list the same approval launches as before.
- `tests/issue_watch/test_cli.py` shows `check-config` prints `approver_is_launch_account` for an approvers file that holds the account and does not print it otherwise, and an unknown config key is still rejected.
- `uv run pytest tests/issue_watch -q` passes.

## Task 10: Update the claim command, the skill and the result file for the new prompts

Depends on: Task 6, Task 7

Apply the prompt decisions of Task 6 to the claim surface: `src/superclaude/commands/issue.md`, `src/superclaude/skills/sc-issue-protocol/SKILL.md`, `src/superclaude/skills/sc-issue-protocol/refs/claim.md` and `src/superclaude/skills/sc-issue-protocol/templates/next-steps.md` accept the new prompt forms, carry the Status command into the launch prompt, and make the last step of a launched agent's prompt the writing of its result file `.dev/issues/<N>/result.md` in the closed format of Task 6 (no GitHub write). The launch prompt tells the agent that only the coordinator writes to an issue, a label or a Project. The launch-level guard is not changed here (Task 13). Update every test and document outside `tests/issue_watch` that pins the old fixed prompt `/sc:issue --claim <N> --pipeline none`. The files that hold the literal today (checked with Grep on 2026-11-19, the seven `tests/issue_watch` files excluded because Task 7 owns them) are `src/superclaude/cli/issue_watch/launch.py` (Task 7), `src/superclaude/commands/issue.md`, `src/superclaude/core/WORKER-CONTRACT.md`, the three skill files named above, `tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py`, `docs/user-guide/commands.md`, `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` and `docs/designs/` files `issue-pipeline-fu1.md`, `issue-watcher-setup.md`, `issue-watcher.md`, `sc-issue-claim-pipeline-flag.md`, `sc-issue-command.md`, `sc-issue-launch-level-hook.md`. Run the Grep again before editing and list every hit in the commit message. Run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- `grep -rn -- "--pipeline none" src tests docs plugins` has no hit that still presents it as the only watcher prompt.
- `tests/commands/test_issue_command.py` and `tests/skills/test_issue_protocol.py` show each allowed prompt form is accepted, a prompt with extra text, an unknown level or `--submit` without `--pipeline full` is refused, and the launch prompt ends with the result-file step and contains no `gh` write or `issue-pipeline complete` call. The same tests show `/sc:troubleshoot` is limited (no `--fix`) in the Worktree launch prompt and carries `--fix` in the Full and Full Submit prompts.
- `uv run pytest tests/commands tests/skills tests/hooks -q` passes.
- `make verify-sync` is clean and no `.claude/` path is staged.

## Task 11: Update the coordinator duties, the worker brief and the push rule

Depends on: Task 6, Task 7

Apply the remaining decisions of Task 6 to `src/superclaude/core/WORKER-CONTRACT.md` section "Issue pipeline duties" (line 291 onward) and to the rule that a push needs the person's go (line 245). The duties section names the Status-to-command table, says how the coordinator reads the Status and Pipeline, covers claims at every level (today it covers only `--pipeline none`, line 293), and names which stored record is the automatic approval record (R29): the claim-time approval in `dispatch.json` and the adoption row, never the plan-hash row. Line 242 (every such action targets `IronbellyOrg/IronClaude`) is reworded to say each action targets the repo the issue belongs to, never the SuperClaude upstream, and the `stage-status` call at line 298 names the issue's repo with `--repo` (Task 15 implements the flag). The brief is used only at level `none` (Task 6) and has no level slot. It states that after the coordinator mirrors the Status (line 298) or moves it to In review, the Project values have changed, so any relaunch needs a fresh approval label. Line 245 gets the replacement sentence decided in Task 6, so the coordinator never pushes worker commits on the Pipeline setting. Update the worker brief template `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` and `src/superclaude/cli/issue_pipeline/brief.py` so the brief carries the Command for the issue's Status, keeping the closed-set checks (no issue text reaches the brief). Update `tests/skills/test_worker_contract.py` and `tests/issue_pipeline/test_brief.py` for the new text and rows, and add the claim-time cases below to `tests/issue_pipeline/test_stage_predicates.py` and `tests/issue_pipeline/test_stage_status.py`. `approval_record.py` and `stage_predicates.py` are not changed: the rule that refuses a claim-time event exists. Run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- `tests/issue_pipeline/test_stage_predicates.py` and `tests/issue_pipeline/test_stage_status.py` show that an approval label carrying the claim-time event id and approver id (a `dispatch.json` fixture), dated before the plan reply, gives `approved: false` with the reason `label-before-plan`, and that a label dated after the plan reply is accepted. `tests/issue_pipeline/test_approval_record.py` shows `record_create` refuses a missing or malformed plan hash and a missing adoption row, and that the `record-create` verb requires `--plan-hash`. The duties text says the coordinator calls `record-create` only with evidence that `stage-status` reports as accepted.
- `tests/issue_pipeline/test_brief.py` shows one brief row per allowed Status at level `none` (the only level that uses the brief), that the Debug row at `none` runs `/sc:troubleshoot` without `--fix` (Task 6 table), and that a bad Status, issue number or nonce is refused with a closed reason. The Worktree, Full and Full Submit troubleshoot forms are tested against the launch prompt in Task 10.
- A test shows the Spec judgment: a well-defined issue yields the `/sc:design` row, an issue that is not yields the `/sc:brainstorm` row with the handoff to `/sc:design` for high complexity, and the reason is recorded in `issue-summary.md`.
- `tests/skills/test_worker_contract.py` asserts the new push sentence and the absence of any coordinator push grant tied to Pipeline; `uv run pytest tests/skills tests/issue_pipeline -q` passes.
- `make verify-sync` is clean and no `.claude/` path is staged.

## Phase 4: Completion update and the launch-level guard, coordinator only

## Task 12: Write the result comment and move the Status to In review

Depends on: Task 3, Task 6, Task 7

Create `src/superclaude/cli/issue_pipeline/complete.py` (requirement R24). A function takes the repo, the issue number, the configured Project node id `project_id` (validated against `^PVT_[A-Za-z0-9_-]+$`), the approval event id of the run, an outcome word (`succeeded`, `failed`, `blocked` or `partial`), a pointer to the result summary file and a Runner from `src/superclaude/cli/issue_watch/runner.py`. For `succeeded`, before any write (the comment included) it reads the issue's Project items and selects the one non-archived item of that Project with the helper Task 7 adds next to `project_check`; zero items gives `refused:project_missing`, more than one `refused:project_ambiguous`, and a Status field without an `In review` option `refused:status_option_missing`. It posts one result comment through `gh api --method POST repos/<owner>/<name>/issues/<N>/comments` carrying the marker `<!-- sc:issue:result issue=<N> run=<approval_event_id> -->`, which never contains the claim marker (`predicates.py` line 14); it posts no second comment only when an exact marker written by its own login is present. For `succeeded` only it then sets the Status with the GraphQL mutation `updateProjectV2ItemFieldValue`, and only when the item's current Status is one of the allowed Statuses that Task 1 names as one module constant (imported, not copied); any other current Status (for example a person moved it to Done) posts the comment and returns `status_moved_by_person` without a mutation. A second call still retries the Status move when the first call's move failed. The end Status comes from one named table keyed by the allowed Status (all four map to `In review`), so an exception is a one-line change. A failed, blocked or partial outcome posts the comment and does not move the Status. Result words are closed and no issue or comment text is echoed. The read-then-write is not atomic, so a person's move inside that window can still be overwritten; the module docstring says so. The module lives outside `github.py`, which stays read-only.

Acceptance criteria:
- New `tests/issue_pipeline/test_complete.py` uses the fake runner and covers: succeeded posts one comment and one Status mutation to the `In review` option on the configured Project's item; failed, blocked and partial post a comment and no mutation; an issue on two Projects uses the configured `projectId` and its item id; zero items and two live items in the Project are refused with no write; an item already at Done gets the comment and no mutation (`status_moved_by_person`); a second call with the same run id and own-login marker posts no comment; another run id does not suppress it; a marker posted by another login does not suppress it; a failed first move is retried on the second call; an unknown outcome word, a bad issue number, a bad project id and a bad repo are refused before any call; a failed mutation reports a closed failure word and leaves the comment in place; the marker does not contain the claim marker.
- One test shows the coordinator's own comment leaves `unchanged_since` clean (comments by the watcher's own login are skipped).
- `tests/issue_watch/test_security_invariants.py` is updated so its NG-2 scope and header (line 10) read `github.py` and the cycle, name `complete.py` and `repo_init.py` as the only allowed writers, and the argv scan (lines 712 to 730) also covers the read calls of the new modules; the test still proves `github.py` has no mutation.
- `tests/issue_watch/test_module_boundaries.py` passes with the new module, and `uv run pytest tests/issue_pipeline tests/issue_watch -q` passes.

## Task 13: Close the Full Submit hole in the launch-level guard

Depends on: Task 6

Change `src/superclaude/hooks/scripts/launch-level-guard.sh` and its tracked mirror `plugins/superclaude/hooks/scripts/launch-level-guard.sh` together (never `.claude/`). The H3 case today puts `issue create`, `issue edit` and `issue comment` in the SUBMIT row (line 653) and SUBMIT is allowed at Full Submit, so a Full Submit agent can write to issues today.

Make these changes in the guard. Remove the three issue verbs from line 653, so it reads `'pr create' | 'pr edit' | 'pr comment' | 'pr ready') LL_CLASSES+='SUBMIT ' ;;`. After the read-allow row at line 652 insert `'project item-list' | 'project field-list') ;;` and then `'issue '* | 'label '* | 'project '*) LL_CLASSES+='ISSUE ' ;;`, so the class fires wherever `gh` appears (not only in command position, unlike the UNKNOWN row at line 654) while `gh issue view`, `list` and `status` stay allowed. Add `ISSUE` to the `for LL_C in` list at line 786, after `GHWRITE`, because a class missing from that list is never evaluated; add `ISSUE:W | ISSUE:WA | ISSUE:F | ISSUE:FS) ll_deny LL-ISSUE ;;` to the case table. Add an `LL-ISSUE` block to the message printer with three parts: Blocked (a GitHub issue, label or project write), Why (only the coordinator writes; a launched session reports through `.dev/issues/<N>/result.md`), You can (write the result file and let the coordinator post). Reword the `LL-SUBMIT` text (lines 70 to 71) from "pull request or issue" to "pull request". Extend the coordinator-only pattern at line 444 with `*issue-pipeline[[:space:]]complete[[:space:]]*` and `*issue-pipeline[[:space:]]complete` (the verb word anchored by spaces, with its own end-of-text form), `*issue_pipeline.complete*`, `*issue_pipeline/complete.py*`, `*issue_pipeline*import*complete*` and `*issue_pipeline*complete.run*`. Never use `*issue-pipeline*complete*`, which refuses `plan-hash` for a path that contains the word completed, or `*issue_pipeline*complete*`, which refuses `uv run pytest tests/issue_pipeline/test_complete.py` in a launched session. The matcher runs on the command text with quotes and backslashes deleted and runs of `/` squeezed (guard line 428), so each alternative is a substring match on that text. The pattern is best effort, not a control; the grant-row rule (`WORKER-CONTRACT.md` line 300) is the control. Accepted over-match, with a test row: a governed command that names `issue_pipeline/complete.py` (`sed`, `git diff`, `ruff`) is refused. Known unmatched forms, stated in the task: string-built names (`getattr`, `importlib` with a split name). The refusal case `p.complete.run()` is written as a full statement that imports the module, because a bare `p.complete.run()` cannot run and no alternative matches it. Add `*.config/superclaude*` to the tamper tokens at line 764 (owner decision of 2026-11-19), with the stated over-match that any governed command whose text mentions that path is refused, reads included. Raise the version stamp from 1 to 2 together in line 10 of the guard and of the mirror, `GUARD_VERSION_LINE` in `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (line 839) and the three test pins (`tests/hooks/test_launch_level_guard.py` line 251, `tests/skills/test_issue_orca_worktree.py` lines 1283 and 1914 to 1916), so a host with the old guard fails the install preflight. The release note says hosts run `superclaude install --force` before the next claim. `stage-status` stays unclassified and the task says so.

Acceptance criteria:
- `tests/hooks/test_launch_level_guard.py` moves the three issue rows (lines 2743 to 2745) out of the SUBMIT oracle into a new `ISSUE` row with `LL-ISSUE` at all four levels, removes them from the T-GH-5 list (lines 2875 to 2876), and adds the class to the expected-result grid. At Worktree, Worktree-allow, Full and Full Submit these are refused with `LL-ISSUE`: `gh issue create`, `gh issue edit 5 --add-label issue-watch:approved`, `gh issue comment 5`, `gh issue close 5`, `gh label create x`, `gh project item-edit`, `true && gh issue comment 5` and the `-R o/r` forms. These stay allowed at every level: `gh issue view 5`, `gh issue list`, `gh project item-list`, `gh project field-list`; `gh pr comment 5` still passes at Full Submit.
- `tests/hooks/test_launch_level_guard.py` also asserts each new code prints a non-empty three-part message, that an edit or shell redirect on `issue-watch.json` under the config directory is refused, and that a guard stamped 1 is refused after the bump. It adds the unbound-session-allowed test, labelled "documents, does not endorse".
- `tests/hooks/test_launch_level_guard_worker.py` shows these are refused with the tamper code: `superclaude issue-pipeline complete --repo o/r --issue 5`, the `uv run` form, `python -m superclaude.cli.issue_pipeline.complete`, `from superclaude.cli.issue_pipeline import complete`, `from superclaude.cli.issue_pipeline.complete import run`, `python -c "from superclaude.cli import issue_pipeline as p; p.complete.run()"` and `superclaude issue-pipeline complete` at the very end of the command text; and these stay allowed: `issue-pipeline plan-hash`, `check-approval`, `uv run pytest tests/issue_pipeline/test_complete.py`, `uv run pytest tests/issue_pipeline/test_complete_cli.py`, `plan-hash` with a path containing "completed" and `git commit -m "docs: complete the fu1 design"`. The accepted over-match has its own rows: governed `sed`, `git diff` and `ruff` on `issue_pipeline/complete.py` are refused.
- `uv run pytest tests/hooks tests/skills tests/issue_pipeline tests/issue_watch -q` passes, `make verify-sync` is clean and no `.claude/` path is staged.

## Task 14: Add the coordinator-only `complete` verb and make the coordinator call it

Depends on: Task 10, Task 11, Task 12, Task 13

In `src/superclaude/cli/issue_pipeline/cli.py` add an `issue-pipeline complete` verb (next to `release-worker` at line 200 and `stage-status` at line 335) that calls Task 12 and prints one closed result word. It takes `--repo`, `--issue`, `--project-id`, `--run` (the approval event id) and the outcome; the coordinator copies the project id from the repo's watcher config. Update `src/superclaude/core/WORKER-CONTRACT.md` section "Issue pipeline duties" so the coordinator runs the verb under the issue's grant row after it has read a worker's `worker_done` contract (level None) or a launched agent's result file (other levels), per Task 6, and passes the run id. The duties section states that a failed outcome never moves the Status and that the guard pattern of Task 13 is best effort. Run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- A new `tests/issue_pipeline/test_complete_cli.py` covers the verb: a succeeded call prints the closed success word, a refused call prints a `refused:` word and exits 1, the project id and run id are passed through, and no verb output holds issue text.
- The duties section names the verb, the grant-row rule and the rule that a failed outcome never moves the Status; `tests/skills/test_worker_contract.py` is updated and `uv run pytest tests/hooks tests/skills tests/issue_pipeline -q` passes.
- `make verify-sync` is clean and no `.claude/` path is staged.

## Phase 5: Thread the repo through the watcher

## Task 15: Pass the repo into the GitHub reads and the coordinator's stage evidence read

Depends on: Task 3, Task 14

First read the DF-14 rationale (the research file that `tests/issue_watch/test_security_invariants.py` line 919 cites) and stop if it forbids non-null variables outright. In `src/superclaude/cli/issue_watch/github.py`, replace the module constant use of `REPO` (line 37; used at lines 187, 208 and 259) and the hard-coded owner and name inside `EDITS_QUERY` (line 74) and `PROJECT_ITEMS_QUERY` (line 88) with a `repo` parameter (`owner/name`) on `argv_discover`, `_argv_rest_page`, `argv_events` (line 218), `argv_comments` (line 223), `_argv_graphql`, `argv_edits`, `argv_project_items`, `argv_reread` and on the public reads `discover`, `events`, `marker_comments`, `edits`, `project_items` and `reread`. GraphQL queries take `$owner` and `$name` as variables, declared `String!` because `repository(owner:, name:)` needs non-null values; the cursor `$after` stays nullable. Keep `REPO` as the default value of the `github.py` functions so the watcher's own tests keep working unchanged, but `src/superclaude/cli/issue_pipeline/reads.py` takes no default: `read_stage_evidence` and the comments read (`argv_comments_projected`, `reads.py` lines 65 to 67) get a required `repo` parameter that they pass to `gh.events`, `gh.edits` and the comments call (`reads.py` lines 142 and 148). Today the coordinator's `stage-status` verb reads IronClaude's issue whatever repo it serves (`src/superclaude/cli/issue_pipeline/cli.py` line 279 calls `gh.reread` with no repo and line 282 calls `read_stage_evidence`; `github.py` line 37 fixes `REPO`), so a coordinator for another repo would judge approvals from the wrong issue. In `cli.py` add `--repo` (strict `owner/name`, required) to `stage-status` (the verb at line 368 and `_stage_status`, lines 266 to 305) and pass it to `gh.reread` and `read_stage_evidence`; Task 16 makes it optional with the config's `repo` as the default. Validate the value with a strict `owner/name` pattern and raise `ValueError` before any call for anything else. The test `tests/issue_watch/test_security_invariants.py` lines 911 to 919 asserts the old literal `repository(owner: "IronbellyOrg", name: "IronClaude")` and the absence of `$owner` and `$name`; rewrite it: `$after: String` stays nullable, the regex `\$(\w+): String!` yields exactly the names owner and name, `query.count("String!") == 2`, no literal repository, no `mutation` and no `subscription`. A default value such as `$owner: String = "IronbellyOrg"` is not used, because a missing variable would silently read the fork.

Acceptance criteria:
- `tests/issue_watch/test_github.py` shows each argv, `argv_events` and `argv_comments` included, carries the passed repo, and rejects `a/b/c`, an empty string, a value with a space or a leading dash.
- `tests/issue_watch/test_security_invariants.py` lines 911 to 919 are rewritten as described and pass, and the no-mutation checks on the query constants still pass.
- `tests/issue_pipeline/test_stage_status.py` and the test file that covers `read_stage_evidence` show that `stage-status` without `--repo` is a usage error (exit 2), that a `--repo` that is not `owner/name` is refused, that with `--repo Other/Repo` every argv of the reread, events, edits and comments calls carries `Other/Repo` and none carries `IronbellyOrg/IronClaude`, and that an approval label on the IronClaude issue of the same number never approves the other repo's issue (the fake runner serves different labels per repo).
- `uv run pytest tests/issue_pipeline tests/issue_watch -q` passes.

## Task 16: Add the repo to the config and use it for the origin check

Depends on: Task 7, Task 9, Task 15

In `src/superclaude/cli/issue_watch/cycle.py` add an optional `repo` key to `_TOP_KEYS` (line 58, which Task 9 also edits), to `Config` (line 97) and to `load_config` (line 195); when absent it defaults to `IronbellyOrg/IronClaude` so a hand-written config such as `/home/coder/.config/superclaude/issue-watch.json` stays valid. Pass `cfg.repo` from the cycle to every `github.*` call of Task 15. In `src/superclaude/cli/issue_watch/launch.py` change `check_origin` (line 233) and its use (`ORIGIN_REPO` line 50, compared at line 249; called from `cycle.py` `_origin_ok` line 670 and the launch step) to compare against the configured repo, case-insensitively as today. In `src/superclaude/cli/issue_pipeline/cli.py` make `stage-status --repo` optional (Task 15 made it required): when absent it takes the `repo` key of the chosen `--config` (which defaults to `IronbellyOrg/IronClaude` when the key is absent), and when both are given and differ the verb refuses with `refused:repo-mismatch`.

Acceptance criteria:
- `tests/issue_watch/test_cycle.py` runs a cycle for a config with `repo` set to another name and shows every `gh` call carries it and the origin check uses it; a worktree whose origin names a different repo ends with `origin_mismatch`.
- `tests/issue_watch/test_origin_parity.py` and `tests/issue_watch/test_launch.py` are updated and pass.
- A config without `repo` behaves as before (existing tests pass unchanged).
- `tests/issue_pipeline/test_stage_status.py` shows `stage-status --config <config with repo Other/Repo>` without `--repo` reads `Other/Repo`, with the hand-written config (no `repo` key) reads `IronbellyOrg/IronClaude`, and `--repo` naming a different repo than the config's is refused with `refused:repo-mismatch` before any call.
- `uv run pytest tests/issue_watch -q` passes.

## Phase 6: Generate each repo's configuration

## Task 17: Read the central defaults file

Create `src/superclaude/cli/issue_watch/defaults.py`. It reads `issue-watch-defaults.json` from a config directory passed in (default `~/.config/superclaude`; the file the Coder template saves, requirement R1) and returns the fixed approver logins, the two label names, the allowed repo owners and an optional map from `owner/name` to a Project node id. When the file is absent it returns built-in values: approver logins `ironbelly` and `clayphi`, labels `issue-watch:trigger` and `issue-watch:approved`, allowed owner `IronbellyOrg`, an empty map. Unknown keys, a wrong type or a bad login are rejected with the existing `ConfigError` style (`cycle.py` line 81). The module is pure: it reads one file and runs no command.

Acceptance criteria:
- New `tests/issue_watch/test_defaults.py` covers: file absent, a valid file, an unknown key, a bad login such as `-x`, and a map entry whose id does not match `PVT_`; every path is under `tmp_path`.
- `tests/issue_watch/test_module_boundaries.py` passes with the new module.

## Task 18: List and filter the Orca repos

Create `src/superclaude/cli/issue_watch/repos.py` with a function that runs `orca repo list` through the `Runner` of `src/superclaude/cli/issue_watch/runner.py` and returns one record per usable repo: Orca id, name, local path, and `owner/name` read from the path's git `origin`. A failed or timed-out `orca repo list`, or output that cannot be read, raises an error (requirement R15), never an empty list. Skip, and report with a reason, a repo whose path is under `/tmp`, whose origin is not on github.com, or whose origin owner is not in the allowed owners of Task 17. Parse the real format: one line per repo, `<id>  <name>  <path>` (checked on 2026-11-18).

Depends on: Task 17

Acceptance criteria:
- New `tests/issue_watch/test_repos.py` uses the fake runner and covers: six repos with one in `/tmp` skipped, a non-GitHub origin skipped, a foreign owner skipped, a failed list raising, a timed-out list raising, an empty but successful list returning no repos.
- The module uses no shell and passes `tests/issue_watch/test_no_shell.py` and `test_module_boundaries.py`.

## Task 19: Generate one repo's configuration, approvers file and state directory

Create `src/superclaude/cli/issue_watch/generate.py` with `ensure_config(repo_record, defaults, runner, base)` where `base` holds the config directory and the state directory (defaults `~/.config/superclaude` and `~/.local/state/superclaude`). For a repo that has no file at `<config dir>/issue-watch.d/<name>.json` it: reads the account id with `gh api user` (requirement R2); finds the Project with the GraphQL query `repository(owner, name){ projectsV2(first:10){ nodes{ id number title } } }` (R3): zero Projects gives a skip with reason `no_project`, several use the id from the defaults map or give the skip reason `project_ambiguous`; reads maintainers with `gh api "repos/<owner>/<name>/collaborators?permission=maintain"` and adds them to the fixed approvers' account ids (R4; fixed logins are turned into ids with `gh api users/<login>`); writes `<config dir>/issue-watch.d/<name>-approvers.txt` (mode 600, one id per line) and the config JSON (mode 600) with absolute `worktree` (`/home/coder/workspaces/worktrees/<name>/Coordinator`), `approvers_file`, an explicit absolute `state_dir` of `<state dir>/issue-watch/<name>` (R12), the `repo`, the Project id, the account id and `enabled: false`. The generator never writes the launch account's own id into a generated approvers file (the warn-only exclusion of Task 9 stays the owner's choice for a hand-written one). The result is validated with `cycle.load_config` and `cycle.validate_approvers` before it is kept; a file that exists is never overwritten.

Depends on: Task 9, Task 12, Task 16, Task 17, Task 18

Acceptance criteria:
- New `tests/issue_watch/test_generate.py` covers: a repo with one Project, none, several with and without a defaults entry, a failed account read, maintainers added, the launch account id never written to the approvers file, an existing config left untouched, file modes 600, and two repos getting two different `state_dir` values; every path is under `tmp_path` and the test asserts nothing was written under the real home.
- A generated config passes `cycle.load_config` in the test, and `uv run pytest tests/issue_watch -q` passes.
- The module issues only read calls to GitHub (`gh api user`, `gh api users/<login>`, the Project query, the collaborators call), each REST call with `--method GET`, and its argv builders are covered by the scan Task 12 extends.

## Task 20: Create the two labels on a repo when missing

Create `src/superclaude/cli/issue_watch/repo_init.py` with a function that lists the repo's labels (`gh label list --repo <owner/name>`) and creates `issue-watch:trigger` and `issue-watch:approved` with `gh label create --repo <owner/name>` when absent (requirement R11). It is idempotent and reports `created`, `present` or `failed` per label. The label names come from Task 17. Only the per-repo first run (Task 21) calls the creating function; the loop of Tasks 23 and 24 only reports a missing label (R14). This module is one of the two allowed GitHub writers named in Constraints; the coordinator-only guard class of Task 13 applies to launched agents, not to this cron-run module.

Depends on: Task 12, Task 17

Acceptance criteria:
- New `tests/issue_watch/test_repo_init.py` covers: both labels missing, one present, both present (no create call), a failed create.
- `tests/issue_watch/test_security_invariants.py` still passes with `repo_init.py` named as an allowed writer (Task 12 documents the scope).
- The label names are read from the defaults of Task 17, not written as literals in the module.

## Task 21: Run the first-run check and enable a repo

Create `src/superclaude/cli/issue_watch/first_run.py` (requirements R7, R18 and R28). For a freshly generated config it runs, in order: config validation (`check-config` logic), label creation through Task 20, `init-state`, one dry-run cycle (`once --dry-run` logic), the lock test (a second run while the lock is held ends with exit 75, using the store lock of `src/superclaude/cli/issue_watch/record.py`) and the restart test (the state document reloads and a second dry run changes nothing). All pass: it rewrites the config with `enabled: true`. Any fails: the config stays `enabled: false` and a one-line reason is written to `<state dir>/issue-watch/<name>/first-run.txt`. The report it writes also states the ship gate (`GOVERNED_LEVELS_ALLOWED`, Task 8: closed means only Pipeline None launches) and prints `approver_is_launch_account` when the approvers file holds the launch account (Task 9). It is idempotent: a repo whose state already exists is not re-initialised and a repo already enabled is left alone. It takes the same injectable base directories as Task 19. The live-test record of the runbook stays an owner check and is not part of this task.

Depends on: Task 8, Task 9, Task 19, Task 20

Acceptance criteria:
- New `tests/issue_watch/test_first_run.py` covers: all pass gives `enabled: true`; a worktree that does not exist gives `enabled: false` with `worktree_invalid` in the report; a dry-run failure keeps it false; a held lock is detected by the lock test; a state document that does not reload fails the restart test; a second run changes nothing; the report shows the closed gate state and the launch-account warning.
- No real `gh`, Orca or network call is made in the tests, and nothing is written under the real home.

## Phase 7: The dispatcher loop

## Task 22: Print the launched and attempted issue from `once`

Depends on: Task 7, Task 16

In `src/superclaude/cli/issue_watch/cli.py` `once_command` (line 118) currently prints `cycle: <reason>` and `exit: <code>`, and prints `would_launch` only in a dry run. Also print `launched: <issue number>` when the cycle launched an issue (`CycleResult.launched_issue`, `cycle.py` line 455) and `attempted: <issue number>` when a launch ended with an unknown outcome (requirement R26). Today `cycle.py` lines 1106 to 1109 return `launch_unknown` without setting `launched_issue`; add an `attempted_issue` field to `CycleResult`, set there. Print each line only once, and only the number, so the dispatcher can read it from a child's output.

Acceptance criteria:
- `tests/issue_watch/test_cli.py` shows `launched: 12` appears after a confirmed launch, `attempted: 12` appears after an unknown outcome and neither appears otherwise; the existing outputs are unchanged.
- `tests/issue_watch/test_cycle.py` shows `attempted_issue` is set for `launch_unknown` and for no other result.
- `tests/issue_watch/test_no_text.py` still passes (each line contains a number only).

## Task 23: Write the dispatcher core

Create `src/superclaude/cli/issue_watch/dispatch.py` with the loop of requirements R5, R15, R16, R26 and R32. It lists repos (Task 18), calls `ensure_config` and `first_run` (Tasks 19 and 21) for any repo without a config, then starts `superclaude issue-watch once --config <file>` as a child process per repo, one after another. Rules: total loop cap 270 seconds; each child is killed after 255 seconds, longer than the cycle's own 240 second deadline (`DEADLINE_TOTAL_S`, `cycle.py` line 41); repos not reached are skipped and reported; the repo order rotates each sweep (the next start index is kept in a small file under the state directory); the loop stops starting children after the first child whose output has a `launched:` or an `attempted:` line; a child killed or timed out counts as a launch attempt and stops the loop too, unless the repo's `dispatch.json` store (read through `record.py`, read-only) shows no pending or launched entry created during this sweep; `DAY_CAP` stays per repo. Use the `Runner` interface so tests use fakes, pass absolute paths because cron has no PATH, and take the injectable base directories of Task 19.

Depends on: Task 18, Task 19, Task 21, Task 22

Acceptance criteria:
- New `tests/issue_watch/test_dispatch.py` covers: rotation across three sweeps, a stop after the first `launched:` line, a stop after an `attempted:` line, a child killed after 255 seconds with a pending store entry stopping the loop, the same kill with no pending entry letting later repos run, the 270 second cap with unreached repos reported, a repo with no config being generated first, and a failed `orca repo list` giving an error result rather than a clean one.
- A child timeout never kills the loop, and each child's exit code and reason are kept for Task 25.

## Task 24: Add the loop-level account rate wait and the pre-child checks

Extend `src/superclaude/cli/issue_watch/dispatch.py`. Rate wait (requirement R5): when a child's cycle reason is plain `rate_limited` (not the 3600 second clamp reason, `github.py` `rate_limit_wait` line 418), the loop writes one file `<state dir>/issue-watch/account-rate-wait.json` holding the child's `next_permitted_at` and starts no further child until that time; children never write each other's stores. Pre-child checks (R14), each reported rather than silent: the repo's `Coordinator` worktree exists, is a git checkout and its `origin` names the repo; both labels exist (a read-only `gh label list`; a missing label is reported and the repo is skipped, never created by the loop); the Project count is exactly one (Task 19 rule). A failing check skips that repo and records the reason.

Depends on: Task 20, Task 23

Acceptance criteria:
- `tests/issue_watch/test_dispatch.py` adds cases: a `rate_limited` child stops later children until the stored time and a restart of the loop honours the file; a `rate_limit_clamped` child does not write it; a missing `Coordinator` worktree, a wrong origin and missing labels each give a distinct skip reason and no label is created; an expired wait file is ignored.
- All reasons used are written in the audit reason vocabulary (`src/superclaude/cli/issue_watch/audit.py` `REASON_TABLE`, line 26) or a new documented table in `dispatch.py`.

## Task 25: Add the `run-all` command

Depends on: Task 24

In `src/superclaude/cli/issue_watch/cli.py` add a `run-all` command to `issue_watch_group` (decorator at line 94, definition at line 95) that runs the dispatcher of Tasks 23 and 24 and prints one line per repo (repo, result, reason) and an overall line. Exit codes follow the existing set (`_EXIT_*`, lines 34 to 38): 0 for a clean sweep, 2 for a configuration problem in the loop itself, 75 when another sweep holds the loop lock. A second sweep started while one runs exits 75 through a lock file in the state directory (`flock`-style, like `record.py` line 382). It takes a `--dry-run` flag that lists repos and decisions but takes no lock, writes no config, no rotation file and no label and starts no child.

Acceptance criteria:
- `tests/issue_watch/test_cli.py` covers `run-all` output for a clean sweep, a skipped repo, a held lock (exit 75) and `--dry-run` (no lock taken and nothing written; assert a snapshot of the temp directory, lock file included, is unchanged).
- `uv run superclaude issue-watch run-all --help` exits 0 and `uv run superclaude issue-watch --help` lists `run-all`.
- `uv run pytest tests/issue_watch -q` passes.

## Phase 8: Documentation, the Coder handoff and the requirements record

## Task 26: Document the dispatcher, the launch levels, the ship gate and the completion update

Update `docs/designs/issue-watcher.md` and `docs/designs/issue-watcher-setup.md` for: the `run-all` loop and its caps, the config folder `~/.config/superclaude/issue-watch.d/`, the defaults file, the generator and first-run check (lock test and restart test included), the label creation module as one of two allowed writers beside `complete.py`, the `repo` config key, the per-status commands, the Pipeline field and its four levels (pointing to `docs/designs/issue-watcher-status-pipelines.md`), the approval-void rule and the Task 4 observation, the coordinator-only completion update to `In review` and the per-run marker, the `Coordinator` worktree path, and a new section replacing the hand setup steps of the runbook (sections 2 to 5) with the automatic path while keeping the manual commands as a fallback. Also document: who flips the ship gate (a reviewed commit that also un-skips the launch-level observations), each new reason word and warning (`level_gated`, `approver_is_launch_account`, `status_moved_by_person` and the `refused:` words of `complete`) with one plain sentence, the guard refusals of Task 13 and the version bump, and a rollback line for each of the findings of the remediation proposal.

Depends on: Task 2, Task 6, Task 8, Task 10, Task 11, Task 14, Task 25

Acceptance criteria:
- Both files mention `run-all`, `issue-watch.d`, `Coordinator`, `Pipeline`, `In review`, `level_gated` and the allowed statuses, checked with `grep -c`.
- `uv run pytest tests/docs -q` passes.

## Task 27: Write the Coder handoff document

Create `docs/designs/issue-watcher-zero-setup-coder-handoff.md` for the Coder template maintainers (requirements R1, R6, R9, R10, R17, R20, R21; Coder issues 515 and 516). It contains: the exact crontab line to install, built from verified values (`*/5 * * * *`, an explicit `PATH`, `flock -n` on a lock under `~/.aidev/`, full path `/usr/local/bin/superclaude issue-watch run-all`, output appended to `~/.aidev/logs/issue-watch.log`), with the tool locations checked on 2026-11-18 (`/home/coder/.config/orca/linux-orca-cli-shim/orca`, `/home/coder/.local/bin/gh`, `/usr/local/bin/superclaude`, `/usr/local/bin/uv`); the content of the central defaults file of Task 17 for the template to save; the `Coordinator` branch and worktree rules (switch to the remote branch when it exists, create it otherwise, path `/home/coder/workspaces/worktrees/<repo>/Coordinator`, origin equal to the repo); the session name `COORD-<RepoName>` and the standing launch-prompt text that gives the coordinator the issue-pipeline duties, including the coordinator-only completion update and the Full Submit push rule; the credential row (launched agents and workers should hold a token with no issues or projects write, or the watcher a dedicated launch login, because the guard is text-only and the launch account is also an approver); the hosts must run `superclaude install --force` once for the guard version 2; and the open Orca question that `orca worktree create --branch` suffixes a taken name, recorded as open with the reproduction step (R20 is a Coder row and is not verified here). Before writing the cron line, run `env -i HOME=$HOME PATH=/usr/bin:/bin /home/coder/.local/bin/gh auth status` and record whether `gh` stays logged in under cron's environment, and record the result in the file.

Depends on: Task 11, Task 14, Task 25

Acceptance criteria:
- The file lists each of R1, R6, R9, R10, R17, R20 and R21 with the Coder issue number where one exists and the value or text the template must use, or for R20 that it is open with its reproduction step.
- It records the result of the `gh auth status` check under a cron-like environment, whichever way it came out, and states the credential row and the guard version 2 install step.
- The cron line in the file contains an absolute `PATH`, `flock -n`, the log path and `run-all`.

## Task 28: Record the built and tested results in the requirements file

Update `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`: set each row that Tasks 1 to 27 implemented to `built` with the date and the test evidence (the test files and the passing count from the last full run of `uv run pytest tests/issue_watch tests/issue_pipeline tests/hooks tests/skills tests/commands tests/docs -q`), add a row to "Built and tested" for each task, move any decision still open (R20, R21, the ship-gate flip, the Task 4 outcome and the self-approval enforcement choice) under "Open decisions", and state which rows stay with the Coder repository. Record the owner's answers of 2026-11-19 (R33) as decided.

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 11, Task 12, Task 13, Task 14, Task 15, Task 16, Task 17, Task 18, Task 19, Task 20, Task 21, Task 22, Task 23, Task 24, Task 25, Task 26, Task 27

Acceptance criteria:
- Every row R1 to R34 has a status of `built`, `decided (Coder repo)` or `open`, and none is left as an earlier `decided (not built)` or `open` when its task is done.
- The "Built and tested" table has an entry per task with a test file name and a count.
- `make verify-sync` is clean.
