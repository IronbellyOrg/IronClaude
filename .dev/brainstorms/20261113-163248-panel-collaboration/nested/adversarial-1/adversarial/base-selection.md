# Base Selection Report

- Generated: 2026-11-13T18:56:52Z
- Inputs: `variant-1..5-original.md`, `debate/round3-tally.md` (converged), source requirements `../../../seed-brief.md`.
- Scripts (deterministic, re-runnable): `scoring/quant.py` (quantitative layer), `scoring/reconcile.py` (pass comparison), `scoring/final_qual.py` (final verdicts). Raw passes: `scoring/qual-pass1.md` (input order V1-V5) and `scoring/qual-pass2.md` (reverse order V5-V1), each by an independent evaluator agent that wrote none of the variants.

## Quantitative Scoring (50% weight)

Variants: V1 opus:architect, V2 opus:analyzer, V3 haiku:backend, V4 opus:devops, V5 sonnet:performance. RC = 36 brief requirements matched by regex (`scoring/quant.py` REQS); IC = 1 - (arithmetic ERRORs in the diff-analysis completeness grid, plus V3's X-006 self-contradiction) / lines with a number; SR = concrete indicators / (concrete + vague); DC = resolved internal references (section, redesign and requirement ids) / total; SC = H2 count / max H2 count. Running the script twice gave identical output.

| Variant | RC | IC | SR | DC | SC | quant | detail (errors/claims, concrete/vague, refs resolved/total) |
|---|---|---|---|---|---|---|---|
| V1 | 0.971 | 0.993 | 0.997 | 1.000 | 1.000 | 0.989 | 2/302, 395/1, 49/49 |
| V2 | 0.914 | 0.988 | 1.000 | 1.000 | 1.000 | 0.971 | 3/256, 465/0, 23/23 |
| V3 | 0.914 | 0.955 | 1.000 | 0.833 | 1.000 | 0.938 | 5/112, 195/0, 5/6 |
| V4 | 0.971 | 0.994 | 1.000 | 1.000 | 1.000 | 0.990 | 2/345, 588/0, 57/57 |
| V5 | 0.971 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 0/270, 413/0, 24/24 |

| Metric | Weight | V1 | V2 | V3 | V4 | V5 |
|---|---|---|---|---|---|---|
| requirement_coverage | 0.30 | 0.971 | 0.914 | 0.914 | 0.971 | 0.971 |
| internal_consistency | 0.25 | 0.993 | 0.988 | 0.955 | 0.994 | 1.000 |
| specificity_ratio | 0.15 | 0.997 | 1.000 | 1.000 | 1.000 | 1.000 |
| dependency_completeness | 0.15 | 1.000 | 1.000 | 0.833 | 1.000 | 1.000 |
| section_coverage | 0.15 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| **quant_score** | | **0.989** | **0.971** | **0.938** | **0.990** | **0.991** |

Reading: the quantitative layer barely separates V1, V4 and V5 (0.989-0.991); the decision is carried by the qualitative layer.

## Qualitative Scoring (50% weight) - Additive Binary Rubric

30 criteria in 6 dimensions (CP completeness, CR correctness, ST structure, CL clarity, RK risk coverage, IV invariant and edge-case coverage). Each cell is the final verdict with its Claim-Evidence-Verdict evidence (pass 1's evidence where both passes agreed; the re-evaluation reason where they disagreed). Full per-pass evidence is in the two pass files.
### CP

| Criterion | V1 | V2 | V3 | V4 | V5 |
|---|---|---|---|---|---|
| CP1 | MET: Five designs R1-R5 each with schedule/transport/time/safeguards/gain (L148-526); theories L21-92; experiment L544-601. E.g. L171 "B = 116 s per package", gain t | MET: D1-D5 each with schedule, transport, time table, safeguards, gain (L151-476); theories L7-94; experiment L494-533. L174 "348 s / 3 = 116 s per package"; gains n | MET: R1-R5 each with (a)-(h) (L71-126); theories L30-52; experiment L142-167. Time arithmetic e.g. L76 "102 + 14 + 3 + 30 = 149 s ... +28%"; gain targets named (L78  | MET: Five redesigns each (a)-(h) with tables (L188-610); theories L22-85; experiment L630-682. Gain totals add up (R1 L238-245 low 0.20/high 0.88; R3 L419-430 0.23/0 | MET: Designs 1-5 each (a)-(h) (L157-396); theories L33-54; experiment L424-469. Gain tied to issues via move-issue map L85-92 (G1-B1 ... G8-I6/I5) and per-issue tabl |
| CP2 | MET: Per-design failure modes, e.g. L227 "Weaker models skip posting cards...", L374 "Card regions are wrong when anchors are not found (46 unanchored rows)". | MET: Failure modes e.g. L210-215 "hook does not receive the board path", L286 "--resume ... UNVERIFIED: fresh-session fallback". | MET: Failure modes per design (L80, L91, L102, L113, L124). | MET: Failure/runbook tables per design with Detection and Action (L262-270, L331-339, L448-457, L527-535, L601-608). | MET: L197 "ember skips source.md"; L349 "model omits or mangles the moves: line"; L396 "If haiku finishes early (below 100 s)". |
| CP3 | MET: L608 "Preconditions (spikes; each must pass before arms A3 or A4 run)" REQ-S1..S3; harness fixes REQ-H1..H6. | MET: L498 Spike S0 gate; L539 R-1..R-6 harness prerequisites. | MET: L146 "Pre-condition (not optional)" harness fixes; reqs 2-5 (L172-175); L166 hold-out package. | MET: L640-646 Gate 0 spikes S0, S2, S3; R-01..R-05 preconditions L690-696. | MET: L428-433 five spikes; H-1..H-6 L479-484; L538-545 known unverified items. |
| CP4 | MET: L587-595 decision rule with thresholds and stop-early; REQ-E2 pre-registration (L677). | MET: L524-533 pre-registered decision rule; R-27 L579. | MET: L158-161 adopt/extend/reject rule; reqs 20-21. | MET: L664-673 pre-registered decision rule; outcomes table L677-682. | MET: L456-463 decision rule with five conditions and fallback outcomes. |
| CP5 | MET: L111 "The grading-rule problem ... is held constant in every arm ... listed as follow-up work". | MET: explicit exclusions: D3-D5 deferred (V2:496), no Opus or sonnet reviewer in the experiment | MET: explicit exclusions: R3-R5 deferred (V3:154), glm/Qwen excluded, harness fixes separate (V3:126) | MET: explicit exclusions: grok in no design (V4:610), transports rejected for every design, Redesigns 1/4/5 deferred from the experiment | MET: B-1 L490 "No cross-session messaging, Orca mail or A2A in the first experiment"; L446 designs 1 and 5 deferred. |

### CR

| Criterion | V1 | V2 | V3 | V4 | V5 |
|---|---|---|---|---|---|
| CR1 | MET: L171 348 s over 3 packages gives 116 s; L258 715 s gives 238 s; L475 821 s gives 274 s; all match the brief. | MET: L174 116 s, L310 238 s, L377 274 s, L438 "676 s / 3 = 225 s (CR:320)" all match COMBO-REPORT; L71 "ember 81/209 = 39%" matches. | MET: L69 348 s over three packages gives 116 s; legend counts (68, 52, 56 of 76) match the brief; no fabricated figures found. | MET: L156 116 s, L157 S13 100 s, L158 S07/S14 225 s, L159 238 s; L67 "luna 30, ember 33" matches CR:292; gain sums recompute correctly. | MET: L27-29 116/238/274 s and +35% caps match brief (116 x 0.35 = 40.6); L479 "77% of 665" = (665-156)/665; gain sums recompute (L191 0.21). |
| CR2 | MET: L136-138 hooks plus Stop, L179 hard finish signal; read-only board outside sandbox (REQ-H6 L625); caps within +35% (L323). | MET: Fails-closed hooks (L211), fallbacks (L245, L286), +25% to +34% bounded (L182, L255). | MET: Phase-2 caps (L76), hooks (L86), SendMessage flagged UNVERIFIED (L108). | MET: Hooks passed per reviewer with absolute paths (L124); resume with fresh-session fallback (L384); read-only kept (L137). | MET: L106 `--max-turns` not in help so turn caps via hook counter and timeout; L121 hard cap by counter. |
| CR3 | NOT MET: 'B' is both the baseline time (V1:171) and issue prefix B1-B8 (V1:17); 'T1' is both Theory 1 and a time (V1:323) | MET: M1-M9 catalogue, `panel-msg/1`, H/C/CI defined once and used consistently (L137-139). | MET: M1-M6, R1-R5 and numbered requirements used consistently. | MET: T1-T3, M1-M10, Redesign 1-5 and R-01..R-30 used consistently. | MET: G1-G8, EL2/HL2/SL2, DS/AL/DE, H/B/S/C/D requirement families used consistently. |
| CR4 | MET: the 'follow-up work in section 4' line (V1:111) is a dangling reference, not a contradiction between claims | NOT MET: V2:182 '135 s or later gets none' contradicts its own formula, which gives 0 from 128 s (diff-analysis grid) | NOT MET: R1 'complete replacement findings-v1 block' (V3:73) vs req 6 'outside the fenced block' (V3:176); diff-analysis X-006 | MET: Time tables self-consistent; L396 explicitly reconciles 45 s timeout (+39%) with the 35 s luna guard; no contradiction found (L301 typical 142 s excludes the 6  | NOT MET: V5:3 'Nothing was run for this variant' vs V5:106 'Verified in this build. claude --help lists ...' |
| CR5 | MET: Theory tables carry numbers and sources, e.g. L34-41 (0 of 176, 7 of 8, 5 of 11 with INV/CR cites). | MET: Evidence tables with sources L19-29, L41-50, L67-75. | NOT MET: V3:67 haiku 'breaks the cap' contradicts the per-baseline cap (SEED:30); gains do not follow from stated inputs (diff-analysis grid ERRORs) | MET: Evidence tables with file:line sources (L30-37, L45-53, L61-68); gain chains stated (L317-325, L417). | MET: L94 explains how c is derived (half of sonnet's judged rate, sum 1.04 vs measured reach about 1.0) and L141 flags the prompting share as judgment. |

### ST

| Criterion | V1 | V2 | V3 | V4 | V5 |
|---|---|---|---|---|---|
| ST1 | MET: Theories (L21), designs (L96), comparison (L528), experiment (L544), requirements (L604). | MET: Theories, building blocks, designs, comparison, experiment, requirements. | MET: Theories, designs, comparison, experiment, requirements. | MET: Theories, building blocks, redesigns, comparison, experiment, requirements. | MET: Theories, substrate, designs, comparison, experiment, requirements. |
| ST2 | MET: Each design has the same (a)-(h) sub-structure (L148-L524). | MET: D1-D5 each (a)-(h); gate table L83-94 maps issues to theories. | MET: R1-R5 uniform (a)-(h). | MET: Uniform (a)-(h) for each redesign. | MET: 2.0.1-2.0.6 then 2.1-2.5 uniform (a)-(h). |
| ST3 | MET: Shared scaffolding separated in 2.0 (L98-144) from per-design policy. | MET: 2.0 shared blocks L100-147 separate from designs. | MET: Shared rules L56-69 separate from designs; harness fixes L126 separate. | MET: 2.0 substrate (L91-185) separate from designs; section 5.1-5.6 grouping. | MET: Shared substrate separated from per-design sections; H/B/S/C/D/E requirement families. |
| ST4 | MET: Evidence key table L5-15, move ids M1-M10 L115, REQ ids L604-679. | MET: M1-M9 L104-114, R-1..R-28, spike S0. | MET: Legend IDs L11-26, M1-M6, requirement numbers 1-21. | MET: R-01..R-30, M1-M10, S0/S2/S3, source-key abbreviations L3-8. | MET: IDs G1-G8, H-1.., B-.., S-.., C-.., D1-1.., E-..; evidence key table L7-17. |
| ST5 | MET: L604-679 numbered REQ-xx with a Test column. | MET: R-1..R-28 each with *Test:* (L541-580). | MET: L171-191 21 numbered requirements each with "Test:". | MET: R-01..R-30 with Verification column (L690-746). | MET: L473-536 requirement tables with Test column. |

### CL

| Criterion | V1 | V2 | V3 | V4 | V5 |
|---|---|---|---|---|---|
| CL1 | MET: Message kinds fixed, "no free-text field" (L130-134); caps stated numerically. | MET: Message schema with forbidden keys (L116-131); formulas for deliveries. | NOT MET: L69 "If the 348 s figure is a per-package figure instead, every budget here is conservative" contradicts its own "348 s over three packages". | MET: "forbidden fields" list L117; numeric caps in every schedule table. | MET: L119 drop rules incl. verdict-word list; numeric caps. |
| CL2 | MET: Concrete JSON envelope L133, byte/line caps, per-turn seconds L171. | MET: L169 "400 bytes per line; rendered delivery at most 1,200 characters"; per-turn timings L178. | MET: L74 schema with example JSON; L85 enum scope values. | MET: L111 JSON schema; timing constants table L143-148. | MET: L112-118 schema; timing arithmetic with seconds per step (L179-184). |
| CL3 | MET: Each section is purposed (theories / designs / comparison / experiment / requirements). | MET: Sections have distinct purposes; each design states aim at a theory. | MET: Sections have clear purposes. | MET: Each section purposed; devops framing L12-18 lists per-design deliverables. | MET: Section purposes clear; lens stated L3. |
| CL4 | MET: L17 defines labels and "Found /14"; L141 defines J as mean pairwise Jaccard. | MET: L137 CI defined (mean pairwise Jaccard); "natural seal" defined L133; H and C defined L79, L139. | NOT MET: "DE runs" (L33) never defined; "GT10", "GT5" (L39) used while the legend defines only B/I labels. | MET: Move text, "SLO_BREACH" defined R-24 L735, ALARM names defined R-25 L736. | MET: L19-21 DS/AL/DE and "hard ten" defined; L23-29 EL2/HL2/SL2 defined; L94 "What c means". |
| CL5 | MET: L587-595 decision rule and L595 "Stop early" decision point; L681 states what was not checked. | MET: L496 chosen designs with reasons, L532 outcomes ("adopt the static catalog and stop"). | MET: L158-161 decision rule, L160 extension rule. | MET: L677-682 outcome table and abort criteria. | MET: L428 spikes first; L454 interim look; L463 outcomes for no-pass cases. |

### RK

| Criterion | V1 | V2 | V3 | V4 | V5 |
|---|---|---|---|---|---|
| RK1 | NOT MET: Failure-mode lists (L225-231, L517-524) carry no probabilities or impact ratings. | NOT MET: No risk carries probability and impact; L213 "ember ... skipped source.md in 39% of runs" is the only rate. | NOT MET: No probability and impact per risk; only qualitative contamination/reliability columns (L132-138). | NOT MET: Risks list L756-759 and runbook rows give no probability and impact. | NOT MET: probabilities exist for moves (V5:190) but no 3 risks carry probability and impact; failure modes are rated qualitatively |
| RK2 | NOT MET: R5 failure modes (L517-524) list six failures with no mitigation; R1 "Cards act as done signals" has none. | NOT MET: D3 failure modes (L345-351) and D4 (L413-418) list failures with no mitigation. | NOT MET: Failure-mode lists (L80, L91, L113, L124) name failures without mitigations. | MET: Every failure row has an Action, e.g. L335 "switch delivery to 'tool call 8 or later, no seal needed'". | NOT MET: L263, L349, L396 failure lists with no mitigation for several items (e.g. "Models forget to post", "tired reviewer"). |
| RK3 | MET: L376 "Phase 2 is killed at the cap ... fail-open, and the run still counts"; REQ-B7 L658 continue isolated. | MET: L211 "fails closed", L212 "fallback takes its sealed report", R-21/R-22 L570-571. | NOT MET: Failures such as "Ember exits before the challenge arrives" (L113) have no recovery path; only run exclusion (req 16 L186). | MET: Runbook tables (L264-270 etc.), kill switch L139 "PANEL_COLLAB=0", L384 fallback. | MET: L197 "the harness logs 'no delivery' and the run counts as isolated"; L385 15 s rule drops late phase 2. |
| RK4 | MET: L229 "Hook environment inheritance has not been verified"; L469-473 UNVERIFIED SendMessage items; L372 resume with gateway ids. | MET: L172 hooks and Stop block UNVERIFIED; L308 gateway SendMessage; L286 resume with gateway ids. | MET: L75 resume with gateway ids UNVERIFIED; L86 hook env UNVERIFIED; L108 held messages expire after 5 minutes. | MET: L124 hook env UNVERIFIED, L384 resume UNVERIFIED, L532 Stop-hook timeout, L133 SendMessage reasons. | MET: L542 hooks inheriting board path, additionalContext, Stop block, --resume untested; L543 --max-turns missing. |
| RK5 | MET: L140-144 convergence alarm, REQ-A1 L667 audit script, L273 tunnelling alarm. | MET: L137 convergence alarm, R-23 board audit, R-24 L576 alarm reproduces 0.25 on history. | MET: L88 leak check, L77 Jaccard alarm, req 12 L182. | MET: R-23 collab.json fields L734, R-25 alarms L736, R-24 SLO L735. | MET: L132 three convergence alarms; L454 interim look; C-3, C-4 L512-513. |

### IV

| Criterion | V1 | V2 | V3 | V4 | V5 |
|---|---|---|---|---|---|
| IV1 | MET: L227 no gaps leads to isolated behaviour; L374 unanchored rows skipped; caps L167 "ember 3 total, luna 2 total". | MET: R-20 tests at stop times 100, 125, 140 s giving 2, 1, 0 locators (L569); "no-record case" L109; caps L167. | MET: L91 "the board is silently empty"; caps L74, L85 (4 messages, 8 findings, 240 characters). | MET: L455 "Digest empty ... challenges = 0"; L335 seal_missing; caps per reviewer (L288, L372). | MET: L197 ember posts after luna's call 6 so no one receives it; L349 ember gets only one ticket; L228 relay-once dedupe; L330 scaling at n = 5. |
| IV2 | MET: L136 board outside every sandbox; L321 --no-session-persistence blocks --resume; L109 board per package under H3. | MET: L133 natural seal; R-11 L554 seal precedes delivery; L194 board access audit. | MET: L56 "A hook refuses to release peer content until the file exists"; req 10 L180; L80 session expiry between phases. | MET: L270 project hooks in tracked settings also fire; L457 session storage grows; L286 seal precondition. | MET: L325 `stop_hook_active` guard; L396 session storage tied to working directory; L120 independence gate. |
| IV3 | MET: L136 "every write goes through one validator"; REQ-B7 corrupt line/missing dir; L229 invalid move ids rejected. | MET: L129 forbidden keys; R-8/R-9 L551-552 quote must be a substring, path must exist. | MET: req 7 L177 reject other fields; req 8 L178 "rejected, not truncated"; req 11 L181 anchor-leak hard failure. | MET: R-06 L702 bad fixtures rejected; L456 two blocks in one report; R-02 L693 parser limits (anchor 12-200, id 16). | MET: L119 schema/size/verdict-word drop; S-1 L501 seeded bad messages dropped. |
| IV4 | MET: L138 finish at 1.20 x B plus 15% headroom; L323 "1.35 x T1 - 2 s"; L329 "+34.5% hard; expected ~150 s = +29%". | MET: L3 "divided by 3"; L182 floor formula; R-2 L542 cut to 297 characters; L255 expected +25% vs worst +29%. | NOT MET: L69 treats the 348 s total as possibly per-package; no handling of unit/rounding divergence. | MET: L396 45 s vs 35 s guard (+39% vs +30%); R-24 error budget "1 in 12", 1.5x breach; L156 cap 157 s. | MET: L23 per-package = three-package / 3 "confirm against wall_s"; L297 "48.4 s = +41.7%" boundary; L385 +15 s = +6%. |
| IV5 | MET: L555-557 arms A2 vs A3/A4 separate catalogue from exchange; L109 H3 and per-package boards; L595 stop rule if harness alone reaches 3.0. | MET: L141-147 H share separate from C; L511 A2 catalogue-only arm; L528 reports H, catalog, communication separately. | MET: L126 "Overlap with collaboration assumed at 20%" between harness fixes and collaboration; L154 arms differ only in communication. | MET: L184 "Moves M4 and M6 only pay off once H1 and H3 hold"; L270 hook conflicts; A1 static-catalogue arm L653; H4 lowering I7 L597. | MET: L143-153 harness share, L141 prompting share, E-5 L535 three shares reported separately; L446 design 1 value mostly in A2 plus A4. |

### Qualitative Summary

| Dimension | V1 | V2 | V3 | V4 | V5 |
|---|---|---|---|---|---|
| CP | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| CR | 4/5 | 4/5 | 3/5 | 5/5 | 4/5 |
| ST | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| CL | 5/5 | 5/5 | 3/5 | 5/5 | 5/5 |
| RK | 3/5 | 3/5 | 2/5 | 4/5 | 3/5 |
| IV | 5/5 | 5/5 | 4/5 | 5/5 | 5/5 |
| total | 27/30 = 0.900 | 27/30 = 0.900 | 22/30 = 0.733 | 29/30 = 0.967 | 27/30 = 0.900 |

### Edge Case Floor Check

Floor: at least 1/5 on Invariant & Edge Case Coverage. V1 5/5, V2 5/5, V3 4/5, V4 5/5, V5 5/5: all five eligible as base.

## Position-Bias Mitigation

Pass 1 (input order) and pass 2 (reverse order) were run in parallel by separate evaluators. 150 criterion-variant pairs each; 140 agreed, 10 disagreed. Each disagreement was re-evaluated by the orchestrator with both passes' evidence and the variant text (re-checked V5:3, :106, :190, :302); the re-evaluation is final.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Reason |
|---|---|---|---|---|---|---|
| CR3 | V1 | NOT MET | MET | DISAGREE | NOT MET | "B" used for baseline time and issue ids; "T1" for theory and a time |
| CR4 | V1 | NOT MET | MET | DISAGREE | MET | dangling "section 4" reference is not a contradiction between claims |
| CP5 | V2 | NOT MET | MET | DISAGREE | MET | explicit exclusions (D3-D5 deferred; no Opus/sonnet reviewer) |
| CR4 | V2 | NOT MET | MET | DISAGREE | NOT MET | V2:182 "135 s" contradicts its own formula (0 from 128 s) |
| CP5 | V3 | NOT MET | MET | DISAGREE | MET | explicit exclusions (R3-R5 deferred; glm/Qwen excluded) |
| CR4 | V3 | NOT MET | MET | DISAGREE | NOT MET | V3:73 vs V3:176 (X-006) |
| CR5 | V3 | NOT MET | MET | DISAGREE | NOT MET | V3:67 contradicts the per-baseline cap; gains do not follow from inputs |
| CP5 | V4 | NOT MET | MET | DISAGREE | MET | explicit exclusions (grok; rejected transports; deferred designs) |
| CR4 | V5 | NOT MET | MET | DISAGREE | NOT MET | V5:3 "Nothing was run" vs V5:106 "Verified in this build" |
| RK1 | V5 | MET | NOT MET | DISAGREE | NOT MET | no 3 risks with probability and impact |

Disagreements re-evaluated: 10. Final verdicts that differ from pass 1: 5 (V1 CR4, V2 CP5, V3 CP5, V4 CP5, V5 RK1); from pass 2: 5 (V1 CR3, V2 CR4, V3 CR4, V3 CR5, V5 CR4).

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate points won (Round 3 tally) |
|---|---|---|---|---|
| V1 (opus:architect) | 0.4945 | 0.4500 | **0.9445** | 12 of 43 |
| V2 (opus:analyzer) | 0.4855 | 0.4500 | **0.9355** | 8 of 43 |
| V3 (haiku:backend) | 0.4690 | 0.3667 | **0.8357** | 0 of 43 |
| V4 (opus:devops) | 0.4950 | 0.4833 | **0.9783** | 12 of 43 |
| V5 (sonnet:performance) | 0.4955 | 0.4500 | **0.9455** | 11 of 43 |

**Margin**: V4 0.9783 vs runner-up V5 0.9455 = 0.033 (3.3 points), below the 5% threshold. V1 (0.9445) is also within 5%.
**Tiebreaker applied**: Yes.
- Level 1, debate performance: V4 12 and V1 12 points won, V5 11 (0.279 vs 0.256 of 43, within 5%), so no decision at level 1.
- Level 2, correctness criteria MET: V4 5/5, V1 4/5, V5 4/5. **V4 wins at level 2.**
- The tiebreaker agrees with the debate: all five advocates proposed V4 as base in Rounds 1, 2 and 3.

## Selected Base: Variant 4 (opus:devops)

### Selection Rationale

V4 has the highest combined score (0.978), the only perfect correctness subtotal (5/5) and the best risk coverage (4/5), and it is the base every advocate proposed in all three rounds. Its strengths are operational: every redesign carries (a)-(h) plus a detection/action runbook (S-001), a shared substrate with kill switch, baked board path and timing and baseline tables (S-002, U-011, U-013), one requirement-id scheme with a verification column (S-005), and its five redesigns are exactly the five cores of the agreed slate (F3 Move Radar, F4 Idle-Shift Sweeper, F1 Axis-Flip Challenge, F7 Flag-and-Adjudicate, F6 Coverage Deflection). Its weaknesses are the ones the debate repaired: planned-path figures labelled "worst", additive H and C, a seal that needed luna's compliance, a fixed sweeper timeout, and F6 on a non-seed baseline.

### Strengths to Preserve from Base
1. The (a)-(h) per-design layout with runbook tables (S-001).
2. The shared substrate: board, baked settings, kill switch R-05, `collab.json` R-23, SLO budget R-24, hooks fail open R-22 (S-002, U-011, U-013).
3. Requirement tables R-01..R-30 with a verification column (S-005).
4. Move catalogue M1-M10 with the best-style routing column (C-004); 12-200-character anchors (C-005); per-issue gain chains (C-008); relative alarm (C-007); process-exit seal (C-006); one findings block with P2-F ids (X-006).
5. The surface-finding filter (U-014) and Move Radar's zero-authoring telemetry (U-012).

### Strengths to Incorporate from Non-Base Variants
1. V1: searcher/reader complementarity in T1 (C-001); harness bundle with truncate-validate-re-ask and constant grading (C-003, X-008, X-009); panel finish signal, now in measured-reservation form (C-013, INV-001); seed baselines for every design (C-012); act rate tied to REQ-S3 (A-001); control-scale definitions (X-002, X-003, X-005, X-012); EL2 rationale (A-010).
2. V2: three-gate funnel (S-003); fresh A0, static-kit arm and A6 (C-010); one reach endpoint with final-look Fisher (C-011, X-013); no free text (X-007); sealed-report judging under random labels (A-003); gap-card decoys (A-006); confirmation on two new packages (A-009); the INV-005 online balanced deal.
3. V5: comparison columns for net collaboration, tokens per added issue and a static-kit row (S-004); itemised unverified list (S-006); T2a/T2b (C-002); three shares never summed (C-009); bottom-up H 0.03-0.34 (X-001); HL2 shadow schedule (X-004); "the kit may win" (X-010); anchor routes to B1/B2/I4 need the gap card (X-011); priced idle time (A-002); per-package baselines (A-005); c capped against measured reach (A-011); first-hand evidence rule (U-017); Spike 5 (U-018).
4. V3: 12-character leak check on variable fields (U-009); drift band (R2-V3:162-168); its Round 2-3 audit findings (HL2 mislabel, disjoint-split double count).
