# Round 2 rebuttal: Variant 3 (reviewer 3, refactorer, calibrated C 0.71)

Aliases: TL = task file; ADD = design-addendum.md; BR = revision BUILD-REQUEST.md; DES = docs/designs/orchestrator-mode.md; STYLE = src/superclaude/output-styles/pragmatic.md. Every line cited was Read or grepped this round.

## 1. Criticisms of V3 and my answers

| # | Criticism (source) | Answer |
|---|---|---|
| a | Verbatim copy of ADD:13-21 pulls a meta sentence into the live style (V1) | Concede in part. ADD:21 sentence 4 reads "Eligibility is a proposed loaded-instruction contract, not a runtime detector, identity probe, environment flag or evidence that any actual session has coordinator assignment." "Proposed" is planning status and is false inside a delivered style. ADD:13, 15, 17 and 19 contain no planning language: they are the rule itself, and ADD:27 says "The future style definition is the common rule above". The range was too wide; the remedy is not wrong. |
| b | "Some sentences are planning-only" (V2) | Concede for ADD:21 sentence 4 only. V2 is right that the substance (no runtime detector, identity probe, environment flag or assignment grant) should be restated in the present tense, and that ADD:21 sentences 1-3 are operative boundaries. |
| c | Pointer-only or whole-block copy conflicts with BR:41 and BR:20 (V1) | Not my position. BR:20 asks for line-stable edits where Context/Action stay one physical line. Adding five sentences into the 7.10 Action keeps that. |
| d | A new substring assertion in 11.4 is unnecessary (V1, V2) | Concede. TL:1980 pins semantic cases against the actual style, and TL:1212 already requires comparing "all excluded cases against the addendum". |
| e | R3-F1 stale anchor should be LOW (V2) | Agree; I had already lowered it. See the fix location below. |
| f | "Will not match 11.4" overstated; 59-item severity; R3-F3 verifier weak; "45 of 45" has no row ledger; F10 not a defect; R2-F3 irrelevant | All conceded in Round 1 or restated here. |
| g | Single-source F6/F8 (A-010) | F8 downgraded further: ADD:39 says the revision "authorizes no HOME install/update or activation", so an install follow-up is out of scope. Informational only. |

## 2. Updated assessment of V1 and V2

V1: after its concessions its remaining value is the authorization-carrier gap, the 11.4 "re-run the owning item" wording and the exact-8 lens-input detail ("OQ-1 to OQ-8"). Its section 3 point 2 (do not copy the whole block) is correct on ADD:21 sentence 4. Its "circular" claim about the carrier is not established: V2's reading is sound that TL:1210 requires authorization before the edit, TL:1213 logs it afterwards and TL:1293 checks it later, so the log can preserve earlier consent. It also moves the stale-anchor fix to the appended note, which is better than my in-place rewrite.

V2: its two HIGH findings are right and stay at HIGH. Its narrowed remedy (embed the missing clauses, no new assertion) and its "keep ADD:21 sentences 1-3" correction are accurate. Its 0.99 for a conditional defect is acceptable because the confidence is about the implication, not branch probability. V2's slice (40 rows) cannot carry a clean-bill claim, and V2 agrees.

## 3. New evidence

1. TL:1973 (11.3) is the only item containing "same message". A grep for "chat-presentation" and "Formatting never" in TL finds no match anywhere. So ADD:19 last sentence and ADD:21 sentence 1 ("This is a chat-presentation exception only") are absent from every item that writes live text, while 11.4 (TL:1980) pins "role/table request alone" and "direct operative assignment plus separate invocation" against the real style. 7.10 lacks both. This is a verified delivery gap in 7.10, and the remedy is to embed these sentences.
2. TL:3016 requires line-stable in-place edits "before this appended note", and BR:20 allows revision notes appended after the checklist. Two fixes fit the 59-item anchor (59 matches of "not an implemented exception", confirmed): a single sentence in the appended note after TL:3018, plus one clause in the 7.10 Action. No body rewrite of 58 items is needed.
3. The 13.1 stale literal also appears at TL:776. That line is item 5.2, a ticked `[x]` and immutable. It is not a defect to fix.
4. R3-F4 does not hold up. TL:2999 is an entry added by reflect run 2 (R-05), shown in TL:2881. "Three original entries plus one line per new follow-up" (TL:2763) therefore counts TL:2996-2998 as originals and TL:2999 as a new line. I withdraw R3-F4.

## 4. Final positions

