"""
Unit tests for CLI install command

Tests the command installation functionality, plus durable installed-package
resource checks: every resource class the baseline wheel ships must be present
at the imported package location (and its force-included ``_src``/``_plugins``
duplicates), and each installer must copy it into an isolated temp target.

Resources are resolved from the imported ``superclaude`` package and its
distribution metadata only, so this file also runs when copied outside the
checkout against an installed (non-editable) wheel.
"""

import importlib.metadata
import json
from importlib.resources import files
from pathlib import Path
from urllib.parse import unquote, urlparse

import pytest

import superclaude
from superclaude.cli import install_agents as agents_mod
from superclaude.cli import install_commands as commands_mod
from superclaude.cli import install_core as core_mod
from superclaude.cli import install_hooks as hooks_mod
from superclaude.cli import install_skill as skill_mod
from superclaude.cli import install_templates as templates_mod
from superclaude.cli import install_user_setup as user_setup_mod
from superclaude.cli.install_commands import (
    install_commands,
    list_available_commands,
    list_installed_commands,
)
from superclaude.cli.roadmap.templates import get_template_path

# Resolved location of the imported package (editable: <project>/src/superclaude,
# wheel: <site-packages>/superclaude).
PKG = Path(superclaude.__file__).resolve().parent


def _names(block: str) -> tuple:
    return tuple(block.split())


