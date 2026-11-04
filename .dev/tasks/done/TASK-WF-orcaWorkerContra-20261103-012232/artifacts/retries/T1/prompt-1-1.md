e566ed974aca8f0e2a977a8095afe408467cce84
Review one task for spec compliance.

Task brief: ## Task 1: Write the command-side and worker-session rules of `WORKER-CONTRACT.md` and register it as a core file

Before any edit in this plan, record two baselines:
- the AC-C3 baseline: run `uv run pytest tests/skills/ -q -rf` and save its full output to `./artifacts/ac-c3-baseline.txt` (`./source.md` section 7.1, AC-C3);
- the wider baseline that Task 4 compares against: run `uv run pytest tests/core tests/commands tests/recommend tests/cli -q -rf --ignore=tests/cli/eval/test_perf_home_setup.py` and save its full output to `./artifacts/t1-baseline-wider.txt`. The `--ignore` keeps that test from rewriting the tracked file `.dev/releases/current/cliEval/evidence/T02.15/perf.json`. After each baseline run, `git status --short` must show no tracked file changed by the run.

Both baselines are inputs, not evidence: they may contain failures that exist before this plan. Eight such failures are known on 2026-11-03 and are accepted as the baseline:
- `tests/cli/eval/test_ban_import_rule.py::test_clean_tree_passes_ruff_check`
- `tests/cli/eval/test_ban_import_rule.py::test_synthetic_import_anthropic_is_flagged_by_ruff`
- `tests/cli/eval/test_ban_import_rule.py::test_ban_message_references_fr_g1`
- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval`
- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module`
- `tests/cli/test_verify_sync_hooks.py::test_V1_clean_tree_exits_zero`
- `tests/cli/test_verify_sync_hooks.py::test_V2_missing_claude_hook_detected`
- `tests/cli/test_verify_sync_hooks.py::test_V7_regression_to_master`

Write `./artifacts/t1-accepted-failures.md`. It records that both baseline files exist and lists every test that fails in either baseline. Each failing test gets one of two labels: `accepted` if it is in the list above, or `pre-existing` if not. Cite that file, not the raw logs, as this task's evidence.

Create `src/superclaude/core/WORKER-CONTRACT.md` with the rules `./source.md` section 2.1 ("Contract file") assigns to it, written from these source sections:
- Terms from section 2.1: worker run; unattended mode (selected only by the flag, decision D1); the flag parse rule; the person-mode flag refusals; the report directory rule (exactly one of the command's own directory output flag or `--report-dir`); the brief guard, with its scope and its four refusal conditions (case 1, case 2, copies disagree, case 3), its three exact reason texts (`guard refused: brief lacks --unattended`, `guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)`, `guard refused: command copies disagree (stale copy): <paths>`) and the `guard refused:` body prefix for case 3; the never-as-worker list; and the nested propagation rule.
- Command-side requirements from section 2.2: WC-2; WC-4 (the contract fields `worker_contract_version`, `worker_status`, `command`, `report_path`, `artifacts`, `blocked_question`, `reason`, the status mapping, and the exact missing-directory error text); WC-8, WC-9, WC-10 and WC-11.
- Worker-session duties from section 2.2: WC-3, WC-5 (including its last sentences: before P1, a brief that states the AC-0.4 report file and outcome rule replaces the mapping for that Task), WC-7, WC-12, WC-13 and heartbeats, stating only the IronClaude-specific rule and pointing to the dispatch preamble for verb syntax and cadence.

For each rule above, record in `./artifacts/t1-rule-phrases.md` at least one short phrase that the contract file carries for it. Take the phrase from `./source.md` where the spec's own wording can be used (for example the reason texts and the WC-4 error text, copied exactly). For WC-12, WC-13 and heartbeats, use the phrases "Coordinator follow-ups are pulled, not pushed" and "at natural checkpoints" (`./source.md` WC-12), "No Orca fan-out from the worker session" (WC-13), and "at the cadence its preamble sets" (WC-10). Do not copy any Orca verb syntax. Task 5 pins these phrases.

In the same task, add `"WORKER-CONTRACT.md"` to the `KNOWN_CORE_FILES` frozenset in `src/superclaude/cli/install_core.py`. `tests/cli/test_how_we_work_install.py` asserts that `KNOWN_CORE_FILES` equals the set of core files the installer ships, so the file and the entry must land together.

Acceptance criteria:
- `src/superclaude/core/WORKER-CONTRACT.md` exists and contains each item listed above under the spec's own identifiers: WC-2 to WC-13 as listed, the four refusal conditions with the three exact reason texts and the case-3 prefix, the WC-5 P0 override, and the never-as-worker list naming `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn`, `/sc:swarm-wizard` and `/sc:pr-submit`.
- The worker-session part contains no `orca orchestration` verb syntax copied from Orca's guides and no fixed heartbeat cadence; it points to the dispatch preamble for both.
- `uv run python -c "from superclaude.cli.install_core import KNOWN_CORE_FILES; assert 'WORKER-CONTRACT.md' in KNOWN_CORE_FILES"` exits 0 (AC-0.1, first part), and `uv run pytest tests/cli/test_how_we_work_install.py -q` passes.
- `./artifacts/t1-accepted-failures.md` records that `./artifacts/ac-c3-baseline.txt` and `./artifacts/t1-baseline-wider.txt` were written before any file in this plan changed. It lists every failing test in them, labelled `accepted` or `pre-existing`, and states that the runs changed no tracked file.
- `./artifacts/t1-rule-phrases.md` names at least one phrase per rule listed above. Each phrase is present in `src/superclaude/core/WORKER-CONTRACT.md`, and none of them is Orca verb syntax.
- The file contains no `src/superclaude/` path and no `CAPS:`, `INV-` or `EVIDENCE.md:` citation.

AC ids, in the order of the Acceptance criteria bullets: T1.AC1, T1.AC2, T1.AC3, T1.AC4, T1.AC5, T1.AC6.
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
Start sha: e566ed974aca8f0e2a977a8095afe408467cce84
Diff against the start snapshot: Tracked files (git diff against the start tree):
```diff
diff --git a/src/superclaude/cli/install_core.py b/src/superclaude/cli/install_core.py
index bc8ede9b..8444707c 100644
--- a/src/superclaude/cli/install_core.py
+++ b/src/superclaude/cli/install_core.py
@@ -23,6 +23,7 @@ KNOWN_CORE_FILES = frozenset(
         "PRINCIPLES.md",
         "RESEARCH_CONFIG.md",
         "RULES.md",
+        "WORKER-CONTRACT.md",
     }
 )
 
```
New untracked files written by this task (absent from the start tree; the whole file is the diff, Read each in full from disk):
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/src/superclaude/core/WORKER-CONTRACT.md
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-accepted-failures.md
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-rule-phrases.md
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-c3-baseline.txt
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-baseline-wider.txt

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
