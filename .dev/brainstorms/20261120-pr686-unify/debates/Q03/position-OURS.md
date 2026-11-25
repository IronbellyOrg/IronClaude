# Position OURS (Q03): replace the label-writing code with a read-only variant now

Paths: `pr-a` = /home/coder/.cache/ic-snap-20261120/pr-a (Clay's PR 686, the rewrite of the issue watcher, head 8e5ae29ad); `master` = /home/coder/.cache/ic-snap-20261120/master. D09 = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/VERDICT.md.

## Claim

PR 686 should ship the read-only part of Clay's hold (the text check `plan_check`, the `held_incomplete` skip, the person-set `hold:backlog` stop) and NOT ship the label-writing code (`LabelWriter`, label create, add and remove, the label-driven table rows). The poll then writes nothing to GitHub, as rule NG-2 (the poll never writes to GitHub) says today. The label write comes back as its own small PR, together with the NG-2 amendment, only when someone shows a reader for the label.

## Mechanism

The hold already works without the label: `docs/designs/orchestrator.md` 4.11 point 10(a) says "a failing check holds the issue whatever the label shows" and point 8 lists the status output and audit log (`held_incomplete`) beside the label as places the user sees it (pr-a copy). So the decision becomes: backlog label present: skip; check passes: clear (drop any local entry); check fails: keep a local store entry and skip with `held_incomplete`. No label read, no label write, no `hand_removed` state, no live label read.

## Cited facts

1. NG-2 is a written owner non-goal: "no GitHub write (REST GET only ...)" (`master/docs/designs/issue-watcher.md:76`); D09 keeps it as written until a write is enabled.
2. The poll in master has no hold and no label code at all; in pr-a `HOLD_LABEL` appears only in `predicates.py:30`, `hold.py`, `cycle.py`, `github.py`, `record.py`. Shipping the write path is a new capability, not a fix.
3. PR 686 rewrites the invariant test around the capability: the NG-2 test now says "the only writes ... are the three calls on the `hold:plan` label" and asserts `writes and all("hold:plan" in ...)` (`pr-a/tests/issue_watch/test_security_invariants.py:12`, `:634-645`). Dormant code keeps the loosened test in master.
4. "Dormant" means only "no grant in a hand-edited list": `has_grant` at `pr-a/src/superclaude/cli/issue_watch/repos.py:113-115`, used at `cycle.py:1021-1027`. The standing grant list (DQ6) is the element the owner's per-issue grant row rejects (FULL-REPORT.md section 5 table). One config line turns on GitHub writes with no code review and no NG-2 amendment.
5. The dormant form is not clean. With no grant a failing issue logs `hold_write_failed` on every cycle (`cycle.py:1021-1027`, pinned by `tests/issue_watch/test_hold.py:416-426`, which asserts the warning). Row 3 (check passes, `hold:plan` still on the issue) returns "skip" when the grant is missing (`cycle.py:1064-1070`), so a good issue with a leftover label is stuck (read from code, not run).
6. Size of what a read-only variant removes: `LabelWriter` (`github.py:983-1069`), four argv builders (`github.py:267-320`), rows 3 to 5 of `_hold_step` (`cycle.py:1064-1119`), the `hand_removed` state, and about 17 lines of `test_hold.py` that mention a label call or `hand_removed` (grep count, rough).
7. D09 settled that the label's only unique effect is visibility and nobody showed a reader (D09 VERDICT, strongest point OURS 2); the owner's bar is a clear, evidenced benefit.
8. Putting the label back later is cheap and properly gated: the form is in design 4.11, in PR 686's history and in D09 (add and remove one label, grant gated, no comment). The gate is an NG-2 amendment in that later PR.
9. The ladder the owner works by: speculative code with no named user is skipped and named in one line.

## Costs

Rework of Clay's `_hold_step` (about 75 lines shrink to about 30) and tests; a rebase request on a PR Clay owns; person-placed `hold:plan` by hand stops being a stop signal (`hold:backlog` remains); a later label PR must repeat some tests.

## Risks

The plan-request clock keys on local `holds` entries that today are created at row 4 together with the label write (`cycle.py:1091-1096`, `:1139-1149`); the rework must create the entry without the write or the quiet hour never starts. If a person at once wants the label visible, a second PR is needed.

## What it gets right (of Clay's work)

The plan check is a pure text function (`hold.py:122-143`), `hold:backlog` is a read-only person-set stop, `--dry-run` shows holds before any write, and the audit reasons. All are kept.

