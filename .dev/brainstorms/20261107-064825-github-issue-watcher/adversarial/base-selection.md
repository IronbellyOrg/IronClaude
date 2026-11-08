# Base Selection Report

- Artifact: Step 3 of the blind adversarial comparison of requirement-spec variants A to E (seed: `seed-brief.md`; fixed decisions D1 option A, D2 claim-only, D3 integer-only prompt)
- Inputs merged: `scoring-pass1-forward.md` (P1), `scoring-pass2-reverse.md` (P2), `rounds/round2-tally.md`, `rounds/round3-tally.md`; variants opened only to settle disagreements
- Formulas (scoring-protocol A.1 to A.3): quant = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC; qual = criteria met / 30; final = 0.5 quant + 0.5 qual

## Quantitative Scoring (50% weight)

Each cell: P1 / P2 / average. The final quant uses the average of the two passes per metric. The passes used different extraction bases (P1: 40 seed topics for RC; P2: 20), so the averages smooth method noise rather than hide it.

| Metric | Weight | A | B | C | D | E |
|---|---|---|---|---|---|---|
| requirement_coverage | 0.30 | .975 / 1.000 / **.988** | .975 / 1.000 / **.988** | 1.000 / .950 / **.975** | .975 / 1.000 / **.988** | .975 / 1.000 / **.988** |
| internal_consistency | 0.25 | .988 / .964 / **.976** | .985 / .942 / **.964** | 1.000 / 1.000 / **1.000** | 1.000 / 1.000 / **1.000** | .967 / .980 / **.974** |
| specificity_ratio | 0.15 | .959 / .968 / **.964** | .985 / .971 / **.978** | .828 / .545 / **.687** | .982 / 1.000 / **.991** | .959 / .973 / **.966** |
| dependency_completeness | 0.15 | 1.000 / .971 / **.986** | 1.000 / 1.000 / **1.000** | 1.000 / 1.000 / **1.000** | 1.000 / 1.000 / **1.000** | 1.000 / 1.000 / **1.000** |
| section_coverage | 0.15 | 1.000 / 1.000 / **1.000** | same | same | same | same |
| **quant_score** | | **.983** (P1 .983, P2 .982) | **.984** (P1 .987, P2 .981) | **.945** (P1 .974, P2 .917) | **.995** (P1 .990, P2 1.000) | **.985** (P1 .978, P2 .991) |

Notes on the largest gaps:
- C specificity: P1 counted every non-concrete line as vague (.828); P2 used a vague-word grep plus statement judgment (.545). Both agree C is the least specific (no launch argv, discovery command or config keys). The average is used.
- IC: both passes agree on direction. A and B lose on OD-5 / FR-022 / NFR-010 / the lost-reply path; E loses on FR-014 `<agent>` plus three more (confirmed below); C and D have none.
- A DC .971 (P2): `launched_unclaimed` is missing from A's NFR-007 audit enum. B to E resolve every internal reference.

## Qualitative Scoring (50% weight), additive binary rubric, 30 criteria

### Reconciliation method

The passes used different 30-criterion lists. P1 used a task-specific list (Q1 to Q30). P2 used the protocol list (scoring-protocol A.2). Comparing them by position would be meaningless, so the merge uses the protocol slots as the single rubric: C1-C5 Completeness, K1-K5 Correctness, S1-S5 Structure, L1-L5 Clarity, R1-R5 Risk coverage, E1-E5 Invariant and edge case. Each P1 finding is placed in the one slot it best breaches, so no defect is counted twice.

| P1 item | Slot | Why |
|---|---|---|
| Q8 argv contract, variant states wrong content (E) | K2 | Violates a fixed seed constraint (`--agent claude`) |
| Q8, Q18, Q20 argv, discovery command, config keys absent (C) | L2 | Omission, so a concreteness gap |
| Q9 fresh launch after an ambiguous outcome | K2 | Violates the at-most-once constraint |
| Q10 internal contradiction | K4 | Same wording |
| Q15 risk register lacks likelihood/impact or mitigation | R1 + R2 | The protocol puts it under Risk, not Structure |
| Q25 rate-limit signal not handled | R4 | External-dependency failure |
| Q27 bot actor not excluded | E3 | Guard condition gap |
| All other Q (Q1-7, 11-14, 16, 17, 19, 21-24, 26, 28-30) | MET in P1 and P2 | No slot-level conflict |

