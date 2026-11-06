5e9b062753b8b34b6b60e7f0aac181bf7badad47
Review one task for spec compliance.

Task brief: Task T6 (plan file /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md, lines 135-148); AC ids T6.AC1 to T6.AC3 are the bullets under `Acceptance criteria:` in source order.

## Task 6: Convert `/sc:cleanup-audit`: section, final report name, contract write scope

Depends on: Task 1

Files: `src/superclaude/commands/cleanup-audit.md` and `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md`; spec section 3.1 row cleanup-audit.

In `cleanup-audit.md`: add the `--unattended` and `--report-dir` bullets to the "Arguments" list, add one example line inside the Usage code block (the existing usage line is not reworded), and add the `## Unattended mode` section before `## Boundaries`. The section states: report directory is `--report-dir <dir>` only (the command has no directory flag; its audit output stays in the fixed `.claude-audit/`); the contract points `report_path` at `.claude-audit/pass<N>-summary.md` for one pass (surface 1, structural 2, cross-cutting 3) or at `.claude-audit/final-report.md` for `--pass all` (D-P1-10), and lists `.claude-audit/progress.json` and the batch reports in `artifacts`; resume is the `progress.json` checkpoint; "only one audit at a time" runs per worktree because `.claude-audit/` is fixed (spec WC-11); the write scope is `.claude-audit/` plus `<report-dir>/return-contract.yaml`, written as an explicit "except" sentence next to the existing "audit reports written to `.claude-audit/` only" line, without rewording that line; no gate and no person-mode flag; its Agent-tool subagents are unchanged; it pushes, commits and stages nothing.

In `SKILL.md`: name the final report `.claude-audit/final-report.md` in Step 5 "Report" and in "CRITICAL BOUNDARIES" (new sentences), and add the same "except" sentence to the `Write` line of "Tool Coordination" and to the "Output" bullet list. Add this task's entry to `UNATTENDED_EXPECT`: flags `--pass`; phrases `.claude-audit/final-report.md`, `progress.json` and `only one audit at a time`. Add a test to `tests/skills/test_worker_contract.py` that both files name `.claude-audit/final-report.md` and both state the contract write exception.

Acceptance criteria:
- [T6.AC1] `grep -c '^## Unattended mode$' src/superclaude/commands/cleanup-audit.md` prints `1`, and `grep -c 'final-report.md' src/superclaude/commands/cleanup-audit.md src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md` prints a non-zero count for each file.
- [T6.AC2] `uv run pytest tests/skills/test_worker_contract.py tests/skills/test_codegraph_adoption.py -q -p no:cacheprovider` passes.
- [T6.AC3] Check ADDITIVE prints nothing for `cleanup-audit.md`; Check SCAN prints nothing.
Global constraints: (plan `## Constraints`, plan lines 17-44, verbatim)
## Constraints

- Spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` is called "the spec" below, and "spec section N" means its section N. `./source.md` is the inline brief that started this plan. The spec is the authority; where a task cites a section it names the rows the task needs. Decisions: `.dev/orca-command-refactor/decisions/APPROVED.md`, including the 2026-11-05 heartbeat decision (looser reading of spec section 7.2 step 5 condition 4; WC-10 unchanged; P0 verdict PASS). That decision changes nothing in this static plan; it governs how the later live plan reads heartbeat gaps.
- This is the static plan of Phase P1 (spec section 6, last paragraph: each phase plan has a static part and a live part). It covers AC-1.1 and AC-1.4 (spec section 7.3) and the common checks AC-C1 to AC-C6 (spec section 7.1). The live checks AC-1.2, AC-1.3, AC-1.5, AC-1.6, AC-1.7 and AC-1.8 and the P1 phase report belong to the P1 live plan, which is written after this plan's checks pass. P2 to P4 get their own plans later.
- No task in this plan commits, pushes, installs into `~/.claude`, starts an Orca worker, runs an Orca command or asks the owner a question. Between this plan and the live plan, the coordinator session asks the owner, commits and runs the install as spec section 7.2 states, outside any plan run. Nothing under the `.claude/` folder is staged, ever (repo `CLAUDE.md`, "Never Stage or Commit `.claude/` Contents"); `make sync-dev` writes only gitignored `.claude/` copies. `.dev/tasks/` is always staged (`git add .dev/tasks`); staging is not committing.
- `src/superclaude/` is the source of truth. Installed primitives use installed paths only: a new section or sentence never contains `src/superclaude/` and never names an Orca command (spec SA-2; Check SCAN below). The only file under `src/superclaude/core/` that describes the coordinator side is `WORKER-CONTRACT.md`, and this plan does not edit it. The brief-flag table in that file lists the P0-era constraints; the general "Report directory" rule in its section 1 already covers the extra report directory that `--unattended` needs for index-repo and init-lite, so no table row changes.
- Mirrors. UNVERIFIED item 8 of the spec is resolved by the repo's own rule (`src/superclaude/commands/README.md`, step 3): only `help.md`, `recommend.md`, `workflow.md` and `implement.md` are copied byte-for-byte to `plugins/superclaude/commands/`, and `tests/commands/test_workflow_command.py::test_plugin_mirror_matches_src` plus `tests/commands/test_routing_plugin_parity.py` pin them. Of the files this plan edits, only `workflow.md` and the `sc-workflow-protocol` skill (which has a plugin copy) are pinned, so only they are mirrored (Task 9). The other plugin command copies (brainstorm, build, document, index-repo, index, load and test are identical today; analyze, business-panel, design and explain already differ) are not touched.
- Section skeleton. Every `## Unattended mode` section is a level-2 heading written exactly like that, placed immediately before the file's first `## Boundaries` heading (business-panel.md has only `## CRITICAL BOUNDARIES` and uses that; index-repo.md has neither and the section goes after `## Output Format`; graph.md and impact.md name their own anchors in their tasks), and holds only the command's own resolutions. It contains, in this order: an opening sentence that names `~/.claude/WORKER-CONTRACT.md` as the home of the shared rules and tells the reader to read it first; the switch (applies only when `--unattended` is a standalone argument token outside any quoted argument, otherwise nothing in the section applies and no contract is written: spec SA-1 and SA-3); the report directory (exactly one of `--report-dir <dir>` or the command's own directory flag, named per task; if the command has none, `--report-dir` only; `--report-dir` follows the same path rules as the command's own directory flag where it has one: never inside `.git/` or `.codegraph/`, never under the distributable skill, agent or command folders of a `.claude/` folder, created if missing and writable; a report directory that fails them counts as no report directory known, so nothing is written there and the refusal is printed in chat only, as section 1 of `~/.claude/WORKER-CONTRACT.md` says); the contract (`<report-dir>/return-contract.yaml` written on every outcome with `worker_contract_version`, `worker_status`, `command`, `report_path`, `artifacts` and `reason` when failed, naming this command's deliverables for `report_path` and `artifacts`); the person-mode refusals of this command, in every spelling the command accepts (the short form `-i`, the `=` form such as `--format=interactive` or `--mode=socratic`) (refused before any work, contract `worker_status: failed` with the refused flag in `reason`); the gate resolutions of this command (for a no-gate command, the single statement that it has none); the nested invocations of this command (or "none"); and the outward-action rule (the command pushes, commits and stages nothing under `--unattended`, spec WC-9). The section never repeats the shared rules' wording, the exact error text or the status mapping; it points to the contract file.
- Test data. `tests/skills/test_worker_contract.py` gets one entry per command in a dict `UNATTENDED_EXPECT` (Task 1 creates it empty): the command name maps to a dict with `flags` (tokens its section must contain), `phrases` (further text it must contain) and `nested` (the names of the nested commands that receive `--unattended` from this command; an empty list for every command except brainstorm). Each command task adds its own entry in the same task, so the suite is green after every task.
- Check SCAN (spec AC-C1; run after every task that edits a command, skill or core file). Pass: prints nothing.

  ```sh
  grep -rniE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b' \
    src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \
    src/superclaude/hooks src/superclaude/templates plugins/superclaude \
    | grep -v '^src/superclaude/skills/ccsession-tag/' \
    | grep -v '^src/superclaude/core/WORKER-CONTRACT\.md:' \
    | grep -v '^src/superclaude/core/HOW-WE-WORK\.md:' \
    | grep -v '^plugins/superclaude/core/WORKER-CONTRACT\.md:' \
    | grep -v '^plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK\.md:'
  ```

