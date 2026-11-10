# Round 2: Variant A advocate (opus, architect)

Sources: round1-A.md, round1-B.md, round1-C.md, evidence-flg-r1.md, variant-1-opus-architect.md sections 4-12, diff-analysis.md. New reads (read-only) in `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r1/.dev/orca-command-refactor/review/`: `disposition-round2.md` lines 1-40 and `spec-panel-round3.md` lines 141-146.

## Response to criticisms

### From round1-B.md

1. **B-1: the fix map is implicit and easy to game.** Concede. A's V2 (a hunk is mapped if its added text carries an open blocking id or its removed words overlap that finding's quote) is loose, and it has no `declined` outlet. The merge should use B's explicit `fixmap` with `declined <id> <reason>` lines and checks F1 to F3. A keeps only one thing here: the gate also runs inside `open`, so a skipped map stops the next review. One caveat from flg-r1: the four parent fixes there were real, mapped fixes of blocking findings. A stricter map closes id laundering. It does not touch the chains that drove that replicate's count.
2. **B-2: a bad report can end the run with no verdict.** Partly conceded. Most of A's non-demotable rules can become demotable or can be dropped. C13 (`DG-COVER`) goes away (see B-4). C12 becomes moot because the reviewer writes no verdict, so any stray `verdict:` line is stripped. The script writes the C11 header. A C6 label outside the vocabulary is recorded as `deferred: unanchored` with its raw label kept for the proxy count. A C2 duplicate id is renumbered by the script. Only C1 (no parseable `## Diffgate findings` section) and C3 (a finding id in the prose that is missing from the section) still stop the run. In both cases the script cannot tell what the reviewer meant to block on, so B's degrade would have to invent a verdict. In the merged design that stop happens rarely and fails closed.
3. **B-3: renumbering noise is named and left unsolved.** Concede, with a mechanical fix. The explicit map gets a `renumber H<k>.<n>` line. The script accepts it only if every changed token in the hunk is a digit run in a list or heading number position. The hunk still appears on the next surface, so nothing is hidden. It just needs no blocking owner.
4. **B-4: `DG-COVER` costs tokens and proves nothing.** Concede. Drop C13 and `DG-COVER`. A's own text already rated it weak evidence.
5. **B-5: the forecast rests on an untested density assumption and on one replicate's story.** Fully conceded, and flg-r1 now shows it was wrong (next section). A's section 9 said flg-r1's fix 2 made "about 5" blockers from 15 rows and that scaling to a third of the rows would cut them. The recorded data show 4 blockers from 4 blocking fixes. Cutting the 10 non-blocking rows removes one proxy item (R3-7) and no blocker. A's 60% and its "N5 would never have existed" story do not generalise.
6. **B-6: the byte copy contradicts the no-`src/superclaude` test (X-015).** Concede. Adopt C's removal of the `src/superclaude/examples/release-spec-template.md` read in `## Tool Coordination`, list it as the tenth change in A 8.1, and exempt that section in B's drift guard.

### From round1-C.md

1. **C-1: demotion can turn an evidence failure into a misleading scoped PASS.** Partly conceded. The experiment metric is already honest because demoted findings count in the R3 proxy. The operational verdict is the gap. Fix: if the demoted set holds any finding labelled critical or major, or blocking-grade under the profile, the script cannot print a clean PASS. The line reads `PASS (scoped; N demoted blocking-grade findings listed below)`, and the experiment's alternative "clean PASS by review 3" criterion does not credit it. I still reject C's invalid termination. Anchoring mistakes are the expected failure, and ending the replicate throws away a valid review and its accepted blockers.
2. **C-2: A's gate authorizes labels, not bounded repairs.** Conceded on labels (see B-1). Rejected on footprints as the fix. In flg-r1, R2-2 changed three lines (SPEC3:67, 188, 198) and R2-3 changed three lines (182, 183, 189). Each was a legitimate, mapped fix of a blocker, and each still produced a review-3 blocker. A pre-approved footprint would have contained both fixes and stopped neither chain. Footprints defend against laundering, which no replicate has shown, and they cost a coordinator step per blocker. Keep them out of the S1 arm. Report `bytes_by_id` and hunks per id instead.
3. **C-3: report replay is not independent confirmation.** Agreed, and A never claimed it was. Replay makes a hand-edited ledger worthless. It does not judge whether an outcome is true. C's confirmation file does not judge that either, by C's own account ("Presence of a confirmation is checkable; truth of its semantic judgment is not"). Both leave semantic truth to a model. The difference is cost, and replay is cheaper.
4. **C-4: the copy rule contradicts the portability test.** Concede. This is the same issue as B-6, with the same fix.
5. **C-5: token precision is not evidence for the forecast.** Concede. flg-r1 shows why: every review-3 blocker sits on words a blocking fix wrote, so a narrower surface still contains all of them. Token precision cuts review cost and anchor-gaming room. It does not cut the count of fix-induced blockers.

