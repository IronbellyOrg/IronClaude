# Consensus: Reflect UC-1 pre-execution reviewer cards (sc:adversarial Mode A, depth standard, Rounds 1-2)

Aliases. TL = `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`. ADD = `.../revisions/chat-output-exception-20261109-133150/design-addendum.md`. DES = `docs/designs/orchestrator-mode.md`. STYLE = `src/superclaude/output-styles/pragmatic.md`. V1 = reviewer 1 (analyzer, C 0.69), V2 = reviewer 2 (qa, C 0.86), V3 = reviewer 3 (refactorer, C 0.71). The scorer did not advocate for any variant. Lines named below were Read or grepped by the scorer in this pass (TL 774-776, 1143, 1207-1213, 1268-1275, 1290-1296, 1360-1365, 1388-1393, 1551, 1972-1987, 2046-2051, 2262-2270, 2758-2765, 2879-2881, 2992-3021; DES 645, 714-717, 758-761; STYLE 22-90 mentions of DONE / NEXT; ADD 1-46; `coverage-matrix.yaml` 247-249). Severity legend: HIGH = a correct run fails or a required check is lost; MEDIUM = real impact, workaround exists; LOW = minor.

Facts the advocates still disagreed on, settled against the source:
- ADD:21 has four sentences. V2 is right: sentences 1-3 are operative (chat-presentation only; changes no trigger/tool/authority/worker/permission/scheduler/JSON/report; all other rules remain). Only sentence 4 ("Eligibility is a proposed loaded-instruction contract...") is planning language. V1's "line 21 is meta text" and V3's "copy ADD:13-21 verbatim" were each wrong in part.
- The 7.10 Action (TL:1210) lacks the same-message clause, the "Formatting never authorizes..." clause and the "chat-presentation" clause. A grep of TL finds "same message" only at TL:1973 (11.3) and finds no "Formatting never" and no "chat-presentation" anywhere. 11.4 (TL:1980) does pin "role/table request alone" and "direct operative assignment plus separate invocation" against the real style. V3 and V1 are right on the omission; V2 is right that TL:1212 (compare against the addendum) and TL:1980 (semantic cases, not block equality) make a mismatch avoidable.
- "not an implemented exception" occurs 59 times in TL (grep count 59). V3's count holds; each such item also names the actual style as an input (TL:1986 reads both).
- The 13.1 stale literal is real: TL:2265 says copy the DESIGN text when it differs, DES:716 reads "The coordinator runs `/sc:sweep` on every wake, at most once every 5 minutes...", and TL:2267 still greps "The coordinator sweeps on every wake...". The same old literal also sits at TL:776, which is the ticked item 5.2 (`[x]`), so it is historical and must not be edited.
- R3-F4 (the "three" Follow-Up entries) does not hold: TL:2999 carries "(reflect run 2, R-05)" and TL:2881 records that R-05 added that follow-up after the entries TL:2761-2763 count. V3 withdrew it.
- `coverage-matrix.yaml` INF-041 (line 249) quotes only the empty-section sentence; the matrix has no "Distinct affected sessions" text, while DES:645 does. That is an audit-recall gap, not a missing delivery. V2 withdrew R2-F3.

## Scoring matrix

R1/R2 cells give V1 / V2 / V3 positions (severity where one was given). "cond" = conditional on the branch firing. Agreed = all three advocates, or at least two with the third not contesting after Round 2, end on the same winner and severity. C-NNN and X-NNN rows are paired by topic (C-001/X-001 and so on), so their scores move together.