# Baseline expectations: members of the controlled-pair baseline wheel
# superclaude-4.3.5-py3-none-any.whl (sha256 390f4c1a8cfbaa7fdb51ec0de9074fc85c
# 4ca2048671ae5d42930aeacb4bc8eb, 1710 members), relative to superclaude/<class>/.
# Every member of each data directory is listed; for cli/ only its non-.py data
# files (Python modules are code, verified by import/entry-point load).
# The baseline's superclaude/_src/superclaude/<class>/ members are identical, so
# the same table is the expectation for that force-included duplicate.
_PACKAGE_RESOURCES = {
    "agents": _names(
        """
README.md __init__.py audit-analyzer.md audit-comparator.md audit-consolidator.md
audit-scanner.md audit-validator.md auggie-reviewer.md backend-architect.md
business-panel-experts.md confidence-calibrator.md debate-orchestrator.md
deep-research-agent.md deep-research.md devops-architect.md eval-docs-loader.md
eval-run-reporter.md eval-suite-author.md evidence-validator.md
frontend-architect.md implement-retry-adviser.md learning-guide.md merge-executor.md
performance-engineer.md pm-agent.md python-expert.md quality-engineer.md refactoring-expert.md
reflect-reviewer.md repo-index.md requirements-analyst.md reuse-auditor.md
rf-analyst.md rf-assembler.md rf-qa-qualitative.md rf-qa.md rf-task-builder.md
rf-task-executor.md rf-task-researcher.md rf-team-lead.md root-cause-analyst.md
security-engineer.md self-review.md socratic-mentor.md system-architect.md
technical-writer.md
"""
    ),
    "cli": _names(
        """
audit/wiring_whitelist.yaml cleanup_audit/portify-summary.md eval/pty/CHECKLIST.md
eval/pty/PROVENANCE.md eval/schemas/summary.schema.json eval/suites/README.md
eval/suites/adversarial_merge_consistency.yaml
eval/suites/agent_grounding_drift.yaml eval/suites/audit_wiring_guard.yaml
eval/suites/cli_eval_skill_contract.yaml eval/suites/eval_cli_doc_parity.yaml
eval/suites/eval_smoke.yaml eval/suites/freshness_blocks_unread_edit.yaml
eval/suites/frontier_vs_cheap_combo.yaml eval/suites/hook_latency_drift.yaml
eval/suites/installer_sync_drift.yaml eval/suites/model_capability_matrix.yaml
eval/suites/post_release_command_contract.yaml eval/suites/real.yaml
eval/suites/suite.schema.json eval/suites/suite_schema_guard.yaml
eval/suites/task_classification_contract.yaml
eval/suites/tasklist_deterministic_shape.yaml
eval/suites/workflow_vs_task_builder.yaml roadmap/templates/certify.md.j2
roadmap/templates/debate.md.j2 roadmap/templates/diff.md.j2
roadmap/templates/extract.md.j2 roadmap/templates/extract_tdd.md.j2
roadmap/templates/generate.md.j2 roadmap/templates/merge.md.j2
roadmap/templates/reflect.md.j2 roadmap/templates/score.md.j2
roadmap/templates/spec_fidelity.md.j2 roadmap/templates/test_strategy.md.j2
roadmap/templates/tool_schemas/certify.schema.json
roadmap/templates/tool_schemas/debate.schema.json
roadmap/templates/tool_schemas/diff.schema.json
roadmap/templates/tool_schemas/extract.schema.json
roadmap/templates/tool_schemas/extract_tdd.schema.json
roadmap/templates/tool_schemas/generate.schema.json
roadmap/templates/tool_schemas/merge.schema.json
roadmap/templates/tool_schemas/reflect.schema.json
roadmap/templates/tool_schemas/score.schema.json
roadmap/templates/tool_schemas/spec_fidelity.schema.json
roadmap/templates/tool_schemas/test_strategy.schema.json
swarm/lenses/templates/bare-review-output.md
swarm/lenses/templates/doc-completeness-output.md
swarm/lenses/templates/edge-case-hunt-output.md
swarm/lenses/templates/feasibility-probe-output.md
swarm/lenses/templates/refactor-find-output.md
swarm/lenses/templates/reflect-review-output.md
swarm/lenses/templates/spec-completeness-output.md
swarm/lenses/templates/troubleshoot-hypothesis-output.md user_settings_defaults.json
"""
    ),
    "commands": _names(
        """
README.md __init__.py adversarial.md agent.md analyze.md auggie-review.md
brainstorm.md build.md business-panel.md cleanup-audit.md cleanup.md cli-eval.md
cli-portify.md design.md document.md explain.md git.md help.md implement.md
improve.md index-repo.md index.md init-lite.md load.md pm.md post-release.md
pr-submit.md recommend.md reflect.md release-split.md research.md
review-translation.md roadmap.md save.md spawn.md spec-panel.md swarm-wizard.md
task.md tasklist.md tdd.md test.md troubleshoot.md validate-roadmap.md
validate-tests.md workflow.md
"""
    ),
    "core": _names(
        """
BASH_INSPECTION_POLICY.md BUSINESS_PANEL_EXAMPLES.md BUSINESS_SYMBOLS.md CLAUDE.md
CODEGRAPH.md HOW-WE-WORK.md PRINCIPLES.md RESEARCH_CONFIG.md RULES.md __init__.py
"""
    ),
    "examples": _names(
        """
__init__.py deep_research_workflows.md release-spec-template.md
roadmap_template.compressed.md roadmap_template.md tasklist_index_template.md
tasklist_phase_template.md tdd_template.md
"""
    ),
    "hooks": _names(
        """
README.md __init__.py auggie-projects.txt.example hooks.json
scripts/auggie-flag-clear.sh scripts/codegraph-session-start.sh
scripts/freshness-file-changed.sh
scripts/freshness-post-read.sh scripts/freshness-pre-edit.sh
scripts/freshness-session-start.sh scripts/freshness-subagent-start.sh
scripts/freshness-subagent-stop.sh scripts/freshness-user-prompt.sh
scripts/pragmatic-subagent.js scripts/reject-workspace-writes.sh
scripts/sc-recommend-phase0.sh
"""
    ),
    "mcp": _names(
        """
MCP_Airis-Agent.md MCP_Auggie.md MCP_Context7.md MCP_Mindbase.md MCP_Morphllm.md
MCP_Playwright.md MCP_Tavily.md __init__.py configs/__init__.py
configs/airis-agent.json configs/auggie.json configs/context7.json
configs/mindbase.json configs/morphllm.json configs/playwright.json
"""
    ),
    "modes": _names(
        """
MODE_Brainstorming.md MODE_Business_Panel.md MODE_DeepResearch.md
MODE_Introspection.md MODE_Orchestration.md MODE_Task_Management.md
MODE_Token_Efficiency.md __init__.py
"""
    ),
    "output-styles": _names(
        """
pragmatic.md
"""
    ),
    "rules": _names(
        """
contextual/context_embedding.md core/DIRECTORY_STRUCTURE.md
core/agent_discipline_hook.md core/anti_hallucination_task_completion_rules.md
core/anti_sycophancy.md core/changelog_maintenance.md core/file_conventions.md
core/ib_agent_core.md core/quality_gates.md core/report_templating.md
core/tool_selection.md prompts/agent_library.md
prompts/automated_qa_workflow_qa_prompt.md
prompts/automated_qa_workflow_worker_prompt.md prompts/doc_code_analyst_qa_prompt.md
prompts/doc_code_analyst_worker_prompt.md prompts/documentation_expert_qa_prompt.md
prompts/documentation_expert_worker_prompt.md prompts/recruiting_expert_qa_prompt.md
prompts/recruiting_expert_worker_prompt.md
"""
    ),
    "scripts": _names(
        """
README.md __init__.py clean_command_names.py ic session-init.sh
"""
    ),
    "skills": _names(
        """
__init__.py ccsession-tag/MODEL-TIERS.md ccsession-tag/README.md
ccsession-tag/SKILL.md ccsession-tag/ccsession ccsession-tag/ccsession-models.json
ccsession-tag/ccsession.env.example ccsession-tag/hooks/session-start.sh
ccsession-tag/install.sh ccsession-tag/local-gateway-alias-proxy.py
ccsession-tag/models.py ccsession-tag/seed-env.py confidence-check/SKILL.md
confidence-check/__init__.py confidence-check/confidence.ts
operational-guide/SKILL.md prd/SKILL.md prd/refs/agent-prompts.md
prd/refs/build-request-template.md prd/refs/operational-guidance.md
prd/refs/synthesis-mapping.md prd/refs/validation-checklists.md readme/SKILL.md
roadmap/SKILL.md sc-adversarial-protocol/SKILL.md
sc-adversarial-protocol/__init__.py sc-adversarial-protocol/refs/agent-specs.md
sc-adversarial-protocol/refs/artifact-templates.md
sc-adversarial-protocol/refs/debate-protocol.md
sc-adversarial-protocol/refs/scoring-protocol.md sc-auggie-review-protocol/SKILL.md
sc-auggie-review-protocol/evals/evals.json
sc-auggie-review-protocol/refs/auggie-prompts.md
sc-auggie-review-protocol/refs/remediation-handoff.md
sc-auggie-review-protocol/refs/severity-rubric.md sc-bare-review/SKILL.md
sc-bare-review/refs/templates/bare-review-output.md sc-brainstorm-protocol/SKILL.md
sc-brainstorm-protocol/refs/agent-spec-builder.md
sc-brainstorm-protocol/refs/handoff-routing.md
sc-brainstorm-protocol/refs/socratic-templates.md sc-cleanup-audit-protocol/SKILL.md
sc-cleanup-audit-protocol/__init__.py
sc-cleanup-audit-protocol/rules/dynamic-use-checklist.md
sc-cleanup-audit-protocol/rules/pass1-surface-scan.md
sc-cleanup-audit-protocol/rules/pass2-structural-audit.md
sc-cleanup-audit-protocol/rules/pass3-cross-cutting.md
sc-cleanup-audit-protocol/rules/verification-protocol.md
sc-cleanup-audit-protocol/scripts/repo-inventory.sh
sc-cleanup-audit-protocol/templates/batch-report.md
sc-cleanup-audit-protocol/templates/final-report.md
sc-cleanup-audit-protocol/templates/finding-profile.md
sc-cleanup-audit-protocol/templates/pass-summary.md sc-cli-eval-protocol/SKILL.md
sc-cli-eval-protocol/__init__.py sc-cli-eval-protocol/refs/create-pipeline.md
sc-cli-eval-protocol/refs/eval-contracts.md
sc-cli-eval-protocol/refs/integration-map.md
sc-cli-eval-protocol/refs/run-pipeline.md
sc-cli-eval-protocol/templates/run-report.md
sc-cli-eval-protocol/templates/suite-manifest.yaml sc-cli-portify-protocol/SKILL.md
sc-cli-portify-protocol/__init__.py sc-cli-portify-protocol/decisions.yaml
sc-cli-portify-protocol/refs/analysis-protocol.md
sc-cli-portify-protocol/refs/code-templates.md
sc-cli-portify-protocol/refs/pipeline-spec.md sc-crash-recovery/SKILL.md
sc-crash-recovery/refs/investigators.md sc-crash-recovery/refs/pipelines.md
sc-crash-recovery/refs/report-template.md
sc-crash-recovery/scripts/bootstrap_scan.sh
sc-crash-recovery/scripts/parse_session_log.py sc-implement-protocol/SKILL.md
sc-implement-protocol/refs/ledger.md sc-implement-protocol/refs/managed-workspace.md
sc-implement-protocol/refs/qa.md sc-implement-protocol/refs/retry.md
sc-implement-protocol/scripts/archive_workspace.py
sc-init-lite-protocol/SKILL.md sc-pm-protocol/SKILL.md
sc-post-release-protocol/SKILL.md sc-post-release-protocol/refs/additive-diff.md
sc-post-release-protocol/refs/fan-out-pattern.md
sc-post-release-protocol/refs/golden-rule-evidence.md
sc-post-release-protocol/refs/workstream-playbook.md
sc-post-release-protocol/templates/post-release-manifest.json
sc-post-release-protocol/templates/post-release-report.md
sc-post-release-protocol/templates/sysop-test-guide.md
sc-post-release-protocol/templates/user-test-guide.md sc-pr-submit-protocol/SKILL.md
sc-pr-submit-protocol/refs/auggie-fallback.md
sc-pr-submit-protocol/refs/augment-poll.md sc-pr-submit-protocol/refs/ci-poll.md
sc-pr-submit-protocol/refs/detection-contract.md
sc-pr-submit-protocol/refs/finding-verify.md
sc-pr-submit-protocol/refs/loop-guard.md
sc-pr-submit-protocol/refs/review-retrigger.md
sc-pr-submit-protocol/refs/severity-routing.md
sc-pr-submit-protocol/refs/state-machine.md
sc-pr-submit-protocol/refs/thread-reply.md
sc-pr-submit-protocol/refs/troubleshoot-dispatch.md
sc-pr-submit-protocol/scripts/poll-augment-review.sh
sc-pr-submit-protocol/scripts/poll-ci-checks.sh
sc-pr-submit-protocol/scripts/reply-resolve-thread.sh
sc-pr-submit-protocol/scripts/retrigger-review.sh sc-recommend/SKILL.md
sc-recommend/refs/delegation-vs-native-heuristics.md
sc-recommend/refs/plugin-ecosystem-sources.md
sc-recommend/refs/surface-enumeration.md sc-reflect-protocol/SKILL.md
sc-reflect-protocol/__init__.py sc-reflect-protocol/refs/cost-profile.yaml
sc-reflect-protocol/refs/coverage-mapping.md
sc-reflect-protocol/refs/deviation-taxonomy.md
sc-reflect-protocol/refs/grader-extensions.md
sc-reflect-protocol/refs/input-resolution.md
sc-reflect-protocol/refs/ops-integration.md
sc-reflect-protocol/refs/promotion-adapters.md
sc-reflect-protocol/refs/reflection-rubric.md
sc-reflect-protocol/refs/remediation-handoff.md
sc-reflect-protocol/refs/report-template.md
sc-reflect-protocol/refs/reviewer-spec.md
sc-reflect-protocol/refs/runtime-surface.md sc-release-split-protocol/SKILL.md
sc-release-split-protocol/__init__.py
sc-release-split-protocol/refs/adversarial-integration.md
sc-release-split-protocol/refs/phase-templates.md
sc-release-split-protocol/refs/verification-protocol.md
sc-review-translation-protocol/SKILL.md sc-roadmap-protocol/SKILL.md
sc-roadmap-protocol/__init__.py sc-roadmap-protocol/refs/adversarial-integration.md
sc-roadmap-protocol/refs/extraction-pipeline.md sc-roadmap-protocol/refs/scoring.md
sc-roadmap-protocol/refs/templates.md sc-roadmap-protocol/refs/validation.md
sc-swarm-wizard-protocol/SKILL.md sc-swarm-wizard-protocol/refs/cli-contract.md
sc-swarm-wizard-protocol/refs/interview.md
sc-swarm-wizard-protocol/refs/run-monitor-summarize.md
sc-swarm-wizard-protocol/templates/summary.md sc-task-protocol/SKILL.md
sc-task-protocol/__init__.py sc-tasklist-protocol/SKILL.md
sc-tasklist-protocol/__init__.py sc-tasklist-protocol/rules/file-emission-rules.md
sc-tasklist-protocol/rules/tier-classification.md
sc-tasklist-protocol/templates/index-template.md
sc-tasklist-protocol/templates/phase-template.md sc-troubleshoot-protocol/SKILL.md
sc-troubleshoot-protocol/refs/agent-assertions.md
sc-troubleshoot-protocol/refs/calibrator-eval-cases.md
sc-troubleshoot-protocol/refs/contract-enumeration.md
sc-troubleshoot-protocol/refs/diagnosability-audit.md
sc-troubleshoot-protocol/refs/doc-discovery.md
sc-troubleshoot-protocol/refs/effective-input-proof.md
sc-troubleshoot-protocol/refs/environment-deltas.md
sc-troubleshoot-protocol/refs/escalation-rubric.md
sc-troubleshoot-protocol/refs/hardening-output-contract.md
sc-troubleshoot-protocol/refs/hypothesis-card-template.md
sc-troubleshoot-protocol/refs/pipeline-hardening-closure.md
sc-troubleshoot-protocol/refs/primitive-differential.md
sc-troubleshoot-protocol/refs/probe-packs/read-parse.md
sc-troubleshoot-protocol/refs/remediation-handoff.md
sc-troubleshoot-protocol/refs/report-template.md
sc-troubleshoot-protocol/refs/runtime-entrypoint-verification.md
sc-troubleshoot-protocol/refs/triage-checklist.md
sc-troubleshoot-protocol/refs/unmask-and-sweep.md
sc-validate-roadmap-protocol/SKILL.md sc-validate-tests-protocol/SKILL.md
sc-validate-tests-protocol/__init__.py
sc-validate-tests-protocol/classification-algorithm.yaml
sc-workflow-protocol/SKILL.md
sc-workflow-protocol/refs/00_mdtm_template_simple_task.md
sc-workflow-protocol/refs/input-parse.md
sc-workflow-protocol/refs/overlap-routing.md
sc-workflow-protocol/refs/phase-templates.md
sc-workflow-protocol/refs/quality-gates.md
sc-workflow-protocol/refs/return-contract.md task-builder/SKILL.md task/SKILL.md
tdd/SKILL.md tdd/refs/agent-prompts.md tdd/refs/build-request-template.md
tdd/refs/operational-guidance.md tdd/refs/synthesis-mapping.md
tdd/refs/validation-checklists.md tech-reference/SKILL.md tech-research/SKILL.md
"""
    ),
    "templates": _names(
        """
documents/GFxAI_Master_Documentation_Template.md
documents/agent_template_analysis.md documents/agent_template_qa.md
documents/agent_template_worker.md documents/operational_guide_template.md
documents/prd_template.md documents/readme_template.md
documents/release-spec-template.md documents/roadmap_template.md
documents/skill_template.md documents/supplemental-doc-creation-checklist.md
documents/supplemental_doc_template.md documents/tdd_template.md
documents/technical_reference_template.md modularization-template-review/INDEX.md
modularization-template-review/analyst-completeness_report_template.md
modularization-template-review/analyst-coverage-matrix_template.md
modularization-template-review/analyst-cross-validation_report_template.md
modularization-template-review/analyst-gap-analysis_template.md
modularization-template-review/analyst-synthesis-review_report_template.md
modularization-template-review/claim-evidence-matrix_template.md
modularization-template-review/codebase-research_template.md
modularization-template-review/pipeline-complete_report_template.md
modularization-template-review/qa-acceptance-methodology-audit_template.md
modularization-template-review/qa-consolidated-findings_template.md
modularization-template-review/qa-cross-source-contradictions_template.md
modularization-template-review/qa-fix-summary_template.md
modularization-template-review/qa-inventory_report_template.md
modularization-template-review/qa-lens_report_template.md
modularization-template-review/qa-qualitative-operational_report_template.md
modularization-template-review/qa-qualitative-sufficiency_report_template.md
modularization-template-review/qa-research-depth_report_template.md
modularization-template-review/qa-research-evidence_report_template.md
modularization-template-review/qa-research-gap_report_template.md
modularization-template-review/qa-source-fidelity_template.md
modularization-template-review/qa-task-research-alignment_report_template.md
modularization-template-review/qa-task-validation-b2_report_template.md
modularization-template-review/qa-task-validation-structure_report_template.md
modularization-template-review/research-notes_template.md
modularization-template-review/synthetic-dnsp-finding.contract
modularization-template-review/track-scope-map_template.md
modularization-template-review/web-research_template.md
workflow/00_mdtm_template_simple_task.md workflow/01_mdtm_template_generic_task.md
workflow/01_mdtm_template_generic_task__gfdoc.md
workflow/02_mdtm_template_complex_task.md
workflow/03_component_authoring_template.md workflow/03_project_plan_template.md
workflow/04_feature_brief_template.md workflow/05_prd_template.md
workflow/06_architecture_proposal_template.md
workflow/99_mdtm_template_generic_task_old.md workflow/changelog_template.md
"""
    ),
}

