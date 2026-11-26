# Findings: issue 771 (wire /sc:closeout and /sc:worktrees into the coordinator's finish)

Checked against HEAD a7ae3dd30 on branch ironbelly/Issuecleanup, 2026-11-24. Issue 771 is OPEN, label `enhancement`, created 2026-11-24T18:26:36Z by clayphi, no comments, no sub-issues, no linked PRs, no blockedBy/blocking links.

## Verdict

**still-relevant.** Nothing in the repo implements what the issue asks, and the issue is itself a set of open questions awaiting a decision (a design step comes first).

Evidence:
- `src/superclaude/core/WORKER-CONTRACT.md:292-303` ("Issue pipeline duties") ends at the Completion bullet (line 302, `issue-pipeline complete`) and the Never bullet (line 303). No post-merge step, no `/sc:closeout`, no `/sc:worktrees`, no `handback`.
- The only `closeout` and `sc:worktrees` mention in that file is the never-as-worker list at line 23. Grep for `closeout|sc:worktrees` over `src/superclaude/cli/issue_watch`, `src/superclaude/cli/issue_pipeline`, `src/superclaude/skills/sc-issue-protocol` and `docs/designs/issue-watcher*` returns nothing, as the issue says.
- `/sc:closeout` is merged (PR 683, merged 2026-11-20, merge commit 8b2ce556c) and issue 668 is closed as completed. `/sc:worktrees` is merged (PR 711, merged 2026-11-22, merge commit 6b17a7449) and issue 687 is closed as completed. The watcher PR 707 is merged (2ea524514).
- `docs/designs/sc-closeout.md:78` (D22) and lines 205-215 define `issue.handback: remaining`. No coordinator rule reads it.
- Boundaries the issue keeps are real: Full Submit "never covers a merge" (WORKER-CONTRACT.md:246, also pinned in `tests/skills/test_worker_contract.py` near line 3322); `/sc:worktrees` removal needs the person's typed `--apply` (`src/superclaude/commands/worktrees.md:17-21, 38-42`); `/sc:closeout` is "for a person or the orchestrator, never a worker" (`src/superclaude/commands/closeout.md:19`).
- UNVERIFIED trigger question: no merged-pull-request signal exists in the watcher or pipeline code (only `reads.py:165` merges approval events) or in `src/superclaude/commands/sweep.md`. Whether `/sc:sweep` or the watcher store could expose one at runtime is UNVERIFIED.
- UNVERIFIED: "owner ruling R38 part D". Grep of docs/ and src/ for `R38` finds no file; the issue text is the only source here.
- Plugin mirror: `find plugins -name 'WORKER-CONTRACT*'` prints nothing, matching the issue.

## Complexity and size

Complexity: **medium**. Size: **M**. Reason: the edit is one contract section plus rule tests, but it first needs three owner decisions (who runs closeout, who receives `not_done`, how cleanup respects the person-only `--apply`), and a possible new merge trigger would be code.

## Priority

**P2.** Matches the issue's own Medium; running the two commands by hand is a working workaround, and it blocks nothing else, though it overlaps issue 716's C16-C19.

## Concrete next steps

1. Owner (Ryan) answers the three questions in the issue. First, decide this issue versus issue 716 C16-C19 (the issue offers to merge into 716 or have 716 point here); the 2026-11-24 review on 716 also asks to reconcile C16/C17 with the later R38 baseline before building.
2. Settle the UNVERIFIED trigger: read `/sc:sweep` and the watcher store for a merged-PR signal, or decide the person types the closeout line.
3. Write the plan with `/sc:workflow`, then `/sc:implement`: add the post-merge duty and the `handback: remaining` recipient to "Issue pipeline duties", keep line 23 and line 246, and change `commands/worktrees.md` only if the owner explicitly widens it.
4. Add rule tests in `tests/skills/test_worker_contract.py` (with negative cases) and keep `tests/commands/test_worktrees_command.py` aligned; run `make sync-dev`, `make verify-sync`, `make lint`, `uv run pytest`; submit with `/sc:pr-submit --monitor 3`; the merge stays the person's typed go.

## Dependencies

- Needs: owner decisions in the issue's open questions; coordination with issue 716 (C16-C19 overlap). No GitHub blockedBy links exist.
- Blocks: nothing recorded; issue 761 (gap check) is its source.

## Related issues

- 668 (closed, completed): add `/sc:closeout`.
- 687 (closed, completed): daily cleanup of merged worktrees.
- 674 (open): 70 review findings on the closeout design.
- 716 (open, updated 2026-11-24T18:14:24Z): coordinator features incl. C16-C19; its 2026-11-24 comment, item 2 ("Finishing the work (C16 to C19)"), repeats this gap.
- 761 (open): gap check this issue came from.

## Related PRs

- 683 (merged 2026-11-20): `/sc:closeout`.
- 711 (merged 2026-11-22): `/sc:worktrees`.
- 707 (merged 2026-11-20): issue watcher and standing coordinator.
- 700 (merged 2026-11-20): rolled back the issue 655 orchestrator build, kept closeout. 690, 686, 697 (closed, unmerged) are the earlier 655 work, out of scope.
- No PR implements 771 (the issue's `closedByPullRequestsReferences` is empty; `gh pr list --search 771` found none).
