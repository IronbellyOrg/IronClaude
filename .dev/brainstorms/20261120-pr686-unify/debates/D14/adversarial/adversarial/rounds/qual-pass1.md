# D14 qual-pass1: Step 3 hybrid scoring, input order V1 (OURS) then V2 (CLAY)

All numbers are evaluator estimates. Papers judged as the opening position papers. Read-only evaluation.
Spot-check sources: debates/D01, D03, D07, D08, D09, D10 VERDICT.md; inventory/clay-prs.md; /home/coder/workspaces/IronClaude/.dev/analyze/pr686-20261120/FULL-REPORT.md.

## Result

| | V1 OURS | V2 CLAY |
|---|---|---|
| quant | 0.919 | 0.824 |
| qual (MET/30) | 22/30 = 0.733 | 15/30 = 0.500 |
| combined | **0.826** | 0.662 |

Higher: **V1 (OURS)**. Margin 0.164 (16.4 points). Tiebreak (within 5 percent) NOT needed. Debate points won (section D): OURS 12, CLAY 0, HYBRID 9. Edge-case floor: V1 5/5, V2 1/5; both eligible as base.

## A. Quantitative

Methods: RC = requirements R1..R12 that the paper names with a disposition or action / 12. IC = 1 - contradictions / claims (about 28 claims each; a contradiction is two statements in the same paper that cannot both hold). SR = concrete statements (number, date, file:line, PR number, command) / (concrete + vague); counted by reading each sentence, V1 about 55 vs 8, V2 about 46 vs 10. DC = internal references (Dnn verdicts, inventory, FULL-REPORT, defined terms) that resolve to an existing file or defined term / all. SC = H2 count / 6.

| Req | V1 | V2 |
|---|---|---|
| R1 PR 686 | Y split, close after re-file (Claim 2) | Y merge as is, fix forward (Claim) |
| R2 PR 690 | Y keep with named adaptations (Claim 4; names not given) | Y merge after 686 as is (Claim, fact 8) |
| R3 687/689 | N (named in the header only, no disposition) | N (silent) |
| R4 PR 681 | Y keep, stamp "contested", amend (Claim 3) | Y keep as base, amend after (Claim, costs) |
| R5 PR 682 | Y revert first, new PR (Claim 1) | Y do not revert (Claim) |
| R6 683/684 | Y keep 683, 684, 690 (Claim 4) | N (683 only as a dependency in fact 8; 684 only "done") |
| R7 issue 655 | Y rescope (Claim 5) | Y keep as tracking issue (Claim) |
| R8 issue 450 | Y keep open (Claim 5) | Y close into 655 (Claim) |
| R9 order | Y revert first, then split, amend, rest (Claim, "order matters") | Y 681, 682, 684, 686, 690 (Claim) |
| R10 conditions | N (no list; only fact 1 ordering break and the unverified revert tree) | N (only "cron, live test, shadow run before anything runs", not per step) |
| R11 NEEDS-DEBATE PRs 682/681/686 | Y all three dispositioned | Y all three dispositioned |
| R12 recommendation only | Y (Risks: "recommendations; none is made until the owner gives them in chat") | N (imperative; no statement) |
| RC | 10/12 = 0.833 | 8/12 = 0.667 |

| Metric | V1 | V2 |
|---|---|---|
| IC | 0 contradictions: 1.000 | 3: (a) Claim "nothing is lost by landing" vs Costs "follow-ups must reverse parts of 686 (re-add approval and trigger code)"; (b) Mechanism "changes no live behaviour" vs Risks "orchestrator wire names and registry shape become public on master"; (c) fact 4 relies on D03's 50 percent that holds only "if the gate is dropped", while fact 7 says the verdicts adopt controls that keep it. IC = 1 - 3/28 = 0.893 |
| SR | 0.873 | 0.821 |
| DC | about 0.92 (D01 to D13, inventory 2A, FULL-REPORT resolve; R19/R22/R35/R36, ADD1, OQ5 point outside the paper) | about 0.85 (same, plus "D:978-1030", K11/K14/K16, L-1, Q36, "PR D/A/C/P" used without a notation or mapping) |
| SC | 6/6 = 1.00 | 6/6 = 1.00 |
| **quant** | .833*.30 + 1.0*.25 + .873*.15 + .92*.15 + .15 = **0.919** | .667*.30 + .893*.25 + .821*.15 + .85*.15 + .15 = **0.824** |

