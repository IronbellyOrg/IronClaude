# Proposal A: choose claim-only now, but do not accept permission-free sessions yet; the live test waits

## Answer

Set the watcher's claim level to `--pipeline none` (claim only: assign, comment, write the summary files; no worktree, no second agent), but decline, for now, the written acceptance that the first session runs with permission checks off. The first live test (FU-1) waits until either the launched session can run with permission checks on, or the owner later gives the acceptance.

## What happens next if the owner picks it

1. WA-01 proceeds: one small PR changes the watcher so its prompt carries `--pipeline none`, with its pins and tests updated; no file is shared with PR #539 (WA-01 row).
2. The #450 edits (WA-02) post with edit 1 worded "changed to `--pipeline none`", and edit 3 recording that FU-1 is held because the permission acceptance was declined.
3. FU-1 (WA-04) does not run. The ledger records the reason: TB-PERM (every launched session on this host runs permission-free, ADJ E-11) is not accepted for a session that reads untrusted issue text (INV-012).
4. Before FU-1 is reopened, someone establishes whether a watcher-launched session can run with permission checks on (the two permission knobs, `CCSESSION_PERMISSIONS` and `CC_CLAUDE_FLAGS`, INV-011) and whether such a session can finish unattended. Both are UNVERIFIED today.

## What it unlocks

- The design contradiction is removed (the claim stops after the comments, as design decision D2 says: `docs/designs/issue-watcher.md:44`).
- The #423 rewrite can use its "no second agent" wording (V2-01 clause).
- No session reads untrusted issue text with permission checks off on the owner's say-so.

## What it costs or risks

- FU-1 does not happen, so nothing downstream of it starts: enabling the cron schedule (WA-05), reconsidering a watcher panel (WA-06), labelling machine-started sessions in the sweep (SW-10), the sub-orchestrator handoff design (SW-13, WA-07). The open facts FU-1 would settle (whether `agent launch` creates a Run, what the agent row holds, the real operation-id path) stay open.
- A permission-on session may stop at a permission prompt with nobody to answer it; the watcher is unattended. That could make FU-1 impossible in that form.
- A built and reviewed feature stays unused.

## What stays unresolved

- Whether a permission-on watcher session is feasible at all on this host.
- When, if ever, the owner gives the acceptance.
