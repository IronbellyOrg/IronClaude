# Findings: issue 777 (map the watcher and coordinator chain, decide what to automate)

Checked 2026-11-24 against branch `ironbelly/Issuecleanup` (HEAD a7ae3dd30) and the live GitHub state of `IronbellyOrg/IronClaude` (read-only).

## Verdict

**still-relevant.** Nothing has been built or started for this issue.

Evidence:
- Issue 777 is OPEN, created 2026-11-24T18:43:42Z, label `enhancement`, no comments, no linked or closing PR (`gh issue view 777`: `comments: []`, `closedByPullRequestsReferences: []`).
- No whole-chain map exists. Title searches of all issues for "whole chain", "life cycle map manual", "moving pieces", "per-issue map watcher coordinator" and "gap 7" returned only 777 itself plus its own neighbours (761, 770, 773, 775, 774, 781, 716, 718). Title searches of all PRs for "watcher coordinator map", "manual steps" and "life cycle" returned no map PR. A text search of `docs`, `.dev/releases` and `.dev/issues` for "manual by design", "manual by gap" and "moving pieces" returned nothing, and `docs/designs/` has no map or life-cycle file. This supports the issue's claim but is **UNVERIFIED as an absolute absence**: PR and issue bodies, review comments, and plan files outside those three folders were not searched, which is the cross-search the issue itself says would settle it. Whether 773's "Moving pieces" section exists as the issue describes was not read (UNVERIFIED; issue 773 matched the search "moving pieces").
- The design the map must respect is merged and unchanged: PR 707 MERGED 2026-11-20T22:09:24Z (merge commit 2ea524514); owner ruling R38 is at `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64` (keeps cron and one dispatcher, one coordinator per project, a person's typed go for every push and merge).
- Every piece the issue lists exists in code. Ship gate: `src/superclaude/cli/issue_watch/launch.py:48` `GOVERNED_LEVELS_ALLOWED = False`. Pipeline mapping: `launch.py:55-61`. Coordinator verbs in `src/superclaude/cli/issue_pipeline/cli.py`: `plan-hash` (62), `check-approval` (77), `adopt-create` (109), `adopt-mark` (118), `record-create` (135), `record-mark` (180), `complete` (226), `stage-status` (409). The coordinator duties are in `src/superclaude/core/WORKER-CONTRACT.md` (section "Issue pipeline duties"). The claim store `dispatch.json` is handled through `src/superclaude/cli/issue_watch/dispatch.py` and `record.py`.
- All reading sources named in the issue exist: `docs/designs/issue-watcher.md`, `docs/designs/issue-watcher-status-pipelines.md`, `WORKER-CONTRACT.md`, `dispatch.py`, `launch.py`, `issue_pipeline/cli.py`, and the R38 requirements file.
- The six suggestions the map must cross-reference are all still OPEN with no PRs (live state at check time): 770, 771, 772, 773, 775, 776. Also OPEN: 716, 733, 722, 698, 727, 761. 655 is CLOSED as NOT_PLANNED (2026-11-23).
- The `/sc:analyze` quick run on `src/superclaude/cli/issue_watch` is at `.dev/issuecleanup/g7/777/analyze/analyze-report.md` (codegraph fresh); it changed nothing in this verdict.

Open-questions status: the issue's three questions (owner of the map, its location, re-review after 773, 776, 770, 775) have no answers recorded anywhere (no comments on the issue). The issue's own acceptance rule says not to assume answers.

## Complexity and size

Complexity: **simple**. Size: **S**. One documentation file under `docs/designs/` that reads existing code and docs, with no behaviour change; the work is careful reading and labelling, not engineering. (It touches many sources, so the reading is the cost; M is possible if the reviewer insists on checking every step against code.)

## Priority

**P2.** The issue is labelled High by the owner, but it is documentation only and blocks no code. It does inform which of the filed automation issues (770, 773, 775, 776) to build first, so raise it to P1 only if the owner wants the map before those are scheduled.

## Concrete next steps

The issue is not started; these are the steps, in order, matching the issue's Fix approach:

1. Get the owner of the map and its location from Ryan and Clay (open questions 1 and 2). Suggested home: `docs/designs/`. Do not choose for them.
2. Finish the cross-search for gap 7 (PR and issue bodies, review comments, plan files) and record the result; keep the absence claim UNVERIFIED until it is done.
3. Read the six sources in the issue and write the filing-to-merge map in the agreed file. Include every piece listed in the issue's Problem Statement (watcher, claim tab, standing coordinator, worker, the two stores, two approvals, per-issue grant, ship gate, board fields Status, Pipeline, assignment, trigger label). Label each step automatic, manual by design, or manual by gap. Keep today's behaviour apart from proposals.
4. Link 773, 776, 770, 775, 772, 771 beside the steps they would remove; keep 733 and 716 at their stated scope.
5. Present the three open questions to Ryan and Clay; ask which gaps first. Run `uv run pytest`, `make lint`, `make verify-sync` and record results (not run here).

## Dependencies

- Needs: none that block writing. Answers to its own open questions 1 and 2 (the owner and the file location) are needed before step 3.
- Blocks: nothing hard. It informs prioritisation of 770, 771, 772, 773, 775, 776.
- Reading dependency: the map should say that 774 (docs refresh of stale watcher statements) is open, because 774 lists wording the map would otherwise repeat, such as "Nothing manual" and "person-opened coordinator".

## Related issues

- 761 (gap list; gap 7 is this issue), 773, 776, 770, 775, 772, 771 (the suggestions to cross-link), 716 (coordinator features, claim and store baseline), 733 (plan approval removed on the unattended `/sc:implement` route only), 722 (shared GitHub login), 698 (approver rule and text-matching checks), 727 (dashboard, out of scope), 774 (docs refresh, overlaps in wording), 781 (contact agents, out of scope neighbour), 655 (rolled back, CLOSED NOT_PLANNED; not to be adopted).

## Related PRs

- PR 707 (MERGED 2026-11-20, merge commit 2ea524514): the zero-setup watcher and coordinator the map describes. No open PR addresses this issue. PRs 735, 736, 752 and 754 (merged 2026-11-23) are named by issue 774 as already fixing person-opened coordinator wording; not checked here (UNVERIFIED by this review).
