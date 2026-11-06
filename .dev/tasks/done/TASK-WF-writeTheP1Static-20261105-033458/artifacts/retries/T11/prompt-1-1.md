19fab1674b0a233f8debff1590e76c8830d996f8
Review one task for spec compliance.

Task brief: Task T11 (plan file /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md, lines 209-224); AC ids T11.AC1 to T11.AC3 are the bullets under `Acceptance criteria:` in source order.

## Task 11: Convert `/sc:test`, `/sc:explain` and `/sc:business-panel`: person-mode refusals, tools and frontmatter fixes

Depends on: Task 1

Files: `src/superclaude/commands/test.md`, `src/superclaude/commands/explain.md`, `src/superclaude/commands/business-panel.md` and `tests/skills/test_worker_contract.py`; spec section 3.2 rows test, explain and business-panel, and the person-mode refusal rule (spec section 2.1).

`test.md`: add the usage example line and the `--output` explanation line of Task 10 and the `## Unattended mode` section before `## Boundaries`: report directory `--report-dir <dir>` only; `--watch` is refused (it never ends); `report_path` is the `--output` file or `<report-dir>/test-report.md`, holding the coverage and test summary; a failing suite is a verdict in the report and the run still ends `succeeded` (D-P1-8), `failed` only when no runner could run; `--fix` is the caller's consent for non-destructive fixes only, and a destructive change to a test file (the command's "without explicit permission" line) is never made under `--unattended` (D-P1-12); no other gate; it pushes, commits and stages nothing. Entry: flags `--watch` and `--output`; phrases `test-report.md`, `verdict` and `destructive`.

`explain.md`: add the usage example line and the `--output` explanation line of Task 10 and the section before `## Boundaries`: `--format interactive` and `--format=interactive` are refused; the explanation is written to the `--output` file or `<report-dir>/explain-report.md` (named defect fix: add one line to "Tool Coordination" saying Write is used only for the explanation file under `--output` or `--unattended`); `report_path` is that file; no other gate. Entry: flags `--format interactive` and `--output`; phrases `explain-report.md` and `Write`. Add a test that `explain.md` has a bullet that starts with `- **Write**` under "Tool Coordination" (a plain substring test would be satisfied by the existing `TodoWrite` bullet).

`business-panel.md` (exempt from Check ADDITIVE): move the YAML frontmatter out of its code fence so the file starts with `---`, keeps the same keys and values, and has the `# /sc:business-panel` heading after the closing `---`; the effect on how Claude Code loads the command is UNVERIFIED (spec UNVERIFIED item 7) and is recorded in the static report. Add `--output <file>` to the "Output Options" list and the section before `## CRITICAL BOUNDARIES`: report directory `--report-dir <dir>` only; `--mode socratic` and `--mode=socratic` are refused, and `--mode adaptive` never selects the Socratic mode under `--unattended` (the word `adaptive` appears in the section); `report_path` is the `--output` file or `<report-dir>/business-panel-report.md`; no other gate. Entry: flags `--mode socratic` and `--output`; phrases `adaptive` and `business-panel-report.md`. Add a test that `business-panel.md` begins with `---` and has no yaml code fence (a line that starts with three backticks followed by `yaml`) before its first `## ` heading.

Acceptance criteria:
- [T11.AC1] `grep -c '^## Unattended mode$' src/superclaude/commands/test.md src/superclaude/commands/explain.md src/superclaude/commands/business-panel.md` prints `1` for each file, and `head -1 src/superclaude/commands/business-panel.md` prints `---`.
- [T11.AC2] `uv run pytest tests/skills/test_worker_contract.py tests/unit/test_cli_install.py tests/recommend/test_routing_refresh.py -q -p no:cacheprovider` passes with the three new entries and the two new tests.
- [T11.AC3] Check ADDITIVE prints nothing for `test.md` and `explain.md`; for `business-panel.md` `git diff --numstat` shows at most 4 deleted lines (the old heading line, the two code-fence lines and at most one blank line) and `git diff` shows the frontmatter keys and values unchanged byte for byte, including the trailing spaces on line 6; Check SCAN prints nothing.
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
Start sha: 19fab1674b0a233f8debff1590e76c8830d996f8
Diff against the start snapshot: diff --git a/src/superclaude/commands/test.md b/src/superclaude/commands/test.md
index 06c42433..cd4fd66e 100644
--- a/src/superclaude/commands/test.md
+++ b/src/superclaude/commands/test.md
@@ -20,8 +20,11 @@ personas: [qa-specialist]
 
 ```
 /sc:test [target] [--type unit|integration|e2e|all] [--coverage] [--watch] [--fix]
+/sc:test [target] [--output <file>] [--unattended] [--report-dir <dir>]
 ```
 
