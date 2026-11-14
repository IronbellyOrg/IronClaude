# Round 1 advocate statement: Variant 3 (reviewer 3, refactorer, calibrated C 0.71)

Aliases: TL = task file; ADD = design-addendum.md; DES = docs/designs/orchestrator-mode.md; STYLE = src/superclaude/output-styles/pragmatic.md. Every line cited below was Read in this round.

## Position summary

V3 is the only card that tests whether the 82 revised bodies agree with the addendum they implement. It found the paraphrase drift in 7.10 and the false sentence repeated 59 times, and it gave a verdict on all ten Tier-1 findings. V3 is not the strongest card on severity. V2 found the two defects that make a correct run fail, and V3 confirmed those same defects as "outside my slice" without grading them. I concede both HIGH findings to V2 and lower my own R3-F1 to LOW.

## Steelman of Variant 1

V1 audited the widest surface: 111 matrix rows, with about 45 read from source. It found the exact-8 defect on its own (R1-F3, TL:1293, 1363, 1391). It also found two plan-specificity gaps that V2 and V3 did not grade. First, 7.10 names no carrier for "separate direct execution authorization" (TL:1210). Second, the Phase 7 preamble (TL:1143) tells the executor to reset Doing and clear `blocker_reason`, while 7.10 reuses "Branch 1/2" with a different meaning.

V1 also traced a chain across items. A 7.10 omission can make 11.4 fail, and 11.4 then has no named repair step. That chain is a real cross-item observation.

V1 is also right that 7.20's style checks have no command or expected value (U-001), even though TL:1295 says each check is "decided by the expected value written beside its command".

## Steelman of Variant 2

V2 reports the highest-value class of finding for a pre-execution audit: a check that rejects what the plan's own Action produces. Both are certain once the facts are read.

- Item 13.1: TL:2265 says "copy the DESIGN text", and DES:716 begins "The coordinator runs `/sc:sweep` on every wake". TL:2267 still greps "The coordinator sweeps on every wake...". I read TL:2267 and TL:2268-2270 and found no failure branch or repair step for this check.
- Exact-8: the 7.17 branch files match the `OQ-*-decision.md` glob once resolved (TL:1272, 1293).

V2 has zero failed citations, the highest calibrated C (0.86), and a three-case truth table for the count fix. It refused to inflate F9 and F10. Its severities follow the brief definition literally, and that is what a merge needs.

## Strengths claimed (V3)

1. **Full Tier-1 coverage.** V3 gave a verdict on all ten Tier-1 findings. V1 judged five and V2 judged four. F6 and F8 were confirmed only by V3 (A-010). That includes the `install_user_setup.py:140` and `pragmatic-subagent.js:7` evidence.
2. **R3-F2 is real, and the omission list is verified.** I grepped TL:1209-1213. 7.10 contains no "same message", no table-request exclusion and no "formatting never authorizes". TL:1973 (11.3) has the same-message clause and lacks "formatting never". TL:1980 (11.4) requires assertions against the actual style for "direct operative assignment plus separate invocation" and "role/table request alone". So 7.10 omits two cases that 11.4 pins against the style it produces. The calibrator confirmed the quotations.
3. **R3-F1 is factually right.** `grep -c 'not an implemented exception'` returns 59, matching V3's count. After 7.10 the sentence is false for 58 items. Item 11.5 (TL:1986) says both "unqualified table mandate, not an implemented exception" and "actual canonical style" in one Context line.
4. **R3-F3 is a real pattern break.** `sha256sum` appears only at TL:2614, 2642, 2705 and 2733. The fixers that may edit both DESIGN and STYLE (7.30, 7.34) have only the prose ban at TL:1363, "Never change revision authority/design append/decision choice". The calibrator accepts the inconsistency and calls the proposed verifier weak.
5. **The remedy removes a class of defect.** ADD:27 says "The future style definition is the common rule above." Copying ADD:13-21 verbatim means 7.10 and 11.3 cannot drift from each other. That is more durable than V1's single-clause patch (R1-F4).
6. **Citation hygiene.** 19 citations were checked and none failed. V1 has three failures.

