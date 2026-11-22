# Diff Analysis: position paper comparison (Q03, dormant hold:plan label code in PR 686)

Variant 1 = OURS (`position-OURS.md`: remove the label-writing code from PR 686 now, ship a read-only variant). Variant 2 = CLAY (`position-CLAY.md`: keep the label code dormant behind the `issue.hold` grant). Level column = debate taxonomy level (L1 surface, L2 structural, L3 state mechanics), assigned by signal terms, highest level wins.

## Metadata
- Generated: 2026-11-20T07:58:00Z
- Variants compared: 2
- Total differences found: 17 comparable points plus 4 promoted shared assumptions (S 2, C 11, X 4, U 8, A 4)
- Categories: structural (2), content (11), contradictions (4), unique (8), shared assumptions (4 promoted, 3 stated and not promoted)
- Convergence denominator (S + C + X + A): 21

## Moderator-verified facts (read from the pr-a snapshot, available to both advocates)

- M1. The design's own reference `repos.yaml` lists the grant: `grants: [issue.assign, issue.comment, issue.body.append_plan_sections, issue.hold, pr.merge, issue.close]` (`/home/coder/.cache/ic-snap-20261120/pr-a/docs/designs/orchestrator.md:291`; the `grants` row at `:872` repeats the list). The default test fixture also lists it (`/home/coder/.cache/ic-snap-20261120/pr-a/tests/issue_watch/conftest.py:286`). No code under `issue_watch/` outside `repos.py` writes or defaults a `grants` value (grep: no match), so nothing in code turns it off.
- M2. With no grant, `_hold_write_ok` (`cycle.py:1021-1027`) warns and returns False. Row 4 (check fails, no label, no entry) then returns "skip" before `record.set_hold` is reached (`cycle.py:1080-1083`), so for an issue the poll finds itself no `holds` entry is written and the quiet hour never starts. Row 3 (check passes, label still on) also returns "skip" (`cycle.py:1064-1070`). Read from code, not run.
- M3. `plan_check` and the skip need no write: `hold.plan_check` is pure text (`hold.py:122-143`), and the label presence is read from the search row (`cycle.py:1052`).
- M4. The design says a failing check holds the issue "whatever the label shows" (pr-a `docs/designs/orchestrator.md` 4.11 point 10(a)) and lists status output and audit log (`held_incomplete`) as places the user sees a hold (point 8).

## Structural Differences

| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Severity | Level |
|---|------|------------------|------------------|----------|-------|
| S-001 | Section skeleton and fact count | Claim, Mechanism, 9 cited facts, Costs, Risks, What it gets right; paths preamble | Same skeleton, same order, 9 cited facts, paths preamble | Low | L1 |
| S-002 | Credit section | "What it gets right (of Clay's work)": lists the Clay parts that are kept | "What it gets right": credits its own design choices | Low | L1 |

## Content Differences

