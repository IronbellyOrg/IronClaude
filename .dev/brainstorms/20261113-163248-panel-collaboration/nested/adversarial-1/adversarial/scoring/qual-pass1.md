# Qualitative scoring, pass 1 (input order)

Order evaluated: V1, V2, V3, V4, V5. Line numbers refer to each variant-N-original.md. Baselines were spot-checked against COMBO-REPORT (348/300/715/821 s, 676 s for ember+luna+sonnet; 49 blocking findings lost, ember 33 / luna 30; 156 of 665 runs without source.md) and all five agree with them. No variant has a dedicated out-of-scope section; CP5 is MET only where an explicit exclusion statement exists. No variant gives probability AND impact for each risk; RK1 is MET only where risks carry explicit probabilities.

## V1

| Criterion | Verdict | Evidence |
|---|---|---|
| CP1 | MET | Five designs R1-R5 each with schedule/transport/time/safeguards/gain (L148-526); theories L21-92; experiment L544-601. E.g. L171 "B = 116 s per package", gain tables L191-200 name I5, I4, B5, I1, B6, B8, B1, B2. |
| CP2 | MET | Per-design failure modes, e.g. L227 "Weaker models skip posting cards...", L374 "Card regions are wrong when anchors are not found (46 unanchored rows)". |
| CP3 | MET | L608 "Preconditions (spikes; each must pass before arms A3 or A4 run)" REQ-S1..S3; harness fixes REQ-H1..H6. |
| CP4 | MET | L587-595 decision rule with thresholds and stop-early; REQ-E2 pre-registration (L677). |
| CP5 | MET | L111 "The grading-rule problem ... is held constant in every arm ... listed as follow-up work". |
| CR1 | MET | L171 348 s over 3 packages gives 116 s; L258 715 s gives 238 s; L475 821 s gives 274 s; all match the brief. |
| CR2 | MET | L136-138 hooks plus Stop, L179 hard finish signal; read-only board outside sandbox (REQ-H6 L625); caps within +35% (L323). |
| CR3 | NOT MET | "B" means baseline time (L171 "B = 116 s", L138 "1.20 x B") and also issues B1-B8 (L17); "T1" is Theory 1 (L21) and "the moment the last reviewer's phase 1 ends" (L323). |
| CR4 | NOT MET | L111 says the grading rule is "listed as follow-up work in section 4", but section 4 (L544-601) has no such list. |
| CR5 | MET | Theory tables carry numbers and sources, e.g. L34-41 (0 of 176, 7 of 8, 5 of 11 with INV/CR cites). |
| ST1 | MET | Theories (L21), designs (L96), comparison (L528), experiment (L544), requirements (L604). |
| ST2 | MET | Each design has the same (a)-(h) sub-structure (L148-L524). |
| ST3 | MET | Shared scaffolding separated in 2.0 (L98-144) from per-design policy. |
| ST4 | MET | Evidence key table L5-15, move ids M1-M10 L115, REQ ids L604-679. |
| ST5 | MET | L604-679 numbered REQ-xx with a Test column. |
| CL1 | MET | Message kinds fixed, "no free-text field" (L130-134); caps stated numerically. |
| CL2 | MET | Concrete JSON envelope L133, byte/line caps, per-turn seconds L171. |
| CL3 | MET | Each section is purposed (theories / designs / comparison / experiment / requirements). |
| CL4 | MET | L17 defines labels and "Found /14"; L141 defines J as mean pairwise Jaccard. |
| CL5 | MET | L587-595 decision rule and L595 "Stop early" decision point; L681 states what was not checked. |
| RK1 | NOT MET | Failure-mode lists (L225-231, L517-524) carry no probabilities or impact ratings. |
| RK2 | NOT MET | R5 failure modes (L517-524) list six failures with no mitigation; R1 "Cards act as done signals" has none. |
| RK3 | MET | L376 "Phase 2 is killed at the cap ... fail-open, and the run still counts"; REQ-B7 L658 continue isolated. |
| RK4 | MET | L229 "Hook environment inheritance has not been verified"; L469-473 UNVERIFIED SendMessage items; L372 resume with gateway ids. |
| RK5 | MET | L140-144 convergence alarm, REQ-A1 L667 audit script, L273 tunnelling alarm. |
| IV1 | MET | L227 no gaps leads to isolated behaviour; L374 unanchored rows skipped; caps L167 "ember 3 total, luna 2 total". |
| IV2 | MET | L136 board outside every sandbox; L321 --no-session-persistence blocks --resume; L109 board per package under H3. |
| IV3 | MET | L136 "every write goes through one validator"; REQ-B7 corrupt line/missing dir; L229 invalid move ids rejected. |
| IV4 | MET | L138 finish at 1.20 x B plus 15% headroom; L323 "1.35 x T1 - 2 s"; L329 "+34.5% hard; expected ~150 s = +29%". |
| IV5 | MET | L555-557 arms A2 vs A3/A4 separate catalogue from exchange; L109 H3 and per-package boards; L595 stop rule if harness alone reaches 3.0. |