+`--output <file>` writes the test and coverage summary to that file. A standalone run writes a file only when you pass it.
+
 ## Behavioral Flow
 
 1. **Discover**: Categorize available tests using runner patterns and conventions
@@ -91,6 +94,18 @@ Key behaviors:
 # Real-time feedback during development
 ```
 
+## Unattended mode
+
+The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:test` resolves itself.
+
+- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
+- **Report directory.** `--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
+- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the `--output` file, or `<report-dir>/test-report.md`, holding the coverage and test summary. A failing suite is a verdict in that report and the run still ends succeeded; it ends failed only when no test runner could run.
+- **Person-mode flags.** `--watch` is refused before any work, because it never ends (contract `worker_status: failed`, the flag in `reason`).
+- **Gates.** There is no other gate. `--fix` is the caller's consent for non-destructive fixes only; a destructive change to a test file (the rule "without explicit permission") is never made under `--unattended`.
+- **Nested invocations.** None.
+- **Outward actions.** It pushes, commits and stages nothing.
+
 ## Boundaries
 
 **Will:**

diff --git a/src/superclaude/commands/explain.md b/src/superclaude/commands/explain.md
index 3b547f36..5b1cef90 100644
--- a/src/superclaude/commands/explain.md
+++ b/src/superclaude/commands/explain.md
@@ -20,8 +20,11 @@ personas: [educator, architect, security]
 
 ```
 /sc:explain [target] [--level basic|intermediate|advanced] [--format text|examples|interactive] [--context domain]
+/sc:explain [target] [--output <file>] [--unattended] [--report-dir <dir>]
 ```
 
+`--output <file>` writes the explanation to that file. A standalone run writes a file only when you pass it.
+
 ## Behavioral Flow
 
 1. **Analyze**: Examine target code, concept, or system for comprehensive understanding
@@ -47,6 +50,7 @@ Key behaviors:
 
 - **Read/Grep/Glob**: Code analysis and pattern identification for explanation content
 - **TodoWrite**: Progress tracking for complex multi-part explanations
+- **Write**: Used only for the explanation file under `--output` or `--unattended`
 - **Task**: Delegation for comprehensive explanation workflows requiring systematic breakdown
 - **Codegraph one-hop view** (code targets only, when codegraph is usable): `codegraph_search` (limit 10) to find the target symbol, then `codegraph_callers` and `codegraph_callees` (limit 10 each) for its direct callers and callees; Read every row before citing it, and use Read/Grep alone when codegraph is unusable. Codegraph usage rules: read `~/.claude/CODEGRAPH.md` (in a dev checkout without an install, the labelled fallback is `src/superclaude/core/CODEGRAPH.md`).
 
@@ -90,6 +94,17 @@ Key behaviors:
 # Framework-agnostic security principles with practical examples
 ```
 
+## Unattended mode
+
+The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:explain` resolves itself.
+
+- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
+- **Report directory.** `--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
+- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. The explanation is written to the `--output` file, or to `<report-dir>/explain-report.md` when `--output` is absent; Write is used only for that file. `report_path` is that file. The run is succeeded when the explanation is written, and failed otherwise.
+- **Person-mode flags.** `--format interactive` and `--format=interactive` are refused before any work (contract `worker_status: failed`, the flag in `reason`).
+- **Gates.** There is no other gate. Nested invocations: none.
+- **Outward actions.** It pushes, commits and stages nothing.
+
 ## Boundaries
 
 **Will:**

diff --git a/src/superclaude/commands/business-panel.md b/src/superclaude/commands/business-panel.md
index d96cf36f..9b04adb5 100644
--- a/src/superclaude/commands/business-panel.md
+++ b/src/superclaude/commands/business-panel.md
@@ -1,6 +1,3 @@
-# /sc:business-panel - Business Panel Analysis System
-
-```yaml
 ---
 command: "/sc:business-panel"
 category: "Analysis & Strategic Planning"  
@@ -8,7 +5,8 @@ purpose: "Multi-expert business analysis with adaptive interaction modes"
 wave-enabled: true
 performance-profile: "complex"
 ---
-```
+
+# /sc:business-panel - Business Panel Analysis System
 
 ## Overview
 
@@ -78,6 +76,7 @@ Question-driven exploration for deep learning and strategic thinking development
 - `--structured` - Use symbol system for efficiency
 - `--verbose` - Full detailed analysis
 - `--questions` - Focus on strategic questions