## Updated assessment of B and C

**B gains the most from this round.** flg-r1 bears out its forecast (mean 3.5, about 0.25 for both replicates) and its falsification F1 "wrong lever" (R3 of 5 or more with 70% or more of blockers on mapped fix hunks). Under a diffgate arm, a flg-r1-like replicate lands at about 5 with 100% of blockers on mapped blocking-fix text, which is F1 exactly. B's fix-chain printing (U-009) is now the most useful ledger output, because every flg-r1 review-3 blocker is a length-3 chain (finding 8 -> R2-2 -> R3-1, and so on). B's remaining weaknesses are the ones B conceded: line-level hunks on paragraph lines, a reviewer-written verdict, degrade-everything on structural failure, paddable constants, and the missing `test_routing_refresh.py` edit. The merge I would accept: A's script structure, grammar, token surface, test integration and `PROFILES` seam, plus B's explicit map, `declined`, `via=`, `--expect-round`, chains, F1, staging and forecast.

**C's strongest machinery targets a failure the data do not show.** Footprints, coordinator confirmation and invalid termination guard against id laundering, padded outcomes and malformed evidence. flg-r1's count came from small, legitimate, mapped fixes that were themselves defective, and none of C's guards acts on that. C's cost (5 to 13 added minutes per loop and replicates lost to invalid termination) therefore buys protection the S1 question does not need. C is right that no variant should buy convergence by relabelling, and flg-r1 makes that warning more important, because a relabelling rule is now the only thing that could make the bar pass on a flg-r1-like run. C's other contributions belong in the merge: U-016 (line 220), separate acceptance criteria, the spread check, the Skill-invocation transcript check, old-side deletion anchors, the scoped-PASS sentence, the isolated-HOME install test, and valid FAIL exiting 0.

## flg-r1 evidence: revised prediction and any in-theme lever

**What flg-r1 shows.** Review 3 has proxy 6 and 4 blockers. All 4 blockers sit on text written by fixes of blocking findings: R3-1 on R2-2's fix, R3-2 on R2-3's fix, R3-3 on R2-1's fix, and R3-4 on R2-1's and R2-4's fixes. Each review-2 blocker in turn sits on text written by a round-1 blocking fix. A blocking-only fix gate (all three variants) removes R3-7 and nothing else. R3-8, a MAJOR label graded minor, sits on SPEC3:64, which blocking fixes also wrote, so it stays.

**Revised Variant A prediction for the S1 bar.**

