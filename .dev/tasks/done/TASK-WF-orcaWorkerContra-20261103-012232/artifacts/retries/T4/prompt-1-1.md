1fcb0d74f1e8c8369b89d02f6d9f8803100ba015
Review one task for spec compliance.

Task brief: ## Task 4: Add an Orca section to the routing guide and its copies

Depends on: Task 2

Add one new section to `src/superclaude/core/HOW-WE-WORK.md` that describes Orca coordination as `./source.md` defines it:
- the coordinator is a session the person opened (D5);
- it dispatches IronClaude commands as workers using the brief template in `~/.claude/WORKER-CONTRACT.md`;
- a command is dispatched with `--unattended` only when its command file has an `## Unattended mode` section (section 6, "Which commands accept `--unattended`");
- `/sc:pr-submit` and the other commands on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md` are never workers;
- worktrees are created by Orca at its default paths;
- outward actions stay with the coordinator, on `IronbellyOrg/IronClaude`.

Append the section as a new top-level `##` section after the `<!-- /routing-table -->` marker at the end of the file, outside the level-table, other-commands and routing-table markers. Write it in ASCII only: no em dashes, arrows or other non-ASCII characters (`tests/core/test_how_we_work_routing_table.py` checks this). Point to `~/.claude/WORKER-CONTRACT.md` for the rules instead of restating them, and do not hard-code which commands accept the flag. Change no existing line and no routing-table row (`./source.md` SA-5). Then copy the file byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. The section 6 P0 row's other mirrored copy is the level table in `src/superclaude/core/CLAUDE.md`: if the level table is untouched, that copy needs no change (repo `CLAUDE.md`, "Key Documentation Files"). Run `make sync-dev`.

