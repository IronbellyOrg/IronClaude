e38a1b428f1fcc1a534cd75826ff4b0878ff692a
Review one task for spec compliance.

Task brief: ## Task 8: Add the closed ship gate

Depends on: Task 7

Add `GOVERNED_LEVELS_ALLOWED = False` to `src/superclaude/cli/issue_watch/launch.py`. In `_examine` (`cycle.py` line 915), before `_launch` is reached (`_launch` is at line 1026 and sets `c.launching` at line 1028, and its dry run returns at lines 1029 to 1035, so the check must sit before it to keep `would_launch` honest), raise `_Skip("level_gated")` for any Pipeline other than None while the constant is False. Add one row `"level_gated": ("skip", 0)` to `REASON_TABLE` in `src/superclaude/cli/issue_watch/audit.py` (line 26, next to the rows at lines 71 to 80). No config key or environment variable is the switch: the config directory is not tamper-protected, so such a switch would be as writable as the approvers file. Add a coupling test in `tests/hooks/test_launch_level_observations.py` beside `_PENDING` (line 79): when the constant is True, none of `OB-H1 item 1`, `OB-H1 item 5`, `OB-H2` and `OB-H3` appears in `_PENDING`, so the gate opens only in the commit that un-skips the observations. Record in the design note that `refs/claim.md` line 133 (an observation of item 1 before any governed claim) and `docs/designs/sc-issue-launch-level-hook.md` line 201 (item 1 only for `full` and `--submit`) disagree, that one boolean follows the stricter text, and that a per-level split stays an owner option.