## B. Qualitative (claim | evidence | verdict)

### V1

| # | Criterion | Evidence | V |
|---|---|---|---|
| C1 | All explicit requirements | 687/689 and conditions (R3, R10) have no disposition | N |
| C2 | Edge cases, failures | fact 1 (revert plus 686 crashes `--help`, 29 modules); Risks (revert tree unverified; closing read as rejection) | M |
| C3 | Dependencies, prerequisites | fact 1 order break; fact 5 planb patch applies only to the revert tree | M |
| C4 | Success criteria | no pass check or definition of done anywhere | N |
| C5 | Out of scope | none stated | N |
| K1 | No factual errors | spot-checks match: D03 item 3 (29 modules, INV-001); D09 `hold.py:69-70` (HTML comments only); D07 `/home/coder/workspaces/IronOrchestrator` absent; D10 M1 `cycle.py:777-810` | M |
| K2 | Feasible | split of 686 is infeasible per its own later evidence (10 of 13 `predicates` names absent on master), and no verdict says CLOSE | N |
| K3 | Terminology consistent | "gate", "Planb", "coordinator" defined and held | M |
| K4 | No contradictions | none found | M |
| K5 | Claims supported | each of 9 facts carries a Source line | M |
| S1 | Logical order | Claim, Mechanism, Cited facts, Gets right, Costs, Risks | M |
| S2 | Consistent hierarchy | six H2, numbered lists | M |
| S3 | Separation of concerns | gets right / costs / risks split | M |
| S4 | Navigation aids | numbered facts with Source lines; 47 lines | M |
| S5 | Position-paper convention | claim, evidence, concessions, costs, risks | M |
| L1 | Unambiguous | "keep 683, 684, 690 with named adaptations" names none; "little is blocked" | N |
| L2 | Concrete | 66 minutes, 4,599-line revert, 14 and about 30 symbols | M |
| L3 | One purpose per section | each section single-purpose | M |
| L4 | Terms defined at first use | "the gate" and "Planb" defined in the preamble | M |
| L5 | Actionable next steps | Claim 1: revert PR 682 first as a new PR; stamp 681 | M |
| R1 | 3+ risks with probability/impact | four risks, only D02 "62 percent" quantified | N |
| R2 | Mitigation for each | only "split must credit Clay and keep the branch" | N |
| R3 | Failure modes and recovery | fact 1 failure plus "do not merge 686 as it stands" | M |
| R4 | External dependencies | owner chat decisions; Clay's branch; unpushed planb | M |
| R5 | Validation mechanism | revert tree "not verified"; no check defined | N |
| I1 | Collection boundaries | fact 2: 14 symbols in `predicates.py`, about 30 in `github.py` that must survive | M |
| I2 | State across components | fact 6: ack before state file loses the issue (M1), `wrong_target` (M2) | M |
| I3 | Guard condition gaps | fact 8: only HTML comments stripped, unfilled template passes | M |
| I4 | Count/off-by-one | fact 5: 223 vs 225 entries reconciled | M |
| I5 | Interaction effects | fact 1 revert x 686 interaction; planb patch vs revert tree | M |

V1 by dimension: Completeness 2, Correctness 4, Structure 5, Clarity 4, Risk 2, Invariant 5 = **22/30**.

### V2

