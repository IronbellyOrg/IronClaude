# Round 1 advocacy: Variant 1 (reviewer 1, analyzer, calibrated C 0.69)

TL = `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`; ADD = revision `design-addendum.md`; BR = revision `BUILD-REQUEST.md`; DES = `docs/designs/orchestrator-mode.md`. Every line cited below I read in this round.

## Position summary

V1 is the only card that traces how the revised items hand work to each other (7.10, 7.17, 7.20, 11.4, 7.30/7.34) and it found a real defect (exact-8 check) plus four smaller specificity gaps. It under-rated the exact-8 check (V2's HIGH-conditional is right), over-labelled two findings (F2 "gate-bypass", F5 "tick without edit"), and had three failed citations. The card should be merged as the source of the 11.4 repair-wording, the 7.10 carrier gap and the preamble-reconciliation gap, all at LOW to MEDIUM, with V2 owning severity on the two checks that reject correct runs and V3 owning the 7.10 wording fix.

## Steelman of Variant 2

V2 applied the brief's own severity rule ("HIGH = a correct run fails or a required check is lost", reviewer brief line 74) literally and consistently. Its two HIGH findings are both checks that fail while the executor follows the plan's own Action. I verified both. 7.20 requires "(expect 8)" over `OQ-*-decision.md` (TL:1293, repeated TL:1363, TL:1391), while 7.17 writes OQ-17/OQ-18 files (TL:1270) that become `status: RESOLVED` on approval or refusal (TL:1272), so a correct run counts 9 or 10 and the 7.30/7.34 fixers re-run the same literal, so no in-plan step can make it pass. For 13.1, TL:2265 says "copy the DESIGN text", DES:716 reads "The coordinator runs `/sc:sweep` on every wake...", and TL:2267 still greps "The coordinator sweeps on every wake...". Following the Action fails the Verification. V2 also wrote a three-case acceptance test for the fix, avoided any likelihood claim, and its calibration is clean (0 failed citations of 18). The stability of its evidence is why it got C 0.86. It stays in its lane: it says nothing it did not verify.

## Steelman of Variant 3

V3 is the most complete reader of the addendum. It compared 7.10's Action (TL:1210) with ADD:13-21 sentence by sentence and found five omissions, not one: table-omission request and the word "coordinator" (ADD:15), "loaded skill and style ... do not themselves assign" (ADD:15), the same-message case (ADD:17), "Formatting never authorizes advice prohibited by the sweep skill" (ADD:19), and the unchanged-things list (ADD:21). ADD:27 says "The future style definition is the common rule above", so a paraphrase is a drift risk, and V3's fix (copy ADD:13-21 verbatim, add one substring assertion to 11.4) removes the whole class instead of patching one clause. Its 59-item finding is also real: "not an implemented exception" appears in 59 item bodies (TL:1209, 1292, 1986, 2049 among them), and after 7.10 runs that sentence is false for 58 of them. TL:1986 even contradicts itself in one line (stale anchor plus "actual canonical style"). It checked all ten Tier-1 findings, proposed a mechanical hash guard for 7.30/7.34, and corrected a pre-existing "three entries" count. Its weakness is that its two MEDIUMs are risks, not failures.

## Strengths claimed

1. **Exact-8 defect, independently found and fix-ready.** R1-F3 is the strongest finding the calibrator verified. I add two facts V2 did not: the same glob is repeated as the input of the lens items 7.21 onward (TL:1299, 1306, 1313, ... 1348, 1369, 1376, 1397, 1404 all say "OQ-1 to OQ-8"), so a correct fix must touch more than three lines, and TL:1425 (item 8.1) already uses a named eight-file loop, so the repair has an in-plan precedent.
2. **Order and ripple checking.** My Notes confirm 7.10 precedes 7.13, 8.12, 11.3, 11.4 and that no Phase 11 lens input names a later-phase artifact. V2 and V3 did not check this. Diff C-011 treats it as shared, but only V1 states it.
3. **Specificity gap in 7.10's authority evidence (R1-F2).** TL:1209 lists `qa/research-gate-cycle1.md` and the research files, but not the fresh structural, alignment or QA reports. Those exist on disk (Glob: `qa/qa-task-validation-consolidated.md`, `qa/qa-task-research-alignment-report.md`, `qa/qa-qualitative-operational-report.md`, `reflect/pre/`). 7.20 must "independently evidence" them (TL:1293), and BR:55 puts execution authorization with the user. No file carries that authorization. Nobody else saw this.
4. **Phase 7 preamble conflict (R1-F5).** TL:1143 says Branch 2 "resets the task `status` to 'Doing' and clears `blocker_reason`" for every HALT item, while 7.10 reuses "Branch 1/2" with a stricter meaning (TL:1210, 1213). The only reconciliation is in the appended note. Real, LOW.
5. **Unique verified extras.** U-001 (7.20's style checks have no command or expected value despite TL:1295 "each decided by the expected value written beside its command") and U-003 (no existing test pins the "No exceptions" table text) were confirmed by the diff analysis.
6. **Honest uncertainty marking.** I tagged the two behaviours I could not verify as [INFERRED], and the Notes say the TL:353-class stop is "an accepted limitation per BUILD-REQUEST.md:26". The calibrator confirmed 23 of 26 citations.

## Weaknesses identified in the other variants

1. **V2 has narrow reach by design.** 40 of 111 rows, three findings, and no view of the 7.10-to-11.4 flow. Its "0 missing deliveries" is a tally over a slice that, as its own Notes admit, held "parsed requirements only". It cannot find a defect that lives between items.
2. **V2's R2-F2 is outside this revision.** 13.1 is not among the revised bodies (diff X-002 says so). It is a real HIGH defect, but a pre-existing one, and a merge must not present it as caused by this revision.
3. **V2's F9/F10 refutations are correct on classification but dismiss V3's accurate facts.** STYLE:25 is an eighth table mention (diff X-006), and 7.10 does not run the severity modules. Neither is a defect, but "refuted" overstates.
4. **V3 offers no severity on the defects that matter most.** It "confirmed, outside my slice" F3 and F4 (the HIGH-conditional and the carrier gap) without a finding, and its calibrated C (0.71) rests on 19 checks only.
5. **V3's R3-F1 is a risk, not an event.** The sentence is false only to a reader who ignores "actual canonical style" in the same Context line, and lens inputs list the actual style. MEDIUM is a stretch; LOW-MEDIUM. R3-F3's proposed heading-count check proves heading presence, not unchanged content (calibrator).
6. **V3's R3-F2 fix overreaches.** Verbatim copy of ADD:13-21 into three items makes three copies of the rule; a substring assertion in 11.4 also needs whitespace normalisation that the plan does not define. The remedy is sound but costs more than the one-clause patch for the single clause 11.4 actually pins.

## Concessions

1. **Three failed citations.** (a) TL:353 is the Output line of item 2.16 (`qa/r3-b1/qa-spec-fidelity-report.md`), not a preservation stop. The real source is the last sentence of TL:1210 ("Before any original-start retry restore that would erase the design append, STOP and escalate preservation") and BR:26. (b) My quote "sign-off or separate direct execution authorization is absent" sits at TL:1210 (Action, Branch 1); TL:1209 is Context. (c) The OQ-17 filename quote is at TL:1270 and TL:1273; TL:1272 holds "sets `status: RESOLVED`", which is the text I needed and is correct.
2. **R1-F3 severity.** MEDIUM understates it. By the brief definition a correct branch run fails a required check, with no in-plan repair. HIGH-conditional, as V2 and diff X-001 say.
3. **"The cursor branch is likely."** Unsupported. DES:760 calls `page.nextCursor` "UNVERIFIED until step 1.0a item 3". I retract the likelihood and keep the conditional.
4. **R1-F2 label.** "Gate-bypass" is wrong. 7.10 Branch 1 fails closed ("keep Blocked ... STOP without ticking", TL:1210) and TL:1213 forbids completion. It is a missing carrier. Relabel "missing", LOW to MEDIUM.
5. **R1-F5 overclaim.** "Could tick 7.10 without any edit" is blocked by TL:1213 ("cannot be marked as done until the actions are completed"). Residual is a reading-order ambiguity, LOW.
6. **R1-F1 overclaim.** "No executable repair step" is too strong. Precedents (TL:458, 632, 848, 1008, 1295) say "fix in the owning item and re-run this item", and 11.14 (TL:2050) lets a fixer edit the style, skill and test files. 11.4 only omits the "re-run this item" words. LOW to MEDIUM.
7. **R1-F4 and R3-F2.** V3 found four more omissions than I did and a better remedy.

## Shared-assumption responses

- **A-001** ACCEPT. The plan is a checklist; my ordering notes and the "OQ-1..OQ-6 only today" observation (Glob) depend on 7.x creating OQ-7 and OQ-8 before 7.20 (names at TL:1425).
- **A-002** ACCEPT. The precondition is "the branch fires". I withdraw "likely" (DES:760).
- **A-003** QUALIFY. A ticked item is not strictly unrepeatable: TL:1295 and TL:458 re-run owning items. But 11.4 (TL:1982) omits that wording, and its "stop incomplete" ends the run before 11.14, so the contradiction is partial and my [INFERRED] tag was right.
- **A-004** ACCEPT. Severity must be re-graded by the brief definition before weighting by C. By that rule my F3 MEDIUM becomes HIGH-conditional.
- **A-005** ACCEPT. My three failures are listed above; re-read before citing.
- **A-006** ACCEPT. TL:2265 vs TL:2267 is a defect even for a perfect executor. The same logic applies to TL:1293.
- **A-007** ACCEPT. ADD:37 states the static-only limit.
- **A-008** QUALIFY. Authority files stay unchanged, but 7.30/7.34 carry only the prose ban (TL:1363, 1391) while 14.x fixers add sha256. The 11.14 fixer text (TL:2050) also bans editing authority/DESIGN. The difference is real, LOW.
- **A-009** QUALIFY. The reports exist now (Glob above), so the lens can find them; the gap is that 7.10 names none of them and no file carries the authorization. This is a specificity fix, not an existence risk.
- **A-010** ACCEPT. F6 and F8 are single-source (V3) confirmations; I would still hold them LOW.

## Point-by-point positions

| Diff point | Position | Right winner | Confidence |
|---|---|---|---|
| C-001 / X-001 | Concede: HIGH-conditional. V2 right on severity and framing. V1 adds the repeated lens glob and the TL:1425 precedent | V2 | 90% |
| C-002 / X-002 | Not mine. I verified TL:2265/2267 vs DES:716: HIGH, pre-existing | V2 | 90% |
| C-003 / X-003 | Decision correct: stall inferred, not proven; TL:353 link fails. Real but small: baseline had in-place repair, 11.4 omits "re-run this item". LOW | V1 (partly), severity LOW | 70% |
| C-004 / X-008 | Relabel "missing". 7.10 fails closed. Specificity gap real (reports exist but unnamed). LOW to MEDIUM | V1 (only finder) | 65% |
| C-005 / X-007 | V3's verbatim-copy fix is sturdier; omission real, mismatch not inevitable. LOW to MEDIUM | V3 | 75% |
| C-006 / X-004 | Agree LOW; TL:1213 blocks ticking | V1 (LOW) | 75% |
| C-007 / X-005 | No missing requirement (ADD:25, ADD:31); optional only. LOW | V2 on class, V1 on tone | 70% |
| C-008 / X-006 | Both facts true; refuted as defect. I did not judge | V2 | 70% |
| C-009 | V2's R2-F3 is an audit-recall gap I did not check (DES:645 not read by me). Accept as LOW | V2 | 60% |
| C-010 | Notes only. TL:1212 already says make sync-dev cannot activate HOME style, so follow-up is optional. LOW | V3 (facts), severity LOW | 65% |
| C-011 | Order/QA structure retained; shared, no conflict | none | 80% |
| U-001, U-003 | Mine, confirmed by the diff analysis; keep at LOW to MEDIUM | V1 | 80% |
| U-005 | V3 right the risk exists; 59 items; I rate LOW to MEDIUM because the same Context line says "actual canonical style" | V3 | 65% |
| U-006 | V3 right that 7.30/7.34 are prose-only (TL:1363, 1391); LOW | V3 | 70% |
| S-006 | V1's "not in the excerpt" for F5 while R1-F4 is that defect is a bookkeeping flaw | V3 | 70% |
