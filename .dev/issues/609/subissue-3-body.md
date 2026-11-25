Sub-issue 3 of 3 of #609 (Command Jev Preflight). Step 3 of the recommended order. **Blocked by sub-issue 2: do not start unless sub-issue 2 shows Jev clearly beating the keyword table. If it does not, close this issue as not justified and attach the comparison.**

## Feature Summary

Build a standalone, advisory preflight for `/sc:troubleshoot` (for example `superclaude preflight troubleshoot "<prompt>"`) that uses Jev to choose `--type` and returns JSON with each flag, its probability and whether it abstained.

## Problem Statement

The keyword table in Wave 0 of the troubleshoot protocol misses everyday wording (see sub-issue 1). If sub-issue 2 shows that Jev picks the type more accurately than the table on real prompts, a preflight gives repeatable answers, thresholded probabilities and an audit trail. The model that runs Wave 0 already reads the prompt, so the justification is accuracy, determinism and auditability, not new reasoning.

## User Story

As a user of `/sc:troubleshoot`, I want the command to pick `--type` for me accurately and show how sure it was, so that the right specialist agents and escalation rules apply.

## Proposed Solution

Standalone component, advisory, measured; not the gateway.

- A small CLI command in `src/superclaude/cli/` plus one spec file per command (question wording, options and thresholds in one place), with a shared runner. The first spec covers `/sc:troubleshoot` and `--type` only.
- Jev questions: one Choice over the six types plus a companion Noul "does any type fit?", model `jev-1.14.0`. A Noul above 0.7 reads as yes, below 0.3 as no, and the band between leaves the flag unset. Do not gate on Jev's `confidence`.
- Rules: the user's explicit flags always win; the `SC:TROUBLESHOOT:TARGET` audit header records `type: performance (preflight p=0.93)`; with no `TYPESAFE_API_KEY` or no network the preflight fails open to the keyword table, which stays as the floor; a failed call is an error, never an answer.
- Wiring: the command's Wave 0 calls the preflight with Bash. Optionally a `UserPromptExpansion` hook injects the same JSON as `additionalContext` (hooks can add context but cannot rewrite the prompt or arguments).
- Never inferred: `--fix`, `--unattended`, `--report-dir`, `--output-dir`, `--caller`, `--context`, `--models`, `--no-mcp`, `--no-doc-discovery`, `--no-escalate`.
- Design for reuse: a different spec file per command, same runner. `--depth` and `--scope` are later work, not part of this build.

## Acceptance Criteria

- [ ] Precondition: sub-issue 2 recorded "Jev clearly beats the table" under the margin fixed before its run; this issue links that result.
- [ ] `superclaude preflight troubleshoot "<prompt>"` prints JSON with the type, its probability and an abstain flag.
- [ ] Explicit user flags override the preflight; a probability between 0.3 and 0.7 leaves `--type` unset.
- [ ] With no `TYPESAFE_API_KEY` or no network the command falls back to the keyword table and says so; a failed Jev call is reported as an error.
- [ ] The audit header records the preflight choice and its probability.
- [ ] Tests cover the threshold band, the override rule and the fail-open path without calling the live API.
- [ ] The prompt-to-TypeSafe data path is documented, with the public-repository limit stated.

## Out of Scope

- Any LiteLLM gateway rewrite (evaluated and rejected: the gateway sees only the expanded command text, fires on every request of the tool loop, and the user cannot see what was rewritten).
- `--depth` and `--scope` inference in this build.
- Private-repository prompts (open question OD3 in #552).
- Other commands' spec files.

## Components Affected (from `/sc:analyze`)

- New: a preflight CLI entry under `src/superclaude/cli/` and one spec file per command (do not exist yet).
- `src/superclaude/commands/troubleshoot.md` and `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (Wave 0 call and audit header).

## Related Issues/PRs

- #609 (parent: Command Jev Preflight)
- Blocked by sub-issue 2 (Jev vs keyword table comparison).
- #463: earlier closed Jev router research.
- #553: install the TypeSafe Jev plugin by default.
- #576: local inference node, an alternative to the hosted API.

<!-- sc:issue:create template=issue-feature-simple -->
