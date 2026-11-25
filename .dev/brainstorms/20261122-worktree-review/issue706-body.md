## Summary

Follow-up to [#409](https://github.com/IronbellyOrg/IronClaude/issues/409) (the TUI dashboard, `superclaude observe`). #409 stays open for this. The dashboard core is built and merged; these are the criteria that were added to #409 on 2026-11-13 from reviewer feedback and that have no code, no test and no owner ruling yet. Remote fleet is separate and stays in [#604](https://github.com/IronbellyOrg/IronClaude/issues/604).

## Priority

Not known yet: the owner sets it. The first item to decide is whether the dashboard should read the sweep report (item 1) because items 2 to 4 depend on where the data comes from.

## What was tried

Checked on 2026-11-20 against master (merge commit b68d5eeaf of #673 and the earlier releases #503, #514, #592):

- Built and merged: worker ledger, coordinator questions panel, Decision Desk, 160/116/80 layouts, NO_COLOR and ASCII output, unknown-is-not-zero display rules, bounded poll, read-only throughout. Visual parity was delivered by #606 (closed).
- Not built, found by searching the observer code and tests (`src/superclaude/cli/observe/`, `tests/observe/`) and the owner records under `.dev/issues/409/`: no per-session summary, no issue or pull request links, no named steps, no way to open a session, no use of the sweep report as a source, and no test at the 5/8/10-orchestrator and 50/80/100-session sizes (only the 80-worker and 54-row fixtures exist).
- Owner rulings found: the direction record of 2026-11-16 (worker list first, then questions, third screen later) and the decisions of 2026-11-08, 11 and 12. None of them rules on the items below.

## Items

1. **Same facts as the sweep.** The observer shows the same facts as the Orchestrator-mode sweep (`superclaude sweep run`), from one collection and classification, or documents every difference and the reason. Open decision in #409 "Alignment decisions" item 1: read the sweep's JSON (add the missing dimensions to schema v1 or make a v2) or parse the report.
2. **Plain-English summary per session.** What the task is, what is done, what is left, whether it needs the person. Needs GitHub reads and phase data that the sweep Phase 1 excludes (#409 alignment item 3).
3. **Issue and pull request links per session**, where they exist.
4. **Steps by name with state colours** (done, in progress, failed), not a retry count.
5. **Open a session from the view** (navigation only) through a supported Orca mechanism, or disclose that the view cannot do it. Native Orca deep links are unverified (#409 alignment item 4).
6. **Scale tests.** The 5/8/10-orchestrator and 50/80/100-session scenarios, including uneven ownership, shared or unmapped worktrees, historical records, duplicate and out-of-order events, stale sources and missing fields. One-to-one session to worktree mapping must not be assumed.
7. **Owner decisions still open in #409:** navigation only versus read-only recommendation text (alignment item 2), and whether the observer shows watcher state (item 9).

## Relevant files and links

- Parent: #409. Related: [#339](https://github.com/IronbellyOrg/IronClaude/issues/339) (Orchestrator mode and the sweep), [#534](https://github.com/IronbellyOrg/IronClaude/issues/534) (sweep Phase 1 follow-ups), [#604](https://github.com/IronbellyOrg/IronClaude/issues/604) (remote fleet backlog), [#606](https://github.com/IronbellyOrg/IronClaude/issues/606) (visual parity, closed).
- Observer code: `src/superclaude/cli/observe/` (`view.py`, `render.py`, `collector.py`). Sweep code: `src/superclaude/cli/sweep/`.
- Spec and rulings: `.dev/issues/409/bmad/spec-orca-observer/`, `.dev/issues/409/owner-direction-record-20261116.md`.
- User docs for what exists now: `docs/user-guide/observer.md` and `docs/user-guide/orchestrator-mode.md` (not yet merged when this was written).

## Fix approach

Start with the owner decisions for items 1, 5 and 7, because they decide the data source and the scope. Then build items 2 to 4 on the chosen source. Scale tests (item 6) can start now and do not depend on the decisions.

## Test plan

- Item 6: fixtures and tests at the listed sizes, run with `uv run pytest tests/observe/ -v`.
- Items 1 to 5: tests that each new field is shown from real data, shown as `unknown` when absent, and never invented; a test that the record and snapshot do not gain question text.
- A render check at 160, 116 and 80 columns, with NO_COLOR and ASCII, as in the #606 gates.

## Done when

- Each of items 1 to 6 is built, or the owner has ruled in this issue that it is dropped or moved, with the reason written down.
- Items 1, 5 and 7 have an owner ruling recorded in this issue.
- Nothing in the observer writes to Orca, and question text is still on screen only.
- #409 is then closed with a comment that links this issue.

## Pick-up note

The observer must stay read-only: no approve, dispatch, retry, merge or message path, and nothing sent through the issue watcher or a workspace listener. Do not present synthetic fixture fields as Orca API fields. Run the claim with `/sc:issue --claim <number>` from the orchestrator session.

