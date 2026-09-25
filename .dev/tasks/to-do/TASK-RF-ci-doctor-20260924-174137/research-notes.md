# Research Notes: Fix PR 236 CI doctor check

**Status:** Complete
**Date:** 2026-09-24
**Scenario:** A (explicit goal and target)
**Depth Tier:** Quick, skill-delegated from sc-troubleshoot-protocol
**Track Count:** 1

## EXISTING_FILES
- `.github/workflows/test.yml:195-219` — existing doctor-check job (Python 3.10); after `uv pip install --system -e ".[dev]"` the next step runs `superclaude doctor --verbose`; no `superclaude install` step. The PR job log obtained with `gh api repos/IronbellyOrg/IronClaude/actions/jobs/107745130650/logs` confirms doctor failed with six missing ccsession artifacts and exit 1.
- `src/superclaude/cli/main.py:180-198` — CLI install copies skills, wires ccsession, then merges hooks; `src/superclaude/cli/doctor.py:52-103` flags missing artifacts by design.
- `tests/cli/test_update_command.py:113-151` — existing isolated tmp-HOME real CLI install test; it does not call doctor, so CI job remains authoritative post-fix verification.
- `.dev/specs/ccsession-native-install.md:97-109,140-150` — feature contract requires install creates artifacts and doctor flags missing artifacts.
- `.dev/troubleshoot/ci-pr236-doctor-20260924172307/REPORT.md` — verified Tier-1 diagnosis, confidence 1.00 (calibrator), evidence-validator 9 local citations verified + 1 captured GitHub job log, 0 dropped.

## PATTERNS_AND_CONVENTIONS
- Job pattern uses YAML `- name:` then `run: |` for each CI step (`.github/workflows/test.yml:208-219`). Make the new step immediately after Install dependencies and before Run doctor command.
- Package install (`uv pip install ...`) only exposes the CLI. Native ccsession artifacts are created by the explicit CLI install command (`main.py:180-198`). Doctor's exit 1 for missing artifacts is mandated by spec; never weaken the doctor check.
- Use UV for Python operations; never write real user HOME in local validation. GitHub hosted runner HOME is disposable.

## GAPS_AND_QUESTIONS
- Post-fix GitHub Actions success is not yet observable because the workflow has not been edited or pushed. This is a required verification step after the user separately authorizes execution/push.
- No external API/library research needed; diagnosis is grounded in CI log, workflow and spec.

## RECOMMENDED_OUTPUTS
- One task file in this folder from MDTM template 01; no product/source code changes, no CI workflow change during task building.
- When the task is executed: update `.github/workflows/test.yml` only by inserting one named `superclaude install` step; include isolated install→doctor validation and ensure existing checks still run.

## SUGGESTED_PHASES
- Preparation: verify branch, source job, and existing first-failure evidence (from report).
- Implementation: edit only the doctor-check step ordering in `.github/workflows/test.yml`.
- Validation: exercise isolated HOME install→doctor locally; verify unchanged doctor and existing tests; remote CI verification only after separately authorized push.

## TEMPLATE_NOTES
- Template 01 generic task, one affected workflow file, known precise change; no speculative CI refactor. Skill-delegated notes replace researcher fan-out because troubleshoot already read workflow, doc spec, doctor implementation and remote CI log and ran independent confidence/evidence checks.

## AMBIGUITIES_FOR_USER
None — user approved task-file creation only; task execution/commit/push are NOT authorized by that approval.