Re-evaluation rule: where the two passes differ on a slot, the variant text was opened and the slot re-judged once with both evidence lines in view. A fact that does not breach the slot's wording is not a miss and is carried to the incorporate list instead.

### Dimension subtotals (raw P1, raw P2, final on protocol slots)

| Variant | Compl | Corr | Struct | Clar | Risk | Edge | P1 /30 | P2 /30 | **Final /30** | **qual** |
|---|---|---|---|---|---|---|---|---|---|---|
| A | 5 | 3 | 5 | 5 | 5 | 5 | 28 | 28 | **28** | **.933** |
| B | 5 | 3 | 5 | 5 | 5 | 4 | 26 | 29 | **27** | **.900** |
| C | 5 | 5 | 5 | 3 | 3 | 5 | 26 | 26 | **26** | **.867** |
| D | 5 | 5 | 5 | 4 | 5 | 5 | 30 | 29 | **29** | **.967** |
| E | 5 | 3 | 5 | 3 | 3 | 5 | 27 | 25 | **24** | **.800** |

Raw dimension scores (P1 / P2): A 5,3,5,5,5,5 / 5,3,5,5,5,5. B 5,3,5,5,4,4 / 5,4,5,5,5,5. C 5,4,4,3,5,5 / 5,5,5,3,3,5. D 5,5,5,5,5,5 / 5,5,5,4,5,5. E 5,3,4,5,5,5 / 5,4,5,3,3,5 (order Compl, Corr, Struct, Clar, Risk, Edge).

### Final NOT MET ledger (every slot not listed is MET in both passes, evidence in the pass files)

| Variant | Slot | Evidence for NOT MET |
|---|---|---|
| A | K2 | Sec 7 row `pending` (lease expired, no reply): no marker goes to `failed` (`lost_reply`), after which a fresh launch is allowed; NFR-004 promises at most one fresh launch per lease window |
| A | K4 | OD-5 `off` Project mode widens the Sec 3 "In a Project" definition |
| B | K2 | Sec 7.3 row 135: `launched` or `failed`, lease expired, no marker, attempts left: "new launch, attempts + 1" (X-001) |
| B | K4 | FR-022 `--label-only` drops two Sec 3 definitions; NFR-010 "loads as empty" vs NFR-005 |
| B | E3 | No bot or actor-type exclusion anywhere in the approval rule (no "bot" text in the file); allow-list only |
| C | L1 | NFR-004 "bounded retries afterward" states no bound |
| C | L2 | FR-010 gives only `path:<absolute-path>`; no discovery command; no option or config keys |
| C | R1, R2 | Sec 11 is prose: no IDs, likelihood/impact, per-risk mitigation |
| D | L4 | "GWT" is used from the first FR (line 44) and "SLO" in the header lens (line 5); neither is expanded |
| E | K2 | FR-014 `--agent <agent>`; no default `claude` stated (X-008) |
| E | K4 | FR-010 moves a marker-only issue to `claimed`, FR-017 requires assignee and marker; NFR-013 prunes `abandoned` vs Sec 7 `reset`-only exit; Sec 2 "every `gh` call names --repo" vs FR-001 `gh api user` |
| E | L1 | FR-012: "the record is deleted or marked `abandoned`" leaves the outcome open |
| E | L4 | "AC" is used in every FR and never expanded |
| E | R1, R2 | Sec 11 bullets: no likelihood/impact; mitigations missing (P1 names R-2, R-3, R-7; P2 names R-6, R-7) |

### Disagreement log

A disagreement is a slot where the two passes, mapped as above, gave different verdicts (a pass that raised no flag on a slot counts as MET). Passes agreed on every other slot, including all of Completeness, Structure and Edge for A, C, D, E, and on A K4, B K4, C R1/R2/L2, E K4, E R1/R2.

