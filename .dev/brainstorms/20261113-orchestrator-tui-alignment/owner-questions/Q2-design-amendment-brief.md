# Brief: amend the issue watcher design for the owner's Q2 decision (option 3)

Written 2026-11-14 by the orchestrating session on the owner's instruction (Q2 reply: "3 ... Yes, first test session runs with permission checks off ... Amend document re: option 3"). You are a top-level session. Read this whole file first. Plain English in everything you write for a person.

## Where you are
A NEW Orca worktree based on `origin/master`. Run `git status`, `git log --oneline -3` and `git branch --show-current` first. This is a small documentation change (one design document, perhaps one more); no code. Do not touch other worktrees.

## What the owner decided (2026-11-14)
- Q2 option 3: the watcher's claim keeps its DEFAULT level. The watcher launches `/sc:issue --claim <N>` with no `--pipeline`, so the claim runs at the claim command's default `worktree` level: assign the issue, post two comments, write summary files, then create worktree `issue-<N>` and start a governed second agent that stops at a plan for a person. No code change (`--pipeline none` is NOT added).
- This reverses the owner's own 2026-11-07 decision D2 ("claim-only: the claim stops at `next-steps.md`"). The owner made the reversal knowingly.
- Written acceptance, given 2026-11-14: "Yes, first test session runs with permission checks off". It names the FIRST test session. Option 3 also starts a second agent; the owner has not said whether the acceptance covers that second agent. Record it exactly as given and say that coverage of the second agent is not confirmed. Do not widen it.
- The owner also described a review-and-approval flow after the plan is ready (plan posted as a reply on the issue, issue moved to a review state, the assignee mentioned and asked to approve, the move to the next state taken as approval; or the same approval given inside Orca through the coordinator session or the TUI dashboard), and asked for the risk of double starts between the two places to be mitigated. A design exploration of that flow is running separately and is NOT decided. In the document, describe the flow as the owner's intended direction and mark it "to be designed; not part of this change". Do not invent its mechanism.

## What to change
Read `docs/designs/issue-watcher.md` (936 lines) and `docs/designs/issue-watcher-setup.md`. Pointers to check, not a complete list: the decision summary line near line 39; the D2 row near line 44 ("D2 claim-only ... The claim stops at `next-steps.md`"); the non-goals table near line 29 (post-claim pipeline listed as out of scope); the `max_launches` row near line 812 ("D2 claim-only: one session per approval"); the FU-7 row near line 860 ("Revisit D1 and D2"); any rollout checklist or acceptance record in the setup document; any other sentence that says or implies the claim stops at `next-steps.md` or that one approval means one session. Use grep for `claim-only`, `next-steps`, `D2`, `one session` and `pipeline`.
Rules for the edit:
1. Keep history. Do not delete the old decision; mark it superseded on 2026-11-14 with the reason and the owner's words, so a reader sees both.
2. What stays true: the poller itself never assigns, comments or moves items; it only launches the claim session. State this explicitly, so the change is not read as the poller gaining new powers.
3. Be accurate about counts: the poller still makes one launch per approved issue; the claim at the default level then starts a second agent, so downstream sessions per approval go from one to two. Fix every row that says one.
4. Record the owner's written acceptance where the document records owner acceptances (the setup or rollout checklist if one exists; otherwise the decision record), exactly as worded above, with its limit.
5. Do not change what the first live test (FU-1) requires. State only what you can verify in the files: the claim command's own gate (a hook check recorded as not yet run), the need for a separate live-test permission, a reachable Orca, and a named owner of the watcher worktree. If you cannot verify one, leave it out.
6. Do not edit any text that is not affected. No new files except none (edit in place). No code, no tests, no `.claude/` files.
7. Check whether any test pins the text you change: `grep -rn "claim-only\|issue-watcher.md" tests/` and run the relevant tests (`uv run pytest tests/issue_watch -q` and any doc-drift tests you find). Python only through UV.

## Git rules
Stage named paths only (`git add -- <paths>`). Commit locally on your own branch with a conventional message (for example `docs(issue-watch): record the owner's option 3 claim-level decision (refs #450)`), ending with the line `Co-Authored-By: Claude Code <noreply@anthropic.com>`. Do NOT push, open a PR, run `/sc:pr-submit`, comment on or edit any issue, or run any `gh` command that writes. Never interact with the SuperClaude upstream repository `SuperClaude-Org/SuperClaude_Framework`. `git fetch origin` is allowed.
Per the owner's Q25 answer (option 3) you will later build and publish this change yourself, but ONLY after the owner reads your diff and says go. Do not start that step.

## Final report (plain English, short)
1. Each place you changed, with the old and new wording in one line each.
2. Places you checked and left alone, and why.
3. Tests you ran and their observed results.
4. What you are unsure of.
5. The diff (`git diff origin/master --stat`, then the full diff).
