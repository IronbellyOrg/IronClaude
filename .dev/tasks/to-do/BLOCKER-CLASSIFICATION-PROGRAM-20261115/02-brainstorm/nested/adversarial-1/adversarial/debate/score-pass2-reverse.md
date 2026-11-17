# Qualitative scoring, pass 2 (reverse order: V3, then V2, then V1)

- Role: independent scorer. Qualitative layer only (30 binary criteria, Claim-Evidence-Verdict).
- Status: complete. Only this file was written; no git write, nothing sent to GitHub, no Jev or TypeSafe call.
- Variants: V1 = `variant-1-opus-architect.md`, V2 = `variant-2-sonnet-analyzer.md`, V3 = `variant-3-haiku-backend.md` (all in this folder's parent).
- Inputs read: the three variants (V3, V2, V1 in that order), `diff-analysis.md`, `invariant-probe.md`, `02-brainstorm/seed-brief.md`, the rubric in `sc-adversarial-protocol/SKILL.md` (Qualitative Scoring Layer) and `refs/scoring-protocol.md`. No other scorer's file was read.

## Qualitative table

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| completeness.1 | MET | NOT MET | NOT MET |
| completeness.2 | MET | MET | MET |
| completeness.3 | MET | MET | MET |
| completeness.4 | MET | MET | MET |
| completeness.5 | MET | MET | MET |
| correctness.1 | NOT MET | NOT MET | MET |
| correctness.2 | MET | MET | MET |
| correctness.3 | MET | MET | MET |
| correctness.4 | MET | MET | MET |
| correctness.5 | MET | MET | MET |
| structure.1 | MET | MET | MET |
| structure.2 | MET | MET | MET |
| structure.3 | MET | MET | MET |
| structure.4 | MET | MET | NOT MET |
| structure.5 | MET | MET | MET |
| clarity.1 | MET | MET | MET |
| clarity.2 | MET | MET | MET |
| clarity.3 | MET | MET | MET |
| clarity.4 | NOT MET | MET | NOT MET |
| clarity.5 | MET | MET | MET |
| risk.1 | MET | NOT MET | NOT MET |
| risk.2 | MET | MET | MET |
| risk.3 | MET | MET | MET |
| risk.4 | MET | MET | MET |
| risk.5 | MET | MET | MET |
| invariant.1 | MET | MET | MET |
| invariant.2 | MET | MET | MET |
| invariant.3 | MET | MET | MET |
| invariant.4 | MET | MET | MET |
| invariant.5 | MET | MET | MET |

## Evidence

Evaluated in reverse order. Within each criterion the lines run V3, then V2, then V1.

### Completeness

completeness.1 (covers all explicit requirements from the source input)
- V3. CLAIM: all seed-brief requirements, including every open question, are covered. EVIDENCE: all required sections present (diff-analysis coverage checklist), but the open question "Reconcile 21 files and 109 occurrences" is only stated as not reproduced (section 8: "The preamble's 21 files and 109 occurrences is not the result of that search"; section 14 corrections) without explaining the 21; diff-analysis marks it "Partly". VERDICT: NOT MET (no partial credit).
- V2. CLAIM: as above. EVIDENCE: all required sections present, but the open question "whether it may fill qa.md's four checklist answers" is not answered; D8 (section 15) covers only a "rests on" qualifier on `false-claim`; Grep of V2 for checklist-answer filling finds nothing; diff-analysis marks it "Not answered". VERDICT: NOT MET.
- V1. CLAIM: as above. EVIDENCE: diff-analysis checklist is Yes on every row; open questions answered in 5.5 and D8 (qa.md answers: no in v1), 9.1 (21 is a count of listed paths, 8 of 19 without the sentence), 5.3 (decision_basis), D1 and D2 (privacy, key). VERDICT: MET.

completeness.2 (edge cases and failure scenarios)
- V3. CLAIM: met. EVIDENCE: section 12 failure-mode table (model unavailable, full disk, concurrent writer, filing reply lost after remote success); 4.3 "A crash leaves either the old complete ledger or the new one". VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: section 5 case 14 (`consumer-unknown`), 4.2 table row "could not be established", 7.5 "A call error is never an N". VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: 7.4 "if neither surface can be read there, the step writes non-blocking findings into its own report as today and records `ledger: unavailable`"; 8.4 an unsupported deliverable kind "degrades to 'ask', not to 'hide'"; K1 to K11. VERDICT: MET.

completeness.3 (dependencies and prerequisites)
- V3. CLAIM: met. EVIDENCE: section 10 "A checked `/sc:workflow` plan must precede framework edits"; stage 0 "Inventory source and installed variants; validate 30-plus historical findings"; 5.4 key and owner privacy approval. VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: section 12 "No stage starts before the previous exit is met"; 7.5 judge table "Needs" column (API key, permission to send text). VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: section 11 "Entry criteria" column (stage 2 "stage 1 exit; owner approves D3, D4"); 5.4 "The key is a dependency of `JevJudge` only". VERDICT: MET.

completeness.4 (success or completion criteria)
- V3. CLAIM: met. EVIDENCE: section 10 header "Work and exit condition", stage 1 exit "pass missing-input, identity, persistence and filing-reconciliation cases without external calls"; section 9 acceptance-case list. VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: section 3 goals table "How it is checked"; section 12 "Exit criteria" column. VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: section 2 goals table "How we know it is met"; section 11 "Exit criteria" column. VERDICT: MET.

completeness.5 (explicit out of scope)
- V3. CLAIM: met. EVIDENCE: section 2 "Non-goals" (no code, no automatic issue creation, no conversion of missing evidence into proof). VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: section 3 "Non-goals" (35 percent target, no edits, no `/sc:issue` extension in v1, no Jev call, cap unchanged). VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: section 2 "Non-goals" (no code, caps unchanged, code-assigned scales unchanged, no automatic issue creation). VERDICT: MET.

### Correctness

correctness.1 (no factual errors or hallucinated claims)
- V3. CLAIM: no load-bearing false claim. EVIDENCE: the one diff-analysis entry for V3 (project `.claude/REVIEW-SEVERITY.md` as development surface) is a marked proposal, not a claim of existence: section 1 "New paths are explicitly marked proposed; they are not claims that files exist", section 7 "Neither currently gains a new file from this proposal" and "the live development sync omits core ... The implementation plan must add generation"; its sketch claims (S UNSET gives FOLLOW_UP, UNSET excluded from the monotonicity loop) and counts (120 lines, 139 occurrences) are confirmed by diff-analysis V-02, V-17 and C-014. VERDICT: MET.
- V2. CLAIM: no factual errors. EVIDENCE: 7.3 "State it as a design rule: UNSET means 'send to a person'" is false for the sketch it describes (diff-analysis: S = UNSET gives 108 FOLLOW_UP and 108 NOTE states; `verdict(N,N,N,N,N,UNSET)` = NOTE), and the error is safety-relevant; also "Eight test modules pin the rule" (section 11) is incomplete (V-20, V-21). VERDICT: NOT MET.
- V1. CLAIM: no factual errors. EVIDENCE: diff-analysis found four false or overstated V1 claims: "read by path from 81 source files (checked count)" (7.3; V-28 gives 58); "In the plugin build: yes" for `rules/prompts` (7.3; V-12); NEW-1 and NEW-2 as NOTE examples of a pipe defect "that changes no cell a later phase reads" (section 3; contradicted by `gate1-cycle-control.md:9`); T6 "monotone in every input" (10.2; X-008). VERDICT: NOT MET.

correctness.2 (approaches feasible with stated constraints)
- V3. CLAIM: met. EVIDENCE: 4.5 "Recommended v1: ... Pass that description through the existing create flow ... Do not invent a new supported command flag"; it names the missing adapter capabilities ("ledger parsing, write-back, duplicate-safe batches and consent binding") instead of assuming them. VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: 9.1 option 1 installs with no installer change (`install_core.py:58`, line 70 [V]); 6.5 option A "No change to `/sc:issue`"; 10.4 marks the L2 helper as new. VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: 5.1 CLI under the existing `review` click group ("checked: `cli/review/__init__.py:14`", confirmed by V-29 and INV-038); 7.3 skill folder synced by `Makefile:112-125`; 4.5 B1 needs no `/sc:issue` change. VERDICT: MET.

correctness.3 (terminology consistent)
- V3. CLAIM: met. EVIDENCE: the three condition names (Consequential error, Missing required work, Protected risk) and the classes "follow-up" and "note" are used the same way in sections 3, 4.2, 5.3 and 6. VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: section 0 table fixes Medium, Note, Decision basis, Consumer, Ledger; used consistently in 4.1, 6.2 and 8.1. VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: section 0 "Words used in this document"; FOLLOW_UP and NOTE used consistently in sections 3, 4.2, 5.2 and 7.5. VERDICT: MET.

correctness.4 (no internal contradictions)
- V3. CLAIM: met. EVIDENCE: cadence is stated once and held ("At loop completion, the attended top-level session offers the recorded set once", 4.1; "One offer covers the loop's final consolidated set", 4.5); unresolved classifier decisions are kept outside the non-blocking set in both 4.2 and 5.3. No opposing claims found. VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: "once per run, plus at any escalation halt" matches 6.1 step 5 and D2; `consumer-unknown` is non-blocking in 4.2, GR4 and section 5 case 14 alike. VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: the end-of-run offer with the SHOW_USER exception is the same in 4.1 step 4, 4.4 and D4; caps unchanged in section 2, section 3 and 7.4. VERDICT: MET.

correctness.5 (claims supported by evidence or rationale)
- V3. CLAIM: met. EVIDENCE: section 14 table of 12 live spot checks with source and result; section 8 states the Grep pattern behind each count. VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: every repo statement tagged [V], [E], [J] or [U] (section 0); section 16.1 lists 18 spot checks. VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: inline "(checked)" marks and the 17-row table in 15.1. VERDICT: MET.

### Structure

structure.1 (logical ordering)
- V3. CLAIM: met. EVIDENCE: problem, goals, rule (3), record-and-offer (4), classifier (5), guardrails (6), shared rule (7), files (8), tests (9), rollout (10). VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: root cause (2) precedes goals (3) and the rule (4), which precedes the worked examples (5) that apply it. VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: rule (3) before ledger (4) and classifier (5); shared package (7) before the extension points (8) that depend on its registry. VERDICT: MET.

structure.2 (consistent hierarchy, no orphaned subsections)
- V3. CLAIM: met. EVIDENCE: sections 2, 4 and 5 each hold two or more subsections (4.1 to 4.6, 5.1 to 5.5); no single-child subsection. VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: 2.1 to 2.3, 4.1 to 4.5, 6.1 to 6.7, 8.1 to 8.4, 13.1 and 13.2; the extra "15b" is a top-level section, not an orphan. VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: 4.1 to 4.5, 5.1 to 5.5, 7.1 to 7.5, 8.1 to 8.5, 10.1 and 10.2, 15.1 to 15.3. VERDICT: MET.

structure.3 (separation of concerns)
- V3. CLAIM: met. EVIDENCE: ledger contract (4.2), item states (4.3), offer (4.5) and worker return (4.6) are separate; judge contract (5.2) is separate from the decision table (5.3). VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: causes (2), rule (4), examples (5), ledger (6), classifier (7), guardrails (8) each hold one concern. VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: classifier layers L1 to L4 (5.1) separate questions, state builder, judges and decision; section 8 isolates extension contracts. VERDICT: MET.

structure.4 (navigation aids: table of contents, cross-references or index)
- V3. CLAIM: navigation aids present. EVIDENCE: no table of contents or index, and Grep of V3 for "section N" or "(N.N)" cross-references returns no matches; only local pointers such as "described below". Searched: whole file. VERDICT: NOT MET.
- V2. CLAIM: met. EVIDENCE: section 0 "How to read this spec" with a short-names table, and dense cross-references ("section 4.3", "section 8", "section 13"); one dangling reference ("section 4.6" in 2.2, where the loop changes are 4.4) does not remove the aids. VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: section 0 "How to read this variant" names which sections carry the weight; cross-references such as "section 7.5", "section 8.2", "listed in section 15". VERDICT: MET.

structure.5 (follows SPEC conventions)
- V3. CLAIM: met. EVIDENCE: carries every section of the seed brief's required spec shape (diff-analysis coverage checklist, every section row present). VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: same checklist, every required section present (sections 1 to 16). VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: same checklist, every required section present (sections 1 to 15). VERDICT: MET.

### Clarity

clarity.1 (unambiguous language)
- V3. CLAIM: met. EVIDENCE: Grep for "might", "should consider", "as appropriate", "as needed", "perhaps" returns no V3 match; rules use "must", "never", "only". VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: the same Grep returns no V2 match; hedged readings are labelled [J] rather than left as vague requirements. VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: one Grep hit, 4.1 step 4 "because they might be blocking", which gives the reason for an unambiguous instruction ("they are asked at the gate where they arise"), not a hedged requirement. VERDICT: MET.

clarity.2 (concrete rather than abstract)
- V3. CLAIM: met. EVIDENCE: 5.4 "a 10-second attempt, one retry for transient errors, and a 30-second total classifier budget per finding"; fixed column lists in 4.2. VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: section 5 table of 14 graded cases with the named consumer; 8.2 sample sizes ("5.0 percent at n = 60"). VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: 4.2 ledger paths per gate family and column list; 9.2 file and line table. VERDICT: MET.

clarity.3 (each section has a clear purpose)
- V3. CLAIM: met. EVIDENCE: each heading states its purpose ("Guardrails against hiding real defects", "Unattended worker return contract", "Metrics and revert triggers"); section 1 opens with the one-line problem. VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: section 0 summarises the three boldest choices and points to their sections; headings such as "Root cause: why the current rule over-blocks". VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: section 0 states the persona and which sections carry the weight; sections open with a one-line purpose (section 5 "adds only the architecture"). VERDICT: MET.

clarity.4 (acronyms and domain terms defined on first use)
- V3. CLAIM: terms defined on first use. EVIDENCE: Noul and UNSET are defined (5.1, 5.2), but SHOW_USER (first used in 5.3), "Gate 1" (section 1), the existing "Medium" class (section 3) and reflect's "Drift or Regression" (4.4) are used without definition; there is no glossary. Searched sections 1 to 5. VERDICT: NOT MET.
- V2. CLAIM: met. EVIDENCE: section 0 "Short names used below" table defines R2, PF, Gate 1/2/3, F_0 to F_2, P3-001, Medium, Note, Decision basis, Consumer, Ledger, Jev, Noul, Score, Truth table, Shadow mode; the RC, L, GR, M and RT ids are defined in their own tables. VERDICT: MET.
- V1. CLAIM: terms defined on first use. EVIDENCE: a section 0 glossary exists, but "DNSP" (7.5, "synthetic DNSP HIGH stays blocking") is never defined, the name "tau_down" (5.5, stage 4) is never defined, and "today's S4 bullet" (section 3) is used before S1 to S5 are defined in 7.1. VERDICT: NOT MET.

clarity.5 (actionable next steps or decision points)
- V3. CLAIM: met. EVIDENCE: section 13 decision table with a recommendation per row; section 10 "A checked `/sc:workflow` plan must precede framework edits". VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: section 15 D1 to D13, each with a recommendation and reason; 15b "Order of work" for the plan. VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: section 14 D1 to D11, each with a recommendation. VERDICT: MET.

### Risk coverage

risk.1 (at least 3 risks with probability and impact)
- V3. CLAIM: risks carry probability and impact. EVIDENCE: the section 12 table has only "Failure" and "Required response" columns; no likelihood or impact appears in sections 11 to 13 (diff-analysis S-012: "no likelihood"). VERDICT: NOT MET.
- V2. CLAIM: same. EVIDENCE: section 14 columns are Risk, Evidence, Mitigation; no probability or impact rating; the 2.2 "How sure" column rates causes, not risks. VERDICT: NOT MET.
- V1. CLAIM: met. EVIDENCE: section 13 table K1 to K11 with "Likelihood" and "Impact" columns (K1 "medium", "high"). VERDICT: MET.

risk.2 (mitigation per risk)
- V3. CLAIM: met. EVIDENCE: every section 12 row has a "Required response" ("Concurrent writer or resume overlap: Revision conflict; re-read and reconcile"). VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: section 14 "Mitigation" column filled for R1 to R13. VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: section 13 "Mitigation" column filled for K1 to K11. VERDICT: MET.

risk.3 (failure modes and recovery)
- V3. CLAIM: met. EVIDENCE: 4.5 "After a timeout or crash, enter reconcile and search for that exact batch marker. Never retry creation until absence or the existing issue has been established"; section 11 "Revert policy and thresholds, never erase ledgers". VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: section 12 "Rollback" column per stage; 13.2 RT1 to RT8 with "A revert means: restore the previous block". VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: section 11 "Revert per stage" paragraph; section 12 revert triggers 1 to 5. VERDICT: MET.

risk.4 (external dependencies and their failure)
- V3. CLAIM: met. EVIDENCE: 5.4 "Fallback order is approved Jev, approved independent language-model judge, reviewer label"; "Without a key, fall back immediately"; circuit breaker; section 12 rows "Model unavailable" and "Network judge denied by privacy policy". VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: 7.5 judge table with key and privacy needs; "If the last judge is the only one left, the reviewer's label stands"; R7. VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: 5.4 key dependency and judge chain; K8 privacy; D1 and D2. VERDICT: MET.

risk.5 (monitoring or validation for risk detection)
- V3. CLAIM: met. EVIDENCE: section 11 metrics list and "Proposed pilot audit: all safety disagreements plus at least ten non-blockers per pilot run". VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: 8.2 measured false-negative audit, 8.3 seeded-defect recall, 13.1 M1 to M10. VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: R6 sampled audit; section 12 M1 to M7, including M3 escaped-defect rate and M7 drift test failures. VERDICT: MET.

### Invariant and edge case coverage

invariant.1 (collection boundaries: empty, single, maximum)
- V3. CLAIM: met. EVIDENCE: 4.1 "A header-only ledger is valid and records zero findings, not missing execution"; 4.2 "This table exists even for a single finding". VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: 6.2 "The offer shows counts and the first five rows, never the whole list" and short Note rows so the file does not grow into "the 838-line marker pile"; 6.5 option B rejected for 108 findings; 4.5 a review with no finding is still valid. VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: 4.3 "when F is 0 and M is under a threshold ... the offer is one line ... and asks nothing"; 4.5 "above a small count (recommended 5) the session should suggest option 2 instead". VERDICT: MET.

invariant.2 (state variable interactions across component boundaries)
- V3. CLAIM: met. EVIDENCE: 4.1 "The run owner is the only ledger writer ... Nested runs have separate ledgers"; 4.3 expected-revision check and stale-writer re-read; section 7 "A running loop pins its rule version". VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: 6.1 step 6 "Filing writes the issue number back into the ledger rows"; 6.4 ledger path in the worker `artifacts`; R5 "the coordinator never opens it" with a mitigation. VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: 4.1 step 5 status written back "so a re-run never offers or files a row twice"; 7.3 registry rows with stage and digest version per carrier; K9 mixed versions recorded in the ledger header `rule_version`. VERDICT: MET.

invariant.3 (guard condition gaps)
- V3. CLAIM: met. EVIDENCE: 5.3 "It can also return FOLLOW_UP with S UNSET because only unsettled S is lifted. That permits a missing safety answer to look safer"; 5.2 "Accept only finite probabilities between zero and one ... Duplicate IDs, missing required answers, wrong request ID or malformed output are failures". VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: 7.3 table "The check skips every transition that starts or ends at UNSET" with 432 lowering moves; GR2 "A finding without `rests_on` is invalid". VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: 5.2 names the `wrong()` mismatch with `jev-uses.md`; 5.3 "no review output carries that list today", so D is UNSET; R8 "unverified evidence cannot support an auto-downgrade". VERDICT: MET.

invariant.4 (count divergence: off-by-one, inclusive or exclusive ranges)
- V3. CLAIM: met. EVIDENCE: 5.3 "Thresholds and their inclusive boundaries must be versioned"; section 8 "22 files and 120 matching lines, not 120 literal occurrences. The enrichment's 139 occurrences counts repeated matches within lines". VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: 2.2 RC5 "838 times (825 matching lines) in 64 files"; 13.2 RT2 "3 of 60 gives a lower bound of about 1.7 percent; 4 of 60 about 2.6 percent". VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: 9.1 pattern table P1 to P8 with files versus occurrences; reconciliation of 21 paths versus 11 files; 15.2 item 4, the Grep tool skipping gitignored folders (0 versus 6 copies). VERDICT: MET.

invariant.5 (interaction effects when components combine)
- V3. CLAIM: met. EVIDENCE: section 7 "Existing non-forcing installs can keep stale consumers; mixed versions must be detected" and "A consumer missing the required version retains the old gate"; the section 7 model-family table keeps specialized protocol policy. VERDICT: MET.
- V2. CLAIM: met. EVIDENCE: R10 "A machine can hold the new shared document and an old `pragmatic.md`"; RC6 "The word means different things in different primitives". VERDICT: MET.
- V1. CLAIM: met. EVIDENCE: K9 "Mixed meanings during rollout (stage 2 carriers on v2, templates on v1)"; section 1 item 2, `card_convert.py` versus rf-qa meaning of IMPORTANT. VERDICT: MET.

## Subtotals

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 5/5 | 4/5 | 4/5 |
| Correctness | 4/5 | 4/5 | 5/5 |
| Structure | 5/5 | 5/5 | 4/5 |
| Clarity | 4/5 | 5/5 | 4/5 |
| Risk coverage | 5/5 | 4/5 | 4/5 |
| Invariant and edge case coverage | 5/5 | 5/5 | 5/5 |
| Total | 28/30 | 27/30 | 26/30 |
| qual_score | 0.933 | 0.900 | 0.867 |

## Edge case floor

| Variant | Invariant dimension | Eligible as base |
|---|---|---|
| V1 | 5/5 | Yes |
| V2 | 5/5 | Yes |
| V3 | 5/5 | Yes |

No variant is below 1 of 5, so the floor excludes none and is not suspended. Note for the merge: the invariant probe lists 24 unaddressed items against the consensus (for example INV-007 E UNSET counted as not wrong, INV-023 no chosen pipe codec, INV-026 approved body not guaranteed to be what `/sc:issue` posts); these are gaps in the combined design, not grounds to lower any single variant below the floor.
