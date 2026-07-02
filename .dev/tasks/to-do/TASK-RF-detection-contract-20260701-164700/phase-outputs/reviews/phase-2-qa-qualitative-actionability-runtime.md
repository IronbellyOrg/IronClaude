VERDICT: FAIL

# Phase 2 Qualitative QA — actionability-runtime

**Task file:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/TASK-RF-detection-contract-20260701-164700.md`
**Fix authorization:** false
**Assigned scope:** Phase 2 contract setup helper, `/sc:pr-submit` command/skill docs, merged requirements, and design.

## Evidence

Files read directly:

- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/TASK-RF-detection-contract-20260701-164700.md`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/__init__.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/states.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/evidence.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/questions.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/candidate.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/lockgate.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/detection.py`
- `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py`
- `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md`
- `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/design.md`

Targeted verification performed:

- Searched assigned source/docs for `render_pr_submit_missing_contract_halt`, `contract-status`, canonical no-side-effect sentence, `for_arming`, and `--monitor 0`.
- Printed the `_next_command()` output for all nine `ContractState` values with repo/PR arguments.
- Searched the reflect CLI package for a registered `contract-status` command and read `src/superclaude/cli/reflect/commands.py` to confirm only `reflect run` is currently registered.

## Findings

| # | Severity | Affected source file | Finding | Required correction |
|---|----------|----------------------|---------|---------------------|
| 1 | CRITICAL | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py`; `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md`; `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`; `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py` | The printed next safe step is currently unactionable. `_next_command()` emits `superclaude reflect contract-status ...`, and the pr-submit command/skill docs also tell operators to run `superclaude reflect contract-status [--validate] --repo --pr`. However the current reflect CLI source has no `contract-status` command registered; `src/superclaude/cli/reflect/commands.py` only defines `reflect_group` and the `run` subcommand. Running the printed command in the current tree would fail at CLI parse instead of helping the operator recover. This violates the PASS/FAIL rule: fail on any unactionable next step. | Either implement/register `@reflect_group.command("contract-status")` before emitting it from Phase 2 paths, or change Phase 2 `_next_command()`/docs to a command that exists at this phase. If the intended implementation is Phase 3, do not claim the Phase 2 missing-contract halt is actionable until the Phase 3 CLI surface lands. |
| 2 | IMPORTANT | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py` | Not every diagnosis state maps to the correct safe next command. Runtime output from `_next_command()` shows `ready` maps to `superclaude reflect contract-status --repo ... --pr ...`, even though the merged requirements define `ready` as the state where `/sc:pr-submit --monitor >=1` may proceed through the existing gate. `declined_by_user` also maps back to `contract-status`, which does not reflect the requirements meaning “leave existing contract untouched” after user cancellation. These mappings are safe in the narrow sense that they do not mutate state, but they are not the correct next action for the state and can trap operators in a diagnostic loop. | Make `_next_command()` state-specific. For `READY`, emit the safe rerun/proceed command, e.g. `/sc:pr-submit --monitor >=1 ...` or an explicit “ready; rerun pr-submit” message. For `DECLINED_BY_USER`, emit a no-op/status message that preserves cancellation and does not imply setup should continue. Add tests that assert each of the nine states maps to the requirements default action. |

## Checks

### 1. Every diagnosis state maps to a correct safe next command — FAIL

Evidence:

- `states.py` defines all nine UX states.
- `diagnosis.py` maps next commands via `_next_command()`.
- Direct runtime probe produced:
  - `missing: superclaude reflect contract-status --repo IronbellyOrg/IronClaude --pr 123`
  - `unlocked: superclaude reflect contract-status --validate --repo IronbellyOrg/IronClaude --pr 123`
  - `unparseable: superclaude reflect contract-status --repo IronbellyOrg/IronClaude --pr 123`
  - `evidence_missing: superclaude reflect contract-status --validate --repo IronbellyOrg/IronClaude --pr 123`
  - `validation_missing: superclaude reflect contract-status --validate --repo IronbellyOrg/IronClaude --pr 123`
  - `validation_failed: superclaude reflect contract-status --validate --repo IronbellyOrg/IronClaude --pr 123`
  - `stale: superclaude reflect contract-status --validate --repo IronbellyOrg/IronClaude --pr 123`
  - `ready: superclaude reflect contract-status --repo IronbellyOrg/IronClaude --pr 123`
  - `declined_by_user: superclaude reflect contract-status --repo IronbellyOrg/IronClaude --pr 123`
- `src/superclaude/cli/reflect/commands.py` currently has no registered `contract-status` subcommand, so the emitted command is not currently runnable.
- `ready` and `declined_by_user` do not map to the requirements’ default action for those states.

### 2. Missing-contract halt prints structured diagnosis/checked paths/next safe setup command and the exact sentence — PARTIAL PASS / BLOCKED BY FINDING 1

Evidence:

- `render_pr_submit_missing_contract_halt()` renders:
  - `Diagnosis state: ...`
  - `Checked paths:` followed by every checked path
  - `Blockers:`
  - `Next safe step:` followed by `diagnosis.next_command`
- The exact sentence appears in the halt output: `No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed.`
- The structure is present, but the next safe setup/readiness command is not actionable because `superclaude reflect contract-status` is not registered in the current CLI source.

### 3. `--monitor 0` stays unaffected — PASS

Evidence:

- `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md` states that `--monitor 0` “always works (it just opens the PR)” and that the locked-contract check only applies “To arm at `--monitor >= 1`.”
- `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` states that at L0 the FSM never leaves `S0_IDLE`, opens the PR, and returns, while `DetectionContract.for_arming()` is loaded only in Wave 1 for L1+.
- `DetectionContract.for_arming()` remains equivalent to `load(prefer_local_override=True)` in `/config/workspace/IronClaude/src/superclaude/pr_submit/detection.py`, and the Phase 2 helper does not alter that method.

## Summary

- Checks passed: 1 / 3
- Checks failed: 1 / 3
- Partial/blocked: 1 / 3
- Critical issues: 1
- Important issues: 1
- Minor issues: 0
- Actions taken: none; `fix_authorization` is false.

## Required outcome before proceeding

Do not treat the Phase 2 actionability-runtime gate as passed until the next safe command printed to operators is actually runnable in the current tree and every diagnosis state maps to the correct state-specific next action.