| Diff point | Level | R1 | R2 | Agreed | Winner | Confidence | Evidence summary |
|---|---|---|---|---|---|---|---|
| S-001 Slice audited | L2 | V3: none (60%); V1/V2: V2 narrow by design | V2 concedes 40 rows cannot carry a clean bill; V1 agrees | true | none | 75% | Descriptive difference; nobody claims the widest slice wins. V2 concedes "0 missing deliveries" is slice-only (round2-v2 criticism 1). |
| S-002 Finding count and severity profile | L1 | V1: 0 HIGH; V2: 2 HIGH; V3: 0 HIGH (concedes it missed both) | V1 and V3 concede both HIGHs to V2; V3 lowers its own R3-F1 | true | V2 | 85% | Settled by concessions: the merged profile is 2 HIGH (exact-8, 13.1) plus MEDIUM/LOW. Not debated as a row, so scored from the concessions. |
| S-003 Evidence and verifier shape | L1 | V3 R1: V2/V3 citation hygiene better; V1 admits 3 failed citations | V1 concedes; V2 A-005: source Reads decide | true | none | 70% | All agree line citations must be re-read, not carried. Style differences are not contested (not debated as a row). |
| S-004 Calibration outcome | L2 | V3: V2 weight 80% | V3 repeats; V1 accepts (A-004: re-grade by brief definition first); V2 silent | true | V2 | 80% | Weight by C only after re-grading severity by the brief definition; V2 0.86 with 0 failed citations over V3 0.71 over V1 0.69. Single explicit voice plus V1 acceptance. |
| S-005 Finding vocabulary | L1 | not debated | V1 concedes "gate-bypass" to "missing"; V2 calls it an evidence-specificity issue; V3 agrees | true | none | 70% | Labels converge on "missing" for the authorization carrier (TL:1210 fails closed, TL:1213 blocks ticking). Row itself not debated. |
| S-006 Verdicts on Tier-1 F1-F10 | L2 | V1: V3 (bookkeeping flaw on F5); V3: V3 70% | V1: V3 LOW; V3: V3 for coverage; V2: split LOW | true | V3 | 75% | V3 alone judged all ten; V1 concedes it listed F5 "not in the excerpt" while R1-F4 is that defect. Bookkeeping only. |
| S-007 What counts as a coverage gap | L2 | V3: none 65%; V1/V2 silent | V2: split LOW (unequal slices); V3: none | true | none | 75% | Tallies (5, 0, 3) are not comparable across unequal slices; no advocate defends a winner. |
| S-008 State-preservation check depth | L3 | V3: V3 60% | not addressed by V1 or V2 | false | V3 (single voice) | 55% | Only V3 argues (counts of `- [x]` and `- [ ]`, end line). Nobody contested, nobody joined. Unresolved by absence of debate, low stakes. |
| S-009 Uncertainty marking | L1 | V1 claims its [INFERRED] tags as a strength | not addressed | false | none (single voice) | 50% | Only V1 speaks (round1-v1 strength 6). V2 R2 notes its 40/40 does not settle inferred rows; no one ranks the styles. Unresolved by absence of debate. |
| C-001 Exact-8 check | L3 | V1: MEDIUM then concedes HIGH-cond; V2: HIGH 99%; V3: confirms, concedes HIGH | V1 HIGH; V2 HIGH; V3 HIGH (cond) | true | V2 | 97% | TL:1272 sets `status: RESOLVED` on approval or refusal and TL:1270 writes OQ-17/OQ-18 files, so TL:1293 (`OQ-*-decision.md ... wc -l`, expect 8), TL:1363 and TL:1391 count 9 or 10; the 7.30 fixer re-runs the same literal. V1 and V3 conceded. |
| C-002 13.1 stale literal | L2 | V1: verified, HIGH; V2: HIGH 99%; V3: confirms | all HIGH, label pre-existing | true | V2 | 97% | TL:2265 orders copying the DESIGN text, DES:716 now reads "The coordinator runs `/sc:sweep` on every wake...", TL:2267 still greps the old sentence and expects line 404. TL:776 (ticked 5.2) must stay unedited. |
| C-003 11.4 failure path | L3 | V1: MEDIUM then overclaim conceded; V2: MEDIUM clarity; V3: LOW | V1 LOW; V2 LOW; V3 LOW | true | split (V1 narrowed, V3) | 85% | TL:1982 says a failure is fixed "in its owning source item or authorized serialized fixer"; TL:1295 sets the "return to the owning item and re-run this item" convention; stall is inferred, not proven. One sentence adds the missing "re-run". |
| C-004 7.10 authorization carrier | L3 | V1: MEDIUM; V2: MEDIUM 92%; V3: LOW-MEDIUM | V1 MEDIUM; V2 MEDIUM; V3 MEDIUM | true | V1 | 88% | TL:1210 Branch 1 requires "separate direct execution authorization" but names no carrier; TL:1213 logs evidence afterwards and TL:1293 requires it "independently evidenced". V1's "circular" claim was not accepted; severity and fix are agreed. |
| C-005 7.10 omissions | L2 | V1: LOW then MEDIUM; V2: MEDIUM 96%; V3: MEDIUM | V1 MEDIUM (V3 narrowed); V2 MEDIUM split; V3 MEDIUM | true | V3 (finding), V1/V2 (remedy) | 88% | TL:1210 omits ADD:15 s1-2, ADD:17 s3, ADD:19 s4 and ADD:21 s1; 11.4 (TL:1980) pins two of those cases. Remedy agreed by all three in Round 2: embed the missing clauses, not the whole ADD:13-21 block, no new substring assertion. |
| C-006 Preamble branch conflict | L3 | V1: LOW; V2: LOW 96%; V3: LOW | all LOW | true | V1 | 90% | TL:1143 Branch 2 "resets the task status to Doing and clears blocker_reason" conflicts in letter with TL:1210/1213; TL:1213 ("cannot be marked as done") and the TL:3018 note override it. V1's "tick without an edit" was conceded. |
| C-007 Severity-module timing (F9) | L2 | V1: taste; V2: refuted 98%; V3: LOW | all LOW, no action (V2 class) | true | V2 | 92% | ADD:25 and ADD:31 assign immediate text/diff checks to 7.10 and the severity modules to 11.5 (TL:1986-1987). Timing is a true fact, not a missing requirement. |
| C-008 "Seven sites" (F10) | L1 | V1: not judged; V2: refuted; V3: confirmed | V1 V2; V2 V2; V3 V2 (not a defect) | true | V2 | 95% | STYLE mentions DONE / NEXT at 22, 25, 53, 58, 60, 69, 80, 90; STYLE:25 is the length-budget sentence that ADD:27 keeps byte-for-byte. Seven obligations, eight mentions, no defect. |
| C-009 Matrix completeness (R2-F3) | L2 | V1: accept LOW 60%; V2: LOW 98%; V3: LOW does not affect execution | V2 withdraws it; V3 none, exclude; V1 audit gap only | true | none (exclude) | 90% | `coverage-matrix.yaml:249` quotes only the empty-section sentence; "Distinct affected sessions" appears at DES:645 but not in the matrix. Delivery sits in 8.12/10.5 (cited by V2, not re-read by the scorer). |
| C-010 Install follow-up (F8) | L2 | V1: notes only; V2: split LOW; V3: LOW | V2 split; V3 downgrades to informational (ADD:39) | true | split / none | 88% | ADD:39 "authorizes no HOME install/update or activation", so a missing install follow-up is not a plan defect. Single-source (V3) and LOW. |
| C-011 One source per item, order | L2 | V1: order sound; V2/V3: allocation retained | all: no conflict | true | none | 90% | ADD:25-31 allocation matches 7.10, 11.3, 11.4, 11.5 as written. Nobody disputes it. |
| X-001 Severity of exact-8 | L3 | V1: MEDIUM "likely"; V2: HIGH; V3: confirms | V1 withdraws "likely" (DES:760 UNVERIFIED) and accepts HIGH-cond; V3 HIGH-cond | true | V2 | 97% | DES:760 calls `page.nextCursor` UNVERIFIED until step 1.0a item 3, so the defect is certain when the branch fires and likelihood is unknown. Brief definition gives HIGH. |
| X-002 Severity of 13.1 | L2 | V2: HIGH; V3: confirms; V1: verified HIGH | all HIGH | true | V2 | 97% | Following the TL:2265 Action fails the TL:2267 Verification. Superseded T1's MEDIUM. |
| X-003 11.4 repair path | L3 | V1: no repair step, ties to a retry-restore stop; V2: owning path exists; V3: stall inferred | V1 concedes, LOW; V2 LOW; V3 LOW | true | split (V1 narrowed / V3) | 85% | The retry-restore link fails: the preservation stop is the tail of TL:1210 and fires on an original-start restore, not an in-place re-run. TL:1982 plus TL:1295 give a route; 11.4 only omits "re-run this item". |
| X-004 Tick 7.10 without edit | L3 | V1: LOW; V2: LOW 97%; V3: LOW | all LOW | true | V1 (LOW) | 90% | TL:1213: "This item cannot be marked as done until the actions are completed in their entirety"; TL:1210 Branch 1 "STOP without ticking". Residual is a reading-order ambiguity with TL:1143. |
| X-005 Severity-module timing as defect | L2 | V1: taste; V2: refuted; V3: LOW | all: no defect, LOW | true | V2 (class) | 90% | Same evidence as C-007 (ADD:25, ADD:31, TL:1986-1987); V1 withdrew its `grep -c` as redundant (TL:1212 already requires byte-identical severity text). |
| X-006 Eighth DONE / NEXT mention | L1 | V1: not judged; V2: refuted; V3: confirmed | V1 V2; V2 V2; V3 V2 | true | V2 | 95% | Both facts true (STYLE:25 is an eighth mention), refuted as a defect: ADD:27 keeps the length budget, TL:1212 says "all seven live mandatory-table sites". V3 conceded. |
| X-007 Do 7.10 omissions make 11.4 fail? | L2 | V1: "11.4 fails" LOW; V3: "will not match" MEDIUM | V1 MEDIUM, mismatch not inevitable; V2 MEDIUM; V3 concedes overstatement, MEDIUM | true | V3 (finding) | 85% | TL:1212 and TL:1980 make a mismatch avoidable, but the Action is incomplete (see C-005). All three end MEDIUM with the narrowed remedy. |
| X-008 Is the carrier gap a bypass? | L3 | V1: "gate-bypass"; V3: fails closed | V1 concedes label, MEDIUM; V2 MEDIUM; V3 MEDIUM | true | V1 (relabelled "missing") | 85% | TL:1210 Branch 1 keeps Blocked and TL:1213 forbids completion, so no bypass; the gap is the unspecified evidence form. |
| A-001 Executed in checklist order | L3 | V1 accept; V2 accept; V3 accept | unchanged | true | accept | 95% | Every sequencing finding assumes checklist order (7.17 before 7.20, 7.10 before 11.3/11.4). |
| A-002 Branches may fire | L3 | V1 accept; V2 qualify (no likelihood); V3 accept | V1 withdraws "likely" | true | accept as "branch fires" | 95% | DES:760: `page.nextCursor` UNVERIFIED. Never write "likely". |
| A-003 Ticked item cannot be re-run | L3 | V1 qualify; V2 reject; V3 qualify | V1/V3 agree it is only partly true | true | partly contradicted | 80% | TL:1295 re-runs owning items; TL:1982 omits "re-run this item". V2's reject and the others' qualify describe the same position. |
| A-004 Severity comparable across cards | L2 | accept (all three) | unchanged | true | accept | 95% | Re-graded by the brief definition: exact-8 and 13.1 become HIGH. |
| A-005 T1 line numbers current | L1 | V1 accept; V2 reject (source Reads decide); V3 accept | V1 lists failures; V3 re-read lines hold | true | re-read before citing | 85% | The scorer re-read TL:1143, 1210, 1213, 1293, 1363, 1391, 1982, 2265, 2267 and DES:716; they hold. |
| A-006 Check conflicting with its Action is a defect | L3 | accept (all three) | unchanged | true | accept | 95% | TL:2265 vs TL:2267; TL:1293 vs TL:1295 (style checks with no command). |
| A-007 Static checks prove text only | L2 | accept (all three) | unchanged | true | accept | 95% | ADD:37 and TL:3020 state the limit. |
| A-008 Authority files unchanged | L3 | V1 qualify; V2 qualify; V3 qualify | unchanged | true | qualify | 85% | Mechanical in 14.x (`sha256sum` at TL:2614, 2642, 2705, 2733), prose-only in 7.30/7.34 (TL:1363, 1391). |
| A-009 Sign-off and authorization evidence exists | L3 | V1 qualify; V2 qualify; V3 qualify | unchanged | true | qualify | 85% | The reports exist; the gap is that 7.10 (TL:1209-1210) names none and no carrier is specified. |
| A-010 One confirmation suffices (F6/F8) | L2 | V1 accept; V2 reject; V3 qualify | V2 does not carry it forward; both findings end LOW | true | majority (V1, V3) | 65% | V1 and V3 hold LOW single-source enough; V2's R1 dissent was not retracted but not argued in R2. Practical outcome identical (LOW, no action). |

