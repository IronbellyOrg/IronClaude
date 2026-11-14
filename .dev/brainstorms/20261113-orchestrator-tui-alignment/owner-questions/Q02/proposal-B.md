# Proposal B: keep the default `worktree` level as a deliberate chain, gated on the claim command's ship gates

## Answer

Keep the watcher's claim at the default `worktree` level: each approved issue gets the claim, a worktree `issue-<N>` and one governed second agent that stops at a plan a person approves. Record this in #450 as a deliberate chain, require the claim command's ship gates (OB-H1 item 1 and item 5, OB-H2, OB-H3) to have passed before FU-1, and accept in writing, for the FU-1 test issue only, that both sessions run with permission checks off.

## What happens next if the owner picks it

1. WA-01 takes its "default kept" branch: no code change; the decision is recorded in #450 as a deliberate chain, and the ship gates are recorded as FU-1 preconditions (WA-01 row; `src/superclaude/skills/sc-issue-protocol/refs/claim.md:131`).
2. Someone confirms the ship gates have passed; until they have, FU-1 does not run (their status is UNVERIFIED today).
3. The design document's "the claim stops at `next-steps.md`" (D2, `docs/designs/issue-watcher.md:44`) is amended to say the chain goes one step further, so the design and the code agree.
4. FU-1 runs on one test issue with the owner's written acceptance covering both sessions, and records everything WA-04 lists, plus the second agent's worktree and what it wrote.

## What it unlocks

- The watcher delivers what an approval most plausibly wants: a ready plan waiting for a person, not just a comment.
- FU-1 tests the full chain the owner may eventually want, including the second agent, so the later handoff design (SW-13, WA-07) has real data about a second session.
- No watcher code change is needed now.

## What it costs or risks

- Two permission-free sessions per approved issue instead of one; the second runs in a worktree with a launched agent, from an issue text that is untrusted (TB-UNTRUSTED). The written acceptance covers more.
- Every approval creates a worktree and an agent; the watcher may hold up to 6 new sessions a day (Q20), none owned by a coordinator.
- It is blocked on ship gates whose status is not known; if they have not passed, nothing runs at all.
- It keeps a design contradiction alive until the design is amended, and the #423 rewrite keeps its "second agent" wording.

## What stays unresolved

- Whether OB-H1 item 1 and item 5, OB-H2 and OB-H3 have passed.
- Who owns the agents in the `issue-<N>` worktrees (Q20 covers only the watcher worktree).