- Check ADDITIVE (spec AC-C5 / SA-4). For every command file a task edits, `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/commands/<name>.md | awk '$2 != 0'` prints nothing. Edits to command files are added lines; an existing line is never reworded. The only two command files exempt are `business-panel.md` (the frontmatter move deletes the fence lines) and `load.md` (the usage-line fix replaces one line); their tasks say so. Skill and test files have no such rule.
- Check WRITEVERB (spec AC-0.9). New text in any command or skill file must not contain the audit's write-verb phrases: `git add`, `git commit`, `git push`, `git merge`, `git stash`, `git update-ref`, `git worktree add` or `remove`, `gh pr`, `gh api`. The test `tests/skills/test_worker_contract.py::test_every_write_verb_hit_is_classified` and `::test_classification_table_has_no_stale_entries` must still pass, so no classified line is edited. The one classified P1 line is the `.dev/tasks/` staging sentence in `src/superclaude/skills/sc-workflow-protocol/SKILL.md` (category `deferred:P1`); it stays word for word.
- Test commands. Every pytest run in this plan passes `-p no:cacheprovider`. After every test, lint or sync run, `git status --short` shows no tracked file changed by the run itself. The wider test run always passes `--ignore=tests/cli/eval/test_perf_home_setup.py`, because that test rewrites a tracked evidence file. UV for every Python command; no bare `python`, `python3` or `pip`.
- Pre-existing tests that read the files this plan edits, and must still pass: `tests/commands/test_workflow_command.py`, `tests/commands/test_graph_command.py`, `tests/commands/test_impact_command.py`, `tests/commands/test_routing_plugin_parity.py`, `tests/skills/test_brainstorm_protocol.py`, `tests/skills/test_codegraph_adoption.py`, `tests/skills/test_primitive_dual_surface_lookup.py`, `tests/skills/test_tier2_tavily_consistency.py`, `tests/skills/test_repo_inventory_nongit.py`, `tests/skills/test_worker_contract.py`, `tests/cli_portify/test_brainstorm_gaps.py`, `tests/cli/test_init_lite.py`, `tests/unit/test_cli_install.py`, `tests/roadmap/test_threshold_registry.py`, `tests/core/test_how_we_work_routing_table.py` and `tests/recommend/test_routing_refresh.py`. The graph and impact tests pin frontmatter, section order and word lists; the workflow tests pin the `--output` retirement (every line of the command, skill or a ref that contains `--output` must also contain `retired`, `E-LEGACY` or `Never`).
- Decisions this plan makes where the spec is silent or ambiguous (each is also reported to the coordinator). D-P1-1: the spec can be read two ways for graph and impact. Its worker field `command` is the exact command line, but their own contracts already write a `command` key holding the short name (`graph`, `impact`). This plan keeps the existing key and value (spec WC-4: an existing contract keeps every existing field), counts it as the worker `command` field and adds no second key; the owner approved this on 2026-11-05 (decisions file, section "P1 owner decisions"). D-P1-2: for the seven report-style no-gate commands (analyze, build, design, explain, index, test, business-panel) `--output <file>` is new and optional; under `--unattended` without it the report goes to `<report-dir>/<name>-report.md`, so the contract always has a `report_path`. D-P1-3: brainstorm's own status `dry-run` maps to `worker_status: succeeded` with `report_path: null` (the spec's mapping list lacks it). D-P1-4: the nested propagation rule (spec section 2.1) is applied to brainstorm: its adversarial call and its `/sc:analyze` enrichment get `--unattended` and a nested report directory; research enrichment and the `tasklist` and `task` handoffs are skipped and recorded. The owner confirmed this on 2026-11-05 after an adversarial debate (decisions file, section "P1 owner decisions"): spec section 2.1's nested rule applies to every called command that accepts the flag in this phase, and the spec's "from P2" wording covers research enrichment only. D-P1-5: workflow skips a `--handoff implement` under `--unattended` (implement has gates and accepts the flag only in P4) and records it in the package contract as `partial` with an `unresolved` line; its reflect step runs as today (gate-free without `--remediate`). D-P1-6: graph refuses `init` under `--unattended`. D-P1-7: document requires an explicit `--output` for the external, api and guide types under `--unattended`. D-P1-8: a failing test suite is a verdict in the `/sc:test` report, not a failed run; `worker_status` is `failed` only when the runner could not run. D-P1-9: adversarial's `report_path` is its merged output (null when the merge was not reached). D-P1-10: cleanup-audit's `--pass all` final report is named `.claude-audit/final-report.md`. D-P1-11: init-lite writes the worker contract also on `--dry-run`, so the exception in its skill covers Safety Invariant 2 as well as 3 (the spec row names only 3). D-P1-12: a command's consent line is never answered under `--unattended` by assuming consent: analyze modifies no source and design changes no architecture; `/sc:test --fix` is the caller's consent for non-destructive fixes only, and a destructive change to a test file is never made; `/sc:index` overwrites no existing manual documentation and writes only the `--output` path the caller passed (or the default report file).
- Nothing in this plan edits `WORKER-CONTRACT.md`, `HOW-WE-WORK.md`, `KNOWN_CORE_FILES`, any agent file, any other command or skill, or any Python module under `src/superclaude/cli/`.
Start sha: 5e9b062753b8b34b6b60e7f0aac181bf7badad47
Diff against the start snapshot: diff --git a/src/superclaude/commands/cleanup-audit.md b/src/superclaude/commands/cleanup-audit.md
index 183af3ca..7817f05b 100644
--- a/src/superclaude/commands/cleanup-audit.md
+++ b/src/superclaude/commands/cleanup-audit.md
@@ -29,6 +29,7 @@ personas: [analyzer, architect, devops, qa, refactorer]
 
 ```
 /sc:cleanup-audit [target-path] [--pass surface|structural|cross-cutting|all] [--batch-size N] [--focus infrastructure|frontend|backend|all]
+/sc:cleanup-audit --pass surface --unattended --report-dir DIR   # worker mode, see Unattended mode
 ```
 
 ### Arguments