## Convergence assessment

- Agreed points: 36 of 38. Convergence = 36 / 38 = **0.947**.
- Unresolved points: **2**, both unaddressed rather than contested: S-008 (state-preservation depth, only V3 speaks) and S-009 (uncertainty marking, only V1 speaks). Both are L3/L1 bookkeeping rows with no effect on the merged card.
- Conservative reading: S-002, S-003, S-004 and S-005 are scored from concessions or a single explicit voice, not from head-to-head debate. If they are also counted unresolved, convergence is 32 / 38 = 0.842, still above 0.80.
- Caveat: C-NNN and X-NNN rows are paired by topic, so the eight pairs inflate the agreed count together. The topic-level result is unchanged: every disputed finding ended with matching severity from all three advocates.
- Taxonomy coverage of agreed points: L1 6 of 7 agreed (S-002, S-003, S-005, C-008, X-006, A-005; open: S-009); L2 16 of 16; L3 14 of 15 (open: S-008). Each of L1, L2 and L3 has at least one agreed point.
- **Status: CONVERGED on the diff-point score** (0.947 is at least 0.80, and L1, L2 and L3 are all covered). The invariant probe has not run, so the "no HIGH unaddressed invariant" clause is not assessed here. The two HIGH items (M-01, M-02) are addressed by agreed fixes below, not left open.
- No substantive dispute remains. The only unretracted dissent is V2's A-010 reject (single-confirmation findings), which does not change any merge candidate.