# Baseline superclaude/_plugins/superclaude/<class>/ members (force-include of
# plugins/), every member listed; "." is the plugin package root itself.
_PLUGIN_RESOURCES = {
    ".": _names(
        """
__init__.py
"""
    ),
    "agents": _names(
        """
__init__.py backend-architect.md business-panel-experts.md deep-research-agent.md
deep-research.md devops-architect.md frontend-architect.md implement-retry-adviser.md
learning-guide.md performance-engineer.md pm-agent.md python-expert.md
quality-engineer.md refactoring-expert.md repo-index.md requirements-analyst.md
root-cause-analyst.md security-engineer.md self-review.md socratic-mentor.md
system-architect.md technical-writer.md
"""
    ),
    "commands": _names(
        """
__init__.py agent.md analyze.md brainstorm.md build.md business-panel.md cleanup.md
design.md document.md explain.md git.md help.md implement.md improve.md
index-repo.md index.md load.md pm.md recommend.md reflect.md research.md save.md
spawn.md spec-panel.md task.md test.md troubleshoot.md workflow.md
"""
    ),
    "core": _names(
        """
BUSINESS_PANEL_EXAMPLES.md BUSINESS_SYMBOLS.md CODEGRAPH.md PRINCIPLES.md
RESEARCH_CONFIG.md RULES.md __init__.py
"""
    ),
    "examples": _names(
        """
__init__.py deep_research_workflows.md
"""
    ),
    "hooks": _names(
        """
__init__.py hooks.json scripts/auggie-flag-clear.sh
scripts/freshness-file-changed.sh scripts/freshness-post-read.sh
scripts/freshness-pre-edit.sh scripts/freshness-session-start.sh
scripts/freshness-subagent-start.sh scripts/freshness-subagent-stop.sh
scripts/freshness-user-prompt.sh
"""
    ),
    "mcp": _names(
        """
MCP_Context7.md MCP_Morphllm.md MCP_Playwright.md MCP_Tavily.md
__init__.py configs/__init__.py configs/context7.json configs/morphllm.json
configs/playwright.json
"""
    ),
    "modes": _names(
        """
MODE_Brainstorming.md MODE_Business_Panel.md MODE_DeepResearch.md
MODE_Introspection.md MODE_Orchestration.md MODE_Task_Management.md
MODE_Token_Efficiency.md __init__.py
"""
    ),
    "scripts": _names(
        """
__init__.py clean_command_names.py session-init.sh
"""
    ),
    "skills": _names(
        """
__init__.py confidence-check/SKILL.md confidence-check/__init__.py
confidence-check/confidence.ts sc-implement-protocol/SKILL.md
sc-implement-protocol/refs/ledger.md sc-implement-protocol/refs/managed-workspace.md
sc-implement-protocol/refs/qa.md sc-implement-protocol/refs/retry.md
sc-implement-protocol/scripts/archive_workspace.py
sc-recommend/SKILL.md sc-recommend/refs/HOW-WE-WORK.md
sc-recommend/refs/delegation-vs-native-heuristics.md
sc-recommend/refs/plugin-ecosystem-sources.md
sc-recommend/refs/surface-enumeration.md sc-workflow-protocol/SKILL.md
sc-workflow-protocol/refs/00_mdtm_template_simple_task.md
sc-workflow-protocol/refs/input-parse.md
sc-workflow-protocol/refs/overlap-routing.md
sc-workflow-protocol/refs/phase-templates.md
sc-workflow-protocol/refs/quality-gates.md
sc-workflow-protocol/refs/return-contract.md
"""
    ),
    "templates": _names(
        """
roadmaps/documentation-release.md roadmaps/feature-release.md
roadmaps/migration-release.md roadmaps/performance-release.md
roadmaps/quality-release.md roadmaps/security-release.md
"""
    ),
}

