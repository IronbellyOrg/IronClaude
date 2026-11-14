<!-- Provenance: produced by /sc:adversarial -->
<!-- Base: Variant 2 (proposal-B) as frame, core answer from Variant 3 (proposal-C) per Change 1 -->
<!-- Merge date: 2026-11-14 -->

# Merged proposal: claim-only, and a written permission acceptance for the one FU-1 test issue, with FU-1 waiting for its preconditions

<!-- Source: Variant 3 "Answer" (Change 1, replace); precondition clause in the style of base step 2 (Change 2) -->
## Answer

Set the watcher's claim level to `--pipeline none` (claim only: assign, comment, write the summary files; no worktree, no second agent), and accept in writing that the first live test's session (FU-1) runs with permission checks off, for that one test issue only. FU-1 does not run until every precondition listed below holds.

<!-- Source: Variant 3 "What happens next" steps 1 to 4 (Change 2, restructure); new precondition step 3 from the debate consensus (Change 3, insert), written in the base's step 2 style -->
## What happens next if the owner picks it

1. WA-01: one small PR makes the watcher's prompt carry `--pipeline none`, with its pins, retry list, property test and runbook strings updated; no file is shared with PR #539; opened by the PR session under its own grant row (WA-01 row).
2. WA-02: the #450 edits post with edit 1 worded "changed to `--pipeline none`" and edit 3 extended with the permission variables, the real argv and the owner's written acceptance.
3. Someone confirms that every FU-1 precondition holds; until they all do, FU-1 does not run:
   - OB-H1 item 5 (self-started turns wrapped), which the claim command requires "before a claim at any level" (`src/superclaude/skills/sc-issue-protocol/refs/claim.md:131`). It is recorded "Pending, none run" (`docs/designs/sc-issue-launch-level-hook.md:625`); whether that line is current on master is UNVERIFIED.
   - The live-test grant: the first rollout is a bounded test under `GRANT(WA-04,live-test)` with the owner's consent (`merged-requirements.md:331`; dependency row 72, `:719`).
   - Orca answers a read verb on this host (ORCA-AVAILABLE, `merged-requirements.md:604`). Its status today is not known.
   - Q20 (who owns the agent in the watcher worktree) is answered and WA-03 is done; both come before WA-04 in the dependency chain (`merged-requirements.md:811`).
   - The owner's written acceptance from this answer (INV-012).
4. WA-04: FU-1 runs on one test issue and records the claim level, the acceptance, `CCSESSION_PERMISSIONS`, `CC_CLAUDE_FLAGS`, the real argv, Orca's run and worker lists before and after the launch, the agent row, the real operation-id path, the Orca build string, the tab-map entry and the list of writes; the test issue is then closed or unlabelled.
5. The acceptance is recorded in the ledger with the sentence "for the test issue only"; it authorises no later issue (`merged-requirements.md:572`).

<!-- Source: Variant 3 "What it unlocks" (Change 6, replace); "FU-1 can run" qualified by its preconditions per debate point X-001 -->
## What it unlocks

- The design and the code agree: the claim stops after the comments (D2, `docs/designs/issue-watcher.md:44`).
- Once its preconditions hold, FU-1 can run, which settles the open facts only it can settle (whether `agent launch` creates a Run, what the agent row holds, the real launch-reply id path) and unblocks the cron schedule (WA-05), the sweep's machine-started label (SW-10) and work on the deferred handoff design (SW-13, WA-07). That handoff is not built.
- Only one permission-free session per approved issue, not two, and no worktree or agent created per approval.
- The #423 rewrite drops the "second agent" wording (V2-01 clause).

<!-- Source: first bullet from Variant 1 A-002 (Change 4, replace); remaining bullets from Variant 3 "What it costs or risks", carried with Change 1 because the base bullets described the default `worktree` level -->
## What it costs or risks

- The written acceptance covers whatever the one session does on the test issue, not only the writes FU-1 lists: that list is the intended set, not a limit. The session runs with permission checks off (TB-PERM) and reads untrusted issue text (TB-UNTRUSTED) while it assigns the issue, posts comments and runs the accuracy check (INV-012). The acceptance limits this to one test issue; it does not remove it. The owner can write the test issue's text to shrink that risk.
- OB-H1 item 5 binds a claim at any level (`refs/claim.md:131`) and is recorded "Pending, none run" (`docs/designs/sc-issue-launch-level-hook.md:625`), so FU-1 is held until it passes.
- One FU-1 write (a ClickUp script, if its environment is set) has unknown reversibility.
- The watcher delivers less per approval: a claim and comments, not a ready plan.

<!-- Source: Variant 3 "What stays unresolved" (Change 6, replace); last bullet from Variant 1 U-001 (Change 5, append) -->
## What stays unresolved

- Whether a later, non-test issue may run the same way (a new owner decision; this acceptance does not cover it).
- Whether the watcher should later hand an approved issue to an orchestrator (WA-07, deferred; no such handoff exists today).
- Whether a watcher-launched session can run with permission checks on (the two permission knobs, `CCSESSION_PERMISSIONS` and `CC_CLAUDE_FLAGS`, INV-011) and still finish unattended. FU-1 adds a note on this to its record, with no extra run, so a later, non-test decision has real data.
