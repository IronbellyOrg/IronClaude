<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (OURS, original position paper) -->
<!-- Merge date: 2026-11-20T08:04:47Z -->

<!-- Source: Base (original) -->
# Position OURS (Q03): replace the label-writing code with a read-only variant now

Paths: `pr-a` = /home/coder/.cache/ic-snap-20261120/pr-a (Clay's PR 686, the rewrite of the issue watcher, head 8e5ae29ad); `master` = /home/coder/.cache/ic-snap-20261120/master. D09 = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/VERDICT.md.

<!-- Source: Base (original) -->
## Claim

PR 686 should ship the read-only part of Clay's hold (the text check `plan_check`, the `held_incomplete` skip, the person-set `hold:backlog` stop) and NOT ship the label-writing code (`LabelWriter`, label create, add and remove, the label-driven table rows). The poll then writes nothing to GitHub, as rule NG-2 (the poll never writes to GitHub) says today. The label write comes back as its own small PR, together with the NG-2 amendment, only when someone shows a reader for the label.

<!-- Source: Base (original, modified) - Change 1 (dormant-form finding added from M1 and M2) and Change 6 (`hold:plan` label read wording; rows defined once) -->
## Mechanism

The hold already works without the label: `docs/designs/orchestrator.md` 4.11 point 10(a) says "a failing check holds the issue whatever the label shows" and point 8 lists the status output and audit log (`held_incomplete`) beside the label as places the user sees it (pr-a copy). So the decision becomes: backlog label present: skip; check passes: clear (drop any local entry); check fails: keep a local store entry and skip with `held_incomplete`. The poll makes no `hold:plan` label read, no label write, no `hand_removed` state, no live label read. (The `hold:backlog` label is still read, from the search row, `cycle.py:1052`.)

The read-only variant creates the local entry with no write. The dormant form cannot do this for an issue the poll finds itself: with no grant, row 4 returns "skip" before the entry is written (fact 11), and the design's reference config lists the grant, so "no grant" is not the default (fact 10).

Row numbering, defined once: the decision follows a six-row table (`hold.py:146-168`) that `_hold_step` applies. This paper names three rows: row 3 (check passes, `hold:plan` label still on), row 4 (check fails, no label, no entry) and row 6 (a person-placed `hold:plan`). "Rows 3 to 5" always means the label-driven rows that the read-only variant removes. Clay's paper counts "rows 3 to 6"; the extra row is row 6, whose stop stops working once the poll makes no `hold:plan` label read (see Costs).

<!-- Source: Base (original, modified) - Change 1 (facts 10 and 11 added), Change 2 (fact 8 replaced by a pointer) and Change 6 (fact 2 corrected); facts 1, 3, 4, 5, 6, 7 and 9 are Base (original) -->
## Cited facts

Facts 1 to 9 keep the base numbering. Facts 10 and 11 were added after fact 5 because they extend facts 4 and 5.

1. NG-2 is a written owner non-goal: "no GitHub write (REST GET only ...)" (`master/docs/designs/issue-watcher.md:76`); D09 keeps it as written until a write is enabled.
2. The poll in master has no hold and no label code at all. In pr-a, `HOLD_LABEL` is defined in `predicates.py:30` and used in `cycle.py` (`:1052`, `:1113`, `:1294`), `github.py` (`:31`, and in the four label argv builders) and `hold.py` (`:37`, `:43`); `record.py` does not use the constant and only names the text `hold:plan` in its docstring (`record.py:11`). Moderator correction after a grep of `pr-a/src` (the merge executor had listed `record.py` among the users). Shipping the write path is a new capability, not a fix. <!-- Source: Base (original, modified) - Change 6, `HOLD_LABEL` definition and `hold:plan` text location corrected -->
3. PR 686 rewrites the invariant test around the capability: the NG-2 test now says "the only writes ... are the three calls on the `hold:plan` label" and asserts `writes and all("hold:plan" in ...)` (`pr-a/tests/issue_watch/test_security_invariants.py:12`, `:634-645`). Dormant code keeps the loosened test in master.
4. "Dormant" means only "no grant in a hand-edited list": `has_grant` at `pr-a/src/superclaude/cli/issue_watch/repos.py:113-115`, used at `cycle.py:1021-1027`. The standing grant list (DQ6) is the element the owner's per-issue grant row rejects (FULL-REPORT.md section 5 table). One config line turns on GitHub writes with no code review and no NG-2 amendment.
5. The dormant form is not clean. With no grant a failing issue logs `hold_write_failed` on every cycle (`cycle.py:1021-1027`, pinned by `tests/issue_watch/test_hold.py:416-426`, which asserts the warning). Row 3 (check passes, `hold:plan` still on the issue) returns "skip" when the grant is missing (`cycle.py:1064-1070`), so a good issue with a leftover label is stuck (read from code, not run).
10. The design's own reference `repos.yaml` lists the grant: `grants: [issue.assign, issue.comment, issue.body.append_plan_sections, issue.hold, pr.merge, issue.close]` (`/home/coder/.cache/ic-snap-20261120/pr-a/docs/designs/orchestrator.md:291`; the `grants` row at `:872` repeats the list). The default test fixture also lists it (`/home/coder/.cache/ic-snap-20261120/pr-a/tests/issue_watch/conftest.py:286`). No code under `issue_watch/` outside `repos.py` writes or defaults a `grants` value (grep: no match), so nothing in code turns it off. So "dormant" is not the default: if the reference config is copied, the label writes run on the first live cycle (diff point A-001). Both advocates accepted this fact. <!-- Source: Variant 2 (CLAY), Section Cited facts (concession on moderator fact M1, diff-analysis.md) - merged per Change #1 -->
11. With no grant, `_hold_write_ok` (`cycle.py:1021-1027`) warns and returns False. Row 4 (check fails, no label, no entry) then returns "skip" before `record.set_hold` is reached (`cycle.py:1080-1083`), so for an issue the poll finds itself no `holds` entry is written and the quiet hour never starts. Row 3 (check passes, label still on) also returns "skip" (`cycle.py:1064-1070`, see fact 5). Read from code, not run. Both advocates accepted this fact. <!-- Source: Variant 2 (CLAY), Section Cited facts (concession on moderator fact M2, diff-analysis.md) - merged per Change #1 -->
6. Size of what a read-only variant removes: `LabelWriter` (`github.py:983-1069`), four argv builders (`github.py:267-320`), rows 3 to 5 of `_hold_step` (`cycle.py:1064-1119`), the `hand_removed` state, and about 17 lines of `test_hold.py` that mention a label call or `hand_removed` (grep count, rough).
7. D09 settled that the label's only unique effect is visibility and nobody showed a reader (D09 VERDICT, strongest point OURS 2); the owner's bar is a clear, evidenced benefit.
8. The form of the later label write, and its gate, are described in the section "The deferred label-write form" below. <!-- Source: Base (original, modified) - Change 2, one-line fact replaced by a pointer to the new section; numbering kept so references still resolve -->
9. The ladder the owner works by: speculative code with no named user is skipped and named in one line.

<!-- Source: Base (original, modified) - Change 4 (costs priced by Variant 2 added) and Change 6 (row references made consistent); the base sentence is split into bullets -->
## Costs

- Rework of Clay's `_hold_step` (about 75 lines shrink to about 30) and tests. These figures are rough counts: the size of the rework is unmeasured on both sides (diff point C-005, unresolved).
- `test_hold.py` is 1,073 lines with 58 tests (grep count), so cutting rows 3 to 5 is a rewrite of a tested module right before the unification merge. This cost is priced in Clay's paper and is real.
- A rebase request on a PR Clay owns.
- A person-placed `hold:plan` (row 6) stops being a stop signal; `hold:backlog` remains. Clay's side won this point (diff point C-011, 65%), and it is minor.
- Restoring the label write is a second PR, with the NG-2 amendment, where the dormant form would need one grant line plus the amendment (diff point C-009, Clay's side 65%). The later label PR must also repeat some tests.
- Fallback if the rework is judged too large: delete only the write calls, keep the table and the entry creation, and drop `issue.hold` from the reference config.

<!-- Source: Variant 2 (CLAY), Section Mechanism and Cited fact 2 (`github.py:983-992`) - merged per Change #2; replaces the base's one-line fact 8; base fact 8 content (add and remove one label, grant gated, no comment; gate is an NG-2 amendment) is Base (original) -->
## The deferred label-write form

When someone shows a reader for the label, the label write returns in its own PR. That PR restores a form that is already written down in design 4.11, in PR 686's history and in D09:

- One label, added and removed, with no comment. In PR 686, `LabelWriter` has "no comment call here and no way to build one" and an injected refusal guard (`github.py:983-992`).
- Grant gated. `_hold_write_ok` (`cycle.py:1021-1027`) refuses every label write unless `rdoc.has_grant("issue.hold")` (`repos.py:113-115`); a refusal returns "skip" and records nothing.
- The same six-row table (`hold.py:146-168`) drives the decision.
- Gated for switch-on by the NG-2 amendment in that later PR, then by the dry-run shadow run and the cron label-write test described under Risks.

<!-- Source: Base (original, modified) - Change 3 (switch-on gate added); the first two risks are Base (original) -->
## Risks

- The plan-request clock keys on local `holds` entries that today are created at row 4 together with the label write (`cycle.py:1091-1096`, `:1139-1149`); the rework must create the entry without the write or the quiet hour never starts.
- If a person at once wants the label visible, a second PR is needed.
- Switch-on gate for any later label write: the 24-hour dry-run shadow run (the gate D09 sets) plus a cron label-write test, both before the grant is switched on. The read-only variant keeps the `would_hold` listing so that the shadow run has something to show.

<!-- Source: Variant 2 (CLAY), Section Costs and concessions (concession on A-002, sizing before the rework request) - merged per Change #5 -->
## Conditions and open points

The debate did not converge (71.4%, depth quick); the moderator resolved six open points.

Condition before the rework is asked of Clay: size it. Both papers treat PR 686 as the place the decision lands, assume it will be edited by Clay or by the owner before merge, and assume a rework request is acceptable (diff point A-002); both advocates qualified this. Whether stripping is a cheap deletion or a negotiation on someone else's PR depends on the size, and neither side measured it. Sizing step: count the lines and tests that `LabelWriter`, the four argv builders, rows 3 to 5 and the `hand_removed` state touch, then choose between the full read-only rework and the fallback listed under Costs.

Open points, not settled by the debate:

- Is a grant plus the NG-2 test a sufficient switch for label writes (diff point C-002, 55%)? This paper holds it is not, because the standing grant list is the element the owner's per-issue grant row rejects (fact 4). The Variant 2 advocate's own hybrid drops the grant from the reference config.
- Size of the rework (diff point C-005): handled by the sizing step and the fallback.
- Whether the dry-run shadow run needs the full label code (diff point C-007, 50%): the moderator kept `would_hold` and dropped `would_release` (see What it gets right).

<!-- Source: Base (original, modified) - Change 3 (dry-run sentence replaced, from Variant 2 fact 3 and the moderator note on X-003) and Change 6 (dry-run claim corrected) -->
## What it gets right (of Clay's work)

The plan check is a pure text function (`hold.py:122-143`), `hold:backlog` is a read-only person-set stop, and the audit reasons. All are kept.

`--dry-run` is kept in part. `would_hold` and `would_release` are filled today only in the label branches (`cycle.py:1065-1078`). The rework keeps a `would_hold` listing and drops `would_release`, since a read-only variant has no write to preview. D09 makes the 24-hour dry-run shadow run the switch-on gate, so the listing stays.

<!-- Source: Base (original, modified) - Change 6 (Success tests list added; items drawn from facts 5, 10 and 11 and the Risks) -->
## Success tests

1. A zero-write test with the grant absent: the poll writes nothing to GitHub.
2. A leftover `hold:plan` label does not block a passing issue (the row 3 case, fact 5).
3. The local entry is created with no write, so the quiet hour starts (fact 11 and Risks).
4. The grant `issue.hold` is not listed in the reference config (fact 10).
