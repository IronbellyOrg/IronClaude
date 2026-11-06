9e7b92f95a016aa6491c1b7364c26a801810d0d0
Review one task for spec compliance.

Task brief: ## Task 7: Sync the dev copies, run the affected tests and lint, and compare the tree against its starting state

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6

Run `make sync-dev` and then `make verify-sync` from the repository root so the gitignored copies under `.claude/` match `src/superclaude/`. Then run `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_brainstorm_protocol.py tests/skills/test_worker_contract.py tests/skills/test_codegraph_adoption.py tests/skills/test_tier2_tavily_consistency.py tests/commands/test_routing_plugin_parity.py -q -p no:cacheprovider` and `make lint` (which runs `lint-architecture` and then `uv run ruff check .`). Save the outputs to `./artifacts/t7-sync.log`, `./artifacts/t7-pytest.log` and `./artifacts/t7-lint.log`, and save the output of `git status --porcelain` to `./artifacts/status-after.txt`. Append the line `exit=<status>` after each command's output in its log. Do not edit any source file in this task; it writes only the logs under `./artifacts/`. The status snapshot `./artifacts/status-after.txt` is the one non-log file it writes there, and `make sync-dev` rewrites the gitignored copies under `.claude/` (output, not edits).

Acceptance criteria:
- `./artifacts/t7-sync.log` shows `make sync-dev` and `make verify-sync` both exiting 0.
- `./artifacts/t7-pytest.log` shows the five test files passing with no failure, including `tests/skills/test_codegraph_adoption.py` and `tests/skills/test_tier2_tavily_consistency.py`, and `./artifacts/t7-lint.log` shows `make lint` exiting 0 with no new ruff finding in the two edited test files.
- Every line that is in `./artifacts/status-after.txt` and not in `./artifacts/status-before.txt` names one of the six files in Constraints or a path under this package's folder; no such line names a path under `.claude/` or `plugins/`; and every line of `./artifacts/status-before.txt` that names a path under `.dev/tasks/done/` is unchanged in `./artifacts/status-after.txt`.
Global constraints: ## Constraints

