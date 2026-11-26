## Verdict
**still-relevant.** Keep #706 open. This is unfinished follow-up work on an existing dashboard, not an absent dashboard and not evidence of an active feature implementation PR. The parent #409 explicitly remains open until #706 is completed or its remaining scope is dropped/moved by the owner (parent comment of 2026-11-20, still present at this review).

Reviewed on 2026-11-24 at checkout commit `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`. File citations below are relative to `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`.

- **Built:** worker ledger, coordinator questions and Decision Desk, with visual parity, delivered in merged PRs #503, #514, #592 and #673. The live question and question-link switches are now on (`src/superclaude/cli/observe/commands.py:63-70`). PR #708 merged the two user guides; PR #730 preserved records, not new observer capabilities.
- **Still missing:** a shared sweep input/classification or explicit reconciliation of differences; task/done/left/person-needed summaries; issue/PR links; named workflow-step state display; session-opening navigation. The observer uses its own worker-list/question templates (`src/superclaude/cli/observe/adapter.py:29-32`) and collection/parse/merge loop (`src/superclaude/cli/observe/collector.py:274-319`), not sweep output. Its Row model has raw stage/activity/detail fields, but no requested summary/URL/workflow-history model (`src/superclaude/cli/observe/parse.py:110-157`); those raw fields are available in inspector detail (`src/superclaude/cli/observe/view.py:491-510`). Enter opens the local inspector, not an Orca session (`src/superclaude/cli/observe/view.py:1246-1300`).
- **Correct the issue's scale claim:** it says only 80-worker and 54-row fixtures exist and there are no required-size tests. In fact, `tests/observe/test_render.py:99-118` already parameterizes 5/8/10 Runs against 50/80/100 rows at 160/116/80 columns, 27 combinations. Its generator spreads synthetic rows across Runs (`tests/observe/conftest.py:179-188`), not verified live coordinators. Separate collector tests cover uneven/shared/unmapped/history/missing-field variants and duplicate/out-of-order observations (`tests/observe/test_collector.py:381-417`). This is partial satisfaction, not proof of every scenario crossed with every size or of live fleet performance; that full acceptance remains **UNVERIFIED**.
- **Three guide corrections from the issue's 2026-11-22 comment are still needed:** `docs/user-guide/orchestrator-mode.md:24` omits parallel experiments from the separate-worktree rule; `src/superclaude/core/WORKER-CONTRACT.md:47` explicitly requires that separation. `docs/user-guide/observer.md:47` does not disclose that FROZEN is fixture-only; the model and view restrict it to that mode (`src/superclaude/cli/observe/parse.py:157`, `src/superclaude/cli/observe/view.py:560-564`). `docs/user-guide/observer.md:103,123-126` implies a new export file each time, but `src/superclaude/cli/observe/export.py:247-267` builds a timestamped path and atomically replaces it. Two exports with the same second-level generated timestamp reuse the path.
- **New direction must be reconciled, not ignored:** #727, filed 2026-11-22 with the owner's quoted direction, plans a two-way dashboard and gives preliminary architecture/storage evaluation precedence over its release list. It does not implement #706's missing fields, supply a supported navigation contract, or authorize this read-only review to add writes. #706's current no-message/no-dispatch and screen-only question-text constraints remain the implementation baseline until an explicitly scoped replacement contract is approved.

Evidence limits: no tests or live dashboard were run, as the brief prohibits environment/test side effects. Historical PR test counts were read but not re-verified. Bounded PR searches for 706 and observe found no additional pending capability PR; this does not prove an exhaustive GitHub event timeline. Unseen branches, timeline-only links, native session deep-link support and full cross-scenario coverage are **UNVERIFIED**. One sweep Grep attempt failed with EACCES; a subsequent dedicated Glob and Read of the sweep model recovered that inspection. The requested static analysis completed at `.dev/issuecleanup/g4/706/analyze/analyze-report.md`.

## Complexity and size
**complexity: complex; size: L.** The remaining work crosses data-source ownership, schema evolution, session/issue association, missing-evidence presentation, navigation verification and cross-scenario tests; the three guide edits alone are small, but are not the whole issue. This is a provisional scope estimate, not a measured duration; #727's preliminary evaluation may change the approved solution.

## Priority
**P2.** Missing explanations and links weaken oversight and block completion of parent #409, but the existing read-only ledger/questions remain available and no P0/P1 outage, data loss or urgent failure was established. This is a review recommendation, not a claim that the owner already assigned this priority or scheduled implementation.