| Quantity | Round 1 (A section 9) | Revised |
|---|---|---|
| flg-r1-like replicate, R3 critical+major proxy | (not addressed) | 4 to 5 (4 blockers, plus R3-8's MAJOR label; R3-7 removed) |
| flg-r2-like replicate | 1 to 3 | 0 to 2 (N5 and N12 may never exist if fix 1 skips F22) |
| Mean over two fresh replicates | 2.0 | about 3.0 (range 1 to 5) |
| P(both replicates 3 or fewer) | about 60% | about 0.25, the same as B |
| P(at least one replicate triggers B's F1) | n/a | about 0.5 |
| Growth after 2 fix cycles | 15% to 25%, P about 0.95 | 15% to 25%, P about 0.9 (Arm B's flg-r1 already sits at 27.8%) |

The reason is that the observed per-blocking-fix defect rate at fix 2 swings from about 0.17 (flg-r2: 6 blocking fixes, 1 new blocker) to 1.0 (flg-r1: 4 fixes, 4 blockers). With two fresh replicates, the bar passes only if both draw a low rate. Diffgate does not change that rate. It removes noise from minor fixes and makes the chains visible.

**Is there an in-theme lever that acts on blocking-fix-induced chains without relabelling or hiding real defects?** I checked each of the four parts of the theme.

- **Computed surface: no.** The four blockers sit on new words that blocking fixes wrote. V1 puts that text in scope by design, and the token-level surface still contains it. Narrowing the surface further would mean not reviewing fix text, which is hiding.
- **Anchor checker: no.** Each blocker anchors on changed words and cites other lines as evidence. R3-4, for example, anchors on WC-4's new text at SPEC3:64 and cites WC-6 at SPEC3:66, a line no fix-2 row lists as changed. A's C5 accepts that legitimately. Rejecting such findings would be hiding.
- **Fix gate: no reduction.** All four parent fixes were mapped blocking fixes, and two of them changed only three lines. A byte budget or a footprint would not have stopped them. A stricter gate can only push revisers toward under-fixing, which moves the count from "new" to "open prior" (A-003). Both count the same in the proxy.
- **Ledger: detection only.** Before fix 2, the ledger can compute that each review-2 blocker sits on text a round-1 blocking fix wrote. In flg-r1 that recurrence flag would have fired on all 4. The ledger can print the chain, mark the region "second attempt", and, under B's rule, escalate a length-3 chain to a person. Escalating to a person leaves the unattended loop that S1 measures, so it is not an honest lever for this bar. Any rule that downgrades, defers or excludes recurrence blockers is relabelling and is ruled out.

**Honest answer: no mechanism inside the diffgate theme lowers the count of blocking-fix-induced blockers without relabelling or hiding them.** The closest candidate is a reviser aid, not a gate. `gate` could print, for each of the reviser's own hunks, the unchanged lines that share an identifier token with it (WC-6, AC-1.2, `--report-dir`), so the reviser checks for knock-on conflicts before the next review. Two of flg-r1's four blockers (R3-3 and R3-4) have that cross-reference shape. R3-2 does not, because it rests on an external fact about `git status`. This aid is mechanical input but a prose-dependent action, it is unmeasured, and I expect its effect to be small. It needs its own ablation arm and must not count as part of the diffgate result.

**What follows for the experiment.** A should adopt B's F1 as its primary diagnostic and pre-register the forecast above. If the owner runs S1 anyway, the result most likely to be learned is a measured per-blocking-fix defect rate under scope control. That is useful, but it is not a pass. The lever that F1 points to, fix quality, sits outside this theme.

## New evidence

1. **The S1 spec really is one paragraph per line, and fix text is paragraph-sized.** flg-r1's `disposition-round2.md` section 3 reports 67,886 bytes and 293 lines before fix 2, 73,807 bytes and 293 lines after, "60 lines changed", and "every edit stayed inside existing lines". A line-level surface for review 3 would therefore be 60 paragraph lines. This supports A's token-level surface (C-008) on cost and anchor precision, not on count.
2. **Small fixes produced blockers.** R2-2 changed SPEC3:67, 188 and 198, and R2-3 changed 182, 183 and 189 (evidence note). Each produced a review-3 blocker. That is direct evidence against size or footprint containment as a convergence lever (C-014, C-015, X-013).
3. **The reviser deliberately spread blocking fixes.** `disposition-round2.md` method: "Root causes, not single cells: where a fix changed a shared rule, every passage that depends on it was brought into line in the same revision (listed under 'Knock-on edits' in the R2-1 and R2-4 rows)." Knock-on edits carry the blocking id, so every variant's gate passes them. R3-3 and R3-4 sit on R2-1 and R2-4 text. No gate design can tell a knock-on edit from the core fix without semantics.
4. **The chains recur on the same lines.** The same method note says settled round-1 fixes were "reopened only where a finding names them (R2-2 on finding 8, R2-3 on finding 9 ...)". Lines 67 and 188 were written by finding 8's fix, reopened by R2-2, and then cited by R3-1. A ledger can detect this recurrence mechanically, which supports B's chain output (U-009).
5. **The review-3 blockers are real defects with a dependency shape.** `spec-panel-round3.md` lines 141-144: R3-1 (a closed list in 7.2 step 5 against WC-7), R3-2 (`git status --porcelain --untracked-files=all` misses ignored paths, tested in a scratch repo), R3-3 (new P1 scope against AC-1.2 at SPEC3:200), and R3-4 (the WC-4 report directory against WC-6 and the Resume column). All anchor on changed text, so none needs `via=`. That narrows X-005 to a rare case.

## Shared assumptions

- A-001: QUALIFY: the merged recovery path (correct once, then demote, stop only on C1 or C3) needs little improvisation, but compliance is assumed; record it per replicate as a validity input.
- A-002: QUALIFY: flg-r1 shows a smaller surface removes noise from minor fixes (R3-7) but not blockers, which sit on blocking-fix text; record findings per changed token so a density effect is visible.
- A-003: QUALIFY: any gate stricter than "mapped to a blocker" can only move counts from new to open prior; report open priors and `declined` lines separately from new findings.
- A-004: REJECT: the added brief lines are prose that can act without the script; claim the combined treatment or add a briefs-only arm, and keep the reviser cross-reference aid in its own arm.
- A-005: QUALIFY: A's DG-line change is the smallest review-1 change, but review-1 blocker counts must still be checked against Arm B's 13 to 17 as a validity gate.
- A-006: REJECT: now answered by evidence: flg-r2's composition does not hold for flg-r1, and A withdraws the forecast and causal story it built on flg-r2.

## Per-point positions (updated)

| Point | Superior approach (A, B, C, merge like A+B, or tie) | One-line reason |
|---|---|---|
| S-001 | C | Separate test and acceptance sections; all three advocates now prefer C or call it a tie. |
| S-002 | C | Tiered P0/P1 tests with negative cases are the easiest to execute; fold A's 16 script cases into C's tiers. |
| S-003 | C | Implementation acceptance kept apart from experiment success, with C's criterion 15 moved to the experiment gate as C concedes. |
| S-004 | A+C | A's verbatim bullets as single physical lines, plus C's removal of the line-220 template read as a tenth listed change. |
| S-005 | A+B | A's signatures fix the interfaces; B's named constants and line budget bound the size. |
| S-006 | A+B | One shared exit table with a who-acts column; all three advocates accept this. |
| S-007 | B+C | flg-r1 shows dense citations did not stop A's wrong causal story; B's UNVERIFIED tags and replay plus C's PROPOSED labels are the better discipline. |
| S-008 | A+B | A's bullet-keyed residual-risk table plus B's extra concerns such as step order. |
| S-009 | A+C | A's residual column plus C's separate cost envelope. |
| S-010 | B+C | B flags experiment blockers; C gives every question a default. |
| C-001 | A+B | Worker-owned steps locked to each other; the coordinator only reads `status`; C's confirmation checks presence, not truth, by C's own account. |
| C-002 | A | The verified installer analysis decides the name; a by-path call plus C's transcript check of that call is enough. |
| C-003 | A+B | B's smaller set (fold `final` into `close`, `status` optional), keeping A's rule that `open` re-runs the gate. |
| C-004 | A+C | One JSON object per call, with separate verdict and execution-success fields. |
| C-005 | B+C | B's one-meaning-per-code table with C's rule that a valid FAIL exits 0. |
| C-006 | A | JSON-string quotes in DG lines; B concedes `[[...]]` breaks on `]]`; C's strict JSON draft is the largest review-1 change (A-005). |
| C-007 | tie | File layout does not change behaviour; flat files or per-round folders both work. |
| C-008 | A+C | Token-level surface for paragraph lines (flg-r1: 60 changed lines, line count unchanged), plus C's rule that context is never eligible. |
| C-009 | A | `H<k>.<n>` never repeats and is shared by the gate and the next surface; a digest adds nothing the ledger hash lacks. |
| C-010 | A+C | A's rules without C13, plus C's validation of every claimed anchor. |
| C-011 | A+B+C | Demote or degrade anchor failures (A, B), stop only on C1 or C3 (A), and never print a clean PASS when blocking-grade findings were demoted (C). |
| C-012 | A+B | An unanchored finding is a free deferral; C's reject spends the one repair on a legal outcome. |
| C-013 | B | Quote-checked `via=` gives a legal route; over-cap `via` findings should be deferred and still counted in the proxy, which answers C's third-regression worry. |
| C-014 | B | An explicit map with `declined`; footprints would not have stopped flg-r1's chains (R2-2 and R2-3 changed three lines each). |
| C-015 | A+B | Report bytes and hunks per id with no gate; flg-r1 shows small fixes still induce blockers. |
| C-016 | tie | All three reject a severity ceiling; flg-r1 makes a ceiling the obvious relabelling trap. |
| C-017 | B+C | B's `seen:` rounds and no-cite rule plus C's scoped-PASS sentence; A's appendix placement is compatible. |
| C-018 | A+C | The reviewer writes no verdict and the script supplies it; B now agrees. |
| C-019 | A | Presence of an outcome with no paddable constant; C's confirmation is presence-only by C's own words and costs a coordinator step. |
| C-020 | A | No severity field on carried status lines makes upward drift impossible by grammar. |
| C-021 | tie | All three keep minors away from the reviser; in flg-r1 this removes only R3-7. |
| C-022 | A+B | A word-identical reflow is not a hunk; B's coverage warning flags a degenerate surface. |
| C-023 | B | flg-r1 bears B out: 4 of 4 review-3 blockers sit on blocking fixes; A withdraws its 60%. |
| C-024 | tie | All forecasts clear 44.4%; Arm B's flg-r1 already sits at 27.8%. |
| C-025 | A+B+C | B's F1 as the primary diagnosis, A's blindness and demotion conditions, C's spread check. |
| C-026 | A+B | The all-discovered count gates the bar; C concedes. |
| C-027 | C | The most complete accounting; A's estimate omitted correction turns. |
| C-028 | A+B+C | A's hash of the untouched `spec-panel.md` and no `--force`, B's `--expect-round`, C's installed-file hashes and transcript check. |
| C-029 | B | Dropping the 427 flags from Usage is simplest; ignoring them (A) keeps dead text. |
| C-030 | A+B+C | A's two existing-test edits, B's drift guard with a `## Tool Coordination` exemption, C's isolated-HOME install test. |
| C-031 | A+B | A verbatim `## Unattended mode` with the name swapped stays pinnable; A's C1/C3 stop already marks the contract failed, which covers C's concern. |
| C-032 | A+B | No mirror is needed and a separate design note keeps 427's doc historical; C concedes. |
| C-033 | A | A fresh-review blindness audit classified by ledger history; all three now agree. |
| C-034 | A+C | The `PROFILES` seam for rf-qa, with C's limits on replacing `/sc:implement` FINAL or weakening rf-qa guards. |
| C-035 | A+C | Ledger replay plus C's lock and size limits, which are cheap in a script meant for reuse. |
| X-001 | A+B | Same as C-001: worker-run steps with mutual locks. |
| X-002 | A+B+C | Same as C-011: demote, stop only on structure, no clean PASS with demoted blocking-grade findings. |
| X-003 | A+B | A word-identical reflow carries nothing to review; edited words inside it still surface. |
| X-004 | A+B | Same as C-012. |
| X-005 | B | `via=` covers the case it exists for, but all flg-r1 review-3 blockers anchored on changed words, so it is a narrow escape, not a driver. |
| X-006 | A+C | Same as C-018. |
| X-007 | B | flg-r1 evidence supports B's 0.25; A's revised forecast now matches it. |
| X-008 | A+B | Same as C-026. |
| X-009 | A+B | Whitespace-only edits are not hunks and need no owner. |
| X-010 | B | Same as C-029. |
| X-011 | A+B | The parity test pins only README-listed commands. |
| X-012 | A | Only A plans the `_POST_REFRESH_ADDITIONS` edit; B and C concede. |
| X-013 | A+B | No gate, bytes reported; R2-2 and R2-3 show a size gate would not have helped. |
| X-014 | A+B | A name that does not match the command, called by path; C's Skill activation is a legitimate alternative, not an error. |
| X-015 | C | A concedes; remove the line-220 read. |
| X-016 | C | Same fix; B's drift guard exempts `## Tool Coordination`. |
| X-017 | A | Register the variant in a `UNATTENDED_VARIANTS` map; the verbatim section keeps parity with the parent. |
| X-018 | tie | B conceded the 13 versus 14 slip; it has no design effect. |
