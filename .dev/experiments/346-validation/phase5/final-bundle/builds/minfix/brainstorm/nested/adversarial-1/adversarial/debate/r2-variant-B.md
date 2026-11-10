# Round 2 - Variant B (sonnet, analyzer)

## Response to criticisms

Citation form: `A:NN`, `B:NN`, `C:NN` are lines of variant-1, variant-2, variant-3; `rA:NN`, `rB:NN`, `rC:NN` are lines of the Round 1 statements; `r2A:NN` is A's Round 2 rebuttal; `AR:NN` is ARMB-REPORT.md; `SP:NN` is `src/superclaude/commands/spec-panel.md`. Numbers marked "my script" were computed read-only for this round from the table at AR:13.

### 1. A's claim that Arm B's review-1 proxy of 16.5 moves B's forecast from 3.0 to about 4.1 (r2A:80)

**Arithmetic: correct.** B:407 is review-1 proxy times r squared. With 16.5 and r = 0.50 the result is 4.1; with r = 0.42 and 0.58 it is 2.9 and 5.6 (my script). This matches what I conceded in rB:66. The central 3.0 should not stand as a point forecast.

**Premise: not supported by the data A cites, and A's re-basing is internally inconsistent.** Four counter-points:

| # | Point | Evidence |
|---|---|---|
| 1 | The six recorded loops show no positive link between review-1 and review-3 proxy. Correlation of R1 and R3 is -0.54 (n = 6, not significant, but the wrong sign for A's scaling). | AR:13: R1 = 11, 12, 9, 9, 16, 17; R3 = 8, 4, 6, 5, 6, 1 (my script). Per-loop R3/R1: control 0.73, 0.33; treatment A 0.67, 0.56; Arm B 0.38, 0.06. The arm with the highest R1 had the lowest R3 mean (3.5). |
| 2 | R1 is run identically in every arm; the flags only enter at R2 and R3. | AR:6 ("Only difference from treatment A: the round 2 and round 3 review briefs"); AR:32 ("not an Arm B effect"). Treatment A used the same 427 text and got R1 = 9, 9, so the command text does not explain 16, 17. |
| 3 | I do not accept AR:32's "run-to-run spread" as proof either. | Within-arm R1 pairs are tight (11/12, 9/9, 16/17) and between-arm gaps are wide. That looks more like an arm-level cause (time separation, AR:35; flg-r1 master peeks, AR:18 and AR:36) than noise. The honest statement is that R1 for a new arm is unknown between 9 and 16.5, with 12.3 the pooled mean of all six (my script). |
| 4 | A kept r = 0.50, which B:407 derived from the 427 blend (0.66) times a 25% replacement cut. Re-basing R1 to Arm B while keeping the blend's r mixes two regimes. | The 0.66 is a mean of eight per-transition ratios over four 427-text loops (reproduced; control 0.715 over four). Split by arm, treatment A (no flags) runs at 0.81 as a mean of transition ratios (0.77 pooled) and Arm B (the arm A says to start from) at 0.51 (0.41 pooled) (my script). With Arm B's own r and R1 = 16.5 the no-cut model gives 2.8 to 4.3, against Arm B's realised mean of 3.5, so the model reproduces Arm B. A's 4.1 for Arm C is then "no gain over Arm B". Applying B:407's cut factors (0.63 to 0.88) on top of Arm B's own r gives 1.1 to 3.3 at R1 = 16.5, and 0.8 to 2.4 at R1 = 12. |

**What I take from it.** The 4.1 is one cell of a sensitivity grid and not the corrected forecast. Each cell rests on n = 4 transitions per arm, so the grid shows how little the data pin down, not a better estimate.

| R1 assumed | r = 0.42 | r = 0.50 | r = 0.58 | Arm B r (0.41 to 0.51) with cut |
|---|---|---|---|---|
| 9 (treatment A level) | 1.6 | 2.3 | 3.0 | 0.6 to 1.8 |
| 12 (pooled) | 2.1 | 3.0 | 4.0 | 0.8 to 2.4 |
| 16.5 (Arm B level) | 2.9 | 4.1 | 5.6 | 1.1 to 3.3 |

Updated forecast, labelled judgment: central 3.3, band 1.1 to 5.6. P(mean at most 3) about 0.4, P(bar a, every replicate at most 3) about 0.2 to 0.25. The carried-escalation term I conceded in rB:66 pushes up; Arm B's own lower r pushes down; I leave the net near the old centre but with a wider band. The forecast never decided between the designs (calibration and termination do), so I do not defend a number beyond this.

### 2. Remaining A criticisms (rA:63-74, r2A:35-39)

| # | Criticism | Answer |
|---|---|---|
| A1 | Reviser grants its own overrides (B:178), worst case 2 + 4 = 6 doubled findings (rA:65) | **Concede** (already rB:70). Drop the reviser-side `override:` path; keep only the reviewer's `large` flag, which is A's `L`. |
| A2 | Cycle cap `enforce` reverts the highest-gross findings first, which are the CRITICAL ones (B:211) | **Concede.** The order is wrong. Revert lowest-severity, smallest-class findings first, or use a fixed cap (C-005). See positions. |
| A3 | A 12-word minor budget reopens chain class A (B:176-178) | **Concede** (rB:69). Zero. B:226 and B:176 contradict each other and B:476 half-admits it. |
| A4 | An eighth bullet breaks seed:41 | **Concede** (rB:67). Fold into bullet 6 and a section. |
| A5 | Ids are free in the spec (B:165) against B's own evidence (B:476) | **Concede.** Ids belong in the ledger only. |
| A6 | The repository file breaks `test_worker_contract.py:831-839` | **Concede** (rB:68). Drop `## Unattended mode` from the repository file. |
| A7 | Exit 2 means over budget but argparse also exits 2 | **Concede** (X-004 to C). |
| A8 | The 3.5 to 4.5 band reads as "promising" instead of failing the bar | **Concede, and the point is stronger than A made it.** AR:23 calls a 3.5 mean "NOT MET". B:425 must read "bar not met; extend to four replicates as research, not as a pass". B:426 also lacks the spread condition (c) that B:378 requires (AR:25 shows (c) failing for the proxy). Row 6 of B:419-426 must add it. |
| A9 | Five subcommands and 20 to 31 calls (B:303, B:436) | **Concede in part.** Fold `hash` into `snapshot`, and `verify` into `check`. I keep `enforce` as its own verb (see A13). |
| A10 | The `@`-anchored sed misses invocations without ` @` (rA:74) | **Answered by A.** r2A:39 and r2A:79 verified that T05, T07 and T09 each contain `/sc:spec-panel @` once and T06, T08, T10 none; A withdrew it. I re-counted the templates directory: T07 and T09 contain it once, T08 and T10 zero. |
| A11 | Even split of a shared site's words across two ids (B:159) (r2A:37) | **Concede.** One owner per hunk (C's rule, C:62, C:88); other ids may be linked but add no budget. |
| A12 | Approximate matching (40-character substring, 10-word prefix) feeds an automatic revert (r2A:38) | **Partly concede.** The revert itself is exact (baseline bytes), the approximation only chooses attribution, and the error direction is over-revert, which is the safe direction for the budget. `check` runs again after `enforce`. But a wrongly attributed hunk can revert a good fix, so the replay harness (B:479) must report a mis-attribution rate, with a pre-agreed ceiling, before any worker runs. |
| A13 | Replace `enforce` by a `check --revert` flag (r2A:36) | **Contest.** The authoritative re-review run that I adopt from A must be read-only. The T07 and T09 templates say "write ONLY your output file; planning only, no edits to the spec or any other file" and "write ONLY that file; do not edit the spec" (verified in the templates). A mutating flag on the same verb that the reviewer runs is one typo from a violation, and `check` must also be stdout-only in reviewer use (A's `<stem>-fixcheck.json` file, A:86, would break T07). Keep "only `enforce --in-place` ever writes the spec" (B:211) as a safety property. |

### 3. C's criticisms of B (rC:64-76, rC:84-94)

| # | Criticism | Answer |
|---|---|---|
| C1 | Minor allowance contradicts a minimal-fix contract (rC:66) | **Concede.** Zero. |
| C2 | Self-granted exceptions (rC:68) | **Concede.** As A1. |
| C3 | Automatic rollback acts on approximate matching and a checker should validate, not overwrite (rC:70) | **Partly contest.** See A12 for the safety direction. C's own alternative (admit nothing and keep the last accepted spec, C:96) discards good fixes and C concedes the coupling problem anyway (rC:86). I keep script-side revert of whole findings, with C's coupled-revert correction. |
| C4 | `named` is informational, so out-of-scope edits pass (B:168) (rC:72) | **Partly concede.** C's registered-target check is the easier invariant to test. I keep it informational on evidence: B:447 shows both failure modes in the logs (ctl-r1 R2 N4 and N2 are "residue of round-1" findings that propagation would prevent; flg-r2 N3 and N6 are what propagation caused). A hard target gate trades one for the other. Decide when `named: no` shares are measured (B:475). |
| C5 | The failure table softens the bar (rC:74) | **Concede.** As A8. |
| C6 | An FR-8/FR-9 GAP graded minor gets the minor budget (B:481) (rC:76) | **Concede, verified.** SP:259 (bullet 2): "CRITICAL and FR-8/FR-9 findings are blocking". B:128 says the same, and B:481 then encodes a grader inconsistency as a minor budget. A hard-gate or CRITICAL finding graded minor must be an input error (exit 1), as C:43 does, not a budget class. |
| C7 | B:98's 11 of 17 over-cap result does not support "1 to 3 escalations" (rC:161) | **Concede** (A-004). A-004 in my table is "B, as a termination mechanism", not as a prediction. |

### 4. A correction to my own Round 1

I endorsed "C contradicts itself (C:90 against C:167)" on X-003 (rB:121). That was wrong. C:167 says each added paragraph "cites its finding id in the external fix ledger", which puts the id in the ledger and not in the document, the same as C:90. The diff's X-003 contradiction is overstated for C; B (ids free, B:165) is the only outlier. I withdraw the claim.

## Updated assessment

**A, after its defence.** A conceded 10 of 12 criticisms fully and 2 in part (r2A:31), and its Round 2 text now lands almost where B does: 80/120 caps, a script-side revert, the ledger inside the disposition file, hash plus stale-base refusal, no extra files written by workers. What still separates A from the merge, and why it is good:
- **Actor placement.** The reviewer writes every checker input and the reviser and the re-review read the same command line from the report. No coordinator duty. This is the best answer to the unbriefed-coordinator defect (X-012) and I take it.
- **Reviewer-only override, no ids in the spec, seven bullets, `## Unattended mode` dropped, the condition-word counter, the four causal falsifiers.** All verified or conceded. I take them.
- **What I would not take from A.** (1) The `check --revert` fold (A13): the re-review run must be read-only under the T07 and T09 ownership clauses. (2) The `-reviewed.md` copy and the `-ledger.jsonl` file, which A itself dropped (r2A:18). (3) The 4.1 re-basing (response 1): it keeps a 427-blend r on an Arm B R1. (4) Its "continue without the checker" rule, which A itself now drops (r2A:26).
- **A's A-004 position is the weakest of its R1 text** and A now concedes it (r2A:13). The remaining weakness is its forecast of 2.5, which assumed a 40-word cap that nobody now defends; A has not replaced it with a derivation.

**C, after its defence.** C's Round 1 text is honest about its own limits (rC:80 concedes the coordinator gap as "a blocking design defect", rC:82 withdraws the 1/1 forecast, rC:86 accepts the partial-admission coupling). Three things in C are better than B and I now take them:
- **Fail closed on a missing or stale physical input** (C:126). It is the house style of SP:258 bullet 1 ("never fall back to a first review"), and a review slot is the scarcest resource in the loop (3 reviews, SP:261). I move C-019 and X-007 to C.
- **A structural check that a hard-gate or CRITICAL finding is blocking** (C:43). It turns B:481's grader inconsistency into an input error. I move C-015 to C.
- **A fixed gross cycle cap that includes overrides, in bytes as well as words** (C:62), and the fresh-worker valid and invalid probe (C:289). B's relative 10% cap reverts in the wrong order (A2) and a probe proves delivery where a pre-flight hash only proves the script runs. I move C-005 and C-020 to C.

What I still reject in C: coordinator-run `freeze`, `check` and promotion with no route through the briefs (X-012; C conceded); all-or-nothing admission after a second failed check (C:96); a mandatory `wrong_outcome` JSON field on every blocking MAJOR for review 1, which changes the first review (AP-15) and is not needed by the budget; the removal cap (X-009; B's data put reviser removals at 84 to 379 words a cycle, so it rarely binds but adds a failure path to the cheapest fix); and seven new files with plugin mirrors that no test requires (new evidence 4). C's byte-exact reconstruction remains the strongest integrity invariant. With A's amendment (the checker finds each `before` string and computes the byte offsets, so the model supplies no offsets) it becomes buildable, and it is the right second-stage hardening after the replay harness shows the unit-diff attribution error rate.

**Where the merge should land (analyzer's view).**
1. Actors and delivery: A. Calibration, evidence, termination: B. Contract details and fail-closed: C.
2. Order of work: replay harness over the six recorded loops first (B:479), with a pre-agreed mis-attribution ceiling; then a one-replicate pilot to see whether a literal-minded reviser runs the script (B:451); then the n = 2 arm.
3. Forecast: a stated range (1.1 to 5.6), not 2.5, 3.0 or 1.0. The pre-registered fail line stays at the seed bar (mean above 3 fails), as A and C have it.

## New evidence

All read-only; the script ran under a private `/tmp` directory and was removed.

1. **R1 versus R3 across the six recorded loops** (AR:13; my script). Correlation -0.54, n = 6. Per-loop R3/R1: 0.73, 0.33 (control); 0.67, 0.56 (treatment A); 0.38, 0.06 (Arm B). Per-arm mean of transition ratios: control 0.715, treatment A 0.81, Arm B 0.51. Pooled sums: 0.718, 0.767, 0.409. With Arm B's own ratios and R1 = 16.5 the no-cut model gives 2.8 to 4.3 against a realised 3.5. Use: A's 4.1 re-basing does not follow, and neither does my 3.0. The full grid is in the response to criticisms, section 1.
2. **The re-review ownership clauses, verified in the S1 templates.** T07: "Ownership: write ONLY your output file; planning only, no edits to the spec or any other file". T09: "Ownership: write ONLY that file; do not edit the spec". T08: "edit ONLY the spec and write ONLY disposition-round2". Consequences for the merge:
   - The re-review's authoritative `check` run (A's design, adopted) must write nothing: stdout only, no receipt, no `-fixcheck.json`.
   - B's `.fixcheck/` writes at the reviser (T08) are still a literal conflict (B:452 row 7). The conflict is weaker than A's reviewer-authored file because the script writes it, but it is not zero. The pilot (B:451) decides.
   - The reviser's ledger inside the disposition file (B:134) is the only variant of the three that fits all three clauses.
3. **A baseline copy is already a coordinator duty in 427, and the S1 harness already makes it before each reviser.** SP:261 (bullet 4): "The coordinator keeps the review count, the prior-findings file and the saved copy". The coordinator log (lines 59 to 69) shows history copies saved by the coordinator at fixed paths, and the file times in `exp346-ab-flg-r2/.dev/orca-command-refactor/specs/history/` are 12:49 for `spec-v1-draft.md` (before review 1) and 13:12 for `spec-v2-after-round1.md` (after fix cycle 1, before review 2). Use: the reviewer's `reviewed_sha256` can be cross-checked against that existing copy at no cost, and a script-written `base-<N>.md` is redundant wherever the path is named. Limit: T06 and T08 do not name the path, so the reviser still cannot find it without a brief change; I keep `snapshot` as the fallback.
4. **No test forces a plugin mirror for a new command.** `tests/commands/test_routing_plugin_parity.py:41-47` mirrors four named commands only (`help`, `recommend`, `workflow`, `implement`) plus the `sc-recommend` tree. `tests/skills/test_spec_panel_review_loop.py:19-22` pins `spec-panel.md` in `src/` and `plugins/` only, and its T3 seven-bullet pin (line 83) is on those two files. Use: this closes my own UNVERIFIED at B:248 (no mirror is required for `spec-panel-minfix` or its skill) and removes the test-based argument for C's mirrors and design doc (C-030). The seven-bullet limit for the variant rests on seed:41, not on that test; the pin binds at promotion (B:480).
5. **C:167 is consistent with C:90.** Verified in the file: bullet 6 says each added paragraph "cites its finding id in the external fix ledger". The X-003 contradiction in the diff and in my Round 1 does not hold for C (response 4).
6. **FR-8/FR-9 are blocking by rule.** SP:259 (bullet 2) verified. B:128 states this; B:481 then contradicts it. The checker should reject a hard-gate or CRITICAL finding graded minor as an input error.

## Updated per-point positions

"Tie" means the letter is a nominal lean. Letter changes since Round 1: C-005, C-015, C-019, C-020, X-007 moved to C; C-016 and X-002 moved to A. C-008 keeps its letter with amended content.

| id | preferred (A/B/C) | changed since R1? | reason |
|---|---|---|---|
| S-001 | B | no | Tie: the same eight sections in seed order in all three. |
| S-002 | B | no | Tie: heading count does not touch any criterion. |
| S-003 | B | no | Six evidence tables, replicated by A (r2A:13) and by me (rB:34). |
| S-004 | A | no | Steps grouped by actor and phase are the easiest to build from; B's reference H3s interrupt the steps. |
| S-005 | B | no | Tie with A: literal bullet, section, script outline and test list per artifact. |
| S-006 | B | no | Derivation tables let a reader recompute the forecast, and A did (response 1). |
| S-007 | B | no | Detection, mitigation and residual columns per risk. |
| C-001 | B | no | Every finding listed with a derived class; add C's check that a hard-gate or CRITICAL finding is blocking (C:43). |
| C-002 | B | no | 80/50 needs the smallest cut (34% against 48% and 66%, rB:34); A withdrew 40. |
| C-003 | B | no | Tie with C: 120 gross; B adds net and add-only caps. |
| C-004 | A | no | Zero edits for non-blocking findings; B, A and C now agree. |
| C-005 | C | yes | A fixed gross cap that includes overrides, in words and bytes (C:62). B's relative 10% cap reverts the CRITICAL fixes first (A2). |
| C-006 | B | no | Universal and exec-recipe gates; add A's condition-word counter and C's byte counters. |
| C-007 | B | no | The ledger inside the disposition file fits T08 "write ONLY disposition-round2" (new evidence 2). |
| C-008 | B | yes (amended) | Unit diff with the capital-letter lookahead, but one owner per hunk (C:62, C:88) instead of an even split. The replay harness gates the mis-attribution rate. |
| C-009 | B | no | Reviewer hash plus stale-base refusal, with no coordinator duty; cross-check against the coordinator's saved copy (new evidence 3). |
| C-010 | B | no | Tie: `install_skills.py` strips only `sc-`, so all three folder names install (A and I both read it). |
| C-011 | A | no | One invocation for the model; fold `hash` into `snapshot` and `verify` into `check`; `enforce` stays its own verb (A13). |
| C-012 | C | no | argparse keeps exit 2; crash 70; separate input, hash and output failures. |
| C-013 | B | no | Script-side revert of whole findings guarantees termination; C's admit-nothing discards good fixes. Add the coupled-revert correction (A-002). |
| C-014 | A | no | The reviewer grants it, one per report; B's reviser-side path is dropped (A1). |
| C-015 | C | yes | A hard-gate or CRITICAL finding graded minor is an input error (C:43, SP:259), not a minor budget (B:481). |
| C-016 | A | yes | Bullets 2, 5, 6 amended in place, seven bullets, the budget numbers only in the script. A's bullet 6 carries the command line, so it needs no coordinator duty; C's text depends on a coordinator freeze (X-012). C:167 is not a contradiction (response 4), so this is about delivery, not ids. |
| C-017 | A | no | No ids in the spec; the id lives in the ledger. C is equivalent (C:90, C:167); B is the outlier. |
| C-018 | A | no | The re-review's own run is authoritative, in stdout-only mode; the report copies numbers and ids, never ledger prose (B:111). |
| C-019 | C | yes | Stop on a missing or stale receipt or physical input, as SP:258 bullet 1 does. A review slot is the scarce resource; a voided replicate is then impossible by construction. |
| C-020 | C | yes | The fresh-worker valid and invalid probe proves delivery and execution (C:289); my pre-flight hash only proves the script runs. Keep both. |
| C-021 | B | no | The `@`-anchored pattern touches exactly the review briefs (T07, T09 verified; A verified T05). |
| C-022 | B | no | Tie with A: no coordinator duty in either; C's duties have no route through the briefs. |
| C-023 | A | no | The repository file must drop `## Unattended mode` (`test_worker_contract.py:831-839`); the experiment file still uses the 472-line base (X-014). |
| C-024 | B | no | Only forecast with a derivation, but restated as a range, 1.1 to 5.6, central 3.3 (response 1); P(mean at most 3) about 0.4, P(bar a) about 0.2 to 0.25. |
| C-025 | B | no | 14.4% replay-derived and a 16.1% arithmetic ceiling; C's 21.3% byte bound should be stated beside it. |
| C-026 | A | no | Fail line at the seed bar, with causal falsifiers; B:425 and B:426 must be corrected (A8). |
| C-027 | B | no | Itemised cost breakdown. |
| C-028 | A | no | Tie: one short fit assessment per adopter; out of scope for all three. |
| C-029 | B | no | Chain taxonomy and cap replay; replicated twice (rB:34, rA:101). |
| C-030 | B | no | Tie with A: behaviour tests plus the `enforce` property test; no plugin mirror is required by any test (new evidence 4), so C's mirrors are scope. |
| X-001 | A | no | Zero for non-blocking findings; all three agree. |
| X-002 | A | yes | Seven bullets, bullet 6 replaced with the command line in it; C is equal on count but its text depends on a coordinator freeze. B's bullet 8 is conceded. |
| X-003 | A | no | No ids in the spec. Withdrawn from Round 1: "C contradicts itself" (response 4); the only outlier is B. |
| X-004 | C | no | The only layout that keeps argparse's exit 2 free; crash 70. |
| X-005 | B | no | The script reverts whole findings; add the coupled revert; revert order lowest class first. |
| X-006 | A | no | The reviewer grants; not the reviser (B), not an unbriefed coordinator (C). |
| X-007 | C | yes | Stop with a named input error on a missing or stale input; same reason as C-019. |
| X-008 | B | no | Numbers and ids only; flg-r2 round 3 judged statuses from the spec text, not from the disposition. |
| X-009 | B | no | Tie with A: free deletes keep delete-first worth doing; report removed words per cycle, do not cap them. |
| X-010 | B | no | Two independent re-counts (rB:34, rA:101) against A's lower-bound attribution. |
| X-011 | B | no | Size alone does not separate parents with blocking children (B:87); mild lean only (rB:35). |
| X-012 | B | no | Tie with A: no coordinator duty; C conceded the gap (rC:80). |
| X-013 | A | no | The fail line is the seed bar, and AR:23 calls a 3.5 mean "NOT MET". B's "promising" row stays a research action, not a pass. |
| X-014 | B | no | The 472-line base for the experiment file changes one thing at a time (AR:6). |
| A-001 | B | no | QUALIFY stands: B's lookahead splitter and word caps that do not move with unit boundaries; the replay harness gates it before any worker run. |
| A-002 | B | no | QUALIFY stands: `enforce` reverts whole findings; add a `depends:` cascade, a coupled revert for hunks linked to more than one id, and measure with `attacks:`. |
| A-003 | A | no | QUALIFY stands: zero minor budget keeps deferred text out of the changed-line scope; report the proxy and the 427 blocking count separately (C:302). |
| A-004 | B | no | Rejected as a prediction, kept as a termination mechanism: `enforce` converts a missed cut into a recorded escalation; pre-register the 100/60 retry (B:424). |

Tally (55 rows): B 32, A 16, C 7. Round 1 was B 37 (including ties), A 14, C 4 over the same 55 rows (counting the nominal letter of each tie); the seven moves are listed in the first line of this section.
