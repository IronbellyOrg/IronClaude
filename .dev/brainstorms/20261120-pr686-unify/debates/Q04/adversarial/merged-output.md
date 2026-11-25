<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (OURS, position-OURS.md) -->
<!-- Merge date: 2026-11-20 -->

<!-- Source: Base (original, modified) - title reworded because "bound to the head sha" no longer describes the merged rule (Change #1) -->
# Position OURS (Q04), merged: the typed run line is the go for one run's pushes; every other push class and every merge needs its own typed go

<!-- Source: Base (original) -->
Notation: "WC:nnn" is a line of `src/superclaude/core/WORKER-CONTRACT.md` and "D:nnn" a line of `docs/designs/orchestrator.md`, both in the read-only export `/home/coder/.cache/ic-snap-20261120/master` (origin/master 61ac2c2e6). "SPEC:nnn" is a line of `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md`.

## Claim

<!-- Source: Variant 2 (CLAY), Claim - merged per Change #1 (base Claim replaced; base wording on the merge go and on Full Submit kept) -->
A push publishes commits the person has not seen, so a push needs the person's typed go. That go is given once per run, not once per push: the person's typed `/sc:pr-submit --monitor 3` line (or the Full Submit field for that issue, R25) is itself the go for the first push, the PR and the fix-round fast-forward pushes of that one run. The person decides once that this branch may be published, and the fix-round pushes are that decision carried out, inside caps and guards the tool already enforces. A go is bound to a sha only where the commit already exists when the go is given: a push after a rebase (the go names old and new sha) and the merge (SEC-01). A push after a revert, a push by any other actor or in a new run, and every merge each need their own new typed go, and a push go never covers a merge. The Full Submit per-issue go (R25) stays narrow (Mechanism item 5).

## Mechanism

<!-- Source: Variant 2 (CLAY), Mechanism 2 - merged per Change #1 (replaces base Mechanism items 1 and 2) -->
1. The run line is the go. In the person's own top-level session, the typed `/sc:pr-submit --monitor 3` line is the person's go for that run's first push, the PR and each fix-round push. The loop then runs the fix rounds by itself: edits, validation, one fix commit per cycle, push, reply, resolve (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:291, 308`). The push go inside the run carries no sha, because a go bound to a head sha cannot exist for a fix commit that is not yet written. A manual or coordinator push made without `/sc:pr-submit` is not covered (item 3).

<!-- Source: Variant 2 (CLAY), cited facts 3 and 4 - merged per Change #3 (inserted after item 1; the condition of the run go) -->
2. The run go is not a blank check. It holds only while the tool's own fence holds: one fix commit per cycle; a halt with `push_range_mismatch` rather than publishing unreviewed local commits; fast-forward only, with parent checks (`src/superclaude/commands/pr-submit.md:121`, `SKILL.md:342-348`); no force push; no push to the default or protected branch; and `push_count <= max_rounds + 1` (`SKILL.md:262`), where `max_rounds` defaults to 2 with a hard cap of 5 (`pr-submit.md:47`). Each of these can be tested (see the tests in the last section).

<!-- Source: Base (original, modified) - base Mechanism item 2 class list kept, now stated as the classes outside the run - merged per Change #4 -->
3. These classes are outside the run and each needs its own new typed go: a first push without `/sc:pr-submit` (a manual or coordinator push); a push after a revert; a push after a rebase (a force push, refused unless the go names old and new sha; the tool itself never rebases or force-pushes); a new `/sc:pr-submit` run on the same PR; and a merge (its own go, bound to the head sha as in SEC-01 at SPEC:288, never covered by a push go). A push by any other actor, such as a worker script's own push, is covered by no go (SEC-13).

<!-- Source: Base (original, modified) - base Mechanism item 3 replaced by the end of a go - merged per Change #2 (end events from base item 3 and from Variant 2 "What it costs", which noted that no end event existed) -->
4. A go has an end. The run go ends when the run ends, when the PR is merged or closed, or when the branch head moves to a sha outside the run (a commit the run did not make). After that, the next push needs a new typed go. A go that names a sha (a push after a rebase, a merge) is consumed by the push or merge it names and is void when the branch head moves to a sha it did not name.

<!-- Source: Base (original, modified) - base Mechanism item 4 replaced - merged per Change #5 (Variant 2 U-008 wording point on WC:245) -->
5. The Full Submit field value (Pipeline = Full Submit plus the `Approved` field) is the person's go for that issue's first push, the PR and the loop pushes of the one `/sc:pr-submit --monitor 3` run it starts, in a top-level session. It never covers a merge, a force push, a branch deletion or any other push. The worker route stays rejected: a worker does not run `/sc:pr-submit` (ADD1 rejected per D06 item 5; WC:23, WC:244). The WC:245 amendment (SEC-15 in the last section) is worded so that the run line or field is not an "earlier pre-authorization".

## Cited facts

<!-- Source: Base (original) -->
1. WC:245: "Before any push that would publish worker commits the person has not seen, the coordinator shows them to the person and pushes only on the person's go; no earlier pre-authorization waives this. A commit grant covers one Task and ends at that Task's `worker_done`." The rule is per publication, and it names pre-authorization as not enough.

<!-- Source: Base (original, modified) - ADD1 sentence added - merged per Change #5 (ADD1 text from Variant 2 cited fact 1, D:135) -->
2. WC:244 and WC:23: PRs go only through `/sc:pr-submit --monitor 3` in an ordinary top-level session, never as a worker; `/sc:pr-submit` is on the never-as-worker list (owner decision D3, recorded in `/home/coder/workspaces/IronClaude/.dev/orca-command-refactor/decisions/APPROVED.md:10-13`, per D06 VERDICT). ADD1, the Clay design addition (D:135) that would let a handoff worker push its own feature branch and open its PR through `/sc:pr-submit --monitor 3`, stays rejected (D06 item 5).

<!-- Source: Base (original) -->
3. The owner's rule in the spec: SPEC:124 and SPEC:467 both say "a person's typed go precedes every push and merge". The spec panel graded the rule as holding for merge and only "two unreconciled cases" for push (spec panel report, finding F4, `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/panel/review-1/spec-panel-report.md`, line 26 and the rule table row 2).

<!-- Source: Base (original) -->
4. Master IronClaude is unprotected, there is no ruleset and the acting user holds `maintain` (D:118; risk K12, D:1234). Nothing on GitHub stops a push, so the person's go is the only brake (D06 VERDICT, strongest point 2; Clay's advocate agreed in D06 round 2).

