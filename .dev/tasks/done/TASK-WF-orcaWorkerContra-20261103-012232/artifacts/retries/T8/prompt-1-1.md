ebf8633471ff532365c6e1f73aed2f2ec554f729
Review one task for spec compliance.

Task brief: ## Task 8: Write the P0 static report and the commit list for the owner's approval

Depends on: Task 4, Task 6, Task 7

Re-run these checks at the end of the static plan and save each output as its evidence file:
- AC-0.1: the three commands of `./source.md` section 7.3 (the `KNOWN_CORE_FILES` assertion, the install check and `uv run pytest tests/skills/test_worker_contract.py -q`), saved to `./artifacts/ac-0.1.txt`;
- AC-0.2: the `cmp` and the routing-guide test run from Task 4, saved to `./artifacts/ac-0.2.txt`;
- AC-0.3: the deletions check, saved to `./artifacts/ac-0.3.txt`;
- AC-C1: the scan prints nothing, saved to `./artifacts/ac-c1.txt`;
- AC-C2: `make verify-sync` exits 0, saved to `./artifacts/ac-c2.txt`;
- AC-C3 (cite `./artifacts/ac-c3-compare.md` from Task 6, re-running it if any file changed since);
- AC-C5, recorded in `./artifacts/ac-c5.txt` as run with an empty edit set, because P0 edits no command file;
- AC-C6 (cite `./artifacts/ac-c6-depth-setting.txt`).

Run the AC-C4 check on the index and save its output. Write `./artifacts/p0-static-report.md`, then finish the task with `git add .dev/tasks`, so the report and every artifact are staged. The report has one PASS or FAIL line, with its evidence file, for each of AC-0.1, AC-0.2, AC-0.3, AC-0.7, AC-0.9, AC-C1, AC-C2, AC-C3, AC-C4, AC-C5 and AC-C6. It also lists every repo path this plan created or changed, outside `.claude/`, that the coordinator's owner-approved commit must include. That list covers at least `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/cli/install_core.py`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `tests/skills/test_worker_contract.py`, any plugin copy from Task 3, and `.dev/tasks`. It ends with the next steps of `./source.md` section 6 and section 7.2: the coordinator asks the owner to approve the commit, then `uv run superclaude install --force` from this checkout, and then the P0 live plan is written.

Acceptance criteria:
- `./artifacts/p0-static-report.md` has a PASS or FAIL line for each of the eleven checks listed above. Each line names its evidence file, and that file exists: `ac-0.1.txt`, `ac-0.2.txt`, `ac-0.3.txt`, `ac-0.7-depth-trace.md`, `ac-0.9-hits.txt`, `ac-c1.txt`, `ac-c2.txt`, `ac-c3-compare.md`, `ac-c4-index.txt`, `ac-c5.txt` and `ac-c6-depth-setting.txt`, all under `./artifacts/`. The report also has the commit path list.
- `./artifacts/ac-c4-index.txt` holds the output of `git diff --cached --name-only | grep '^\.claude/' | grep -v '^\.claude/settings\.json$'`, and the file is empty (AC-C4 on the index).
- `git diff --cached --name-only -- .dev/tasks` lists this package's files.

AC ids, in the order of the Acceptance criteria bullets: T8.AC1, T8.AC2, T8.AC3.
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
Start sha: ebf8633471ff532365c6e1f73aed2f2ec554f729
Diff against the start snapshot: Files present in the start tree (diff against the start tree):
```diff
diff --git a/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-c3-compare.md b/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-c3-compare.md
index d8be4e57..d648523a 100644
--- a/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-c3-compare.md
+++ b/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-c3-compare.md
@@ -21,3 +21,7 @@ Result: AC-C3 passes.
 ## Tracked files
 
 `git status --short` was captured before and after the run; the two outputs are identical, so the run changed no tracked file.
+
+## Task 8 re-run
+
+After Task 6, only Task 7 changed files, and only under `./artifacts/`. Task 8 re-ran the same command anyway on 2026-11-03: `804 passed in 12.46s`, `rc=0`, no `FAILED` line, and `git status --short` unchanged by the run. The result above still holds: AC-C3 passes.
```
New untracked files written by this task (absent from the start tree; the whole file is the diff, Read each in full from disk):
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-0.1.txt
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-0.2.txt
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-0.3.txt
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-c1.txt
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-c2.txt
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-c4-index.txt
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-c5.txt
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/p0-static-report.md

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
