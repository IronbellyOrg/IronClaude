# Position paper CLAY (D03): keep PR 682, the deletion stands

Topic: PR 682 (Clay, merged 2026-11-20 00:02 UTC) deleted `src/superclaude/cli/issue_pipeline/`, WC-17 and "Issue pipeline duties" in WORKER-CONTRACT.md, and guard G2 rule 1.

## Claim

Keep PR 682. The package guarded a step (a person approves a plan after the claim) that the new design removes on purpose: the plan is reviewed when the issue is created, and a worker should not wait for a label or an `approved` comment. The code never ran in production, relies on a login anyone on the host can use, and needs a coordinator, a grant row per issue and two sessions for each approval. Deleting it first lets PR 686 remove the watcher symbols it imports without a shim.

## Mechanism

1. Issue 655 (Clay's plan, "replaces #450") lists the gate under "Dropped on purpose": "the plan is reviewed at creation, so the worker does not wait for a label or an `approved` comment" (quoted in E-pr682.md line 46).
2. The merged design (`docs/designs/orchestrator.md`, merged by PR 681) states rule R1 at line 73 and lists, file by file, what to delete in section 7.2 (lines 978-993) and what guard G2 still needs in 7.3 (line 995 onward). PR 682 is that plan carried out, first in the order (PR D before PR A, design line 1030).
3. The plan-quality check moves earlier: `/sc:issue --create` now requires the `Priority`, `Fix approach` and `Test plan` sections at every depth (`src/superclaude/skills/sc-issue-protocol/SKILL.md:102`, PRs 651 and 661 merged), and the poll holds an issue that lacks them (`hold.py` on PR 686, design 4.11).
4. Double-start protection moves to the orchestrator: write-ahead `intent` then `done` log, `worker_start_intent` settled only by reading `worker-list`, exclusive-create state file, lease comment (design lines 568, 700-712, 1108-1112).

## Cited facts

1. PR 682 body and commit: "Nothing runs this code: the issue watcher has `enabled: false` and never ran live" and removing it first lets PR A delete the `issue_watch` symbols without a shim. Verified: the old package imports `issue_watch.predicates` (`EditEvidence`, `LabelEvent`, `CommentEdit`), `github`, `runner` and `record` (`git show 01e7a9e23^:src/superclaude/cli/issue_pipeline/stage_predicates.py`, import line 42).
2. The ruling came from a written question to the owner. Clay's comment on issue 450 (the owner's watcher rollout issue) at 2026-11-18 17:00:32, addressed to `@ironbelly`, says the approval label and approver list "add another layer that a person then has to go and set ... the new burden we are trying to remove" and ends "What do you think?" (E-pr682.md line 54; FULL-REPORT.md section 1 point 4). Issue 655 was filed about three hours later and states its dropped items with reasons.
3. The gate has a known hole that the owner accepted in writing. Decision 4 (owner-answers.md:126) reads one login as accepted: "an agent on this host could apply the approval label as the owner", filed as risk L-1. The actor-type rule (the approver must be a User) cannot tell the owner from an agent that shares the login (FU-1 record j, `issue-pipeline-fu1.md:117`: actor `ironbelly`, id 7361222, type `User`).
4. The gate was costly by the owner's own words. Q36 "Latency approved for now, approve in coordinator" (owner-answers.md:185): the person approves in a coordinator session, which needs a person-opened coordinator, a grant row per issue (decision 8, E-pr682.md line 37) and two sessions per approval (E-pr682.md line 76).
5. The deletion was scoped with care. Guard G2 rule 2 stays (a bound worker passes no `--to`); the one contract sentence it relies on became its own bullet in the worker duties and is asserted in `tests/skills/test_worker_contract.py` (this fixes finding F14 of issue 665, "missing contract text for the worker side of guard rule 2", per the PR 682 commit message); the module `tests/hooks/test_launch_level_guard_worker.py` was rewritten so the guard's own release path is tested (a typed `/sc:implement` prompt) instead of through a helper; the PR body records an independent guard review: PASS (E-pr682.md line 61).
6. Removal order is a real constraint. Design line 982: "`issue_pipeline` imports from `issue_watch`, so PR A cannot remove those symbols while `issue_pipeline` exists". Keeping 682 keeps PR 686 (59 files, +14,256/-16,637 at its first analysed head 4e7f12b1a, FULL-REPORT.md section 2) mergeable without a compatibility shim.
7. Replacement protections are specified and have named tests. Design lines 1108-1112 list the PR B tests: a kill after each `intent` and before `done` resumes without repeating the act; exclusive create refuses a second state file; two orchestrators given one issue create one state file. The poll side keeps one winner per cycle by the watcher's lock (`flock` on `state_dir/lock`, a second cycle exits 75; design lines 700-712, point 4 layer 1).
8. Dead-code cost avoided: 4,599 lines deleted, about 1,600 source and about 2,900 tests (E-pr682.md summary). `docs/user-guide/cli-groups.md` no longer documents a command group that did not run.
9. The watcher is off. `enabled: false` is the default, so no issue is exposed to a missing gate today (FULL-REPORT.md section 3, "case for the deletion").

## What it costs

- Human approval of the plan before a worker implements is gone and replaced only by a presence check on three headings (`hold.py`), which does not judge the plan (E-pr682.md line 69).
- The owner's local branch (`claim-handoff-planb`, 53 files, extends the deleted package) must be reworked (E-pr682.md line 67).
- Master text still says "when a coordinator owns the issue, it runs the worktree step" (`issue.md:85`, `SKILL.md:140`); PR E is to add banners.
- Equal double-start protection does not exist until PR B is built (E-pr682.md line 68).

## What it risks

- A worker can build from an unreviewed plan if the plan-hold check passes on present-but-empty headings and the issue is assigned by anyone with triage access (the claim "assignment is safe" is marked UNVERIFIED in issue 655; design open question OQ6 finds two gaps, per E-pr682.md line 83).
- It reverses the owner's merged work and decisions 2, 3, 6 and Q35 to Q38 without naming them or recording agreement (E-pr682.md line 81).

## What it gets right

It is internally consistent with the design the rest of the stack builds on; it removes dead code before replacing it so PR 686 stays small; it keeps the one guard rule that still binds; and it is honest that the gate "never ran live" in production. Its weakness is not the code it removed but the missing decision record from the person whose decisions it reversed.

