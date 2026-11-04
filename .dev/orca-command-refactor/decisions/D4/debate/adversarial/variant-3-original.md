# D4 option (c): split by whether the action leaves the machine

Position: a brief may authorize a worker to make **local commits** on its own feature branch, and nothing else outward. Every action that leaves the machine or touches a shared target (push, merge, PR, GitHub comment or project update, install on a shared or real target, VM, paid external run) is never done by a worker; the coordinator or the person does it after reading the contracts.

Commit rule (the issue #326 question): a worker commits only when the brief says so, quoting the user's instruction; it commits only its Task's own files plus `.dev/tasks` (`CLAUDE.md:37`), never on `master` or the default branch, never pushes; inside `/sc:implement` it commits only after a task's `complete` line and before the next task's Q0, so the retry ladder's "HEAD has not moved" guard is not tripped (`src/superclaude/skills/sc-implement-protocol/refs/retry.md:41`; `.dev/orca-command-refactor/review/issue-326-evaluation.md:51`). The contract lists each commit's SHA in `artifacts`.

Citation key: `SPEC:N` = spec line; `HWW:N` = `src/superclaude/core/HOW-WE-WORK.md:N`; `PRL:N` = `src/superclaude/skills/sc-post-release-protocol/SKILL.md:N`; `EVAL:N` = `.dev/orca-command-refactor/review/issue-326-evaluation.md:N`.

## Why a third option
The repo already draws this exact line for people: "**Never push without approval.** Commit locally, show your lead what changed, and push only when they say go" (`HWW:282`); "Commit locally on the feature branch only when authorized" (`HWW:212`); for `/sc:git`, "a commit needs authorization. Do not append push, merge or PR creation" (`HWW:324`). (c) applies the same line to workers.

## Safety
- What a worker can do is local and undoable (`git reset` on its own branch); nothing is published from a session no person watches. Everything published still passes through the top-level coordinator, where outward steps are confirmed "unless the user pre-authorized them this session" (`PRL:351`), and PRs go through `/sc:pr-submit` (`CLAUDE.md:50`).
- The cross-session provenance gap of (a) is limited to the one action that can be undone.

## Reliability
- One boundary, easy to state and check: AC-4.2's "no new PR" and an added "`git log origin/<branch>` unchanged" check (`SPEC:275`). Per-task commits are compatible with implement's retry ladder only between tasks (`EVAL:51`, read from the protocol, UNVERIFIED live).

## How a person works day to day
- Workers can leave a clean per-task commit history (issue #326, `EVAL:19`), which the person reviews before the coordinator pushes and opens the PR. post-release workers report install, VM and PR steps as skipped (`PRL:340`); the coordinator runs them with the person.

## Implementation cost
- Spec: WC-9 sentence, the section 4 `/sc:git` row (drop the README citation, `EVAL:50`), and the implement row's commit-window sentence (`EVAL:51`). No command needs a new outward flag under `--unattended`. Loosening to (a) later stays possible.