@@ -37,6 +38,8 @@ personas: [analyzer, architect, devops, qa, refactorer]
 - **--pass**: Audit pass to run (`surface` = Pass 1, `structural` = Pass 2, `cross-cutting` = Pass 3, `all` = sequential 3-pass)
 - **--batch-size**: Files per agent batch (default: 50 for surface, 25 for structural, 30 for cross-cutting)
 - **--focus**: Domain filter for targeted auditing (`infrastructure`, `frontend`, `backend`, `all`)
+- **--unattended**: Worker mode: no step waits for a person; see Unattended mode
+- **--report-dir**: With `--unattended`, the directory that holds the worker contract (required; the command has no other directory flag)
 
 ## Behavioral Summary
 
@@ -84,6 +87,18 @@ Runs all 3 passes sequentially with quality gates between each pass. Pass 1 inve
 Do NOT proceed with protocol execution using only this command file.
 The full behavioral specification is in the protocol skill.
 
+## Unattended mode
+
+The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:cleanup-audit` resolves itself.
+
+- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
+- **Report directory.** `--report-dir <dir>` only: the command has no directory flag, and its audit output stays in the fixed `.claude-audit/`. Without `--report-dir` the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/`, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
+- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is `.claude-audit/pass<N>-summary.md` for one pass (`surface` is 1, `structural` 2, `cross-cutting` 3) or `.claude-audit/final-report.md` for `--pass all`; `artifacts` lists `.claude-audit/progress.json` and the batch reports. A run that finishes every requested pass is succeeded; one that stops after a checkpoint is partial, and a rerun resumes from `.claude-audit/progress.json`.
+- **Concurrency.** `.claude-audit/` is fixed, so only one audit at a time runs per worktree (WC-11 in `~/.claude/WORKER-CONTRACT.md`).
+- **Write scope.** `.claude-audit/` plus `<report-dir>/return-contract.yaml`; the read-only rule for repository files is unchanged.
+- **Gates.** None, and no person-mode flag. Nested invocations: none; its Agent-tool subagents are unchanged.
+- **Outward actions.** It pushes, commits and stages nothing.
+
 ## Boundaries
 
 **Will:**
@@ -116,4 +131,6 @@ The full behavioral specification is in the protocol skill.
 - Final report (executive summary + prioritized actions)
 - progress.json (checkpoint state for resume capability)
 
+Except under `--unattended`: `<report-dir>/return-contract.yaml` is also written (see Unattended mode).
+
 **Next Step**: Use `/sc:cleanup` to execute safe recommendations, then `/sc:test` to verify no regressions, then `/sc:git` to commit changes.

