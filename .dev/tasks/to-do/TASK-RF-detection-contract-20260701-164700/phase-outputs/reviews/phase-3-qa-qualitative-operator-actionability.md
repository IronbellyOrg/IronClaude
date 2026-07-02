# QA Report — Phase 3 Qualitative Operator Actionability

**Topic:** Detection-contract readiness operator text
**Date:** 2026-07-02
**Phase:** synthesis-gate-equivalent / task-integrity
**Lens:** operator-actionability
**Fix authorization:** false

---

## Overall Verdict

VERDICT: FAIL

The operator-facing surface is close, but it still contains stale and unactionable next-step text in two live rendering paths, and the assigned source requirements file still contains older `/sc:reflect --contract-status` examples that conflict with the approved sibling CLI surface. Under the provided PASS/FAIL rule, these are blocking because they create ambiguous operator steps and stale current-surface wording.

## Verification Scope

Assigned files reviewed:

- `/config/workspace/IronClaude/src/superclaude/commands/reflect.md`
- `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`
- `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md`

Additional implementation files read to independently verify operator text against the actual readiness surface:

- `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/detection.py`
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/TASK-RF-detection-contract-20260701-164700.md`

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Next safe step clearly states `superclaude reflect contract-status [--validate] --repo <owner/repo> --pr <number>` for readiness/validation and rerun `/sc:pr-submit --monitor >=1` only after validated local lock exists | FAIL | PASS evidence: `/config/workspace/IronClaude/src/superclaude/commands/reflect.md:64-73`, `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md:58-67`, `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md:59-61`, and `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:89-90` all name the approved sibling CLI command and no-default-write/arm boundary. FAIL evidence: live `Diagnosis.next_command` still renders `not yet implemented in Phase 2; after Phase 3 use: ...` in `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py:347-364`; ready state next command is only `/sc:pr-submit --monitor 1` in `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py:182-183` and `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py:352-353`, despite `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md:24-27` requiring PR context or an existing PR number. |
| 2 | Missing-contract halt unambiguously fails closed through `DetectionContract.for_arming()` before Monitor arming when no locked contract resolves | PASS | `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md:59-61` states `DetectionContract.for_arming()` raises before Monitor arming; `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:89-90` says Wave 1 refuses to arm if no locked contract resolves and stops before output-dir/run-log/baseline initialization or Monitor arming; implementation preserves the arm surface in `/config/workspace/IronClaude/src/superclaude/pr_submit/detection.py:190-199`. |
| 3 | `--monitor 0` versus `--monitor >=1` behavior is distinguishable to an operator | PASS | `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md:33-38` separates usage examples for monitor 0/1/2/3; `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md:59-61` says `--monitor 0` always works/open PR only while `--monitor >=1` requires a locked contract; `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:89-90` states L0 never leaves `S0_IDLE` and L1+ loads `DetectionContract.for_arming()`. |
| 4 | Docs avoid ambiguity between approved sibling CLI readiness surface and older `/sc:reflect --contract-status` examples | FAIL | Current command/skill docs correctly use `superclaude reflect contract-status` (`/config/workspace/IronClaude/src/superclaude/commands/reflect.md:64-73`, `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md:58-67`), but the assigned requirements source still presents older examples as operator-facing next steps in `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md:306-313` and `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md:317-324`. That creates exactly the stale-current-surface ambiguity the checklist asks this gate to reject. |
| 5 | Operator text does not imply readiness command itself creates/writes a local lock by default | PASS | `/config/workspace/IronClaude/src/superclaude/commands/reflect.md:73`, `/config/workspace/IronClaude/src/superclaude/commands/reflect.md:120-123`, `/config/workspace/IronClaude/src/superclaude/commands/reflect.md:279-282`, `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md:67`, and `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md:61` all explicitly say no local lock is written by default. Implementation verification: `contract_status()` calls `write_report()` on validation but not `write_lock()` in `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py:96-115`. |
| 6 | Operator text does not imply readiness resumes or continues the pr-submit monitor automatically | PASS | `/config/workspace/IronClaude/src/superclaude/commands/reflect.md:73` and `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md:67` explicitly say no resume; `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md:61` says rerun `/sc:pr-submit --monitor 1` or higher after a validated local lock exists; `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:90` says no diagnosis/readiness path resumes or mutates PR state by default. |
| 7 | Recommended commands are actionable and include placeholders where repo/pr are required | FAIL | Readiness command examples include placeholders in `/config/workspace/IronClaude/src/superclaude/commands/reflect.md:68-70` and `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md:62-64`. However, ready-state commands emitted by actual render helpers are only `/sc:pr-submit --monitor 1` with no PR context or existing PR placeholder (`/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py:182-183`; `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py:352-353`), while `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md:24-27` documents PR context or existing PR number as required. |

## Findings

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py:347-364`; consumed by `render_pr_submit_missing_contract_halt()` at `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py:225-243` | The fail-closed missing-contract halt can print stale next-step text: `not yet implemented in Phase 2; after Phase 3 use: ...`. Phase 3 has already landed the approved CLI surface, so this wording is stale current-surface text and makes the operator wonder whether the documented command exists yet. | Replace `_next_command()` output with the real command shape now that Phase 3 exists: `superclaude reflect contract-status [--validate] --repo <owner/repo> --pr <number>` as appropriate, without any `not yet implemented` prefix. Add/adjust tests for `render_pr_submit_missing_contract_halt()` so stale phase wording cannot reappear. |
| 2 | IMPORTANT | `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py:172-194`; `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py:347-364` | Ready-state next command is `/sc:pr-submit --monitor 1`, but `/sc:pr-submit` requires PR context (`--head`/`--base`/`--title`/`--body`) or an existing PR number. As emitted, the recommended command is not actionable and does not include placeholders for required PR context. | Render a complete operator-safe next step for ready state, e.g. `/sc:pr-submit --monitor 1 --pr <number>` if that is the accepted attach syntax, or `/sc:pr-submit --monitor 1 --head <branch> --base <branch> --title <title> --body <body>` if opening a PR is required. The docs and helper output must agree on the supported shape. |
| 3 | IMPORTANT | `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md:306-313` and `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md:317-324` | The assigned requirements document still contains older `/sc:reflect --contract-status` examples. Even though the source command/skill docs were updated, this file remains in the operator/reviewer evidence set and contradicts the approved sibling CLI surface. | Update the stale examples to `superclaude reflect contract-status --repo <owner/repo> --pr <number>` and `superclaude reflect contract-status --validate --repo <owner/repo> --pr <number>`, or mark the old slash-command examples as superseded historical context so they cannot be interpreted as current operator instructions. |

