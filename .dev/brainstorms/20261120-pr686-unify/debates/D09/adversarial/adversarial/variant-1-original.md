# Position OURS: D09 watcher writes to GitHub

Advocate for the owner's line. Snapshot paths are under `/home/coder/.cache/ic-snap-20261120/`.

## Claim

The poll stays read-only on GitHub (NG-2 and decision D2 stay as written). Every GitHub write stays with the coordinator, under a per-issue grant, after a human approval. The plan hold is not a reason to give the poll write rights: the part of Clay's hold that is worth having (a mechanical "does the issue have a plan" check) works without any label write.

## Mechanism

1. The owner's gate is a person: the `Approved` issue field set to `Yes` (requirement R35) plus the trigger label. A person looks at the issue before anything launches, so "is the issue ready" is already answered by a human in the same step.
2. The poll reads, decides and wakes or launches. It never writes. The one write path is the coordinator's, which needs that issue's grant row (R24, `WORKER-CONTRACT.md`), so a write always has a named, recorded reason.
3. A hold that only needs to be seen by the owner can be shown in `superclaude issue-watch status` and the audit log, which the owner already reads. No GitHub label is needed for that.

## Cited facts

1. NG-2 is a binding non-goal: "no GitHub write (REST GET only; GraphQL POST only with a constant query without `mutation`)". Source: `/home/coder/.cache/ic-snap-20261120/master/docs/designs/issue-watcher.md:76`.
2. Decision D2 (owner): "the poller itself never assigns, comments or moves Project items" and it "still never reads the approval"; it was restated after both supersessions of 2026-11-14 and 2026-11-17. Source: `issue-watcher.md:41-43` and `:48`. (D2 names assign, comment and Project moves; NG-2 is the stricter rule that covers labels.)
3. NG-2 is enforced by tests, not by prose: master `tests/issue_watch/test_security_invariants.py:10` ("nothing writes to GitHub (no `mutation`, no POST to a REST path)"), `:245-251` (no `mutation`, argv scan for `--method`), `:693-698` (every REST argv carries `--method GET`). The design notes why: `gh api --help` makes a call a POST once parameters are added (`issue-watcher.md:561`).
4. Owner requirement R24 repeats the boundary for new writes: all completion writes are the coordinator's, need the issue's grant row, and "live in `src/superclaude/cli/issue_pipeline/`, never in `issue_watch/github.py` (read-only, NG-2)". Source: `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:50`.
5. Owner requirement R11 and R14: the watcher never creates labels; a missing label is reported by the loop, not fixed by the poll. Source: same file, lines 34 and 42.
6. Workers never write to GitHub (WC-9) and only the orchestrator writes in `sc-issue-protocol`: `src/superclaude/skills/sc-issue-protocol/refs/claim.md:9` ("Only the orchestrator writes to GitHub or ClickUp"). The least-privilege split is consistent end to end; a poll with write rights is the one place that would break it.
7. The poll runs unattended from cron every few minutes with no person present. A write that is wrong (wrong label, wrong repo, a bug in `plan_check`) repeats every cycle until noticed. A read-only poll cannot do that. Clay's own design admits the search index "can show a label one cycle late" and adds a live read to compensate (`/home/coder/.cache/ic-snap-20261120/master/docs/designs/orchestrator.md:494`, limit (a), and row 5 at `:456`): the write path creates a consistency problem the read-only poll does not have.
8. Size of what the label write drags in: section 4.11 is about 60 lines of rules (`orchestrator.md:436-495`), a `holds` store with four states, four evidence reads (E1 to E4), eight new audit reasons (`:340`), a label writer (`:410`), and `test_hold.py` with 111 hold-related matches in PR 686 (`/home/coder/.cache/ic-snap-20261120/pr-a/tests/issue_watch/test_hold.py`). The poll becomes stateful about issues it has not even claimed.
9. Clay's ruling 33 says "hold label only, no comment (as Jay does)". The comparison to Jay's system is not a source we can check here (UNVERIFIED), and a label is still a write by an account (`ironbelly` is the shared login on this host), so it shows no sign of who acted (FULL-REPORT section 1, item 7).

## What it costs

- A plan-less assigned issue is not visibly marked on GitHub. The owner sees it only in `status`, the audit log or the coordinator's report.
- Without the one-hour plan request, a plan-less issue waits until a person or the coordinator acts.

## What it risks

- If the human approval gate is dropped later (Clay's R1: assignment is the only trigger), nothing blocks an empty issue except a mechanical check. That is a reason to keep the human gate, not to widen the poll.

## What it gets right

- Keeps the one security property the owner built and tested: the unattended component cannot change GitHub state.
- Needs no new GitHub scope for the poll and no label created at runtime (R11).
- Keeps the audit trail clean: every write has a grant row and a person behind it.

## Honest concession

The pure function `plan_check(body)` (`orchestrator.md:440`) reads text only and calls no GitHub write. It fills a gap OURS has (no early check that an issue has a plan before a launch is spent). OURS can take it and the `held_incomplete` skip reason as read-only changes. What OURS does not accept is the poll writing the label or sending a plan request on its own timer.
