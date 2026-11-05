---
topic: "Design the hook that mechanically enforces the launch level of agents started by /sc:issue --claim --pipeline (issue #394). Cover: what it blocks at each level (worktree, full, full with --submit), how it knows it is in a claim-launched session and which level applies, where the level is stored so the agent cannot edit it, how a human approves and how the hook tells a human command from an agent command, subagents and nested subagents, the Skill, Task and Bash tools, shell wrappers around git, fail-closed behaviour, plain-words block messages, performance, and how it is tested. Goal: maximum effect with the fewest edge cases and unwanted behaviour. @/home/coder/workspaces/IronClaude/.dev/issues/394/issue-body.md @/home/coder/workspaces/IronClaude/.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/launch-levels-addendum.md"
domain: code
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-11-05T17:10:00+00:00
---

# Seed Brief: launch-level-hook

No human is available, so the Socratic questions were answered from the issue, the addendum (FR-21 to FR-31, section 6), `WORKER-CONTRACT.md`, the repository and the official hooks documentation. Each answer is recorded as an assumption (A1 to A12) so the debate can attack it.

## Problem Statement

An agent that `/sc:issue --claim --pipeline` starts in a fresh Orca worktree runs with permission prompts off. Its only limit today is a sentence in `launch-prompt.md`. Issue #394 asks for a hook that turns the chosen launch level into a mechanical block: `worktree` (stop at an approved plan), `full` (implementation, no commit or push), `full` plus `--submit` (commit, push to the fork, `/sc:pr-submit`), and at no level a merge or a push to `master`/`main`. The hook must leave every ordinary session untouched, cover the agent's subagents, survive worktree renames and re-claims, and explain each block in plain words. Fewest edge cases wins over completeness: the design is a guardrail for an agent that drifts from its instructions, not a sandbox against a hostile one.

## Known Context

- Verified harness facts (details and sources in `enrichment/research-light.md`): a PreToolUse exit 2 holds with permission prompts off (live test V3); hooks run inside subagents with `agent_id` (V4); a typed slash command fires `UserPromptExpansion`, a model-called skill fires PreToolUse(`Skill`) only (V5); `UserPromptSubmit` carries the prompt text and also fires on self-started turns, with no origin field (V6); a crashing or timing-out hook does not block (V8).
- Repository facts (`enrichment/codebase-context.md`): hook scripts live in `src/superclaude/hooks/scripts/`, are registered in `hooks.json`, must be listed in `_FRESHNESS_SCRIPTS`, and are tested by running the real script with JSON on stdin (`tests/hooks/test_block_bare_python.py`). The #357 hook shows that parsing shell properly cost three PR review rounds and still has nine documented ceilings.
- The claim feature (`orca_worktree.py`, `launch-prompt.md`, `pipeline.json`) does not exist yet; FR-31 only says the skill writes `pipeline.json` as the hook's input and that the hook design may move it.
- `--submit` conflicts with `WORKER-CONTRACT.md` WC-9 only if the launched session counts as a worker run (UNVERIFIED, U7).

## Constraints

