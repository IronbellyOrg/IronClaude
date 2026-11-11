5ea28075e3fb46f09f5eacf3821b7eebbad65551
Review one task for spec compliance.

Task brief: 
## Task 5: Rewrite the HOW-WE-WORK Orca bullet and keep the plugin copy identical

Depends on: Task 3

In `src/superclaude/core/HOW-WE-WORK.md`, in the "Orca coordination" section replace the bullet at line 403 ("**`--unattended` only where the command supports it.** ...") with a bullet headed `**\`--unattended\` is the default on a worker's \`Command:\` line.**` that says: put `--unattended` and exactly one report directory on every `Command:` line, per step and never session-wide, unless the two-copy test in `~/.claude/WORKER-CONTRACT.md` ("Before the first task-create for a command") fails for that command; the default set is the 16 phase 1 commands until a phase 2 live check passes; the flag drops approval-required items (improve, cleanup), a failing test suite still ends `succeeded`, research is forced to planning, workflow skips `--handoff implement`, and no push or PR; start each command through its Skill call; a person-in-the-loop run is not a worker. Do not change any other line, including the routing table and the level table. Then copy the file byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (`cp`).

Acceptance criteria:
- T5.AC1: `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` exits 0.
- T5.AC2: `git diff --stat` shows only the one bullet changed in each of the two files, and `src/superclaude/core/CLAUDE.md` is unchanged because no level-table text changed.
- T5.AC3: `uv run pytest tests/core/test_how_we_work_routing_table.py tests/commands/test_routing_plugin_parity.py tests/cli/test_how_we_work_install.py -q` passes.

Global constraints: 
## Constraints

- Edit only these files: `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` and `tests/skills/test_worker_contract.py`. Run `make sync-dev` afterwards; never stage anything under `.claude/`.
- Do not edit any of the 31 files in `src/superclaude/commands/`, `/sc:recommend`, the claim pipeline, Orca's own guide or skills, or any prose for headless callers (sprint, issue-watch, claim-launched agents, eval suites, Coder CI).
- Do not make a worker add the flag, install a copy or rewrite its brief. The guard stays report-only.
- Leave untouched, and do not decide, the owner decisions: the five gates that turn a person's check into a caller input (`/sc:review-translation --context`, `/sc:cli-portify --resume`, `/sc:cli-eval` W3, `/sc:reflect --remediate`, `/sc:tdd`), and whether cleanup, improve, task, tasklist and cli-eval are held out until phase 2 passes. The existing table rows for these commands keep their wording.
- Do not push and do not open a PR. Stage `.dev/tasks` with `git add .dev/tasks`. A local commit on the feature branch is allowed.

Start sha: 5ea28075e3fb46f09f5eacf3821b7eebbad65551
Diff against the start snapshot: 
diff --git a/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md b/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
index 1af98ef3e..4aa11d24d 100644
--- a/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
+++ b/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
@@ -400,7 +400,7 @@ Orca can run IronClaude commands as workers. The rules live in `~/.claude/WORKER
 
 - **The coordinator is a session the person opened.** It plans the work, creates one Orca Task per unit of work, starts one worker per Task and reads each worker's report. It is never a session that Orca itself started as a worker.
 - **Each worker runs one IronClaude command.** The coordinator writes each Task's brief from the brief template in `~/.claude/WORKER-CONTRACT.md`, with the guard line first and the command on its own `Command:` line. The command runs at the top level of the worker session, never inside a subagent, and commands themselves never call Orca.
-- **`--unattended` only where the command supports it.** A command is dispatched with `--unattended` only when its command file has an `## Unattended mode` section. Check the command file instead of relying on a list here; which commands have the section changes as the rollout proceeds.
+- **`--unattended` is the default on a worker's `Command:` line.** Put `--unattended` and exactly one report directory on every `Command:` line, for each step and never for the whole session, unless the two-copy test in `~/.claude/WORKER-CONTRACT.md` ("Before the first task-create for a command") fails for that command. The default set is the 16 phase 1 commands until a phase 2 live check passes. The flag changes what a command does: improve and cleanup skip approval-required items, a failing test suite still ends `succeeded`, research is forced to planning, workflow skips `--handoff implement`, and nothing is pushed or opened as a PR. Start each command through its Skill call. A person-in-the-loop run is not a worker.
 - **Some commands are never workers.** `/sc:pr-submit` and the other commands on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md` stay with the coordinator or the person.
 - **Orca creates the worktrees.** Feature and child worktrees are created by Orca at its default paths, not with raw `git worktree add` and not under `.dev/worktrees/`.
 - **Outward actions stay with the coordinator.** Every push, PR, merge, comment, install and paid run is done by the coordinator, on `IronbellyOrg/IronClaude` only, never on the SuperClaude upstream. PRs go through `/sc:pr-submit --monitor 3` as section 4 says.
diff --git a/src/superclaude/core/HOW-WE-WORK.md b/src/superclaude/core/HOW-WE-WORK.md
index 1af98ef3e..4aa11d24d 100644
--- a/src/superclaude/core/HOW-WE-WORK.md
+++ b/src/superclaude/core/HOW-WE-WORK.md
@@ -400,7 +400,7 @@ Orca can run IronClaude commands as workers. The rules live in `~/.claude/WORKER
 
 - **The coordinator is a session the person opened.** It plans the work, creates one Orca Task per unit of work, starts one worker per Task and reads each worker's report. It is never a session that Orca itself started as a worker.
 - **Each worker runs one IronClaude command.** The coordinator writes each Task's brief from the brief template in `~/.claude/WORKER-CONTRACT.md`, with the guard line first and the command on its own `Command:` line. The command runs at the top level of the worker session, never inside a subagent, and commands themselves never call Orca.
-- **`--unattended` only where the command supports it.** A command is dispatched with `--unattended` only when its command file has an `## Unattended mode` section. Check the command file instead of relying on a list here; which commands have the section changes as the rollout proceeds.
+- **`--unattended` is the default on a worker's `Command:` line.** Put `--unattended` and exactly one report directory on every `Command:` line, for each step and never for the whole session, unless the two-copy test in `~/.claude/WORKER-CONTRACT.md` ("Before the first task-create for a command") fails for that command. The default set is the 16 phase 1 commands until a phase 2 live check passes. The flag changes what a command does: improve and cleanup skip approval-required items, a failing test suite still ends `succeeded`, research is forced to planning, workflow skips `--handoff implement`, and nothing is pushed or opened as a PR. Start each command through its Skill call. A person-in-the-loop run is not a worker.
 - **Some commands are never workers.** `/sc:pr-submit` and the other commands on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md` stay with the coordinator or the person.
 - **Orca creates the worktrees.** Feature and child worktrees are created by Orca at its default paths, not with raw `git worktree add` and not under `.dev/worktrees/`.
 - **Outward actions stay with the coordinator.** Every push, PR, merge, comment, install and paid run is done by the coordinator, on `IronbellyOrg/IronClaude` only, never on the SuperClaude upstream. PRs go through `/sc:pr-submit --monitor 3` as section 4 says.


Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (empty)

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