- Background: the P1 live check lc10 failed because the codebase-enrichment wave ran on `quality_tier: fallback_1` (the auggie tool was not available in the worker session) and wrote no `nested/analyze-1/` directory, while the live plan expected one. The owner decided on 2026-11-05 that the check wording was wrong, not the worker. The archived record is in `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/` (`artifacts/lc10-result.md`, `artifacts/p1-owner-decisions-20261105.md`); those files are read, never edited.
- This plan replaces two earlier plans for the same work, packages `TASK-WF-brainstormFixBri-20261106-001016` and `TASK-WF-brainstormFixBri-20261106-021737`. An independent review found the first not ready to run (its Task 6 wording decided the nested folder by `quality_tier`, its Task 7 status check could not pass on the current tree, and the owner rule was not fully pinned). A second review found that the second plan's live-check sentence required the folder whenever any `Skill`, `Agent` or `Task` call passed the flag text, so a `Task` prompt followed by an auggie or `fallback_1` scan would fail a correct run; the owner amended the brief's Part 4 on 2026-11-06 and this plan carries the amended text. Both earlier packages are left as they are.
- Edit only these six files: `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`, `src/superclaude/commands/brainstorm.md`, `tests/skills/test_brainstorm_protocol.py`, `tests/skills/test_worker_contract.py` and `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `make sync-dev` also rewrites the gitignored copies under `.claude/`; those are output, not edits, and are never staged.
- `src/superclaude/` is the source of truth. `plugins/superclaude/commands/brainstorm.md` is a copy that already differs from the `src` file, and no test requires the two to match (`tests/commands/test_routing_plugin_parity.py` covers only the `sc-recommend` skill). It is not edited. This is this plan's resolution of spec open item 8 for `brainstorm.md`. Task 7 confirms nothing under `plugins/` changed.
- No new text in the installed files (the skill, its refs, the command file) may name a `src/superclaude/` path or an Orca command; `tests/skills/test_worker_contract.py` (`_check_unattended_section`) fails on both.
- UV for every Python command: `uv run pytest ...`, `uv run python ...`. Test runs use `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`. No `superclaude install` (the owner updates the installed copies under `~/.claude/` later). No git commit, push, merge or PR.
- The edits reach the next live plan only after the owner commits and merges them; this plan does not commit.
- Open conflict, no change planned here: from phase P2 brainstorm's research enrichment also passes a nested report directory, and the research-deep fallback is itself a nested command. The corrected wording covers only the codebase-enrichment wave. This is an open conflict for the owner and the P2 live-plan author.
- Starting state: the working tree already holds uncommitted edits to `src/superclaude/cli/install_core.py` and `tests/cli/test_how_we_work_install.py` that are not part of this work, and a staged archive of the earlier live plan under `.dev/tasks/done/`. Task 1 records this state before any edit and Task 7 compares against it.
Start sha: 9e7b92f95a016aa6491c1b7364c26a801810d0d0
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/status-before.txt b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/status-after.txt
similarity index 99%
rename from .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/status-before.txt
rename to .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/status-after.txt
index 71a3a657..fdf0cb34 100644
--- a/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/status-before.txt
+++ b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/status-after.txt
@@ -1,3 +1,4 @@
+ M .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
 R  .dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/TASK-WF-p1LivePlanBrief-20261105-164506.md -> .dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/TASK-WF-p1LivePlanBrief-20261105-164506.md
 A  .dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/ac-1.3.md
 A  .dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/ac13-branch.txt
@@ -961,11 +962,17 @@ A  .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/TASK-WF-brainstormF
 A  .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/return-contract.yaml
 A  .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/source.md
  M src/superclaude/cli/install_core.py
+ M src/superclaude/commands/brainstorm.md
+ M src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
+ M src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
  M tests/cli/test_how_we_work_install.py
+ M tests/skills/test_brainstorm_protocol.py
+ M tests/skills/test_worker_contract.py
 ?? .dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-001016/
 ?? .dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-021737/
 ?? .dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-113538-20261106113956/
 ?? .dev/reflect/pre-TASK-WF-p1LivePlanBrief-20261105-164506-20261105165021/
 ?? .dev/reflect/pre-TASK-WF-p1LivePlanBrief-20261105-164506-20261105172548/
 ?? .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/
+?? .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/progress.md
 ?? docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-P1.md
diff --git a/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t7-lint.log b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t7-lint.log
new file mode 100644
index 00000000..7ca5fb44
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t7-lint.log
@@ -0,0 +1,161 @@
+🔍 Checking architecture policy compliance...
+
+=== Check 1/2: Bidirectional Command ↔ Skill Links ===
+  ✅ [Check 1]: adversarial → sc-adversarial-protocol
+  ✅ [Check 1]: auggie-review → sc-auggie-review-protocol
+  ✅ [Check 1]: brainstorm → sc-brainstorm-protocol
+  ✅ [Check 1]: cleanup-audit → sc-cleanup-audit-protocol
+  ✅ [Check 1]: cli-eval → sc-cli-eval-protocol
+  ✅ [Check 1]: cli-portify → sc-cli-portify-protocol
+  ✅ [Check 1]: graph → sc-graph-protocol
+  ✅ [Check 1]: impact → sc-impact-protocol
+  ✅ [Check 1]: implement → sc-implement-protocol
+  ✅ [Check 1]: init-lite → sc-init-lite-protocol
+  ✅ [Check 1]: issue → sc-issue-protocol
+  ✅ [Check 1]: pm → sc-pm-protocol
+  ✅ [Check 1]: post-release → sc-post-release-protocol
+  ✅ [Check 1]: pr-submit → sc-pr-submit-protocol
+  ✅ [Check 1]: recommend → sc-recommend (utility skill; no -protocol suffix)
+  ✅ [Check 1]: reflect → sc-reflect-protocol
+  ✅ [Check 1]: release-split → sc-release-split-protocol
+  ✅ [Check 1]: review-translation → sc-review-translation-protocol
+  ✅ [Check 1]: roadmap → sc-roadmap-protocol
+  ✅ [Check 1]: swarm-wizard → sc-swarm-wizard-protocol
+  ✅ [Check 1]: task → sc-task-protocol
+  ✅ [Check 1]: tasklist → sc-tasklist-protocol
+  ✅ [Check 1]: troubleshoot → sc-troubleshoot-protocol
+  ✅ [Check 1]: validate-roadmap → sc-validate-roadmap-protocol
+  ✅ [Check 1]: validate-tests → sc-validate-tests-protocol
+  ✅ [Check 1]: workflow → sc-workflow-protocol
+  ✅ [Check 2]: sc-adversarial-protocol ← adversarial.md
+  ✅ [Check 2]: sc-auggie-review-protocol ← auggie-review.md
+  ✅ [Check 2]: sc-brainstorm-protocol ← brainstorm.md
+  ✅ [Check 2]: sc-cleanup-audit-protocol ← cleanup-audit.md
+  ✅ [Check 2]: sc-cli-eval-protocol ← cli-eval.md
+  ✅ [Check 2]: sc-cli-portify-protocol ← cli-portify.md
+  ✅ [Check 2]: sc-graph-protocol ← graph.md
+  ✅ [Check 2]: sc-impact-protocol ← impact.md
+  ✅ [Check 2]: sc-implement-protocol ← implement.md
+  ✅ [Check 2]: sc-init-lite-protocol ← init-lite.md
+  ✅ [Check 2]: sc-issue-protocol ← issue.md
+  ✅ [Check 2]: sc-pm-protocol ← pm.md
+  ✅ [Check 2]: sc-post-release-protocol ← post-release.md
+  ✅ [Check 2]: sc-pr-submit-protocol ← pr-submit.md
+  ✅ [Check 2]: sc-reflect-protocol ← reflect.md
+  ✅ [Check 2]: sc-release-split-protocol ← release-split.md
+  ✅ [Check 2]: sc-review-translation-protocol ← review-translation.md
+  ✅ [Check 2]: sc-roadmap-protocol ← roadmap.md
+  ✅ [Check 2]: sc-swarm-wizard-protocol ← swarm-wizard.md
+  ✅ [Check 2]: sc-task-protocol ← task.md
+  ✅ [Check 2]: sc-tasklist-protocol ← tasklist.md
+  ✅ [Check 2]: sc-troubleshoot-protocol ← troubleshoot.md
+  ✅ [Check 2]: sc-validate-roadmap-protocol ← validate-roadmap.md
+  ✅ [Check 2]: sc-validate-tests-protocol ← validate-tests.md
+  ✅ [Check 2]: sc-workflow-protocol ← workflow.md
+
+=== Check 3/4: Command Size Limits ===
+  ⚠️  WARN [Check 3]: brainstorm.md (217 lines, warn threshold 200)
+  ⚠️  WARN [Check 3]: reflect.md (305 lines, warn threshold 200)
+  ⚠️  WARN [Check 3]: spawn.md (210 lines, warn threshold 200)
+  ⚠️  WARN [Check 3]: spec-panel.md (462 lines, warn threshold 200)
+  ⚠️  WARN [Check 3]: troubleshoot.md (215 lines, warn threshold 200)
+
+=== Check 6: Activation Section Present (for paired commands) ===
+  ✅ [Check 6]: adversarial.md has ## Activation
+  ✅ [Check 6]: auggie-review.md has ## Activation
+  ✅ [Check 6]: brainstorm.md has ## Activation
+  ✅ [Check 6]: cleanup-audit.md has ## Activation
+  ✅ [Check 6]: cli-eval.md has ## Activation
+  ✅ [Check 6]: cli-portify.md has ## Activation
+  ✅ [Check 6]: graph.md has ## Activation
+  ✅ [Check 6]: impact.md has ## Activation
+  ✅ [Check 6]: implement.md has ## Activation
+  ✅ [Check 6]: init-lite.md has ## Activation
+  ✅ [Check 6]: issue.md has ## Activation
+  ✅ [Check 6]: pm.md has ## Activation
+  ✅ [Check 6]: post-release.md has ## Activation
+  ✅ [Check 6]: pr-submit.md has ## Activation
+  ✅ [Check 6]: reflect.md has ## Activation
+  ✅ [Check 6]: release-split.md has ## Activation
+  ✅ [Check 6]: review-translation.md has ## Activation
+  ✅ [Check 6]: roadmap.md has ## Activation
+  ✅ [Check 6]: swarm-wizard.md has ## Activation
+  ✅ [Check 6]: task.md has ## Activation
+  ✅ [Check 6]: tasklist.md has ## Activation
+  ✅ [Check 6]: troubleshoot.md has ## Activation
+  ✅ [Check 6]: validate-roadmap.md has ## Activation
+  ✅ [Check 6]: validate-tests.md has ## Activation
+  ✅ [Check 6]: workflow.md has ## Activation
+
+=== Check 8: Skill Frontmatter Completeness ===
+  ✅ [Check 8]: sc-adversarial-protocol frontmatter complete
+  ✅ [Check 8]: sc-auggie-review-protocol frontmatter complete
+  ✅ [Check 8]: sc-brainstorm-protocol frontmatter complete
+  ✅ [Check 8]: sc-cleanup-audit-protocol frontmatter complete
+  ✅ [Check 8]: sc-cli-eval-protocol frontmatter complete
+  ✅ [Check 8]: sc-cli-portify-protocol frontmatter complete
+  ✅ [Check 8]: sc-graph-protocol frontmatter complete
+  ✅ [Check 8]: sc-impact-protocol frontmatter complete
+  ✅ [Check 8]: sc-implement-protocol frontmatter complete
+  ✅ [Check 8]: sc-init-lite-protocol frontmatter complete
+  ✅ [Check 8]: sc-issue-protocol frontmatter complete
+  ✅ [Check 8]: sc-pm-protocol frontmatter complete
+  ✅ [Check 8]: sc-post-release-protocol frontmatter complete
+  ✅ [Check 8]: sc-pr-submit-protocol frontmatter complete
+  ✅ [Check 8]: sc-reflect-protocol frontmatter complete
+  ✅ [Check 8]: sc-release-split-protocol frontmatter complete
+  ✅ [Check 8]: sc-review-translation-protocol frontmatter complete
+  ✅ [Check 8]: sc-roadmap-protocol frontmatter complete
+  ✅ [Check 8]: sc-swarm-wizard-protocol frontmatter complete
+  ✅ [Check 8]: sc-task-protocol frontmatter complete
+  ✅ [Check 8]: sc-tasklist-protocol frontmatter complete
+  ✅ [Check 8]: sc-troubleshoot-protocol frontmatter complete
+  ✅ [Check 8]: sc-validate-roadmap-protocol frontmatter complete
+  ✅ [Check 8]: sc-validate-tests-protocol frontmatter complete
+  ✅ [Check 8]: sc-workflow-protocol frontmatter complete
+
+=== Check 9: Protocol Naming Consistency ===
+  ✅ [Check 9]: sc:adversarial-protocol ends in -protocol
+  ✅ [Check 9]: sc:auggie-review-protocol ends in -protocol
+  ✅ [Check 9]: sc:brainstorm-protocol ends in -protocol
+  ✅ [Check 9]: sc:cleanup-audit-protocol ends in -protocol
+  ✅ [Check 9]: sc:cli-eval-protocol ends in -protocol
+  ✅ [Check 9]: sc-cli-portify-protocol ends in -protocol
+  ✅ [Check 9]: sc:graph-protocol ends in -protocol
+  ✅ [Check 9]: sc:impact-protocol ends in -protocol
+  ✅ [Check 9]: sc:implement-protocol ends in -protocol
+  ✅ [Check 9]: sc:init-lite-protocol ends in -protocol
+  ✅ [Check 9]: sc:issue-protocol ends in -protocol
+  ✅ [Check 9]: sc:pm-protocol ends in -protocol
+  ✅ [Check 9]: sc:post-release-protocol ends in -protocol
+  ✅ [Check 9]: sc:pr-submit-protocol ends in -protocol
+  ✅ [Check 9]: sc:reflect-protocol ends in -protocol
+  ✅ [Check 9]: sc:release-split-protocol ends in -protocol
+  ✅ [Check 9]: sc:review-translation-protocol ends in -protocol
+  ✅ [Check 9]: sc:roadmap-protocol ends in -protocol
+  ✅ [Check 9]: sc:swarm-wizard-protocol ends in -protocol
+  ✅ [Check 9]: sc:task-protocol ends in -protocol
+  ✅ [Check 9]: sc:tasklist-protocol ends in -protocol
+  ✅ [Check 9]: sc:troubleshoot-protocol ends in -protocol
+  ✅ [Check 9]: sc-validate-roadmap-protocol ends in -protocol
+  ✅ [Check 9]: sc:validate-tests-protocol ends in -protocol
+  ✅ [Check 9]: sc:workflow-protocol ends in -protocol
+
+=== Check 10: Workspace Suffix Blocklist ===
+  ✅ [Check 10]: no *-workspace directories under .claude/skills/
+
+=== Check 11: Contract Constant Anti-Duplication (Contract #5 + #8) ===
+  ✅ [Check 11]: no contract-constant duplications
+
+=== Checks 5/7: NEEDS DESIGN (skipped) ===
+  ℹ️  Check 5 (inline protocol detection) — pending design
+  ℹ️  Check 7 (activation references correct skill) — pending design
+
+=== Summary ===
+  Errors:   0
+  Warnings: 5
+  ✅ PASS — architecture policy compliant (5 warning(s))
+Running linter...
+uv run ruff check .
+All checks passed!
+exit=0
diff --git a/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t7-pytest.log b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t7-pytest.log
new file mode 100644
index 00000000..fe263498
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t7-pytest.log
@@ -0,0 +1,24 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 459 items
+
+tests/skills/test_brainstorm_protocol.py ...                             [  0%]
+tests/skills/test_worker_contract.py ................................... [  8%]
+........................................................................ [ 23%]
+........................................................................ [ 39%]
+........................................................................ [ 55%]
+........................................................................ [ 71%]
+........................................................................ [ 86%]
+.                                                                        [ 86%]
+tests/skills/test_codegraph_adoption.py ................................ [ 93%]
+..................                                                       [ 97%]
+tests/skills/test_tier2_tavily_consistency.py .....                      [ 98%]
+tests/commands/test_routing_plugin_parity.py .....                       [100%]
+
+============================= 459 passed in 0.77s ==============================
+exit=0
diff --git a/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t7-status-compare.txt b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t7-status-compare.txt
new file mode 100644
index 00000000..be7dafa9
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t7-status-compare.txt
@@ -0,0 +1,16 @@
+== new lines in status-after (not in status-before)
+ M .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
+ M src/superclaude/commands/brainstorm.md
+ M src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
+ M src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
+ M tests/skills/test_brainstorm_protocol.py
+ M tests/skills/test_worker_contract.py
+?? .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/progress.md
+== new lines naming .claude/ or plugins/ (expect 0)
+0
+== new lines outside the six files and the package (expect 0)
+0
+== .dev/tasks/done/ lines before vs after (expect identical)
+identical
+953
+== lines removed from before (for information)
diff --git a/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t7-sync.log b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t7-sync.log
new file mode 100644
index 00000000..c49e386a
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t7-sync.log
@@ -0,0 +1,227 @@
+🔄 Syncing src/superclaude/ → .claude/ for local development...
+✅ Sync complete.
+   Skills:    39 directories
+   Agents:    48 files
+   Commands:  46 files
+   Hooks:     13 files
+   Templates: 52 files
+exit=0
+🔍 Verifying src/superclaude/ ↔ .claude/ sync...
+
+=== Skills ===
+  ✅ ccsession-tag
+  ✅ confidence-check
+  ✅ operational-guide
+  ✅ prd
+  ✅ readme
+  ✅ roadmap
+  ✅ sc-adversarial-protocol
+  ✅ sc-auggie-review-protocol
+  ✅ sc-bare-review
+  ✅ sc-brainstorm-protocol
+  ✅ sc-cleanup-audit-protocol
+  ✅ sc-cli-eval-protocol
+  ✅ sc-cli-portify-protocol
+  ✅ sc-crash-recovery
+  ✅ sc-graph-protocol
+  ✅ sc-impact-protocol
+  ✅ sc-implement-protocol
+  ✅ sc-init-lite-protocol
+  ✅ sc-issue-protocol
+  ✅ sc-pm-protocol
+  ✅ sc-post-release-protocol
+  ✅ sc-pr-submit-protocol
+  ✅ sc-recommend
+  ✅ sc-reflect-protocol
+  ✅ sc-release-split-protocol
+  ✅ sc-review-translation-protocol
+  ✅ sc-roadmap-protocol
+  ✅ sc-swarm-wizard-protocol
+  ✅ sc-task-protocol
+  ✅ sc-tasklist-protocol
+  ✅ sc-troubleshoot-protocol
+  ✅ sc-validate-roadmap-protocol
+  ✅ sc-validate-tests-protocol
+  ✅ sc-workflow-protocol
+  ✅ task-builder
+  ✅ task
+  ✅ tdd
+  ✅ tech-reference
+  ✅ tech-research
+
+=== Agents ===
+  ✅ audit-analyzer.md
+  ✅ audit-comparator.md
+  ✅ audit-consolidator.md
+  ✅ audit-scanner.md
+  ✅ audit-validator.md
+  ✅ auggie-reviewer.md
+  ✅ backend-architect.md
+  ✅ business-panel-experts.md
+  ✅ confidence-calibrator.md
+  ✅ debate-orchestrator.md
+  ✅ deep-research-agent.md
+  ✅ deep-research.md
+  ✅ devops-architect.md
+  ✅ eval-docs-loader.md
+  ✅ eval-run-reporter.md
+  ✅ eval-suite-author.md
+  ✅ evidence-validator.md
+  ✅ frontend-architect.md
+  ✅ implement-retry-adviser.md
+  ✅ issue-worker-t1.md
+  ✅ issue-worker-t2.md
+  ✅ issue-worker-t3.md
+  ✅ learning-guide.md
+  ✅ merge-executor.md
+  ✅ performance-engineer.md
+  ✅ pm-agent.md
+  ✅ python-expert.md
+  ✅ quality-engineer.md
+  ✅ refactoring-expert.md
+  ✅ reflect-reviewer.md
+  ✅ repo-index.md
+  ✅ requirements-analyst.md
+  ✅ reuse-auditor.md
+  ✅ rf-analyst.md
+  ✅ rf-assembler.md
+  ✅ rf-qa-qualitative.md
+  ✅ rf-qa.md
+  ✅ rf-task-builder.md
+  ✅ rf-task-executor.md
+  ✅ rf-task-researcher.md
+  ✅ rf-team-lead.md
+  ✅ root-cause-analyst.md
+  ✅ security-engineer.md
+  ✅ self-review.md
+  ✅ socratic-mentor.md
+  ✅ system-architect.md
+  ✅ technical-writer.md
+  ✅ troubleshoot-analyst.md
+
+=== Commands ===
+  ✅ adversarial.md
+  ✅ agent.md
+  ✅ analyze.md
+  ✅ auggie-review.md
+  ✅ brainstorm.md
+  ✅ build.md
+  ✅ business-panel.md
+  ✅ cleanup-audit.md
+  ✅ cleanup.md
+  ✅ cli-eval.md
+  ✅ cli-portify.md
+  ✅ design.md
+  ✅ document.md
+  ✅ explain.md
+  ✅ git.md
+  ✅ graph.md
+  ✅ help.md
+  ✅ impact.md
+  ✅ implement.md
+  ✅ improve.md
+  ✅ index-repo.md
+  ✅ index.md
+  ✅ init-lite.md
+  ✅ issue.md
+  ✅ load.md
+  ✅ pm.md
+  ✅ post-release.md
+  ✅ pr-submit.md
+  ✅ recommend.md
+  ✅ reflect.md
+  ✅ release-split.md
+  ✅ research.md
+  ✅ review-translation.md
+  ✅ roadmap.md
+  ✅ save.md
+  ✅ spawn.md
+  ✅ spec-panel.md
+  ✅ swarm-wizard.md
+  ✅ task.md
+  ✅ tasklist.md
+  ✅ tdd.md
+  ✅ test.md
+  ✅ troubleshoot.md
+  ✅ validate-roadmap.md
+  ✅ validate-tests.md
+  ✅ workflow.md
+
+=== Hooks ===
+  ✅ auggie-flag-clear.sh
+  ✅ block-bare-python.sh
+  ✅ codegraph-session-start.sh
+  ✅ freshness-file-changed.sh
+  ✅ freshness-post-read.sh
+  ✅ freshness-pre-edit.sh
+  ✅ freshness-session-start.sh
+  ✅ freshness-subagent-start.sh
+  ✅ freshness-subagent-stop.sh
+  ✅ freshness-user-prompt.sh
+  ✅ reject-workspace-writes.sh
+  ✅ sc-recommend-phase0.sh
+  ✅ pragmatic-subagent.js
+
+=== Templates ===
+  ✅ workflow/05_prd_template.md
+  ✅ workflow/03_project_plan_template.md
+  ✅ workflow/03_component_authoring_template.md
+  ✅ workflow/00_mdtm_template_simple_task.md
+  ✅ workflow/01_mdtm_template_generic_task__gfdoc.md
+  ✅ workflow/06_architecture_proposal_template.md
+  ✅ workflow/02_mdtm_template_complex_task.md
+  ✅ workflow/04_feature_brief_template.md
+  ✅ workflow/changelog_template.md
+  ✅ workflow/01_mdtm_template_generic_task.md
+  ✅ workflow/99_mdtm_template_generic_task_old.md
+  ✅ documents/prd_template.md
+  ✅ documents/operational_guide_template.md
+  ✅ documents/GFxAI_Master_Documentation_Template.md
+  ✅ documents/tdd_template.md
+  ✅ documents/agent_template_analysis.md
+  ✅ documents/supplemental-doc-creation-checklist.md
+  ✅ documents/agent_template_qa.md
+  ✅ documents/skill_template.md
+  ✅ documents/roadmap_template.md
+  ✅ documents/agent_template_worker.md
+  ✅ documents/release-spec-template.md
+  ✅ documents/supplemental_doc_template.md
+  ✅ documents/technical_reference_template.md
+  ✅ documents/readme_template.md
+  ✅ modularization-template-review/qa-fix-summary_template.md
+  ✅ modularization-template-review/qa-task-research-alignment_report_template.md
+  ✅ modularization-template-review/analyst-synthesis-review_report_template.md
+  ✅ modularization-template-review/research-notes_template.md
+  ✅ modularization-template-review/synthetic-dnsp-finding.contract
+  ✅ modularization-template-review/INDEX.md
+  ✅ modularization-template-review/qa-task-validation-structure_report_template.md
+  ✅ modularization-template-review/qa-cross-source-contradictions_template.md
+  ✅ modularization-template-review/track-scope-map_template.md
+  ✅ modularization-template-review/claim-evidence-matrix_template.md
+  ✅ modularization-template-review/qa-inventory_report_template.md
+  ✅ modularization-template-review/analyst-coverage-matrix_template.md
+  ✅ modularization-template-review/codebase-research_template.md
+  ✅ modularization-template-review/analyst-completeness_report_template.md
+  ✅ modularization-template-review/analyst-gap-analysis_template.md
+  ✅ modularization-template-review/qa-lens_report_template.md
+  ✅ modularization-template-review/qa-consolidated-findings_template.md
+  ✅ modularization-template-review/qa-task-validation-b2_report_template.md
+  ✅ modularization-template-review/qa-research-gap_report_template.md
+  ✅ modularization-template-review/qa-research-evidence_report_template.md
+  ✅ modularization-template-review/qa-qualitative-operational_report_template.md
+  ✅ modularization-template-review/qa-qualitative-sufficiency_report_template.md
+  ✅ modularization-template-review/analyst-cross-validation_report_template.md
+  ✅ modularization-template-review/qa-acceptance-methodology-audit_template.md
+  ✅ modularization-template-review/pipeline-complete_report_template.md
+  ✅ modularization-template-review/qa-source-fidelity_template.md
+  ✅ modularization-template-review/qa-research-depth_report_template.md
+  ✅ modularization-template-review/web-research_template.md
+
+=== Installer Registration ===
+  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh and *.js
+
+=== Hooks Cross-Consistency ===
+  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes
+
+✅ All components in sync.
+exit=0
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