| Criterion | Variant | Pass 1 | Pass 2 | Final | Reason |
|---|---|---|---|---|---|
| K1 no factual errors | A | MET | NOT MET | MET | P2 said `make verify-deps` is not a documented target. The checkout Makefile defines it (3 hits), so NFR-011's check is real. P2 finding refuted. |
| K2 constraints respected (at-most-once) | A | NOT MET | MET | NOT MET | P2 folded the lost-reply path into K4. It is a separate defect: Sec 7 allows a fresh launch after a pending entry with no stored reply, and NFR-004 forbids that. |
| K2 constraints respected (at-most-once) | B | NOT MET | MET | NOT MET | P2 gave no flag. Sec 7.3 row 135 relaunches from `launched` or `failed` with no marker once the lease expires (X-001, D led 4/5). |
| R4 external-dependency failure | B | NOT MET | MET | MET | B names rate limits as R9 (Low/Low), mitigated by the 5-minute cadence and the NFR-007 call cap. That is consideration with a mitigation, which is what R4 asks. Missing 403/429 detection is carried to the incorporate list. |
| E3 guard gaps | B | NOT MET | MET | NOT MET | P2 E3 cited only the bool/float/huge-int guard. The approval rule has no actor-type check, while A, C, D, E all exclude bots. |
| L1 unambiguous | C | MET | NOT MET | NOT MET | NFR-004 requires "bounded retries" and gives no number, in a variant that otherwise defers its values. |
| L4 terms defined | D | MET | NOT MET | NOT MET | "GWT" (line 44) and "SLO" (line 5) are never expanded. Minor, one-line fix. |
| K2 constraints respected (argv) | E | NOT MET | MET | NOT MET | P2 logged the `<agent>` issue under K4 only. The seed fixes `--agent claude`; E states a placeholder with no default. K4 is scored separately for the other contradictions. |
| L1 unambiguous | E | MET | NOT MET | NOT MET | FR-012 leaves "deleted or marked `abandoned`" open, so two tests could disagree. |
| L4 terms defined | E | MET | NOT MET | NOT MET | "AC" is used on every FR and not defined (no definition found by search). |

- disagreements_found = 10
- verdicts_changed = 5 (Final differs from Pass 1: B R4, C L1, D L4, E L1, E L4). Final also differs from Pass 2 in 5 rows (A K1, A K2, B K2, B E3, E K2), so every disagreement sided with exactly one pass.
- Disagreements re-evaluated: 10. Variant text opened for: A (Makefile, Sec 7), B (Sec 7.3, R9, bot search), C (NFR-004), D (lines 5, 44), E (FR-010, FR-012, FR-014, FR-017, AC search).

### Edge-case floor check (floor 1/5 on E1-E5)

| Variant | A | B | C | D | E |
|---|---|---|---|---|---|
| Edge score | 5/5 | 4/5 | 5/5 | 5/5 | 5/5 |
| Eligible as base | yes | yes | yes | yes | yes |

## Position-Bias Mitigation

P1 evaluated in order A, B, C, D, E; P2 in order E, D, C, B, A. The per-slot comparison is the disagreement log above.

| Variant | P1 order | P2 order | P1 /30 | P2 /30 | Delta (P2 - P1) | Final /30 |
|---|---|---|---|---|---|---|
| A | 1st | 5th | 28 | 28 | 0 | 28 |
| B | 2nd | 4th | 26 | 29 | +3 | 27 |
| C | 3rd | 3rd | 26 | 26 | 0 | 26 |
| D | 4th | 2nd | 30 | 29 | -1 | 29 |
| E | 5th | 1st | 27 | 25 | -2 | 24 |

- Slot comparisons: 150 (6 dimensions x 5 slots x 5 variants after mapping). Agreement on 140; 10 disagreements (6.7%), listed above.
- No order pattern. A first-position advantage would lift P1's first variant (A: 0) and P2's first variant (E: -2, a drop); neither happened. The largest swing is B (+3), which sits mid-order in both passes.
- The swings come from the rubric difference and from flags one pass raised and the other did not: P1 caught B's relaunch row and missing bot guard; P2 caught the undefined acronyms in D and E and C's unbounded retries. D is first on qual-plus-quant under P1 only, P2 only and the merge; the places behind D differ (P1: A, E; P2: B, A; merge: A, B).
- Both passes were run independently and neither saw the other's verdicts, which holds the bias risk down.
- Round 3 (`round3-tally.md`): 19 of 21 findings ADDRESSED, INV-010 left as residual risk. None changes a score here; they feed the refactor.

## Combined Scoring

final = 0.5 x quant + 0.5 x qual

