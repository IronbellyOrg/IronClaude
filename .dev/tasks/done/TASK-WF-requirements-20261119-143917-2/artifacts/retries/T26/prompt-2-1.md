3bec86c711133bc1ab9ef87baff51060baa91332
Review one task for spec compliance.

Task brief: ## Task 26: Document the dispatcher, the launch levels, the ship gate and the completion update

Update `docs/designs/issue-watcher.md` and `docs/designs/issue-watcher-setup.md` for: the `run-all` loop and its caps, the config folder `~/.config/superclaude/issue-watch.d/`, the defaults file, the generator and first-run check (lock test and restart test included), the label creation module as one of two allowed writers beside `complete.py`, the `Approved` issue field as the approval (R35: who may set it, the field-event read, the pseudo label `issue-field:Approved`, the one-second event id limit), the `repo` config key, the per-status commands, the Pipeline field and its four levels (pointing to `docs/designs/issue-watcher-status-pipelines.md`), the approval-void rule and the Task 4 observation, the coordinator-only completion update to `In review` and the per-run marker, the `Coordinator` worktree path, and a new section replacing the hand setup steps of the runbook (sections 2 to 5) with the automatic path while keeping the manual commands as a fallback. Also document: who flips the ship gate (a reviewed commit that also un-skips the launch-level observations), each new reason word and warning (`level_gated`, `approver_is_launch_account`, `status_moved_by_person` and the `refused:` words of `complete`) with one plain sentence, the guard refusals of Task 13 and the version bump, and a rollback line for each of the findings of the remediation proposal.

Depends on: Task 2, Task 6, Task 8, Task 10, Task 11, Task 14, Task 25