Subtotals: CP 5/5, CR 3/5, ST 5/5, CL 5/5, RK 3/5, IV 5/5, total 26/30

## V2

| Criterion | Verdict | Evidence |
|---|---|---|
| CP1 | MET | D1-D5 each with schedule, transport, time table, safeguards, gain (L151-476); theories L7-94; experiment L494-533. L174 "348 s / 3 = 116 s per package"; gains name I5, B8, B6, I7, B1 etc. (L199-206). |
| CP2 | MET | Failure modes e.g. L210-215 "hook does not receive the board path", L286 "--resume ... UNVERIFIED: fresh-session fallback". |
| CP3 | MET | L498 Spike S0 gate; L539 R-1..R-6 harness prerequisites. |
| CP4 | MET | L524-533 pre-registered decision rule; R-27 L579. |
| CP5 | NOT MET | Only deferral ("D3-D5 are deferred", L496) and "Nothing here reaches B1, B2, I4 or I6" (L206); no scope exclusion statement. |
| CR1 | MET | L174 116 s, L310 238 s, L377 274 s, L438 "676 s / 3 = 225 s (CR:320)" all match COMBO-REPORT; L71 "ember 81/209 = 39%" matches. |
| CR2 | MET | Fails-closed hooks (L211), fallbacks (L245, L286), +25% to +34% bounded (L182, L255). |
| CR3 | MET | M1-M9 catalogue, `panel-msg/1`, H/C/CI defined once and used consistently (L137-139). |
| CR4 | NOT MET | L182 "a luna that stops at 135 s or later gets none" contradicts the formula min(2, floor((150 - t_stop - 12)/11)) (L182, R-20 L569), which gives 0 from t_stop of 128 s. |
| CR5 | MET | Evidence tables with sources L19-29, L41-50, L67-75. |
| ST1 | MET | Theories, building blocks, designs, comparison, experiment, requirements. |
| ST2 | MET | D1-D5 each (a)-(h); gate table L83-94 maps issues to theories. |
| ST3 | MET | 2.0 shared blocks L100-147 separate from designs. |
| ST4 | MET | M1-M9 L104-114, R-1..R-28, spike S0. |
| ST5 | MET | R-1..R-28 each with *Test:* (L541-580). |
| CL1 | MET | Message schema with forbidden keys (L116-131); formulas for deliveries. |
| CL2 | MET | L169 "400 bytes per line; rendered delivery at most 1,200 characters"; per-turn timings L178. |
| CL3 | MET | Sections have distinct purposes; each design states aim at a theory. |
| CL4 | MET | L137 CI defined (mean pairwise Jaccard); "natural seal" defined L133; H and C defined L79, L139. |
| CL5 | MET | L496 chosen designs with reasons, L532 outcomes ("adopt the static catalog and stop"). |
| RK1 | NOT MET | No risk carries probability and impact; L213 "ember ... skipped source.md in 39% of runs" is the only rate. |
| RK2 | NOT MET | D3 failure modes (L345-351) and D4 (L413-418) list failures with no mitigation. |
| RK3 | MET | L211 "fails closed", L212 "fallback takes its sealed report", R-21/R-22 L570-571. |
| RK4 | MET | L172 hooks and Stop block UNVERIFIED; L308 gateway SendMessage; L286 resume with gateway ids. |
| RK5 | MET | L137 convergence alarm, R-23 board audit, R-24 L576 alarm reproduces 0.25 on history. |
| IV1 | MET | R-20 tests at stop times 100, 125, 140 s giving 2, 1, 0 locators (L569); "no-record case" L109; caps L167. |
| IV2 | MET | L133 natural seal; R-11 L554 seal precedes delivery; L194 board access audit. |
| IV3 | MET | L129 forbidden keys; R-8/R-9 L551-552 quote must be a substring, path must exist. |
| IV4 | MET | L3 "divided by 3"; L182 floor formula; R-2 L542 cut to 297 characters; L255 expected +25% vs worst +29%. |
| IV5 | MET | L141-147 H share separate from C; L511 A2 catalogue-only arm; L528 reports H, catalog, communication separately. |

