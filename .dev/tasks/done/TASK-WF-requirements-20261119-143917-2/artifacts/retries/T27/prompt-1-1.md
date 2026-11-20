1975b2aeaac7696d1509db9f1c89771dff33d4e6
Review one task for spec compliance.

Task brief: ## Task 27: Write the Coder handoff document

Create `docs/designs/issue-watcher-zero-setup-coder-handoff.md` for the Coder template maintainers (requirements R1, R6, R9, R10, R17, R20, R21; Coder issues 515 and 516). It contains: the exact crontab line to install, built from verified values (`*/5 * * * *`, an explicit `PATH`, `flock -n` on a lock under `~/.aidev/`, full path `/usr/local/bin/superclaude issue-watch run-all`, output appended to `~/.aidev/logs/issue-watch.log`), with the tool locations checked on 2026-11-18 (`/home/coder/.config/orca/linux-orca-cli-shim/orca`, `/home/coder/.local/bin/gh`, `/usr/local/bin/superclaude`, `/usr/local/bin/uv`); the content of the central defaults file of Task 17 for the template to save; the `Coordinator` branch and worktree rules (switch to the remote branch when it exists, create it otherwise, path `/home/coder/workspaces/worktrees/<repo>/Coordinator`, origin equal to the repo); the session name `COORD-<RepoName>` and the standing launch-prompt text that gives the coordinator the issue-pipeline duties, including the coordinator-only completion update and the Full Submit push rule; the organization issue field `Approved` (single select, option `Yes`, visible to the organization members) that every workspace's approvers set, with the note that the template does not create it; the credential row (launched agents and workers should hold a token with no issues or projects write, or the watcher a dedicated launch login, because the guard is text-only and the launch account is also an approver); the hosts must run `superclaude install --force` once for the guard version 2; and the open Orca question that `orca worktree create --branch` suffixes a taken name, recorded as open with the reproduction step (R20 is a Coder row and is not verified here). Before writing the cron line, run `env -i HOME=$HOME PATH=/usr/bin:/bin /home/coder/.local/bin/gh auth status` and record whether `gh` stays logged in under cron's environment, and record the result in the file.

Depends on: Task 11, Task 14, Task 25

