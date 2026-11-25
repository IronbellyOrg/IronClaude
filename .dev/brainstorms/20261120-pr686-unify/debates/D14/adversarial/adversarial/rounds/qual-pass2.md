# D14 scoring, pass 2 (reverse order: V2 CLAY first, then V1 OURS)

All numbers are evaluator estimates. pass-1 file not opened. Folder: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/adversarial/adversarial/`. Variants = the two opening papers only (`variant-2-original.md`, `variant-1-original.md`). "Dnn" = `debates/Dnn/VERDICT.md`.

## Summary

| Variant | quant | qual (MET/30) | combined |
|---|---|---|---|
| V2 CLAY | 0.813 | 15/30 = 0.500 | 0.656 |
| V1 OURS | 0.890 | 22/30 = 0.733 | 0.812 |

Higher: V1 (OURS). Margin 0.156 (15.6 points). Tiebreak (within 5 percent) NOT needed. Edge-case floor: V2 has 2/5, V1 has 5/5, both eligible as base.

## A. Quantitative (V2 first)

Requirement coverage per R (1 = named with disposition or action, 0.5 = partial, 0 = absent):

| R | Item | V2 | V1 |
|---|---|---|---|
| R1 | PR 686 | 1 (merge, fix forward) | 1 (split, close after re-file) |
| R2 | PR 690 | 1 (merge after 686) | 1 (keep, "named adaptations", not named) |
| R3 | issues 687, 689 | 0 | 0 (listed in the header only; claim never dispositions them) |
| R4 | PR 681 | 1 (done; single base; amend after) | 1 (keep, stamp "contested", amend) |
| R5 | PR 682 | 1 (do not revert) | 1 (revert first) |
| R6 | PRs 683, 684 | 0.5 (684 "done"; 683 only as a dependency in fact 8) | 1 (keep both) |
| R7 | issue 655 | 1 (tracking issue) | 1 (rescope) |
| R8 | issue 450 | 1 (close into 655) | 1 (keep open) |
| R9 | order | 1 (681, 682, 684, 686, 690) | 0.5 (only step 1 is ordered; rest is a list) |
| R10 | conditions first | 0 | 0.5 (INV-001 precondition, owner chat, unverified revert tree; no list) |
| R11 | flagged PRs 682, 681, 686 | 1 | 1 |
| R12 | recommendation only | 0 (imperative "Merge it") | 1 (line 45: none made until owner says it in chat) |
| | RC | 8.5/12 = 0.708 | 10/12 = 0.833 |

| Metric (method) | V2 | V1 |
|---|---|---|
| IC = 1 - contradictions/claims | 23/26 = 0.885 (3 found, below) | 35/36 = 0.972 (1 soft tension, below) |
| SR = concrete/(concrete+vague), per sentence or bullet | 34/48 = 0.708 | 52/64 = 0.813 |
| DC = resolved refs/internal refs (D-verdict item, inventory section, FULL-REPORT) | 18/22 = 0.818 | 20/24 = 0.833 |
| SC = H2 count / max H2 (6 each) | 6/6 = 1.00 | 6/6 = 1.00 |
| quant = RC*.30+IC*.25+SR*.15+DC*.15+SC*.15 | 0.2125+0.2212+0.1063+0.1227+0.15 = 0.813 | 0.25+0.2431+0.1219+0.125+0.15 = 0.890 |

DC notes: all D-verdict item refs checked and resolve (D03 recommendation item 3 and Confidence, D08 action 8, D10 items 8/10/11, D07 Strongest OURS 2, D09 item 6, D12, D13 Implications, clay-prs.md 2A, 4, 5C). `FULL-REPORT.md` exists nowhere in the brainstorm folder (find returned none), so it is unresolved in both (V2 4 refs, V1 2 refs); V1 also leaves owner requirement ids R17, R19, R22, R35, R36 undefined in the paper.

Contradictions, V2 (3): (a) Mechanism "nothing is lost... code ends up on master anyway" vs Costs "follow-up PRs must reverse parts of PR 686 (re-add approval and trigger code)"; (b) fact 4 uses D03's 50 percent (valid only "if D01 rules assignment-only", D03 line 73) while fact 7 says the verdicts adopt D01, which rules the gate stays; (c) claim order "681, 682, 684, 686, 690" vs Mechanism order "D, A, C, P" (C missing, 684 absent from the design order). V1 (1 soft): header lists "issues 687 and 689" but the claim's part (4) says "PRs 683, 684, 690" and never mentions them; counted as a gap under R3, not a contradiction. I counted the "revert first, then split" ordering tension as 1 soft item.

## B. Qualitative: V2 (CLAY), 15/30

| # | Criterion | Claim / Evidence | Verdict |
|---|---|---|---|
| C1 | All explicit requirements | R3, R10, R12 absent, 683 silent | NOT MET |
| C2 | Edge cases, failures | Risks lines 44-47: revert + 686 breaks `superclaude --help` (INV-001), M1/M2 ship | MET |
| C3 | Dependencies, prerequisites | fact 8 (683 points to `/sc:issue --plan`, lands only in 690); line 14 cron, live test, shadow run | MET |
| C4 | Success criteria | none stated | NOT MET |
| C5 | Out of scope | none stated | NOT MET |
| K1 | No factual errors (3 spot-checks) | D12 KEEP-ADAPT four fixes: true; D13 683 dangling ref: true; "verdicts adopt Clay's pieces in all thirteen topics... code ends up on master anyway" contradicts D03 (revert) and D01 (gate stays) | NOT MET |
| K2 | Feasible | merging 686 first breaks the CLI; D03 line 17 makes "686 must not merge ahead of the D03 decision" a mandatory precondition | NOT MET |
| K3 | Terminology consistent | "the poll", `enabled: false` defined line 5, used consistently | MET |
| K4 | No internal contradictions | (a), (b), (c) above | NOT MET |
| K5 | Claims supported | "adaptation is cheaper after landing" has no source; `enabled: false` as brake is one config default (D03 item 7b) | NOT MET |
| S1 | Logical order | Claim, Mechanism, Facts, Gets right, Costs, Risks | MET |
| S2 | Consistent hierarchy | six flat H2, numbered facts | MET |
| S3 | Separation of concerns | gets right / costs / risks split | MET |
| S4 | Navigation aids | numbered facts with "Source:" tags, notation line 5 | MET |
| S5 | Position paper convention | claim, mechanism, evidence, steelman of own cost | MET |
| L1 | Unambiguous | "small follow-up PR", "cheaper", "adaptation" never specified | NOT MET |
| L2 | Concrete | fact 1: head 8e5ae29ad, 12 rounds, 27/24/64 comments; fact 4: 4,599 lines | MET |
| L3 | One purpose per section | yes | MET |
| L4 | Terms defined first use | line 5 defines Dnn, "the poll", `enabled: false` | MET |
| L5 | Actionable next steps | explicit merge order in Claim | MET |
| R1 | 3+ risks with probability/impact | four risks, no probabilities | NOT MET |
| R2 | Mitigation each | none | NOT MET |
| R3 | Failure modes and recovery | revert "closed off"; no recovery | NOT MET |
| R4 | External dependencies | line 14 owner cron/live test/shadow run (450); line 46 unprotected master, no owner review | MET |
| R5 | Validation mechanism | CI green is evidence, no gate or test proposed | NOT MET |
| E1 | Collection boundaries | planb "225 entries, six shared files" given with no boundary or check (line 40, UNVERIFIED) | NOT MET |
| E2 | State across components | line 47 M1/M2 in the wake transport (named, not explained) | MET |
| E3 | Guard condition gaps | leans on `enabled: false`; never examines its gap (X-003) | NOT MET |
| E4 | Count/off-by-one | none | NOT MET |
| E5 | Interaction effects | line 44 revert x 686 breaks `--help` (D03 INV-001) | MET |

Tally V2: Completeness 2, Correctness 1, Structure 5, Clarity 4, Risk 1, Edge 2 = 15.

## B. Qualitative: V1 (OURS), 22/30

| # | Criterion | Claim / Evidence | Verdict |
|---|---|---|---|
| C1 | All explicit requirements | 687/689 undispositioned, order only partly given | NOT MET |
| C2 | Edge cases, failures | Risks lines 43-46: revert tree unverified (D03 Unverified), contributor read as rejected, D02 at 62 percent | MET |
| C3 | Dependencies, prerequisites | fact 1 (revert x 686 order), fact 5 (planb, 13-file patch applies only on revert tree), Mechanism line 15 | MET |
| C4 | Success criteria | no gates or tests named ("named adaptations" unnamed) | NOT MET |
| C5 | Out of scope | none stated | NOT MET |
| K1 | No factual errors (3 spot-checks) | D03 item 3 INV-001, 29 modules: verified (D03 line 17); D08 action 8 "Must land before any merge": verified; D10 M1 `cycle.py:777-810`, M2 `:994`, `route.py:407-413`: verified; D07 R17 and missing `/home/coder/workspaces/IronOrchestrator`: verified | MET |
| K2 | Feasible | opening "split, keep additive parts, close after re-filing": R2 import check shows 10 of 13 `predicates` names absent on master, no verdict says CLOSE | NOT MET |
| K3 | Terminology consistent | "the gate", "Planb" defined line 5 | MET |
| K4 | No internal contradictions | none hard found | MET |
| K5 | Claims supported | each of 9 facts carries a source (D-item, file:line, gh output) | MET |
| S1 | Logical order | same six-section order | MET |
| S2 | Consistent hierarchy | six flat H2 | MET |
| S3 | Separation of concerns | yes | MET |
| S4 | Navigation aids | numbered facts, "Source:" tags | MET |
| S5 | Position paper convention | yes | MET |
| L1 | Unambiguous | "named adaptations", "additive, read-only and rule-compatible parts" undefined | NOT MET |
| L2 | Concrete | fact 2 per-file +/- counts, fact 3 timestamps 22:56Z, 00:02Z, 66 minutes | MET |
| L3 | One purpose per section | yes | MET |
| L4 | Terms defined first use | line 5 | MET |
| L5 | Actionable next steps | Claim (1) to (5): revert PR 682 first as a new PR, split 686, stamp 681 | MET |
| R1 | 3+ risks with probability/impact | line 46 verdict confidence 62 to 85 percent, line 43 unverified revert tree, line 44 contributor read, costs lines 37-39 give impact | MET |
| R2 | Mitigation each | only "credit Clay and keep the branch" (1 of 4) | NOT MET |
| R3 | Failure modes and recovery | no recovery for an unverified revert | NOT MET |
| R4 | External dependencies | line 45 owner chat decisions; planb unpushed; CHANGELOG conflict | MET |
| R5 | Validation mechanism | none (fact 5 `git apply --check` is evidence only) | NOT MET |
| E1 | Collection boundaries | fact 2: 14 `predicates.py` and about 30 `github.py` symbols D01 says survive; 29 failing modules | MET |
| E2 | State across components | fact 6 M1 ack before state file `cycle.py:777-810`, M2 `wrong_target` | MET |
| E3 | Guard condition gaps | fact 8 plan check passes unfilled template, `hold.py:69-70, :140`; fact 9 ADD1 contradicts WORKER-CONTRACT 239-246 | MET |
| E4 | Count/off-by-one | fact 5 reconciles planb 223 then vs 225 now | MET |
| E5 | Interaction effects | fact 1 revert x 686; fact 5 planb x 686 | MET |

Tally V1: Completeness 2, Correctness 4, Structure 5, Clarity 4, Risk 2, Edge 5 = 22.

## C. Debate-performance count (21 diff points, final round-2 rebuttals)

Both rebuttals converged: revert PR 682 behind Q1; adapt PR 686 in place as a draft (not merge as is, not split, not close); two lanes; planb first; `enabled` absent means off pinned as a test.

| Point | Winner | Basis |
|---|---|---|
| S-001 | HYBRID | identical section sets |
| S-002 | OURS | CLAY adopts the per-item table with conditions |
| S-003 | OURS | CLAY: "Issues 687, 689, 655, 450: as OURS section 4" |
| S-004 | OURS | CLAY adopts condition-first table, adds mechanical checks |
| C-001 | HYBRID | not merged as is (OURS), adapt in place keeping review history (CLAY) |
| C-002 | OURS | revert accepted by CLAY |
| C-003 | HYBRID | revert-before-686 (OURS), 690 independent lane (CLAY) |
| C-004 | OURS | stamp or banner now, amend later |
| C-005 | HYBRID | named adaptations (OURS), not queued behind 686 (CLAY) |
| C-006 | OURS | 450 open, 655 rescoped |
| C-007 | OURS | brake is thin, revert x 686 breaks CLI |
| C-008 | HYBRID | review history kept via adapt in place |
| C-009 | HYBRID | revert accepted; CLAY corrects the 225 to 22 files, 7 source |
| X-001 | OURS | 686 not first; precondition |
| X-002 | OURS | gate stays (D01), Q1 |
| X-003 | OURS | CLAY concedes `enabled: false` is thin |
| X-004 | OURS | banner states "no owner approval recorded on GitHub" |
| A-001 | HYBRID | dry run in clean git checkout (both), INV-009 artifact explained by CLAY |
| A-002 | HYBRID | Q2 who adapts left to the owner |
| A-003 | OURS | CLAY concedes |
| A-006 | OURS | owner approvals in chat, recorded by agent |

Count: OURS 13, CLAY 0, HYBRID 8. Not needed for the result since the margin exceeds 5 percent; the tiebreak order would have gone to V1 (debate points) anyway.

## D. Notes

- V2's weakest points on the opening paper: it proposes merging 686 ahead of the D03 mandatory precondition and omits R3, R10, R12. V1's weakest: the "split and close" mechanism has no verdict behind it and 687/689 are never dispositioned.
- Diff-analysis S-003 says V1 "names all nine items in the claim"; the claim actually omits 687 and 689 (header only), so I scored R3 as 0 for both.
