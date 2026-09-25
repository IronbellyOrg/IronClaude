# BUILD REQUEST

Source: skill-delegated
Calling Skill: sc-troubleshoot-protocol
Task Directory: /config/workspace/IronClaude/.dev/worktrees/ccsession-native-install/.dev/tasks/to-do/TASK-RF-ci-doctor-20260924-174137/
Research Notes: /config/workspace/IronClaude/.dev/worktrees/ccsession-native-install/.dev/tasks/to-do/TASK-RF-ci-doctor-20260924-174137/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true
CLI_MODE: false

GOAL: Fix PR 236 CI doctor-check by inserting the native `superclaude install` step after package dependency installation and before `superclaude doctor --verbose` in `.github/workflows/test.yml`; keep all other workflow jobs and the doctor implementation unchanged.
WHY: GitHub Actions job 107745130650 installed only the Python package on a clean runner, so doctor correctly reported missing ccsession artifacts. The diagnosis `.dev/troubleshoot/ci-pr236-doctor-20260924172307/REPORT.md` is the driving bug report; `.dev/specs/ccsession-native-install.md` FR-1 and FR-4 is a related component contract, not a CI task specification. No separate driving CI spec exists, so PRE spec-coverage reflection is not applicable.
TEMPLATE: 01
QA_INTENSITY: lite
QA_GATE_REQUIREMENTS: NONE (single existing CI YAML step; isolated validation is still mandatory)
VALIDATION_REQUIREMENTS: Preserve the doctor fail-on-missing behavior and all other workflow steps; run `superclaude install` then `superclaude doctor --verbose` in an isolated temporary HOME, never real HOME; check YAML/shell formatting, `make verify-sync` and existing relevant tests. A successful rerun of GitHub's doctor-check after a separately authorized push is the remote acceptance check.
TESTING_REQUIREMENTS: INTEGRATION (reuse `tests/cli/test_update_command.py` coverage and run isolated install→doctor sequence; do not add a test file unless needed to make the CI contract reproducible).
POST_REFLECT_GATE: ENABLED
EXECUTION_SCOPE: The builder must write only task-building artifacts, not the CI workflow, production code, a commit, PR comments, or a push. Executing/pushing requires separate user action.