| Variant | Quant (x0.50) | Qual (x0.50) | **Final** | Rank | Debate tiebreaker (agreed leads) |
|---|---|---|---|---|---|
| D | .497 (.9949) | .483 (29/30) | **.981** | 1 | 4 of 9 = 44% |
| A | .491 (.9826) | .467 (28/30) | **.958** | 2 | 1 of 9 = 11% |
| B | .492 (.9838) | .450 (27/30) | **.942** | 3 | 1 of 9 = 11% |
| C | .473 (.9455) | .433 (26/30) | **.906** | 4 | 2 of 9 = 22% |
| E | .492 (.9845) | .400 (24/30) | **.892** | 5 | 1 of 9 = 11% |

Margins: D to A = .023 (2.3 points of the 0-1 scale), D to B = .039. Both are below the 5% threshold, so the tiebreaker applies. D to C = .075 and D to E = .089 are above it.

### Tiebreaker

Level 1, debate performance. Counted from `rounds/round2-tally.md`: points whose status is AGREED and whose leading letter is a single variant (H and N excluded).

| Variant | Points | Count |
|---|---|---|
| D | C-017, C-018, X-001, X-002 | 4 |
| C | C-011, X-004 | 2 |
| A | C-021 | 1 |
| B | S-007 | 1 |
| E | C-003 | 1 |

Total 9. D leads A by 3 points (33 percentage points of share), well past 5%, so level 1 decides: **D**. Level 2 (correctness count: D 5/5, A 3/5, B 3/5) would give the same answer and is not needed. Two further D leads, X-003 and X-005, are OPEN (3/5, not agreed) and are not counted; counting them would make D 6 of 11.

Sensitivity: D ranks first in P1 alone (.995 vs A .958), P2 alone (.983 vs B .974) and the merge (.981 vs A .958). The result does not depend on the tiebreaker.

## Selected Base: Variant D

### Selection Rationale

- Highest combined score: .981 against A .958, B .942, C .906, E .892. D is first under P1 alone, P2 alone and the merge.
- Highest quant (.995) and highest qual (29/30). It has one miss in 30 slots (undefined "GWT" and "SLO"); the nearest rivals have two (A) or three (B).
- Only variant, with C, that has zero internal contradictions (IC 1.000 in both passes), and the only one that also gives the exact launch argv (12 elements, `--agent claude`), the exact discovery argv, a lost-reply path that never relaunches, and a risk table with likelihood/impact and mitigation.
- Won the most agreed debate points (4 of 9: C-017, C-018, X-001, X-002), and led the open X-003 and X-005. The contested design choices (no relaunch after an ambiguous outcome, no `--label-only` degraded mode) went D's way.
- Its one clarity miss is a one-line fix and does not touch any requirement.

### Strengths to Preserve from Base

1. Operator runbook kept in the design doc (D Sec 1, Sec 8), apart from the requirements.
2. `attempts` / `launches` counters with `launches < max_launches` (D Sec 7): at-most-once launch even when attempts are retried.
3. `pending_orphan` and `unknown_expired` resolve to `abandoned`, never to a fresh launch; `--retry-launch <id>` is the only recovery from `unknown` (D Sec 7, FR-015).
4. Kill switch file and disabled-by-default activation, one workspace per login (D OD-2, OD-7, T7, FR-018).
5. Exit-code table with an operator action per code (D Sec 8).
6. Exact discovery argv with no `title`/`body`/`comments` field (D FR-003) and the exact 12-element launch argv (D FR-013).
7. Fail closed at exactly 100 items (exit 4) and on a corrupt record (D FR-004, NFR-011).
8. GWT acceptance line on every FR, with stub-`gh`/`orca` tests T1-T12 (D Sec 4, Sec 8).
9. Risk table R1-R9 with "Likelihood / impact" and "Mitigation" columns (D Sec 11).
10. Audit line and SLO signals (D NFR-006, NFR-013), `fcntl.flock` cycle lock (FR-017), pre-launch re-read (FR-011).
11. Approval rule with `actor.type == User` and the approver-labeled / outsider-unlabeled / outsider-labeled sequence (D Sec 3 Approved (d), FR-006).

### Strengths to Incorporate from Non-Base Variants

Each item names source variant and section, then the target place in D. None of them removes a D strength.

