8c7191b15d02a1a18dcfd3805d62b1706fa10317
Review one task for spec compliance.

Task brief: ## Task 10: Refresh the project mirrors and run the full gates

Depends on: Task 9

Run `make sync-dev` so the project mirrors receive the canonical changes (the mirrors stay gitignored and are never staged), then run the gates and save their output: `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_worker_agents.py tests/skills/test_worker_contract.py tests/commands/test_issue_command.py tests/cli/test_issue_body_templates.py -v` to `./artifacts/gate-focused.log`, then `make test` to `./artifacts/gate-test.log`, `make lint` to `./artifacts/gate-lint.log` and `make verify-sync` to `./artifacts/gate-verify-sync.log`. If `make test` fails on a test this change did not touch, record the test id and its failure on a clean `integration` checkout of the same test before calling it pre-existing; fix anything this change broke. Confirm the launch-level safeguards were not touched: no file under `src/superclaude/hooks/` and no `templates/launch-prompt.md` line appears in `git diff --name-only`.

Acceptance criteria:
- [T10.AC1] `make verify-sync` exits 0 after `make sync-dev`, and `git status --short` shows no path under the project mirror folders as a change to stage (only `src/`, `docs/`, `tests/` and `.dev/` paths appear).
- [T10.AC2] `make lint` exits 0, the focused five-file pytest command exits 0, and `make test` exits 0 or every failure is shown to be unrelated and pre-existing with its evidence in `./artifacts/gate-test.log`.
- [T10.AC3] `grep -rn "new material or a contradiction" src/ docs/` prints nothing (this search deliberately excludes `tests/`; Tasks 7 and 8 already require the same search over `tests/` to print nothing).
- [T10.AC4] `git diff --name-only` lists no path under `src/superclaude/hooks/` and no change to `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md`.
- [T10.AC5] The package `./artifacts/` holds the four gate logs and the Task 9 kit.
Global constraints: ## Constraints

- Base branch is `integration` (the issue text says `master`; that is stale). Edit only canonical sources under `src/superclaude/`, `docs/` and `tests/`. The generated project mirrors are refreshed only by `make sync-dev`, never edited by hand.
- Keep `AskUserQuestion` in the `allowed-tools` line of `src/superclaude/skills/sc-issue-protocol/SKILL.md` (pinned by `ALLOWED_TOOLS` in `tests/skills/test_issue_protocol.py:40`).
- Keep the full issue body never shown for approval (default B1), the post-create flag pushback comment (create Wave 5, `templates/create-review-comment.md`), the three required plan sections and their one shared rule sentence (`PLAN_SECTIONS_RULE`, `tests/skills/test_issue_worker_agents.py:34-39`), claim assignment, ClickUp, Orca, watcher and launch safeguards, the stage-claim recommendation skip from pull request 833, and the launched `worktree` agent's plan-approval boundary. None of these text blocks may change in meaning. Task 9 and Task 10 each carry a check that the launch-level safeguards stay untouched.
- Lines of `src/superclaude/skills/sc-issue-protocol/refs/create.md` that `tests/skills/test_worker_contract.py` pins verbatim (the GitHub-write rule paragraph near line 9, the lookup paragraph near line 20 and step 6 of Wave 5 near line 95) must stay byte-identical. SKILL.md step 6 of create mode (line 103) is also pinned there; Task 4 updates that pinned copy together with the line.
- Do not add a new return-contract field, flag, script, agent or dependency to the product. The classification is instruction text plus tests, as the current rule is. The kit of Task 9 is evidence tooling under this package's `./artifacts/`, not product code.
- A contradiction counts only with all three parts: its category, the user's own words (a quote from `description.md` or a flag passed on the command line), and the conflicting evidence (draft text, or a verified `path:line` of code the worker read). A line missing any part is New material. `None` is the empty marker, never an item, and a notes file with `- None` under both headings is the same state as empty notes.
- The changed-flag category means the drafted issue itself would not honor a flag the user passed (for example it would be filed with another mode or type). A worker's disagreement with a user-supplied flag is not a contradiction when the issue is filed with the user's flag; it stays a pushback comment.
- When an addition is also the only evidence for a contradiction, it is listed under Contradictions, and "keep my wording" removes only that content; every other New material item stays.
- The session that carries out this plan is a launched session whose guard refuses the installer for the whole tool, a child agent session, a Skill call to the issue protocol and any Bash text that names the GitHub CLI together with `issue` or `api`. No task here runs a create flow, starts a child session or runs `superclaude install`. Task 9 therefore prepares a kit and leaves the controlled runs to a person, and the final report calls the plan partial until that run fills the matrix.
Start sha: 8c7191b15d02a1a18dcfd3805d62b1706fa10317
Diff against the start snapshot: 
--- new untracked file .dev/tasks/to-do/TASK-WF-issueSummary-20261125-190451/artifacts/task10-checks.md (full contents) ---
# Task 10 checks (orchestrator evidence, run in the launched session)