## Merge candidates

Every cited line below was Read by the scorer. Status tags: agreed (all three end on the same severity and fix), majority (two of three, third silent). "Smallest fix" is one edit; "Verifier" is a command or read that shows the fix landed.

**M-01 | HIGH | unsound-check (a check rejects a correct run) | agreed**
- Location: TL:1293 (7.20 Action: `grep -l 'status: RESOLVED' ...OQ-*-decision.md | wc -l` "(expect 8)"), repeated at TL:1363 (7.30) and TL:1391 (7.34). The optional OQ-17/OQ-18 files are written at TL:1270 and set `status: RESOLVED` at TL:1272. DES:760 marks the cursor field UNVERIFIED.
- Claim: when a 7.17 allowlist branch fires, a correct run matches 9 or 10 files, and the 7.30/7.34 fixers re-run the same literal, so no in-plan step makes it pass. State it as "fails when the branch fires", never "likely".
- Smallest fix: count only the eight named prerequisites (`OQ-[1-8]-*-decision.md`) at TL:1293, 1363 and 1391, and check each existing OQ-17/OQ-18 file separately (each must be RESOLVED). Optional: reword "the eight decision records `OQ-*-decision.md` (OQ-1 to OQ-8)" in the lens inputs at TL:1299 to 1404 and TL:2572, which glob the same files.
- Verifier: three file sets must pass (eight prerequisites; eight plus one resolved optional; eight plus two) and an unresolved required record must fail (U-004). Folds in the V2 acceptance design.
- Sources: R1-F3 (V1, MEDIUM, raised to HIGH-cond), R2-F1 (V2, HIGH), T1 F3, U-004, C-001/X-001.