# Baseline entry_points.txt (pyproject [project.scripts] and pytest11).
_BASELINE_ENTRY_POINTS = {
    ("console_scripts", "ic", "superclaude.cli.ic:main"),
    ("console_scripts", "superclaude", "superclaude.cli.main:main"),
    ("pytest11", "superclaude", "superclaude.pytest_plugin"),
}


def _force_include_roots() -> tuple:
    """Return where pyproject's force-include ``src``/``plugins`` live for this install.

    Wheel: ``<pkg>/_src`` and ``<pkg>/_plugins``. Editable: the force-include
    sources ``<project>/src`` and ``<project>/plugins``, with the project taken
    from the distribution's ``direct_url.json``.
    """
    dist = importlib.metadata.distribution("superclaude")
    raw = dist.read_text("direct_url.json")
    info = json.loads(raw) if raw else {}
    if info.get("dir_info", {}).get("editable"):
        project = Path(unquote(urlparse(info["url"]).path)).resolve()
        assert PKG == project / "src" / "superclaude", (PKG, project)
        return project / "src", project / "plugins"
    located = Path(dist.locate_file("superclaude/__init__.py")).resolve()
    assert located == PKG / "__init__.py", (located, PKG)
    return PKG / "_src", PKG / "_plugins"


def _assert_present(root: Path, names) -> None:
    missing = [name for name in names if not (root / name).is_file()]
    assert not missing, (
        f"{len(missing)} baseline member(s) missing in {root}: {missing}"
    )


