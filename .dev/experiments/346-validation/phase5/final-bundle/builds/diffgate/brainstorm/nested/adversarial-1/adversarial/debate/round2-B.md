# Round 2: Variant B advocate (sonnet, refactorer)

Sources: round1-A.md, round1-B.md, round1-C.md, round2-A.md, evidence-flg-r1.md, diff-analysis.md, variant-2-sonnet-refactorer.md (grep for C1, degrade, FIX_BUDGET). New read-only checks in `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r1/.dev/orca-command-refactor/`: `review/disposition-round2.md` lines 1-45, `review/spec-panel-round3.md` lines 138-151, and token counts on `specs/orca-worker-contract-spec.md` (lines 64, 66, 67, 162, 188, 200). Round1-C is the only C text so far; C has not yet rebutted.

## Response to criticisms

### From round1-A.md (A's weaknesses of B)

1. **A-W1, byte-identical copy and drift guard contradict "no `src/superclaude`" (X-016).** Concede. Adopt C's removal of the line-220 template read (U-016) as a named change in the variant. The drift guard compares every untouched `## ` body to `spec-panel.md`, and for `## Tool Coordination` compares after that one substitution.
2. **A-W2, `test_routing_refresh.py` is missing from B's plan (X-012).** Concede. Stage B adds `"spec-panel-diffgate"` to `_POST_REFRESH_ADDITIONS`, as A's 8.6 does.
3. **A-W3, graceful degradation hides format failure.** Partly concede. Structure failures (no FINDING lines and no `FINDINGS none`, or a round line that disagrees with the ledger) that survive the one repair now exit 1 with no verdict, which is A's rule. Everything else still degrades. A degraded run can no longer print a clean PASS: it prints `PASS (scoped; N degraded or deferred blocking-grade findings)`, which is C's disclosure. What I keep: degraded and deferred findings stay in `R3-proxy-all` by their reviewer label, so degrading cannot win the bar.
4. **A-W4, reviewer writes a `verdict:` line (X-006).** Concede. The reviewer writes none; `check` prints the verdict line and the command appends it. Rule C1's verdict clause and C13 are deleted, which removes a reject path.
5. **A-W5, arbitrary constants.** Concede both. `OUTCOME_MIN = 25` is replaced by A's rule (an `outcome` other than `-`), which has the same checkability and no padding threshold. `FIX_BUDGET_BYTES` and the `over_budget` flag are removed; the gate reports `bytes_by_id` and hunks per id as figures only. flg-r1 supports removal: R2-2 and R2-3 were three-line fixes and each still produced a review-3 blocker, so a byte budget would not have fired where it mattered. Fewer constants is less debt.
6. **A-W6, replay count 13 versus 14 (X-018).** Concede. The gate would have allowed 14 lines. I now state the replay only qualitatively (noise removed, the induced blocker kept).
7. **A-W7, concurrency left open.** Concede the cheap half. `begin` re-runs `check` on the recorded report and exits 2 on any ledger mismatch (A's U-004), and a single exclusive-create lock file guards writes (a few lines). C's size limits and symlink refusal are cut as over-scope for an experiment arm.

### From round1-C.md (C's weaknesses of B)

1. **C-W1, degrade is safe in one error direction only.** Covered by A-W3 above. The other direction (a real changed-line blocker removed from acceptance) stays visible: it is listed in `deferred.md` with `reason=unanchored`, counted in the bar, and named in the scoped-PASS line.
2. **C-W2, `MERGE_GAP = 2` lets unchanged gap lines become eligible anchors.** Concede; this was a real hole. Eligibility now comes only from lines that changed, tested at token level (A's C5 overlap rule). `MERGE_GAP` only groups adjacent changed lines into one hunk id for the fix map and the display; gap lines and display context are never eligible. Pure deletions use C's old-side quote plus an insertion-boundary anchor.
3. **C-W3, the `via` cap bounds discovery, not harm.** Partly concede. Evidence: in flg-r1 none of the 10 review-3 findings needed `via` (all anchor on changed lines), so the cap is a rare-case guard, not a driver. Fix: a `via` finding over the cap is not dropped; it is deferred with `reason=via-cap`, counted in the proxy, and forces the scoped-PASS wording. `VIA_CAP` remains a guess and its use is recorded.
4. **C-W4, a sidecar map without containment permits id laundering.** Partly concede. Footprints are the only mechanism of the three that closes laundering, and I say so. But the data show no laundering: the flg-r1 reviser tagged every changed passage with its `R2-N` id and listed knock-on edits per row (`disposition-round2.md` lines 11-12), and the four blocking fixes were genuine. Footprints would have contained R2-2 and R2-3 (three lines each) and stopped neither chain, at the cost of a coordinator step per blocker. Position: not in the S1 arm. Hardening trigger for later: if the `bytes_by_id` audit finds mapped edits with no word overlap with the finding's quote, add footprints then.
5. **C-W5, two integration holes (X-012, X-016).** Concede; same as A-W1 and A-W2.
6. **C-W6, the replay is overprecise (X-018).** Concede; same as A-W6.

### From round2-A.md (A's rebuttal remarks on B)

1. **Line-level hunks on paragraph lines.** Concede the eligibility part: anchors are now checked at token level. Counter on ids: A's token-level hunks needed a new `renumber H<k>.<n>` rule that depends on parsing "a digit run in a list or heading number position". Block-level ids avoid the problem, because a renumbered list merges into one hunk that needs one owner. Merge: token overlap decides which text can carry a blocker; block ids decide who owns an edit.
2. **Reviser-written verdict, degrade-everything, paddable constants, missing routing edit.** All four conceded above (A-W4, A-W3, A-W5, A-W2).
3. **"Escalating a length-3 chain to a person leaves the unattended loop."** Concede. The chain line is a report line only (`R1.5 -> R2.1 -> R3.2`). The "revise this region by hand" advice moves to the end-of-loop summary; no rule halts on chain length. The only halt is 427's own `halt: escalate` at a FAIL at the cap.
4. **Fix map inline-id convenience.** A's inline form has one real advantage: flg-r1 revisers already tag changed spec passages with `R2-N`. Merge: `fixcheck` pre-fills `fixmap` candidates from inline `R<k>.<j>` tags in the added text, and the reviser confirms or writes `declined`. The explicit file stays the authority.

## Updated assessment of A and C

**A.** Stronger than in round 1 and closest to a base for the merge. It conceded the implicit fix map, `DG-COVER`, the line-220 contradiction and its 60% forecast, and its stop-only-on-C1/C3 rule now matches what I conceded. Its honest answer to the flg-r1 question (no honest lever) is correct. What still favors A: token-level eligibility (I adopt it), the verified installer naming analysis, both existing-test edits, ledger replay, `PROFILES`, the grammar with no severity field on carried lines. What still favors B over A: explicit `declined` and map, `via=`, `--expect-round`, chains, F1, staging, and the one replay on recorded data. A's new `renumber` rule is a heuristic parser rule that block ids make unnecessary.

**C.** Round 1 showed the most careful acceptance design, and flg-r1 sharpens the cost side. Footprints, coordinator confirmation and invalid termination guard against laundering, padded outcomes and malformed evidence. None of those appears in the flg-r1 data, and none would have changed its count. Invalid termination is also worse with n=2: a single mistyped anchor discards a replicate. C's integrity parts stay in the merge: U-016 (line 220), U-017 (spread check), U-019 (Skill-invocation transcript check where a skill is used), the acceptance-versus-experiment split, old-side deletion anchors, valid FAIL exiting 0, the scoped-PASS sentence, the isolated-HOME install test. C's own concessions (metric ambiguity X-008, missing two existing-test edits, ungrounded forecast) stand. I withhold a final view of C's rebuttal until it exists.

## flg-r1 evidence: revised prediction and any in-theme lever

**What flg-r1 shows for B.** In flg-r1 review 3, all 4 blockers sit on text written by blocking fixes (R3-1 on R2-2, R3-2 on R2-3, R3-3 on R2-1, R3-4 on R2-1 and R2-4), and each review-2 blocker sits on text a round-1 blocking fix wrote. A blocking-only fix gate removes R3-7 (a MAJOR label graded minor, on a minor-only fix) and nothing else. That is B's F1 "wrong lever" case. B's round-1 guess of "about 5 and 2" fits this, but it was a judgement made without reading flg-r1 (my open question 12), so the match supports the replay method and not more.

**Revised B prediction for the S1 bar.**

| Quantity | B round 1 | B revised |
|---|---|---|
| flg-r1-like replicate, R3 critical+major proxy | about 5 (guess, flg-r1 unread) | 5 (4 blockers + R3-8's MAJOR label; R3-7 removed) |
| flg-r2-like replicate | about 2 | about 2 (replay: 5 to 2) |
| Mean over two fresh replicates | 3.5 | 3.5 (range 1.5 to 5.5) |
| P(both replicates 3 or fewer) | about 0.25 | about 0.2 |
| P(F1 fires in at least one replicate) | not stated | about 0.55 |
| Growth after 2 fix cycles (44.4% bar) | mean 23%, about 0.9 | same; flg-r1 Arm B is already at 27.8% and the gate drops minor-fix growth |

Reason for 0.2: the per-blocking-fix defect rate at fix 2 swings between runs (flg-r1: 4 blockers from 4 blocking fixes; flg-r2, as A and B both reported: about 1 from 6). With two fresh draws the bar passes only if both draw the low rate and land at 3 or fewer. Diffgate does not change that rate. S1 as written is therefore mostly a measurement of that rate under scope control, and I expect it to say "bar missed, F1 fires" about as often as it says "bar met".

**Two edits to B that follow.**
- F1 is re-based on the bar instead of a separate constant: F1 fires when the R3 proxy is above 3 and at least 70% of review-3 blocking findings sit on mapped fix hunks. The old "R3 of 5 or more" is brittle: remove R3-8 (a label graded minor) from flg-r1 and the proxy is 4, the mechanism is identical, and F1 would not fire.
- Report the label proxy (the bar) and the 427-blocking count side by side. In flg-r1, 2 of 6 proxy items (R3-7, R3-8) are MAJOR labels graded minor. That label noise of about 2 is large against a bar of 3.

**Is there an in-theme lever that acts on blocking-fix chains without relabelling or hiding?** I went through the four parts as A did and agree with A's verdict, with one correction to A's candidate.

- **Computed surface: no.** The four blockers sit on new words that blocking fixes wrote. Narrowing the surface further means not reviewing fix text, which is hiding. I also checked that the surface would have changed nothing for review 3: every SPEC3 line named in the origin column of all 10 review-3 findings falls in a changed-line list of `disposition-round2.md`.
- **Anchor checker: no.** Each blocker anchors on changed words and cites other lines as evidence. Rejecting those would be hiding.
- **Fix gate: no reduction.** All four parent fixes were mapped blocking fixes. A stricter gate (budget or footprint) only pushes revisers to under-fix, which moves a finding from new to open prior (A-003) and counts the same in the proxy.
- **Ledger: detection only.** It can flag, before fix 2, that a review-2 blocker sits on text a round-1 blocking fix wrote (recurrence), and it prints the chain. In flg-r1 this would have fired on all 4. Any rule that downgrades, defers or excludes recurrence blockers is relabelling and is ruled out. I withdraw B's halt-on-chain-length as a rule (see response to round2-A, item 3); it is a report line.

**A's candidate, the cross-reference closure aid** (the fix gate prints, for each reviser hunk, the unchanged lines sharing an identifier token with it). A estimated two of four flg-r1 blockers have that shape. I tested the line pairs the review names, counting WC/AC/SA/FR/D ids and `--flag` tokens on the spec:

| Blocker | Conflict pair | Result |
|---|---|---|
| R3-1 | SPEC3:67 and 188 | Share `WC-7`, but both lines were changed by the same fix (R2-2), so closure adds nothing the surface does not already show |
| R3-2 | `git status` behaviour | External fact; no identifier link |
| R3-3 | SPEC3:162 (changed) and 200 (unchanged) | Line 162 does not name `AC-1.2`, which appears only on line 200; they share `WC-4` and `P1`, and `WC-4` occurs on 14 lines, so the real hit would be one of 14 |
| R3-4 | SPEC3:64 and 66 | No shared identifier (64 carries `WC-4`, `WC-5`; 66 carries `WC-6`, `--retry-of`); the link is conceptual ("fresh dir" versus retry) |

Ceiling on flg-r1: no clean hit, one hit buried among 14 lines, out of four. The reviser had also already worked by root cause with explicit knock-on lists and still missed these. So the aid's expected effect is about 0 to 1 blockers, reached only if the reviser reads a noisy list. It would need its own ablation arm and must not count toward the diffgate result.

**Honest answer: no mechanism inside the diffgate theme lowers fix-induced blockers without relabelling or hiding real defects.** What the theme can legitimately do is make the result interpretable: print chains, report chain-length distribution, apply the re-based F1, report label and blocking counts, and apply C's spread check so a single swing of the rate (0.17 versus 1.0 at n=2) is not read as an effect. The lever F1 points to is fix quality, which is outside this theme. One consequence for delivery, in the refactorer's minimal-risk spirit: ship Stage A (inert script, tests, skill) on its own merits, since the self-computed diff, checked origin tags and checked counts do not depend on the bar; run Stage B as the experiment; gate Stage C (fold into `spec-panel.md`) on the pre-registered result classes (bar met; bar missed with F1; bar missed without F1), not on the bar alone. If the owner wants a decision-grade answer on convergence, a third replicate per arm buys more than any added machinery.

## New evidence

1. **The scope gate would have changed none of flg-r1's review-3 findings.** I cross-checked each SPEC3 line in the origin column (67, 188, 183, 189, 88-90, 162, 64, 102-128, 70, 107, 93, 112) against the changed-line lists in `disposition-round2.md`: all fall inside changed lines. The computed surface would agree with the reviewers' own origin tags. For this run diffgate's value is verification of the tag, not a smaller count.
2. **The fix gate has very little to remove in flg-r1.** Lines touched only by minor rows in fix 2 are 62, 70, 107, 202 and 234, five of the 60 changed lines (60 per `disposition-round2.md` section 3; the blocking-row ranges such as 102-128 make this an approximate figure). The flg-r2 replay removed 3 of 5 review-3 items; flg-r1 removes 1 of 6.
3. **Closure-list ceiling measured** (table above): zero clean hits and one buried hit on four blockers.
4. **Label noise.** Two of six proxy items (R3-7, R3-8) are MAJOR labels that 427 graded minor.
5. **Revisers already produce a fix map.** The flg-r1 reviser tagged every changed passage with `R2-N` (except a pure reorder) and listed knock-on edits per row. An explicit map is a by-product; pre-filling it from inline tags makes B's map nearly free.
6. **Variance between replicates is large.** flg-r1 fix 2: 4 of 4 blocking fixes produced a blocker. I verified this one; the 1-of-6 flg-r2 figure is A's and B's round-1 number and I did not re-read flg-r2 this round. At n=2 the within-arm spread swallows any plausible effect, so C's spread check should be part of the pre-registered pass rule.
7. **Test addition.** Add an flg-r1-shaped fixture to `tests/skills/fixtures/diffgate/`: four mapped blocking fixes, four new blockers on those hunks, one MAJOR label graded minor on a shared line, one minor-only line. Expected outputs: the gate allows all four fix hunks and drops the minor-only line, chains of length 3 print, F1 fires, label proxy 5 and blocking count 4. This pins the very case this round turned up, at no model cost.

## Shared assumptions (A-001..A-006: ACCEPT|REJECT|QUALIFY: one-line reason, updated)

- A-001: QUALIFY: one scripted command per exit code leaves little to improvise, but compliance is assumed; record recovery-path compliance per replicate as a validity input.
- A-002: QUALIFY: flg-r1 shows narrowing removes noise (R3-7) but not blockers (10 of 10 findings were already on changed text); record hunks per surface and findings per hunk before attributing any gain to density.
- A-003: QUALIFY: all four flg-r1 parent fixes were mapped, so under-fixing was not the issue there, but a stricter gate can only move counts from new to open prior; report open priors and `declined` lines apart from new findings.
- A-004: REJECT: the added brief lines and the `fixcheck` line are prose that can change reviser behaviour without the script; claim the combined treatment or add a briefs-only arm.
- A-005: QUALIFY: B's one-line grammar (now with JSON-quoted anchors and no verdict line) is a smaller review-1 tax than before; check review-1 blocker counts against Arm B's 13 to 17 as a validity gate.
- A-006: REJECT: now answered by evidence; flg-r2 composition does not hold for flg-r1 (all 4 blockers sit on blocking-fix chains), so any forecast resting on flg-r2 alone is unsupported.

## Per-point positions (updated)

| Point | Superior approach (A, B, C, merge like A+B, or tie) | One-line reason |
|---|---|---|
| S-001 | C | Separate test and acceptance sections; all three advocates now prefer C or call it a tie. |
| S-002 | C | Tiered P0/P1 tests with negative cases are easiest to run; fold A's 16 script cases and the flg-r1-shaped fixture into them. |
| S-003 | C | Implementation acceptance apart from experiment success; move C's criterion 15 to the experiment gate. |
| S-004 | A+C | A's nine verbatim bullets as single physical lines, plus C's removal of the line-220 read as a tenth listed change. |
| S-005 | A+B | A's signatures fix the interfaces; B's named constants and per-part line budget bound the size (with B's cut constants gone). |
| S-006 | A+B | One exit table with a who-acts column; all three advocates accept it. |
| S-007 | B+C | flg-r1 showed dense citations did not protect a causal story; UNVERIFIED tags, a replay and PROPOSED labels are the better discipline. |
| S-008 | A+B | A's bullet-keyed residual-risk table plus B's extra concerns such as step order. |
| S-009 | A+C | A's residual column plus C's separate cost envelope. |
| S-010 | B+C | B flags experiment blockers; C gives every question a default. |
| C-001 | A+B | The worker that owns each step runs it, `begin` re-runs the fix gate, the coordinator only reads `status`; C's confirmation checks presence, not truth. |
| C-002 | A | The verified installer analysis decides the name (`sc-diffgate`, called by path); add C's transcript check of that call. |
| C-003 | A+B | B's four-subcommand set (`final` folded into `close`/`check`) with A's rule that `begin` re-runs the gate. |
| C-004 | A+C | One JSON object per call with separate verdict and execution-success fields is easier to test; I withdraw the key:value preference. |
| C-005 | B+C | One meaning per code in B's table, plus C's rule that a valid FAIL exits 0. |
| C-006 | A+B | A's JSON-quoted values (no `[[ ]]` limit) carrying B's `via=`, `cites=`, `declined` fields; C's strict JSON draft is the largest review-1 change. |
| C-007 | tie | File layout does not change behaviour; flat files are smaller, per-round folders are tidier. |
| C-008 | A+B | Token-level eligibility (A) with block-level hunk ids for ownership (B); no `renumber` rule needed. |
| C-009 | A | `H<k>.<n>` never repeats across reviews and is shared by the gate and the next surface; a digest adds nothing the ledger hash lacks. |
| C-010 | A+C | A's token-overlap rule C5 plus C's validation of every claimed anchor; B's hard versus soft split stays. |
| C-011 | A+B+C | Demote or degrade anchor failures, stop only on structure, never print a clean PASS when blocking-grade findings were degraded or deferred. |
| C-012 | A+B | An unanchored finding is a free deferral; C's reject spends the one repair on a legal outcome. |
| C-013 | B | Quote-checked `via=`; over-cap findings deferred but counted in the proxy and shown in the scoped-PASS line (this answers C's worry). |
| C-014 | B | Explicit map with `declined`, pre-filled from inline tags; footprints would not have stopped flg-r1's chains (R2-2 and R2-3 were 3-line fixes). |
| C-015 | A+B | Report `bytes_by_id` and hunks per id, no gate and no threshold; I drop B's budget. |
| C-016 | tie | All three reject a severity ceiling; flg-r1 makes it the obvious relabelling trap. |
| C-017 | B+C | B's `seen: rounds 2,3` and the no-cite rule for deferred ids, plus C's scoped-PASS sentence. |
| C-018 | A+C | The reviewer writes no verdict and the script supplies it; B now agrees. |
| C-019 | A | Presence of an outcome, no paddable constant; C's confirmation is presence-only by C's own words and adds a coordinator step. |
| C-020 | A | No severity field on carried status lines makes upward drift impossible by grammar. |
| C-021 | tie | All three keep minors away from the reviser; in flg-r1 this removes only R3-7. |
| C-022 | A+B | A word-identical reflow is not a hunk; B's `coverage:` warning flags a degenerate surface. |
| C-023 | B | flg-r1 bears out a bar miss: 4 of 4 review-3 blockers sit on blocking fixes; A withdrew its 60%. |
| C-024 | tie | All forecasts clear 44.4%; flg-r1 Arm B is already at 27.8%. |
| C-025 | A+B+C | B's F1 re-based on the bar as the primary diagnosis, A's blindness and demotion conditions, C's spread check. |
| C-026 | A+B | The all-discovered count by reviewer label gates the bar; C concedes. |
| C-027 | C | The most complete accounting (Read-backs, correction turns); A and B estimates omit some of it. |
| C-028 | A+B+C | A's hash of the untouched `spec-panel.md` and no `--force`, B's `--expect-round`, C's installed-file hashes and transcript check. |
| C-029 | B | Dropping the 427 flags from the variant's Usage is simplest; ignoring (A) keeps dead text and verifying (C) adds code. |
| C-030 | A+B+C | A's two existing-test edits, B's fixtures and drift guard (with the `## Tool Coordination` exemption), C's isolated-HOME install test. |
| C-031 | A+B | Verbatim `## Unattended mode` with the name swapped stays pinnable against the parent; registered through A's `UNATTENDED_VARIANTS`. |
| C-032 | A+B | No plugin mirror is needed (parity test pins only README-listed commands); a separate design note keeps 427's doc historical. |
| C-033 | A | A fresh-review blindness audit, misses classified by ledger history; all three now agree. |
| C-034 | A+C | A's `PROFILES` seam toward rf-qa, with C's limits on replacing the `/sc:implement` FINAL review or weakening rf-qa guards. |
| C-035 | A+C | A's ledger replay plus C's exclusive-create lock; size limits and symlink refusal are cut as over-scope. |
| X-001 | A+B | Worker-run steps with mutual locks; the coordinator is also a prose follower. |
| X-002 | A+B+C | Same as C-011: stop only on structure, degrade the rest, no clean PASS with degraded blocking-grade findings. |
| X-003 | A+B | A word-identical reflow carries nothing to review; edited words inside it still surface. |
| X-004 | A+B | Same as C-012. |
| X-005 | B | `via=` covers the case it exists for; flg-r1 had 0 of 10 findings needing it, so it is a narrow escape, not a driver. |
| X-006 | A+C | Same as C-018. |
| X-007 | B | flg-r1 supports about 0.2 for both replicates meeting the bar; A's revised forecast now matches. |
| X-008 | A+B | Same as C-026; deferred and degraded findings count by label. |
| X-009 | A+B | Whitespace-only edits are not hunks and need no owner; C's rule contradicts its own mask. |
| X-010 | B | Same as C-029. |
| X-011 | A+B | The parity test pins only README-listed commands, so a mirror is unneeded scope. |
| X-012 | A | Only A plans the `_POST_REFRESH_ADDITIONS` edit; B and C concede. |
| X-013 | A+B | No gate, bytes reported only; flg-r1's 3-line fixes show a size gate would not have helped. |
| X-014 | A+B | A name that does not match the command, called by path; C's Skill activation is a legitimate alternative, not an error. |
| X-015 | C | A concedes; remove the line-220 read. |
| X-016 | C | Same fix; B's drift guard exempts `## Tool Coordination`. |
| X-017 | A | Register the variant through `UNATTENDED_VARIANTS`; a verbatim section keeps parity with the parent. |
| X-018 | tie | B conceded the 13 versus 14 slip; it has no design effect. |
