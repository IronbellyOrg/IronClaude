# Position CLAY (Q03): keep the label code in PR 686, dormant behind the `issue.hold` grant

Paths: `pr-a` = /home/coder/.cache/ic-snap-20261120/pr-a (Clay's PR 686, the rewrite of the issue watcher, head 8e5ae29ad). D09 = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/VERDICT.md.

## Claim

Keep the hold in PR 686 as one piece, with the label write dormant: it runs only when the repo list names the grant `issue.hold`. Today no repo names it, so the poll writes nothing. Fix the two rough edges (the per-cycle warning, the stuck leftover label) instead of cutting out a tested design.

## Mechanism

`_hold_write_ok` (`pr-a/src/superclaude/cli/issue_watch/cycle.py:1021-1027`) refuses every label write unless `rdoc.has_grant("issue.hold")` (`repos.py:113-115`). A refusal returns "skip" and records nothing. The six-row table (`hold.py:146-168`) stays whole, so the day the owner wants a mark on GitHub the switch is one grant line plus the NG-2 amendment.

## Cited facts

1. The no-write state is pinned by a test: `test_without_the_grant_issue_hold_the_poll_writes_nothing` asserts `writes(world) == []` and `res.woken == ()` (`pr-a/tests/issue_watch/test_hold.py:416-426`).
2. The write form is narrow by construction: `LabelWriter` has "no comment call here and no way to build one" (`github.py:983-992`) and an injected refusal guard.
3. `--dry-run` runs the whole step and writes nothing, listing `would_hold` and `would_release` (`cycle.py:1053`, `:1065-1078`; design 4.11 under the table). D09 makes the 24-hour dry-run shadow run the switch-on gate, and only the full code can produce it.
4. The NG-2 test still bounds the capability: every write seen must be on `hold:plan` and only POST or DELETE (`test_security_invariants.py:634-645`). Any other write fails the build.
5. The plan-request machinery depends on the rows: entries are created at row 4 (`cycle.py:1091-1096`) and read at `:1139-1149`; removing the label path means reworking design 4.11 rows 3 to 6 (D09 Actions: Clay "did not size the rework").
6. `test_hold.py` is 1,073 lines with 58 tests (grep count); cutting rows 3 to 6 is a rewrite of a tested module right before the unification merge.
7. D09 itself notes the owner's own local branch writes a label once per repo (`repo_init.py:72`, `:116`, requirement R11; not re-read here), so "the watcher package never writes" is already not literal.
8. D09 adopts the narrow label-write form as the "pre-agreed fallback" (D09 VERDICT, Clay strengths to adopt, last item).
9. Ruling 33 (Clay's) set "hold label only, no comment (as Jay does)" (`docs/designs/orchestrator.md` 4.11 point 4); the label is the design's visible mark.

## Costs

Dead code for an unknown time; a warning every cycle for each failing issue until fixed; one more branch in the review surface.

## Risks

A grant in a config file turns writes on without a code review (the NG-2 test would still fail any write beyond the label). The loosened NG-2 test text can mislead a reader into thinking labels are allowed today.

## What it gets right

It avoids a rewrite of the busiest module, keeps the design and the tests in step, and keeps the dry-run gate available. A one-line change makes the no-grant state silent.

