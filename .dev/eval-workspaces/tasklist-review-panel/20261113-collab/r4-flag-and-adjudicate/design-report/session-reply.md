| Status | Result |
|---|---|
| DONE | Wrote the design for Redesign 4 (Flag-and-Adjudicate) to `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r4-flag-and-adjudicate/DESIGN.md`. It covers all seven items you asked for. |
| DONE | Ran three independent reviews (the maximum the review loop allows). Reviews 1 and 2 found 6 and 2 blocking defects; each was fixed, and the next review confirmed the fix. |
| DONE | Review 3 found 3 more blocking defects. I fixed them in the design, but nobody has checked those fixes. |
| DONE | Wrote the worker contract to `design-report/return-contract.yaml` with status succeeded, which is the command's own rule once the document exists. It records the review status. |
| NEXT | Have someone check the three unchecked fixes, then plan the build with `/sc:workflow`. |

RUNS: nothing yet; this run produced a design only. NOT BUILT: every script, hook and test the design specifies.

**What you should know before building:**
- **Haiku + 2x luna probably can't run this design.** With haiku's planning turn time (23 s), each luna can receive zero cards on every package. The launcher refuses that case rather than label an isolated run as collaboration. Whether it runs depends on haiku's turn times, which the timing spike (Spike 4) measures.
- **Sonnet + 2x luna works, but cards often arrive late.** Sonnet does the flagging and is the slowest reviewer, so its card posts lengthen the panel's total time. Many cards will reach the lunas after they have finished, and those are logged as `late`.
- **The source contradicts itself.** One rule bans any board message containing a ground-truth quote. But a card that points at the right sentence always contains one, because the ground-truth quotes come from the same candidate text. The design enforces the ban only on text the harness writes, and reports the overlap in card anchors as a count.
- **The H3 baseline sandboxes are built from recorded snapshots, not commits.** Each package's `progress.md` records a git tree id from when implementation began. The packages were squash-merged, so the commit before the first implementing commit can't be identified for sure.
- **The judge script runs byte-for-byte unchanged.** It writes its output into a temporary folder outside the old eval workspace, and that folder is deleted afterwards because its files contain ground truth.
- **Reviewers could still reach ground truth if they tried.** They have unrestricted shell access and run as the same user, so the design detects such reads in its audit but cannot prevent them.
- **Three changes to the reviewer launch line were not in the source's list of allowed differences.** The design adds `--session-id`, records peer tags in a separate file, and calls the card helper by its full path instead of through `PATH`.

**Recommended action:** have someone check the three unchecked fixes first. They are in section 2.10 (the audit), in deviation D-5 together with section 2.6 step 4 (finding the transcript of a reviewer killed by the time limit), and in the corrected audit-coverage statement. Two open questions in section 7.2 need your answer before the experiment runs: whether to keep the same role mapping on haiku, and whether the four timing-spike runs count toward the isolated baseline's 12 runs. Then plan the build:

```text
/sc:workflow "Build Redesign 4 per .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r4-flag-and-adjudicate/DESIGN.md" --depth standard --handoff none
```

Not checked: no spike was run, so it is still unconfirmed whether hooks fire for these models, whether `--resume` and `--session-id` work, and how fast the turns are. Two minor points from review 3 are left open: the session-count pattern assumes how the `claude` wrapper starts the real binary, and the judge step does not wait for the concurrency limit.