@pytest.fixture(autouse=True)
def _isolated_home(tmp_path, monkeypatch):
    """Point HOME at a temp dir so no test can touch the operator's ~/.claude."""
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    assert Path.home() == home
    return home


class TestInstallCommands:
    """Test suite for install commands functionality"""

    def test_list_available_commands(self):
        """Test listing available commands"""
        commands = list_available_commands()

        assert isinstance(commands, list)
        assert len(commands) > 0
        assert "research" in commands
        assert "index-repo" in commands

    def test_install_commands_to_temp_dir(self, tmp_path):
        """Test installing commands to a temporary directory"""
        target_dir = tmp_path / "commands"

        success, message = install_commands(target_path=target_dir, force=False)

        assert success is True
        assert "Installed" in message
        assert target_dir.exists()

        # Check that command files were copied
        command_files = list(target_dir.glob("*.md"))
        assert len(command_files) > 0

        # Verify specific commands
        assert (target_dir / "research.md").exists()
        assert (target_dir / "index-repo.md").exists()

    def test_install_commands_skip_existing(self, tmp_path):
        """Test that existing commands are skipped without --force"""
        target_dir = tmp_path / "commands"

        # First install
        success1, message1 = install_commands(target_path=target_dir, force=False)
        assert success1 is True

        # Second install without force
        success2, message2 = install_commands(target_path=target_dir, force=False)
        assert success2 is True
        assert "Skipped" in message2

    def test_install_commands_force_reinstall(self, tmp_path):
        """Test force reinstall of existing commands"""
        target_dir = tmp_path / "commands"

        # First install
        success1, message1 = install_commands(target_path=target_dir, force=False)
        assert success1 is True

        # Modify a file
        research_file = target_dir / "research.md"
        research_file.write_text("modified")
        assert research_file.read_text() == "modified"

        # Force reinstall
        success2, message2 = install_commands(target_path=target_dir, force=True)
        assert success2 is True
        assert "Installed" in message2

        # Verify file was overwritten
        content = research_file.read_text()
        assert content != "modified"
        assert "research" in content.lower()

    def test_list_installed_commands(self, tmp_path):
        """Test listing installed commands"""
        target_dir = tmp_path / "commands"

        # Before install
        # Note: list_installed_commands checks ~/.claude/commands by default
        # We can't easily test this without mocking, so just verify it returns a list
        installed = list_installed_commands()
        assert isinstance(installed, list)

        # After install to temp dir
        install_commands(target_path=target_dir, force=False)

        # Verify files exist
        command_files = list(target_dir.glob("*.md"))
        assert len(command_files) > 0

    def test_install_commands_creates_target_directory(self, tmp_path):
        """Test that target directory is created if it doesn't exist"""
        target_dir = tmp_path / "nested" / "commands"

        assert not target_dir.exists()

        success, message = install_commands(target_path=target_dir, force=False)

        assert success is True
        assert target_dir.exists()

    def test_available_commands_format(self):
        """Test that available commands have expected format"""
        commands = list_available_commands()

        # Should be list of strings
        assert all(isinstance(cmd, str) for cmd in commands)

        # Should not include file extensions
        assert all(not cmd.endswith(".md") for cmd in commands)

        # Should be sorted
        assert commands == sorted(commands)

    def test_research_command_exists(self, tmp_path):
        """Test that research command specifically gets installed"""
        target_dir = tmp_path / "commands"

        install_commands(target_path=target_dir, force=False)

        research_file = target_dir / "research.md"
        assert research_file.exists()

        content = research_file.read_text()
        assert "research" in content.lower()
        assert len(content) > 100  # Should have substantial content

    def test_all_expected_commands_available(self):
        """Test that all expected commands are available"""
        commands = list_available_commands()

        expected = ["agent", "index-repo", "recommend", "research"]

        for expected_cmd in expected:
            assert expected_cmd in commands, (
                f"Expected command '{expected_cmd}' not found"
            )