**M-02 | HIGH | unsound-check / stale-text (Verification contradicts its own Action) | agreed | predates the revision**
- Location: TL:2265 (13.1 Action: "copy the DESIGN text and log the difference"), TL:2267 (Verification greps "The coordinator sweeps on every wake, at most once every 5 minutes." and expects line 404), DES:716 (R2 bullet now "The coordinator runs `/sc:sweep` on every wake, at most once every 5 minutes, beside "The sweep."").
- Claim: copying the current DESIGN text, as the Action says, fails the item's own first Verification grep.
- Smallest fix: change the 13.1 Action quote and the first Verification grep to the DES:716 wording, and keep the placement check against the neighbouring bullets. Do not touch TL:776 (ticked item 5.2).
- Verifier: the edited grep prints line 404 on `src/superclaude/core/HOW-WE-WORK.md` after the edit, and `grep -c 'sweeps on every wake\.\*\*'` is 0.
- Sources: R2-F2 (V2, HIGH), T1 F1 (MEDIUM, superseded), C-002/X-002. Label it pre-existing (outside the revised bodies, per diff-analysis X-002).

**M-03 | MEDIUM | partial (required clauses missing from the item that writes the rule) | agreed**
- Location: TL:1210 (7.10 Action) against ADD:15 (sentences 1-2), ADD:17 (sentence 3, same message), ADD:19 (sentence 4, "Formatting never authorizes..."), ADD:21 (sentences 1-3). 11.4 (TL:1980) pins "role/table request alone" and "direct operative assignment plus separate invocation" against the style; 11.3 (TL:1973) has the same-message clause; TL:1212 tells the executor to compare against the addendum.
- Claim: 7.10 omits operative clauses that 11.4 tests, so a paraphrasing executor can write a style 11.4 rejects. A mismatch is avoidable but not guaranteed to be avoided.
- Smallest fix: embed the missing sentences in the 7.10 Action on the same physical line (line-stable edit, TL:3016). Restate ADD:21 sentence 4 in the present tense ("not a runtime detector, identity probe, environment flag or assignment grant"); do not copy "proposed". Add no new substring assertion to 11.4.
- Verifier: `grep -n 'same message\|Formatting never\|chat-presentation'` on TL then hits line 1210 as well as 1973 (today only 1973 matches "same message" and nothing matches the other two).
- Sources: R3-F2 (V3, MEDIUM), R1-F4 (V1, LOW raised to MEDIUM), C-005/X-007. INF-A15 "length budget partial" (V3) is not carried: ADD:27 keeps the length budget and the scorer did not verify a gap.