diff --git a/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md b/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md
index 4f16cc85..a5300c0a 100644
--- a/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md
@@ -67,7 +67,7 @@ argument-hint: "[target-path] [--pass surface|structural|cross-cutting|all] [--b
 2. **Configure**: Parse `$ARGUMENTS` for pass selection and focus area. Load pass-specific rules from `rules/` supporting files. Create TodoWrite tasks for each batch. Initialize output directory at `.claude-audit/`.
 3. **Orchestrate**: Spawn parallel subagents via Task tool in waves of 7-8 concurrent agents. Pass 1 uses `audit-scanner` (Haiku), Pass 2 uses `audit-analyzer` (Sonnet), Pass 3 uses `audit-comparator` (Sonnet). Each agent writes batch reports incrementally to disk. Track progress via TodoWrite.
 4. **Validate**: Spawn `audit-validator` for 10% spot-check sampling (5 findings per 50 files). Verify grep claims match actual results. Enforce quality gates: all batch reports must have required sections and mandatory per-file profiles. Failed reports trigger regeneration.
-5. **Report**: Spawn `audit-consolidator` to merge batch reports into pass summaries. For `--pass all`, produce final report with executive summary, prioritized action items, cross-cutting findings, and discovered issues registry. Apply ultrathink synthesis for cross-pass pattern extraction.
+5. **Report**: Spawn `audit-consolidator` to merge batch reports into pass summaries. For `--pass all`, produce final report with executive summary, prioritized action items, cross-cutting findings, and discovered issues registry. Apply ultrathink synthesis for cross-pass pattern extraction. The final report of `--pass all` is `.claude-audit/final-report.md`.
 
 Key behaviors:
 
@@ -90,7 +90,7 @@ Key behaviors:
 
 - **Read/Grep/Glob**: Core audit tools available to all subagents — file content reading, reference tracing via regex, file inventory via pattern matching
 - **Bash(git/wc/find/du)**: Controlled shell access for orchestrator only — `git ls-files` for inventory, `wc` for counting, `find` for scope calculation, `du` for size metrics
-- **Write**: Report generation restricted to `.claude-audit/` output directory — batch reports, pass summaries, final report, progress tracking files
+- **Write**: Report generation restricted to `.claude-audit/` output directory — batch reports, pass summaries, final report, progress tracking files. Except under `--unattended`: `<report-dir>/return-contract.yaml` is also written (see the Unattended mode section of the command file).
 - **TodoWrite**: Progress tracking with per-batch tasks — create tasks during Configure, update during Orchestrate, verify completion during Validate
 - **Task**: Subagent delegation with 5 specialized agent types — audit-scanner (Haiku, Pass 1), audit-analyzer (Sonnet, Pass 2), audit-comparator (Sonnet, Pass 3), audit-consolidator (Sonnet, reports), audit-validator (Sonnet, spot-check)
 
@@ -169,4 +169,6 @@ Runs all 3 passes sequentially with quality gates between each pass. Pass 1 inve
 - Final report (executive summary + prioritized actions)
 - progress.json (checkpoint state for resume capability)
 
+The final report of `--pass all` is `.claude-audit/final-report.md`. Except under `--unattended`: `<report-dir>/return-contract.yaml` is also written (see the Unattended mode section of the command file).
+
 **Next Step**: Use `/sc:cleanup` to execute safe recommendations, then `/sc:test` to verify no regressions, then `/sc:git` to commit changes.

diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index 1b262ce0..1847409a 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -305,6 +305,15 @@ UNATTENDED_EXPECT: dict = {
         "phrases": ["explicit"],
         "nested": [],
     },
+    "cleanup-audit": {
+        "flags": ["--pass"],
+        "phrases": [
+            ".claude-audit/final-report.md",
+            "progress.json",
+            "only one audit at a time",
+        ],
+        "nested": [],
+    },
 }
 
 # Commands with an `## Unattended mode` section after P1 (./source.md section 6
@@ -668,6 +677,19 @@ def test_unattended_section_check_fails_on_synthetic_defects(
         _check_unattended_section(mutate(good), ok)
 
 
+def test_cleanup_audit_names_final_report_and_contract_write_exception():
+    paths = (
+        Path(_THIS.COMMANDS_DIR) / "cleanup-audit.md",
+        _REPO / "src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md",
+    )
+    for path in paths:
+        text = path.read_text(encoding="utf-8")
+        assert ".claude-audit/final-report.md" in text, path.name
+        assert re.search(
+            r"Except under `--unattended`[^\n]*return-contract\.yaml", text
+        ), path.name
+
+
 def test_unattended_section_check_forbids_nested_text_without_a_nested_list():
     text = _SYNTHETIC_SECTION
     with pytest.raises(AssertionError):

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