- Same OS user for the agent and the hook: nothing can be made truly unwritable without root. The design states the residual risks instead of pretending otherwise.
- The hook runs on every tool call of every session, so the path for an ordinary session must be a few milliseconds.
- Bash plus `jq`, like the existing hooks; no Python at hook run time; exit 0 allow, exit 2 block with a stderr message.
- `onFailure: "block"` cannot be used on the registration (it would also block ordinary sessions when the hook breaks); fail-closed has to be inside the script and only for governed sessions.
- Out of scope: the claim feature, the ccsession shim, agent launching, the worktree write boundary (#322).
- Source of truth is `src/superclaude/hooks/`; `.claude/` mirrors are never staged.

## Success Criteria

- Every acceptance criterion of #394 maps to a row in a decision table and to a named test.
- A blocked action prints what was blocked, why, and what the human can do, in plain words.
- An ordinary session pays at most one cheap check per tool call and is never blocked.
- The test plan names cases for each level, approval, session isolation, subagents and nested subagents, missing or unreadable state, tampering, worktree rename, re-claim, git wrappers, and a speed budget.
- The spec lists what the hook does not stop (residual risks) and the decisions that belong to the owner.

## Assumptions (self-answered Socratic questions)

**Clarify batch**

- **A1 (scope).** One script `launch-level-guard.sh` handling four events (SessionStart housekeeping optional, UserPromptSubmit, UserPromptExpansion, PreToolUse), a `hooks.json` registration, a tests folder, and a short interface list for the claim feature. Not the claim code.
- **A2 (failure mode).** The realistic failure is an agent that reads `launch-prompt.md`, then still runs `/sc:implement`, `git commit` or `git push` because nothing stops it, or that finds a way around the instructions by an unusual command shape. A hostile agent that deletes its own guard is not the target (threat model T1: honest but drifting agent; T2: agent that tries obvious workarounds such as `bash -c`, `env`, `command git`, `/usr/bin/git`, a script file). Residual risks beyond T2 are listed, not designed against.
- **A3 (constraints).** See Constraints.
- **A4 (done).** The eight acceptance criteria of #394, plus the owner's goal "maximum effect with the fewest edge cases and unwanted behaviour".

**Validate batch**

- **A5 (what to align with).** Follow `block-bare-python.sh` for I/O contract and tests, and the `~/.claude/state/` per-session-file convention for state. Do not copy its awk shell parser.
- **A6 (consumers).** The launched agent and its subagents (blocked), the human at the terminal (never blocked), the claim script (writes the launch record), CI tests.
- **A7 (test surface).** Table-driven pytest cases that run the real script with JSON payloads and a temporary `HOME`, plus a speed assertion, plus three observed checks on a real launch (OB-H1 payload shapes, OB-H2 binding before the first tool call, OB-H3 end to end at each level).
- **A8 (forcing function).** None, but the addendum says `full` and `--submit` should not be used on real issues until the hook ships.
- **A9 (rollback).** Remove the hook entries from `hooks.json` and reinstall; sessions already bound keep their file until it is deleted by a human with `rm`. A governed session whose store is deleted becomes ordinary (fail open) only when no session file AND no launch marker exist; see D1.

**Probe notes**

- **A10 (simplest version).** Level taken from a record, five fixed rules, no approval state: approval = the human relaunches at a higher level. Why this may not be enough: AC-3 requires typing the command or replying `approved` in the running session.
- **A11 (riskiest assumption).** That `session_id` is the same inside subagents (U1) and that the Skill tool's payload has a `skill` key (U2). The design carries a fallback and an observed check for each.
- **A12 (unwanted behaviour).** Over-matching: a governed agent running `echo "git commit"` or `git log --grep push` gets blocked. Accepted because the message is plain and the session is governed; ordinary sessions never see it.

## Interface requests to the claim feature (FR-22, FR-23, FR-27, FR-31 follow-ups)

These are what the hook needs; the design may propose them but does not implement them.

- R1: before `orca agent launch`, the claim script writes a **launch record** to a place outside the worktree (proposal: `~/.claude/state/launch-level/pending/<nonce>.json`) with level, submit flag, issue number, repository, the worktree real path at launch, and a creation time.
- R2: the launch `--prompt` begins with a fixed marker `[sc-launch:v1:<nonce>]` followed by the existing one-sentence instruction. The marker is how the hook learns that the session is claim-launched (FR-23 forbids a leading `/`, a `[` is fine).
- R3: `pipeline.json` stays as documentation only; the hook never reads a file inside the worktree for the level.
- R4: a human tool to release a session (`rm` of one file is enough for v1).

## Contested design questions for the debate

- **D1 Session identity.** (a) launch record plus marker in the first prompt, bound to `session_id` at the first UserPromptSubmit; (b) an environment variable set by the shim; (c) record keyed by worktree path or git-common-dir plus branch. Weigh: rename survival, re-claim isolation, who can forge it, interface cost.
- **D2 State location and tamper rule.** Store outside the worktree, files written only by the claim script and the hook, plus a deny rule on any tool call that names the store. Alternatives: HMAC, read-only mode bits, root-owned directory.
- **D3 Approval and human-versus-agent.** Which events create approval (typed `/sc:implement` or `/task` via `UserPromptExpansion`, whole-prompt `approved` via `UserPromptSubmit`), what the approval unlocks (implementation only, never commit or push), how long it lasts, and how self-started turns (cron, wakeup) and `orca terminal send` are kept from faking it.
- **D4 Bash classification.** Real parsing (reuse the awk scanner), word-window over-matching, a PATH shim for `git`, or git-level hooks (`pre-push`, `reference-transaction`). Weigh coverage of wrappers against edge cases and the #357 experience.
- **D5 Tool coverage.** Which of Skill, Agent/Task, Bash, Edit/Write, CronCreate/ScheduleWakeup, Monitor, Workflow, MCP tools are inspected; whether direct source edits at the `worktree` level are gated; escape routes (`claude -p`, `ccsession`, `orca`, `Agent isolation: remote`).
- **D6 Fail-closed and speed.** What "closed" means for each failure (no jq, unreadable record, bad JSON, timeout), what the fast path costs, and how the budget is tested.
- **D7 Tests.** Named case list per acceptance criterion; what is automated and what is observed.

## Open Questions

- U1 to U8 in `enrichment/research-light.md`.
- Whether the owner wants direct source edits blocked at the `worktree` level (D5).
- Whether `--submit` sessions may also be restricted to `gh ... --repo IronbellyOrg/IronClaude` (the CLAUDE.md fork rule).
- Whether a released or finished governed session should be cleaned up by the hook or by a human.

## Enrichment Context

- `enrichment/codebase-context.md` (fallback_1: native tools; auggie MCP unavailable): hook layout, registration and sync rules, the #357 hook and its test pattern, state conventions, what exists of the claim feature.
- `enrichment/research-light.md` (fallback_1: WebFetch of the official pages plus one live experiment): 14 verified facts, 8 unverified items with tolerance rules.