| Diff point | Final winner | Final severity | Reason |
|---|---|---|---|
| S-004 / S-006 (calibration, Tier-1 coverage) | V2 weight; V3 on coverage | LOW | Weight by C; V3 alone judged all ten Tier-1 findings, bookkeeping only. |
| C-001 / X-001 exact-8 | V2 | HIGH (conditional) | The `OQ-*` glob counts the optional OQ-17/OQ-18 files; no in-plan step repairs it (TL:1293, 1363, 1391). |
| C-002 / X-002 13.1 | V2 | HIGH (pre-existing) | TL:2265 orders copying DES:716; TL:2267 greps the old sentence. |
| C-003 / X-003 11.4 repair | split V1/V3 | LOW | The TL:353 link fails; TL:1982 and TL:1295 give a repair route. The only change is adding "re-run the owning item". |
| C-004 / X-008 carrier | V1 | MEDIUM | Fail-closed, so not a bypass. The form of evidence is unspecified, and one clause (quote the user's authorization with its date) closes it. I move from LOW-to-MEDIUM to MEDIUM because V1 and V2 both rate it so. |
| C-005 / X-007 7.10 omissions | V3 (finding), V1/V2 (remedy) | MEDIUM | Delivery gap confirmed above. Embed sentences; no new assertion. |
| C-006 / X-004 preamble | V1 | LOW | TL:1213 and TL:3018 override. A one-clause pointer is optional. |
| C-007 / X-005 (F9) | V2 | LOW | ADD:25 and ADD:31 permit the timing. No action. |
| C-008 / X-006 (F10) | V2 | LOW | Seven obligations plus a length-budget sentence at STYLE:25. No action. |
| C-009 / R2-F3 | none | LOW | Audit-recall only. Exclude from the merged card. |
| C-010 (F8) | V2 | LOW | ADD:39 excludes installation. Note only. |
| U-001 / U-003 | V1 | LOW | Wording gaps with no failure. Fold U-001 into the exact-8 fix at TL:1293. |
| U-004 | V2 | LOW (verifier) | The three-set acceptance is the verifier for the exact-8 fix, not a separate defect. |
| U-005 59-item anchor | V3 | LOW | The sentence is false after 7.10 for 58 items. No downstream item orders a revert. |
| U-006 sha256 pattern | V3 | LOW | Prose-only guard in 7.30/7.34 (TL:1363) against `sha256sum` in 14.x (TL:2614, 2642, 2705, 2733). |
| U-007 R3-F4 | none | withdrawn | See new evidence 4. |
| U-008 GQ-63 wording | V3 | LOW | Single-source; optional. |

## 5. Merge candidates for the merged card

1. **HIGH (conditional): exact-8 decisions-gate count** at 7.20 (TL:1293), 7.30 (TL:1363), 7.34 (TL:1391). Smallest fix: restrict the glob to `OQ-[1-8]-*`, or write "expect 8 plus one per recorded OQ-17/OQ-18 file". The 7.21/7.35 inputs "OQ-1 to OQ-8" need the same wording. Verify with V2's three file sets. Fold in U-001 by adding a `grep -c` and an expected value for the style checks in the same line.
2. **HIGH (pre-existing): 13.1** (TL:2265 versus TL:2267, DES:716). Smallest fix: grep the DES wording "The coordinator runs `/sc:sweep` on every wake, at most once every 5 minutes", or take the literal from the DES text. Check the placement against neighbouring bullets. Label it pre-existing. Do not touch TL:776.
3. **MEDIUM: 7.10 authorization evidence carrier** (TL:1210, 1213, 1293). Smallest fix: the Execution Log entry quotes the user's authorization message with its date, and 7.20 checks the quote. No new file.
4. **MEDIUM (R3-F2, survives narrowed): 7.10 omits operative clauses that 11.4 pins.** Smallest fix: add to the 7.10 Action, on the same physical line, ADD:15 sentences 1-2, ADD:17 sentence 3, ADD:19 sentence 4, and ADD:21 sentences 1-3 verbatim. Reword ADD:21 sentence 4 in the present tense: "This rule is not a runtime detector, identity probe, environment flag or assignment grant." No new 11.4 assertion.
5. **LOW (R3-F1, survives): the "unqualified table mandate, not an implemented exception" anchor in 59 items.** Smallest fix: one sentence in the appended note after TL:3018 saying later items describe the pre-7.10 state and executors read the actual style, plus one clause in the 7.10 Action. No body rewrite.
6. **LOW: 11.4 repair wording** (TL:1982). Add "re-run the owning item", and say that a 7.10 re-run needs authorization only if the original scope does not cover the repair.
7. **LOW (R3-F3, survives, optional): 7.30/7.34 fixers guard authority with prose only.** Smallest fix: add a before/after `sha256sum` of the addendum, BR and OQ-6 record to the re-run commands. The heading count I proposed is dropped.
8. **LOW (optional): preamble conflict** (TL:1143 versus TL:1210). One-clause pointer to TL:1213 and TL:3018.

R3-F4 is withdrawn; F8, F9, F10 and R2-F3 are excluded as no-action or refuted.