## Concrete next steps
1. **Reconcile the backlog before feature coding.** The coordinator should bring #706's unresolved source/scope choices into #727's owner-directed preliminary evaluation: sweep JSON versus explicit documented differences, ownership of summaries/links/step data, navigation support versus disclosure, recommendations and watcher-state visibility. Do not treat either issue's proposal as an already selected API or storage design. Record the owner's resulting decisions in chat and then in the issue/spec through the coordinator after the owner's go.
2. **Apply the three already identified guide corrections as a separate bounded documentation change.** Add the parallel-experiment child-worktree case; identify FROZEN as fixture-only; disclose same-second export replacement rather than promising a distinct file per press. Check the first against the worker contract and the other two against model/view/export code. No observer behavior change is needed merely to correct those guide sentences.
3. **Map scale acceptance to existing tests first.** Reuse the 27 rendering size/width combinations and the separate edge-case fixtures. Identify which required size-by-ownership/history/ordering/staleness/missing-field cases lack coverage; add only those and any explicitly agreed live capacity checks. Do not call synthetic Run counts actual orchestrator capacity.
4. **After the source/scope decisions, implement the approved missing fields in one authoritative path.** Extend the selected model, parser/collector, view/render and record/snapshot contracts only as agreed. Display missing data as unknown, not invented summaries or ownership. Existing raw stage/activity detail is not a substitute for named workflow steps with state.
5. **Verify navigation before promising session-open links.** Use only a documented supported mechanism or explicitly disclose inability to open sessions. No deep-link scheme or terminal identifier was verified in this review. Keep #706's no-approve/no-dispatch/no-retry/no-merge/no-message boundary unless the owner explicitly replaces that contract in the later roadmap; keep payload question text out of existing exports (`src/superclaude/cli/observe/export.py:158-180`, `tests/observe/test_export.py:312-337`).
6. Validate the resulting implementation at the existing widths and colour/ASCII modes and review every #706 item, including its November 22 comment. Close #706 and then parent #409 only after their acceptance is met or the owner explicitly drops/moves remaining scope. This task performed no GitHub edits or closures.

## Dependencies
- **Blocks #409 closure:** the parent explicitly delegates the unfinished local criteria to #706 and stays open until they are resolved.
- **Needs owner decisions, not wholesale completion of another issue:** shared-source shape and scope, navigation support/disclosure, recommendations and watcher-state visibility. #727 now supplies an overarching preliminary evaluation and two-way direction; reconcile the overlapping choices there, but do not make all documentation/test progress wait for completion of the entire roadmap.
- **Related source work #339 and #534:** sweep and its follow-ups matter if sweep data is selected. No evidence here makes closure of either whole issue a prerequisite to all #706 work.
- **#606 is satisfied:** visual parity is CLOSED and its implementation PR #673 is MERGED. It is not a remaining blocker.
- **#604 is separate:** remote fleet is OPEN and explicitly deferred; it is not a prerequisite to the local follow-up in #706.
- **#718 is not a required predecessor:** its report-entry-link work overlaps conceptually, but the 2026-11-22 owner comment parks the work-report tool and holds its first two items. Do not make #706 depend on restoring that separate tool.
- Structured GitHub dependency edges were not queried under the brief's read-only verb restriction; they are **UNVERIFIED**. The relationships above come from live issue text/comments, not an inferred GitHub dependency graph.

## Related issues
- #409, OPEN: parent TUI dashboard and original acceptance/owner direction. Its older body has stale implementation statements; current source and later comments take precedence.
- #339: agent-facing orchestration and sweep. Referenced by #706 and parent #409; current full body/implementation not re-audited here, so its complete present status is **UNVERIFIED**.
- #534, OPEN: sweep Phase 1 follow-ups, relevant to shared-source design rather than an automatic dependency on every item.
- #604, OPEN: separate remote fleet backlog, with a cross-host ownership gate.
- #606, CLOSED: completed visual-parity work.
- #718, OPEN: report/dashboard-view gaps from the issue 655 split; owner has parked the report-tool-dependent work. This is not a duplicate of the local observer capabilities here.
- #726, OPEN: intervention votes and local decision records, adjacent future work, not already implemented by this issue.
- #727, OPEN: later owner-directed roadmap for a two-way dashboard; preliminary architecture and storage evaluation takes precedence over its release list. Reconcile boundaries rather than silently treating #706's read-only constraint as permanent for all future work.

Live issue bodies/comments for #706, #409, #534, #604, #718, #726 and #727 were read; #606 state was read directly. Other repositories were not accessed. PR-search results and issue-list hits were treated as leads, not proof of implementation.

## Related PRs
Each row below was read directly using `gh pr view` against IronbellyOrg/IronClaude. All are MERGED; merge dates and commits are GitHub's returned values, not inferred from issue prose.

| PR | Contribution and remaining boundary | Merge date | Merge commit |
|---|---|---|---|
| #503 | Release 1 worker ledger and observer pipeline, not session summaries/links | 2026-11-11 | `9e2608b03857c78ab89fc9439c85256d3bd5d989` |
| #514 | Release 2 one-Run coordinator questions, initially live-disabled | 2026-11-12 | `cd873619957b3fd4235c54f00363664fca28a193` |
| #592 | Release 3 question text, verified dispatch join and Decision Desk | 2026-11-17 | `3206bdb9cb6b0fe3c81e6cdbeadcc1455aeeffda` |
| #673 | Visual parity at 160/116/80 columns for #606 | 2026-11-19 | `b68d5eeaf618a8e33cde55cb660acfdd8f321f67` |
| #708 | User guides only; its three unresolved guide findings were added to #706 in the owner's November 22 comment | 2026-11-20 | `52d371e2c20a32a4c17613108daa7f0a295baa36` |
| #730 | Preserved existing research, specs and review records, not observer code | 2026-11-23 | `98879e631e6d7986d14c0dc94720007cbb2fde0b` |
| #539 | Agent-facing read-only sweep, not integration into observe | 2026-11-14 | `4d3c0b126151789bd0cb5b481b10f572a0c4e6b7` |

PR #708's body, reviews and ordinary comments were read. The original inline threads named by #706 could not be fetched through the brief's allowed `gh pr view` JSON fields; their exact thread state is **UNVERIFIED**. The three substantive claims were instead checked against current guides, source and worker contract. No pull request or issue was edited, linked, commented on, labeled or closed. No local commit was made.
