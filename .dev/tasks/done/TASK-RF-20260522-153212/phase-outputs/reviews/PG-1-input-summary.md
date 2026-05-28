=== Phase 2 test files modified ===
 tests/cli/eval/test_coverage_gate.py          | 15 ++++++++++++++
 tests/cli/eval/test_scratch_root_allowlist.py | 30 +++++++++++++++++++++++----
 2 files changed, 41 insertions(+), 4 deletions(-)

=== Phase 2 RED baseline pytest output ===
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0 -- /config/workspace/IronClaude/.venv/bin/python
cachedir: .pytest_cache
SuperClaude: 4.2.0
benchmark: 5.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /config/workspace/IronClaude
configfile: pyproject.toml
plugins: superclaude-4.2.0, benchmark-5.2.3, cov-7.1.0
collecting ... collected 3 items

tests/cli/eval/test_coverage_gate.py::test_coverage_gate_fails_on_corrupt_settings_json FAILED [ 33%]
tests/cli/eval/test_scratch_root_allowlist.py::test_resolve_scratch_root_rejects_bare_prefix FAILED [ 66%]
tests/cli/eval/test_eval_run.py::test_run_emits_warning_when_null_lifecycle_executor_active FAILED [100%]

=================================== FAILURES ===================================
______________ test_coverage_gate_fails_on_corrupt_settings_json _______________
tests/cli/eval/test_coverage_gate.py:332: in test_coverage_gate_fails_on_corrupt_settings_json
    assert result.passed is False
E   assert True is False
E    +  where True = CoverageResult(matchers=(), covered=(), missing=(), artifacts={}, coverage_map={}).passed
________________ test_resolve_scratch_root_rejects_bare_prefix _________________
tests/cli/eval/test_scratch_root_allowlist.py:63: in test_resolve_scratch_root_rejects_bare_prefix
    with pytest.raises(ScratchRootViolation):
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   Failed: DID NOT RAISE <class 'superclaude.cli.eval.config.ScratchRootViolation'>
__________ test_run_emits_warning_when_null_lifecycle_executor_active __________
tests/cli/eval/test_eval_run.py:656: in test_run_emits_warning_when_null_lifecycle_executor_active
    assert "NullLifecycleExecutor" in (result.stderr or "")
E   AssertionError: assert 'NullLifecycleExecutor' in (('' or ''))
E    +  where '' = <Result okay>.stderr
=========================== short test summary info ============================
FAILED tests/cli/eval/test_coverage_gate.py::test_coverage_gate_fails_on_corrupt_settings_json - assert True is False

+ where True = CoverageResult(matchers=(), covered=(), missing=(), artifacts={}, coverage_map={}).passed
FAILED tests/cli/eval/test_scratch_root_allowlist.py::test_resolve_scratch_root_rejects_bare_prefix - Failed: DID NOT RAISE <class 'superclaude.cli.eval.config.ScratchRootViolation'>
FAILED tests/cli/eval/test_eval_run.py::test_run_emits_warning_when_null_lifecycle_executor_active - AssertionError: assert 'NullLifecycleExecutor' in (('' or ''))
+ where '' = <Result okay>.stderr
============================== 3 failed in 0.25s ===============================
EXIT_CODE=0

=== Phase 2 ruff output (broader scope; pre-existing F401s noted) ===
F401 [*] `superclaude.cli.eval.commands.build_doctor_report` imported but unused
  --> tests/cli/eval/test_capability_classifications.py:66:5
   |
64 | from superclaude.cli.eval.commands import (
65 |     HARD_FAIL_EXIT_CODE,
66 |     build_doctor_report,
   |     ^^^^^^^^^^^^^^^^^^^
67 |     eval_group,
68 |     render_checklist,
   |
help: Remove unused import: `superclaude.cli.eval.commands.build_doctor_report`

F401 [*] `typing.Iterable` imported but unused
  --> tests/cli/eval/test_capability_gates.py:23:20
   |
22 | import shutil
23 | from typing import Iterable
   |                    ^^^^^^^^
24 |
25 | import pytest
   |
help: Remove unused import: `typing.Iterable`

F401 [*] `superclaude.cli.eval.capabilities.CapabilityStatus` imported but unused
  --> tests/cli/eval/test_capability_gates.py:31:5
   |
29 |     CapabilityGates,
30 |     CapabilityReport,
31 |     CapabilityStatus,
   |     ^^^^^^^^^^^^^^^^
32 |     _CapabilitySpec,
33 |_DEFAULT_CAPABILITY_SPECS,
   |
help: Remove unused import: `superclaude.cli.eval.capabilities.CapabilityStatus`

F401 [*] `typing.Mapping` imported but unused
  --> tests/cli/eval/test_expect_exit_code.py:20:20
   |
19 | from pathlib import Path
20 | from typing import Mapping
   |                    ^^^^^^^
21 |
22 | import pytest
   |
help: Remove unused import: `typing.Mapping`

F401 [*] `superclaude.cli.eval.loader.SchemaError` imported but unused
  --> tests/cli/eval/test_no_pty_exclusion.py:34:41
   |
32 |     eval_group,
33 | )
34 | from superclaude.cli.eval.loader import SchemaError, SuiteLoader, validate_manifest
   |                                         ^^^^^^^^^^^