## Weaknesses identified in the other variants

1. **V1 under-grades the exact-8 defect.** R1-F3 is MEDIUM on the claim that the cursor branch is "likely" because DES names `page.nextCursor`. DES:760 calls that field UNVERIFIED (quoted in X-001). The defect is certain whenever the branch fires, so the brief's HIGH definition applies.
2. **V1's TL:353 link does not hold.** R1-F1 ties the 11.4 stall to a "retry-restore stop" at TL:353. The stop is the tail of TL:1210: "Before any original-start retry restore that would erase the design append, STOP and escalate preservation". It fires on an original-start restore, not on an in-place re-run. TL:1295 sets the convention: "return to the owning item and re-run this item". V1's own Notes also call the stop "by design, not a defect". V1 is internally inconsistent here.
3. **V1 labels R1-F2 "gate-bypass" but 7.10 fails closed.** TL:1210 Branch 1 reads "keep Blocked ... STOP without ticking". TL:1213 reads "This item cannot be marked as done until the actions are completed in their entirety". The real gap is specificity (no named carrier), not a bypass.
4. **V1 treats ticking 7.10 without an edit (R1-F5) as plausible.** TL:1213 blocks that, so R1-F5 is a reading-order nuisance. V1 rated it LOW itself.
5. **V2's "0 gaps" is misleading.** V2 reports 40 of 40 adherent and 0 missing deliveries, then reports three defects. Its slice is parsed requirement rows only. V2 is silent on 7.10's omissions, 11.4's repair wording, the authorization carrier and the 59-item sentence. The 0.86 weight therefore reflects reliability, not breadth.
6. **V2's R2-F3 does not affect execution.** It is an audit-recall defect in `coverage-matrix.yaml` (items 8.12 and 10.5 already deliver the requirement).
7. **V2's confidence of 0.99 on R2-F1 is high for a conditional defect.** The condition is that a 7.17 branch fires.

## Concessions

1. **V2's two HIGH findings are correct HIGH.** Under the brief definition (a correct run fails), 13.1 fails unconditionally: following the Action fails the Verification, and the stale text also fails the routing-rows lens (TL:2342). The exact-8 check fails whenever the branch fires. I confirmed both as "outside my slice" and never graded them. Having both in my slice and scoring 0 HIGH was a real miss.
2. **R3-F2's prediction is overstated.** TL:1212 tells the executor to compare against the addendum and ADD:27 makes the rule common. TL:1980 pins semantic cases, not a whitespace-normalized substring. The omissions are real, but paraphrases need not fail 11.4. My "will not match" claim was too strong, and X-007's LOW-to-MEDIUM stands.
3. **R3-F1 is LOW, not MEDIUM.** The sentence is false in 58 items after 7.10. But TL:1362, 1292 and 2341 each also give the addendum and the canonical style as inputs. No downstream item orders a revert; the 7.30 and 7.34 fixers act only on listed findings. The remaining risk is a false BLOCKING finding from a lens that trusts the label over the disk. It is a text risk, not an observed event, and I do not defend MEDIUM. The fix is cheap (an in-place rewrite that keeps line counts).
4. **F10 is not a defect.** The eighth mention at STYLE:25 is a length-budget sentence, which ADD:27 preserves. V2 is right to refute it as a defect.
5. **R3-F3's verifier is weak.** A heading count proves presence, not unchanged contents. The sha256 pattern break stands but is LOW.
6. **Coverage "45 of 45" is a reported count with no row ledger.** The deviation-class field is free-form (calibrated 0.25). The bare `BUILD-REQUEST.md:55` alias was ambiguous.
7. **V1's R1-F2 and V2's truth-table acceptance design (U-004) are better than my equivalents** where they overlap.

## Shared-assumption responses

