# Findings: issue 770 (watcher hands each claim to the coordinator, results come back)

Checked 2026-11-24 on branch ironbelly/Issuecleanup at a7ae3dd30 (master after #754). Issue is OPEN, label enhancement, opened by clayphi 2026-11-24, zero comments.

## Verdict

**still-relevant.** Every gap the issue records is still real on the current tree; nothing is done and no PR works on it.

- Claim launch sends the coordinator nothing: `src/superclaude/cli/issue_watch/launch.py:136-157` (`launch_argv` builds `orca agent launch ... --surface terminal`, `--surface` at line 152). The watcher's only claim write is `record.mark_claimed` (`cycle.py:959`, defined `record.py:654`), which writes `dispatch.json` and notifies no one.
- No verb lists claims: `src/superclaude/cli/issue_pipeline/cli.py` has plan-hash, check-approval, init, adopt-create (line 109), adopt-mark (118), record-create/show/mark, release-worker, complete (226), stage-status (409). Grep for `unadopted|list-claims|wake` in issue_pipeline and issue_watch: no match.
- Contract line 296 names sources but no trigger or wake step; line 302 and `docs/designs/issue-watcher-status-pipelines.md:75` say `result.md` is "noticed through the `/sc:sweep` report": confirmed in `src/superclaude/core/WORKER-CONTRACT.md:302`.
- Sweep does not read it: grep for `result.md|dispatch.json|claimed` over `src/superclaude/cli/sweep/`, `src/superclaude/skills/sc-sweep-protocol/` and `src/superclaude/commands/sweep.md` returns no match. So the documented behaviour does not exist.
- Live-test record `docs/designs/issue-watcher-live-test.md` does not exist (ls fails). Issue 450 (closed) closing comment lists it as a leftover and says issue 717 carries it.
- Real state of the watcher: merged in PR 707; live on the host (284 cycles per the 450 closing comment, UNVERIFIED by me: host not readable). Ship gate closed: `GOVERNED_LEVELS_ALLOWED = False` at `launch.py:48` (used `cycle.py:1032`), so only Pipeline None claims launch today. This narrows urgency for the result.md path (levels worktree/full/full submit launch their own agent and write result.md) but not for the claim-adoption path.
- The issue's Coder claim (coordinator-ensure line 37, Coder#516 wording) is in another repo: UNVERIFIED.
- Whether any issue has passed the whole chain live: UNVERIFIED (needs host `audit.jsonl` and `dispatch.json`).
- Option (a) overlaps open issue 757, which is in-progress (backlog review 2026-11-24: Complex/L, P2) and already received clayphi's comment asking for exactly this.

## Complexity and size

Complexity: medium. Size: M. One small link (list verb plus wake step, or a hook into the 757 wake task) with tests and a doc alignment, but blocked on a design choice and the live-run record needs the host.

## Priority

P1. The issue says High: a claim waits for a person before any worker starts, which defeats the watcher. It is held down from P0 because the ship gate keeps governed levels off, so impact is limited to level-None claims, and option (a) may land inside 757.

## Concrete next steps

1. Owner or Ryan chooses (a), (b), (c) or a mix. Recommendation: (a) via 757 for the wake, plus the small list verb from (c) so the wake has something to call.
2. Store claim listing on the existing `dispatch.json` (`record.py`); no second store.
3. Add the list verb to `issue_pipeline/cli.py` (unadopted claims, new `result.md`), tests in `tests/issue_pipeline/` and `tests/cli/test_issue_pipeline_registered.py`.
4. Add the wake-time step to `WORKER-CONTRACT.md` near lines 290-302; either make the sweep read `result.md` (`cli/sweep/probes.py`, `models.py`, `report.py`, skill and command text, `tests/sweep/`) or correct line 302 and `issue-watcher-status-pipelines.md:75` to name the new path.
5. Record one live run (cron tick, claim, adopt, worker, `issue-pipeline complete`) in `docs/designs/issue-watcher-live-test.md`; merge with issue 717 to avoid duplicate work.
6. Run `uv run pytest`, `make lint`, `make verify-sync`.

## Dependencies

Needs: 757 (option a), a decision from Ryan; live record needs host access and overlaps 717 and 761's list. Constrained by 755 (one inbox per Run decides where a claim notice is read). Blocks nothing recorded.

## Related issues

757 (scheduled wake, open), 755 (multiple Runs, open), 716 (coordinator gaps, open), 590 (sweep needs parsed contract, open), 761 (parent gap list, open), 450 (rollout tracker, closed), 717 (live-test and fixtures, per 450 comment; state UNVERIFIED), Coder#516 (UNVERIFIED, other repo).

## Related PRs

707 (merged, watcher and ship gate), 591 (merged, coordinator handoff Plan B), 584 (merged, approval core Plan A), 729 (merged, R38 docs), 735 (merged, one coordinator per project), 754 (merged, docs). No open PR addresses 770.