Acceptance criteria:
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` exits 0, and `uv run pytest tests/core/test_how_we_work_routing_table.py tests/core/test_claude_md_routing_block.py tests/cli/test_how_we_work_install.py -q` passes (AC-0.2).
- `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/core/HOW-WE-WORK.md | awk '$2 != 0'` prints nothing (AC-0.3: no existing line deleted).
- `uv run pytest tests/core tests/commands tests/recommend tests/cli -q -rf --ignore=tests/cli/eval/test_perf_home_setup.py` shows no test that passed in `./artifacts/t1-baseline-wider.txt` now failing. The per-test comparison, which names each remaining failure as accepted in `./artifacts/t1-accepted-failures.md`, is saved to `./artifacts/t4-wider-compare.md`. That comparison file is this check's evidence, not the raw log, and `git status --short` shows no tracked file changed by the run.
- The AC-C1 scan in `./source.md` section 7.1 prints nothing, and `make verify-sync` exits 0 (AC-C2).

AC ids, in the order of the Acceptance criteria bullets: T4.AC1, T4.AC2, T4.AC3, T4.AC4.
Package root (resolves ./artifacts/ and ./source.md): /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232
Global constraints: ## Constraints

- This is the static plan of Phase P0 (`./source.md` section 6, last paragraph: each phase's plan has a static part and a live part). It covers AC-0.1, AC-0.2, AC-0.3, AC-0.7 and AC-0.9 (section 7.3), and the common checks AC-C1, AC-C2, AC-C3, AC-C5 and AC-C6 (section 7.1). AC-C4 is checked on the index at the end of this plan and again by the coordinator at commit time. The live checks (AC-0.4, AC-0.5, AC-0.6) and the P0 phase report belong to the P0 live plan, which is written after this plan's checks pass. AC-0.8 is a P1 check (section 7.3). Phases P1-P4 get their own plans later; they are not dropped.
- No task in this plan commits, installs into `~/.claude`, starts an Orca worker or asks the owner a question. Between this plan and the live plan, the coordinator session asks the owner, commits and runs `uv run superclaude install --force`, as `./source.md` section 7.2 states, outside any plan run. `/sc:implement` may not prompt the user outside its halt paths (`./source.md` section 6, last paragraph).
- P0 edits no command file, no `SKILL.md` and no agent file (`./source.md` section 6, P0 row: "no command edits"). The only file this plan writes inside a skill package (`src/superclaude/skills/` or `plugins/superclaude/skills/`) is the byte-for-byte copy of `HOW-WE-WORK.md` at `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` that Task 4 makes. `tests/skills/test_worker_contract.py` is a test file, not a skill package. The `.claude/` copies that `make sync-dev` writes are sync output. No command gains `--unattended` or an `## Unattended mode` section in P0 (section 6, table "Which commands accept `--unattended`", P0 row: none).
- `WORKER-CONTRACT.md` restates only what `./source.md` sections 2.1, 2.2 and 2.3 say and adds no rule the spec lacks. The one exception is the brief template, which also carries the section 3.1 "Brief must pass" flags and the section 6 phase markers (`--report-dir` marked "from P1"). For the worker-session duties (WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats), the contract states only the IronClaude-specific rule and points to the dispatch preamble for Orca verb syntax and heartbeat cadence, never copying them (section 2.1, "Contract file"). These duties are not copied in full. Task 5 pins them by the short phrases that Tasks 1 and 2 record. This no-copy rule does not cover the coordinator's brief template, whose guard line and `worker_done` text are copied word for word from section 2.3 "Brief layout".
- `WORKER-CONTRACT.md` and the new `HOW-WE-WORK.md` section are installed files, so they use installed paths only (`~/.claude/...`). They copy none of the spec's evidence ids (`CAPS:`, `INV-`, `EVIDENCE.md:`) and no `src/superclaude/...` or other repo-path citations (repo `CLAUDE.md`, "Never Hardcode `src/superclaude/` Paths in Installed Primitives"). Where a rule needs to cite a skill file (for example `ledger.md:71` or `refs/retry.md:498` in the section 2.3 resume check), the citation is rewritten as an installed path, such as `~/.claude/skills/sc-implement-protocol/refs/ledger.md`.
- `src/superclaude/` is the source of truth. After editing it, run `make sync-dev`; never stage `.claude/` paths other than `.claude/settings.json` (repo `CLAUDE.md`, "Never Stage or Commit `.claude/` Contents"). `.dev/tasks/` is always staged (`git add .dev/tasks`); staging is not committing.
- No command, skill or agent file may name `orca` or `orca-ide` verbs (`./source.md` SA-2, AC-C1). Only `WORKER-CONTRACT.md` and `HOW-WE-WORK.md`, and their plugin copies, may describe the coordinator side.
- Every git and GitHub outward action targets `IronbellyOrg/IronClaude` only; SuperClaude upstream is never pushed to or interacted with (`./source.md` section 2.3, "Git and GitHub ownership"). This plan pushes nothing and opens no PR.
- Orca checks in this plan are read-only: no Orca command that starts, sends or creates anything is run.
- Use `uv run` for all Python.
Start sha: 1fcb0d74f1e8c8369b89d02f6d9f8803100ba015
Diff against the start snapshot: Files present in the start tree (diff against the start tree):
```diff
diff --git a/src/superclaude/core/HOW-WE-WORK.md b/src/superclaude/core/HOW-WE-WORK.md
index dbd79241..9fbf138a 100644
--- a/src/superclaude/core/HOW-WE-WORK.md
+++ b/src/superclaude/core/HOW-WE-WORK.md
@@ -391,3 +391,14 @@ The `changes_files` column is not a zero-write promise: `yes` includes requested
 | tier-validation | validate task-tier behavior against YAML expectations, not application coverage | - | 1. verify supplied YAML file/directory or advertised default suite exists<br>2. `/sc:validate-tests <verified target>` with supplied controls only when prerequisites exist<br>3. stop at classification result and requested report | - | no | 3.13, 3.14 | retain `/sc:validate-tests --verbose --summary --category <name> --stop-on-fail --report <path>` only as requested and without conflicting verbosity; advertised tests/sc-task default is absent here, so report missing prerequisite rather than invent a fixture/result; no code/config repairs or fabricated counts |
 
 <!-- /routing-table -->
+
+## Orca coordination
+
+Orca can run IronClaude commands as workers. The rules live in `~/.claude/WORKER-CONTRACT.md`; this section only says how the pieces fit.
+
+- **The coordinator is a session the person opened.** It plans the work, creates one Orca Task per unit of work, starts one worker per Task and reads each worker's report. It is never a session that Orca itself started as a worker.
+- **Each worker runs one IronClaude command.** The coordinator writes each Task's brief from the brief template in `~/.claude/WORKER-CONTRACT.md`, with the guard line first and the command on its own `Command:` line. The command runs at the top level of the worker session, never inside a subagent, and commands themselves never call Orca.
+- **`--unattended` only where the command supports it.** A command is dispatched with `--unattended` only when its command file has an `## Unattended mode` section. Check the command file instead of relying on a list here; which commands have the section changes as the rollout proceeds.
+- **Some commands are never workers.** `/sc:pr-submit` and the other commands on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md` stay with the coordinator or the person.
+- **Orca creates the worktrees.** Feature and child worktrees are created by Orca at its default paths, not with raw `git worktree add` and not under `.dev/worktrees/`.
+- **Outward actions stay with the coordinator.** Every push, PR, merge, comment, install and paid run is done by the coordinator, on `IronbellyOrg/IronClaude` only, never on the SuperClaude upstream. PRs go through `/sc:pr-submit --monitor 3` as section 4 says.
diff --git a/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md b/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
index dbd79241..9fbf138a 100644
--- a/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
+++ b/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
@@ -391,3 +391,14 @@ The `changes_files` column is not a zero-write promise: `yes` includes requested
 | tier-validation | validate task-tier behavior against YAML expectations, not application coverage | - | 1. verify supplied YAML file/directory or advertised default suite exists<br>2. `/sc:validate-tests <verified target>` with supplied controls only when prerequisites exist<br>3. stop at classification result and requested report | - | no | 3.13, 3.14 | retain `/sc:validate-tests --verbose --summary --category <name> --stop-on-fail --report <path>` only as requested and without conflicting verbosity; advertised tests/sc-task default is absent here, so report missing prerequisite rather than invent a fixture/result; no code/config repairs or fabricated counts |
 
 <!-- /routing-table -->
+
+## Orca coordination
+
+Orca can run IronClaude commands as workers. The rules live in `~/.claude/WORKER-CONTRACT.md`; this section only says how the pieces fit.
+
+- **The coordinator is a session the person opened.** It plans the work, creates one Orca Task per unit of work, starts one worker per Task and reads each worker's report. It is never a session that Orca itself started as a worker.
+- **Each worker runs one IronClaude command.** The coordinator writes each Task's brief from the brief template in `~/.claude/WORKER-CONTRACT.md`, with the guard line first and the command on its own `Command:` line. The command runs at the top level of the worker session, never inside a subagent, and commands themselves never call Orca.
+- **`--unattended` only where the command supports it.** A command is dispatched with `--unattended` only when its command file has an `## Unattended mode` section. Check the command file instead of relying on a list here; which commands have the section changes as the rollout proceeds.
+- **Some commands are never workers.** `/sc:pr-submit` and the other commands on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md` stay with the coordinator or the person.
+- **Orca creates the worktrees.** Feature and child worktrees are created by Orca at its default paths, not with raw `git worktree add` and not under `.dev/worktrees/`.
+- **Outward actions stay with the coordinator.** Every push, PR, merge, comment, install and paid run is done by the coordinator, on `IronbellyOrg/IronClaude` only, never on the SuperClaude upstream. PRs go through `/sc:pr-submit --monitor 3` as section 4 says.
```
New untracked files written by this task (absent from the start tree; the whole file is the diff, Read each in full from disk):
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t4-checks.txt
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t4-wider.txt
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t4-wider-compare.md

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