Acceptance criteria:
- T8.AC1: `tests/issue_watch/test_cycle.py` shows an issue at Worktree, Full and Full Submit ends `level_gated` with no launch call and no store write, an issue at None launches, and a dry run shows no `would_launch` for a gated level.
- T8.AC2: `tests/issue_watch/test_audit.py` (or the test that counts `REASON_TABLE` rows) is updated for the new row and passes.
- T8.AC3: The coupling test passes with the constant False and would fail if the constant were True with the four observations still in `_PENDING`.
- T8.AC4: `uv run pytest tests/issue_watch tests/hooks -q` passes.
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
Start sha: e38a1b428f1fcc1a534cd75826ff4b0878ff692a
Diff against the start snapshot: diff --git a/docs/designs/issue-watcher-status-pipelines.md b/docs/designs/issue-watcher-status-pipelines.md
deleted file mode 100644
index d3a332ef9..000000000
--- a/docs/designs/issue-watcher-status-pipelines.md
+++ /dev/null
@@ -1,104 +0,0 @@
-# Issue watcher: per-status commands, launch levels and completion
-
-**Status:** design note, decided 2026-11-19 (Task 6 of the zero-setup plan `TASK-WF-requirements-20261119-143917-2`). It records the owner's decisions of 2026-11-18 and 2026-11-19 (requirements R23, R24, R25, R29, R31, R32, R33, R34 and R35) and fixes every interface that Tasks 7 to 14 implement. Where a line of code or text is named, it was read on 2026-11-19.
-
-Terms: the **Status** is the Project 2 single-select field `Status`; the **Pipeline** is its single-select field `Pipeline` (`None`, `Worktree`, `Full`, `Full Submit`); the **stage** is the word the watcher derives from the Status (`research`, `spec`, `plan`, `debug`); the **level** is the launch level derived from the Pipeline (`none`, `worktree`, `full`, `full submit`). The **approval** is the issue field `Approved` set to `Yes` (R35, `docs/designs/issue-watcher.md`).
-
-## 1. What acts and what does not (R22, Task 1)
-
-Only an issue whose one live Project item has Status `Research`, `Spec`, `Plan` or `Debug` acts (`predicates.ALLOWED_STATUSES`). `Backlog`, `Ready`, `In progress`, `In review`, `Done`, an empty Status and any status added to the board later never act. **Ready triggers nothing**: no command, no launch.
-
-The Pipeline picks the level: `None` or empty is level `none`, `Worktree` is `worktree`, `Full` is `full`, `Full Submit` is `full submit`. Until the ship gate of Task 8 is opened by a reviewed commit, only level `none` launches; every other level ends `level_gated`.
-
-## 2. The decision table
-
-All four Status pipelines end at **`In review`** (owner, 2026-11-19; held in one named table in `complete.py`, Task 12). Only a `succeeded` outcome moves the Status.
-
-| Status | Command at the stage | Runs as the coordinator's worker? (level `none`) | Level `none` | Level `worktree` | Level `full` | Level `full submit` | End Status |
-|---|---|---|---|---|---|---|---|
-| Research | `/sc:research` | Yes: `src/superclaude/commands/research.md:117` has `## Unattended mode` | worker runs it unattended and reports | agent runs it, writes the report in the issue's worktree, halts, no commit | as `worktree` plus one local commit of the report on the issue branch | as `full` plus push of that branch to `origin` and `/sc:pr-submit --monitor 3` | In review |
-| Spec | `/sc:design` when the issue is well defined, else `/sc:brainstorm` with a handoff to `/sc:design` for high complexity or scope | Yes: `design.md:117` and `brainstorm.md:148` | as above | as above | as above | as above | In review |
-| Plan | `/sc:workflow` | Yes: `workflow.md:80` | as above; stops before `/sc:implement` and `/task` | as above | as above | as above | In review |
-| Debug | `/sc:troubleshoot` | Yes: `troubleshoot.md:169` | worker runs it **without `--fix`** | agent runs it **without `--fix`** (propose next steps, halt) | agent runs it **with `--fix`** (a remediation tasklist package, never an applied code change) | as `full` plus push and PR | In review |
-| Ready | none | not applicable | nothing | nothing | nothing | nothing | unchanged |
-
-None of the five commands is on the never-as-worker list (`src/superclaude/core/WORKER-CONTRACT.md:23`: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:sweep`, `/sc:swarm-wizard`, and `/sc:pr-submit` while decision D3 holds). Each has an `## Unattended mode` section at the line shown, so no alternative is needed. `/sc:pr-submit` is never a worker command: at level `full submit` the launched agent runs it in its own top-level session, as D3 allows.
-
-**Debug at level `none`.** The coordinator's worker runs `/sc:troubleshoot` without `--fix`, because a level `none` worker stops before any code change; code-affecting remediation starts only at `full` and `full submit`. The worker brief is used only at level `none`; at the other levels the launched agent runs the command from its launch prompt, so the brief has no level slot.
-
-**What `--fix` does.** `src/superclaude/commands/troubleshoot.md:54`: `--fix` offers the Tier 3 remediation chain (`/sc:workflow` produces a tasklist package; the user runs `/sc:implement`); code changes never auto-apply. At `full` the agent therefore leaves a remediation package, not a code change.
-
-## 3. The launch prompt (decision 1)
-
-The watcher sends one of these prompts to `orca agent launch --prompt`. The stage is derived from the Status read by `_revalidate`; the level from the Pipeline.
-
-| Level | Prompt for stage `research` (the others replace the last word) |
-|---|---|
-| none | `/sc:issue --claim <N> --pipeline none --stage research` |
-| worktree | `/sc:issue --claim <N> --pipeline worktree --stage research` |
-| full | `/sc:issue --claim <N> --pipeline full --stage research` |
-| full submit | `/sc:issue --claim <N> --pipeline full --submit --stage research` |
-
-Stages: `research`, `spec`, `plan`, `debug`. `--stage` is a new claim-only option of `/sc:issue` (Task 10); `--submit` stays valid only after `--pipeline full`. The launch-level guard has no prompt allow-list, so the pin is the pattern in `launch.py`, which replaces `PROMPT_PATTERN` (line 33):
-
-```
-^/sc:issue --claim [1-9][0-9]{0,8} --pipeline (?:none|worktree|full(?: --submit)?) --stage (?:research|spec|plan|debug)$
-```
-
-`build_claim_prompt` (line 84) takes the issue number, the stage and the level and raises `ValueError` for any input that does not match, so no other text reaches `--prompt`. `launch_argv` (line 95) and `retry_argv` (line 119) keep refusing a prompt that does not fullmatch the pattern. The prompt is built from the item that `_revalidate` rereads (Task 7), so a Status or Pipeline moved between examine and launch cannot launch the old command.
-
-## 4. Which session runs the Status command (decision 3)
-
-- **Level `none`.** The watcher's claim session assigns the issue, posts its two marked comments and writes `.dev/issues/<N>/issue-summary.md` and `next-steps.md`; it creates no worktree and starts no agent. The coordinator then reads the claim's stage, creates the worktree and starts one worker from the worker brief, whose `Command:` line carries the stage's command (section 7).
-- **Levels `worktree`, `full`, `full submit`.** `/sc:issue --claim` creates the worktree and launches an agent in it. The stage command enters the agent's `launch-prompt.md` (written by the claim from `templates/next-steps.md`, Task 10): its first step is the stage command in the form of the table above, its last step is writing `.dev/issues/<N>/result.md`, and it states that only the coordinator writes to an issue, a label or a Project (section 8). The agent runs the command from that prompt.
-
-## 5. How the Status and Pipeline reach the coordinator (decision 4)
-
-A `--pipeline none` claim writes no worktree record. The watcher stores the stage and the level in the claim's `.dev/issues/<N>/next-steps.md` header lines (`stage: <word>` and `level: <word>`) next to the existing summary, and the coordinator reads them there, in the checkout that ran the claim, with the `claimed` entry of `dispatch.json` read-only. The coordinator never trusts a Status it remembers: it rereads the Project item through `stage-status` at each gate, which also reads the approval and the plan reply.
-
-## 6. "Well defined" for Spec (decision 5)
-
-The claim worker that writes `issue-summary.md` judges it, from the Complexity issue field and the summary text: `Simple` or `Medium` with a stated acceptance criterion is well defined (`/sc:design`); anything else, or `Complex`, is not (`/sc:brainstorm`, with a handoff to `/sc:design` for high complexity or scope). It records the verdict and the reason in one line of `issue-summary.md` (`spec-route: design|brainstorm — <reason>`). No code judges it and no issue text reaches the brief.
-
-## 7. The worker brief (levels `none` only)
-
-`src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` and `brief.py` carry one row per allowed Status instead of one row per complexity. The brief's `Command:` line is the command of the Status (the table), built from a closed template; the issue number is a validated integer and the Status a closed set, so no issue text reaches the brief. The brief states that after the coordinator mirrors the Status or moves it to `In review`, the Project values have changed, so any relaunch needs a fresh approval (section 9). `brief.py` keeps the closed-set checks and refuses a bad Status, issue number or nonce with a closed reason. The Debug row at `none` has no `--fix`.
-
-## 8. The approval record (decision 6, R19, R29, R35)
-
-"Automatic approval record" of R19 means the **claim-time approval already kept in `dispatch.json`** (`approver_id`, `approval_event_id`, `approved_at`, now taken from the `Approved` field event) plus the **adoption row** (`adopt-create`). It is not the plan-hash approval row. The plan-hash row (`approval_record.py`, `record_create`) is created only from a worker's `ask` that carries the plan hash (WC-17, R29). A claim-time event is refused as plan approval in `src/superclaude/cli/issue_pipeline/stage_predicates.py` (rule `label-before-plan`, lines 161 to 170, through `stage-status`), because `approval_record.record_create` cannot tell the two events apart and is not changed. The coordinator calls `record-create` only with evidence that `stage-status` reports as accepted. Task 11 tests this where it is enforced, in `tests/issue_pipeline/test_stage_predicates.py` and `test_stage_status.py`.
-
-## 9. The completion update (R24, decision 7)
-
-Only the coordinator writes to an issue, a label or a Project item, and only under that issue's grant row (`WORKER-CONTRACT.md` lines 241 to 243 and 300). An agent launched at any level and every worker reports through its result file and never runs `issue-pipeline complete`.
-
-- **How the coordinator learns a run finished.** At level `none`: the worker's `worker_done` contract. At the other levels: the result file `.dev/issues/<N>/result.md` in the issue's worktree, noticed by the `/sc:sweep` report the coordinator already reads at each wake (WC-16).
-- **Closed format of `result.md`.** Four lines, no free text: `outcome: succeeded|failed|blocked|partial`, `artifacts: <repo-relative paths, comma separated, may be empty>`, `pull_request: <number or none>`, `run: <approval event id>`. The coordinator reads only these four keys; nothing else of the file is posted.
-- **The result comment.** One comment per run, carrying the per-run marker `<!-- sc:issue:result issue=<N> run=<approval_event_id> -->` and the outcome word, the artifact paths and the pull request number. The marker never contains the claim marker. The approval event id keys it because each relaunch needs a fresh approval, so a second run has a different id; a marker already written by the coordinator's own login for the same run suppresses a second comment (idempotency).
-- **Only `succeeded` moves the Status**, with a compare-and-set: the Status moves only from `Research`, `Spec`, `Plan` or `Debug`; any other current Status (for example a person moved it to `Done`) posts the comment and returns `status_moved_by_person` without a move. A `failed`, `blocked` or `partial` outcome posts the comment only. The end Status comes from one table keyed by the allowed Status (all four `In review`), so an exception is a one-line change. The read then write is not atomic; the module says so.
-- **Effect on the approval.** The coordinator's own comment never voids an approval (comments by the watcher's own login are skipped, `predicates.py` `unchanged_since`). Its move to `In review` changes the Status value time, so it voids the approval by design (R31): a retry or relaunch needs a fresh `Approved` set after the last Project change, and `In review` fails `project_check`, so the owner moves the Status back first. The same holds for the coordinator's mirror of the Status at line 298 of the duties.
-
-## 10. The Full Submit push rule (decision 8)
-
-`WORKER-CONTRACT.md` line 245 gets this sentence in place of the current one: "At Full Submit the launched agent pushes only its own feature branch to origin and opens the pull request through /sc:pr-submit; the owner's Pipeline value plus an approval later than the last Project change is the go for that issue only. The coordinator never pushes worker commits on that basis; for every other push the rule above stands." Task 11 applies it and tests that no coordinator push grant is tied to the Pipeline.
-
-## 11. Which sessions the guard governs (decision 10)
-
-Governed means a session with a record in the launch-level store: the agents launched at `worktree`, `full` and `full submit`, and bound workers. Not governed: the watcher-launched `--pipeline none` claim session and the coordinator. The claim session's two marked comments are allowed by design; it reads untrusted issue text under the launch login. The counted marker login is the **workspace's single `gh` login**, shared by the watcher, the coordinator and launched agents; the guard (Task 13) is a text check on `gh` commands and cannot tell them apart by login, so the complete control is a token without issues or projects write for launched agents (a Coder row, Task 27).
-
-## 12. Files that change in Tasks 7 to 14 (by path)
-
-| Task | Files |
-|---|---|
-| 7 | `src/superclaude/cli/issue_watch/launch.py`, `src/superclaude/cli/issue_watch/cycle.py`, `src/superclaude/cli/issue_watch/predicates.py`, and the seven test files `tests/issue_watch/test_cli.py`, `test_cli_e2e.py`, `test_crash_injection.py`, `test_cycle.py`, `test_launch.py`, `test_no_text.py`, `test_security_invariants.py` |
-| 8 | `src/superclaude/cli/issue_watch/launch.py`, `cycle.py`, `audit.py`, `tests/hooks/test_launch_level_observations.py`, `tests/issue_watch/test_cycle.py`, `test_audit.py` |
-| 9 | `src/superclaude/cli/issue_watch/predicates.py`, `cycle.py`, `cli.py`, tests under `tests/issue_watch/` |
-| 10 | `src/superclaude/commands/issue.md`, `src/superclaude/skills/sc-issue-protocol/SKILL.md`, `refs/claim.md`, `templates/next-steps.md`, `tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py`, and the docs that quote the old prompt |
-| 11 | `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt`, `brief.py`, `tests/skills/test_worker_contract.py`, `tests/issue_pipeline/test_brief.py`, `test_stage_predicates.py`, `test_stage_status.py` |
-| 12 | `src/superclaude/cli/issue_pipeline/complete.py` (new), `tests/issue_pipeline/test_complete.py` (new), `tests/issue_watch/test_security_invariants.py` |
-| 13 | `src/superclaude/hooks/scripts/launch-level-guard.sh`, `plugins/superclaude/hooks/scripts/launch-level-guard.sh`, `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, the guard and issue-worktree tests |
-| 14 | `src/superclaude/cli/issue_pipeline/cli.py`, `src/superclaude/core/WORKER-CONTRACT.md`, `tests/issue_pipeline/test_complete_cli.py` (new), `tests/skills/test_worker_contract.py` |
-
-## 13. Ship-gate note (Task 8)
-
-`docs/designs/sc-issue-launch-level-hook.md` line 201 limits observation item 1 to `full` and `--submit`, while `refs/claim.md` line 133 asks for an observation of item 1 before any governed claim. One boolean, `GOVERNED_LEVELS_ALLOWED`, follows the stricter text (no governed level launches until the observations pass). A per-level split stays an owner option.
diff --git a/src/superclaude/cli/issue_watch/audit.py b/src/superclaude/cli/issue_watch/audit.py
index de4c3670b..ba239267d 100644
--- a/src/superclaude/cli/issue_watch/audit.py
+++ b/src/superclaude/cli/issue_watch/audit.py
@@ -80,6 +80,8 @@ REASON_TABLE: dict[str, tuple[str, int]] = {
     "revalidation_failed": ("skip", 0),
     "marker_unreadable": ("skip", 0),
     "edits_unreadable": ("skip", 0),
+    # The ship gate (R33): a Pipeline other than None while the gate is closed.
+    "level_gated": ("skip", 0),
     # Entry reasons.
     "prompt_invalid": ("entry", 7),
     "revalidation_transient": ("entry", 7),
diff --git a/src/superclaude/cli/issue_watch/cycle.py b/src/superclaude/cli/issue_watch/cycle.py
index 354b640ee..0848ab435 100644
--- a/src/superclaude/cli/issue_watch/cycle.py
+++ b/src/superclaude/cli/issue_watch/cycle.py
@@ -993,6 +993,14 @@ class _Cycle:
         if why is not None:
             raise _Skip(why)
         c.item = predicates.live_item(items, cfg.project_id)  # type: ignore[arg-type]
+        # The ship gate (R33) sits before _launch, so a dry run's would_launch is
+        # honest and a gated level touches no store and no probe.
+        if (
+            not launch.GOVERNED_LEVELS_ALLOWED
+            and c.item is not None
+            and c.item.pipeline_name not in (None, "None")
+        ):
+            raise _Skip("level_gated")
         return self._launch(c, approval)
 
     # -- step 12: the launch steps ---------------------------------------------
diff --git a/src/superclaude/cli/issue_watch/launch.py b/src/superclaude/cli/issue_watch/launch.py
index d3471a7b5..07d57f6ec 100644
--- a/src/superclaude/cli/issue_watch/launch.py
+++ b/src/superclaude/cli/issue_watch/launch.py
@@ -45,6 +45,13 @@ STAGE_OF_STATUS = {
 }
 """The stage word the claim runs for each allowed Project Status (R23)."""
 
+GOVERNED_LEVELS_ALLOWED = False
+"""The ship gate (R33): while False only Pipeline None launches and every other
+level ends ``level_gated``. No config key or environment variable is the switch,
+because the config directory is not tamper-protected. Flipped only by a reviewed
+commit that also un-skips the launch-level observations of
+``tests/hooks/test_launch_level_observations.py`` (a coupling test enforces it)."""
+
 PIPELINE_ARGS = {
     None: "none",
     "None": "none",
diff --git a/tests/hooks/test_launch_level_observations.py b/tests/hooks/test_launch_level_observations.py
index 5077c5eb4..ab60b6ed7 100644
--- a/tests/hooks/test_launch_level_observations.py
+++ b/tests/hooks/test_launch_level_observations.py
@@ -79,6 +79,32 @@ def test_probe_with_unwritable_log_path_exits_zero_silently(tmp_path):
 _PENDING = [f"OB-H1 item {n}" for n in range(1, 10)] + ["OB-H2", "OB-H3", "OB-CTX"]
 
 
+_GATE_ITEMS = ("OB-H1 item 1", "OB-H1 item 5", "OB-H2", "OB-H3")
+
+
+def _gate_may_be_open(gate: bool, pending: list[str]) -> bool:
+    """R33: the watcher's ship gate may be True only when no gate item is pending."""
+    return not gate or not any(item in pending for item in _GATE_ITEMS)
+
+
+def test_the_ship_gate_coupling_rule_itself__r33():
+    assert _gate_may_be_open(False, _PENDING)  # closed gate: always fine
+    assert not _gate_may_be_open(True, _PENDING)  # open gate, observations pending
+    assert not _gate_may_be_open(True, ["OB-H2"])  # any one of the four blocks it
+    assert _gate_may_be_open(True, ["OB-H1 item 2", "OB-CTX"])  # none of the four
+
+
+def test_the_ship_gate_opens_only_when_its_observations_are_run__r33():
+    """A commit that flips ``launch.GOVERNED_LEVELS_ALLOWED`` while OB-H1 items 1 and
+    5, OB-H2 or OB-H3 are still pending (skipped here) fails this test, so the gate
+    opens in the commit that runs the observations."""
+    from superclaude.cli.issue_watch import launch
+
+    assert _gate_may_be_open(launch.GOVERNED_LEVELS_ALLOWED, _PENDING), (
+        "GOVERNED_LEVELS_ALLOWED is True while its observations are still pending"
+    )
+
+
 @pytest.mark.parametrize("item", _PENDING)
 def test_pending_live_observation(item):
     pytest.skip(f"{item}: needs a real governed session and has not been run")
diff --git a/tests/issue_watch/test_audit.py b/tests/issue_watch/test_audit.py
index 68de37bdf..30852485c 100644
--- a/tests/issue_watch/test_audit.py
+++ b/tests/issue_watch/test_audit.py
@@ -1,6 +1,6 @@
 """Tests for the audit log: reason table pin, line builders, writer, rotation.
 
-The 59 reason names and the (kind, exit) table below are literal copies of the
+The 60 reason names and the (kind, exit) table below are literal copies of the
 closed reason table (spec lines 330-358 plus the five proposals DF-02, DF-03,
 DF-22 and DF-57, and the two Gate C proposals ``cycle_complete`` (exit 0) and
 ``cycle_crashed`` (exit 1), fix findings C-2 and C-3). They are never imported
@@ -35,7 +35,7 @@ from .conftest import FakeClock
 MIB = 1024 * 1024
 ROTATE_AT = 5 * MIB
 
-# The 59 reason names, in the order of the reason table.
+# The 60 reason names, in the order of the reason table.
 EXPECTED_NAMES = [
     "config_invalid",
     "approvers_invalid",
@@ -81,6 +81,7 @@ EXPECTED_NAMES = [
     "revalidation_failed",
     "marker_unreadable",
     "edits_unreadable",
+    "level_gated",
     "prompt_invalid",
     "revalidation_transient",
     "attempts_exhausted",
@@ -144,6 +145,7 @@ EXPECTED_TABLE = {
     "revalidation_failed": ("skip", 0),
     "marker_unreadable": ("skip", 0),
     "edits_unreadable": ("skip", 0),
+    "level_gated": ("skip", 0),
     "prompt_invalid": ("entry", 7),
     "revalidation_transient": ("entry", 7),
     "attempts_exhausted": ("entry", 0),
@@ -211,12 +213,12 @@ def names_in(directory) -> list[str]:
 # ---------------------------------------------------------------- reason table
 
 
-def test_reasons_pin_59_names__ac14_fr020_nfr006():
-    assert len(EXPECTED_NAMES) == 59
-    assert len(set(EXPECTED_NAMES)) == 59
+def test_reasons_pin_60_names__ac14_fr020_nfr006():
+    assert len(EXPECTED_NAMES) == 60
+    assert len(set(EXPECTED_NAMES)) == 60
     assert isinstance(REASONS, frozenset)
     assert REASONS == frozenset(EXPECTED_NAMES)
-    assert len(REASON_TABLE) == 59
+    assert len(REASON_TABLE) == 60
     assert list(REASON_TABLE) == EXPECTED_NAMES
 
 
diff --git a/tests/issue_watch/test_cycle.py b/tests/issue_watch/test_cycle.py
index 560991d41..fef113db5 100644
--- a/tests/issue_watch/test_cycle.py
+++ b/tests/issue_watch/test_cycle.py
@@ -2850,6 +2850,45 @@ def test_the_prompt_sent_names_the_stage_of_the_issues_status__r23(
     ]
 
 
+@pytest.mark.parametrize("pipeline", ["Worktree", "Full", "Full Submit"])
+def test_a_governed_level_ends_level_gated_with_no_launch_and_no_store_write__r33(
+    tmp_path, tmp_state, gh_world, pipeline
+):
+    """The ship gate is closed: nothing but Pipeline None launches."""
+    assert cycle.launch.GOVERNED_LEVELS_ALLOWED is False
+    world = gh_world()
+    world.issue(9, items=[{"pipeline": pipeline}])
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert (res.exit_code, res.reason) == (0, "cycle_complete")
+    assert _decisions(_lines_of(tmp_state, res)) == [(9, "level_gated")]
+    assert deps.launcher.calls == []
+    assert not _probed(world)
+    assert tmp_state.load().entries == {}  # a skip writes no entry
+    assert not (tmp_state.state_dir / cycle.PROMPTS_FILE).exists()
+
+
+@pytest.mark.parametrize("pipeline", [None, "None"])
+def test_pipeline_none_still_launches_while_the_gate_is_closed__r33(
+    tmp_path, tmp_state, gh_world, pipeline
+):
+    world = gh_world()
+    world.issue(9, items=[{"pipeline": pipeline}])
+    res, deps = _run(tmp_path, tmp_state, world)
+    assert _decisions(_lines_of(tmp_state, res)) == [(9, "launched")]
+    assert len(deps.launcher.calls) == 1
+
+
+def test_a_dry_run_reports_no_would_launch_for_a_gated_level__r33(
+    tmp_path, tmp_state, gh_world
+):
+    world = gh_world()
+    world.issue(9, items=[{"pipeline": "Full Submit"}])
+    res, deps = _run(tmp_path, tmp_state, world, dry_run=True)
+    assert res.would_launch is None
+    assert _decisions(_lines_of(tmp_state, res)) == [(9, "level_gated")]
+    assert deps.launcher.calls == []
+
+
 def test_a_launch_keeps_its_prompt_for_the_status_retry_command__r23(
     tmp_path, tmp_state, gh_world
 ):
@@ -2881,9 +2920,10 @@ def test_a_launch_keeps_its_prompt_for_the_status_retry_command__r23(
     ],
 )
 def test_a_status_or_pipeline_moved_between_examine_and_launch_fails__r27(
-    tmp_path, tmp_state, gh_world, examined, reread
+    tmp_path, tmp_state, gh_world, examined, reread, monkeypatch
 ):
     """Every value time stays before the approval, so only the comparison refuses."""
+    monkeypatch.setattr(cycle.launch, "GOVERNED_LEVELS_ALLOWED", True)  # gate open
     world = gh_world()
     world.issue(9, items=examined)
     _on_nth(world, "items", 9, 2, lambda: world.update(9, items=reread))
@@ -2894,9 +2934,10 @@ def test_a_status_or_pipeline_moved_between_examine_and_launch_fails__r27(
 
 
 def test_a_pipeline_lowered_with_a_time_after_the_approval_is_edited__r27_r31(
-    tmp_path, tmp_state, gh_world
+    tmp_path, tmp_state, gh_world, monkeypatch
 ):
     """The overlap case: the value-time rule wins over the comparison."""
+    monkeypatch.setattr(cycle.launch, "GOVERNED_LEVELS_ALLOWED", True)  # gate open
     world = gh_world()
     world.issue(9, items=[{"pipeline": "Full Submit"}])
     lowered = [
diff --git a/docs/designs/issue-watcher-status-pipelines.md b/docs/designs/issue-watcher-status-pipelines.md
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


Codegraph context
index_state: fresh
checked_at: 2026-11-19T15:32:25Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff (Grep, read): REASON_TABLE is read by audit.py itself and by tests/issue_watch/test_cycle.py (exit and kind per reason); the new row level_gated is ("skip", 0) so exit codes are unchanged. The refs/claim.md line 133 versus sc-issue-launch-level-hook.md line 201 disagreement is already recorded in docs/designs/issue-watcher-status-pipelines.md section 13 (written in Task 6, which Task 8 builds on); this diff does not touch that file. Three Task 7 tests that start from a Full Submit item now set launch.GOVERNED_LEVELS_ALLOWED True with monkeypatch, because a closed gate would end them at level_gated before the revalidation they test. tests/issue_watch, tests/issue_pipeline and the observations test: 3017 passed, 12 skipped.

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
