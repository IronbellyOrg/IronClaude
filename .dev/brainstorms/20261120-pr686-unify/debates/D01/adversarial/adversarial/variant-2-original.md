# Position CLAY (D01): assignment is the only trigger; no approval label, no approver list, no plan-approval gate

Paths: `SNAP` = /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6, includes Clay's merged design); `PRA` = /home/coder/.cache/ic-snap-20261120/pr-a (PR 686, Clay's rewrite of the watcher, head 8e5ae29ad); `DESIGN` = `SNAP/docs/designs/orchestrator.md` (cited D:nnn, merged in PR 681); `REQ` = the owner's zero-setup requirements file in worktree `claim-handoff-planb`.

## The claim

An issue assigned to the user is the only trigger. A person who assigns an issue has already decided the work is theirs and wanted; asking for a second human act (a trigger label, an approval label or field, an approver list, a Backlog column, a plan-approval gate after the claim) is a burden that defeats the purpose of the system, which is that nobody starts the work by hand. Readiness is checked by a script that reads the issue body (the plan check), and a person keeps a veto with `hold:backlog`. The plan is reviewed at creation, not again before building.

## The mechanism

1. R1 (D:73): "Assignment is the only trigger: no trigger label, no approval label, no approver list, no plan-approval gate after the claim. The hold of 4.11 is a precondition, not a trigger ... no person has to set or approve anything for work to start (a person may stop an issue with `hold:backlog`), and the check is a script".
2. DQ1 (D:111): only the user's own login counts; the issue must be open, not a PR, the user is an assignee and no one else is; any co-assignee gives `assigned_other`.
3. The poll finds issues with one GitHub search per login and org, `is:issue is:open assignee:<login> org:<owner>` (`PRA/src/superclaude/cli/issue_watch/github.py:165-168`, `DESIGN` ADD3 line 137), filters on the repo list, and routes each to exactly one orchestrator (`PRA/.../route.py:512-559`).
4. The hold (4.11): `plan_check(body)` requires `## Priority`, `## Fix approach` and `## Test plan` present once and filled (`PRA/.../hold.py:122-143`); an issue that fails gets `hold:plan` and is not woken; one hour of quiet then sends a plan request that makes the plan via `/sc:issue --plan`.
5. Safety moves from "a person approves" to bounded automation: repo allow-list (D:134 OQ6), day cap, 3 issues in flight per orchestrator (D:55), 62 audit reasons, the nine-row escalation table (D:664-696), merge only when every condition holds with `--match-head-commit` (D:118, ADD5 line 139).

## Cited facts

1. **A decision was posted before the build, addressed to the owner.** Clay's #450 comment of 2026-11-18 17:00:32 is addressed to `@ironbelly` and ends "What do you think?" (FULL-REPORT.md section 1 point 4; `E-pr682.md:54`). Issue 655 (filed 19:55 the same day) states the dropped layers and the reason ("the plan is reviewed at creation", `E-pr682.md:46`). So the change was proposed in writing, not hidden.
2. **The approval gate has a documented weakness that makes it weaker than it looks.** Accepted risk L-1: an agent on the same GitHub login can apply the approval label (`E-pr682.md:75`); the whole trust set is one login on this host (FULL-REPORT.md header). A gate that the same login can pass is a speed bump, not a person.
3. **It was never run live.** The watcher is `enabled: false` and "never ran live" (PR 682 body, `E-pr682.md:43`); the handoff had one throwaway-issue test (issue 452, `E-pr682.md:74`). So "removing a protection" removes an untested protection.
4. **The owner's own goals point at less manual work.** Issue 339 says "no sessions should be run interacted with manually" (`H-design681-map.md:66`); the zero-setup requirements say "needs no setup by the person using it" (`REQ` line 9) and R18 turned the manual switch-on into an automatic check. The approval is one of the few manual gates left (`REQ` lines 102-104).
5. **The owner already moved toward fewer gates.** R35 (line 61) turned the label into a field; R36 (line 62, 2026-11-20) withdrew the rule that voided approval after a Status or Pipeline change; the Q36 latency was accepted only "for now" (`E-pr682.md:76`). The approval step also needs two sessions and a grant row per approval (`E-pr682.md:76`).
6. **The claim-time trust set is the same as the approval trust set.** Triage-or-write users can assign (D:74 R2, checked against GitHub's pages in OQ6, D:134); the collaborators with write or higher on this repo are `ironbelly`, `clayphi`, `IB-JonathanB` (`gh api repos/IronbellyOrg/IronClaude/collaborators`, 2026-11-20), the same people REQ R4 (line 30) lets approve. The approval widens nothing, so removing it narrows nothing.
7. **Readiness gets a real signal that approval never gave.** The built watcher had no check that the issue contained a plan; the approval label could be put on an empty issue (`H-design681-map.md:53`: "Nothing held plan-less issues"). `plan_check` plus `hold:plan` is new and cheap; PR 686 also adds a person's stop label, so opt-out exists.
8. **Smaller surface and fewer failure modes.** PR 686 deletes the approval, edit, Project-items and approver-file reads and 14 predicate symbols (symbol diff of `SNAP` against `PRA`), and with them failure reasons such as `events_incomplete`, `approval_before_trigger`, `project_mismatch`, `approvers_invalid` and the Project scope failure (`issue-watcher.md:165,361`). Fewer manual steps means fewer reasons for a correct issue to be skipped. About 88 percent of the lines PR 686 deletes are old tests (FULL-REPORT section 2).
9. **The design is built to be tested and has an unverified list.** 62 reasons, tests T1 to T13, an UNVERIFIED list (D:1146-1216 OD1 to OD15, FULL-REPORT section 5), and PR 686 reuses the built runner, audit, lock and call budget (D:361-434, design table 4.10).

## What it costs

- It removes the only human decision between "someone assigned it" and "a worker starts"; PR 682 deleted the code that implemented the owner's decision 6 = B (`E-pr682.md:36-38`), and no replacement human gate exists (`E-pr682.md:69`).
- It depends on a premise its own author marks UNVERIFIED ("only users with triage or write access can assign", `E-pr682.md:48`; two gaps in D:134 OQ6).
- It adds writes to GitHub by the poll (labels), against NG-2 (`SNAP/docs/designs/issue-watcher.md:76`); topic D09.

## What it risks

- Wrong or stale issue content starts a worker (nothing compares the issue now with what a person read), with `master` unprotected and workers unguarded (D:117, D:118).
- A bot or app with issue-write permission can assign (D:134 OQ6 gap 2).
- The design was approved by its author calling themselves the owner (FULL-REPORT section 4); the owner's records say the opposite for this exact point (REQ R19).

## What it gets right

- The extra human step is the stated burden of the whole effort; if it can be replaced by a script that checks the plan, work starts sooner and the system really is unattended.
- The plan check and the `hold:backlog` veto are new capabilities the owner's line lacks (`H-design681-map.md:66-71` lists them as "worth folding in").
- An approval by a login that an agent can also use proves little (L-1), so the owner's gate buys less safety than its code size suggests.

## Recommended rule (the spec text)

A new assignment to the user's own login in a listed repo starts the work, once, with no approver, no trigger label and no Project Status. The poll only checks, with a script, that the three plan sections are filled in; an incomplete issue waits; a person stops an issue with `hold:backlog`.

