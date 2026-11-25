Sub-issue 1 of 3 of #609 (Command Jev Preflight). Step 1 of the recommended order.

## Feature Summary

Add the missing performance phrases to the `--type` keyword table in the `sc-troubleshoot-protocol` skill, so that `/sc:troubleshoot "ccsession is taking too long to load"` auto-detects `--type performance`. One edit; no data leaves the machine.

## Problem Statement

Wave 0 of `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (lines 152-159 of the installed copy) auto-detects the type from keywords. The performance row lists only "slow", "latency", "p99", "memory", "leak" and profiler output. "ccsession is taking too long to load" matches none of them, so the type stays unset. This is also the baseline that sub-issue 2 compares Jev against, so the table should be as good as a cheap fix can make it before the comparison runs.

## User Story

As a user of `/sc:troubleshoot`, I want everyday performance wording such as "takes forever" or "hangs" to select `--type performance`, so that the performance specialist agents are used without me passing the flag.

## Proposed Solution

In `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`, extend the performance row of the Wave 0 keyword table with: "too long to load", "takes forever", "hangs". Resolve the double listing of "leak" (it is under both performance and security) in the same edit, or record why it is kept. Edit under `src/superclaude/`, then run `make sync-dev` and `make verify-sync`; never stage `.claude/` copies. Add or extend a test only if the repository already tests this table; otherwise record the manual check.

## Acceptance Criteria

- [ ] The performance row contains "too long to load", "takes forever" and "hangs".
- [ ] The treatment of "leak" (performance and security) is decided and written down.
- [ ] A manual check shows `/sc:troubleshoot "ccsession is taking too long to load"` auto-detects `--type performance`; the observed result is recorded in this issue.
- [ ] `make verify-sync` passes.

## Out of Scope

- Any Jev call or preflight component (sub-issues 2 and 3).
- Changes to other types' keyword rows beyond the "leak" decision.

## Components Affected (from `/sc:analyze`)

- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (Wave 0, keyword table)

## Related Issues/PRs

- #609 (parent: Command Jev Preflight)
- Sub-issue 2 (Jev vs keyword table) uses the table after this fix as its baseline.

<!-- sc:issue:create template=issue-feature-simple -->
