# OQ-1 Helper Granularity Decision

Status: Complete

- Open Question: OQ-1 / Fork A — helper granularity
- Recommended default: `package`
- Selected value: `package`
- Decision recorded at: 2026-07-01 19:18 UTC
- Decision source: user selected Package (Recommended) during the Step 1.3 human-decision gate.

## Rationale

The approved design recommends a package because the shared helper owns distinct responsibilities: diagnosis, file-based evidence loading, candidate derivation, validation, safe report/local-lock writing, and declarative setup questions. The package preserves the stable facade import path `superclaude.pr_submit.contract_setup` while keeping implementation modules independently testable.

## Dependent Phases Unlocked

- Phase 2 helper implementation.
- Phase 4 helper tests.
- Phase 5 final fidelity.

## Dependent Paths Unlocked

- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/__init__.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/states.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/evidence.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/candidate.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/lockgate.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/questions.py`

## Blocking Status

Decision is non-PENDING. Phase 2 may use the package path after the Phase 1 QA gate passes. No alternate single-module path is approved by this decision.