**M-04 | MEDIUM | missing (evidence form unspecified; not a bypass) | agreed**
- Location: TL:1210 Branch 1 ("separate direct execution authorization"), TL:1213 (log "check/authorization evidence" at completion), TL:1293 (7.20: authorization "independently evidenced"), TL:1209 (Context lists the research-gate file and the research files, but none of the fresh structural/alignment/QA reports).
- Claim: 7.10 fails closed, but it names no carrier for the user's authorization or for the fresh sign-off reports, so 7.20 has nothing specific to check.
- Smallest fix: add one clause to the 7.10 Action: the Execution Log entry and the step-7.10 result file quote the user's separate authorization message verbatim with its date, and list the fresh sign-off report paths; 7.20 checks that quote. No new grant file (V1 dropped its proposed `OQ-6-style-execution-authorization.md`).
- Verifier: the step-7.10 result file and the log row contain the dated quote; `grep -n 'verbatim' ` on TL:1210 hits.
- Sources: R1-F2 (V1, relabelled from gate-bypass), T1 F4, C-004/X-008. V1's "circular" sub-claim was not accepted by V2 or V3 and is dropped.

**M-05 | LOW | partial (repair wording) | agreed**
- Location: TL:1982 (11.4 Verification: "A failure is fixed in its owning source item or authorized serialized fixer ... and stop incomplete until checks pass"); convention at TL:1295 ("return to the owning item and re-run this item"); fixer 11.14 at TL:2048-2050 is the only item allowed to edit STYLE.
- Claim: 11.4 omits "re-run this item", so the in-place repair route is implicit. No stall is proven.
- Smallest fix: add "return to the owning item (7.10, 11.1 or 11.3) and re-run this item; a 7.10 re-run needs fresh authorization only if the original scope does not cover the repair".
- Verifier: `grep -n 're-run this item'` hits TL:1982.
- Sources: R1-F1 (downgraded from MEDIUM; the "no executable repair step" and retry-restore claims were conceded), T1 F2, C-003/X-003.

**M-06 | LOW | stale-text (misleading context in 58 later items) | agreed**
- Location: "(unqualified table mandate, not an implemented exception)" appears 59 times (grep count): TL:1209 (7.10 itself), 1292, 1362, 1390, 1986, 2049 and others. After 7.10 runs it is false for the other 58. Each also names the actual style as input (TL:1986 reads "actual canonical style" in the same Context).
- Claim: false future context, with no downstream item ordering a revert. A lens that trusts the label over the disk could raise a false BLOCKING finding.
- Smallest fix: one sentence in the appended note after TL:3018 saying later items describe the pre-7.10 state and executors read the actual style, plus one clause in the 7.10 Action. No edit of the 58 bodies (TL:3016 allows only line-stable in-place body changes, and BR line-stable rule).
- Verifier: `grep -c 'not an implemented exception'` still prints 59; the appended note contains the new sentence.
- Sources: R3-F1 (V3, lowered from MEDIUM by V3 itself), U-005.