| # | Source | Strength | Target in D |
|---|---|---|---|
| 1 | C Sec 3 | Identity anchored on account ID, with login kept for display; Projects v2 item tied to the issue node ID, so a rename or login reuse cannot change who approved | D Sec 3 definitions of Own login, Approved, In a Project; add `approver_id` to the Sec 7 record fields |
| 2 | C Sec 3 | One-sentence rationale that the watcher "deliberately selects a stricter subset than the existing claim command" | D Sec 3, opening paragraph |
| 3 | C Sec 2 | Scoring table for the rejected alternatives B and C, with their revisit conditions | D Sec 2, after the decision list (replaces prose) |
| 4 | E FR-008, Sec 5 | Per-issue GraphQL read of `projectItems` and `Status`, replacing the whole-Project `item-list` read; removes the 100-item Project ceiling | D Sec 4 Project/Backlog FR (FR-007); update its GWT, T-tests and Sec 6 data-minimization row; keep exit 3 on scope error |
| 5 | E FR-018, NFR-012 | Daily launch cap (`max_launches_per_day` 6 [PROPOSAL]) and the worst-case spend statement | D Sec 4 caps FR (FR-016); new NFR in Sec 5; OD in Sec 10 |
| 6 | C NFR-004 | Persist the next-permitted-request time after a rate-limit reply; no GitHub call before it (fake-clock test) | D rate-limit NFR (NFR-9); store the time in the Sec 7 record file |
| 7 | A Sec 8, E Sec 8 | `check-config` verb: validates config, tools, scopes and paths with no launch | D Sec 8 verb list, exit-code table (new row), GWT test |
| 8 | A NFR-011, Sec 8 | Typed stage protocols; `cycle.py` imports only protocols and public functions; import test | D Sec 5 maintainability NFR; D Sec 8 module table |
| 9 | A OD-9 | JSON config file at a fixed path, chosen for Python 3.10 | D Sec 10 OD (config format); D Sec 8 `once --config` option |
| 10 | E FR-023, A F-5 | `reset <N>` (A calls it `release <N>`) as the only exit from `abandoned`, shown in `status` | D Sec 8 verbs and Sec 7 transition table; resolves the E pruning contradiction by keeping pruning out |
| 11 | B FR-014, T7 | Pre-launch probe: try `orca-ide` then `orca`, accept only the `orca-cli` binary (`orca` can be the GNOME screen reader); else `E-ORCA-NOT-FOUND`, zero launches | D Sec 4 launch FR (FR-013) as a precondition; D Sec 6 new threat row; Sec 8 stub test |
| 12 | B FR-002 | `origin` remote must be `IronbellyOrg/IronClaude` before any `gh` call; otherwise exit 3 | D Sec 4 FR-001 / FR-002 precondition |
| 13 | B Sec 1.1 | Root-cause table (why the existing flow cannot do this unattended) | D Sec 1, after the purpose paragraph |
| 14 | B OD-6 | Re-approval event is reported but does not reset `attempts` | D Sec 10 OD; D Sec 7 note under transitions |
| 15 | B Sec 8.3 | `_assumed_shape` fixtures: JSON shapes not yet seen live are marked as assumed in the fixture name | D Sec 8 tests paragraph; ties to the live-test follow-up FU-1 |

### Corrections to the base (not incorporations)

- C1. Expand "GWT" (Given/When/Then) and "SLO" (service-level objective) at first use in D's header lens and Sec 4 (L4 miss).
- C2. When item 4 lands, drop the `gh project item-list` wording from D's runbook R2 pre-flight and keep only the `read:project` refresh.

### Not taken, with reason

| Item | Source | Reason |
|---|---|---|
| `--label-only` degraded mode (FR-022) | B | Drops two Sec 3 definitions; X-005 went to D |
| OD-5 `off` Project mode | A | Widens eligibility; contradicts Sec 3 |
| Fresh launch after `failed` or `lost_reply` | A, B | Violates at-most-once; X-001 went to D |
| `--agent <agent>` | E | Seed fixes `claude`; X-008 |
| Prose risk section | C, E | No likelihood/impact; D's table is better |
| Rate limits "not handled specially" (R9) | B | D, A, C, E all stop on 403/429; keep D's NFR-9 plus item 6 |