class TestInstallCommandsEdgeCases:
    """Test edge cases and error handling"""

    def test_install_to_nonexistent_parent(self, tmp_path):
        """Test installation to path with nonexistent parent directories"""
        target_dir = tmp_path / "a" / "b" / "c" / "commands"

        success, message = install_commands(target_path=target_dir, force=False)

        assert success is True
        assert target_dir.exists()

    def test_empty_target_directory_ok(self, tmp_path):
        """Test that installation works with empty target directory"""
        target_dir = tmp_path / "commands"
        target_dir.mkdir()

        success, message = install_commands(target_path=target_dir, force=False)

        assert success is True


def test_cli_integration():
    """
    Integration test: verify CLI can import and use install functions

    This tests that the CLI main.py can successfully import the functions
    """
    from superclaude.cli.install_commands import (
        list_available_commands,
    )

    # Should not raise ImportError
    commands = list_available_commands()
    assert len(commands) > 0


class TestProtocolSkillInstallMapping:
    """F2 regression guard (sc:reflect 2026-06-03): protocol skills stay standalone.

    The installer's ``_has_corresponding_command`` strips ONLY the ``sc-`` prefix.
    Protocol skills are named ``sc-<command>-protocol`` (e.g. sc-roadmap-protocol
    backing commands/roadmap.md) and are therefore NOT command-backed -- they are
    installed standalone, which is required because each /sc:<command> command
    activates its skill by name via ``Skill sc:<command>-protocol``.

    These tests would FAIL if a future change generalized the match to also strip
    a ``-protocol`` suffix (which would sweep every protocol skill into
    ``served_by_command`` and remove its standalone install).
    """

    def test_new_init_lite_protocol_is_not_command_backed(self):
        from superclaude.cli.install_skills import _has_corresponding_command

        assert _has_corresponding_command("sc-init-lite-protocol") is False

    def test_sample_existing_protocol_skills_not_command_backed(self):
        from superclaude.cli.install_skills import _has_corresponding_command

        for name in ("sc-roadmap-protocol", "sc-reflect-protocol", "sc-task-protocol"):
            assert _has_corresponding_command(name) is False, name

    def test_bare_sc_command_mapping_still_works(self):
        """The strip-``sc-`` behavior is intact: a hypothetical bare sc-<cmd> maps."""
        from superclaude.cli.install_skills import _has_corresponding_command

        # commands/roadmap.md exists, so a bare "sc-roadmap" WOULD be command-backed.
        assert _has_corresponding_command("sc-roadmap") is True
        # Non-sc- skills are never command-backed.
        assert _has_corresponding_command("some-other-skill") is False

    def test_command_activated_skill_is_not_command_backed(self):
        """A thin command cannot replace the skill it explicitly activates."""
        from superclaude.cli.install_skills import _has_corresponding_command

        assert _has_corresponding_command("sc-recommend") is False

    def test_install_all_skills_installs_command_activated_skill(self, tmp_path):
        """The global install payload includes /sc:recommend's backing skill."""
        from superclaude.cli.install_skills import install_all_skills

        target = tmp_path / "skills"
        success, message = install_all_skills(target_path=target, force=True)

        assert success is True
        assert (target / "sc-recommend" / "SKILL.md").exists()
        assert "sc-recommend → /sc:recommend" not in message

    def test_no_available_protocol_skill_is_command_backed(self):
        """Across the real skill roster, zero ``sc-*-protocol`` skills are swept."""
        from superclaude.cli.install_skills import (
            _has_corresponding_command,
            list_available_skills,
        )

        available = list_available_skills()
        protocol_skills = [
            s for s in available if s.startswith("sc-") and s.endswith("-protocol")
        ]
        assert protocol_skills, (
            "expected at least one sc-*-protocol skill in the roster"
        )
        swept = [s for s in protocol_skills if _has_corresponding_command(s)]
        assert swept == [], (
            f"protocol skills wrongly treated as command-backed: {swept}"
        )

    def test_install_all_skills_keeps_protocol_skills_standalone(self, tmp_path):
        """End-to-end: protocol skills are installed standalone, not removed."""
        from superclaude.cli.install_skills import (
            install_all_skills,
            list_available_skills,
        )

        target = tmp_path / "skills"
        success, _message = install_all_skills(target_path=target, force=True)
        assert success is True

        available = set(list_available_skills())
        for name in ("sc-init-lite-protocol", "sc-roadmap-protocol"):
            assert name in available, f"{name} missing from the skill roster"
            assert (target / name).exists(), f"{name} should be installed standalone"


