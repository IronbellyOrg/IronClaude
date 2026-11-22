# Adversarial Debate Transcript

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: depth=quick; Round 3 skipped: depth=quick)
- Convergence achieved: 87.5% (14 of 16 diff points)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (agent a59412e1f1207f605 for Variant 1, agent a684a1b5bbaca471a for Variant 2; both general-purpose, read-only)
- Taxonomy coverage gate: L1 (S-001), L2 (C-005, C-007, X-002, A-003), L3 (C-001 to C-004, X-001, X-003, A-001, A-004, A-005) all addressed in Round 1; no forced round needed.

## Round 1: Advocate Statements

### Variant 1 Advocate (OURS)

**Position summary.** Variant 1 should win the default. A typed go is needed for the first push and PR, for any push after a revert or rebase, and for the merge. A fix-round push inside one `/sc:pr-submit --monitor 3` run is covered by the typed run line, which is also Variant 1's own admission at Risks bullet 1. Variant 2 shows one separable benefit, adopted as a hybrid.

**Steelman of Variant 2.** `/sc:pr-submit --monitor 3` is by design an unattended fix, push, reply and resolve loop and the typed line is the decision. A go per round turns `--monitor 3` into `--monitor 2` and adds up to 5 prompts. The loop is fenced mechanically: one fix commit per cycle, fast-forward only, halt on `push_range_mismatch`, `push_count <= max_rounds + 1` (SKILL.md:262, 343, 361; pr-submit.md:46-47). A sha-bound go cannot exist for an unwritten commit, and merge is the irreversible step.

**Strengths claimed.**
1. WC:245 is per publication: "no earlier pre-authorization waives this". A go lasting until merge is such a pre-authorization; Variant 2 admits it.
2. Keeping the typed line as the run's go does not break the mandatory PR path (the X-001 resolution).
3. A rebase or revert changes the commit set; the loop is fast-forward only and never force-pushes (SKILL.md:343), so those fall outside the run and need a new go.
4. Variant 1 alone raises the PR 368 incident (memory note, 15 days old, UNVERIFIED); a go that ends at merge, close or head move prevents it.
5. A push go and a merge go never cover each other (SEC-01, SEC-12).
6. WC:23 and WC:244 keep `/sc:pr-submit` off workers.

**Weaknesses in Variant 2.**
1. Mechanism 1 relies on ADD1 (D:135) where a worker runs `/sc:pr-submit`; WC:244 says never as a worker, and D06 item 5 rejected ADD1 (X-002).
2. "Until merge" has no end event (Variant 2 concedes it).
3. SEC-13: a worker script's push would look authorized after the fact.
4. The fence guards only pushes made inside the run (A-005).
5. Merge-time controls catch a bad fix only if the person reads the diff; a never-shown fix commit is the WC:245 problem itself.

**Concessions.** Mechanism 2 contradicts Risks bullet 1 (X-001) and must be rewritten. A sha-bound go is impossible for an unwritten fix commit (U-005). Sha-bound push is not recorded in D06 or Q01 (U-004, X-003). The record and sha check are design only.

