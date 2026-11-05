b08410b60b9a3684301249967ce400cd0509a6c3
Review one task for spec compliance.

Task brief: ## Task 20: Add the CHANGELOG entry and sync the dev copies

Depends on: Task 18, Task 19

Insert the entry of source section 15 under `## [Unreleased]` in `CHANGELOG.md` (no package version bump, per the version note in source section 15). Run `make sync-dev` so `.claude/` mirrors the edited skill, refs, scripts and command (do not stage `.claude/`).

Acceptance criteria:
- `CHANGELOG.md` contains "### sc:pr-submit: merge-conflict detection and resolution (#305)" under `## [Unreleased]`; `pyproject.toml` version is unchanged.
- `make verify-sync` passes; `make lint` passes; `uv run ruff format --check src/ tests/` passes; `uv run pytest tests/pr_submit tests/unit/test_cli_install.py tests/commands -q` passes; outputs saved to `./artifacts/t20-checks.log`.
- `git status --porcelain` lists no staged `.claude/` path other than `.claude/settings.json`.
Global constraints: 
- The design in `./source.md` is the specification. Every section reference below (for example "source section 5.3") points into it. Where a task and the source disagree, the source wins; record the disagreement in the task's evidence.
- Never force-push, and never write a force flag after the words "git push" on any line of a `.md` or `.sh` file in `src/superclaude/skills/sc-pr-submit-protocol/` (the force-push scan in `tests/pr_submit/test_static_grep.py:758-776` covers every such file). The only push text is `git push origin <target_sha>:<HEAD_BRANCH>`; prohibitions are written in words.
- `push_parent_ok`, `evaluate_push_decision`, `push_fail_state`, `push_idempotency_key`, `needs_rebase` and every existing `transition()` edge in `src/superclaude/pr_submit/fsm.py` stay byte-identical (source section 6.1). `resolve_crash_window` in `recovery.py` keeps its signature and return value.
- T-N50: no `git` or `gh` token (regex `\bgh\b|\bgit\b`), docstrings and comments included, in `conflicts.py`, `fsm.py`, `ci.py`, `refs/state-machine.md`, `refs/loop-guard.md` and every other file in `CORE_PURE_FILES` (`tests/pr_submit/test_static_grep.py:37-51`).
- Installed primitives (`SKILL.md`, refs, scripts, `commands/pr-submit.md`) never name a `src/superclaude/` path in new text.
- Every `gh` call in new text carries `--repo "$REPO"` or a `repos/<owner/repo>/` path. Nothing contacts `SuperClaude-Org/SuperClaude_Framework`.
- Never stash, never use a hook-skipping flag, never amend, never stage everything; stage exact paths only.
- `SKILL.md` keeps exactly one python code block (`tests/pr_submit/test_cosmos_protocol.py:36`, `tests/pr_submit/test_codex_reviews.py:688`) and grows by at most 15 lines (source section 8.1).
- Edit `src/superclaude/`, then run `make sync-dev`; never stage `.claude/` paths except `.claude/settings.json`. `.dev/tasks/` is always staged (`git add .dev/tasks`), including this package and its `artifacts/`.
- Python through UV only (`uv run pytest ...`, `uv run python ...`). Run the tests each task names plus `tests/pr_submit/`, `tests/unit/test_cli_install.py` and `tests/commands/`; do not run the full suite (`make test`) or `tests/cli/eval/` as a directory (orchestrator brief; this overrides the `make test` step of source section 12.5).
- Real-git tests run only inside pytest temporary directories with a local bare repository as `origin`, a `gh` stub on `PATH`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, and for real `uv` `UV_OFFLINE=1`, `UV_NO_CONFIG=1`, `UV_CACHE_DIR=<tmp>` (source section 12 preamble). No test touches the network or `~/.claude`.
- Out of scope: P3 late re-sync (#361) and the post-release verification follow-ups V1 to V8 of source section 14; they are not implemented by this plan.
- Task evidence (test logs, grep output) goes under `./artifacts/` in this package.
Start sha: b08410b60b9a3684301249967ce400cd0509a6c3
Diff against the start snapshot: diff --git a/CHANGELOG.md b/CHANGELOG.md
index e18e86ad..d7dff412 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -4,6 +4,25 @@ All notable changes to IronClaude are documented in this file.
 
 ## [Unreleased]
 
+### sc:pr-submit: merge-conflict detection and resolution (#305)
+
+#### Added (pr-submit conflicts)
+
+- At `--monitor 1` and above, the end of Wave 0 checks for a git operation in progress (halts `foreign_op_in_progress`), reads GitHub's `mergeable`, and only on a conflict runs a read-only local probe (`git merge-tree --write-tree`) that classifies every conflicted path into a tier and prints the plan before any edit.
+- Tier 1: a conflicted root `uv.lock` is regenerated with `uv lock` at Wave 8 entry and published as one merge commit of the recorded base tip, pushed fast-forward (never forced). It spends no review round, re-triggers no reviewer, is counted in the new `sync_push_count`, and the CI wait then expects checks on the new head (`expect_checks`), so an empty check list right after the push is no longer read as clean.
+- Tier 2 (off by default): text and tree conflicts resolved by stated intent before the first review, with a per-file resolution record, an `evidence-validator` grounding check, full tests, a reviewer re-trigger and one round. Enable with `--conflict-max-tier 2`.
+- Tier 3 (submodule, symlink, mode change, protected or migration path, binary, lock or generated file without a rule, more than 8 text files, anything unclassifiable) halts at the end of Wave 0 at L3 with nothing touched, and is reported at L1 and L2.
+- New flag `--conflict-max-tier {0,1,2}` (default 1); 0 detects and reports only.
+- New core module `superclaude.pr_submit.conflicts`, refs `conflict-mechanical.md` and `conflict-intent.md`, scripts `probe-merge.sh`, `finish-merge.sh` and `collect-conflict-evidence.sh`, and `poll-ci-checks.sh --evidence-sha`.
+
+#### Changed (pr-submit conflicts)
+
+- At `--monitor 1` and above the create path no longer rebases or halts when the branch is behind its base; it reports how many commits behind. `--monitor 0` is unchanged.
+- Every push record carries a `kind` (`fix`, `merge`, `sync`, `ci`); `--resume` uses it, so a crashed CI or sync push resumes into the CI wait instead of the review re-trigger path. Old run-logs read as `fix`.
+- `push_count` counts fix, CI and Tier 2 merge pushes; Tier 1 sync pushes are in `sync_push_count`. The documented bound is `push_count <= max_rounds + 1`.
+- The run-log event enum has 43 members (`sync_started`, `sync_concluded`).
+- A PR that is still conflicting at Wave 8 with nothing pushed skips the CI wait (`pr_conflicting`) and ends `terminal_halted` instead of waiting for checks that GitHub will not run; a run that saw a conflict re-reads `mergeable` before claiming clean. Late re-sync during the CI wait is #361.
+
 ## [5.0.0] - 2026-11-02
 
 Major release: codegraph replaces codebase-memory-mcp and Serena, and several commands, flags and core files are removed. Read the [5.0.0 release notes](docs/releases/v5.0.0.md) for the breaking changes and upgrade steps. This is the first versioned section of this changelog; it covers every change since the package version was set to 4.3.5 (2026-06-04), which was never tagged.
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t20-checks.log b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t20-checks.log
new file mode 100644
index 00000000..cef3cdea
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t20-checks.log
@@ -0,0 +1,530 @@
+make test (VG-2) not run per orchestrator brief; the plan's Constraints restrict the run to tests/pr_submit, tests/unit/test_cli_install.py and tests/commands
+
+=== [1] make verify-sync ===
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
+EXIT: 0
+
+=== [2] make lint ===
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
+  ⚠️  WARN [Check 3]: brainstorm.md (201 lines, warn threshold 200)
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
+EXIT: 0
+
+=== [3] uv run ruff format --check src/ tests/ ===
+1189 files already formatted
+EXIT: 0
+
+=== [4] PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/pr_submit tests/unit/test_cli_install.py tests/commands tests/cli/reflect/test_contract_status_cli.py -q -p no:cacheprovider ===
+tests/pr_submit/test_troubleshoot_seed.py ....                           [ 85%]
+tests/pr_submit/test_validated_not_verified.py ...                       [ 85%]
+tests/pr_submit/test_validation_gate.py .........                        [ 85%]
+tests/unit/test_cli_install.py ......................................... [ 87%]
+.......................................................                  [ 90%]
+tests/commands/test_auggie_review_remediation_chain.py ............      [ 91%]
+tests/commands/test_auggie_review_revagent.py ............               [ 91%]
+tests/commands/test_graph_command.py ................................... [ 93%]
+...............                                                          [ 94%]
+tests/commands/test_help_command.py ......                               [ 94%]
+tests/commands/test_impact_command.py .................................. [ 96%]
+.............................................                            [ 98%]
+tests/commands/test_research_command.py ..                               [ 98%]
+tests/commands/test_routing_plugin_parity.py .....                       [ 98%]
+tests/commands/test_workflow_command.py .................                [ 99%]
+tests/cli/reflect/test_contract_status_cli.py ........                   [100%]
+
+=============================== warnings summary ===============================
+tests/cli/reflect/test_contract_status_cli.py::test_contract_status_runs_without_tasklist
+  /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts/tests/cli/reflect/test_contract_status_cli.py:90: DeprecationWarning: 'isolated_filesystem' is deprecated and will be removed in Click 9.0. Use 'tempfile.TemporaryDirectory' or pytest's 'tmp_path' fixture with absolute paths instead.
+    with cli_runner.isolated_filesystem():
+
+tests/cli/reflect/test_contract_status_cli.py::test_contract_status_does_not_launch_reflect_audit_machinery
+  /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts/tests/cli/reflect/test_contract_status_cli.py:109: DeprecationWarning: 'isolated_filesystem' is deprecated and will be removed in Click 9.0. Use 'tempfile.TemporaryDirectory' or pytest's 'tmp_path' fixture with absolute paths instead.
+    with cli_runner.isolated_filesystem():
+
+tests/cli/reflect/test_contract_status_cli.py::test_contract_status_validate_does_not_write_lock_by_default
+  /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts/tests/cli/reflect/test_contract_status_cli.py:133: DeprecationWarning: 'isolated_filesystem' is deprecated and will be removed in Click 9.0. Use 'tempfile.TemporaryDirectory' or pytest's 'tmp_path' fixture with absolute paths instead.
+    with cli_runner.isolated_filesystem() as fs:
+
+tests/cli/reflect/test_contract_status_cli.py::test_contract_status_output_is_metadata_only
+  /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts/tests/cli/reflect/test_contract_status_cli.py:157: DeprecationWarning: 'isolated_filesystem' is deprecated and will be removed in Click 9.0. Use 'tempfile.TemporaryDirectory' or pytest's 'tmp_path' fixture with absolute paths instead.
+    with cli_runner.isolated_filesystem():
+
+tests/cli/reflect/test_contract_status_cli.py::test_contract_status_validate_output_redacts_raw_payload_body
+  /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts/tests/cli/reflect/test_contract_status_cli.py:259: DeprecationWarning: 'isolated_filesystem' is deprecated and will be removed in Click 9.0. Use 'tempfile.TemporaryDirectory' or pytest's 'tmp_path' fixture with absolute paths instead.
+    with cli_runner.isolated_filesystem() as fs:
+
+-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
+====================== 2015 passed, 5 warnings in 32.39s =======================
+EXIT: 0
+
+=== [5a] git diff --cached --name-only ===
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T1/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T1/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T10/notes.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T10/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T10/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T11/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T11/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T12/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T12/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T13/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T13/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T14/notes.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T14/probe-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T14/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T14/prompt-2-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T14/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T14/review-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T15/notes.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T15/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T15/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T16/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T16/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T17/notes.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T17/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T17/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T18/notes.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T18/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T18/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T19/notes.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T19/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T19/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T2/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T2/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T3/probe-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T3/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T3/prompt-2-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T3/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T3/review-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T4/notes.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T4/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T4/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T5/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T5/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T6/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T6/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T7/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T7/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T8/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T8/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T9/prompt-1-1.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/retries/T9/q0-head
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t1-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t10-grep.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t10-mode.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t10-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t11-grep.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t11-mode.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t11-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t12-grep.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t12-mode.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t12-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t13-diff.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t13-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t14-grep.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t14-pins.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t14-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t15-grep.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t15-pins.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t15-record-check.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t15-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t16-grep.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t16-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t16-usage-match.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t17-checks.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t17-diffstat.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t17-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t18-negative-check.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t18-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t19-cases.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t19-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t2-grep.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t2-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t3-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t4-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t5-fsm-diff.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t5-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t5-triad-pre-change.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t6-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t7-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t8-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t9-exports.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t9-import.txt
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t9-tests.log
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/progress.md
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/return-contract.yaml
+.dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md
+src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh
+src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh
+src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh
+EXIT: 0
+
+=== [5b] git status --porcelain | grep '\.claude/' ===
+EXIT (grep; 1 = no match): 1
+
+=== [5c] staged .claude/ paths other than .claude/settings.json ===
+EXIT (grep; 1 = none staged): 1

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