Acceptance criteria:
- T27.AC1: The file lists each of R1, R6, R9, R10, R17, R20 and R21 with the Coder issue number where one exists and the value or text the template must use, or for R20 that it is open with its reproduction step.
- T27.AC2: It records the result of the `gh auth status` check under a cron-like environment, whichever way it came out, and states the credential row and the guard version 2 install step.
- T27.AC3: The cron line in the file contains an absolute `PATH`, `flock -n`, the log path and `run-all`.
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
Start sha: 1975b2aeaac7696d1509db9f1c89771dff33d4e6
Diff against the start snapshot: diff --git a/docs/designs/issue-watcher-zero-setup-coder-handoff.md b/docs/designs/issue-watcher-zero-setup-coder-handoff.md
new file mode 100644
index 000000000..0ade16e16
--- /dev/null
+++ b/docs/designs/issue-watcher-zero-setup-coder-handoff.md
@@ -0,0 +1,65 @@
+# Issue watcher zero setup: handoff to the Coder template maintainers
+
+**Audience:** the maintainers of the Coder template (repository `IronbellyOrg/Coder`). **Source:** the zero-setup requirements of `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md` (rows R1, R6, R9, R10, R17, R20, R21) and Coder issues 515 (cron) and 516 (the coordinator). IronClaude builds the watcher side; the template must provide the rows below. Every value was read or run on 2026-11-18 or 2026-11-20 unless marked otherwise.
+
+## 1. What the template must provide
+
+| Row | Coder issue | What the template must do, with the value to use |
+|---|---|---|
+| R1 | none | Save the central defaults file of section 3 as `~/.config/superclaude/issue-watch-defaults.json` so no user writes one by hand. |
+| R6 | 515 (https://github.com/IronbellyOrg/Coder/issues/515) | Install `cron`, start the daemon from `startup.sh` at every boot, and make the crontab of section 2 exist exactly once at every boot. |
+| R9 | 516 (https://github.com/IronbellyOrg/Coder/issues/516) | For every project: a `Coordinator` branch, a `Coordinator` worktree and a running coordinator session, checked at boot and on every watcher run (section 4). |
+| R10 | 516 | The watcher's worktree is the `Coordinator` worktree, path `/home/coder/workspaces/worktrees/<repo>/Coordinator`, created by Orca with an agent; its `origin` must equal the repository it serves. |
+| R17 | 516 | Nothing manual. The session is named `COORD-<RepoName>` and starts from the standing prompt of section 5. |
+| R20 | none | Open, not verified here: `orca worktree create --branch` suffixes a taken branch name (`Coordinator-2`), so using an existing remote `Coordinator` branch needs a verified method. Reproduction: in a repository that has a remote branch named `Coordinator`, run `orca worktree create --name Coordinator --branch Coordinator --agent claude --prompt "<task>"` and read the branch name with `git -C <path> branch --show-current`; a result other than `Coordinator` reproduces it. IronClaude has no remote `Coordinator` branch (checked with `git ls-remote`), so it takes the create path and is not affected today. |
+| R21 | 515 | Cron's environment is only `PATH=/usr/bin:/bin` and no `~/.aienv`, so the entry sets `PATH` and uses full paths (section 2). |
+
+## 2. The crontab
+
+Tool locations checked on 2026-11-18 and found again on 2026-11-20: `/home/coder/.config/orca/linux-orca-cli-shim/orca`, `/home/coder/.local/bin/gh`, `/usr/local/bin/superclaude` (a link to `/opt/uv/tools/superclaude/bin/superclaude`), `/usr/local/bin/uv`, `/usr/bin/flock`. The folder `/home/coder/.aidev/logs` exists.
+
+```cron
+PATH=/home/coder/.local/bin:/usr/local/bin:/usr/bin:/bin
+*/5 * * * * /usr/bin/flock -n /home/coder/.aidev/issue-watch.lock /usr/local/bin/superclaude issue-watch run-all --orca /home/coder/.config/orca/linux-orca-cli-shim/orca >> /home/coder/.aidev/logs/issue-watch.log 2>&1
+```
+
+Notes: `flock -n` makes a second entry exit at once while a sweep runs (the loop has its own lock too and exits 75). `--orca` is explicit because the Orca shim is not on cron's `PATH`; `gh` is found through the `PATH` line. `superclaude issue-watch run-all` exists only in a build that contains the zero-setup work: the `/usr/local/bin/superclaude` on this machine on 2026-11-20 does not list `run-all` yet, so the template must install a build that has it.
+
+**`gh` login under cron's environment.** Run on 2026-11-20: `env -i HOME=$HOME PATH=/usr/bin:/bin /home/coder/.local/bin/gh auth status`. Result: `gh` stayed logged in (`Logged in to github.com account ironbelly`, token scopes `gist`, `project`, `read:org`, `repo`, `workflow`, exit 0). It reads the login from `$HOME/.config/gh/hosts.yml`, so the entry needs `HOME` (cron sets it) and no token variable. Orca listing under the same empty environment worked on 2026-11-18 (6 repositories).
+
+## 3. The central defaults file
+
+Content for the template to save at `~/.config/superclaude/issue-watch-defaults.json` (these equal the built-in values, so a missing file behaves the same; `projects` is optional and only needed for a repository with several Projects):
+
+```json
+{
+  "approver_logins": ["ironbelly", "clayphi"],
+  "trigger_label": "issue-watch:trigger",
+  "approval_field": "Approved",
+  "approval_option": "Yes",
+  "allowed_owners": ["IronbellyOrg"],
+  "projects": {}
+}
+```
+
+## 4. The `Coordinator` branch and worktree rules
+
+- When the repository has a `Coordinator` branch on the remote, switch to it; create it only when it does not exist (R20 above is the open question of how Orca does this).
+- The worktree path is `/home/coder/workspaces/worktrees/<repo>/Coordinator`; its `origin` must name the repository (the sweep refuses a repository whose `origin` differs, reason `origin_mismatch`).
+- The worktree is created through Orca with an agent. Check all three (branch, worktree, session) at boot and on every watcher run, and restart a stopped session.
+
+## 5. The coordinator session
+
+The session name is `COORD-<RepoName>`. Its standing launch prompt must state, as a standing owner authorization, that the coordinator carries the issue-pipeline duties of `~/.claude/WORKER-CONTRACT.md` section 4 ("Issue pipeline duties"). The duties include: adopt a claimed issue, start a worker for a level `none` claim, and, after a run ends `succeeded`, the coordinator-only completion update `superclaude issue-pipeline complete` that moves the Project Status to `In review` and posts one result comment. The Full Submit push rule: at Full Submit the launched agent pushes its own feature branch; the coordinator never pushes worker commits without the person's go.
+
+## 6. The organization issue field `Approved`
+
+The approval is the organization issue field `Approved` (single select, option `Yes`, visible to the organization members) that every workspace's approvers set. The template does not create it; the owner creates it once for the organization. The first-run check reports `approved_field_missing` for a repository whose organization lacks it, and the loop skips that repository.
+
+## 7. Credentials
+
+The launch-level guard is text-only, and the launch account is also an approver, so launched agents and workers should hold a token with no issues or projects write, or the watcher should run under a dedicated launch login. Until then the first-run report and `check-config` print `warning: approver_is_launch_account` when the approvers file holds the launch account.
+
+## 8. Hosts must install guard version 2
+
+The launch-level guard version stamp is 2. Each host runs `superclaude install --force` once after receiving the build; until then the hook script on the host is version 1.

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