class TestPostReleaseCommandContract:
    """Contract tests for the /sc:post-release command-backed refactor.

    Verifies: command discovery (5.1), command install (5.2), command Activation
    text (5.3), protocol skill discovery + standalone install (5.4),
    _has_corresponding_command mapping (5.5), and protocol skill
    frontmatter (5.8).
    """

    # --- 5.1 command discovery ---
    def test_post_release_command_discoverable(self):
        """/sc:post-release command file is discoverable by list_available_commands."""
        assert "post-release" in list_available_commands()

    # --- 5.2 command install ---
    def test_post_release_command_installed_to_target(self, tmp_path):
        """post-release.md is copied into the target commands dir on install."""
        target_dir = tmp_path / "commands"
        success, _message = install_commands(target_path=target_dir, force=False)
        assert success is True
        assert (target_dir / "post-release.md").exists()

    # --- 5.3 command Activation text ---
    def test_post_release_command_activation_text(self):
        """Command Activation section contains the dev-guide handoff tokens.

        Protects both Claude Code command behavior and cli-portify/resolution.py
        Activation parsing: the ## Activation section must contain BOTH the
        ``> Skill sc:post-release-protocol`` handoff AND the prohibition sentence.
        """
        text = (PKG / "commands" / "post-release.md").read_text()

        # Extract the ## Activation section (from the header to the next ## header).
        lines = text.splitlines()
        activation = []
        in_section = False
        for line in lines:
            if line.strip() == "## Activation":
                in_section = True
                continue
            if in_section and line.startswith("## "):
                break
            if in_section:
                activation.append(line)
        activation_text = "\n".join(activation)

        assert "> Skill sc:post-release-protocol" in activation_text
        assert (
            "Do NOT proceed with protocol execution using only this command file."
            in activation_text
        )

    # --- 5.4 protocol skill discovery + standalone install ---
    def test_post_release_protocol_skill_discoverable(self):
        from superclaude.cli.install_skill import list_available_skills

        assert "sc-post-release-protocol" in list_available_skills()

    def test_post_release_protocol_skill_installed_standalone(self, tmp_path):
        """Protocol skill installs standalone (not swept by served-by-command)."""
        from superclaude.cli.install_skills import install_all_skills

        target = tmp_path / "skills"
        success, _message = install_all_skills(target_path=target, force=True)
        assert success is True
        assert (target / "sc-post-release-protocol").exists()

    # --- 5.5 _has_corresponding_command mapping ---
    def test_post_release_command_skill_mapping(self):
        """Lock the command↔protocol split: bare sc-post-release is command-served;
        sc-post-release-protocol is NOT."""
        from superclaude.cli.install_skills import _has_corresponding_command

        assert _has_corresponding_command("sc-post-release") is True
        assert _has_corresponding_command("sc-post-release-protocol") is False

    # --- 5.8 protocol skill frontmatter ---
    def test_post_release_protocol_skill_frontmatter(self):
        text = (PKG / "skills" / "sc-post-release-protocol" / "SKILL.md").read_text()
        frontmatter = text.split("---")[1]

        assert "name: sc:post-release-protocol" in frontmatter
        assert "allowed-tools:" in frontmatter
        assert "argument-hint:" in frontmatter
        assert "<version>" in frontmatter


def test_commands_readme_not_installed(tmp_path):
    target = tmp_path / "sc"
    ok, message = install_commands(target_path=target, force=True)
    assert ok, message
    assert (target / "help.md").exists()
    assert not (target / "README.md").exists()


# ---------------------------------------------------------------------------
# Installed-package resource coverage (baseline wheel members)
# ---------------------------------------------------------------------------


class TestInstalledPackageResources:
    """Every baseline resource class exists at the resolved package location."""

    def test_package_location_matches_distribution(self):
        src_root, plugins_root = _force_include_roots()
        assert (PKG / "__init__.py").is_file()
        assert (src_root / "superclaude").is_dir(), src_root
        assert (plugins_root / "superclaude").is_dir(), plugins_root

    def test_baseline_entry_points_registered_and_loadable(self):
        dist = importlib.metadata.distribution("superclaude")
        actual = {(ep.group, ep.name, ep.value) for ep in dist.entry_points}
        assert _BASELINE_ENTRY_POINTS <= actual, _BASELINE_ENTRY_POINTS - actual
        for ep in dist.entry_points:
            if (ep.group, ep.name, ep.value) in _BASELINE_ENTRY_POINTS:
                assert ep.load() is not None, ep

    @pytest.mark.parametrize("resource_class", sorted(_PACKAGE_RESOURCES))
    def test_package_resource_class_present(self, resource_class):
        _assert_present(PKG / resource_class, _PACKAGE_RESOURCES[resource_class])

    @pytest.mark.parametrize("resource_class", sorted(_PACKAGE_RESOURCES))
    def test_src_duplicate_resource_class_present(self, resource_class):
        src_root, _plugins_root = _force_include_roots()
        _assert_present(
            src_root / "superclaude" / resource_class,
            _PACKAGE_RESOURCES[resource_class],
        )

    @pytest.mark.parametrize("resource_class", sorted(_PLUGIN_RESOURCES))
    def test_plugins_duplicate_resource_class_present(self, resource_class):
        _src_root, plugins_root = _force_include_roots()
        _assert_present(
            plugins_root / "superclaude" / resource_class,
            _PLUGIN_RESOURCES[resource_class],
        )

    def test_missing_member_fails_not_skips(self, tmp_path):
        (tmp_path / "present.md").write_text("x")
        _assert_present(tmp_path, ["present.md"])
        with pytest.raises(AssertionError, match="absent.md"):
            _assert_present(tmp_path, ["present.md", "absent.md"])


