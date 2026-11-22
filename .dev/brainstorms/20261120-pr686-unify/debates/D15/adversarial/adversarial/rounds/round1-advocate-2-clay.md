# D15 Round 1, Advocate 2 (CLAY, Clay's line)

Variant 2 = CLAY. "They" is Clay (account `clayphi`); the repository owner is `ironbelly`. Weighting rule applied: OURS wins unless CLAY shows a clear, evidenced benefit; a tie goes to OURS; a clear separable CLAY benefit is a HYBRID.

Notation: "D:nnn" is a line of `docs/designs/orchestrator.md` in `/home/coder/.cache/ic-snap-20261120/master`. "D04" to "D13" are the verdicts in `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/`. "Inventory" is `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/inventory/clay-prs.md`.

## Position summary

The Clay control layer (merge-gate, answer-check, E-NO-GRANT, refuse, escalate, audit, hand-back) should be adopted as ONE verb group with one JSON contract and built once, with T1 to T13, the U-register and the K-register as its single test plan, and with the owner's rules applied as a named amendment list. I withdraw "as built" and I withdraw the contested rules: the weighting rule gives those to OURS, and the verdicts already did. What stays CLAY is the build unit and the test plan, because the verdicts show the controls lean on each other and OURS has no equivalent plan.

## Steelman of OURS

OURS' strongest version: the weighting rule is per element, so a bundle must earn its place row by row. Thirteen verdicts did exactly that, and the result is a hybrid in which almost every Clay part comes in with a change (D06 winner; D04 winner; D07 winner; D10 winner; D11 winner). Taking the stack "as built" would also import five contested rules that are Clay's own rulings, not the owner's (D06 Implications; D04 "What the owner must know"): assignment-only trigger (D01), standing `pr.merge` and `issue.close` grants (D04, D06), no launch guard for `worker-start` workers (D05, D:117), label writes by the poll (D09), and the registry repo (D07). The code encodes some of them, for example the NG-2 test that pins three label calls (D09, Clay strengths: "the NG-2 test changes from three calls to two").

OURS is also right that "as built" is false in several places, each verified: a pinned test forbids the 14 approval reasons that D01 needs back (`pr-a/tests/issue_watch/test_audit.py:86-98`); the wake code acknowledges before the state file exists and loses an abandoned wake (D10 M1 and M2; `pr-a/src/superclaude/cli/issue_watch/cycle.py:777-810`); `answer-check` is hardwired to Clay (D:694; D04 item 5); `E-NO-GRANT` covers at most 2 of 6 grant entries (D04 "Clay strengths to adopt", INV-006); `plan_check` passes an unfilled `<...>` template (D09 item 6). And the verbs are design text: `merge-gate` and `answer-check` exist nowhere in master, PR 686 or the pr-p export (D06 Unverified; D11 "Strongest points" OURS 3). OURS keeps the owner's gates (approval, level none, guard required, a person's go for merge) while taking every cited Clay benefit. That is a sound result.

## Strengths claimed

1. **The controls lean on each other, and the verdicts' own recommendations show it.** This is the one fact the per-element table has to carry as extra rows.
   - Merge: `E-NO-GRANT` does not see a raw `gh pr merge`, so the merge must go through one verb that demands the go entry (D06 item 8, INV-011). That verb needs the gate run twice (D06 item 2, INV-001) and a new gate reason "no recorded merge go" (D04 item 6). The go is checked by an `answer-check`-style verb with the owner identity as a parameter (D04 item 5; D06 item 9).
   - Config guard: the `repos` verbs refuse to change `grants`, `reach_daily_max` or `merge_safety_files` without an accepted `--answer-ref` (D:758, D:1116; D04 item 7).
   - Refusal: the release and tag patterns of `refuse` pass only with an `answer_ref` that `answer-check` accepted (D:767). The `--interrupt` pattern passes only when the caller is `escalate` (D:749, D:767).
   - Tests: T13 pins merge-gate reasons and the `answer-check` question key together (D:1141).
   If one of these is rejected or deferred, its neighbours need a rewrite. OURS' own "What it risks" says the same: a table "must say, per row, which neighbours it needs".