**Shared assumptions.** A-001 QUALIFY (a script can type the line, INV-003; the record must come from a person-opened session). A-003 QUALIFY (top-level session only, or WC:23 and WC:244 break). A-004 REJECT (WC:245 does apply to the tool's fix commits; the typed run line is its stated waiver and covers only the run). A-005 QUALIFY (`pr_head_ok` and `push_range_mismatch` stop only a head that moved inside the run). A-006 REJECT (sha pin is merge only).

| Point | Superior | Reason |
|---|---|---|
| C-001 | Hybrid | Sha-bind first push, rebase and merge; the typed run line, no sha, covers fix rounds |
| C-002 | Hybrid | Fix rounds covered by the typed run line (Variant 2's benefit, adopted) |
| C-003 | Variant 1 | Revert or rebase changes the commit set; loop never force-pushes |
| C-004 | Variant 1 | Void at run end, merge or close, or head move; prevents PR 368 |
| C-005 | Variant 1 | R25: "nothing else is pushed"; WC:245 bars earlier pre-authorization |
| C-007 | Variant 1 | WC:23 and WC:244; ADD1 rejected by D06 |
| X-001 | Hybrid | Fix Mechanism text, keep typed run line as the go |
| X-002 | Variant 1 | Contract text explicit |
| X-003 | Variant 1 | Recorded sha binding is merge only |
| S-001 | Neither | Same layout |

### Variant 2 Advocate (CLAY)

**Position summary.** CLAY's strongest part is narrow: the person's typed `/sc:pr-submit --monitor 3` line is the go for every push that run makes, and the tool already fences them. CLAY loses outside that run (a worker pushing, a rebase, a revert, a go that lasts "until merge"). The advocate argues for a hybrid.

**Steelman of Variant 1.** Master is unprotected and the acting user holds `maintain` (D:118). A push publishes unreviewed commits. WC:245: "no earlier pre-authorization waives this". A sha-bound go cannot be reused for another branch state. PR 368 shows a go that outlives PR state is dangerous. Push and merge goes stay separate.

**Strengths claimed.**
1. The tool bounds its own pushes: one fix commit per cycle, `push_range_mismatch` halt, no force push, no push to the default branch, merge-commit parents exactly the PR head and recorded base tip (SKILL.md:342-348, pr-submit.md:121).
2. `push_count <= max_rounds + 1` (SKILL.md:262) and hard cap 5 (pr-submit.md:47) make a run-level go testable.
3. The mandatory PR path is unattended (pr-submit.md:38); a per-fix go behaves like `--monitor 2`, which Variant 1 admits.
4. A sha-bound go cannot exist for a not-yet-written fix commit (Variant 1 Risks bullet 2).

**Weaknesses in Variant 1.**
1. Self-contradiction (X-001): the rule as written is unusable.
2. "Consumed by the push it names" cannot work in a fix loop; the pushed sha does not exist when the person types.
3. The rebase claim is mostly moot for this tool; `pr-submit.md` forbids both, so a rebase is a different actor's act, not a `/sc:pr-submit` push class.
4. "Sha-bound per push" is not in D06 or Q01 (Variant 1 Risks bullet 3).

**Concessions.** Mechanism 1 and fact 1 rest on a route D06 item 5 rejected. "Until merge" has no end event; PR 368 is a real counterexample. A per-issue go given before the commits exist is an "earlier pre-authorization" under WC:245 and needs the R25 amendment, wider. A rebase or revert changes the commit set; one go would silently cover it. A worker's script can push with no guard (D:117 DQ7); a long-lived go would make that look authorized.

**Shared assumptions.** A-001 QUALIFY (person-opened session only; typed text and script text look alike). A-003 QUALIFY (holds for the run line in a top-level session, not for CLAY's worker route). A-004 QUALIFY (the tool's fix commits are not worker commits so WC:245 does not strictly apply, but the typed run line must say so explicitly). A-005 ACCEPT (`push_parent_ok` and git's non-fast-forward rejection stop a head moved by other means). A-006 REJECT (D06 items 1 and 7 name no sha for push).

| Point | Superior | Reason |
|---|---|---|
| C-001 | Hybrid | Bind first push and merge to a sha; fix pushes bind to the run line and its guards |
| C-002 | Hybrid | Fix rounds inside one run covered by the run line; a separable CLAY benefit |
| C-003 | Variant 1 | Rebase or revert is outside the tool, needs its own go |
| C-004 | Hybrid | Ends at the run's terminal status, PR close or merge, or head change outside the run; "until merge" untestable |
| C-005 | Variant 1 | R25 text says "nothing else is pushed"; whether the launched run's loop pushes count is UNVERIFIED |
| C-007 | Variant 1 | WC:23 and WC:244 forbid it |
| X-001 | Variant 2 | Variant 1's Mechanism 2 cannot stand against its own Risks bullet |
| X-002 | Variant 1 | ADD1 rejected, contract explicit |
| X-003 | Variant 1 | Sha-bound push is "OURS extended, not recorded" |
| S-001 | Variant 1 | Tie goes to OURS |

## Scoring Matrix

"Agreed" means both advocates chose the same label, or chose different labels with the same stated resolution (noted).

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 | Variant 1 | 60% | Same layout; tie goes to OURS |
| C-001 | Hybrid | 85% | Both: sha only where the commit exists (first push, rebase, merge); the run line covers fix rounds |
| C-002 | Hybrid | 90% | Both: fix rounds covered by the typed run line; V1 conceded in its own Risks |
| C-003 | Variant 1 | 90% | Both: revert or rebase is outside the tool and needs its own go |
| C-004 | Hybrid | 80% | Labels differ (V1 says V1, V2 says Hybrid) but both end the go at run end, PR close or merge, or head move outside the run |
| C-005 | Variant 1 | 85% | Both follow R25 "nothing else is pushed"; loop pushes of the launched run UNVERIFIED |
| C-006 | Variant 1 | 95% | Merge is its own go in both papers |
| C-007 | Variant 1 | 95% | WC:23, WC:244; ADD1 rejected by D06; V2 conceded |
| C-008 | Hybrid | 70% | Both state the 5-prompt cost; resolved by C-002 |
| X-001 | Hybrid | 85% | Labels differ (V1 Hybrid, V2 Variant 2) but both say rewrite Mechanism 2 and keep the typed run line as the go |
| X-002 | Variant 1 | 95% | Both agree ADD1 route is out |
| X-003 | Variant 1 | 95% | Both agree the sha pin is merge only |
| A-001 | Qualified | 85% | Both QUALIFY: person-opened session; spoofing is a residual risk |
| A-003 | Qualified | 85% | Both QUALIFY: top-level session only |
| A-004 | Unresolved | 50% | V1 REJECT (WC:245 applies, run line is the waiver) vs V2 QUALIFY (WC:245 not strictly applicable, run line must say so); same drafting outcome |
| A-005 | Unresolved | 55% | V1 QUALIFY (guards only inside the run) vs V2 ACCEPT (guards stop other head moves) |

## Convergence Assessment
- Points resolved: 14 of 16 (S-001, C-001 to C-008, X-001 to X-003, A-001, A-003)
- Unresolved: A-004, A-005 (both end in one drafting requirement: the contract text must name the typed run line as the go for that run's pushes and say a head moved outside the run voids it)
- Alignment: 87.5%; Threshold: 80%
- Status: CONVERGED (Round 2.5 invariant probe skipped by depth quick, so the invariant gate was not applied)
