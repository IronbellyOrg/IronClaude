# Proposal C: claim-only, and accept permission-free sessions in writing for the one test issue

## Answer

Set the watcher's claim level to `--pipeline none` (claim only: assign, comment, write the summary files; no worktree, no second agent), and accept in writing that the first live test's session (FU-1) runs with permission checks off, for that one test issue only.

## What happens next if the owner picks it

1. WA-01: one small PR makes the watcher's prompt carry `--pipeline none`, with its pins, retry list, property test and runbook strings updated; no file is shared with PR #539; opened by the PR session under its own grant row (WA-01 row).
2. WA-02: the #450 edits post with edit 1 worded "changed to `--pipeline none`" and edit 3 extended with the permission variables, the real argv and the owner's written acceptance.
3. WA-04: FU-1 runs on one test issue and records the claim level, the acceptance, `CCSESSION_PERMISSIONS`, `CC_CLAUDE_FLAGS`, the real argv, Orca's run and worker lists before and after the launch, the agent row, the real operation-id path, the Orca build string, the tab-map entry and the list of writes; the test issue is then closed or unlabelled.
4. The acceptance is recorded in the ledger with the sentence "for the test issue only"; it authorises no later issue (`merged-requirements.md:572`).

## What it unlocks

- The design and the code agree: the claim stops after the comments (D2, `docs/designs/issue-watcher.md:44`).
- FU-1 can run, which settles the open facts only it can settle (whether `agent launch` creates a Run, what the agent row holds, the real launch-reply id path) and unblocks the cron schedule (WA-05), the sweep's machine-started label (SW-10) and the handoff design (SW-13, WA-07).
- Only one permission-free session per approved issue, not two, and no worktree or agent created per approval.
- The #423 rewrite drops the "second agent" wording (V2-01 clause).

## What it costs or risks

- The one session still assigns the issue, posts comments and runs the accuracy check over untrusted issue text with permission checks off (INV-012). The acceptance limits this to one test issue; it does not remove it.
- If the claim command's ship gate for "a claim at any level" (OB-H1 item 5, `refs/claim.md:131`) has not passed, FU-1 may still be held; its status is UNVERIFIED.
- One FU-1 write (a ClickUp script, if its environment is set) has unknown reversibility.
- The watcher delivers less per approval: a claim and comments, not a ready plan.

## What stays unresolved

- Whether a later, non-test issue may run the same way (a new owner decision; this acceptance does not cover it).
- Whether the watcher should later hand an approved issue to an orchestrator (WA-07, deferred).
