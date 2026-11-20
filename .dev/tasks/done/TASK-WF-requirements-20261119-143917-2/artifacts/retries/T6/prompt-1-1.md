f15f76d6ed25bbe2074944a9da2a4b106350000c
Review one task for spec compliance.

Task brief: ## Task 6: Write the design note for per-status commands, launch levels and completion

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
- T6.AC1: The file exists and has a table with one row per Status (Research, Spec, Plan, Debug, Ready) giving the command, the prompt text for each of the four Pipeline values, the end Status per level, and whether it can run as a worker with the file and line that shows it.
- T6.AC2: Every decision listed above has a stated decision; a command that cannot run as a worker has a stated alternative, not a blank.
- T6.AC3: The note says which files change in Tasks 7 to 14 by path.
Global constraints: ## Constraints

- Scope is the IronClaude repository only. The Coder template work (requirements R1, R6, R9, R10, R17, R20, R21; Coder issues 515 and 516) is not implemented here; Task 27 hands it over with exact values.
- This plan applies requirement R33, which adopts the remediation proposal `.dev/remediation/watcher-plan-v3/remediation-proposal.md` with the owner's answers of 2026-11-19: the ship gate stays closed, the `updatedAt` observation is run, self-approval is warn-only, `~/.config/superclaude` joins the guard's tamper tokens, all four pipelines end at In review, and the extra guard refusals are confirmed. It also applies requirement R34, the five blocking corrections of the fourth review (P4-1 to P4-5): the coordinator's approval read names its repo (Tasks 15 and 16), an empty Pipeline has no time to compare (Tasks 3 and 5), the claim-time approval refusal is tested where it is enforced (Task 11), the guard pattern for `issue-pipeline complete` is anchored on the verb word (Task 13), and the worker brief is tested at level `none` only (Tasks 6, 10 and 11).
- This plan applies requirement R35 (owner decision of 2026-11-19): the approval is no longer the label `issue-watch:approved`. It is the organization issue field `Approved` (single select, one option `Yes`, field id 50144115 on `IronbellyOrg`) set to `Yes` by an allowed approver (IronBelly, Clay or a maintainer, the approvers file of today). The trigger label `issue-watch:trigger` stays. Who set the field and when comes from the issue's GraphQL timeline events `IssueFieldAddedEvent`, `IssueFieldChangedEvent` and `IssueFieldRemovedEvent` (each carries `actor`, `createdAt`, `issueField` and the value; verified read-only on 2026-11-19 against issue 675 with another field), because the REST events endpoint names the event but not the field or the value. Task 4a builds the read; the approval predicates, the approval-void rule and the claim-time refusal keep their logic and see the field events as label events named by `approval_label`. A real label with the old name never approves. Task 4 is amended to observe the field instead of the label; the plan was copied from `TASK-WF-requirements-20261119-143917` (Tasks 1 to 3 complete there) and edited by owner instruction, and `source.md` still carries the label wording of the requirements file (Task 28 updates the requirements file).
- Edit `src/superclaude/`, then run `make sync-dev` and `make verify-sync`. Never edit or stage anything under `.claude/` (only `.claude/settings.json` is tracked). The tracked plugin mirror `plugins/superclaude/hooks/scripts/launch-level-guard.sh` is changed together with its source.
- Python only through UV (`uv run pytest`, `uv run ruff`). Tests use the faked `gh` and Orca runners already in `tests/issue_watch/conftest.py`; no task runs the watcher against the real GitHub or Orca, except the read-only schema check of Task 3 and the read-only reads of Task 4.
- `src/superclaude/cli/issue_watch/github.py` stays read-only: no mutation, no POST to a REST path (security invariant NG-2, `tests/issue_watch/test_security_invariants.py`). The only modules that write to GitHub are two new ones outside `github.py`: `src/superclaude/cli/issue_pipeline/complete.py` (Task 12: result comment and Status move, run only by the coordinator) and `src/superclaude/cli/issue_watch/repo_init.py` (Task 20: labels).
- Only the coordinator writes to an issue, a label or a Project item (owner decision of 2026-11-19; `src/superclaude/core/WORKER-CONTRACT.md` lines 241 to 243 and 300), and only under that issue's grant row. An agent launched at Worktree, Full or Full Submit, and every worker, never runs `issue-pipeline complete`, never posts an issue comment and never changes a label or a Project field; it reports through its result file `.dev/issues/<N>/result.md`. The launch-level guard refuses every `gh issue`, `gh label` and `gh project` write at every level, Full Submit included (Task 13), and every `gh api` write at every level. This is a text check on `gh` commands only: a script or another HTTP client is not seen. The complete control is a token with no issues or projects write for launched agents (a Coder row, owner decision). This is the one place the plan goes beyond issue verbs.
- Governed means a session with a record in the launch-level store: the agents launched at Worktree, Full and Full Submit, and bound workers. Not governed: the watcher-launched `--pipeline none` claim session and the coordinator. The claim session's two marked comments are allowed by design, and it reads untrusted issue text under the launch login.
- The approval (the `Approved` issue field set to Yes, R35), the allowed Project Status, the approval-void rule of Task 5 and the "edited after approval" refusal (`predicates.py`) stay the gate. Nothing in this plan removes or auto-satisfies them. The plan-hash approval row (`src/superclaude/cli/issue_pipeline/approval_record.py`) is created only from a worker's `ask` that carries the plan hash (`WORKER-CONTRACT.md`, WC-17), never from claim-time fields. Approval by the launch account is accepted unless the owner sets the exclusion key `approval_excluded_ids` (Task 9, warn-first).
- The cron watcher may launch every Pipeline level as a capability (owner, 2026-11-19), but the ship gate of Task 8 is closed: until a reviewed commit flips `GOVERNED_LEVELS_ALLOWED` and un-skips the launch-level observations (`tests/hooks/test_launch_level_observations.py`), only Pipeline None launches and every other level ends `level_gated`. Full Submit commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`; it never merges. For an issue the owner has put at Full Submit and approved with the `Approved` field after the last Project change, that setting is the person's go for that issue's push and pull request, and nothing else is pushed.
- `~/.config/superclaude` was not in the guard's tamper tokens (guard line 764); Task 13 adds it. Until that lands, the exclusion key and any future config key are as writable as the approvers file, so the exclusion limits an honest but injected session, not a hostile one.
- The term is "coordinator", never "orchestrator". The coordinator branch and worktree are both named `Coordinator`; the session is named `COORD-<RepoName>`.
- Tasks that edit the same file run in plan order, never in parallel: `cycle.py` (Tasks 4a, 5, 7, 8, 9, 16, 22), `launch.py` (Tasks 7, 8, 16), `github.py` (Tasks 3, 4a, 15), `predicates.py` (Tasks 1, 3, 5, 7, 9), `audit.py` (Task 8), `launch-level-guard.sh` (Task 13), `WORKER-CONTRACT.md` (Tasks 11, 14), `issue_pipeline/cli.py` (Tasks 14, 15, 16), `issue_pipeline/reads.py` (Task 15), `test_security_invariants.py` (Tasks 3, 4a, 7, 12, 15). Task 1 leaves `cycle.py` unchanged.
- Every new module that writes under the user's home takes an injectable base directory, and its tests run with every path inside `tmp_path` and assert nothing was written under the real home.
- Do not switch any real watcher on, claim a real issue, install a real cron entry, move a real issue's Status or start a worker for a real issue. Each generated config starts with `enabled: false` and only the automatic first-run check of Task 21 may turn it on.
Start sha: f15f76d6ed25bbe2074944a9da2a4b106350000c
Diff against the start snapshot: diff --git a/docs/designs/issue-watcher-status-pipelines.md b/docs/designs/issue-watcher-status-pipelines.md
new file mode 100644
index 000000000..d3a332ef9
--- /dev/null
+++ b/docs/designs/issue-watcher-status-pipelines.md
@@ -0,0 +1,104 @@
+# Issue watcher: per-status commands, launch levels and completion
+
+**Status:** design note, decided 2026-11-19 (Task 6 of the zero-setup plan `TASK-WF-requirements-20261119-143917-2`). It records the owner's decisions of 2026-11-18 and 2026-11-19 (requirements R23, R24, R25, R29, R31, R32, R33, R34 and R35) and fixes every interface that Tasks 7 to 14 implement. Where a line of code or text is named, it was read on 2026-11-19.
+
+Terms: the **Status** is the Project 2 single-select field `Status`; the **Pipeline** is its single-select field `Pipeline` (`None`, `Worktree`, `Full`, `Full Submit`); the **stage** is the word the watcher derives from the Status (`research`, `spec`, `plan`, `debug`); the **level** is the launch level derived from the Pipeline (`none`, `worktree`, `full`, `full submit`). The **approval** is the issue field `Approved` set to `Yes` (R35, `docs/designs/issue-watcher.md`).
+
+## 1. What acts and what does not (R22, Task 1)
+
+Only an issue whose one live Project item has Status `Research`, `Spec`, `Plan` or `Debug` acts (`predicates.ALLOWED_STATUSES`). `Backlog`, `Ready`, `In progress`, `In review`, `Done`, an empty Status and any status added to the board later never act. **Ready triggers nothing**: no command, no launch.
+
+The Pipeline picks the level: `None` or empty is level `none`, `Worktree` is `worktree`, `Full` is `full`, `Full Submit` is `full submit`. Until the ship gate of Task 8 is opened by a reviewed commit, only level `none` launches; every other level ends `level_gated`.
+
+## 2. The decision table
+
+All four Status pipelines end at **`In review`** (owner, 2026-11-19; held in one named table in `complete.py`, Task 12). Only a `succeeded` outcome moves the Status.
+
+| Status | Command at the stage | Runs as the coordinator's worker? (level `none`) | Level `none` | Level `worktree` | Level `full` | Level `full submit` | End Status |
+|---|---|---|---|---|---|---|---|
+| Research | `/sc:research` | Yes: `src/superclaude/commands/research.md:117` has `## Unattended mode` | worker runs it unattended and reports | agent runs it, writes the report in the issue's worktree, halts, no commit | as `worktree` plus one local commit of the report on the issue branch | as `full` plus push of that branch to `origin` and `/sc:pr-submit --monitor 3` | In review |
+| Spec | `/sc:design` when the issue is well defined, else `/sc:brainstorm` with a handoff to `/sc:design` for high complexity or scope | Yes: `design.md:117` and `brainstorm.md:148` | as above | as above | as above | as above | In review |
+| Plan | `/sc:workflow` | Yes: `workflow.md:80` | as above; stops before `/sc:implement` and `/task` | as above | as above | as above | In review |
+| Debug | `/sc:troubleshoot` | Yes: `troubleshoot.md:169` | worker runs it **without `--fix`** | agent runs it **without `--fix`** (propose next steps, halt) | agent runs it **with `--fix`** (a remediation tasklist package, never an applied code change) | as `full` plus push and PR | In review |
+| Ready | none | not applicable | nothing | nothing | nothing | nothing | unchanged |
+
+None of the five commands is on the never-as-worker list (`src/superclaude/core/WORKER-CONTRACT.md:23`: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:sweep`, `/sc:swarm-wizard`, and `/sc:pr-submit` while decision D3 holds). Each has an `## Unattended mode` section at the line shown, so no alternative is needed. `/sc:pr-submit` is never a worker command: at level `full submit` the launched agent runs it in its own top-level session, as D3 allows.
+
+**Debug at level `none`.** The coordinator's worker runs `/sc:troubleshoot` without `--fix`, because a level `none` worker stops before any code change; code-affecting remediation starts only at `full` and `full submit`. The worker brief is used only at level `none`; at the other levels the launched agent runs the command from its launch prompt, so the brief has no level slot.
+
+**What `--fix` does.** `src/superclaude/commands/troubleshoot.md:54`: `--fix` offers the Tier 3 remediation chain (`/sc:workflow` produces a tasklist package; the user runs `/sc:implement`); code changes never auto-apply. At `full` the agent therefore leaves a remediation package, not a code change.
+
+## 3. The launch prompt (decision 1)
+
+The watcher sends one of these prompts to `orca agent launch --prompt`. The stage is derived from the Status read by `_revalidate`; the level from the Pipeline.
+
+| Level | Prompt for stage `research` (the others replace the last word) |
+|---|---|
+| none | `/sc:issue --claim <N> --pipeline none --stage research` |
+| worktree | `/sc:issue --claim <N> --pipeline worktree --stage research` |
+| full | `/sc:issue --claim <N> --pipeline full --stage research` |
+| full submit | `/sc:issue --claim <N> --pipeline full --submit --stage research` |
+
+Stages: `research`, `spec`, `plan`, `debug`. `--stage` is a new claim-only option of `/sc:issue` (Task 10); `--submit` stays valid only after `--pipeline full`. The launch-level guard has no prompt allow-list, so the pin is the pattern in `launch.py`, which replaces `PROMPT_PATTERN` (line 33):
+
+```
+^/sc:issue --claim [1-9][0-9]{0,8} --pipeline (?:none|worktree|full(?: --submit)?) --stage (?:research|spec|plan|debug)$
+```
+
+`build_claim_prompt` (line 84) takes the issue number, the stage and the level and raises `ValueError` for any input that does not match, so no other text reaches `--prompt`. `launch_argv` (line 95) and `retry_argv` (line 119) keep refusing a prompt that does not fullmatch the pattern. The prompt is built from the item that `_revalidate` rereads (Task 7), so a Status or Pipeline moved between examine and launch cannot launch the old command.
+
+## 4. Which session runs the Status command (decision 3)
+
+- **Level `none`.** The watcher's claim session assigns the issue, posts its two marked comments and writes `.dev/issues/<N>/issue-summary.md` and `next-steps.md`; it creates no worktree and starts no agent. The coordinator then reads the claim's stage, creates the worktree and starts one worker from the worker brief, whose `Command:` line carries the stage's command (section 7).
+- **Levels `worktree`, `full`, `full submit`.** `/sc:issue --claim` creates the worktree and launches an agent in it. The stage command enters the agent's `launch-prompt.md` (written by the claim from `templates/next-steps.md`, Task 10): its first step is the stage command in the form of the table above, its last step is writing `.dev/issues/<N>/result.md`, and it states that only the coordinator writes to an issue, a label or a Project (section 8). The agent runs the command from that prompt.
+
+## 5. How the Status and Pipeline reach the coordinator (decision 4)
+
+A `--pipeline none` claim writes no worktree record. The watcher stores the stage and the level in the claim's `.dev/issues/<N>/next-steps.md` header lines (`stage: <word>` and `level: <word>`) next to the existing summary, and the coordinator reads them there, in the checkout that ran the claim, with the `claimed` entry of `dispatch.json` read-only. The coordinator never trusts a Status it remembers: it rereads the Project item through `stage-status` at each gate, which also reads the approval and the plan reply.
+
+## 6. "Well defined" for Spec (decision 5)
+
+The claim worker that writes `issue-summary.md` judges it, from the Complexity issue field and the summary text: `Simple` or `Medium` with a stated acceptance criterion is well defined (`/sc:design`); anything else, or `Complex`, is not (`/sc:brainstorm`, with a handoff to `/sc:design` for high complexity or scope). It records the verdict and the reason in one line of `issue-summary.md` (`spec-route: design|brainstorm — <reason>`). No code judges it and no issue text reaches the brief.
+
+## 7. The worker brief (levels `none` only)
+
+`src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` and `brief.py` carry one row per allowed Status instead of one row per complexity. The brief's `Command:` line is the command of the Status (the table), built from a closed template; the issue number is a validated integer and the Status a closed set, so no issue text reaches the brief. The brief states that after the coordinator mirrors the Status or moves it to `In review`, the Project values have changed, so any relaunch needs a fresh approval (section 9). `brief.py` keeps the closed-set checks and refuses a bad Status, issue number or nonce with a closed reason. The Debug row at `none` has no `--fix`.
+
+## 8. The approval record (decision 6, R19, R29, R35)
+
+"Automatic approval record" of R19 means the **claim-time approval already kept in `dispatch.json`** (`approver_id`, `approval_event_id`, `approved_at`, now taken from the `Approved` field event) plus the **adoption row** (`adopt-create`). It is not the plan-hash approval row. The plan-hash row (`approval_record.py`, `record_create`) is created only from a worker's `ask` that carries the plan hash (WC-17, R29). A claim-time event is refused as plan approval in `src/superclaude/cli/issue_pipeline/stage_predicates.py` (rule `label-before-plan`, lines 161 to 170, through `stage-status`), because `approval_record.record_create` cannot tell the two events apart and is not changed. The coordinator calls `record-create` only with evidence that `stage-status` reports as accepted. Task 11 tests this where it is enforced, in `tests/issue_pipeline/test_stage_predicates.py` and `test_stage_status.py`.
+
+## 9. The completion update (R24, decision 7)
+
+Only the coordinator writes to an issue, a label or a Project item, and only under that issue's grant row (`WORKER-CONTRACT.md` lines 241 to 243 and 300). An agent launched at any level and every worker reports through its result file and never runs `issue-pipeline complete`.
+
+- **How the coordinator learns a run finished.** At level `none`: the worker's `worker_done` contract. At the other levels: the result file `.dev/issues/<N>/result.md` in the issue's worktree, noticed by the `/sc:sweep` report the coordinator already reads at each wake (WC-16).
+- **Closed format of `result.md`.** Four lines, no free text: `outcome: succeeded|failed|blocked|partial`, `artifacts: <repo-relative paths, comma separated, may be empty>`, `pull_request: <number or none>`, `run: <approval event id>`. The coordinator reads only these four keys; nothing else of the file is posted.
+- **The result comment.** One comment per run, carrying the per-run marker `<!-- sc:issue:result issue=<N> run=<approval_event_id> -->` and the outcome word, the artifact paths and the pull request number. The marker never contains the claim marker. The approval event id keys it because each relaunch needs a fresh approval, so a second run has a different id; a marker already written by the coordinator's own login for the same run suppresses a second comment (idempotency).
+- **Only `succeeded` moves the Status**, with a compare-and-set: the Status moves only from `Research`, `Spec`, `Plan` or `Debug`; any other current Status (for example a person moved it to `Done`) posts the comment and returns `status_moved_by_person` without a move. A `failed`, `blocked` or `partial` outcome posts the comment only. The end Status comes from one table keyed by the allowed Status (all four `In review`), so an exception is a one-line change. The read then write is not atomic; the module says so.
+- **Effect on the approval.** The coordinator's own comment never voids an approval (comments by the watcher's own login are skipped, `predicates.py` `unchanged_since`). Its move to `In review` changes the Status value time, so it voids the approval by design (R31): a retry or relaunch needs a fresh `Approved` set after the last Project change, and `In review` fails `project_check`, so the owner moves the Status back first. The same holds for the coordinator's mirror of the Status at line 298 of the duties.
+
+## 10. The Full Submit push rule (decision 8)
+
+`WORKER-CONTRACT.md` line 245 gets this sentence in place of the current one: "At Full Submit the launched agent pushes only its own feature branch to origin and opens the pull request through /sc:pr-submit; the owner's Pipeline value plus an approval later than the last Project change is the go for that issue only. The coordinator never pushes worker commits on that basis; for every other push the rule above stands." Task 11 applies it and tests that no coordinator push grant is tied to the Pipeline.
+
+## 11. Which sessions the guard governs (decision 10)
+
+Governed means a session with a record in the launch-level store: the agents launched at `worktree`, `full` and `full submit`, and bound workers. Not governed: the watcher-launched `--pipeline none` claim session and the coordinator. The claim session's two marked comments are allowed by design; it reads untrusted issue text under the launch login. The counted marker login is the **workspace's single `gh` login**, shared by the watcher, the coordinator and launched agents; the guard (Task 13) is a text check on `gh` commands and cannot tell them apart by login, so the complete control is a token without issues or projects write for launched agents (a Coder row, Task 27).
+
+## 12. Files that change in Tasks 7 to 14 (by path)
+
+| Task | Files |
+|---|---|
+| 7 | `src/superclaude/cli/issue_watch/launch.py`, `src/superclaude/cli/issue_watch/cycle.py`, `src/superclaude/cli/issue_watch/predicates.py`, and the seven test files `tests/issue_watch/test_cli.py`, `test_cli_e2e.py`, `test_crash_injection.py`, `test_cycle.py`, `test_launch.py`, `test_no_text.py`, `test_security_invariants.py` |
+| 8 | `src/superclaude/cli/issue_watch/launch.py`, `cycle.py`, `audit.py`, `tests/hooks/test_launch_level_observations.py`, `tests/issue_watch/test_cycle.py`, `test_audit.py` |
+| 9 | `src/superclaude/cli/issue_watch/predicates.py`, `cycle.py`, `cli.py`, tests under `tests/issue_watch/` |
+| 10 | `src/superclaude/commands/issue.md`, `src/superclaude/skills/sc-issue-protocol/SKILL.md`, `refs/claim.md`, `templates/next-steps.md`, `tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py`, and the docs that quote the old prompt |
+| 11 | `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt`, `brief.py`, `tests/skills/test_worker_contract.py`, `tests/issue_pipeline/test_brief.py`, `test_stage_predicates.py`, `test_stage_status.py` |
+| 12 | `src/superclaude/cli/issue_pipeline/complete.py` (new), `tests/issue_pipeline/test_complete.py` (new), `tests/issue_watch/test_security_invariants.py` |
+| 13 | `src/superclaude/hooks/scripts/launch-level-guard.sh`, `plugins/superclaude/hooks/scripts/launch-level-guard.sh`, `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, the guard and issue-worktree tests |
+| 14 | `src/superclaude/cli/issue_pipeline/cli.py`, `src/superclaude/core/WORKER-CONTRACT.md`, `tests/issue_pipeline/test_complete_cli.py` (new), `tests/skills/test_worker_contract.py` |
+
+## 13. Ship-gate note (Task 8)
+
+`docs/designs/sc-issue-launch-level-hook.md` line 201 limits observation item 1 to `full` and `--submit`, while `refs/claim.md` line 133 asks for an observation of item 1 before any governed claim. One boolean, `GOVERNED_LEVELS_ALLOWED`, follows the stricter text (no governed level launches until the observations pass). A per-level split stays an owner option.

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