Commands were run from the repository root after `make sync-dev` (output in `sync-dev.log`, exit 0).

## Gate results

- Focused five-file pytest command: 1012 passed, exit 0 (`gate-focused.log`, last lines).
- `make lint`: `All checks passed!`, exit 0 (`gate-lint.log`).
- `make verify-sync`: `All components in sync.`, exit 0 (`gate-verify-sync.log`).
- `make test`: 2 failed, 25184 passed, 69 skipped, exit 2 (`gate-test.log`). Both failures are in `tests/cli/eval/test_claude_process_adapter.py`, which this change does not touch; cause `No module named ruff` for the repo's `.venv` Python (see the note appended at the end of `gate-test.log`). Not proven on a clean integration checkout (the session's guard refuses a second worktree).

## Read-only checks

- `git status --short` after the sync lists only these changed tracked paths: `docs/designs/sc-issue-command.md`, `docs/user-guide/commands.md`, `src/superclaude/agents/issue-worker-t1.md`, `src/superclaude/agents/issue-worker-t2.md`, `src/superclaude/agents/issue-worker-t3.md`, `src/superclaude/commands/issue.md`, `src/superclaude/skills/sc-issue-protocol/SKILL.md`, `src/superclaude/skills/sc-issue-protocol/refs/create.md`, `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md`, `tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py`, `tests/skills/test_worker_contract.py`; untracked: `.dev/issues/834/`, `.dev/reflect/` run folders, `.dev/tasks/archive/TASK-WF-issueSummary-20261125-175321/`, `.dev/tasks/to-do/TASK-WF-issueSummary-20261125-190451/`. No path under the project mirror folders appears as a change.
- A search of `src/` and `docs/` for the whole old trigger phrase (the one in the plan's Task 10) printed nothing; the same search of `tests/` printed nothing.
- `git diff --name-only` lists no path under `src/superclaude/hooks/` and no change to `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md`.

--- new untracked file .dev/tasks/to-do/TASK-WF-issueSummary-20261125-190451/artifacts/gate-lint.log (full contents) ---
🔍 Checking architecture policy compliance...

=== Check 1/2: Bidirectional Command ↔ Skill Links ===
  ✅ [Check 1]: adversarial → sc-adversarial-protocol
  ✅ [Check 1]: auggie-review → sc-auggie-review-protocol
  ✅ [Check 1]: brainstorm → sc-brainstorm-protocol
  ✅ [Check 1]: cleanup-audit → sc-cleanup-audit-protocol
  ✅ [Check 1]: cli-eval → sc-cli-eval-protocol
  ✅ [Check 1]: closeout → sc-closeout-protocol
  ✅ [Check 1]: graph → sc-graph-protocol
  ✅ [Check 1]: impact → sc-impact-protocol
  ✅ [Check 1]: implement → sc-implement-protocol
  ✅ [Check 1]: init-lite → sc-init-lite-protocol
  ✅ [Check 1]: issue → sc-issue-protocol
  ✅ [Check 1]: pm → sc-pm-protocol
  ✅ [Check 1]: post-release → sc-post-release-protocol
  ✅ [Check 1]: pr-submit → sc-pr-submit-protocol
  ✅ [Check 1]: recommend → sc-recommend (utility skill; no -protocol suffix)
  ✅ [Check 1]: reflect → sc-reflect-protocol
  ✅ [Check 1]: release-split → sc-release-split-protocol
  ✅ [Check 1]: swarm-wizard → sc-swarm-wizard-protocol
  ✅ [Check 1]: sweep → sc-sweep-protocol
  ✅ [Check 1]: task → sc-task-protocol
  ✅ [Check 1]: troubleshoot → sc-troubleshoot-protocol
  ✅ [Check 1]: validate-tests → sc-validate-tests-protocol
  ✅ [Check 1]: workflow → sc-workflow-protocol
  ✅ [Check 2]: sc-adversarial-protocol ← adversarial.md
  ✅ [Check 2]: sc-auggie-review-protocol ← auggie-review.md
  ✅ [Check 2]: sc-brainstorm-protocol ← brainstorm.md
  ✅ [Check 2]: sc-cleanup-audit-protocol ← cleanup-audit.md
  ✅ [Check 2]: sc-cli-eval-protocol ← cli-eval.md
  ✅ [Check 2]: sc-closeout-protocol ← closeout.md
  ✅ [Check 2]: sc-graph-protocol ← graph.md
  ✅ [Check 2]: sc-impact-protocol ← impact.md
  ✅ [Check 2]: sc-implement-protocol ← implement.md
  ✅ [Check 2]: sc-init-lite-protocol ← init-lite.md
  ✅ [Check 2]: sc-issue-protocol ← issue.md
  ✅ [Check 2]: sc-pm-protocol ← pm.md
  ✅ [Check 2]: sc-post-release-protocol ← post-release.md
  ✅ [Check 2]: sc-pr-submit-protocol ← pr-submit.md
  ✅ [Check 2]: sc-reflect-protocol ← reflect.md
  ✅ [Check 2]: sc-release-split-protocol ← release-split.md
  ✅ [Check 2]: sc-swarm-wizard-protocol ← swarm-wizard.md
  ✅ [Check 2]: sc-sweep-protocol ← sweep.md
  ✅ [Check 2]: sc-task-protocol ← task.md
  ✅ [Check 2]: sc-troubleshoot-protocol ← troubleshoot.md
  ✅ [Check 2]: sc-validate-tests-protocol ← validate-tests.md
  ✅ [Check 2]: sc-workflow-protocol ← workflow.md

=== Check 3/4: Command Size Limits ===
  ⚠️  WARN [Check 3]: brainstorm.md (214 lines, warn threshold 200)
  ⚠️  WARN [Check 3]: reflect.md (315 lines, warn threshold 200)
  ⚠️  WARN [Check 3]: spec-panel.md (488 lines, warn threshold 200)
  ⚠️  WARN [Check 3]: troubleshoot.md (226 lines, warn threshold 200)

=== Check 6: Activation Section Present (for paired commands) ===
  ✅ [Check 6]: adversarial.md has ## Activation
  ✅ [Check 6]: auggie-review.md has ## Activation
  ✅ [Check 6]: brainstorm.md has ## Activation
  ✅ [Check 6]: cleanup-audit.md has ## Activation
  ✅ [Check 6]: cli-eval.md has ## Activation
  ✅ [Check 6]: closeout.md has ## Activation
  ✅ [Check 6]: graph.md has ## Activation
  ✅ [Check 6]: impact.md has ## Activation
  ✅ [Check 6]: implement.md has ## Activation
  ✅ [Check 6]: init-lite.md has ## Activation
  ✅ [Check 6]: issue.md has ## Activation
  ✅ [Check 6]: pm.md has ## Activation
  ✅ [Check 6]: post-release.md has ## Activation
  ✅ [Check 6]: pr-submit.md has ## Activation
  ✅ [Check 6]: reflect.md has ## Activation
  ✅ [Check 6]: release-split.md has ## Activation
  ✅ [Check 6]: swarm-wizard.md has ## Activation
  ✅ [Check 6]: sweep.md has ## Activation
  ✅ [Check 6]: task.md has ## Activation
  ✅ [Check 6]: troubleshoot.md has ## Activation
  ✅ [Check 6]: validate-tests.md has ## Activation
  ✅ [Check 6]: workflow.md has ## Activation

=== Check 8: Skill Frontmatter Completeness ===
  ✅ [Check 8]: sc-adversarial-protocol frontmatter complete
  ✅ [Check 8]: sc-auggie-review-protocol frontmatter complete
  ✅ [Check 8]: sc-brainstorm-protocol frontmatter complete
  ✅ [Check 8]: sc-cleanup-audit-protocol frontmatter complete
  ✅ [Check 8]: sc-cli-eval-protocol frontmatter complete
  ✅ [Check 8]: sc-closeout-protocol frontmatter complete
  ✅ [Check 8]: sc-graph-protocol frontmatter complete
  ✅ [Check 8]: sc-impact-protocol frontmatter complete
  ✅ [Check 8]: sc-implement-protocol frontmatter complete
  ✅ [Check 8]: sc-init-lite-protocol frontmatter complete
  ✅ [Check 8]: sc-issue-protocol frontmatter complete
  ✅ [Check 8]: sc-pm-protocol frontmatter complete
  ✅ [Check 8]: sc-post-release-protocol frontmatter complete
  ✅ [Check 8]: sc-pr-submit-protocol frontmatter complete
  ✅ [Check 8]: sc-reflect-protocol frontmatter complete
  ✅ [Check 8]: sc-release-split-protocol frontmatter complete
  ✅ [Check 8]: sc-swarm-wizard-protocol frontmatter complete
  ✅ [Check 8]: sc-sweep-protocol frontmatter complete
  ✅ [Check 8]: sc-task-protocol frontmatter complete
  ✅ [Check 8]: sc-troubleshoot-protocol frontmatter complete
  ✅ [Check 8]: sc-validate-tests-protocol frontmatter complete
  ✅ [Check 8]: sc-workflow-protocol frontmatter complete

=== Check 9: Protocol Naming Consistency ===
  ✅ [Check 9]: sc:adversarial-protocol ends in -protocol
  ✅ [Check 9]: sc:auggie-review-protocol ends in -protocol
  ✅ [Check 9]: sc:brainstorm-protocol ends in -protocol
  ✅ [Check 9]: sc:cleanup-audit-protocol ends in -protocol
  ✅ [Check 9]: sc:cli-eval-protocol ends in -protocol
  ✅ [Check 9]: sc:closeout-protocol ends in -protocol
  ✅ [Check 9]: sc:graph-protocol ends in -protocol
  ✅ [Check 9]: sc:impact-protocol ends in -protocol
  ✅ [Check 9]: sc:implement-protocol ends in -protocol
  ✅ [Check 9]: sc:init-lite-protocol ends in -protocol
  ✅ [Check 9]: sc:issue-protocol ends in -protocol
  ✅ [Check 9]: sc:pm-protocol ends in -protocol
  ✅ [Check 9]: sc:post-release-protocol ends in -protocol
  ✅ [Check 9]: sc:pr-submit-protocol ends in -protocol
  ✅ [Check 9]: sc:reflect-protocol ends in -protocol
  ✅ [Check 9]: sc:release-split-protocol ends in -protocol
  ✅ [Check 9]: sc:swarm-wizard-protocol ends in -protocol
  ✅ [Check 9]: sc:sweep-protocol ends in -protocol
  ✅ [Check 9]: sc:task-protocol ends in -protocol
  ✅ [Check 9]: sc:troubleshoot-protocol ends in -protocol
  ✅ [Check 9]: sc:validate-tests-protocol ends in -protocol
  ✅ [Check 9]: sc:workflow-protocol ends in -protocol

=== Check 10: Workspace Suffix Blocklist ===
  ✅ [Check 10]: no *-workspace directories under .claude/skills/

=== Check 11: Contract Constant Anti-Duplication (Contract #5 + #8) ===
  ✅ [Check 11]: no contract-constant duplications

=== Checks 5/7: NEEDS DESIGN (skipped) ===
  ℹ️  Check 5 (inline protocol detection) — pending design
  ℹ️  Check 7 (activation references correct skill) — pending design

=== Summary ===
  Errors:   0
  Warnings: 4
  ✅ PASS — architecture policy compliant (4 warning(s))
Running linter...
uv run ruff check .
All checks passed!
rc=0

--- new untracked file .dev/tasks/to-do/TASK-WF-issueSummary-20261125-190451/artifacts/gate-verify-sync.log (full contents) ---
🔍 Verifying src/superclaude/ ↔ .claude/ sync...

=== Skills ===
  ✅ ccsession-tag
  ✅ confidence-check
  ✅ sc-adversarial-protocol
  ✅ sc-auggie-review-protocol
  ✅ sc-bare-review
  ✅ sc-brainstorm-protocol
  ✅ sc-cleanup-audit-protocol
  ✅ sc-cli-eval-protocol
  ✅ sc-closeout-protocol
  ✅ sc-crash-recovery
  ✅ sc-graph-protocol
  ✅ sc-impact-protocol
  ✅ sc-implement-protocol
  ✅ sc-init-lite-protocol
  ✅ sc-issue-protocol
  ✅ sc-pm-protocol
  ✅ sc-post-release-protocol
  ✅ sc-pr-submit-protocol
  ✅ sc-recommend
  ✅ sc-reflect-protocol
  ✅ sc-release-split-protocol
  ✅ sc-swarm-wizard-protocol
  ✅ sc-sweep-protocol
  ✅ sc-task-protocol
  ✅ sc-troubleshoot-protocol
  ✅ sc-validate-tests-protocol
  ✅ sc-workflow-protocol

=== Agents ===
  ✅ audit-analyzer.md
  ✅ audit-comparator.md
  ✅ audit-consolidator.md
  ✅ audit-scanner.md
  ✅ audit-validator.md
  ✅ auggie-reviewer.md
  ✅ backend-architect.md
  ✅ business-panel-experts.md
  ✅ confidence-calibrator.md
  ✅ debate-orchestrator.md
  ✅ deep-research-agent.md
  ✅ deep-research.md
  ✅ devops-architect.md
  ✅ eval-docs-loader.md
  ✅ eval-run-reporter.md
  ✅ eval-suite-author.md
  ✅ evidence-validator.md
  ✅ frontend-architect.md
  ✅ implement-retry-adviser.md
  ✅ issue-worker-t1.md
  ✅ issue-worker-t2.md
  ✅ issue-worker-t3.md
  ✅ learning-guide.md
  ✅ merge-executor.md
  ✅ performance-engineer.md
  ✅ pm-agent.md
  ✅ python-expert.md
  ✅ quality-engineer.md
  ✅ refactoring-expert.md
  ✅ reflect-reviewer.md
  ✅ repo-index.md
  ✅ requirements-analyst.md
  ✅ reuse-auditor.md
  ✅ rf-analyst.md
  ✅ rf-assembler.md
  ✅ rf-qa-qualitative.md
  ✅ rf-qa.md
  ✅ rf-task-builder.md
  ✅ rf-task-executor.md
  ✅ rf-task-researcher.md
  ✅ rf-team-lead.md
  ✅ root-cause-analyst.md
  ✅ security-engineer.md
  ✅ self-review.md
  ✅ socratic-mentor.md
  ✅ system-architect.md
  ✅ technical-writer.md
  ✅ troubleshoot-analyst.md
  ✅ workflow-reviser.md

=== Commands ===
  ✅ adversarial.md
  ✅ agent.md
  ✅ analyze.md
  ✅ auggie-review.md
  ✅ brainstorm.md
  ✅ business-panel.md
  ✅ cleanup-audit.md
  ✅ cleanup.md
  ✅ cli-eval.md
  ✅ closeout.md
  ✅ design.md
  ✅ document.md
  ✅ explain.md
  ✅ git.md
  ✅ graph.md
  ✅ help.md
  ✅ impact.md
  ✅ implement.md
  ✅ init-lite.md
  ✅ issue.md
  ✅ pm.md
  ✅ post-release.md
  ✅ pr-submit.md
  ✅ recommend.md
  ✅ reflect.md
  ✅ release-split.md
  ✅ research.md
  ✅ spec-panel.md
  ✅ swarm-wizard.md
  ✅ sweep.md
  ✅ task.md
  ✅ test.md
  ✅ troubleshoot.md
  ✅ validate-tests.md
  ✅ workflow.md
  ✅ worktrees.md

=== Hooks ===
  ✅ auggie-flag-clear.sh
  ✅ block-bare-python.sh
  ✅ codegraph-session-start.sh
  ✅ freshness-file-changed.sh
  ✅ freshness-post-read.sh
  ✅ freshness-pre-edit.sh
  ✅ freshness-session-start.sh
  ✅ freshness-subagent-start.sh
  ✅ freshness-subagent-stop.sh
  ✅ freshness-user-prompt.sh
  ✅ launch-job-identity.sh
  ✅ launch-level-guard.sh
  ✅ launch-level-pre-push.sh
  ✅ reject-workspace-writes.sh
  ✅ require-orca-worktree-agent.sh
  ✅ sc-recommend-phase0.sh
  ✅ pragmatic-subagent.js

=== Templates ===
  ✅ workflow/05_prd_template.md
  ✅ workflow/03_project_plan_template.md
  ✅ workflow/03_component_authoring_template.md
  ✅ workflow/00_mdtm_template_simple_task.md
  ✅ workflow/01_mdtm_template_generic_task__gfdoc.md
  ✅ workflow/06_architecture_proposal_template.md
  ✅ workflow/02_mdtm_template_complex_task.md
  ✅ workflow/04_feature_brief_template.md
  ✅ workflow/changelog_template.md
  ✅ workflow/01_mdtm_template_generic_task.md
  ✅ workflow/99_mdtm_template_generic_task_old.md
  ✅ documents/prd_template.md
  ✅ documents/operational_guide_template.md
  ✅ documents/GFxAI_Master_Documentation_Template.md
  ✅ documents/tdd_template.md
  ✅ documents/agent_template_analysis.md
  ✅ documents/supplemental-doc-creation-checklist.md
  ✅ documents/agent_template_qa.md
  ✅ documents/skill_template.md
  ✅ documents/roadmap_template.md
  ✅ documents/agent_template_worker.md
  ✅ documents/release-spec-template.md
  ✅ documents/supplemental_doc_template.md
  ✅ documents/technical_reference_template.md
  ✅ documents/readme_template.md
  ✅ modularization-template-review/qa-fix-summary_template.md
  ✅ modularization-template-review/qa-task-research-alignment_report_template.md
  ✅ modularization-template-review/analyst-synthesis-review_report_template.md
  ✅ modularization-template-review/research-notes_template.md
  ✅ modularization-template-review/synthetic-dnsp-finding.contract
  ✅ modularization-template-review/INDEX.md
  ✅ modularization-template-review/qa-task-validation-structure_report_template.md
  ✅ modularization-template-review/qa-cross-source-contradictions_template.md
  ✅ modularization-template-review/track-scope-map_template.md
  ✅ modularization-template-review/claim-evidence-matrix_template.md
  ✅ modularization-template-review/qa-inventory_report_template.md
  ✅ modularization-template-review/analyst-coverage-matrix_template.md
  ✅ modularization-template-review/codebase-research_template.md
  ✅ modularization-template-review/analyst-completeness_report_template.md
  ✅ modularization-template-review/analyst-gap-analysis_template.md
  ✅ modularization-template-review/qa-lens_report_template.md
  ✅ modularization-template-review/qa-consolidated-findings_template.md
  ✅ modularization-template-review/qa-task-validation-b2_report_template.md
  ✅ modularization-template-review/qa-research-gap_report_template.md
  ✅ modularization-template-review/qa-research-evidence_report_template.md
  ✅ modularization-template-review/qa-qualitative-operational_report_template.md
  ✅ modularization-template-review/qa-qualitative-sufficiency_report_template.md
  ✅ modularization-template-review/analyst-cross-validation_report_template.md
  ✅ modularization-template-review/qa-acceptance-methodology-audit_template.md
  ✅ modularization-template-review/pipeline-complete_report_template.md
  ✅ modularization-template-review/qa-source-fidelity_template.md
  ✅ modularization-template-review/qa-research-depth_report_template.md
  ✅ modularization-template-review/web-research_template.md

=== Installer Registration ===
  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh and *.js

=== Hooks Cross-Consistency ===
  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes

✅ All components in sync.
rc=0

--- new untracked file .dev/tasks/to-do/TASK-WF-issueSummary-20261125-190451/artifacts/sync-dev.log (full contents) ---
🔄 Syncing src/superclaude/ → .claude/ for local development...
✅ Sync complete.
   Skills:    27 directories
   Agents:    49 files
   Commands:  36 files
   Hooks:     17 files
   Templates: 52 files


Codegraph context:
index_state=stale checked_at=2026-11-25T19:23:07Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-834 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-834
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor; dependents of the changed text that are not in this task's touched set are edited by later tasks of the plan.

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