Subtotals: CP 4/5, CR 4/5, ST 5/5, CL 5/5, RK 3/5, IV 5/5, total 26/30

## V3

| Criterion | Verdict | Evidence |
|---|---|---|
| CP1 | MET | R1-R5 each with (a)-(h) (L71-126); theories L30-52; experiment L142-167. Time arithmetic e.g. L76 "102 + 14 + 3 + 30 = 149 s ... +28%"; gain targets named (L78 "I7 (M2), B8 (M3), I5 (M5), B5 (M1), I4 (M4)"). Gain figures are aggregate ranges, thin per issue. |
| CP2 | MET | Failure modes per design (L80, L91, L102, L113, L124). |
| CP3 | MET | L146 "Pre-condition (not optional)" harness fixes; reqs 2-5 (L172-175); L166 hold-out package. |
| CP4 | MET | L158-161 adopt/extend/reject rule; reqs 20-21. |
| CP5 | NOT MET | L154 "R3, R4 and R5 are deferred" and L126 harness fixes "separate" are deferrals, not scope exclusions. |
| CR1 | MET | L69 348 s over three packages gives 116 s; legend counts (68, 52, 56 of 76) match the brief; no fabricated figures found. |
| CR2 | MET | Phase-2 caps (L76), hooks (L86), SendMessage flagged UNVERIFIED (L108). |
| CR3 | MET | M1-M6, R1-R5 and numbered requirements used consistently. |
| CR4 | NOT MET | L56 "Edit, Write and NotebookEdit disabled" yet "Each reviewer writes a sealed first-pass file (pass1.md)"; L73 phase-2 returns "a complete replacement findings-v1 block" vs req 6 L176 "output in a separate section outside the fenced block". |
| CR5 | NOT MET | L67 "Haiku (233 s median) and grok (790 s) alone break the +35% cap" is unsupported; the cap is relative to each panel's own isolated baseline (haiku + 2x luna 715 s is a measured baseline). |
| ST1 | MET | Theories, designs, comparison, experiment, requirements. |
| ST2 | MET | R1-R5 uniform (a)-(h). |
| ST3 | MET | Shared rules L56-69 separate from designs; harness fixes L126 separate. |
| ST4 | MET | Legend IDs L11-26, M1-M6, requirement numbers 1-21. |
| ST5 | MET | L171-191 21 numbered requirements each with "Test:". |
| CL1 | NOT MET | L69 "If the 348 s figure is a per-package figure instead, every budget here is conservative" contradicts its own "348 s over three packages". |
| CL2 | MET | L74 schema with example JSON; L85 enum scope values. |
| CL3 | MET | Sections have clear purposes. |
| CL4 | NOT MET | "DE runs" (L33) never defined; "GT10", "GT5" (L39) used while the legend defines only B/I labels. |
| CL5 | MET | L158-161 decision rule, L160 extension rule. |
| RK1 | NOT MET | No probability and impact per risk; only qualitative contamination/reliability columns (L132-138). |
| RK2 | NOT MET | Failure-mode lists (L80, L91, L113, L124) name failures without mitigations. |
| RK3 | NOT MET | Failures such as "Ember exits before the challenge arrives" (L113) have no recovery path; only run exclusion (req 16 L186). |
| RK4 | MET | L75 resume with gateway ids UNVERIFIED; L86 hook env UNVERIFIED; L108 held messages expire after 5 minutes. |
| RK5 | MET | L88 leak check, L77 Jaccard alarm, req 12 L182. |
| IV1 | MET | L91 "the board is silently empty"; caps L74, L85 (4 messages, 8 findings, 240 characters). |
| IV2 | MET | L56 "A hook refuses to release peer content until the file exists"; req 10 L180; L80 session expiry between phases. |
| IV3 | MET | req 7 L177 reject other fields; req 8 L178 "rejected, not truncated"; req 11 L181 anchor-leak hard failure. |
| IV4 | NOT MET | L69 treats the 348 s total as possibly per-package; no handling of unit/rounding divergence. |
| IV5 | MET | L126 "Overlap with collaboration assumed at 20%" between harness fixes and collaboration; L154 arms differ only in communication. |

Subtotals: CP 4/5, CR 3/5, ST 5/5, CL 3/5, RK 2/5, IV 4/5, total 21/30

## V4