2. **One test plan and one register of what is unproven.** The design carries T1 to T13 (D:1123-1141), a U-register (60 `| U<n> |` rows from D:1253 onward, by my count of the grep) and a K-register (11 rows by the same count). The verdicts keep asking for exactly these live checks: D10 item 13 (mailbox send from outside a Run, U5; `tui-idle` meaning; `orca agent launch` tag, U25), D05 (staging probe), D06 (`orca terminal send` marking; terminal plus `ccsession` start at depth 0, U3). They map onto T1 to T9 and U5, U25, U3. OURS' position paper names no equivalent plan for the coordinator layer; its only live program in the verdicts is issue 442's guard observations (D05). UNVERIFIED that the owner has no other plan outside the verdicts I read.

3. **Capabilities OURS lacks, each verified by a verdict.** Under the weighting rule a capability OURS lacks is a clear benefit: in-flight cap and restart of a dead coordinator (D07, grep zero in the owner's `src/superclaude/cli`); merge gate with head-pinned merge, and the post-merge audit (D06, D05); typed-answer check (D04, D06); closed refusal list (D04, D05); acknowledged wake (D10 CLAY point 1: OURS has only a pending record); hand-back for work a PR did not finish (D:610-616 and D:612 `HANDBACK_MAX`; D12 `--remaining`); nine-row reason list (D11, as an inventory). Every verdict D04 to D11 adopted at least one of these (D06 adopts nine).

4. **Built and reviewed pieces, not only text.** PR 661 is merged (inventory line 43); `/sc:closeout`, the report skill and the design text are merged (PRs 683, 684, 681; inventory line 26); D13 adopts closeout "as is" and D11 adopts the silent-loss rules and `check.py` gate "as is". PR 686 head `8e5ae29ad` shows CI all green and mergeable CLEAN (inventory line 135), though D14 has not decided its fate. PR 690 has three review rounds and a sandbox hand run (D12 CLAY point 2).

5. **One verb group, one JSON contract, one refusal function.** ADD6 (D:140) makes the fixed-result steps verbs of one group; `refuse(argv)` is one function (D:767) with one parametrised test (D:1117). Writing the seven missing verbs against one contract is one design and one parser. Writing them as separate rows means each gets its own contract. This is a build-cost claim; no measured cost exists on either side (UNVERIFIED size), so I rest it on the dependency evidence in point 1, not on a number.

6. **The risk register states its limits.** `refuse` "sees only the commands that the verbs run" (D:769); K22 and U42 stay open; K12 is graded M / H. D06 item 10 turns this into a wording rule ("narrows", not "closes"). Using the register as the base carries those limits into the unified design without a second pass.

7. **"Never ran live" and "unbuilt" cut both ways (X-001).** The owner's own `issue_pipeline` never ran live (FULL-REPORT.md line 43); D10 says "Nothing in either line has run live"; the owner's guard G2 facts 1 to 4 are UNVERIFIED (D05); `GOVERNED_LEVELS_ALLOWED` and R25 exist only in an unpushed worktree (D04 Unverified; D06 Unverified). So those marks do not separate the two lines.

## Weaknesses identified in OURS

1. **No neighbour list (C-001, C-007).** OURS' outcomes include "reject or defer" and "adopt with change", and OURS admits the pieces may lean on a rejected part (its "What it risks", example `E-NO-GRANT` listing `pr.merge`). The verdicts show the leaning is wider than that one example: see Strengths 1. A per-element table without a dependency column will leave dangling references, for instance `answer-check` referenced by the `repos` guard, by `refuse` and by the merge-gate reason but adopted only "with a stated limit" (D06 item 9).

2. **It treats the verbs as separate rows, which hides that they are one unbuilt group (C-002).** OURS states the verbs are design text only (its fact 4) and then prices adoption per element. Seven verbs written one at a time, with a rename each (D08 action 8) and a re-home each (D07), is the case where a shared contract matters most. OURS offers no shared contract.

3. **No coordinator-layer live-test plan (U-004, C-008).** The verdicts require live spikes before anything runs: D10 item 13, D05 staging probe, D06 residual risks, D07 session detection (U25). OURS supplies a plan only for the guard (issue 442; D05). T1 to T13 and the U-list already specify throwaway issues, passes and failures. UNVERIFIED that no other owner plan exists.

4. **Capabilities absent (C-005).** OURS has no cap, no restart, no acknowledged wake, no hand-back (D07; D10 CLAY 1; D12). Its two objections, tier path unverified (U28, D:726) and `HANDBACK_MAX` = 3 "this design's value, not measured" (D:612), are tunable constants and a live check, not defects in the capability. A constant that is not measured is a reason to measure, not a reason to leave the capability out.

5. **The wake defects are reasons to amend, not to reject (C-004).** M1 and M2 are real in Clay's code. D10 still picks Clay's transport as the winner and fixes both with two spec lines (acknowledge only after the state file exists; retarget or surface an abandoned wake). OURS has no signal that a running coordinator saw a claim (D10 CLAY point 1; Coder issue 516 gap), so the defects do not tip C-004 to OURS.

6. **The reasons table argument stops at "edit one test" (C-003, U-001).** The test at `test_audit.py:86-98` forbids the 14 old reasons. That is correct and it blocks "as is". But the cure is a reviewed edit to a pinned table, and the table is how new skip reasons get a visible, closed home. D01 already adds `plan_incomplete` and `held_backlog` and says the dashboard must see them (D01 Implications); D07 adds `coordinator_full` and `name_collision`. Master's table has 59 reasons (arithmetic at `test_audit.py:98`) and OURS has no counterpart for the new ones.

7. **The "unbuilt counts against a piece" argument is asymmetric (X-001).** See Strengths 7. OURS' own R23, R25 and R33 are in an unpushed local plan; its guard binding for `worker-start` workers has never been observed (D05 CLAY point 1).

8. **OURS also rests on the verdicts as if they were rulings (A-001).** D01 R19, D04 R9 and R10, and D06 amendments await owner approval in chat. Both papers lean on that baseline.

## Concessions

- **"As built" is withdrawn.** Eight places need a fix or an override before adoption: (1) the 14-reason test; (2) M1; (3) M2; (4) `answer-check` hardwired to Clay (D:694); (5) `E-NO-GRANT` covers at most 2 of 6 entries (INV-006); (6) `plan_check` placeholder gap (`hold.py:69-70`, `:140`; D09 item 6); (7) `plan_body.py` passes any non-empty text except "Not known yet" (D12); (8) the copied terminal code with no parity test (D10 item 9).
- **C-006, the five contested rules, go to OURS.** Assignment-only trigger, standing `pr.merge` and `issue.close`, no launch guard, label writes by the poll, and the registry repo are all rejected or re-homed by D01, D04, D05, D06, D07 and D09. I do not argue them. Clay's rulings 3, 8, 9 and 10 are Clay's, not the owner's (D05 and D07 "What the owner must know").
- **C-009, where settings live, goes to OURS.** Per-repo config under `~/.config/superclaude/issue-watch.d/`, no `repos.yaml`, no registry repo (D07). CLAY's key set is adopted inside it (D07 item 5).
- **X-002, who pays the rewrite: tie, so OURS.** Renames (D08 action 8) and re-homes (D07) cost the same either way. No measured cost of either approach exists. My one remaining point is that the interface edits are the same three or four edits reused across rows (grants list, `answer-check` owner, merge needs the go, `E-NO-GRANT` scope). That is evidenced by repetition across D04, D05, D06 and D11, but its size is UNVERIFIED.
- **PR 690's "23,043 tests passing"** is a full-suite count on the first head, so it says little about the plan feature. D12 still needs four adaptations before merge (fence-aware heading count, one definition of "passes", document the `--remaining` caller, confirm the live head). I use PR 690 only as evidence of three review rounds and a hand run.
- **The Owner column of the design (U-007)** says "decided (ruling N)" or "no" (D:109-140), and the rulings are Clay's. It does not give the repository owner a ruling place. I drop that as a strength.
- **Tier settings are a tie, so OURS (defer).** The path through `worker-start --model <picker id>` is UNVERIFIED (U28, D:726). The cap of 5 notices (ruling 39) is Clay's ruling, not settled (D11 table).
- **Nothing in the set has run live.** The U-register has 60 rows, and T1 to T13 are not yet run. The verb group is design text (D06 Unverified). Adoption means writing it, and that is why the build unit matters.
- **Risk of accidental landing is real.** Importing a code-and-test set can land a contested rule through a test pin (the NG-2 example). I accept a guard: no row lands without its named amendment and a failing-then-passing test.

## Shared assumptions

- **A-001 (verdicts as baseline): QUALIFY.** Fine as a working baseline, but they are recommendations and D01 R19, D04 R9 and R10 and D06 amendments need the owner in chat. If the owner flips one, the interlocked verb group still stands; only its trigger and grant rows change.
- **A-002 (per-element classification does not break interlocks): REJECT in part.** It holds for the report, closeout, plan check and `hold:backlog`. It fails for merge-gate, `answer-check`, `E-NO-GRANT`, `refuse`, the `repos` guard and `escalate`, which reference each other (Strengths 1; D:758, D:767, D:1116, D:1141).
- **A-003 (a carrier PR exists for each element): QUALIFY.** PR 686 and PR 690 exist. The verb group has no carrier: PR B does not exist (Inventory line 49; D06 Actions). So there is no PR to cherry-pick from; the group must be built, and building it once is the CLAY point. D14 still decides PR 686.
- **A-004 (the verbs bind what they claim): ACCEPT as a limit.** `refuse` sees only commands the verbs run (D:769, K22). `answer-check` cannot tell a person from a script (D06 INV-003). `E-NO-GRANT` misses raw `gh pr merge` (INV-011). The unified text must say "narrows", never "closes" (D06 item 10).
- **A-005 (weighting rule applies to bundles): ACCEPT.** I apply it by conceding C-003 as-is, C-006, C-009, X-002 and the tier settings, and by claiming only the build unit, the test plan and the capabilities OURS lacks.
- **A-006 (one settings file is chosen once): ACCEPT.** D07 picks per-repo config under `issue-watch.d/`, so the keys `grants`, `merge`, tier keys and `reach_daily_max` move there once. Each key that changes authority keeps its `--answer-ref` guard, because that config directory is "not tamper-protected" (D07 item 5; D04 item 7).
- **A-007 (names change before merge): QUALIFY.** Agree for wire and persisted names: `/sc:orchestrator --wake`, `orchestrator-<short>-<n>`, `.orchestrator/`, `orchestrators.json` and `target.orchestrator` (D08 action 8; D10 item 12 says to rename ack buckets only with both readers and a pinned schema). A single rename sweep over one verb group is easier to test than one per element. But the rename cost itself is the same for both lines.

## Per-point verdicts (C-001 to C-009, X-001, X-002)

- **C-001 unit of adoption: HYBRID.** CLAY for the control verbs as one build and test unit, OURS for the decision on every rule row; the verdicts show the interlocks (Strengths 1).
- **C-002 status of unbuilt verbs: HYBRID.** OURS is right that they are text only, CLAY is right that they are one group with one contract (D:140), so they are written once.
- **C-003 62-reason table: OURS as is, CLAY as a pattern.** The test forbids 14 reasons D01 needs; keep the closed, pinned form and the changed exit codes, edit the test in a reviewed change.
- **C-004 wake transport: HYBRID.** Clay's file plus acknowledgment wins (D10 CLAY points 1 to 3); OURS' M1 and M2 become mandatory conditions.
- **C-005 tier settings and hand-back: HYBRID.** Hand-back is a capability OURS lacks, so CLAY; tiers are a tie on UNVERIFIED U28, so OURS defers; `HANDBACK_MAX` stays a labelled, unmeasured default.
- **C-006 contested rules: OURS.** Owner gates win on all five; CLAY's amendment list is only the vehicle that carries the overrides.
- **C-007 who pays the rewrite: OURS (tie).** Equal rename and re-home cost; no measured saving, my residual point is UNVERIFIED in size.
- **C-008 readiness evidence: HYBRID.** CLAY wins for merged and reviewed pieces (PRs 661, 683, 684, 690 review rounds); OURS wins that the unbuilt verbs carry no proof and that plan check is presence only.
- **C-009 where settings live: OURS.** Per-repo config, no registry (D07); CLAY's key set is adopted inside it.
- **X-001 "never ran live" or "unbuilt" counts against a piece: split.** CLAY wins on "never ran live" (both lines, D10; FULL-REPORT.md line 43); OURS wins on "unbuilt" as weak evidence for the verb rows. So the weighting rule asks for a capability gap, which Strengths 3 supplies.
- **X-002 piecemeal adoption multiplies the rewrite: OURS.** Rename and re-home are the same either way, and no cost figure favours the set.

## What I ask the judges to take

A HYBRID with this shape: OURS decides every rule row; CLAY's control verbs are built as one group against one contract; T1 to T13, the U-register and the K-register become the single test plan, amended; and a named amendment list carries the overrides. That list is already finite in the verdicts: grants without `pr.merge` and `issue.close` (D04 action 4; D:116, D:291, D:872); `answer-check` owner parameter (D04; D:694); merge go entry, second gate run, new gate reason (D06 items 1, 2, 8; D04 item 6); rewrite DQ7, OD1, K12 for the guard (D05); rewrite DQ8, ADD1, ADD4, OD3, OD4, K7 (D06 action 4); wake M1 and M2 (D10); config home (D07); names (D08).
