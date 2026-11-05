79243a519931e425388f4dc1b74c3018aaf2f6ac
Review one task for spec compliance.

Task brief: T5 (AC ids in order of the "Acceptance criteria:" bullets: T5.AC1,T5.AC2,T5.AC3). Plan file: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/TASK-WF-implementSavedPr-20261105-034852.md, lines 79-89:
## Task 5: Add tests/skills/test_implement_saved_prompt_rule.py and run the checks

Depends on: Task 4

Create `tests/skills/test_implement_saved_prompt_rule.py`. Its tests read the three refs from both `src/superclaude/skills/sc-implement-protocol/refs/` and `plugins/superclaude/skills/sc-implement-protocol/refs/` and fail when: `refs/qa.md` still contains "when they differ", or lacks "differs only in blank lines or trailing whitespace", "after the start-sha header", the heading "### Defective saved prompt (recovery)", "next unused `j` of the same `k`", "appends the task's `complete` line again", "moved unchanged" or "In a legacy run"; `refs/ledger.md` lacks "## Re-review complete line"; the line of `refs/managed-workspace.md` that begins "6. `pass` → run the helper" lacks "every `issues` item of the FINAL concerns a saved prompt", or `refs/managed-workspace.md` lacks "superseded-prompts/"; or any of the three files differs between the `src/` and `plugins/` copies. Then run `make sync-dev` once, `make verify-sync` and `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills -q -p no:cacheprovider`.

