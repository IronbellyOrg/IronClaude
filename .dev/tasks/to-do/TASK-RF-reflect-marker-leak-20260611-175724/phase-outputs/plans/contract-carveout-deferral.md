# Contract §3.2 Carve-Out — Deferral Plan

**Task:** TASK-RF-reflect-marker-leak-20260611-175724
**Step:** 2.3
**Date:** 2026-06-11
**Decision (original):** DEFER (default path). No in-session operator authorization for a cross-worktree edit was given at execution time, so the sibling-worktree contract was NOT edited during the main task run.

**UPDATE — 2026-06-12: APPLIED.** The operator explicitly authorized the cross-worktree edit in-session ("Apply the documented §3.2 contract carve-out to the sibling worktree once you authorize the cross-worktree edit"). The exact deferred patch (below) was applied to `/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md` §3, immediately after the generator `MUST NOT clear, unset, or overwrite` bullet, as a sibling bullet. Verified surgical: `git diff --stat` in the reflectWrapper worktree = 5 insertions, 0 deletions, no unrelated text changed.

## Why deferral is the default path

The authoritative reflect-wrapper contract lives in a **sibling worktree**:
`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md`

That `reflectWrapper` worktree may be owned by a concurrent task/session. Editing another worktree's tracked handoff file from this worktree risks clobbering concurrent work and is therefore a **non-default** action requiring explicit in-session operator authorization. None was recorded for this execution, so the carve-out is documented here as a ready-to-apply patch rather than applied.

## Current contract obligation that needs the carve-out

Research 04 (`research/04-conventions-contract-template.md` §3) confirms the contract §3 generator obligations currently state (contract lines ~94-96):

> **Generators (obligations):**
> - MUST NOT clear, unset, or overwrite `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`.

This blanket "MUST NOT clear, unset, or overwrite" conflicts with the verification-only marker strip introduced by this task's §6.1.1 control (i). The contract needs a narrow exception so the two are consistent.

## Exact deferred patch (to apply when operator authorizes the cross-worktree edit)

Add the following exception clause immediately after the generator `MUST NOT clear, unset, or overwrite ...` bullet in §3 of
`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md`:

> Exception: executors MAY remove `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` only from ordinary verification/build/test subprocess environments that cannot emit or execute reflect gates; they MUST preserve it for reflect audits, reflect gate commands, and auto-run `/task` execution so nested-gate suppression remains intact.

## Why the deferral does not block this task

- The behavioural fix lives in `src/superclaude/skills/sc-reflect-protocol/SKILL.md` §6.1.1 control (i), which is in THIS worktree and is the operative source of truth for the reflect agent's verification envelope.
- The §6.1.1 control (i) wording is already self-consistent with the marker's documented purpose (nested-gate suppression) and explicitly preserves the marker for audits/gates/`/task`.
- The contract carve-out is documentation alignment, not a functional dependency of the fix. Recording the exact patch here resolves the open question (per task Open Questions) without an unsafe cross-worktree write.

## Follow-up

A future task (or this task, if the operator authorizes the cross-worktree edit in-session) should apply the patch above to keep the contract text consistent with §6.1.1 control (i).