| Criterion | Verdict | Evidence |
|---|---|---|
| CP1 | MET | Five redesigns each (a)-(h) with tables (L188-610); theories L22-85; experiment L630-682. Gain totals add up (R1 L238-245 low 0.20/high 0.88; R3 L419-430 0.23/0.94); per-issue rows B1...I6. |
| CP2 | MET | Failure/runbook tables per design with Detection and Action (L262-270, L331-339, L448-457, L527-535, L601-608). |
| CP3 | MET | L640-646 Gate 0 spikes S0, S2, S3; R-01..R-05 preconditions L690-696. |
| CP4 | MET | L664-673 pre-registered decision rule; outcomes table L677-682. |
| CP5 | NOT MET | L610 "Grok is used in no design" and deferrals (L634-638) are design choices; no explicit out-of-scope statement. |
| CR1 | MET | L156 116 s, L157 S13 100 s, L158 S07/S14 225 s, L159 238 s; L67 "luna 30, ember 33" matches CR:292; gain sums recompute correctly. |
| CR2 | MET | Hooks passed per reviewer with absolute paths (L124); resume with fresh-session fallback (L384); read-only kept (L137). |
| CR3 | MET | T1-T3, M1-M10, Redesign 1-5 and R-01..R-30 used consistently. |
| CR4 | MET | Time tables self-consistent; L396 explicitly reconciles 45 s timeout (+39%) with the 35 s luna guard; no contradiction found (L301 typical 142 s excludes the 6 s seal, a minor slip). |
| CR5 | MET | Evidence tables with file:line sources (L30-37, L45-53, L61-68); gain chains stated (L317-325, L417). |
| ST1 | MET | Theories, building blocks, redesigns, comparison, experiment, requirements. |
| ST2 | MET | Uniform (a)-(h) for each redesign. |
| ST3 | MET | 2.0 substrate (L91-185) separate from designs; section 5.1-5.6 grouping. |
| ST4 | MET | R-01..R-30, M1-M10, S0/S2/S3, source-key abbreviations L3-8. |
| ST5 | MET | R-01..R-30 with Verification column (L690-746). |
| CL1 | MET | "forbidden fields" list L117; numeric caps in every schedule table. |
| CL2 | MET | L111 JSON schema; timing constants table L143-148. |
| CL3 | MET | Each section purposed; devops framing L12-18 lists per-design deliverables. |
| CL4 | MET | Move text, "SLO_BREACH" defined R-24 L735, ALARM names defined R-25 L736. |
| CL5 | MET | L677-682 outcome table and abort criteria. |
| RK1 | NOT MET | Risks list L756-759 and runbook rows give no probability and impact. |
| RK2 | MET | Every failure row has an Action, e.g. L335 "switch delivery to 'tool call 8 or later, no seal needed'". |
| RK3 | MET | Runbook tables (L264-270 etc.), kill switch L139 "PANEL_COLLAB=0", L384 fallback. |
| RK4 | MET | L124 hook env UNVERIFIED, L384 resume UNVERIFIED, L532 Stop-hook timeout, L133 SendMessage reasons. |
| RK5 | MET | R-23 collab.json fields L734, R-25 alarms L736, R-24 SLO L735. |
| IV1 | MET | L455 "Digest empty ... challenges = 0"; L335 seal_missing; caps per reviewer (L288, L372). |
| IV2 | MET | L270 project hooks in tracked settings also fire; L457 session storage grows; L286 seal precondition. |
| IV3 | MET | R-06 L702 bad fixtures rejected; L456 two blocks in one report; R-02 L693 parser limits (anchor 12-200, id 16). |
| IV4 | MET | L396 45 s vs 35 s guard (+39% vs +30%); R-24 error budget "1 in 12", 1.5x breach; L156 cap 157 s. |
| IV5 | MET | L184 "Moves M4 and M6 only pay off once H1 and H3 hold"; L270 hook conflicts; A1 static-catalogue arm L653; H4 lowering I7 L597. |

Subtotals: CP 4/5, CR 5/5, ST 5/5, CL 5/5, RK 4/5, IV 5/5, total 28/30

## V5

