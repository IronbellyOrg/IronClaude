# Phase 2 QA Consolidated Report

VERDICT: FAIL

## Scope

Consolidates Phase 2 QA reports matching `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/phase-outputs/reviews/phase-2-qa-*.md`:

- `phase-2-qa-template-conformance.md` — FAIL
- `phase-2-qa-evidence-quality.md` — FAIL
- `phase-2-qa-no-side-effect-static-boundary.md` — FAIL
- `phase-2-qa-qualitative-actionability-runtime.md` — FAIL
- `phase-2-qa-qualitative-domain-accuracy.md` — FAIL
- `phase-2-qa-qualitative-raw-payload-redaction.md` — PASS

Overall verdict is FAIL because at least one report contains CRITICAL/IMPORTANT findings. Duplicate findings are merged below by affected behavior and required correction.

## Consolidated Findings

| ID | Severity | Source lens(es) | Affected source file(s) | Required correction |
|---|---|---|---|---|
| P2-QA-001 | CRITICAL | template-conformance; evidence-quality | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py`; downstream references in `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/lockgate.py` and `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py` | Align public validation dataclasses with the approved design: `CheckResult` must expose design fields `name`, `passed`, `detail`; `ValidationReport` must expose design fields `result`, `classifier_result`, `expected_result`, `checks`, `negative_controls`, `decline_validation`, `evidence_sha256`, `validated_surfaces`, and `blockers`. Update all call sites. |
| P2-QA-002 | IMPORTANT | template-conformance; evidence-quality; raw-payload-redaction (positive distinction) | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/evidence.py`; `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py`; `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py` | Resolve public-surface drift for `omitted_surfaces` and `cross_pr_shape_only`: either update the approved design to include them or internalize them while still preserving required reporting of omitted surfaces and cross-PR shape-only behavior. Do not regress redaction, where omitted surfaces are currently distinct from present/validated surfaces. |
| P2-QA-003 | CRITICAL | evidence-quality | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/evidence.py` | Make `load_evidence()` raise `FileNotFoundError` when no `combined-payload.json` and no supported surface JSON file exists. Track actual loaded payload files before synthesizing combined payload. |
| P2-QA-004 | CRITICAL | template-conformance; evidence-quality | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py`; `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py` | Replace invalid `decline_validation="exercised"` with approved vocabulary `passed`, `not_exercised`, or `failed`; persist only approved values. |
| P2-QA-005 | IMPORTANT | evidence-quality; domain-accuracy | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/candidate.py` | Change required observed identity logic so a lock requires at least one observed Augment identity (`augment_bot_login` OR `augment_app_slug`), not both. Allow `augment_app_slug=None` when bot login is observed and validation passes. |
| P2-QA-006 | CRITICAL | no-side-effect-static-boundary; evidence-quality | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/lockgate.py`; `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py` | Enforce the exact intended lock destination `.dev/pr-monitor/detection-contract.locked.md` under the active repository root. Reject nested/reordered `.dev/.../pr-monitor/...`, arbitrary absolute paths outside the repo, `.claude/`, and shipped `src/` refs. |
| P2-QA-007 | IMPORTANT | evidence-quality | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py`; likely `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py` | Include required lock metadata `generated_at` and `validation_report`. Ensure `write_lock()` receives or derives the validation report path without fabricating provenance. |
| P2-QA-008 | CRITICAL | evidence-quality | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/lockgate.py`; likely `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py` | Make the safe-lock predicate “validation report is written and references evidence hash” real. `LockGate` must verify a written validation report path/file and matching evidence hash, not just `report.passed` and a truthy hash. |
| P2-QA-009 | CRITICAL | actionability-runtime; evidence-quality | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py`; `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md`; `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`; `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py` | Do not emit an unactionable `superclaude reflect contract-status` command. Implement/register the CLI readiness surface before treating it as the next safe command, or change Phase 2 emitted commands/docs to a currently implemented surface until Phase 3 lands. |
| P2-QA-010 | IMPORTANT | actionability-runtime; domain-accuracy | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py` | Make `next_command` state-specific. `READY` should direct the operator to rerun/proceed with `/sc:pr-submit --monitor >=1`; `DECLINED_BY_USER` should preserve cancellation and not imply continuing setup. Add handling for all nine UX states. |
| P2-QA-011 | IMPORTANT | domain-accuracy | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py`; possibly facade/setup result surface | Add an operational handling path for `declined_by_user`, not just an enum literal. The path must leave existing contract files untouched and return/render the cancellation state consistently. |
| P2-QA-012 | CRITICAL | domain-accuracy | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py`; `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/lockgate.py`; `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py` | Enforce cross-PR shape-only semantics. `cross_pr_shape_only=True` must not produce current-PR readiness or pass lock writing as if current review state was validated. |

## Non-Blocking Positive Result

- `phase-2-qa-qualitative-raw-payload-redaction.md` reported PASS. Preserve current redaction properties while fixing the blocking findings above: summaries/status output must not render raw payload bodies, and omitted surfaces must remain distinct from present/validated surfaces.