Acceptance criteria:
- T26.AC1: Both files mention `run-all`, `issue-watch.d`, `Coordinator`, `Pipeline`, `In review`, `level_gated` and the allowed statuses, checked with `grep -c`.
- T26.AC2: `uv run pytest tests/docs -q` passes.
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
Start sha: 3bec86c711133bc1ab9ef87baff51060baa91332
Diff against the start snapshot: diff --git a/docs/designs/issue-watcher-setup.md b/docs/designs/issue-watcher-setup.md
index 94c333998..beeea9703 100644
--- a/docs/designs/issue-watcher-setup.md
+++ b/docs/designs/issue-watcher-setup.md
@@ -704,3 +704,17 @@ Every item below is run by the owner; nothing in the implementation runs any of
 - Verify the [staleness alert (section 8.4)](#84-the-staleness-alert).
 - Only then [set `enabled` to `true` (section 8.6)](#86-set-enabled).
 - Install the [cron entry (section 8.7)](#87-install-the-cron-entry-fu-2).
+
+## 17. The automatic path (replaces the hand steps of sections 2 to 5)
+
+On a host with the Coder template, nothing in sections 2 to 5 is done by hand. The cron entry runs `superclaude issue-watch run-all` (see `docs/designs/issue-watcher-zero-setup-coder-handoff.md` for the line). For every repository Orca knows, the loop does this:
+
+1. Finds or creates the config `~/.config/superclaude/issue-watch.d/<name>.json` and its approvers file from the defaults file `~/.config/superclaude/issue-watch-defaults.json` (the Project and approvers are read from GitHub).
+2. Runs the first-run check (config, trigger label, state, dry run, lock test, restart test). The trigger label is created here and nowhere else. A passing check sets `enabled` to `true`; a failing one leaves it `false` and the reason is in `<state dir>/first-run.txt`.
+3. Before each child it checks the repository's `Coordinator` worktree (path `/home/coder/workspaces/worktrees/<repo>/Coordinator`, `origin` equal to the repository), the trigger label, the `Approved` field and the Project (the repository has one Project, or several with the defaults map naming the configured one; otherwise the reasons are `no_project`, `project_ambiguous` or `project_mismatch`). A repository that fails is skipped with a reason and nothing is created.
+
+To approve an issue, a person in the approvers file sets the issue field `Approved` to `Yes` (not a label) after the owner has set the Status (Research, Spec, Plan or Debug) and the Pipeline. While the ship gate is closed only Pipeline None launches; other levels end with `level_gated`. The coordinator moves the Status to `In review` when a run succeeds. A coordinator must be running for each repository (session `COORD-<RepoName>`).
+
+Check a host without changing anything: `superclaude issue-watch run-all --dry-run`. A real sweep (without `--dry-run`) exits 75 when another sweep is running; a dry run takes no lock and never does.
+
+The manual commands of sections 2 to 5 remain valid as a fallback: write the config and approvers file by hand, run `superclaude issue-watch check-config` and `init-state`, and create the label with `gh label create`. A hand-written config is left alone by the generator.
diff --git a/docs/designs/issue-watcher.md b/docs/designs/issue-watcher.md
index bbed0123b..99803d576 100644
--- a/docs/designs/issue-watcher.md
+++ b/docs/designs/issue-watcher.md
@@ -940,3 +940,65 @@ All criteria run under `uv run pytest tests/issue_watch/` with fakes or PATH stu
 | NFR-012 | 11, 13 |
 | NFR-013 | 10.3 |
 | NFR-014 | 5.1 to 5.4 |
+
+## 19. Zero-setup additions (plan `TASK-WF-requirements-20261119-143917-2`)
+
+This section records what the zero-setup work added. The per-status commands, the launch levels and the end Status are decided in `docs/designs/issue-watcher-status-pipelines.md`; the first-time setup of a host is in section 17 of `docs/designs/issue-watcher-setup.md`.
+
+### 19.1 The `run-all` loop and its caps
+
+`superclaude issue-watch run-all` (module `dispatch.py`) runs one sweep over every Orca repository and starts one `once` child per enabled repository. Caps: the whole sweep stops starting children after about 270 seconds (`LOOP_CAP_S`), one child is killed after 255 seconds (`CHILD_TIMEOUT_S`, longer than the 240 second cycle deadline), and the sweep stops after the first child that reports `launched:` or `attempted:`, so one sweep starts at most one agent. The start repository rotates between sweeps (file `<state dir>/issue-watch/rotation.json`). A second sweep exits 75 through the lock file `<state dir>/issue-watch/run-all.lock`. When a child ends with the plain reason `rate_limited` the loop writes `<state dir>/issue-watch/account-rate-wait.json` and starts no child until that time; the clamped reason `rate_limit_clamped` writes nothing. `--dry-run` lists each repository and its decision, takes no lock and writes no config, rotation file or label. Exit codes: 0 clean, 1 a child failed or the repository list could not be read, 2 a configuration problem of the loop itself, 75 another sweep holds the lock.
+
+### 19.2 Configuration folder, defaults file, generator and first run
+
+Each repository has its own file `~/.config/superclaude/issue-watch.d/<name>.json` and its own approvers file beside it. The central defaults file `~/.config/superclaude/issue-watch-defaults.json` (module `defaults.py`; built-in values apply when it is absent) holds the approver logins, the trigger label, the `Approved` field name and option, the allowed owner and a map of repository to Project id. The generator (`generate.py`) writes a missing config from reads only (launch account, the one Project, approvers), mode 600, with `enabled: false`; a file that exists is never overwritten. The first-run check (`first_run.py`) enables the config only after six steps pass in order: config, label, state, dry run, lock test (a second cycle ends 75 while the lock is held) and restart test (the state reloads and `dispatch.json` is unchanged). Its report is `<state dir>/first-run.txt`. The config has a `repo` key (strict `owner/name`); every GitHub read and the coordinator's `stage-status --repo` use it, so a repository other than IronClaude is read as itself.
+
+### 19.3 Writers
+
+Only two modules may write to GitHub: `issue_pipeline/complete.py` (the completion update) and `issue_watch/repo_init.py` (creating the trigger label once per repository, from the first run only; the loop itself never creates a label). `tests/issue_watch/test_security_invariants.py` scans for any other writer.
+
+### 19.4 The `Approved` issue field is the approval (R35)
+
+The approval is the organization issue field `Approved` set to `Yes`, not a label. The watcher reads the issue's field-change events, turns each into a label-style event with the pseudo label `issue-field:Approved`, and runs the existing approval logic on it. Only a person in the approvers file counts. The event id is the event time in whole epoch seconds, so two approval events on one issue within one second share an id. The old label `issue-watch:approved` is no longer read.
+
+### 19.5 Approval-void rule and the Task 4 observation
+
+As built (R31), an approval is void when the Status or the Pipeline value changed after it; the refusal word is the existing `edited_after_approval`. Task 4's observation of the field value times is in the plan's artifacts (`t4-updatedat-observation.md`). Owner decision R36 of 2026-11-20 withdraws R31: the amendment `.dev/releases/backlog/issue-watcher-zero-setup/amendment-r36-withdraw-r31.md` removes `value_changed_after` and its tests in a separate pass after this plan finishes. Until that pass runs, the code still voids the approval; after it, only the existing edit rule (`unchanged_since`) and the closed ship gate hold back a Pipeline raised after approval.
+
+### 19.6 The `Coordinator` worktree, completion update and ship gate
+
+Each repository has a worktree `/home/coder/workspaces/worktrees/<repo>/Coordinator` on branch `Coordinator`; the sweep checks that it exists, is a git checkout and that `origin` names the repository, and skips the repository with `worktree_invalid`, `worktree_not_git` or `origin_mismatch` otherwise. The coordinator (not the worker, not the watcher) moves the Project Status to `In review` when a run ends `succeeded`, with `issue-pipeline complete` (`complete.py`), compare-and-set from Research, Spec, Plan or Debug on the configured item. It posts one result comment carrying a per-run marker keyed on the approval event id, so a retry never posts twice. Only the allowed Statuses (Research, Spec, Plan, Debug) act.
+
+The ship gate is the constant `GOVERNED_LEVELS_ALLOWED = False` in `launch.py`. While it is `False` only Pipeline None launches and any other level ends with the skip reason `level_gated`. It is flipped by one reviewed commit that also un-skips the launch-level observations in `tests/hooks/test_launch_level_observations.py`; a coupling test enforces the pairing. No config key or environment variable is the switch.
+
+### 19.7 New reason words and warnings
+
+| Word | Meaning |
+|---|---|
+| `level_gated` | The issue's Pipeline asks for a level above None while the ship gate is closed; nothing launched. |
+| `warning: approver_is_launch_account` | The approvers file lists the account the watcher launches with, so that account could approve its own issue; printed by `check-config` and in `first-run.txt`; a warning only. |
+| `status_moved_by_person` | `complete` found the Status already moved by someone else, left it alone and only commented. |
+| `refused:bad_outcome`, `bad_issue`, `bad_project_id`, `bad_repo`, `bad_run`, `bad_summary` | `complete` was given an invalid argument and wrote nothing. |
+| `refused:project_missing`, `project_ambiguous`, `status_option_missing` | The Project, or its `In review` option, could not be found exactly once; nothing was changed. |
+| `failed:*` | A GitHub call of `complete` failed; run it again. |
+
+Loop skip reasons (`SKIP_REASONS` in `dispatch.py`) include `config_invalid`, `not_enabled`, `worktree_invalid`, `origin_mismatch`, `label_missing`, `approved_field_missing` and the Project reasons; each repository that is skipped is printed with its word.
+
+### 19.8 Guard refusals and version 2
+
+The launch-level guard (`src/superclaude/hooks/scripts/launch-level-guard.sh`, mirrored in `plugins/superclaude/hooks/scripts/`) now refuses every `gh issue` verb except view, list and status, and every `gh label` and `gh project` write, at every level including Full Submit (`project item-list` and `project field-list` are allowed). `issue-pipeline complete` is coordinator-only. The token `*.config/superclaude*` guards the watcher's own configuration. The guard's version stamp is 2, so each host runs `superclaude install --force` once.
+
+### 19.9 Rollback of each remediation finding
+
+Each line says how to undo it; none is needed unless the finding's change misbehaves.
+
+- Q-1 (writes by Full Submit agents): revert the guard and its mirror to stamp 1; Full Submit agents can then write to issues again.
+- Q-2 (ship gate): nothing to roll back; flipping the constant is the opening step, and reverting that commit closes the gate again.
+- Q-3 (the value-time rule): R36 withdraws it; see 19.5. The fallback the proposal names is a level-specific approval label.
+- Q-4 (reread order): restore the earlier order in `_revalidate`; two reasons may then be reported for one reread.
+- Q-5 (Status move on the wrong item): remove the compare-and-set in `complete.py`; the move then trusts the first item.
+- Q-6 (per-run marker): revert to the shared marker; a second run's comment would then be suppressed.
+- Q-7 (acceptance of the prompt task): move a `tests/issue_watch` file that pins `--pipeline none` back to the later task; that task's acceptance then fails until the file is updated.
+- Q-8 (variable types in the GraphQL query): restore the literal repository in the query and the old assertion in `test_security_invariants.py`; the repo parameter then stops working.
+- Q-9 (which sessions the guard governs): remove the unbound-session guard test and its wording; the guard itself does not change.
+- Q-10 (ordering and dependency edges): wording and plan ordering only; revert the lines.

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 3bec86c711133bc1ab9ef87baff51060baa91332
# Task 26 review 1

Earlier blocking findings: none given (first review).

## ACs
- T26.AC1 met. T26.AC1@docs/designs/issue-watcher-setup.md:710 and docs/designs/issue-watcher.md:63. `grep -c` gives at least 1 per term in both files: run-all 2/2, issue-watch.d 1/3, Coordinator 2/1, Pipeline 5/2, In review 3/2, level_gated 2/1. The four allowed Statuses (Research, Spec, Plan, Debug) appear in both files.
- T26.AC2 met. T26.AC2@tests/docs: `uv run pytest tests/docs -q` gave 11 passed.

## Claims checked against live source and found true
- Caps and constants: `LOOP_CAP_S` 270, `CHILD_TIMEOUT_S` 255 (dispatch.py:52-53).
- Rotation, wait and lock files under `<state dir>/issue-watch/` (dispatch.py:154-160, 177, 235).
- The clamped reason writes nothing (dispatch.py:441-446).
- Exit codes 0, 1, 2 and 75 (cli.py:36-40, 513-514).
- First-run steps and their order, the `first-run.txt` report and `approver_is_launch_account` (first_run.py:1-20, 190).
- Coordinator path (generate.py:252) and `GOVERNED_LEVELS_ALLOWED = False` (launch.py:48), with `level_gated` raised at cycle.py:1043.
- `complete` reason words (complete.py:75-88) and the ALLOWED_STATUSES move to In review (complete.py:54-59).
- Guard stamp 2 (launch-level-guard.sh:10), the `*.config/superclaude*` token (:777), the `item-list` and `field-list` allowances (:664), and the source/plugin mirror (identical).
- The R36 amendment file and the `t4-updatedat-observation.md` artifact exist.
- The Q-1 to Q-10 rollback lines match the remediation proposal.

## Findings
F1.1 ac=scope at=docs/designs/issue-watcher-setup.md:718 anchor=src/superclaude/cli/issue_watch/cli.py:507-509 chk=amiss:n,false:y,harm:n,constraint:n family=dryrun-lock fix=Delete "Exit 75 means another sweep is running" from the dry-run sentence, or say that only a real sweep (without --dry-run) exits 75. : The doc says `run-all --dry-run` can exit 75. In cli.py a dry run runs `run_sweep` without `loop_lock`, so it never takes the lock and never exits 75. Section 19.1 of issue-watcher.md states this correctly ("takes no lock"), so the two docs contradict each other.

F1.2 ac=scope at=docs/designs/issue-watcher-setup.md:714 anchor=src/superclaude/cli/issue_watch/dispatch.py:302 chk=amiss:n,false:y,harm:n,constraint:n family=project-check fix=Say that the configured Project must be one of the repository's Projects, and that with several Projects the defaults map must name the configured one (reasons no_project, project_mismatch, project_ambiguous). : The doc says the sweep checks "that there is exactly one Project". The code allows several Projects when `defaults.projects[repo]` equals the configured Project id (`if len(ids) > 1 and defaults.projects.get(config.repo) != config.project_id` gives `project_ambiguous`). The check also fails with `project_mismatch`.

F1.3 ac=scope at=docs/designs/issue-watcher-setup.md:710 anchor=docs/designs/issue-watcher-zero-setup-coder-handoff.md (file does not exist) chk=amiss:n,false:n,harm:n,constraint:n family=dangling-ref fix=Keep, since Task 27 creates the handoff file, or say "Task 27 hands over the line". : Advisory only. The text points to a file that is not in the tree yet; a reader following it now gets nothing. This is a forward reference to Task 27 and not a task 26 failure.

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