| Criterion | Verdict | Evidence |
|---|---|---|
| CP1 | MET | Designs 1-5 each (a)-(h) (L157-396); theories L33-54; experiment L424-469. Gain tied to issues via move-issue map L85-92 (G1-B1 ... G8-I6/I5) and per-issue table L245-257. L177 "EL2, 116 s per package, cap +40.6 s". |
| CP2 | MET | L197 "ember skips source.md"; L349 "model omits or mangles the moves: line"; L396 "If haiku finishes early (below 100 s)". |
| CP3 | MET | L428-433 five spikes; H-1..H-6 L479-484; L538-545 known unverified items. |
| CP4 | MET | L456-463 decision rule with five conditions and fallback outcomes. |
| CP5 | MET | B-1 L490 "No cross-session messaging, Orca mail or A2A in the first experiment"; L446 designs 1 and 5 deferred. |
| CR1 | MET | L27-29 116/238/274 s and +35% caps match brief (116 x 0.35 = 40.6); L479 "77% of 665" = (665-156)/665; gain sums recompute (L191 0.21). |
| CR2 | MET | L106 `--max-turns` not in help so turn caps via hook counter and timeout; L121 hard cap by counter. |
| CR3 | MET | G1-G8, EL2/HL2/SL2, DS/AL/DE, H/B/S/C/D requirement families used consistently. |
| CR4 | NOT MET | L3 "Nothing was run for this variant" contradicts L106 "Verified in this build. `claude --help` lists --resume, --settings ...". |
| CR5 | MET | L94 explains how c is derived (half of sonnet's judged rate, sum 1.04 vs measured reach about 1.0) and L141 flags the prompting share as judgment. |
| ST1 | MET | Theories, substrate, designs, comparison, experiment, requirements. |
| ST2 | MET | 2.0.1-2.0.6 then 2.1-2.5 uniform (a)-(h). |
| ST3 | MET | Shared substrate separated from per-design sections; H/B/S/C/D/E requirement families. |
| ST4 | MET | IDs G1-G8, H-1.., B-.., S-.., C-.., D1-1.., E-..; evidence key table L7-17. |
| ST5 | MET | L473-536 requirement tables with Test column. |
| CL1 | MET | L119 drop rules incl. verdict-word list; numeric caps. |
| CL2 | MET | L112-118 schema; timing arithmetic with seconds per step (L179-184). |
| CL3 | MET | Section purposes clear; lens stated L3. |
| CL4 | MET | L19-21 DS/AL/DE and "hard ten" defined; L23-29 EL2/HL2/SL2 defined; L94 "What c means". |
| CL5 | MET | L428 spikes first; L454 interim look; L463 outcomes for no-pass cases. |
| RK1 | MET | L197 "ember skips source.md (39% of runs) ... 1 of 3 outcomes is a bad index"; "luna ignores the wrapper (a about 0.3 chance)"; L139 act rate 0.5-0.85. Impact stated qualitatively. Marginal. |
| RK2 | NOT MET | L263, L349, L396 failure lists with no mitigation for several items (e.g. "Models forget to post", "tired reviewer"). |
| RK3 | MET | L197 "the harness logs 'no delivery' and the run counts as isolated"; L385 15 s rule drops late phase 2. |
| RK4 | MET | L542 hooks inheriting board path, additionalContext, Stop block, --resume untested; L543 --max-turns missing. |
| RK5 | MET | L132 three convergence alarms; L454 interim look; C-3, C-4 L512-513. |
| IV1 | MET | L197 ember posts after luna's call 6 so no one receives it; L349 ember gets only one ticket; L228 relay-once dedupe; L330 scaling at n = 5. |
| IV2 | MET | L325 `stop_hook_active` guard; L396 session storage tied to working directory; L120 independence gate. |
| IV3 | MET | L119 schema/size/verdict-word drop; S-1 L501 seeded bad messages dropped. |
| IV4 | MET | L23 per-package = three-package / 3 "confirm against wall_s"; L297 "48.4 s = +41.7%" boundary; L385 +15 s = +6%. |
| IV5 | MET | L143-153 harness share, L141 prompting share, E-5 L535 three shares reported separately; L446 design 1 value mostly in A2 plus A4. |

Subtotals: CP 5/5, CR 4/5, ST 5/5, CL 5/5, RK 4/5, IV 5/5, total 28/30

## Summary

| Variant | CP | CR | ST | CL | RK | IV | Total /30 |
|---|---|---|---|---|---|---|---|
| V1 | 5 | 3 | 5 | 5 | 3 | 5 | 26 |
| V2 | 4 | 4 | 5 | 5 | 3 | 5 | 26 |
| V3 | 4 | 3 | 5 | 3 | 2 | 4 | 21 |
| V4 | 4 | 5 | 5 | 5 | 4 | 5 | 28 |
| V5 | 5 | 4 | 5 | 5 | 4 | 5 | 28 |