35 | from superclaude.cli.eval.models import EvalOutcome, EvalSpec
36 | from superclaude.cli.eval.suites import SCHEMA_PATH
   |
help: Remove unused import: `superclaude.cli.eval.loader.SchemaError`

F401 [*] `threading` imported but unused
  --> tests/cli/eval/test_pty_lifecycle.py:37:8
   |
35 | import sys
36 | import textwrap
37 | import threading
   |        ^^^^^^^^^
38 | import time
39 | from dataclasses import dataclass, field
   |
help: Remove unused import: `threading`

F401 [*] `json` imported but unused
  --> tests/cli/eval/test_reporter.py:23:8
   |
22 | import hashlib
23 | import json
   |        ^^^^
24 | import xml.etree.ElementTree as ET
25 | from pathlib import Path
   |
help: Remove unused import: `json`

F401 [*] `json` imported but unused
  --> tests/cli/eval/test_retention_policy.py:48:8
   |
46 | from __future__ import annotations
47 |
48 | import json
   |        ^^^^
49 | import os
50 | import subprocess
   |
help: Remove unused import: `json`

Found 8 errors.
[*] 8 fixable with the `--fix` option.
EXIT_CODE=0

=== Phase 2 verify-sync output (post sync-dev) ===
🔍 Verifying src/superclaude/ ↔ .claude/ sync...

=== Skills ===
  ✅ confidence-check
  ✅ prd
  ✅ sc-adversarial-protocol
  ✅ sc-auggie-review-protocol
  ✅ sc-cleanup-audit-protocol
  ✅ sc-cli-portify-protocol
  ✅ sc-crash-recovery
  ✅ sc-pm-protocol
  ✅ sc-recommend-protocol
  ✅ sc-release-split-protocol
  ✅ sc-review-translation-protocol
  ✅ sc-roadmap-protocol
  ✅ sc-tasklist-protocol
  ✅ sc-task-protocol
  ⚠️  DIFFERS: sc-troubleshoot-protocol
      Files src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md and .claude/skills/sc-troubleshoot-protocol/refs/report-template.md differ
  ✅ sc-validate-roadmap-protocol
  ✅ sc-validate-tests-protocol
  ✅ task
  ✅ task-builder
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
  ✅ evidence-validator.md
  ✅ frontend-architect.md
  ✅ learning-guide.md
  ✅ merge-executor.md
  ✅ performance-engineer.md
  ✅ pm-agent.md
  ✅ python-expert.md
  ✅ quality-engineer.md
  ✅ refactoring-expert.md
  ✅ repo-index.md
  ✅ requirements-analyst.md
  ✅ rf-analyst.md
  ✅ rf-assembler.md
  ✅ rf-qa.md
  ✅ rf-qa-qualitative.md
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
  ✅ cli-portify.md
  ✅ design.md
  ✅ document.md
  ✅ estimate.md
  ✅ explain.md
  ✅ git.md
  ✅ help.md
  ✅ implement.md
  ✅ improve.md
  ✅ index.md
  ✅ index-repo.md
  ✅ load.md
  ✅ pm.md
  ✅ recommend.md
  ✅ reflect.md
  ✅ release-split.md
  ✅ research.md
  ✅ review-translation.md
  ✅ roadmap.md
  ✅ save.md
  ✅ sc.md
  ✅ select-tool.md
  ✅ spawn.md
  ✅ spec-panel.md
  ✅ tasklist.md
  ✅ task.md
  ✅ tdd.md
  ✅ test.md
  ✅ troubleshoot.md
  ✅ validate-roadmap.md
  ✅ validate-tests.md
  ✅ workflow.md

=== Hooks ===
  ✅ auggie-flag-clear.sh
  ✅ freshness-file-changed.sh
  ✅ freshness-post-read.sh
  ✅ freshness-pre-edit.sh
  ✅ freshness-session-start.sh
  ✅ freshness-subagent-start.sh
  ✅ freshness-subagent-stop.sh
  ✅ freshness-user-prompt.sh
  ✅ offer-pr-review.sh
  ✅ reject-workspace-writes.sh

=== Templates ===
  ✅ workflow/05_prd_template.md
  ✅ workflow/03_project_plan_template.md
  ✅ workflow/06_architecture_proposal_template.md
  ✅ workflow/02_mdtm_template_complex_task.md
  ✅ workflow/04_feature_brief_template.md
  ✅ workflow/changelog_template.md
  ✅ workflow/01_mdtm_template_generic_task.md
  ✅ workflow/99_mdtm_template_generic_task_old.md
  ✅ documents/operational_guide_template.md
  ✅ documents/GFxAI_Master_Documentation_Template.md
  ✅ documents/supplemental-doc-creation-checklist.md
  ✅ documents/release-spec-template.md
  ✅ documents/supplemental_doc_template.md
  ✅ documents/technical_reference_template.md
  ✅ documents/readme_template.md

=== Installer Registration ===
  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh

=== Hooks Cross-Consistency ===
  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes

❌ Drift detected! Run 'make sync-dev' to fix, or copy .claude/ changes to src/.
make: *** [Makefile:168: verify-sync] Error 1
EXIT_CODE=0
