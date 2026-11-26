# Findings: issue 774 (docs refresh for the issue watcher and coordinator)

Checked 2026-11-24 in worktree HEAD a7ae3dd30; origin/master is f2894fc44. The 6 commits between them touch only install and swarm docs, none of the files named in the issue. Issue 774: OPEN, label `enhancement`, no assignee, created 2026-11-24T18:28:15Z, no comments, no PR references it (gh pr list search found none). Analyze report: `.dev/issuecleanup/g7/774/analyze/analyze-report.md`.

## Verdict

**still-relevant.** Nothing in the issue has been done yet and none of the stale text has been corrected. Part B also waits for an owner ruling, so work cannot fully start.

Evidence per item (all re-read on disk today):

- A.1 approval label: still "approval label" at `docs/designs/issue-watcher.md:21`, `:43`; `docs/designs/issue-pipeline-fu1.md:32`, `:94`; `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:45` (R19), `:105`; docstrings `src/superclaude/cli/issue_pipeline/cli.py:267`, `src/superclaude/cli/issue_pipeline/stage_predicates.py:1`, `:24`. Loader claim is correct: `src/superclaude/cli/issue_watch/cycle.py:251-254` rejects only a `labels.approval` value other than the default, with the message that approval is the Approved issue field. Whether that field is a Project field or an organization issue field: UNVERIFIED (not checked in code).
- A.2 person-opened: still at `docs/designs/issue-watcher.md:43`, `docs/user-guide/orchestrator-mode.md:11` ("You open it") and `:19`. `src/superclaude/core/HOW-WE-WORK.md:356` is already corrected ("whether a person opened it or a script started it"). PRs 735, 736, 752, 754 all MERGED 2026-11-23. In `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` the old wording sits in a table row quoting HOW-WE-WORK `:400` marked NORMATIVE, and a "Roles" item; the issue's line numbers 699 and 708 land on those two rows. How to label them is the open question.
- A.3 Full "also implements": `src/superclaude/commands/issue.md:16` ("`full` also implements without a commit or a push"), `docs/designs/sc-issue-command.md:44`, `docs/designs/sc-issue-claim-pipeline-flag.md:162`; pinned by `tests/skills/test_issue_protocol.py:880` (`"`full` also implements without a commit or a push" in skill`). The issue cites `claim.md:80` as the watcher-stage rule, but line 80 is the next-steps step; the stage handling is nearer `claim.md:83` (`--stage`). Treat that citation as imprecise. The ship gate is closed (`src/superclaude/cli/issue_watch/launch.py:48`, `GOVERNED_LEVELS_ALLOWED = False`), so today only Pipeline None launches, which makes the Full text mostly dormant but still wrong for stage claims.
- A.4 coordinator does every push: `docs/user-guide/orchestrator-mode.md:11`, `src/superclaude/core/HOW-WE-WORK.md:362`, `SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:318` all say the coordinator does every push; `src/superclaude/core/WORKER-CONTRACT.md:242,246` add the person's go. Confirmed.
- A.5 "Nothing manual": `requirements.md:40` (R9), `:43` (R17), `docs/designs/issue-watcher-zero-setup-coder-handoff.md:13`; `requirements.md:105` says a grant row and approval are still needed per issue. Confirmed.
- A.6 "never run live": `docs/designs/issue-watcher.md:3` still says never run live, `enabled` false, no schedule. Issue 450 is CLOSED 2026-11-24T13:00:34Z with a comment saying the watcher is live with 284 cycles and cron installed. `docs/designs/issue-watcher-setup.md:579` (14.1 live test) vs `:701` (section 17 automatic path) confirmed as headings that conflict.
- A.7 one local commit: `docs/designs/issue-watcher-status-pipelines.md:19` ("one local commit of the report") vs `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md:28` ("Make no commit, push no branch and open no pull request"). Confirmed.
- A.8 cadence: `docs/designs/issue-watcher.md:15` ("Every 5 minutes") and `issue-watcher-zero-setup-coder-handoff.md:23` (`*/5 * * * *`). I ran read-only `crontab -l` on this host: the `issue-watch run-all` entry is `* * * * *`. That settles the issue's UNVERIFIED point for this workspace (the Coder PR 526 itself is in another repository and I did not read it: UNVERIFIED). The docs are stale.
- B contradiction: `WORKER-CONTRACT.md:155,158` allow L4 restart on Orca's positive stall proof; `:303` says "relaunch a dead worker by itself (WC-6 and the person decide)" is never allowed; `:79` lets the coordinator settle a crashed attempt. Confirmed. Installed copy `~/.claude/WORKER-CONTRACT.md` is identical to the source copy.

## Complexity and size

Complexity **medium**, size **M**: about 20 files across docs, two docstrings, one pinned test, and three routing-guide copies that must stay byte-aligned, but no behaviour change.

## Priority

**P2** (the issue body itself says Low; I raise it one step because the restart contradiction can make two agents act differently on a dead worker): wrong text can mislead readers and agents (restart rule, approval, coordinator permission), but the watcher runs correctly and the ship gate is closed, so nothing breaks while it waits.

## Concrete next steps

1. Owner answers the four questions in the issue's Proposed Solution (confirm design stays under R38; which rule governs a watcher-claimed worker's restart and its budget; one change set after part B; update or annotate the backlog requirements). No work on B until then.
2. After the answers, one docs-only branch: fix A.1 to A.8 in the files listed above; keep `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (currently identical) and the level table in `src/superclaude/core/CLAUDE.md` together.
3. Update `tests/skills/test_issue_protocol.py:878-880` with the new Full sentence.
4. Update cadence text to every minute, citing the `crontab -l` evidence above.
5. Run `uv run pytest tests/skills/test_issue_protocol.py`, then the full suite, `make lint`, `make sync-dev` and `make verify-sync`; open the PR only through `/sc:pr-submit --monitor 3` (coordinator's action, not a worker's).
6. Link the setup-guide contradiction (`issue-watcher-setup.md` 14.1 vs 17) to issue 717 item W15 and leave the runbook rewrite to it.

## Dependencies

Needs: the owner's answers (item B and the requirements-file choice). Soft overlap with 717 (W15 owns the setup runbook rewrite). Blocks: none found.

## Related issues

450 (closed rollout tracker, source of the leftovers), 717 (open, W15 and fixture work), 761 (open, the gap check this issue came from), 707 is a PR (below).

## Related PRs

707 (merged 2026-11-20, zero-setup watcher), 735, 736, 752, 754 (merged 2026-11-23, coordinator wording). Coder PR 526 (cadence change): UNVERIFIED, other repository, not read. No open PR for 774.
