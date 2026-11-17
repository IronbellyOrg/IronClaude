# Qualitative Score, Pass 1 (order: Variant A, then Variant B), slot X-15 tasklist-medium-and-fidelity-vocab

Rubric: 30-criterion additive binary (sc-adversarial-protocol, Qualitative Scoring Layer T04.02; refs/scoring-protocol.md A.2). Protocol: Claim-Evidence-Verdict, no partial credit, no evidence means NOT MET. Variants scored as written (`variant-1-original.md` = A, `variant-2-original.md` = B); Round 2 hybrids (A+, H+) are not credited. Code facts re-read at HEAD 50d4d2b9d (read-only).

## Variant A (Proposal A, Medium is a non-blocking warning), evaluated first

| ID | Criterion (short) | Verdict | Evidence |
|---|---|---|---|
| CO1 | Covers all explicit requirements | MET | Sections 1-8 map to every brief item: position (1), core and modules (2), evidence (3), invariants (4), test or measurement (5), PR review and rf-qa (6), C-01..C-03 (0 and 8). |
| CO2 | Edge cases and failure scenarios | MET | Section 4.2 lists six costs, e.g. "A run whose only residual findings are Medium used to HALT at the P2 cap ... under this position it completes with a follow-up list" and "Grade-boundary sensitivity". |
| CO3 | Dependencies and prerequisites | MET | Section 0 table of the C-01, C-02, C-03 outcomes relied on; section 8 states "Not an input: C-05". |
| CO4 | Success/completion criteria | MET | Section 5 static tests T1-T4 "red before the change, green after" plus "The result that would show the position right: few Medium rows are blocking by the implement rule". |
| CO5 | Explicit out of scope | MET | Section 9 "Not claimed" (no branch/PR plan, no risk register) and section 2.1 "Which engine hosts tasklist review is not decided by this slot". |
| CR1 | No factual errors | NOT MET | Section 2.2 says the pinned phrase "the unresolved High or Medium HALT resolves as blocked" changes "in the skill and in both pins"; at HEAD that phrase exists only in `src/superclaude/commands/tasklist.md:113` (SKILL.md:1615 reads "this HALT resolves as blocked"), and the command file is absent from A's edit list. Also `SKILL.md:1445` is listed as a "High or Medium" site but reads "no blocking drift", and section 4.2 item 4 leans on a C-03 reviewer union that Stage 7 cannot supply (one agent per task slice, SKILL.md:1351-1368). |
| CR2 | Approaches feasible | MET | Both maps parse (verified `findings.py:100-101`, `findings_v2.py:155-162`); A states the `reflect_category` hazard that a v2 tasklist lens must not set it. Edits are text and fixture rewrites. |
| CR3 | Terminology consistent | MET | High/Medium/Low to CRITICAL/MAJOR/MINOR map used the same way in sections 1, 2, 4, 5; "Form 1 / Form 2" stable. |
| CR4 | No internal contradictions | NOT MET | Fact 13 calls the CLI "a separate roadmap-pipeline validator", while section 7 answer 3 argues "one product should not have a gate that passes a report and a skill that halts on the same row". |
| CR5 | Claims supported | MET | Section 3 is a 16-row table with source and tag per fact; section 7 answers each objection with cited facts (e.g. fact 9 commit history, which I re-checked: the #343 message records no Medium decision). |
| ST1 | Logical ordering | MET | 0 inputs, 1 position, 2 design, 3 evidence, 4 invariants, 5 tests, 6 effects, 7 objection, 8 dependencies, 9 limits. |
| ST2 | Consistent hierarchy depth | MET | H3 only under sections 2 (2.1-2.3) and 4 (4.1-4.2); no single-child subsection. |
| ST3 | Separation of concerns | MET | Position, design consequence, evidence, invariants, tests and downstream effects each have their own section. |
| ST4 | Navigation aids | MET | Abbreviation key `SK/PR/GT/RG/PM` and tags (section 3), numbered facts cited as "fact 9", "fact 13", cross-references "section 2.3", "section 5". |
| ST5 | Follows artifact conventions | MET | Follows the proposal shape the brief fixes: position, core/module consequence, evidence, invariants, test, PR/rf-qa effect, slot consistency, strongest objection. |
| CL1 | Unambiguous language | MET | No hedge phrases ("should consider", "might", "as appropriate"); the two "may" hits are a factual statement and a quoted objection; unknowns are tagged [UNVERIFIED]. |
| CL2 | Concrete, not abstract | MET | Names edit sites by line (`SK:1439` ... `:1614`), test names and lines, and copies the HIGH/MEDIUM/LOW definitions from `prompts.py:51-69` (verified). |
| CL3 | Section purpose clear | MET | Each section opens with its purpose, e.g. section 2.3 "The tasklist module declares, once, as module data: the labels ...". |
| CL4 | Terms defined on first use | MET | Header defines the evidence tags; section 0 defines C-01..C-03 before use; INV codes glossed inline ("INV-I (a review that did not happen never certifies PASS)"). |
| CL5 | Actionable next steps/decisions | MET | Form 1 versus Form 2 decision with a stated preference; M1 and M2 each say what result would show the position wrong. |
| RK1 | At least 3 risks with probability and impact | NOT MET | Section 4.2 gives six costs with consequences but no probability assessment, and section 9 says "no risk register". |
| RK2 | Mitigation for each risk | NOT MET | Section 4.2 item 2 (loosening) and item 3 (monotonicity stops firing on Medium churn) are stated as costs with no mitigation. |
| RK3 | Failure modes and recovery | MET | Section 4.1 INV-I: synthetic finding for a failed Stage 7 agent stays High and non-demotable, zero-success stays the report-validation-error terminal (SK:1400-1401, :1431 verified); `--unattended` still resolves as `blocked` (SK:1615). |
| RK4 | External dependencies and failure | MET | Section 8 per-slot dependencies, including C-02's unaddressed INV-016; M2 "if none exists M2 cannot be run and M1 is the only measurement". |
| RK5 | Monitoring/validation mechanism | MET | T1-T4 static tests (parity test T2), M1 blind grading, M2 Medium-row audit. |
| IE1 | Collection boundaries | MET | "a zero-success Stage 7 stays the report-validation-error terminal" and the Medium-only residual set (4.2 item 2). |
| IE2 | State interactions across boundaries | MET | Section 2.1: with `reflect_category` set a MAJOR must be blocking (`findings_v2.py:161-162`), opposite to the Medium map; section 8 depends on `brief_ids` holding blocking rows only. |
| IE3 | Guard condition gaps | MET | Section 2.1 Form 1: "the parser accepts MAJOR with either blocking value, so the rule rests on the brief"; 4.2 item 4: the CRITICAL floor keys on the reviewer-typed severity. |
| IE4 | Count divergence | MET | Section 2.3: `_tasklist_ready_consistent` checks `tasklist_ready` only against the typed `high_severity_count`, not the Deviation Report body (verified `roadmap/gates.py:195-240`); 4.2 item 3 `\|F_k\|` counts High only. |
| IE5 | Interaction effects | MET | Section 4.2 item 4 combines the grade boundary with the C-02 CRITICAL floor; section 2.1 combines Form 2 with `reflect_category`. |

## Variant B (Proposal B, Medium stays blocking), evaluated second

| ID | Criterion (short) | Verdict | Evidence |
|---|---|---|---|
| CO1 | Covers all explicit requirements | MET | Sections 1-8 cover position (1), core and modules (2), evidence (3), invariants (4), test or measurement (5), PR review and rf-qa (6), C-01..C-03 (7), strongest objection (8). |
| CO2 | Edge cases and failure scenarios | MET | E7: both archived reports have "High: 0, Medium: 4" and "High: 0, Medium: 2" so a non-blocking Medium would short-circuit Stage 8; section 4 covers stalled Medium and the INV-016 exposure. |
| CO3 | Dependencies and prerequisites | MET | Section 7: "B depends on C-01's condition that unknown keys stay open" and C-02's typed `blocking` authority; "if any of those is reopened, B is reopened with it". |
| CO4 | Success/completion criteria | MET | M-X15-1 "a majority of at least 2/3 either way; between 1/3 and 2/3 ... the label is mixed"; M-X15-3 requires the existing pins to pass unchanged. |
| CO5 | Explicit out of scope | MET | Section 2 closing: "Nothing else in the core or in the other named modules changes"; "the only seam B allows is a read-only adapter"; section 6 "Neither future consumer depends on B's choice". |
| CR1 | No factual errors | MET | Re-read and held: SKILL.md:1439, :1537, :1567, :1608, :1610, :1614-1615; 139 rows and 12 tasklist rows; archive headers (v3.66 line 6, test1 line 7); map accepted by v1 and v2. Line-range slips (`prompts.py:28-62` for definitions at 49-69; `_tasklist_ready_consistent` `:195-233` vs 240) still contain the true claim and are minor. |
| CR2 | Approaches feasible | MET | The High/Medium/Low map satisfies `blocking == (severity != MINOR)` (`findings_v2.py:161-162` verified); P2 loop left as it is; adapter seam is read-only. |
| CR3 | Terminology consistent | MET | Keeps the skill's "Medium" and the CLI's "MEDIUM" distinct and names the collision with the S1-S5 Medium (E4, section 4). |
| CR4 | No internal contradictions | NOT MET | Sections 1 and 2 call Medium-as-blocking "the tasklist skill's own model, which pragmatic.md S4 permits", while section 8 concedes "the skill states no model and no definition of Medium (E4, E6), and B adds both". |
| CR5 | Claims supported | MET | E1-E9 each carry line cites and tags; E6 and E7 quote the archived reports (verified: M2 "T01.03 omits Developer Guide Section 9.7"; header counts). The "mostly an omitted ... requirement" wording in section 8 is tagged UNVERIFIED as a general fact in E6. |
| ST1 | Logical ordering | MET | 1 position, 2 design, 3 evidence, 4 invariants, 5 tests, 6 effects, 7 slot consistency, 8 objection. |
| ST2 | Consistent hierarchy depth | MET | Flat: 8 H2 and no H3, so no orphaned subsections. |
| ST3 | Separation of concerns | MET | Design, evidence, invariants, tests, downstream effects and slot consistency are separate sections. |
| ST4 | Navigation aids | MET | Evidence labels E1-E9 cross-referenced ("(E4, E6)", "E5"), measurement ids M-X15-1..4, "section 7 below". |
| ST5 | Follows artifact conventions | MET | Same proposal shape the brief fixes (position, consequence, evidence, invariants, test, effects, consistency, objection). |
| CL1 | Unambiguous language | NOT MET | Section 8 ends "the right move is to redefine Medium (and possibly demote it), which this proposal does not rule out and does not pre-judge", a hedge on the decision point itself. |
| CL2 | Concrete, not abstract | MET | Concrete map "High -> CRITICAL blocking true; Medium -> MAJOR blocking true; Low -> MINOR false", M-X15-1..4, pinned sites. Caveat: the Medium definition B promises to add is not written out. |
| CL3 | Section purpose clear | MET | Each section is summarizable in one sentence, e.g. section 7 "Consistency with the adjudicated slots C-01, C-02 and C-03". |
| CL4 | Terms defined on first use | MET | Header defines the evidence tags; INV codes glossed in section 4 ("INV-J (binary blocking, Medium non-blocking among minor findings, at most 2 fix cycles ...)"); S4 is quoted in E4. |
| CL5 | Actionable next steps/decisions | MET | M-X15-1 decision rule with thresholds and the stated stop condition "if M-X15-1 finds that most Medium findings are wording or ambiguity ... the objection stands". |
| RK1 | At least 3 risks with probability and impact | NOT MET | Section 4 "Endangered" list rates impact on two items only ("(MEDIUM)", "(LOW to MEDIUM)") and gives no probability for any. |
| RK2 | Mitigation for each risk | NOT MET | "One product, two meanings" is accepted ("does not remove it") and "new skill text that no test yet pins" has no mitigation. |
| RK3 | Failure modes and recovery | MET | Section 4: a stalled Medium "ends in a human decision" via the monotonicity halt, the 2-pass cap and `blocked` under `--unattended` (SKILL.md:1610-1615 verified); INV-I preserved. |
| RK4 | External dependencies and failure | MET | Section 7 reopening conditions for C-01, C-02, C-03; E9 shared `SPEC_FIDELITY_GATE` contract and schema (`spec_fidelity.schema.json:22,30` verified); E7 notes two reports are a small sample. |
| RK5 | Monitoring/validation mechanism | MET | M-X15-1..4, including M-X15-4 static check that no `Medium` token enters `findings.py`, `findings_v2.py`, `ledger.py` or the ledger JSON. |
| IE1 | Collection boundaries | MET | E7: a zero-blocking set (High 0) short-circuits at SKILL.md:1439; section 4 keeps the Stage 7 some-versus-zero gate and `synthetic-dnsp` HIGH. |
| IE2 | State interactions across boundaries | MET | Section 2: the map parses in both engines including with `reflect_category`; `card_convert.py` sends `medium` to MINOR so a converter must use the module map (verified lines 71-83). |
| IE3 | Guard condition gaps | MET | Section 4: "a tasklist reviewer that types `MAJOR` with `blocking: false` drops the row. B relies on the module brief". |
| IE4 | Count divergence | MET | Section 2: the P2 loop "is not folded into the ledger's `cap_reviews` of 3, so the cap unit mismatch ... stays a documented difference"; E1 `F_k` counts High and Medium. |
| IE5 | Interaction effects | MET | Section 4: counting Medium as blocking "enlarges the set of rows that can stall a loop" under C-03's union; C-02's CRITICAL floor does not cover MAJOR. |

## Dimension subtotals

| Dimension | Variant A | Variant B |
|---|---|---|
| Completeness (CO1-5) | 5/5 | 5/5 |
| Correctness (CR1-5) | 3/5 (CR1, CR4 not met) | 4/5 (CR4 not met) |
| Structure (ST1-5) | 5/5 | 5/5 |
| Clarity (CL1-5) | 5/5 | 4/5 (CL1 not met) |
| Risk Coverage (RK1-5) | 3/5 (RK1, RK2 not met) | 3/5 (RK1, RK2 not met) |
| Invariant & Edge Case (IE1-5) | 5/5 | 5/5 |
| **Total** | **26/30** | **26/30** |

qual_score: A = 26/30 = 0.867; B = 26/30 = 0.867.

## Edge Case Floor check (Invariant & Edge Case Coverage >= 1/5)

- Variant A: 5/5, eligible as base.
- Variant B: 5/5, eligible as base.

## Notes for the reconciler (lowest-margin verdicts)

- CR1 (A, NOT MET) rests on code I re-read: the phrase "the unresolved High or Medium HALT resolves as blocked" occurs only in `src/superclaude/commands/tasklist.md:113` (grep over `src` and `plugins`), which the pin reads through `_unattended_section` (`tests/skills/test_worker_contract.py:893-906`); A names the skill and omits the command file. B has only minor line-range slips, so CR1 is MET for B.
- CR4 is NOT MET for both: A fact 13 versus section 7 answer 3; B sections 1-2 ("the skill's own model") versus section 8 ("the skill states no model").
- CL1 (B, NOT MET) is the thinnest call: one hedge ("possibly demote it ... does not pre-judge"). A's unset M1 threshold is an explicit deferral, not hedge wording, so it is not penalised under CL1.
- RK1 and RK2 are NOT MET for both under the same bar: neither gives probabilities, and each leaves at least one named cost without a mitigation.
- Not credited: the Round 2 hybrids (A+, H+), the A concessions (Form 2 withdrawn, union dropped) and B's re-reading of the archive (2 omissions, 2 dropped acceptance criteria, 1 contradiction, 1 assumption), none of which appear in the variant documents.
- Verified at HEAD (read-only): `findings.py:14,26,29,100-101`; `findings_v2.py:35-36,143-145,155-162`; `prompts.py:43-69,94-100`; `tasklist/gates.py:23-46`; `roadmap/gates.py:118-142,195-240,1322-1345`; `executor.py:189-244`; `commands.py:181-183`; `card_convert.py:71-83`; `SKILL.md:1351-1368,1384-1391,1420-1422,1439,1445,1478-1481,1531,1537,1567,1571,1608-1615`; `pragmatic.md:225-231`; fixture 139 rows and 12 `group: tasklist` (plan copy tracked, also 12); both archived ValidationReport headers; commit `80f934de5` message; `.dev/reflect/pre-removeTheAnyIssu-20261102054021/adversarial/merged-verdict.md` absent (B's claim holds).