## Evidence Bullets

- Approved sibling CLI readiness surface is present in source docs: `/config/workspace/IronClaude/src/superclaude/commands/reflect.md:64-73` and `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md:58-67`.
- Missing-contract fail-closed behavior is stated in `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md:59-61` and `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:89-90`, and the actual arming loader remains `DetectionContract.for_arming()` in `/config/workspace/IronClaude/src/superclaude/pr_submit/detection.py:190-199`.
- Actual reflect CLI registers `contract-status` with `--validate`, `--repo`, and `--pr` in `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py:76-80`.
- Actual reflect CLI validation writes a validation report only, not the local lock, via `write_report()` in `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py:96-115`.
- Stale/ambiguous next-step rendering remains in `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py:347-364`.
- Older slash-command examples remain in the assigned source requirements at `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md:306-313` and `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md:317-324`.

## Confidence and Tool Engagement

- Confidence: Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 14 | Grep: 0 | Glob: 0 | Bash/rg: 2
- Web research: none; no external lookup required.
- Unchecked items: none.
- Unverifiable items: none.

## Actions Taken

No source files were modified. `fix_authorization: false`.

## Recommendation

Do not proceed past the Phase 3 operator-actionability gate until all three IMPORTANT findings are fixed. The highest-priority fix is to remove stale `not yet implemented in Phase 2` output from the live missing-contract halt path, because that message is emitted directly to the operator when the fail-closed arming path fires.

## QA Complete
