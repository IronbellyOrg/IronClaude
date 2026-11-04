# Option D: the coordinator runs git through an Agent-tool subagent of its own session

Position paper for the git-ownership debate. Argues D as strongly as the evidence allows.

Citation keys: as in `option-a.md` (`SPEC`, `CAPS`, `EVAL`, `HWW`, `[G]`, `[G:cl]`, `[G:wc]`, `[G:rc]`, `[G:pl]`, `GITDEMO`). `AGENT-TOOL` = the Agent tool's own description in this Claude Code session (2026-11-02), which states that subagents "inherit the parent session's permission mode" and that an agent type's "tools come from its definition (`.claude/agents/*.md` frontmatter)".

## The proposal
The coordinator keeps git ownership (as in A) but delegates the mechanical work to an Agent-tool subagent with a narrow role: "given these settled contracts and this authorization, stage these exact paths and commit with a conventional message; report the SHA". The coordinator's main chat keeps the decision; the subagent absorbs the diff reading. Workers never run mutating git.

## What D buys
- **Context isolation.** Diff reading, commit-message drafting and `git status` output stay in the subagent; the coordinator receives a short result. This is A's main weakness (context load) addressed without a new Orca worker.
- **A narrow tool list.** An agent definition can restrict tools in frontmatter, as `src/superclaude/agents/reflect-reviewer.md:5` does (`tools: Read, Grep, Glob, ...`, no Bash). A git agent could list only `Bash, Read`. Whether the frontmatter can restrict Bash to git subcommands only is UNVERIFIED; no agent in `src/superclaude/agents/` uses a `Bash(...)` pattern (grep, 2026-11-02).
- **No Orca overhead.** No readiness start (`CAPS:44`), no retention request (`[G:rc] 157`), no Task bookkeeping.
- **Same single-writer correctness as A.** The subagent runs in the coordinator's process tree, against the same worktree, at the coordinator's chosen quiescent points; one subagent at a time means one `index.lock` holder (GITDEMO).

## What D costs
- **Top-level-only commands cannot run there.** `/sc:pr-submit` "MUST run in the main orchestrating session ... Do NOT run it inside an Agent-tool subagent", and the main session must never "hand a side effect to a background shell, detached loop, or subagent" (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:47-49,82-84`). PRs, pushes made by the monitor, review replies and thread resolution therefore stay in the coordinator's main chat. D covers local commits and branch work only; outward actions fall back to A.
- **Approvals pass one more hop.** The user's authorization reaches the subagent only through the prompt the coordinator writes; the subagent's report returns in the same confident register whether right or wrong (AGENT-TOOL). Subagents inherit the parent's permission mode (AGENT-TOOL), so a permission prompt from the subagent's Bash call still reaches the person, but the person sees a git command without the coordinator's reasoning next to it.
- **No Orca record.** A subagent is not a Task or Dispatch (`CAPS:155-158`), so git actions leave no Orca outcome; the audit trail is the coordinator transcript plus the subagent's returned summary.
- **Parallel subagents would collide.** Two git subagents in one worktree hit `index.lock` (GITDEMO); the coordinator must run them one at a time.

## Correctness under parallel workers
As A: explicit paths from contracts, never while an `/sc:implement` worker runs in the same worktree (`src/superclaude/skills/sc-implement-protocol/refs/retry.md:41,44`).

## Recovery
A subagent crash returns an error to the coordinator, which inspects `git status` itself. A coordinator crash kills the subagent too; recovery as A.

## Context load on the coordinator
Lower than A for commits; unchanged for PRs (pr-submit must stay in the main chat).

## Fit with repo PR rules
PR rules force the PR step back into the main chat (`CLAUDE.md:50`; `SKILL.md:47-49`), so D is never a complete owner of GitHub actions.

## How a person works day to day
Identical to A from the person's side, except some git output arrives as a subagent summary rather than raw output.

## Implementation cost
Low: one agent definition (or a prompt template) for "commit these paths", plus the A wording in the spec.

## Weaknesses an opponent will press
1. It cannot do the actions that matter most (PR, push via monitor, comments through pr-submit).
2. It adds a hop for authorization without adding an audit record.
3. A commit is small; the context saving may not justify a second actor.