- **A-001 ACCEPT.** The plan is a sequential checklist, and every sequencing finding assumes checklist order.
- **A-002 ACCEPT.** The precondition is "the branch fires", never "likely" (DES:760).
- **A-003 QUALIFY.** Re-running an owning item is the plan convention (TL:1295; TL:458, 632, 848 per the diff analysis). But 11.4 (TL:1982) omits the words "re-run this item", so the convention is not stated where it is needed.
- **A-004 ACCEPT.** Re-grade by the brief definition before weighting by C.
- **A-005 ACCEPT.** I re-read the cited lines and they hold. V1's TL:353 does not support its claim.
- **A-006 ACCEPT.** A check that contradicts its own Action is a defect regardless of executor quality (13.1).
- **A-007 ACCEPT.** The static assertions prove the text contract only (ADD:37).
- **A-008 QUALIFY.** The guard is mechanical in 14.x (`sha256sum` at TL:2614, 2642, 2705, 2733) and prose-only in 7.30/7.34 (TL:1363). That is a LOW pattern gap, not evidence of change.
- **A-009 QUALIFY.** The reports exist on disk, but 7.10 (TL:1209-1210) does not name them or the authorization carrier. The gap is specificity, and 7.10 fails closed.
- **A-010 QUALIFY.** F6 and F8 are single-source, but both are LOW, and the cited files are greppable. Single-source confirmation is enough at LOW.

## Point-by-point positions

Severity: H = a correct run fails or a required check is lost; M = real impact, workaround exists; L = minor.

| Point | My position | Winner | Conf. |
|---|---|---|---|
| S-001 slice | V1 widest, V3 targeted, V2 narrow. Not decisive | none | 60% |
| S-004 calibration | Weight by C: V2 0.86 over V3 0.71 over V1 0.69 | V2 | 80% |
| S-006 Tier-1 verdicts | V3 complete, but its confirmations of F3 and F4 are thin | V3 | 70% |
| S-007 gap definition | Tallies are not comparable across the cards | none | 65% |
| S-008 preservation depth | V3 counted checkboxes and the end line, but did not byte-compare. V1 took the matrix as evidence | V3 | 60% |
| C-001 / X-001 exact-8 | H, conditional on the branch firing. Decision is right | V2 | 85% |
| C-002 / X-002 13.1 | H, unconditional. Decision is right | V2 | 90% |
| C-003 / X-003 11.4 repair | Stall is inferred and the TL:353 link fails. LOW-to-MEDIUM; fix is one sentence ("re-run this item") | split V1/V3 | 70% |
| C-004 / X-008 authorization | Fails closed. Relabel "missing", LOW-to-MEDIUM. Decision is right | V1 | 75% |
| C-005 / X-007 7.10 omissions | Omissions are real. Failure is not inevitable. LOW-to-MEDIUM. Verbatim copy is the sturdier remedy | V3 on remedy | 70% |
| C-006 / X-004 preamble | LOW. TL:1213 blocks ticking without an edit | V1 | 75% |
| C-007 / X-005 severity-module timing | LOW optional. No missing requirement | V1/V2 | 70% |
| C-008 / X-006 "eighth mention" | Cosmetic. As a defect it is refuted | V2 | 80% |
| C-009 matrix completeness | LOW, does not affect execution | V2 | 70% |
| C-010 install follow-up | LOW. V3 alone drew a follow-up | V3 | 65% |
| C-011 ordering | Order is sound | none | 80% |
| U-001 (V1) 7.20 style checks | Valuable, LOW-to-MEDIUM | V1 | 65% |
| U-004 (V2) three-set acceptance | Best verifier offered | V2 | 80% |
| U-005 (V3) 59-item sentence | LOW (conceded down from the diff analysis's Medium) | V3 on fact | 65% |
| U-006 (V3) sha256 pattern | LOW. Pattern gap only | V3 | 60% |
| U-007 (V3) "three" entries | LOW, pre-existing | V3 | 80% |
| U-008 (V3) stale GQ-63 wording | LOW, single-source | V3 | 65% |
| U-009 to U-011 (V3) | LOW notes | V3 | 60% |