| # | Topic | Variant 1 (OURS) | Variant 2 (CLAY) | Severity | Level |
|---|-------|------------------|------------------|----------|-------|
| C-001 | What ships in PR 686 | Remove `LabelWriter`, label create/add/remove, rows 3 to 5 of `_hold_step`, the `hand_removed` state; keep `plan_check`, `held_incomplete`, `hold:backlog` | Keep all of it; the label write is off unless the grant `issue.hold` is listed | High | L2 |
| C-002 | What turns the writes on | One hand-edited config line (the standing grant list, DQ6); no code review, no NG-2 amendment | The grant plus the NG-2 amendment plus the NG-2 test that pins exactly the label calls | Medium | L3 |
| C-003 | Behaviour with no grant | Warns `hold_write_failed` every cycle; a good issue with a leftover label is skipped (row 3) | Silent after a "one-line change"; row 3 not discussed | Medium | L3 |
| C-004 | The NG-2 invariant test | Rewritten to allow three label calls; dormant code keeps the loosened test | Still bounds the capability: any write beyond `hold:plan` POST or DELETE fails | Medium | L3 |
| C-005 | Size of the rework | `_hold_step` about 75 lines to about 30; about 140 lines removed from `github.py`; about 17 test lines mention label calls | `test_hold.py` is 1,073 lines and 58 tests; rows 3 to 6 are a rewrite right before unification | Medium | L2 |
| C-006 | The quiet-hour clock and `holds` entries | Entry must be created without the write, or the hour never starts | Entries are created at row 4 with the write; removing the write path means reworking rows 3 to 6 | Medium | L3 |
| C-007 | Dry-run shadow run as the switch-on gate | Keeps `--dry-run` as a read-only listing | Only the full code can produce the 24-hour shadow run that D09 makes the gate | Medium | L2 |
| C-008 | Evidence that anyone reads the label | None shown (D09: both sides conceded) | Ruling 33 sets the label as the design's visible mark; the owner's own branch writes a label | Medium | L2 |
| C-009 | Cost of enabling the label later | A small separate PR that restores the code and amends NG-2 | One grant line plus the NG-2 amendment | Medium | L2 |
| C-010 | Where a held issue shows without the label | `issue-watch status` and the audit log (M4) | The label on GitHub | Low | L2 |
| C-011 | A person placing `hold:plan` by hand | No longer a stop signal (`hold:backlog` remains) | Still works (row 6) | Low | L2 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact | Level |
|---|-------------------|--------------------|--------------------|--------|-------|
| X-001 | Is "dormant" the default? | "Dormant means only no grant in a hand-edited list"; one config line enables | "Today no repo names it, so the poll writes nothing" | Medium | L3 |
| X-002 | How clean is the dormant state after the fix | Row 3 sticks a good issue with a leftover label (M2); warning every cycle | "A one-line change makes the no-grant state silent" | Medium | L3 |
| X-003 | Does the dry-run survive the removal | Lists `--dry-run` among what is kept | `would_hold` and `would_release` are filled only in the label branches (`cycle.py:1065-1078`), so a read-only variant has no write to preview | Low | L2 |
| X-004 | Is "the watcher package never writes" literal | NG-2 as written: the poll writes nothing to GitHub | Already not literal: the owner's local branch creates a label once per repo (`repo_init.py`, not re-read, UNVERIFIED) | Medium | L2 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | 1 (OURS) | The row 3 defect: a leftover label blocks a passing issue when no grant is set (`cycle.py:1064-1070`) | High |
| U-002 | 1 (OURS) | The standing grant list (DQ6) is the element the owner's per-issue grant row rejects (FULL-REPORT.md section 5) | Medium |
| U-003 | 1 (OURS) | Shipping the code makes master's NG-2 text untrue about the capability and replaces the zero-write test | Medium |
| U-004 | 1 (OURS) | Inventory of what a read-only variant removes (argv builders, `hand_removed`, live label read) | Low |
| U-005 | 2 (CLAY) | `LabelWriter` is narrow by construction: no comment call, injected refusal guard (`github.py:983-992`) | Medium |
| U-006 | 2 (CLAY) | `--dry-run` with `would_hold` and `would_release` is the test bed for any later switch-on | Medium |
| U-007 | 2 (CLAY) | Ruling 33 and the owner branch's init label write as precedent for a once-per-repo label write | Low |
| U-008 | 2 (CLAY) | Reworking a 58-test module right before the unification merge is itself a risk | Medium |

## Shared Assumptions

Classified STATED (kept, not promoted): (a) a failing `plan_check` alone holds the issue without the label (M4); (b) enabling any write needs an NG-2 amendment that tests enforce; (c) the one-hour plan request is a wake-file item, not a GitHub write (D09).

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|-----------|------------------|--------|--------|
| A-001 | The grant `issue.hold` is absent in the config that will run, so "dormant" is the real default | Both treat dormant as "no writes today" | A shipped reference config lists the grant (M1); if copied, the label writes run on the first live cycle | UNSTATED, promoted, L3 |
| A-002 | PR 686 will be edited by Clay or by the owner before merge, and a rework request is acceptable | Both treat PR 686 as the place the decision lands | Decides whether strip is a cheap deletion or a negotiation on someone else's PR | UNSTATED, promoted, L2 |
| A-003 | The quiet-hour clock and the plan request keep working when the label write is off | Both say entries are created at row 4 | With no grant, row 4 returns before `set_hold` (M2), so poll-found issues never get an entry or a plan request | UNSTATED, promoted, L3 |
| A-004 | A grant list in a config file is protected against edit by an untrusted party | Both treat the grant as the switch | D07 records the config directory "is not tamper-protected" (`launch.py` 48-53, via D07 VERDICT); which file holds this grant is UNVERIFIED | UNSTATED, promoted, L3, UNVERIFIED |

## Summary
- Total structural differences: 2
- Total content differences: 11
- Total contradictions: 4
- Total unique contributions: 8
- Total shared assumptions surfaced: 7 (UNSTATED 4 promoted, STATED 3, CONTRADICTED 0)
- Highest-severity items: C-001 (High), U-001 (High)
- Taxonomy coverage: L1 = S-001, S-002; L2 = C-001, C-005, C-007 to C-011, X-003, X-004, A-002; L3 = C-002, C-003, C-004, C-006, X-001, X-002, A-001, A-003, A-004. All three levels have points.
