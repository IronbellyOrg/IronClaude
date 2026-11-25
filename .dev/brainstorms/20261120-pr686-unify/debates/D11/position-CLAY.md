# D11 position paper: CLAY (Clay's line)

Topic: Observability stack: work report, sweep, observer, TUI dashboard.

"M:" means the read-only export of origin/master 61ac2c2e6 at `/home/coder/.cache/ic-snap-20261120/master`.

## The claim

The thing the person actually reads each day already exists, is tested and is on master: the work report (PR 684 "move the agent-work-report skill into IronClaude and add the living report", merged 2026-11-20 02:01 UTC). It gives, per issue, a plain-English summary, what is done, what is left, whether it needs the person, and a link to the PR or issue. That is exactly what the owner's issue 409 asks for in Clay's reply of 2026-11-11 and in "Requirements from reviewer feedback". The sweep cannot produce it (no GitHub reads, no summary text) and the observer has not built the screens that would show it (Decision Desk is "NOT BUILT"). So the unified stack should keep the report as the work-item layer, add the nine-row table and the cap of 5 notices a day to the whole stack, and let the sweep and the observer feed or read it where they overlap. Do not hold working code until a contract note and a schema change exist.

## The mechanism

1. One entry file per issue the orchestrator holds, in `.dev/coordinator/orchestrated/`; the daily run leaves those issues out (`exclude.py`, Step 4b) so nothing is reported twice, and `run.py refresh` rebuilds the shared page from the last daily report plus the entry files with no model call (M:src/superclaude/skills/agent-work-report/SKILL.md, "The living report" and Step 12).
2. Everything else is joined into one item each (`match.py`), sorted by fixed rules (`classify.py`), compared with the previous report (`compare.py`) and checked by script before delivery (`check.py`, then `run.py gate` prints PASS). "No report that failed a check reaches Clay" (SKILL.md Step 11).
3. A person-facing rule for escalation: one table of nine rows says what may reach the person; anything else the orchestrator decides and records; a notice (DM or unread mark) is capped at 5 per repo per 24 hours; the entry on the page is never dropped (M:docs/designs/orchestrator.md:664-696, 1164, 1177).

## Cited facts

1. The report answers the 409 asks. Issue 409 comment of 2026-11-11 (by `clayphi`): "a simple plain english summary of the task/issue, whats done, whats left to do, and if it needs me. Link to the pr/issue". `templates/item-template.md` (73 lines) lays out state (one of nine), priority, Done with evidence, Still to do, Needs you, Next, links; `check.py` fails an item that departs from it (M:src/superclaude/skills/agent-work-report/SKILL.md:10).
2. The sweep and observer have the gap on their own record. Issue 409 "Alignment decisions" item 3: the reviewer's asks "need GitHub reads and phase data. Phase 1 excludes GitHub reads, and the sweep has no per-session summary text. Decide which phase adds them". The sweep allows only Orca and worktree commands (M:src/superclaude/cli/sweep/probes.py:49-56) and has no GitHub call (grep for `gh` and `api.github` in `cli/sweep/*.py` finds none).
3. It is built and tested. PR 684 adds 10,488 lines in 28 files, moves the IronFlow test (102 cases kept) and adds 28 cases (PR 684 body); `tests/skills/test_agent_work_report.py` has 142 test functions and 4,005 lines (M: `grep -c "def test"`). The waker automations were "VERIFIED 2026-11-03" (SKILL.md Input section). The page is served at 127.0.0.1:8765 and opened as a tab in Orca (Step 13), so a working human-facing page exists today.
4. It prevents silent loss. "Every item open in the previous report is listed or closed with a reason the source confirmed; a failed read carries items, never closes them"; every source not read is listed under "Not checked"; an unanswered "Needs you" entry stays until answered (SKILL.md "Why This Process Works").
5. It reads what the sweep does not: GitHub items across both orgs and Projects boards, ClickUp tasks, DM replies and each session's transcript from where the last report stopped (prompts, errors, repeated steps, last event; M:.../scripts/sessions.py:1-28). The sweep reads only a 256 KiB transcript tail for classification (M:src/superclaude/cli/sweep/probes.py:865-867).
6. The nine-row table and the cap are not duplicated by anything. The sweep has a class "waiting on a person" but no reason list (M:src/superclaude/cli/sweep/report.py:233,284 splits waiting by kind a or b only). The table is test-pinned in the design plan ("exactly nine rows", M:docs/designs/orchestrator.md:1116) and sets "when in doubt, a case does not reach Clay" (line 668). The cap is settled by ruling 39 (line 1164, OD13) and never drops an entry (line 1177).
7. The living report costs no model call: `run.py refresh` rebuilds the page from the last daily report plus entry files "with no model call" (SKILL.md line 16), so only the daily run spends tokens and the sweep's 5-minute cadence is not slowed by it.
8. The two other pieces have not delivered the unification either. `observe/` has no reference to `sweep`, and the contract note `docs/designs/observe-sweep-contract.md` does not exist (find over the master export). Waiting for one data source delays a daily tool that works now.

## What it costs

- One more place a person reads (page, DM, session summary) beside the sweep report and the TUI.
- The report is tied to one person today (`config.json` has `"person": "clayphi"`, a ClickUp token, America/Chicago), and its model step costs tokens each day.
- PR 684's skill still says `/sc:orchestrator` and `.dev/coordinator/` (singular), which the owner's naming and layout decisions (coordinator, `.dev/coordinators/`) have not yet cleared.

## What it risks

- Three overlapping readers of Orca sessions (sweep, observer, `sessions.py`) can disagree about one session's status; the report uses its own status words (working, progressed, waiting on you, stuck, stalled, done) against the sweep's eight classes.
- The report's DM and commit steps are writes the sweep and observer rules forbid.

## What CLAY gets right

It is the only piece that already gives a person the plain-English "what is done, what is left, does it need me" per issue that the owner's own dashboard issue asks for, with a script gate that stops a bad report, and it fills three gaps the owner's work leaves open: the reason list for "needs a person", the cap on notices, and one living entry per issue.