| # | Criterion | Evidence | V |
|---|---|---|---|
| C1 | All explicit requirements | R3, R6, R10, R12 missing | N |
| C2 | Edge cases, failures | Risks: revert closed once 686 lands; planb modify/delete conflict; M1/M2 ship | M |
| C3 | Dependencies, prerequisites | fact 8: 683 points to `/sc:issue --plan` that lands only in 690; design order | M |
| C4 | Success criteria | none | N |
| C5 | Out of scope | none | N |
| K1 | No factual errors | fact 4 uses D03's 50 percent, which D03 ties to "if D01 rules assignment-only"; D01 rules the gate stays; "nothing is lost" misstates the verdicts, which require renames "before any merge" (D08 action 8) | N |
| K2 | Feasible | merge as is breaks D03 item 3's "must not merge ahead" precondition; D08 "must land before any merge" | N |
| K3 | Terminology consistent | no term switches | M |
| K4 | No contradictions | three listed in IC | N |
| K5 | Claims supported | 9 facts with sources (inventory 4, FULL-REPORT 3, D03, D12) | M |
| S1 | Logical order | same order as V1 | M |
| S2 | Consistent hierarchy | six H2 | M |
| S3 | Separation of concerns | yes | M |
| S4 | Navigation aids | "D:978-1030", "PR D/A/C/P", K11/K14/K16 unresolved in the paper | N |
| S5 | Position-paper convention | yes | M |
| L1 | Unambiguous | "small follow-up PR", "adaptation" never specified | N |
| L2 | Concrete | 12 rounds, 27/24/64 comments, 4,599 lines | M |
| L3 | One purpose per section | yes | M |
| L4 | Terms defined at first use | "the poll", `enabled: false` defined | M |
| L5 | Actionable next steps | Claim gives a merge order | M |
| R1 | 3+ risks with probability/impact | four risks, none rated | N |
| R2 | Mitigation for each | only "follow-ups"; none per risk | N |
| R3 | Failure modes and recovery | none given for revert-closed-off or M1/M2 | N |
| R4 | External dependencies | owner cron, live test, shadow run (issue 450); planb | M |
| R5 | Validation mechanism | cron, live test and shadow run before anything runs | M |
| I1 | Collection boundaries | none | N |
| I2 | State across components | M1/M2 named without mechanism | N |
| I3 | Guard condition gaps | leans on `enabled: false` without testing it (D03 7b: ship gate R33 not built) | N |
| I4 | Count/off-by-one | none | N |
| I5 | Interaction effects | Risks: 682 revert x 686 breaks `superclaude --help` (D03 INV-001) | M |

V2 by dimension: Completeness 2, Correctness 2, Structure 4, Clarity 4, Risk 2, Invariant 1 = **15/30**.

## C. Combined

V1 = 0.5*0.919 + 0.5*0.733 = **0.826**. V2 = 0.5*0.824 + 0.5*0.500 = **0.662**. Higher: V1. Margin 0.164, outside the 5 percent band, so the tiebreak is not needed.

## D. Debate points (final round-2 rebuttals vindicate)

| Pt | Side | Basis |
|---|---|---|
| S-001 same section set | HYBRID | identical in both |
| S-002 granularity | OURS | CLAY adopts OURS's per-item table ("Issues: as OURS section 4") |
| S-003 per-item coverage | HYBRID | OURS table base; CLAY adds PR 685 and eight removal PRs |
| S-004 start conditions | OURS | CLAY conceded; both tables are condition-first |
| C-001 PR 686 | HYBRID | neither merge as is nor split: adapt in place as draft |
| C-002 PR 682 | OURS | both tables: REVERT |
| C-003 order | HYBRID | two lanes (CLAY's point), revert and planb gating (OURS) |
| C-004 PR 681 | HYBRID | keep as base (CLAY) plus stamp or banner (OURS) |
| C-005 PR 690 | OURS | rebase-and-adapt, not as is |
| C-006 issues 655/450 | OURS | 450 stays open, 655 rescoped |
| C-007 safe/unsafe to merge first | OURS | CLAY conceded `enabled: false` is a thin brake; pinned test added |
| C-008 review rounds as evidence | HYBRID | in-place adapt keeps the PR and its history, but not as grounds to merge |
| C-009 cost model | HYBRID | CLAY reprices planb overlap to 22 files (7 source); the revert cost stands |
| X-001 landing 686 closes revert | OURS | merge-condition and CI canary adopted by both |
| X-002 approval gate | OURS | Q1: both gates stay; 686 may not delete D01 names (diff check) |
| X-003 `enabled: false` | OURS | "enabled absent means off" pinned in both |
| X-004 who gave notice | OURS | banner states no owner approval on record (checked 2026-11-20) |
| A-001 revert tree builds | HYBRID | clean-checkout dry run (both) and CLAY's record.py test finding |
| A-002 who re-files | HYBRID | Q2 who adapts: Clay or a supervised session |
| A-003 `enabled: false` reliable | OURS | conceded by CLAY |
| A-006 one decider | OURS | banner and chat-only approvals |

Totals (21): OURS 12, CLAY 0, HYBRID 9.

## E. Notes for base selection

V1 gaps to fill from V2 or the rebuttals: 687/689 dispositions, pre-conditions per step, success checks, and the withdrawn split and close-original. V2 strengths worth keeping: the 683 to 690 dependency, the review-history point, the planb overlap price, and the 50 percent premise as a stated conditional.