<!-- Source: Base (original) -->
5. Workers run with no L1 guard and no L2 pre-push hook, and a worker's own script can still push a feature branch (D:117 DQ7; SPEC:300 SEC-13; D05 VERDICT item 4: the guard "narrows honest drift on master and main", not a script run). A go that lasts "until merge" would make every such push look authorized.

<!-- Source: Base (original) -->
6. A real miss by an unattended push: on 2026-11-04 the owner squash-merged PR 368 mid-cycle, GitHub deleted the branch, and the skill's round-2 push re-created the deleted branch with an unmerged fix (commit 2306437c; memory `pr-submit-check-pr-open-before-push`, 15 days old, not re-verified). A go that outlives the PR's state is how that happens.

<!-- Source: Base (original) -->
7. `/sc:pr-submit` itself treats the push as separately gated: ordinal gates G-arm, G-edit, G-push (`src/superclaude/commands/pr-submit.md:46`), L2 halts before the push (`SKILL.md:307`), and the merge push is allowed only with exact parents (`pr-submit.md:121`). The push is a named, separately granted capability, not a by-product.

<!-- Source: Base (original, modified) - head-sha binding now stated for the rebase push and the merge only - merged per Change #1 -->
8. Q01 recommendation 5 and D06 item 1 already give the merge go an end (action done, head moves, owner revokes) and a head sha. The sha pin for a push after a rebase uses the same record and the same check (Q01 VERDICT item 5); neither verdict binds a sha to a fix-round push.

<!-- Source: Base (original, modified) - Full Submit narrowed to one run - merged per Change #5 -->
9. Full Submit is already scoped narrowly in the owner's own text: "that setting is the person's go for that issue's push and pull request, and nothing else is pushed" (requirements.md R25 row; D06 item 7 amendment of WC:245). The merged rule reads that go as covering that issue's first push, the PR and the loop pushes of the one `/sc:pr-submit --monitor 3` run it starts, and nothing else (no merge, force push, branch deletion or other push). The R25 wording, which ends at "nothing else is pushed", has to be amended to say so (SEC-15 in the last section).

<!-- Source: Variant 2 (CLAY), cited fact 3 - merged per Change #3 (supports the run go as the project's mandatory PR path) -->
10. The built tool already runs unattended after one command: the project `CLAUDE.md` says `/sc:pr-submit --monitor 3` "fixes the confirmed findings ... pushes the fixes without asking", and `pr-submit.md:38` (`--monitor 3 --max-rounds 3`) is the "full loop: fix, push, reply, resolve". A fresh go per fix-round push is incompatible with the mandatory way the owner opens PRs.

## What it costs

<!-- Source: Base (original, modified) - restructured to the agreed accounting - merged per Change #6 (cost basis from Variant 1; no-end-event cost from Variant 2 now answered by item 4) -->
- One go per run, not one per push. For a normal PR the person types their own `/sc:pr-submit --monitor 3` line (the go for the first push, the PR and the fix-round pushes) and later a merge go. The per-push reading would have cost one prompt per review round, up to 5 (`--max-rounds` hard cap 5, `pr-submit.md:47`), and made `--monitor 3` behave like `--monitor 2`; that cost is removed.
- A new typed go is still needed for each class outside the run (item 3): a manual or coordinator push, a revert, a rebase, a new run on the same PR.
- A go record, an end-of-run check and a sha check (for a push after a rebase and for the merge) must be built; not built today (D06 notes the gate and verb are design only).

