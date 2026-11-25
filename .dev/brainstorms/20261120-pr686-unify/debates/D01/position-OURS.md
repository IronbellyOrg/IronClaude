# Position OURS (D01): a human approval stays the gate; assignment alone does not start work

Paths: `SNAP` = /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6); `PRA` = /home/coder/.cache/ic-snap-20261120/pr-a (PR 686, Clay's rewrite of the watcher, head 8e5ae29ad); `REQ` = zero-setup requirements file in worktree `claim-handoff-planb` (/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md); `DESIGN` = `SNAP/docs/designs/orchestrator.md` (cited D:nnn).

## The claim

Assignment tells the system whose issue it is. It does not tell the system that a person has said "start it now". The watcher must keep one deliberate human act as the start signal: the approval (today the `issue-watch:approved` label, per the owner's 2026-11-19 change the organisation issue field `Approved` = `Yes`, REQ R35) set by an allowed approver, plus the issue's Project Status in the allow-list (REQ R22). Assignment stays a necessary condition (discovery already filters on it) but never a sufficient one.

## The mechanism (what the kept code does)

1. Discovery needs assignment AND the trigger label: `argv_discover` runs `gh issue list --label <trigger> --assignee <login>` (`SNAP/src/superclaude/cli/issue_watch/github.py:180-198`). So in the owner's design assignment is already half of the trigger. The dispute is only whether it may be all of it.
2. `approval_of` accepts the latest approval event only when the actor is a `User`, not a `[bot]`, and in the approver set; a later unlabel voids it; the approval must come after the trigger label and after store init (`SNAP/.../predicates.py:185-234`).
3. `unchanged_since` refuses an approval when the issue body, a foreign comment or a rename is dated at or after the approval (`predicates.py:237-259`). This is the only code that binds "what the person said yes to" to "what the worker will read".
4. `project_check` (today Backlog only, `predicates.py:262-271`) is being turned into the Status allow-list Research, Spec, Plan, Debug (REQ R22, line 46) so a person can park an issue by Status.
5. The closed ship gate `GOVERNED_LEVELS_ALLOWED = False` (REQ R33, line 59) means only Pipeline `None` (claim only: assign, comment, summary files) launches until a reviewed commit opens it.

## Cited facts

1. **Assignment is a routine ownership act and an effect of claiming, not a readiness signal.** `/sc:issue --claim` itself runs `gh issue edit <N> --add-assignee @me` (`src/superclaude/skills/sc-issue-protocol/SKILL.md:87`, also `refs/claim.md:48`) and accepts an unassigned issue (`refs/claim.md:41-48`). If assignment starts work, a manual claim, a triage assignment or a hand-off all look the same as "go".
2. **The people who can assign are the same people the owner's design lets approve, so the approval gate does not widen trust; it adds a deliberate act.** `gh api repos/IronbellyOrg/IronClaude/collaborators` (read 2026-11-20): `ironbelly` admin, `clayphi` maintain, `IB-JonathanB` maintain; the other seven collaborators are read-only. REQ R4 (line 30): approvers are `ironbelly`, `clayphi` and repository maintainers (adds IB-JonathanB). Same set, so the gate costs one extra act by someone already trusted and protects against accident and stale content, not against an outsider.
3. **The assignment-safety premise is unproven by Clay's own text.** Issue 655 says assignment "is safe because only users with triage or write access can assign ... (stated by the owner; UNVERIFIED here)" (quoted in `.dev/analyze/pr686-20261120/E-pr682.md:48`). The design's own check finds two gaps: whether a read-only user can self-assign is UNVERIFIED, and apps and bots with issue-write permission can assign (`DESIGN` OQ6, line 134).
4. **Gate removal is far more consequential in Clay's design than it was in the built watcher.** The built watcher only claims at `--pipeline none` (`SNAP/docs/designs/issue-watcher.md:48`, D2). In Clay's design the same assignment ends in a worker that codes, pushes and a merge by the orchestrator (`DESIGN` DQ8 line 118, G2 line 56), workers run with no launch-level guard and no pre-push hook (DQ7 line 117), and `master` is unprotected: `gh api repos/IronbellyOrg/IronClaude/branches/master --jq .protected` printed `false`, `rulesets` length 0 (read 2026-11-20). Nothing between "someone assigned it" and "merged on master" is a human act except bot reviews.
5. **The replacement for the human step is a presence check, not a decision.** `plan_check` only verifies that three headings are present once and not empty or "Not known yet"; its own docstring says "It does not say whether the plan is good" (`PRA/src/superclaude/cli/issue_watch/hold.py:122-143`, line 131). `E-pr682.md:69` records "Replacement for human approval: none."
6. **Edit-after-approval protection has no equal in PR 686.** The names removed from `predicates.py` by PR 686 include `approval_of`, `unchanged_since`, `project_check`, `marker_in_window`, `LabelEvent`, `EditEvidence` (symbol diff of `SNAP` against `PRA`, 14 symbols in predicates, about 30 in github.py). `DESIGN` DQ3 and wave 1 re-read the issue live but nothing compares it with what a person looked at.
7. **The owner has recorded this decision more than once.** REQ R19 (line 45): "Confirmed by the owner in chat 2026-11-18: the approval label plus the issue's state stay the gate". REQ "Gates that stay manual" (lines 102-104): the approval and the issue state stay the gate. R35 (line 61) kept the trigger label and moved approval into a field; R36 (line 62, 2026-11-20) only withdrew the void-on-later-Status-change rule R31, it did not remove the approval. (FULL-REPORT section 7 says R36 "withdraws the Status gate"; REQ line 62 shows it withdraws R31 only.)
8. **The approval flow is built, tested and has a recorded live-test plan.** REQ "Built and tested" (line 70): 10677 passed, 15 skipped on 2026-11-20 across `tests/issue_watch tests/issue_pipeline tests/hooks tests/skills tests/commands tests/docs`; 28 tasks each reviewed independently. `tests/issue_watch/test_predicates.py` has the outsider, bot, unlabel, relabel and edit-after-approval cases (`issue-watcher.md:665-667`, T2 to T4).

## What it costs

- One manual act per issue (set `Approved`), plus Status and Pipeline: the burden Clay names (#450 comment, quoted in `E-pr682.md:54`: "another layer that a person then has to go and set ... the new burden").
- More code than assignment-only: the approval, edit, Project and approver-file reads (about 30 functions in `github.py`, call budget of three reads per candidate, `issue-watcher.md:361`).
- The approval can still be applied by an agent running on the same GitHub login (accepted risk L-1, `E-pr682.md:75`); the gate proves a deliberate act by an approved login, not a human body.

## What it risks

- Friction may push people to approve in bulk, which turns the gate into a rubber stamp.
- Two signals (trigger label plus approval) is one more than needed; Clay's point has some force there (see "what it gets right").
- Nothing here has run live; the owner's watcher is also `enabled: false` (`REQ` line 44, R18, and the closed ship gate).

## What it gets right (and what we concede)

- Plan content is a genuine readiness precondition that approval alone does not guarantee; `plan_check` (pure, no I/O, `hold.py:122-143`) is worth taking as a skip reason before the approval is even looked at. This is separable from the trigger rule.
- A person-set stop label `hold:backlog` is a cheap veto (opt-out) that complements opt-in approval; reading it needs no GitHub write (labels are already in `DiscoveredIssue.labels`, `PRA/.../predicates.py:139-160`).
- The label write (`hold:plan`) conflicts with NG-2 "the poller never writes to GitHub" (`issue-watcher.md:76`); that is topic D09, not decided here.

## Recommended rule (the spec text)

Work starts only when all of these hold: the issue is open and assigned only to the own login; the approval is present and unedited since (REQ R19/R35, with R36's withdrawal of R31); the Project Status is in the allow-list; `hold:backlog` is absent; `plan_check(body).ok` is true. Assignment alone never starts work.

