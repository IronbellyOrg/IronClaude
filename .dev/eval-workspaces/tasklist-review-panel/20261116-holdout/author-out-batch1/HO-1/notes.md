# HO-1 notes

## Result: 0 ground-truth items (all findings dropped)

The plan copied (`.dev/tasks/done/TASK-WF-workerContractFo-20261106-214402/...md`, sha256 a59a432c...) is **version 2**. It is not the text the report reviewed.
- The report's `artifacts/input-snapshot.yaml` records the reviewed plan as sha256 de8cbefe... (version 1). Version 1 was never committed: git history holds only version 2 (same hash as the `PLAN:` line of progress.md).
- The plan's own "Revision note (version 2)" says it was revised with findings M-1 to M-11 and RF-1 to RF-3 before execution.
- The report's plan line cites (plan :30, :66, :69, :76, :81) do not match version 2's line numbers.

Each finding checked against version 2 text and found already fixed (so dropped, not a plan defect):
- M-1: Task 5 now pins the exact phrase "`succeeded` when `superclaude init-lite` exited 0" on the SKILL.md and init-lite.md lines and bans "when the audit finished".
- M-2: Task 4 now requires "paths git ignores are left out", WC-4 and `[]`, and adds "left out" to UNATTENDED_EXPECT.
- M-3: owner decision recorded in the Revision note; WC-4 states only the exclusion.
- M-4: Constraints now record the planning spec and history files as unchanged copies.
- M-5: Task 1 asserts on the WC-4 span only and adds the phrase to RULE_PHRASES["WC-4"].
- M-6: the new WC-4 sentence says it applies to every command's list "including a fixed list in the command's own section".
- M-7: AC reworded to "no new WC-4 text contains the literal `git add`".
- M-8: Task 3 drops the restated reason and "outside the repository" from build.md.
- M-9: Task 2 names `~/.claude/WORKER-CONTRACT.md` and forbids a backticked `artifacts` above line 52.
- M-10: "nothing else listable" is used in Task 4.
- M-11: "the tool's exit code is the only basis for `succeeded`" is in Task 5.
- RF-1 (developer guide) is in Task 1; RF-2 in Constraints; RF-3 in Task 5.

No implementation-time review records exist under artifacts/ for this plan (only prompt and q0-head files), so nothing there either.

## Base
`start sha=f7d0bad...` is a **tree** object, not a commit (`git cat-file -t` = tree). The package uses the HEAD commit recorded in `artifacts/retries/T1/q0-head`: cb8f2f81ab7d99c51bcfe81fec8e200b52cf2c86 (commit; ancestor of the implementing commit 746138227; matches the plan's "based on origin/master cb8f2f81"). The plan folder is untracked at that commit (it exists only in the tree snapshot). masked_paths: [] (no file added by the implementation exists at base).
