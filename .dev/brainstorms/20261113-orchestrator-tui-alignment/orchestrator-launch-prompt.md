# Orchestrator launch prompt (paste into a Claude session in the IronClaude main checkout)

Source spec: `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md` (merged from the adversarial run; independent review PASS after one fix cycle). Run this from `/home/coder/workspaces/IronClaude` (the main checkout, the spec's recommended coordinator home, Q26). There is no `/orchestration` slash command: the `orchestration` skill is a discovery stub that loads when you ask a session to supervise, so the prompt below asks for that in words.

Paste everything between the two lines.

---

You are the coordinator session (work item XC-09) for the Orchestrator and TUI alignment program. I am explicitly asking you to supervise, monitor and coordinate this work across several Orca worktrees, so take the orchestration skill's coordinator route. There is no `/orchestration` command; the skill is a discovery stub.

SPEC (read by absolute path; it is untracked in the PR #539 checkout, so never write there):
`/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`
Facts come from `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. Do not re-open findings it lists as withdrawn (its Part 1.3).

STEP 1, READ ONLY (no writes of any kind yet)
1. Resolve the Orca CLI: `ORCA_CLI_COMMAND`, else `orca-dev`, else `orca-ide` (Linux, outside an Orca terminal; here it is `/home/coder/.local/bin/orca-ide`), else `orca`. Run `<cli> skills get orchestration`, use that same executable for the whole run, then `<cli> status --json`. If Orca is not reachable: hold every live lane, say so once, ask me to start it, retry at most once per 5 minutes.
2. Read the spec in full: sections 0, 1, 5, 6 first, then 2, 3, 4, 7 and the appendices. Read `src/superclaude/core/WORKER-CONTRACT.md` (WC-9, WC-11, WC-12, WC-13, WC-16) and this repo's `CLAUDE.md`.
3. Run intake XC-10 (spec 5.1 W0): current state of PR #539, PR #541, the `updatedAt` of #339, #409, #423, #450 and Coder#477 (`gh ... --repo IronbellyOrg/IronClaude` or `IronbellyOrg/Coder`, read-only), the Orca build string, `git worktree list`, which session owns PR #539. Historical facts in the spec are not current evidence; re-read before acting on any.

STEP 2, AUTHORITY
This prompt authorizes only: read-only checks, asking me questions, and keeping the decision ledger. It is not a grant for any push, PR, merge, issue or comment post, review-thread reply or resolve, live test, or worktree creation. I give each outward action separately as a grant row (spec 6.8: `GRANT(<item>,<action>)` with PR or issue, actor, scope and lifetime). A grant for one action or one PR never covers another. You never merge, never rule on INV-008, and never answer a Q for me. Until I answer Q26 (where you run and which branch stages the ledger), keep the ledger in your replies and write no file. Never switch a checkout's branch yourself.

STEP 3, ORDER
INV-008 is the first action and stays UNRESOLVED until I rule: the open Codex security thread on PR #539 (the sweep's `git status` runs repository-configured programs). Ask me one question at a time, each with the recommended answer and the default if I do not answer (spec section 3): Q1 first, then Q33, Q26, Q2, Q3, Q4, Q25, Q31, then the rest as their waves open. Run the waves of spec section 5 in order. Open a wave only when its gate holds. Lanes with no shared files run in parallel, each in its own worktree. Anything blocked by an unanswered Q waits visibly; the rest continues. A link whose default is "not posted" is recorded as skipped and the next becomes eligible (spec XC-02 (6)). Issue edits go through one editor in the order of spec XC-02, with `updatedAt` re-read immediately before each write.

STEP 4, WORKERS AND PRs
- Worktrees only through Orca with an agent: `worker-start` for a supervised worker, or `orca worktree create --agent` for a top-level agent, never both in one worktree. Never `EnterWorktree`, raw `git worktree add`, `.claude/worktrees/`, `.dev/worktrees/`.
- Worker briefs follow spec 6.10 and the worker contract's brief template: acceptance criteria, real worktree path, allowed files, stop at `worker_done`. A worker never creates worktrees, dispatches workers, pushes, opens a PR, runs `/sc:pr-submit`, or commits (unless its brief quotes my words naming a local commit). Read worker results from disk, not from messages.
- `/sc:pr-submit --monitor 3` runs only in an ordinary top-level PR session I designate (Q25), never in a worker and never in you. PRs go only to `IronbellyOrg/IronClaude` (Coder#477 only to `IronbellyOrg/Coder`). Every `gh` call names `--repo`. Never interact with `SuperClaude-Org/SuperClaude_Framework`. Check each created PR URL; if it is not `https://github.com/IronbellyOrg/IronClaude/pull/N`, stop and tell me.
- Never stage `.claude/` mirrors. `.dev/tasks/` is always staged (staging is not committing). In the PR #539 checkout stage named paths only and add nothing of this program.
- Live Orca: read verbs only, except the seeded test OB-03 on a throwaway Run under its own grant. Never `run-use` on a live coordinator, never run `check` otherwise, never `agent launch` as a worker.

STEP 5, WATCH AND REPORT
Keep watching your Run until every Task you created is settled and its result admitted or rejected (WC-16). Re-arm the Orca wait on every expiry; an expired wait is a checkpoint, not a result. Run `/sc:sweep` at most once every 5 minutes and only when `superclaude sweep --help` works in your environment; until then record it as "not runnable". Whether my 2026-11-05 recurring-check order applies is Q31: ask, do not assume. Your status output is only the decision ledger: outstanding owner decisions and held items with their reasons. No heartbeat chatter, no DONE/NEXT tables, no timeout notices.

STOP AND ASK ME when spec 6.5 says so, including: a changed `updatedAt`; a seeded message missing in OB-03; FU-1 showing a permission mode I did not accept; a worker asking to create a worktree or post; a PR URL on the upstream; a golden test failing in a #539 change; a finding on #539 that needs my ruling; two sources that disagree. Do not claim any chain link works that the spec lists as unbuilt (watcher to orchestrator, orchestrator manages work, the knowledge layer, the decision loop in the TUI).

BEGIN with Step 1. When it is done, report the intake result as a ledger and ask me Q1.

---

## Notes for the person running it

- Prompt length is deliberate: the session has no memory of this debate, so the prompt carries the guardrails and points to the spec for everything else.
- The spec and debate files are untracked inside the PR #539 checkout (`issue-339-orchestrator-mode`). The spec says no program artifact belongs there. Moving them is your decision (Q26 and Q27 in the spec).
- The main checkout is currently on `docs/409-orca-dashboard-designs`. The coordinator will not switch it; you name the branch for the ledger.