**M-07 | LOW | authority (prose-only guard where 14.x uses a hash) | agreed | optional**
- Location: TL:1363 (7.30) and TL:1391 (7.34) guard with "Never change revision authority/design append/decision choice"; `sha256sum` appears only at TL:2614, 2642, 2705, 2733.
- Claim: pattern break; no mutation is shown.
- Smallest fix: add a before/after `sha256sum` of the addendum, the revision BUILD-REQUEST and the OQ-6 record to the 7.30/7.34 re-run commands. Drop V3's heading count (it proves presence, not content).
- Verifier: fix log shows equal hashes before and after; `grep -c sha256sum` on TL rises.
- Sources: R3-F3 (V3), U-006, A-008.

**M-08 | LOW | missing (check with no expected value) | agreed**
- Location: last sentence of TL:1293 (7.20 style checks: read the addendum, record the style diff, confirm "all seven table sites agree") has no command or expected value, while TL:1295 says each check is "decided by the expected value written beside its command". The 7.30/7.34 re-run lists (TL:1363, 1391) omit it too.
- Smallest fix: make the same edit as M-01 and add `grep -c 'Except for the sweep chat-summary exception above,' src/superclaude/output-styles/pragmatic.md` (expect 6, per TL:1210 and ADD:27) with a PASS/FAIL line.
- Verifier: the 7.20 Action then has a command and expected value for the style check.
- Sources: U-001 (V1); V3 R2 folds it into the M-01 edit.

**M-09 | LOW | ordering (preamble conflict) | agreed | optional**
- Location: TL:1143 (preamble Branch 2 "resets the task `status` to Doing and clears `blocker_reason`" for every HALT item) against TL:1210/1213; override only at TL:3018 (end of file).
- Claim: letter conflict, settled by TL:1213 and TL:3018; ticking without an edit is blocked.
- Smallest fix: a one-clause pointer in the 7.10 Action to TL:1213 and the TL:3018 note.
- Verifier: `grep -n` of the pointer in TL:1210.
- Sources: R1-F5 (V1, LOW; "tick without an edit" claim conceded), T1 F7, C-006/X-004.

**M-10 | LOW | stale-text (GQ-63 scope attribution) | majority | optional**
- Location: TL:1551 (8.14 lens: "the layout follows the recorded GQ-35 and GQ-63 decisions") and TL:1812 ("OQ-4 (GQ-35) and OQ-6 (GQ-63)"); the OQ-6 record line 12 says the decision "affects only the sweep skill's chat reply, not the report file's layout" (grep match at line 12; TL:1812 context seen only through the grep match).
- Claim: the report-layout lens cites a decision that does not govern the report layout, which can yield a false finding.
- Smallest fix: reword both lines so GQ-63 governs the chat reply and GQ-35 governs the report layout.
- Verifier: `grep -n 'GQ-35 and GQ-63'` no longer matches TL:1551.
- Sources: T1 F6 as confirmed by V3 (U-008); V2 R1 agreed in substance; V1 silent.

### Disposition of every card finding and unique row