Acceptance criteria:
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_implement_saved_prompt_rule.py -q -p no:cacheprovider` passes (`./artifacts/t5-new-tests.txt`), and each test asserts on a phrase or byte comparison listed above.
- `make verify-sync` reports "All components in sync." (`./artifacts/t5-verify-sync.txt`), and `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills -q -p no:cacheprovider` shows no failures (`./artifacts/t5-pytest-skills.txt`; the baseline before this plan was 804 passed).
- `git diff --cached --name-only -- .claude` prints nothing (`./artifacts/t5-claude-staged.txt`), and `git status --porcelain -- docs src plugins tests`, saved as `./artifacts/t5-status-after.txt`, differs from `./artifacts/t1-status-before.txt` only by the three refs, their three `plugins/` twins and the new test file; in particular `tests/skills/test_implement_severity_static.py` has no entry.


Global constraints: (plan ## Constraints, .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/TASK-WF-implementSavedPr-20261105-034852.md lines 17-27)
## Constraints

- Rule changes go only in `src/superclaude/skills/sc-implement-protocol/refs/qa.md`, `src/superclaude/skills/sc-implement-protocol/refs/ledger.md` and `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md`, each with a byte-identical copy at the same relative path under `plugins/superclaude/skills/sc-implement-protocol/`. No other skill, command, agent or core file changes, and the reviewer template block (the fenced block that begins "Review one task for spec compliance." under "## Subagent prompt (when not inline)" in `refs/qa.md`) and the `ledger-grammar-block` fenced blocks in `refs/ledger.md` do not change.
- `tests/skills/test_implement_severity_static.py` is not modified. Its classification test fails on any line in the protocol files that matches the words `Ruling` (capital R), `halt`, `halts`, `halted`, `halting`, `E-HALT-QA` or `E-ARCHIVE-BLOCKED` and is not already listed there, so every new or rewritten line in the three refs avoids those words (say "a user-accepted gap" and "stop"), and additions to step 6 of `refs/managed-workspace.md` stay inside the existing single step-6 line. The existing wording "`issues` → STOP `E-ARCHIVE-BLOCKED`" stays verbatim.
- A prompt-builder script, any other lesson in `docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md`, and the globally installed copy of this skill (it changes when the user runs `superclaude install`) are out of scope.
- Never stage `.claude/` contents. `make sync-dev` copies `src/superclaude/` into `.claude/` only and does not touch `plugins/`, so each task copies its edited ref into the `plugins/` twin by hand, and Task 5 runs `make sync-dev` once after all edits to `src/superclaude/`.
- Installed primitives (the three refs above) must not tell an agent to read anything through a `src/superclaude/...` path.
- In `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/`, only the new file `artifacts/prompt-template-check.md` is added; its prompts, ledger and every other file stay byte-unchanged.
- Scripts and evidence for this plan go under this package's `./artifacts/`.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included. Staging is not committing; commit only when the user asks.


Start sha: 79243a519931e425388f4dc1b74c3018aaf2f6ac
Diff against the start snapshot: (git diff 79243a519931e425388f4dc1b74c3018aaf2f6ac -- src/superclaude/skills/sc-implement-protocol/refs/qa.md src/superclaude/skills/sc-implement-protocol/refs/ledger.md src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md plugins/superclaude/skills/sc-implement-protocol/refs/qa.md plugins/superclaude/skills/sc-implement-protocol/refs/ledger.md plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md tests/skills/test_implement_saved_prompt_rule.py, plus the task's new artifact files under .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/ listed after the diff)

=== new untracked file in the touched set: tests/skills/test_implement_saved_prompt_rule.py ===
"""Pin the saved-reviewer-prompt rules of the sc-implement-protocol refs.

Rule A: the comparison of a saved prompt with the reviewer template is stated once,
        in "## FINAL derived test", and a difference only in blank lines or trailing
        whitespace is a note.
Rule B: a defective saved prompt is recovered by a template-exact re-review and an
        unchanged move to superseded-prompts/, started from step 6 of the archive gate.
The plugin copy of each ref must stay byte-identical to the source copy.
"""

from __future__ import annotations

from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_SRC = _REPO / "src/superclaude/skills/sc-implement-protocol/refs"
_PLUGIN = _REPO / "plugins/superclaude/skills/sc-implement-protocol/refs"
_REFS = ("qa.md", "ledger.md", "managed-workspace.md")


def _read(root: Path, name: str) -> str:
    return (root / name).read_text(encoding="utf-8")


@pytest.fixture(params=[_SRC, _PLUGIN], ids=["src", "plugin"])
def root(request) -> Path:
    return request.param


def test_old_when_they_differ_wording_is_gone(root):
    assert "when they differ" not in _read(root, "qa.md")


@pytest.mark.parametrize(
    "phrase",
    [
        "differs only in blank lines or trailing whitespace",
        "after the start-sha header",
        "### Defective saved prompt (recovery)",
        "next unused `j` of the same `k`",
        "appends the task's `complete` line again",
        "moved unchanged",
        "In a legacy run",
        "is not a confirmed blocker",
    ],
)
def test_qa_has_rule_wording(root, phrase):
    assert phrase in _read(root, "qa.md"), phrase


def test_ledger_has_re_review_complete_line_section(root):
    assert "## Re-review complete line" in _read(root, "ledger.md")


def test_step_six_of_the_archive_gate_starts_the_recovery(root):
    lines = [
        line
        for line in _read(root, "managed-workspace.md").splitlines()
        if line.startswith("6. `pass` → run the helper")
    ]
    assert len(lines) == 1
    assert "every `issues` item of the FINAL concerns a saved prompt" in lines[0]
    assert "`issues` → STOP `E-ARCHIVE-BLOCKED`" in lines[0]


def test_managed_workspace_names_superseded_prompts(root):
    assert "superseded-prompts/" in _read(root, "managed-workspace.md")


@pytest.mark.parametrize("name", _REFS)
def test_plugin_copy_is_byte_identical_to_source(name):
    assert (_SRC / name).read_bytes() == (_PLUGIN / name).read_bytes(), name

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t1-status-before.txt ===
 M docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
M  docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t5-status-after.txt ===
 M docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
M  docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md
 M plugins/superclaude/skills/sc-implement-protocol/refs/ledger.md
 M plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
 M plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
 M src/superclaude/skills/sc-implement-protocol/refs/ledger.md
 M src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
 M src/superclaude/skills/sc-implement-protocol/refs/qa.md
?? tests/skills/test_implement_saved_prompt_rule.py

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t5-claude-staged.txt ===

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t5-new-tests.txt ===
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 4.3.5
rootdir: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs
configfile: pyproject.toml
plugins: superclaude-4.3.5, anyio-4.16.0
collected 27 items

tests/skills/test_implement_saved_prompt_rule.py ....................... [ 85%]
....                                                                     [100%]

============================== 27 passed in 0.14s ==============================

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t5-sync-dev.txt ===
🔄 Syncing src/superclaude/ → .claude/ for local development...
✅ Sync complete.
   Skills:    38 directories
   Agents:    45 files
   Commands:  45 files
   Hooks:     12 files
   Templates: 52 files

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t5-verify-sync.txt ===
🔍 Verifying src/superclaude/ ↔ .claude/ sync...

=== Skills ===
  ✅ ccsession-tag
  ✅ confidence-check
  ✅ operational-guide
  ✅ prd
  ✅ readme
  ✅ roadmap
  ✅ sc-adversarial-protocol
  ✅ sc-auggie-review-protocol
  ✅ sc-bare-review
  ✅ sc-brainstorm-protocol
  ✅ sc-cleanup-audit-protocol
  ✅ sc-cli-eval-protocol
  ✅ sc-cli-portify-protocol
  ✅ sc-crash-recovery
  ✅ sc-graph-protocol
  ✅ sc-impact-protocol
  ✅ sc-implement-protocol
  ✅ sc-init-lite-protocol
  ✅ sc-pm-protocol
  ✅ sc-post-release-protocol
  ✅ sc-pr-submit-protocol
  ✅ sc-recommend
  ✅ sc-reflect-protocol
  ✅ sc-release-split-protocol
  ✅ sc-review-translation-protocol
  ✅ sc-roadmap-protocol
  ✅ sc-swarm-wizard-protocol
  ✅ sc-task-protocol
  ✅ sc-tasklist-protocol
  ✅ sc-troubleshoot-protocol
  ✅ sc-validate-roadmap-protocol
  ✅ sc-validate-tests-protocol
  ✅ sc-workflow-protocol
  ✅ task-builder
  ✅ task
  ✅ tdd
  ✅ tech-reference
  ✅ tech-research

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

=== Commands ===
  ✅ adversarial.md
  ✅ agent.md
  ✅ analyze.md
  ✅ auggie-review.md
  ✅ brainstorm.md
  ✅ build.md
  ✅ business-panel.md
  ✅ cleanup-audit.md
  ✅ cleanup.md
  ✅ cli-eval.md
  ✅ cli-portify.md
  ✅ design.md
  ✅ document.md
  ✅ explain.md
  ✅ git.md
  ✅ graph.md
  ✅ help.md
  ✅ impact.md
  ✅ implement.md
  ✅ improve.md
  ✅ index-repo.md
  ✅ index.md
  ✅ init-lite.md
  ✅ load.md
  ✅ pm.md
  ✅ post-release.md
  ✅ pr-submit.md
  ✅ recommend.md
  ✅ reflect.md
  ✅ release-split.md
  ✅ research.md
  ✅ review-translation.md
  ✅ roadmap.md
  ✅ save.md
  ✅ spawn.md
  ✅ spec-panel.md
  ✅ swarm-wizard.md
  ✅ task.md
  ✅ tasklist.md
  ✅ tdd.md
  ✅ test.md
  ✅ troubleshoot.md
  ✅ validate-roadmap.md
  ✅ validate-tests.md
  ✅ workflow.md

=== Hooks ===
  ✅ auggie-flag-clear.sh
  ✅ codegraph-session-start.sh
  ✅ freshness-file-changed.sh
  ✅ freshness-post-read.sh
  ✅ freshness-pre-edit.sh
  ✅ freshness-session-start.sh
  ✅ freshness-subagent-start.sh
  ✅ freshness-subagent-stop.sh
  ✅ freshness-user-prompt.sh
  ✅ reject-workspace-writes.sh
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

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t5-pytest-skills.txt ===
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 4.3.5
rootdir: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs
configfile: pyproject.toml
plugins: superclaude-4.3.5, anyio-4.16.0
collected 831 items

tests/skills/test_brainstorm_protocol.py .                               [  0%]
tests/skills/test_codegraph_adoption.py ................................ [  3%]
..................                                                       [  6%]
tests/skills/test_implement_adviser_family.py ...                        [  6%]
tests/skills/test_implement_retry_citation.py .....................      [  9%]
tests/skills/test_implement_retry_revert.py ............................ [ 12%]
..........................                                               [ 15%]
tests/skills/test_implement_saved_prompt_rule.py ....................... [ 18%]
....                                                                     [ 18%]
tests/skills/test_implement_severity_replay.py ............              [ 20%]
tests/skills/test_implement_severity_static.py ......................... [ 23%]
...                                                                      [ 23%]
tests/skills/test_primitive_dual_surface_lookup.py ...                   [ 23%]
tests/skills/test_reflect_input_snapshot.py ...............              [ 25%]
tests/skills/test_repo_inventory_nongit.py .....                         [ 26%]
tests/skills/test_review_severity_rule.py .............................. [ 29%]
................................                                         [ 33%]
tests/skills/test_sc_recommend_routing_contract.py ..................... [ 36%]
......                                                                   [ 37%]
tests/skills/test_task_builder_merge.py ................................ [ 40%]
....................................                                     [ 45%]
tests/skills/test_task_workspace_lifecycle.py .......................... [ 48%]
...............................................                          [ 54%]
tests/skills/test_task_workspace_smoke.py ....                           [ 54%]
tests/skills/test_tier2_tavily_consistency.py .....                      [ 55%]
tests/skills/test_worker_contract.py ................................... [ 59%]
........................................................................ [ 67%]
........................................................................ [ 76%]
.................                                                        [ 78%]
tests/skills/test_workflow_archive.py .................................. [ 82%]
........................................................................ [ 91%]
.......................................................................  [100%]

============================= 831 passed in 12.90s =============================

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
