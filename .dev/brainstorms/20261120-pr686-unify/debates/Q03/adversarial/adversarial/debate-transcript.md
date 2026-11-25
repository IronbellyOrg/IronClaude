# Adversarial Debate Transcript (Q03)

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 3 skipped: depth=quick)
- Convergence achieved: 71.4% (15 of 21 points)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (Variant 1 OURS, Variant 2 CLAY), both general-purpose agents on the session model
- Round 2.5 (invariant probe): skipped, --depth quick. No invariant-probe.md is written; the invariant gate is not applied.
- Taxonomy coverage gate: L1, L2 and L3 each have at least one point addressed by both advocates; no forced round.
- Shared-assumption omissions: none (both advocates answered A-001 to A-004).

## Round 1: Advocate Statements

### Variant 1 Advocate (OURS)

**Position**: Strip the label-writing code from PR 686 and ship the read-only hold: `plan_check`, the `held_incomplete` skip and the person-set `hold:backlog` stop. Clay's dormant form is not actually dormant or clean: it switches off the plan-request mechanism along with the label, and one config line turns on GitHub writes. Nobody has shown a reader for the label, so Clay has no evidenced benefit to outweigh the owner's NG-2 line.

**Steelman of Variant 2**: The hold is one tested design. Rows 3 to 6 of `_hold_step`, the `holds` entries and the plan-request clock are interlocked (`cycle.py:1046-1149`). `test_hold.py` has 1,073 lines and 58 tests (Clay's count, not re-checked); cutting into it right before the unification merge is a real risk. Writes are gated by the grant `issue.hold` (`cycle.py:1021-1027`), `LabelWriter` has no comment call (`github.py:983-992`), and the NG-2 test still fails any write other than POST or DELETE on `hold:plan` (`test_security_invariants.py:634-645`). The `--dry-run` listing (`would_hold`, `would_release`, `cycle.py:1065-1078`) is the test bed for any later switch-on, and enabling the label later is one grant line plus the NG-2 amendment. Clay is also right that "never writes" is not fully literal if the owner's own branch creates a label at init (from Clay's paper, not re-read, UNVERIFIED).

**Key strengths claimed**:
1. The hold works with zero writes: design 4.11 point 10(a) "a failing check holds the issue whatever the label shows", point 8 names status output and the audit log (M4); `plan_check` is pure text (`hold.py:122-143`, M3).
2. Clay's dormant state breaks the hold: with no grant row 4 returns "skip" at `cycle.py:1080-1083`, before `record.set_hold` at `:1091`, so a poll-found issue never gets a `holds` entry and the quiet hour never starts (M2). A read-only variant creates the entry with no write.
3. Row 3 (check passes, `hold:plan` still on) returns "skip" with no grant (`cycle.py:1064-1070`): a good issue with a leftover label is stuck; each failing issue also logs `hold_write_failed` every cycle (`:1026`, pinned by `test_hold.py:416-426`).
4. "Dormant" is not the default: the reference `repos.yaml` lists `issue.hold` (M1: `orchestrator.md:291`, `:872`; `conftest.py:286`). A copied config turns writes on at the first live cycle. This is the standing grant list the owner's per-issue grant row rejects (FULL-REPORT.md section 5, as cited in the paper, not re-read).
5. The invariant weakens even when nothing runs: the NG-2 test is rewritten to allow three label calls (`test_security_invariants.py:634-645`) while master's text reads "no GitHub write" (`master/docs/designs/issue-watcher.md:76`).
6. No reader for the label has been shown (D09: both sides conceded).

**Weaknesses identified in Variant 2**:
1. "One line makes the no-grant state silent" is a promise, not code; it does not address the stuck row 3 or the missing entry (M2).
2. "Today no repo names it" is true only for configs that omit the grant; the design's reference config includes it (M1), so Clay's safety rests on A-001.
3. Clay's rework-risk argument (C-005, U-008) cuts against Clay too: row 4 with no grant must be reworked anyway to create the entry.
4. The dry-run argument is weak: in a read-only variant `would_hold` still lists what the hold catches; only `would_release` has no meaning. The 24-hour shadow gate was D09's gate for switching on writes, not for this PR.
5. Ruling 33 and the init label are precedent for a design choice, not evidence that anyone reads the label.

**Concessions**:
- M2 hurts both sides: the missing entry is a bug in Clay's code, but fixing it means the rework this variant proposes.
- The rework cost is real and lands on a PR Clay owns (A-002); the line counts (about 75 to about 30, about 140, about 17) are rough grep counts.
- Re-adding the label later repeats some tests; a person-placed `hold:plan` stops being a stop signal (C-011).
- The NG-2 test still bounds the capability, a real safeguard.
- Fallback if rework cost blocks: delete only the write calls (`LabelWriter`, `_label_write`) and the grant check, keep the six-row table and entry creation, rewrite the NG-2 test back to zero writes.

**Shared assumptions**: A-001 QUALIFY (dormant is real only if the running config omits `issue.hold`; M1; which file runs is UNVERIFIED). A-002 QUALIFY (acceptable if the owner or Clay edits PR 686 before merge; if Clay refuses, the strip is a negotiation and the fallback applies). A-003 REJECT (row 4 returns before `set_hold`, M2). A-004 REJECT (D07 says the config directory "is not tamper-protected", via D07 VERDICT, not re-read; which file holds the grant is UNVERIFIED).

**Per-point stance**:
S-001 NEITHER 90%; S-002 NEITHER 80%; C-001 OURS 65%; C-002 OURS 60%; C-003 OURS 65%; C-004 OURS 55%; C-005 CLAY 60%; C-006 OURS 60%; C-007 NEITHER 55%; C-008 OURS 70%; C-009 CLAY 55%; C-010 OURS 65%; C-011 CLAY 55%; X-001 OURS 60%; X-002 OURS 65%; X-003 OURS 60%; X-004 NEITHER 50%. (Each line in the agent's report carried a one-sentence reason with evidence; the reasons are folded into the Scoring Matrix below.)

*Moderator note: the agent also cited `HOLD_LABEL` in `record.py` through the paper; the evaluator in Step 3 found the constant is not in `record.py` (the text `hold:plan` appears in its docstring at line 11). Form-level slip, recorded in base-selection.md.*

### Variant 2 Advocate (CLAY)

**Position**: Keep the hold as one tested unit in PR 686 with the label write off unless the repo list names `issue.hold`, and fix the two rough edges (the per-cycle warning and the stuck leftover label). Argued as the cheaper path, but under the weighting rule Clay has to show a clear benefit and some evidence points the other way.

**Steelman of Variant 1**: NG-2 is a written owner non-goal: "no GitHub write (REST GET only ...)" (`master/docs/designs/issue-watcher.md:76`). A grant check is a weaker guard than code review because one config line turns writes on. The label's only unique effect is visibility and D09 records nobody showed a reader. The read-only core already holds the issue "whatever the label shows" (4.11 point 10(a), M4). Variant 1 found a real defect: with no grant row 3 returns "skip" (`cycle.py:1064-1070`) so a passing issue with a leftover label is stuck, and row 4 returns before `record.set_hold` (`cycle.py:1080-1083`) so the quiet hour never starts (M2). Shipping a capability the owner has not approved, with the NG-2 test rewritten to allow it (`test_security_invariants.py:634-645`), is the larger risk. Variant 1 keeps `plan_check`, `held_incomplete`, `hold:backlog` and the audit reasons, so little is lost.

**Key strengths claimed**:
1. The dormant state is pinned by a test: `test_without_the_grant_issue_hold_the_poll_writes_nothing` asserts `writes(world) == []` and `res.woken == ()` (`test_hold.py:416-426`, re-read).
2. The write form is narrow: `LabelWriter` has no comment call and an injected refusal guard (`github.py:983-992`); the NG-2 test fails any write beyond POST or DELETE on `hold:plan`.
3. The rows depend on each other: the plan-request clock keys on `holds` entries created at row 4 and read in `_held` (`cycle.py:1091-1096`, `:1139-1149`); cutting rows 3 to 5 reworks the busiest module (`test_hold.py`: 1,073 lines, 58 tests by Variant 2's count). D09 says Clay "did not size the rework".
4. `--dry-run` fills `would_hold` and `would_release` only in the label branches (`cycle.py:1065-1078`); D09 makes the 24-hour shadow run the switch-on gate.

**Weaknesses identified in Variant 1**:
1. The cost of a rework is asserted, not shown ("about 75 lines to about 30" is an estimate; neither side ran either rework).
2. "Dormant means one config line" is only as strong as the config path; which file holds the grant is UNVERIFIED (A-004); the NG-2 test still bounds the damage to one label on one repo, no comments.
3. Variant 1 lists `--dry-run` as kept, but in a read-only variant `would_hold` and `would_release` have nothing to fill (X-003); the shadow gate loses its subject.
4. The "put it back later" cost is not priced: a second PR must re-add `LabelWriter`, four argv builders, rows 3 to 5, `hand_removed` and the tests, and run another review round.

**Concessions**:
- M1 hurts: the design's reference `repos.yaml` lists `issue.hold` (`orchestrator.md:291`, `:872`) and so does the default fixture (`conftest.py:286`); "today no repo names it" is true only of live config; a copy of the reference turns writes on at the first live cycle; "dormant" is not a safe default unless the reference drops the grant.
- M2 hurts: with no grant a poll-found failing issue gets no `holds` entry, so no plan request ever fires; dormant also means the plan-request feature is dead. Variant 1's read-only form (local entry, no write) is better here.
- The "one-line change makes it silent" claim is not shown and does not repair row 3 or row 4.
- No evidence shows anyone reads the label (C-008); Ruling 33 and the owner branch's label write are precedent, not a reader (`repo_init.py` not re-read, UNVERIFIED).
- Dead code for an unknown time is a cost.

**Shared assumptions**: A-001 QUALIFY (dormant holds only if the grant is absent from the config that runs; the reference must drop `issue.hold`). A-002 QUALIFY (a rework request on Clay's PR is acceptable only if sized). A-003 REJECT (M2). A-004 QUALIFY (a grant in a config file is protected only as far as the file is; D07 says the directory is not tamper-protected; the NG-2 test caps the effect at one label).

**Per-point stance**:
S-001 NEITHER 90%; S-002 OURS 65%; C-001 OURS 62%; C-002 HYBRID 55%; C-003 OURS 72%; C-004 OURS 60%; C-005 NEITHER 60%; C-006 OURS 66%; C-007 CLAY 60%; C-008 OURS 70%; C-009 CLAY 55%; C-010 OURS 65%; C-011 CLAY 55%; X-001 OURS 68%; X-002 OURS 70%; X-003 CLAY 55%; X-004 NEITHER 50%.

**Advocate's own closing hybrid** (not a ruling): keep the narrow `LabelWriter` form and the `--dry-run` listing, decouple the local `holds` entry from the write so the quiet hour and plan request work with no grant, and drop `issue.hold` from the reference `repos.yaml`. This removes M1 and M2 without cutting the tested design. The advocate did not verify that this rework is smaller than stripping the code.

## Scoring Matrix

Confidence rule used: mean of the two advocates' stated confidences, +10 when the losing advocate conceded the point in its text, never above 90. Split points are marked unresolved at 50%.

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|------------|-------|--------|------------|-----------------|
| S-001 | L1 | Neither (agreed) | 90% | Identical skeletons and fact counts |
| S-002 | L1 | Unresolved | 50% | OURS-advocate: neither; CLAY-advocate: OURS; presentation only |
| C-001 | L2 | OURS | 74% | Both advocates: the read-only hold works with zero writes (M3, M4); the dormant form leaves the quiet-hour clock dead (M2); CLAY-advocate conceded |
| C-002 | L3 | Unresolved (OURS lean) | 55% | OURS vs HYBRID; both agree the grant is a weak switch (M1) and that the NG-2 test bounds the damage to one label |
| C-003 | L3 | OURS | 78% | Row 3 stuck and the per-cycle warning are in code (`cycle.py:1026`, `:1064-1070`); CLAY-advocate conceded the one-line fix is not shown |
| C-004 | L3 | OURS | 67% | Test loosened from zero writes to three calls (`test_security_invariants.py:634-645`); the bound it keeps is acknowledged |
| C-005 | L2 | Unresolved | 50% | OURS-advocate: CLAY 60%; CLAY-advocate: NEITHER 60%; both sizes are unmeasured estimates |
| C-006 | L3 | OURS | 73% | M2: with no grant row 4 never creates an entry; a read-only variant can; CLAY-advocate conceded |
| C-007 | L2 | Unresolved | 50% | NEITHER vs CLAY; moderator: `would_hold` survives a read-only variant, `would_release` does not |
| C-008 | L2 | OURS | 80% | No reader of the label shown; both advocates agree |
| C-009 | L2 | CLAY | 65% | One grant line plus the amendment is cheaper than restoring code, but only if the label is ever wanted |
| C-010 | L2 | OURS | 75% | Status output and audit log show a hold (M4) |
| C-011 | L2 | CLAY | 65% | A hand-placed `hold:plan` is lost; `hold:backlog` remains |
| X-001 | L3 | OURS | 74% | M1: the reference config and the fixture list the grant; CLAY-advocate conceded |
| X-002 | L3 | OURS | 77% | Row 3 and the missing entry are in code; the "one line" fix is unshown; CLAY-advocate conceded |
| X-003 | L2 | Unresolved | 50% | OURS vs CLAY; moderator: `would_hold` is still meaningful read-only, low impact |
| X-004 | L2 | Neither (agreed) | 50% | The init label write is unverified and outside the poll that NG-2 governs |
| A-001 | L3 | QUALIFY (both) | 88% | Dormant holds only if the running config omits the grant |
| A-002 | L2 | QUALIFY (both) | 85% | Acceptable only if the rework is sized and agreed |
| A-003 | L3 | REJECT (both) | 90% | M2, read from code |
| A-004 | L3 | Unresolved | 50% | REJECT vs QUALIFY; which file holds the grant is UNVERIFIED |

## Convergence Assessment

- Points resolved: 15 of 21 (S-001, C-001, C-003, C-004, C-006, C-008, C-009, C-010, C-011, X-001, X-002, X-004, A-001, A-002, A-003)
- Alignment: 71.4% (agreement means both advocates name the same superior side or the same ACCEPT, REJECT or QUALIFY answer)
- Threshold: 80%
- Status: NOT_CONVERGED (maximum rounds for depth quick reached); not blocked by taxonomy or invariant gates
- Unresolved points: S-002, C-002, C-005, C-007, X-003, A-004
- Per the error matrix: force-select by combined score, document non-convergence, status partial.
- What the six unresolved points mean: S-002 is wording only. C-005 (rework size) and C-007 (dry-run gate) are unmeasured. C-002 and A-004 turn on which config file holds the grant, UNVERIFIED. X-003 is low impact. None of the six changes the direction of the outcome; they decide how much code is removed.
