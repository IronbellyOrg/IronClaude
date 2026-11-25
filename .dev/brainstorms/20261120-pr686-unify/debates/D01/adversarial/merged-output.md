<!-- Provenance: merged document for D01 (trigger and approval gate), produced by the merge-executor for /sc:adversarial.
     Base: Variant A (OURS), variant-1-original.md (selected in base-selection.md, final 0.903 vs 0.832).
     Incorporated: Variant B (CLAY), variant-2-original.md, strengths 1 to 3; invariant-probe.md requirements MR-1 (INV-001) and MR-2 (INV-002).
     Planned changes applied: #1 to #6 from refactor-plan.md, in order. Every base citation is kept unchanged except fact 6 (Change #3).
     Section tags below: Base original / Base modified (reason) / Variant 2 section ref, Change #N. -->

# Position OURS (D01): a human approval stays the gate; assignment alone does not start work

<!-- Source: Base original -->
Paths: `SNAP` = /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6); `PRA` = /home/coder/.cache/ic-snap-20261120/pr-a (PR 686, Clay's rewrite of the watcher, head 8e5ae29ad); `REQ` = zero-setup requirements file in worktree `claim-handoff-planb` (/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md); `DESIGN` = `SNAP/docs/designs/orchestrator.md` (cited D:nnn).

## The claim

<!-- Source: Base original -->
Assignment tells the system whose issue it is. It does not tell the system that a person has said "start it now". The watcher must keep one deliberate human act as the start signal: the approval (today the `issue-watch:approved` label, per the owner's 2026-11-19 change the organisation issue field `Approved` = `Yes`, REQ R35), set by an allowed approver, plus the issue's Project Status in the allow-list (REQ R22). Assignment stays a necessary condition (discovery already filters on it) but never a sufficient one.

## The mechanism (what the kept code does)

<!-- Source: Base original -->
1. Discovery needs assignment AND the trigger label: `argv_discover` runs `gh issue list --label <trigger> --assignee <login>` (`SNAP/src/superclaude/cli/issue_watch/github.py:180-198`). So in the owner's design assignment is already half of the trigger. The dispute is only whether it may be all of it.
2. `approval_of` accepts the latest approval event only when the actor is a `User`, not a `[bot]`, and in the approver set; a later unlabel voids it; the approval must come after the trigger label and after store init (`SNAP/.../predicates.py:185-234`).
3. `unchanged_since` refuses an approval when the issue body, a foreign comment or a rename is dated at or after the approval (`predicates.py:237-259`). This is the only code that binds "what the person said yes to" to "what the worker will read".
4. `project_check` (today Backlog only, `predicates.py:262-271`) is being turned into the Status allow-list Research, Spec, Plan, Debug (REQ R22, line 46) so a person can park an issue by Status.
5. The closed ship gate `GOVERNED_LEVELS_ALLOWED = False` (REQ R33, line 59) means only Pipeline `None` (claim only: assign, comment, summary files) launches until a reviewed commit opens it.

## Cited facts

<!-- Source: Base original for facts 1 to 5, 7 and 8; fact 6 is Base modified (Change #3, narrowed after Round 2: Variant B is not silent about edits, `DESIGN` line 488, AD-A3 / ruling 23) -->
1. **Assignment is a routine ownership act and an effect of claiming, not a readiness signal.** `/sc:issue --claim` itself runs `gh issue edit <N> --add-assignee @me` (`src/superclaude/skills/sc-issue-protocol/SKILL.md:87`, also `refs/claim.md:48`) and accepts an unassigned issue (`refs/claim.md:41-48`). If assignment starts work, a manual claim, a triage assignment or a hand-off all look the same as "go".
2. **The people who can assign are the same people the owner's design lets approve, so the approval gate does not widen trust; it adds a deliberate act.** `gh api repos/IronbellyOrg/IronClaude/collaborators` (read 2026-11-20): `ironbelly` admin, `clayphi` maintain, `IB-JonathanB` maintain; the other seven collaborators are read-only. REQ R4 (line 30): approvers are `ironbelly`, `clayphi` and repository maintainers (adds IB-JonathanB). Same set, so the gate costs one extra act by someone already trusted and protects against accident and stale content, not against an outsider.
3. **The assignment-safety premise is unproven by Clay's own text.** Issue 655 says assignment "is safe because only users with triage or write access can assign ... (stated by the owner; UNVERIFIED here)" (quoted in `.dev/analyze/pr686-20261120/E-pr682.md:48`). The design's own check finds two gaps: whether a read-only user can self-assign is UNVERIFIED, and apps and bots with issue-write permission can assign (`DESIGN` OQ6, line 134).
4. **Gate removal is far more consequential in Clay's design than it was in the built watcher.** The built watcher only claims at `--pipeline none` (`SNAP/docs/designs/issue-watcher.md:48`, D2). In Clay's design the same assignment ends in a worker that codes, pushes and a merge by the orchestrator (`DESIGN` DQ8 line 118, G2 line 56), workers run with no launch-level guard and no pre-push hook (DQ7 line 117), and `master` is unprotected: `gh api repos/IronbellyOrg/IronClaude/branches/master --jq .protected` printed `false`, `rulesets` length 0 (read 2026-11-20). Nothing between "someone assigned it" and "merged on master" is a human act except bot reviews.
5. **The replacement for the human step is a presence check, not a decision.** `plan_check` only verifies that three headings are present once and not empty or "Not known yet"; its own docstring says "It does not say whether the plan is good" (`PRA/src/superclaude/cli/issue_watch/hold.py:122-143`, line 131). `E-pr682.md:69` records "Replacement for human approval: none."
6. **The edit-after-approval binding has no counterpart in PR 686, but PR 686 is not silent about edits.** PR 686 accepts edits made after assignment on purpose: its wave 1 re-reads the issue live and re-runs the `plan_check` and `hold:backlog` checks (`DESIGN` line 488, AD-A3 / ruling 23). What it lacks is any code that compares the issue now with what a person looked at: the names removed from `predicates.py` by PR 686 include `approval_of`, `unchanged_since`, `project_check`, `marker_in_window`, `LabelEvent`, `EditEvidence` (symbol diff of `SNAP` against `PRA`, 14 symbols in predicates, about 30 in github.py). `plan_check` tests only that three headings are filled (`hold.py:131`), so a body rewritten after assignment that still has three filled headings passes. The approval's added value is that `unchanged_since` ties a person's yes to the content that person read (it also catches renames and foreign comments); that matters most when the worker can push and merge (fact 4). Conceded cost: any edit voids the approval, so a typo fix needs a new approval. <!-- Source: Base modified, Change #3 (restructure of base fact 6: "no equal" and "nothing compares" narrowed to "no counterpart"; B's deliberate acceptance of edits added, Variant 2 mechanism and debate Round 2 evidence) -->
7. **The owner has recorded this decision more than once.** REQ R19 (line 45): "Confirmed by the owner in chat 2026-11-18: the approval label plus the issue's state stay the gate". REQ "Gates that stay manual" (lines 102-104): the approval and the issue state stay the gate. R35 (line 61) kept the trigger label and moved approval into a field; R36 (line 62, 2026-11-20) only withdrew the void-on-later-Status-change rule R31, it did not remove the approval. (FULL-REPORT section 7 says R36 "withdraws the Status gate"; REQ line 62 shows it withdraws R31 only.)
8. **The approval flow is built, tested and has a recorded live-test plan.** REQ "Built and tested" (line 70): 10677 passed, 15 skipped on 2026-11-20 across `tests/issue_watch tests/issue_pipeline tests/hooks tests/skills tests/commands tests/docs`; 28 tasks each reviewed independently. `tests/issue_watch/test_predicates.py` has the outsider, bot, unlabel, relabel and edit-after-approval cases (`issue-watcher.md:665-667`, T2 to T4).

## What it costs

<!-- Source: Base original -->
- One manual act per issue (set `Approved`), plus Status and Pipeline: the burden Clay names (#450 comment, quoted in `E-pr682.md:54`: "another layer that a person then has to go and set ... the new burden").
- More code than assignment-only: the approval, edit, Project and approver-file reads (about 30 functions in `github.py`, call budget of three reads per candidate, `issue-watcher.md:361`).
- The approval can still be applied by an agent running on the same GitHub login (accepted risk L-1, `E-pr682.md:75`); the gate proves a deliberate act by an approved login, not a human body.

## What it risks

<!-- Source: Base original -->
- Friction may push people to approve in bulk, which turns the gate into a rubber stamp.
- Two signals (trigger label plus approval) is one more than needed; Clay's point has some force there (see "What it gets right (and what we concede)").
- Nothing here has run live; the owner's watcher is also `enabled: false` (`REQ` line 44, R18, and the closed ship gate).

## What it gets right (and what we concede)

<!-- Source: Base modified, Changes #1 and #2 (first two bullets extended; third bullet is Base original). Variant 2 mechanism step 4 and cited fact 7 (plan_check); Variant 2 mechanism step 1 (R1, D:73) (hold:backlog) -->
- Plan content is a genuine readiness precondition that approval alone does not guarantee; `plan_check` (pure, no I/O, `hold.py:122-143`) is worth taking as a skip reason evaluated before the approval counts, so an issue with no plan never reaches the approval check. This is separable from the trigger rule. The built watcher had no check that an issue contained a plan: the approval label could be put on an empty issue (`H-design681-map.md:53`: "Nothing held plan-less issues"). <!-- Source: Base modified, Change #1 (ordering made explicit; B's evidence added from Variant 2 fact 7) -->
- A person-set stop label `hold:backlog` is a cheap veto (opt-out) that complements opt-in approval; the design states the rule as "a person may stop an issue with `hold:backlog`" (`DESIGN` R1, D:73). Reading it needs no GitHub write (labels are already in `DiscoveredIssue.labels`, `PRA/.../predicates.py:139-160`), so the watcher stays read-only for this veto. <!-- Source: Base modified, Change #2 (read-only veto stated; R1 citation added from Variant 2 mechanism step 1) -->
- The label write (`hold:plan`) conflicts with NG-2 "the poller never writes to GitHub" (`issue-watcher.md:76`); that is topic D09, not decided here. <!-- Source: Base original -->

## Recommended rule (the spec text)

<!-- Source: Base modified, Changes #1, #2, #4, #5. The base rule paragraph is kept; the ordering of the two skip reasons, MR-1 and MR-2 are added below it -->
Work starts only when all of these hold: the issue is open and assigned only to the own login; the approval is present and unedited since (REQ R19/R35, with R36's withdrawal of R31); the Project Status is in the allow-list; `hold:backlog` is absent; `plan_check(body).ok` is true. Assignment alone never starts work.

`plan_check(body).ok` and `hold:backlog` are read-only skip reasons and are looked at before the approval counts: an issue that fails either is skipped without reading the approval or edit evidence. <!-- Source: Base modified, Changes #1 and #2 (Variant 2 mechanism steps 1 and 4) -->

### Requirement MR-1: the check at the moment of start repeats the gates

<!-- Source: Base modified, Change #4 (appended; from invariant-probe.md INV-001, verified by the orchestrator, debate-transcript.md Round 2.5) -->
The check made at the moment the worker starts (the live re-check, "still open, still assigned to the user, and the check still passes", `DESIGN` line 317) must repeat the approval, `unchanged_since` and the Status allow-list, not only `plan_check` and `hold:backlog`. Evidence: PR 686's wave 1 re-checks `hold:backlog` and `plan_check` only (`DESIGN` lines 488 and 543; `PRA/.../cycle.py:1279-1305` has no approval, edit or Status read), and a `hold:backlog` applied after the wake is honoured only at wave 1 (`PRA/.../cycle.py:992-1005`). Master has `_revalidate`, which re-reads approval and Status (`SNAP/.../cycle.py:979`, called at `:1058`). Without MR-1 a gap exists between wake and claim.

### Requirement MR-2: keep the claim-marker guard

<!-- Source: Base modified, Change #5 (appended; from invariant-probe.md INV-002, verified by the orchestrator, debate-transcript.md Round 2.5) -->
A manual `/sc:issue --claim` assigns the issue (fact 1) and posts the claim marker (`src/superclaude/skills/sc-issue-protocol/refs/claim.md:30,92`). Master's `_examine` marks an issue that has a `CLAIM_MARKER` comment after the approval as claimed without launching it, through `marker_in_window` (`SNAP/.../cycle.py:858,946-947`), so a manual claim plus a watcher start cannot double start. PR 686 keeps only the constant (`PRA/.../predicates.py:18`); its layers (DQ3) are the poll store, an `O_EXCL` state file and a lease comment, and layer 4 says a claim by the current login is idempotent. Whichever tree is built must keep `marker_in_window`.

## Merged recommendation

<!-- Source: New closing section. Base "Recommended rule" (Base original) plus Change #1 and #2 (Variant 2 plan_check and hold:backlog), Changes #4 and #5 (MR-1, MR-2) and Change #6 (Conditions to revisit; Variant 2 Round 2 (b) and Variant 1 Round 2 (d) from debate-transcript.md) -->
Work starts only when all of these hold:

1. the issue is open and assigned only to the own login;
2. an allowed approver's approval (field `Approved` per R35; the `issue-watch:approved` label until then) is present and unedited since (`unchanged_since`; REQ R19/R35, with R36's withdrawal of R31);
3. the Project Status is in the allow-list (Research, Spec, Plan, Debug; REQ R22);
4. `hold:backlog` is absent;
5. `plan_check(body).ok` is true.

Assignment alone never starts work.

- **MR-1.** The check at the moment of start repeats the approval, `unchanged_since` and the Status allow-list, not only `plan_check` and `hold:backlog` (evidence in "Requirement MR-1" above).
- **MR-2.** Keep the claim-marker guard `marker_in_window`, so a manual `/sc:issue --claim` plus a watcher start cannot double start (evidence in "Requirement MR-2" above).

### Conditions to revisit

<!-- Source: Base modified, Change #6 (new section appended; Variant 2 Round 2 (b) and Variant 1 Round 2 (d), debate-transcript.md) -->
The approval requirement can be reopened, and assignment alone considered as the start signal, only when all four of these hold:

1. The launch guard refuses to start a worker when it is not effective, and this has tests (topic D05).
2. Workers cannot push or merge: the ship gate stays closed or an equal control exists (topic D06).
3. The watcher skips any issue that already has a claim record or worktree (MR-2 is the same guard).
4. The owner records the reversal of R19 in chat.

Owner decisions still open: whether to reverse R19 (condition 4), and whether the separate trigger label stays a manual act (REQ R35 line 61 says it stays; the trigger label is redundant once assignment fills its discovery role and the claim-record skip exists, so this is the owner's call).