# Installer source lookups and the package-relative path each must resolve to.
_RESOLVERS = {
    "core": (core_mod._get_core_source, "core"),
    "commands": (commands_mod._get_commands_source, "commands"),
    "agents": (agents_mod._get_agents_source, "agents"),
    "templates": (templates_mod._get_templates_source, "templates"),
    "hooks-json": (hooks_mod._get_hooks_source, "hooks/hooks.json"),
    "hooks-scripts": (hooks_mod._get_hooks_scripts_source, "hooks/scripts"),
    "hooks-legacy-scripts": (hooks_mod._get_legacy_scripts_source, "scripts"),
    "hooks-seed-root": (hooks_mod._get_hooks_source_root, "hooks"),
    "rules": (lambda: user_setup_mod._package_dir("rules"), "rules"),
    "output-styles": (
        lambda: user_setup_mod._package_dir("output-styles"),
        "output-styles",
    ),
    "skill": (
        lambda: skill_mod._get_skill_source("sc-recommend"),
        "skills/sc-recommend",
    ),
    "ic-script": (
        lambda: Path(str(files("superclaude.scripts").joinpath("ic"))),
        "scripts/ic",
    ),
    "roadmap-examples": (
        lambda: get_template_path("roadmap_template.compressed.md"),
        "examples/roadmap_template.compressed.md",
    ),
}


@pytest.mark.parametrize("name", sorted(_RESOLVERS))
def test_installer_source_resolves_inside_package(name):
    resolver, rel = _RESOLVERS[name]
    resolved = resolver()
    assert resolved is not None, name
    assert Path(resolved).resolve() == PKG / rel
    assert (PKG / rel).exists(), PKG / rel


def _skill_members() -> dict:
    by_skill: dict = {}
    for rel in _PACKAGE_RESOURCES["skills"]:
        if "/" in rel:
            by_skill.setdefault(rel.split("/", 1)[0], []).append(rel)
    return by_skill


def _install_core(target):
    result = core_mod.install_core_files(target_path=target, force=True)
    md = [n for n in _PACKAGE_RESOURCES["core"] if n.endswith(".md")]
    return result, target, md


def _install_commands(target):
    result = install_commands(target_path=target, force=True)
    expected = [
        n
        for n in _PACKAGE_RESOURCES["commands"]
        if n.endswith(".md") and n not in commands_mod._EXCLUDE_FILES
    ]
    return result, target, expected


def _install_agents(target):
    result = agents_mod.install_agents(target_path=target, force=True)
    expected = [
        n
        for n in _PACKAGE_RESOURCES["agents"]
        if n.endswith(".md") and n not in agents_mod._EXCLUDE_FILES
    ]
    return result, target, expected


def _install_skills(target):
    from superclaude.cli.install_skills import (
        _has_corresponding_command,
        install_all_skills,
    )

    result = install_all_skills(target_path=target, force=True)
    expected = []
    for skill, members in sorted(_skill_members().items()):
        if _has_corresponding_command(skill):
            assert not (target / skill).exists(), skill
        else:
            expected.extend(members)
    return result, target, expected


def _install_templates(target):
    result = templates_mod.install_templates(target_path=target, force=True)
    return result, target, list(_PACKAGE_RESOURCES["templates"])


def _install_hooks(target):
    result = hooks_mod.install_hooks(target_path=target / "settings.json", force=True)
    assert "session-init.sh" in _PACKAGE_RESOURCES["scripts"]
    expected = [
        "hooks/" + n.split("/", 1)[1]
        for n in _PACKAGE_RESOURCES["hooks"]
        if n.startswith("scripts/")
    ] + ["hooks/session-init.sh", "settings.json"]
    for src_name, dest_name in hooks_mod._SEED_FILES:
        assert src_name in _PACKAGE_RESOURCES["hooks"], src_name
        expected.append(dest_name)
    settings = json.loads((target / "settings.json").read_text())
    assert settings.get("hooks"), "hook registrations were not merged"
    return result, target, expected


def _install_rules(target):
    result = user_setup_mod.install_rules(home=target, force=True)
    return result, target / ".claude" / "rules", list(_PACKAGE_RESOURCES["rules"])


def _install_output_styles(target):
    result = user_setup_mod.install_output_styles(home=target, force=True)
    return (
        result,
        target / ".claude" / "output-styles",
        list(_PACKAGE_RESOURCES["output-styles"]),
    )


_INSTALLERS = {
    "core": _install_core,
    "commands": _install_commands,
    "agents": _install_agents,
    "skills": _install_skills,
    "templates": _install_templates,
    "hooks": _install_hooks,
    "rules": _install_rules,
    "output-styles": _install_output_styles,
}


@pytest.mark.parametrize("name", sorted(_INSTALLERS))
def test_installer_copies_baseline_resources_to_isolated_target(
    name, tmp_path, _isolated_home
):
    target = tmp_path / "target"
    (success, message), root, expected = _INSTALLERS[name](target)
    assert success is True, message
    assert expected, f"no baseline expectation for {name}"
    _assert_present(root, expected)
    assert list(_isolated_home.iterdir()) == [], "installer wrote into HOME"


# Module seam each installer uses to find its source, and a call that must fail
# (not skip) when that source is missing.
_MISSING_SOURCE = {
    "core": (core_mod, "_get_core_source", core_mod.install_core_files),
    "commands": (commands_mod, "_get_commands_source", install_commands),
    "agents": (agents_mod, "_get_agents_source", agents_mod.install_agents),
    "templates": (
        templates_mod,
        "_get_templates_source",
        templates_mod.install_templates,
    ),
    "hooks": (
        hooks_mod,
        "_get_hooks_source",
        lambda target: hooks_mod.install_hooks(target_path=target / "settings.json"),
    ),
    "skill": (
        skill_mod,
        "_get_skill_source",
        lambda target: skill_mod.install_skill_command("sc-recommend", target),
    ),
    "rules": (
        user_setup_mod,
        "_package_dir",
        lambda target: user_setup_mod.install_rules(home=target),
    ),
    "output-styles": (
        user_setup_mod,
        "_package_dir",
        lambda target: user_setup_mod.install_output_styles(home=target),
    ),
}


@pytest.mark.parametrize("name", sorted(_MISSING_SOURCE))
def test_installer_fails_when_source_missing(name, tmp_path, monkeypatch):
    module, seam, call = _MISSING_SOURCE[name]
    absent = tmp_path / "absent"
    monkeypatch.setattr(module, seam, lambda *args, **kwargs: absent)
    success, message = call(tmp_path / "target")
    assert success is False, message