+- `--output <file>` - Write the analysis to that file (a standalone run writes a file only when you pass it)
 
 ## Auto-Persona Activation
 
@@ -91,6 +90,17 @@ Question-driven exploration for deep learning and strategic thinking development
 - Supports wave orchestration for comprehensive business analysis
 - Integrates with scribe persona for professional business communication
 
+## Unattended mode
+
+The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:business-panel` resolves itself.
+
+- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
+- **Report directory.** `--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
+- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the `--output` file, or `<report-dir>/business-panel-report.md` when `--output` is absent. The run is succeeded when the analysis document is written, and failed otherwise.
+- **Person-mode flags.** `--mode socratic` and `--mode=socratic` are refused before any work (contract `worker_status: failed`, the flag in `reason`). `--mode adaptive` never selects the Socratic mode under `--unattended`; it chooses between discussion and debate only.
+- **Gates.** There is no other gate. Nested invocations: none.
+- **Outward actions.** It pushes, commits and stages nothing.
+
 ## CRITICAL BOUNDARIES
 
 **SYNTHESIS OUTPUT ONLY - NOT IMPLEMENTATION**

diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index 78b11cbd..19b6324f 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -344,6 +344,21 @@ UNATTENDED_EXPECT: dict = {
         "phrases": ["design-report.md", "no gate", "consent is never given"],
         "nested": [],
     },
+    "test": {
+        "flags": ["--watch", "--output"],
+        "phrases": ["test-report.md", "verdict", "destructive"],
+        "nested": [],
+    },
+    "explain": {
+        "flags": ["--format interactive", "--output"],
+        "phrases": ["explain-report.md", "Write"],
+        "nested": [],
+    },
+    "business-panel": {
+        "flags": ["--mode socratic", "--output"],
+        "phrases": ["adaptive", "business-panel-report.md"],
+        "nested": [],
+    },
 }
 
 # Commands with an `## Unattended mode` section after P1 (./source.md section 6
@@ -739,6 +754,20 @@ def test_init_lite_contract_exception_and_pass_through_are_documented():
     assert "--unattended" in activation and "--report-dir" in activation
 
 
+def test_explain_declares_write_under_tool_coordination():
+    text = (Path(_THIS.COMMANDS_DIR) / "explain.md").read_text(encoding="utf-8")
+    tools = text.split("## Tool Coordination", 1)[1].split("\n## ", 1)[0]
+    # `TodoWrite` also contains "Write", so match the bullet itself.
+    assert any(ln.startswith("- **Write**") for ln in tools.splitlines())
+
+
+def test_business_panel_frontmatter_is_not_inside_a_code_fence():
+    text = (Path(_THIS.COMMANDS_DIR) / "business-panel.md").read_text(encoding="utf-8")
+    assert text.startswith("---\n")
+    head = text.split("\n## ", 1)[0]
+    assert not re.search(r"^```yaml", head, re.M)
+
+
 def test_unattended_section_check_forbids_nested_text_without_a_nested_list():
     text = _SYNTHETIC_SECTION
     with pytest.raises(AssertionError):

diff --git a/tests/recommend/test_routing_refresh.py b/tests/recommend/test_routing_refresh.py
index 428e5487..f9d2b8f5 100644
--- a/tests/recommend/test_routing_refresh.py
+++ b/tests/recommend/test_routing_refresh.py
@@ -581,13 +581,16 @@ def test_unmatched_cache_hints_are_consulted_then_rejected():
 
 
 def test_example_only_flags_are_not_declared_or_routed():
-    """T44: build --validate and cleanup --preview are examples; design has no --output."""
+    """T44: build --validate and cleanup --preview are examples; the guide never routes design --output."""
     for name, flag in (("build", "--validate"), ("cleanup", "--preview")):
         source = (_COMMANDS / f"{name}.md").read_text(encoding="utf-8")
         usage = _section(source, "## Usage", "\n## ")
         examples = _section(source, "## Examples", "\n## ")
         assert flag not in usage and flag in examples, name
-    assert "--output" not in (_COMMANDS / "design.md").read_text(encoding="utf-8")
+    # P1 gave design an optional `--output <file>` for the worker report file; the
+    # routing loop below still pins that the guide does not route it.
+    design = (_COMMANDS / "design.md").read_text(encoding="utf-8")
+    assert "--output" in _section(design, "## Usage", "\n## ")
     for route, flag in (
         ({"block": "other", "command": "sc:build"}, "--validate"),
         ({"block": "routing", "row": "cleanup"}, "--preview"),

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
