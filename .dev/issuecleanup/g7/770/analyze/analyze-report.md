# /sc:analyze report: src/superclaude/cli/issue_watch (architecture, quick)

Codegraph: index_state=fresh, checked_at=2026-11-24T20:41:34Z; degraded: none

## Layout
- issue_watch (watcher): cycle.py (poll cycle; calls record.mark_claimed at cycle.py:959), launch.py (builds `orca agent launch`; ship gate `GOVERNED_LEVELS_ALLOWED = False` at launch.py:48), record.py (dispatch.json store; `claimed` state, mark_claimed at record.py:654), dispatch.py (cron sweep runner), first_run.py (automatic first-run check).
- issue_pipeline (coordinator side): cli.py verbs plan-hash, check-approval, init, adopt-create, adopt-mark, record-create/show/mark, release-worker, complete, stage-status. No verb lists claims.
- sweep: classify, commands, models, probes, report. Grep for `result.md|dispatch.json|claimed` over cli/sweep, skill sc-sweep-protocol and commands/sweep.md: no match.

## Findings
1. (High) Watcher-to-coordinator link is absent. launch_argv (launch.py:136-157) only starts a terminal agent; nothing messages or marks the coordinator. WORKER-CONTRACT.md:296 names sources to read after adoption but no trigger or list command.
2. (High) Contract WORKER-CONTRACT.md:302 and docs/designs/issue-watcher-status-pipelines.md:75 say result.md is "noticed through the /sc:sweep report"; the sweep code never reads it. Documented behaviour does not exist.
3. (Medium) Live-test record docs/designs/issue-watcher-live-test.md does not exist.
4. (Info) Ship gate closed: only Pipeline None launches governed levels are blocked (launch.py:48, cycle.py:1032).

## Recommendation
Choose link option (a) wake task (issue 757), (b) hand-off via coordinator, or (c) list verb plus wake step; reuse dispatch.json (record.py).
