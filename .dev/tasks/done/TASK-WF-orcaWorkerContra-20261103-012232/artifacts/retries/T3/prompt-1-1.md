cc919c571a9b246518574def7dbf35a2eb71f23f
Review one task for spec compliance.

Task brief: ## Task 3: Decide the plugin copy of `WORKER-CONTRACT.md` and run the AC-0.1 install check

Depends on: Task 2

Decide whether a copy of `WORKER-CONTRACT.md` belongs in `plugins/superclaude/core/`. Read `scripts/build_superclaude_plugin.py` and list the files already in `plugins/superclaude/core/` (today it holds some core files but not `CLAUDE.md` or `HOW-WE-WORK.md`). Add the copy only if that existing convention requires it, and record the decision and the file lines that decided it in `./artifacts/t3-plugin-mirror.md`. If a copy is added, run `make sync-dev` afterwards.

Acceptance criteria:
- The AC-0.1 install check in `./source.md` section 7.3 (the block below the table) exits 0: `uv run python -c "import pathlib, tempfile; from superclaude.cli.install_core import install_core_files; d = pathlib.Path(tempfile.mkdtemp()); ok, msg = install_core_files(target_path=d); assert ok, msg; assert (d / 'WORKER-CONTRACT.md').is_file()"`.
- `uv run pytest tests/cli/test_how_we_work_install.py tests/cli/test_issue_body_templates.py -q` passes.
- `./artifacts/t3-plugin-mirror.md` states whether a plugin copy was added and cites the file lines that decided it; if a copy was added, `cmp src/superclaude/core/WORKER-CONTRACT.md plugins/superclaude/core/WORKER-CONTRACT.md` exits 0.

AC ids, in the order of the Acceptance criteria bullets: T3.AC1, T3.AC2, T3.AC3.
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
Start sha: cc919c571a9b246518574def7dbf35a2eb71f23f
Diff against the start snapshot: Files present in the start tree (diff against the start tree):
```diff
```
New untracked files written by this task (absent from the start tree; the whole file is the diff, Read each in full from disk):
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t3-plugin-mirror.md

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
