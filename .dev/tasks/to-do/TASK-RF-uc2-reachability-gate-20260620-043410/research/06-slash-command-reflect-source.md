# Research 06 — Slash Command Reflect Source

Status: Complete

## Scope

- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/commands/reflect.md`

## Findings

### Current flag table and insertion point

- The slash-command flag table currently lists `--spec`, `--tasklist`, `--diff`, `--commit-range`, `--scope`, `--task-log`, `--depth`, `--tier`, `--reviewers`, `--output`, `--coverage-floor`, `--no-mcp`, `--no-evidence-validator`, `--no-doc-discovery`, `--no-verify`, `--onboard`, `--with-hierarchy`, `--remediate`, budget and promotion flags at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/commands/reflect.md:72-95`.
- There is no `--no-reachability` row in the current table. The closest analogous disable row is `--no-verify` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/commands/reflect.md:86`, which describes a default-on UC-2 gate disabled by a negative flag.
- Recommended insertion point: add a `--no-reachability` row immediately after the `--no-verify` row at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/commands/reflect.md:86` so both default-on UC-2 verification controls are adjacent.

### Required semantics for the slash-command row

- The row must use patched REPORT R2/R3/R9 semantics, not stale merged-requirements text: `--no-reachability` disables Step 5.6 and records telemetry only (`reachability_gate_ran: false`, `reachability_skip_reason: --no-reachability`, null ledger path, zero counters, no reachability-created Grounding Gap, no `needs_human_decision`, no `status: partial`). Source: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:49-68`.
- The row should state the default behavior is enabled for UC-2 when side-effect requirements are eligible, but v1 blocking eligibility requires explicit `durable_sink:` or `@sink`; semantic classification is advisory-only. Source: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:229-239`.
- The row should not claim zero added work. It may say no new tool class, but must preserve bounded-work language from patched R8. Source: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:211-227`.

### Activation/handoff constraints

- The command file is a thin front door: the Behavioral Summary states it parses arguments, validates environment, hands off to the skill, and surfaces results at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/commands/reflect.md:110-115`.
- The activation block mandates invoking `Skill sc:reflect-protocol` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/commands/reflect.md:125-128`. The implementation task should therefore update command documentation/argument hints but keep behavior in `src/superclaude/skills/sc-reflect-protocol/SKILL.md` and wrapper plumbing in `src/superclaude/cli/reflect/`.

## Recommended MDTM task-item breakdown

1. Update the `argument-hint` in `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/commands/reflect.md` if the hint enumerates flags and should include `--no-reachability`; verify the current hint at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/commands/reflect.md:10` before editing.
2. Add the `--no-reachability` row after `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/commands/reflect.md:86` with patched telemetry-only semantics.
3. Add a Tool Coordination bullet only if the task also documents Step 5.6 coordination in the command file; if added, mirror the patched real-boot-only and advisory-only semantics rather than stale merged-requirements text.
4. Run `make sync-dev` and `make verify-sync` after command/source edits so `.claude/commands/sc/reflect.md` is regenerated but never staged.

## Gaps and Questions

None blocking. The command file needs documentation/argument-surface updates only; parser/forwarding behavior for `superclaude reflect run` is handled by the Python wrapper research, and protocol semantics live in the skill research.

## Summary

`src/superclaude/commands/reflect.md` directly needs a `--no-reachability` row next to `--no-verify`, optional argument-hint/tool-coordination updates, and sync-dev verification. The row must encode patched REPORT semantics: disable/spec-absent are telemetry-only, real-boot is the only Regression proof path, semantic fallback is advisory-only, and the cost is bounded rather than zero.