| Item | Disposition | Reason |
|---|---|---|
| R1-F1 (11.4 no repair step, MEDIUM) | carried, downgraded to LOW as M-05 | TL:1982 and TL:1295 give a route; the retry-restore link fails; V1 conceded. |
| R1-F2 (authorization carrier, "gate-bypass") | carried as M-04, relabelled "missing", MEDIUM | TL:1210/1213 fail closed. |
| R1-F3 (exact-8, MEDIUM) | carried, raised to HIGH as M-01 | Brief definition; V1 conceded. |
| R1-F4 (same-message clause, LOW) | merged into M-03, raised to MEDIUM | V3 found five omissions; V1 conceded. |
| R1-F5 (preamble conflict, LOW) | carried as M-09 | TL:1213 and TL:3018 settle it; optional. |
| R2-F1 (exact-8, HIGH) | carried as M-01 | Agreed by all three. |
| R2-F2 (13.1, HIGH) | carried as M-02 | Agreed by all three. |
| R2-F3 (matrix recall, LOW) | dropped | V2 withdrew it; delivery exists; matrix:249 only quotes a shorter sentence. |
| R3-F1 (59-item anchor, MEDIUM) | carried, downgraded to LOW as M-06 | V3 lowered it; false context, not an observed revert. |
| R3-F2 (7.10 omissions, MEDIUM) | carried as M-03 | Remedy narrowed by V1 and V2, accepted by V3. |
| R3-F3 (7.30/7.34 prose guard, LOW) | carried as M-07, optional | Pattern gap only. |
| R3-F4 ("three" entries, LOW) | dropped | V3 withdrew it; TL:2999 was added by R-05 (TL:2881). |
| U-001 (7.20 style checks without a command) | carried as M-08 | Real wording gap; fix lands with M-01. |
| U-002 (7.17 step 2 follow-up has no item) | dropped | Unchanged from baseline; V1 scoped it out; TL:1271 reviewed. |
| U-003 (no test pins "No exceptions") | dropped as a finding | 11.4 supplies the pin (V1 R2, V2 R2); not re-run by the scorer. |
| U-004 (three-set acceptance) | merged into M-01 as its verifier | V2, V3 agree it is the verifier, not a defect. |
| U-005 (59-item sentence) | merged into M-06 | Same finding as R3-F1. |
| U-006 (sha256 pattern) | merged into M-07 | Same finding as R3-F3. |
| U-007 ("three" entries) | dropped | Same as R3-F4. |
| U-008 (GQ-63 wording) | carried as M-10, optional | Majority (V3, V2 R1). |
| U-009 (INF-A29, INF-A14) | dropped | V3 itself calls INF-A29 harmless; not verified. |
| U-010 ("OWNER DECISION PENDING" history) | dropped | Kept as history; a POST reviewer may flag it, not a plan defect. |
| U-011 (repeated lens sentence in 7.31, 7.32, 7.35, 7.36) | dropped | Harmless copy-paste. |
| T1 F1 / F3 | carried as M-02 / M-01, upgraded to HIGH | See above. |
| T1 F2 / F4 / F7 | carried as M-05 / M-04 / M-09 | Reduced certainty. |
| T1 F5 | merged into M-03 | Refined to R3-F2. |
| T1 F6 | carried as M-10 | Single-source, LOW. |
| T1 F8 | dropped | ADD:39 excludes installation; informational. |
| T1 F9, F10 | dropped | Timing and the eighth mention are true facts, not defects (ADD:25, 27, 31; STYLE:25). |

Counts: 2 HIGH (M-01, M-02), 2 MEDIUM (M-03, M-04), 6 LOW (M-05 to M-10).

## Conceded points

- V1 conceded: R1-F3 should be HIGH-conditional and its "likely" claim is unsupported (DES:760); R1-F1's "no executable repair step" and its TL:353 link; R1-F2's "gate-bypass" label; R1-F5's "tick without an edit"; its S-006 bookkeeping flaw; three failed citations (TL:353, TL:1209, TL:1272); that R1-F4 saw one omission where V3 saw five. V1 also dropped its proposed authorization file and its "circular" framing.
- V2 conceded: the 40-row slice cannot carry a clean bill; R2-F3 is withdrawn from the merged card; its own MEDIUM ratings on recovery and stale anchors move to LOW; its earlier endorsement of copying the whole ADD:13-21 block, replaced by embedding only the missing clauses; F9 and F10 are refuted as defects, not as facts.
- V3 conceded: both of V2's findings are HIGH and it had scored 0 HIGH; R3-F1 is LOW; R3-F2's "will not match" prediction is overstated; the new 11.4 substring assertion is unnecessary; the whole-block verbatim copy was too wide (ADD:21 sentence 4 is planning language); R3-F3's heading-count verifier is weak; R3-F4 is withdrawn; F10 is not a defect; F8 is informational; its "45 of 45" has no row ledger.
- Cross-concessions: all three accept A-001, A-002, A-004, A-006, A-007, and the re-grading of severity by the brief definition (A-004).
- Not conceded: V2's A-010 dissent (a single confirmation needs independent grounding); it affects no merge candidate.