## What it risks

<!-- Source: Base (original, modified) - restructured to the agreed accounting - merged per Change #6 (risks from Variant 1 and Variant 2) -->
- A script can type the run line (D06 INV-003). The run line is the person's go only when the person types it in their own top-level session.
- A worker script's own push is covered by no go (SEC-13; D:117 DQ7; Mechanism item 3). Workers run with no L1 guard and no L2 pre-push hook (cited fact 5), so the run go must never be read as covering such a push.
- The head can move outside the run (someone else pushes to the branch, or the branch is rebased). A push after that is refused under item 4, and that check is not built yet.
- A sha-bound push go for a fix-round push would be OURS extended and is not in D06 or Q01: those bind the head sha to the merge go, and no verdict says a push go carries a sha (WC:245 names none). The merged rule pins a sha only for a push after a rebase and for the merge.
- A bad fix push is caught only at the merge go, by the merge-time controls (the 13-reason `merge-gate`, `--match-head-commit`, reviewer hold; D06 items 1, 2, 4). So the merge go stays bound to the head sha and a push go never covers it.

## What it gets right

<!-- Source: Base (original) -->
- It keeps the one rule that protects an unprotected `master`: nothing publishes unseen commits without a person.
- It separates push from merge, so a push go can never release a merge and a merge go can never release a push (SEC-01, SEC-12).
- It gives every class that changes the commit set (revert, rebase, re-run) its own go, which is where the PR 368 incident and `push_range_mismatch` show the risk lives.

## Resulting rule and rows

<!-- Source: Variant 2 (CLAY), Claim and Mechanism - merged per Change #7 (new final section; rule text supplied by the orchestrator from the debate and copied unchanged) -->

### The rule

THE RULE (one sentence, testable): "A push to a PR's feature branch needs a person's typed go, except that the person's typed `/sc:pr-submit --monitor 3` line (or the Full Submit field for that issue) is itself that go for the first push, the PR and the fix-round fast-forward pushes of that one run, ending when the run ends, when the PR is merged or closed, or when the branch head moves outside the run; a push after a revert or rebase (the go names the old and new sha), a push by any other actor or in a new run, and every merge each need their own new typed go, and a merge go is bound to the 40-character head sha."

### Per push class

Per push class: first push and PR = covered by the person's typed run line or the Full Submit field (a manual or coordinator push without `/sc:pr-submit` needs a typed go); each fix-round push by the same session on the same PR = covered, no new go, while the fence holds (one fix commit per cycle, `push_range_mismatch` halt, fast-forward only, no force push, no push to the default or protected branch, `push_count <= max_rounds + 1`); push after a revert = new go; push after a rebase = new go naming old and new sha (the tool never rebases or force-pushes); merge = new go bound to the 40-character head sha, never covered by a push go.

### Tests that can check it

Tests that can check it: a push with no typed run line, Full Submit field or go record is refused; a second `/sc:pr-submit` run on the same PR needs a new line; a push after the PR is merged or closed, or after the head moved outside the run, is refused; a fix-round push count above `max_rounds + 1` is impossible; a merge command with only a push go is refused.

### Rows to change in SPEC.md

Rows to change in `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md` (line numbers as of this debate):

- The flow sentence at line 124 and the stage-rules sentence at line 467 ("a typed go precedes every push and merge"): add "except the run line of Full Submit or `/sc:pr-submit --monitor 3`, per SEC-15 and SEC-22".
- FR-32 (line 233, the push clause): restate the push clause to match THE RULE above.
- SEC-15 (line 302, the WC:245 amendment): say the run line or field is the go for the first push, PR and that run's fix-round pushes only, never a merge, force push, branch deletion or another push, and that it is given in the live session at the time of the run, so it is not an earlier pre-authorization.
- Section 13.2 guard probe row (line 699): the Full Submit cycle probe, checked by the tests above.
- New row SEC-22: the end of a run go (run end, PR merged or closed, head moved outside the run).
- SEC-01 (line 288): add that a push go never covers a merge.

### WORKER-CONTRACT.md lines touched

Lines of `src/superclaude/core/WORKER-CONTRACT.md` (read-only export named in the Notation) that this touches:

- Line 245 (the push rule, cited fact 1): amended, through the SEC-15 wording above.
- Line 23 (`/sc:pr-submit` is on the never-as-worker list): unchanged.
- Line 244 (PRs go only through `/sc:pr-submit --monitor 3` in a top-level session): unchanged.
