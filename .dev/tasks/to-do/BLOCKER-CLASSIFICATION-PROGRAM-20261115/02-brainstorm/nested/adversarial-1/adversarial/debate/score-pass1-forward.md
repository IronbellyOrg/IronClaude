# Score pass 1 (forward order: V1, V2, V3)

- Role: independent scorer, pass 1, forward order. I did not write or debate any variant.
- Status: complete. Only this file was written; no git write, nothing sent to GitHub, no Jev or TypeSafe call.
- Inputs read in full: the three variants, `diff-analysis.md` (V-01 to V-30 and its false-claim list), `invariant-probe.md`, `02-brainstorm/seed-brief.md`, and the scoring protocol. Measurements below were made with Grep and with read-only `uv run --no-project python -` scripts on the variant text (stdin scripts, no file written).
- Variants: V1 = `variant-1-opus-architect.md`, V2 = `variant-2-sonnet-analyzer.md`, V3 = `variant-3-haiku-backend.md` (all in the parent folder of this file).
- Protocol: `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` (A.1 quantitative, A.2 qualitative, CEV rules).

## Part A: Quantitative

### A1. Requirement coverage (RC)

Source requirements. The 'Required Spec Shape' paragraph (`seed-brief.md:53`) names 14 items separated by semicolons. Three of them join two items with "and" and are split to give the 17 named items: goals / non-goals, one-source-of-truth design / primitives that keep their own scale, metrics / revert triggers. R18 and R19 are the two 'Success Criteria' bullets (`seed-brief.md:38-39`).

| Id | Requirement | V1 (heading) | V2 (heading) | V3 (heading) |
|---|---|---|---|---|
| R1 | Problem statement | Yes (1) | Yes (1, plus 2 root cause) | Yes (1) |
| R2 | Goals | Yes (2, Goals G1-G6) | Yes (3, Goals G1-G7) | Yes (2, Goals 1-8) |
| R3 | Non-goals | Yes (2, Non-goals) | Yes (3, Non-goals) | Yes (2, Non-goals) |
| R4 | Rule in plain words, three conditions, never-downgraded class | Yes (3) | Yes (4.1) | Yes (3) |
| R5 | Record-and-offer behaviour (flow, ledger, offer wording, unattended, batching) | Yes (4.1-4.5) | Yes (6.1-6.7) | Yes (4.1-4.6) |
| R6 | Classifier concept and Jev use (questions, truth table, confidence, key, fallback, shadow) | Yes (5.1-5.5) | Yes (7.1-7.6) | Yes (5.1-5.5) |
| R7 | Guardrails against hiding real defects | Yes (6, R1-R10) | Yes (8, GR1-GR11) | Yes (6) |
| R8 | One-source-of-truth design: shared rule document and drift test | Yes (7.2-7.4, 10.2 T1-T3) | Yes (9.1, 9.2) | Yes (7) |
| R9 | Which primitives keep their own scale | Yes (7.5) | Yes (9.3) | Yes (7, model-family table) |
| R10 | Files and primitives that change, from Grep, with counts and patterns | Yes (9.1 P1-P8, 9.2) | Yes (10.1-10.4) | Yes (8) |
| R11 | Tests that pin the rule text and what changes | Yes (10) | Yes (11) | Yes (9) |
| R12 | Rollout stages | Yes (11) | Yes (12) | Yes (10) |
| R13 | Metrics | Yes (12, M1-M7) | Yes (13.1, M1-M10) | Yes (11) |
| R14 | Revert triggers | Yes (12, triggers 1-5) | Yes (13.2, RT1-RT8) | Yes (11, disable rules) |
| R15 | Risks | Yes (13, K1-K11) | Yes (14, R1-R13) | Yes (12) |
| R16 | Owner decisions, each with a recommendation | Yes (14, D1-D11) | Yes (15, D1-D13) | Yes (13) |
| R17 | What was verified and what was not | Yes (15) | Yes (16) | Yes (14) |
| R18 | Success criterion 1: spec states rule, record-and-offer flow, classifier with Jev and key, guardrails, Grep file list, tests, rollout, metrics, risks, decisions, verified and not | Yes (sections 3-15) | Yes (sections 4-16) | Yes (sections 3-14) |
| R19 | Success criterion 2: every claim about a file, count or line is from a live Read or Grep | No: claims it says it did not re-read (15.3 "taken from the enrichment files, not re-read", e.g. `validate_prompts.py:130`); "81 source files (checked count)" not reproduced (V-28: 58) | No: many line claims tagged [E], not re-read (10.3 "rf-qa 398, 402 to 415, 549 [E]"; 16.3 says so) | No: 8 "Additional integration sites from those searches and the supplied enrichment" (enrichment, not live); "The enrichment identifies eight rule or severity pin modules" (9) |

| Variant | Matched | Total | RC |
|---|---|---|---|
| V1 | 18 | 19 | 0.947 |
| V2 | 18 | 19 | 0.947 |
| V3 | 18 | 19 | 0.947 |

Note: V3 is closest to R19 (every count and line it states is marked "Live" and was reproduced by V-01, V-02, V-06), but it still carries file claims sourced to the enrichment, so the binary match is No.

### A2. Internal consistency (IC)

Sample method: 30 falsifiable claims per variant (a path, count, line, threshold, or a must/never/only rule), taken as the first two such statements of each H2 section in document order, continuing in later sections until 30. Each sampled claim and each diff-analysis contradiction row (X-001 to X-013) was then searched for a contradicting statement anywhere inside the same variant. Only within-variant contradictions count; false claims against the repository are scored under correctness.1, not here. The denominator is the fixed sample of 30, as the brief requires.

Contradictions found:

| Variant | # | Statement A | Statement B | Source |
|---|---|---|---|---|
| V1 | 1 | 3 class table: NOTE example "a table-pipe defect that changes no cell a later phase reads (NEW-1, NEW-2)" | 3 table-shape rule: "A pipe that splits a column a parser reads is condition 1"; the same row is disputed and "the rule must name the reader of the cell" | diff-analysis X-011 ("under V1's own table-shape rule the row is condition 1 if a parser reads that cell") |
| V1 | 2 | 6 R4: "if the reviewer or the classifier cannot tell, the outcome is SHOW_USER, never FOLLOW_UP" | 5.2: the sketch's `wrong()` returning N when E is UNSET "is the more useful behaviour" (an unanswered E then yields NOTE or FOLLOW_UP; invariant-probe INV-007: `verdict(N,N,N,N,UNSET,Y)` = NOTE) | found by this scorer, confirmed by INV-007 |
| V2 | 1 | 4.2 table: consequence "could not be established: Medium, tagged `consumer-unknown`" (non-blocking, not sent to a person at the gate); 4.3 "every finding is `consumer-unknown` and lands as Medium" | 7.3: "UNSET means 'send to a person'"; 7.6 item 3: with D UNSET "nearly every wrong-outcome row lands in SHOW_USER" (same situation, no decision basis, two different outcomes) | found by this scorer; related to diff-analysis X-003 and X-007 |
| V2 | 2 | 11: "I confirmed that the nine paths below exist" | the table directly below lists 8 test modules | found by this scorer |
| V3 | none | | | |

| Variant | Contradictions | Claims | IC |
|---|---|---|---|
| V1 | 2 | 30 | 1 - 2/30 = 0.933 |
| V2 | 2 | 30 | 1 - 2/30 = 0.933 |
| V3 | 0 | 30 | 1 - 0/30 = 1.000 |

### A3. Specificity ratio (SR)

Sample method (deterministic): the body of each variant was filtered to non-blank lines longer than 25 characters that are not headings or table separator or column-header rows (V1 326 lines, V2 406, V3 492). Forty lines were taken at even spacing (index = floor(i x n / 40), i = 0 to 39). A regex pre-tagged a line concrete when it holds a digit, a backticked name, an all-capitals identifier or a file name; every line was then checked by hand against the protocol: concrete = numbers, named files, named tests, thresholds, measurable or testable criteria, named entities; vague = general principle, deferral or qualifier with no measurable referent; excluded = metadata, boilerplate lead-ins ("The Filings table has exactly these columns:") and table headers, per the protocol's exclusion rule.

Hand adjustments to the regex tags:
- V1: S08 ("one header block plus one table"), S18 (named Python tuple test list), S19 ("about six bullets"), S23 (named scale families) moved to concrete; S02 and S28 stay vague; S01 (status line), S20 (lead-in), S31 (table header) excluded.
- V2: S03 (Jev, Noul, Score defined), S09 (decision-table row), S11 (named code check) moved to concrete; S01 (status line) and S10 (table header) excluded.
- V3: S04, S05, S15, S16, S17, S18, S24, S26, S28, S35, S36, S37, S39 moved to concrete (each names a number, value set or testable rule); S07 ("The plan must choose and test one escaping convention", a deferral), S11, S12, S13, S14 ("materially changed"), S19, S23, S25 ("retention-bounded", no figure), S29, S38 ("Small historical sample") stay vague; S01, S09, S10, S31, S34 excluded.

| Variant | Sampled | Excluded | Concrete | Vague | SR |
|---|---|---|---|---|---|
| V1 | 40 | 3 | 35 | 2 | 35/37 = 0.946 |
| V2 | 40 | 2 | 38 | 0 | 38/38 = 1.000 |
| V3 | 40 | 5 | 25 | 10 | 25/35 = 0.714 |

### A4. Dependency completeness (DC)

Internal references counted: numbered section references ("section 7.5", "(8.2)", "Section 2.2"), references to the variant's own ids (D, R, K, M, T, P, B, L, G for V1; D, GR, RC, RT, M, T, L, G, R for V2), and positional pointers ("listed below") that point at document content. Excluded as external: section numbers of other documents (enrichment files, `jev-uses.md`, `rule-copies-and-tests.md`), labels belonging to other files (V1 lines 295-296 use stoprule B1-B3 and qa.md B1-B4), numbers that only look like section ids (V2 line 414 "3.0 percent", "2.0 percent"), and "above"/"below" used as comparisons ("above 0.20").

| Variant | Section refs (resolved/total) | Id refs (resolved/total) | Positional refs | Total resolved/total | DC |
|---|---|---|---|---|---|
| V1 | 20/20 | 68/68 (75 matches minus 7 external stoprule and qa.md labels) | 1/1 (line 15 "proposed below", resolved by 7.3) | 89/89 | 1.000 |
| V2 | 63/64 (unresolved: line 85 "loop and consolidation changes (section 4.6)"; section 4 ends at 4.5, the changes are in 4.4) | 69/69 | 3/3 (lines 22, 131, 467) | 135/136 | 0.993 |
| V3 | 0/0 (no numbered cross-references at all) | 0/0 (no ids) | 4/4 (lines 24, 104, 134, 458) | 4/4 | 1.000 |

Note: V3's 1.000 rests on a denominator of 4; it resolves everything it references but references almost nothing (see structure.4).

### A5. Section coverage (SC)

H2 headings counted with `^## `: V1 16 (sections 0 to 15), V2 18 (sections 0 to 16 plus 15b), V3 14 (sections 1 to 14). Max = 18.

| Variant | H2 | SC |
|---|---|---|
| V1 | 16 | 16/18 = 0.889 |
| V2 | 18 | 18/18 = 1.000 |
| V3 | 14 | 14/18 = 0.778 |

### A6. Quantitative score

quant_score = RC x 0.30 + IC x 0.25 + SR x 0.15 + DC x 0.15 + SC x 0.15

| Variant | RC x 0.30 | IC x 0.25 | SR x 0.15 | DC x 0.15 | SC x 0.15 | quant_score |
|---|---|---|---|---|---|---|
| V1 | 0.284 | 0.233 | 0.142 | 0.150 | 0.133 | 0.943 |
| V2 | 0.284 | 0.233 | 0.150 | 0.149 | 0.150 | 0.966 |
| V3 | 0.284 | 0.250 | 0.107 | 0.150 | 0.117 | 0.908 |

## Qualitative table

Evaluation order: V1, then V2, then V3, criterion by criterion. Binary, no partial credit; no cited evidence means NOT MET.

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| completeness.1 | NOT MET | NOT MET | NOT MET |
| completeness.2 | MET | MET | MET |
| completeness.3 | MET | MET | MET |
| completeness.4 | MET | MET | MET |
| completeness.5 | MET | MET | MET |
| correctness.1 | NOT MET | NOT MET | MET |
| correctness.2 | MET | MET | MET |
| correctness.3 | MET | NOT MET | MET |
| correctness.4 | NOT MET | NOT MET | MET |
| correctness.5 | MET | MET | MET |
| structure.1 | MET | MET | MET |
| structure.2 | MET | MET | MET |
| structure.3 | MET | MET | MET |
| structure.4 | MET | MET | NOT MET |
| structure.5 | MET | MET | MET |
| clarity.1 | MET | MET | NOT MET |
| clarity.2 | MET | MET | MET |
| clarity.3 | MET | MET | MET |
| clarity.4 | NOT MET | NOT MET | NOT MET |
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

### Completeness

- completeness.1 V1. CLAIM: covers all explicit requirements of the source is not met. EVIDENCE: RC table R19 is No (15.3 lists line claims "taken from the enrichment files, not re-read"; "81 source files (checked count)" is not reproduced, diff-analysis V-28 gives 58). VERDICT: NOT MET
- completeness.1 V2. CLAIM: not met. EVIDENCE: R19 is No (10.3 line numbers tagged [E], 16.3 "were not re-read"); diff-analysis coverage table: the open question "may the classifier fill `qa.md`'s four answers" is "Not answered". VERDICT: NOT MET
- completeness.1 V3. CLAIM: not met. EVIDENCE: R19 is No (8: "Additional integration sites from those searches and the supplied enrichment"); diff-analysis coverage: the 21-files reconciliation is only "Partly". VERDICT: NOT MET
- completeness.2 V1. CLAIM: edge cases and failure scenarios addressed. EVIDENCE: 6 R4 "Unknown is not minor"; 8.4 "an unsupported kind degrades to 'ask', not to 'hide'"; 13 K5 pointer unreadable, "ledger steps fail open (`ledger: unavailable`)". VERDICT: MET
- completeness.2 V2. CLAIM: met. EVIDENCE: 4.2 row "could not be established | Medium, tagged `consumer-unknown`, listed first in the offer"; 6.7 "If the agent finds that a picked Medium finding is in fact decision-bearing, it stops and says so". VERDICT: MET
- completeness.2 V3. CLAIM: met. EVIDENCE: 12 table rows "Ledger write denied, full disk or bad encoding", "Filing reply lost after remote success | Reconcile batch marker; never blind create retry". VERDICT: MET
- completeness.3 V1. CLAIM: dependencies and prerequisites included. EVIDENCE: 11 table "Entry criteria" column (stage 2: "stage 1 exit; owner approves D3, D4"); 5.4 "The key is a dependency of `JevJudge` only". VERDICT: MET
- completeness.3 V2. CLAIM: met. EVIDENCE: 7.5 judges table "Needs" column ("an API key; permission to send finding text off the machine"); 12 "No stage starts before the previous exit is met and the owner has seen the numbers". VERDICT: MET
- completeness.3 V3. CLAIM: met. EVIDENCE: 10 "A checked `/sc:workflow` plan must precede framework edits"; 5.4 "The supplied research reports a Bearer key dependency using `TYPESAFE_API_KEY`". VERDICT: MET
- completeness.4 V1. CLAIM: success criteria defined. EVIDENCE: 2 goals table column "How we know it is met"; 11 stage 2 exit "5 attended runs with metrics M1-M6 inside the revert thresholds". VERDICT: MET
- completeness.4 V2. CLAIM: met. EVIDENCE: 3 goals table column "How it is checked"; 12 stage 1 exit "At least 5 runs; ... zero safety misses in shadow". VERDICT: MET
- completeness.4 V3. CLAIM: met. EVIDENCE: 10 stage 1 "Ledger adapters, table and fixture judge pass missing-input, identity, persistence and filing-reconciliation cases without external calls". VERDICT: MET
- completeness.5 V1. CLAIM: out of scope stated. EVIDENCE: 2 Non-goals, e.g. "No automatic issue creation; no Jev API call, no account, no key request." VERDICT: MET
- completeness.5 V2. CLAIM: met. EVIDENCE: 3 Non-goals, e.g. "Extending `/sc:issue` in version 1" and "Raising or lowering the cap of 2 fix cycles." VERDICT: MET
- completeness.5 V3. CLAIM: met. EVIDENCE: 2 Non-goals, e.g. "No automatic issue creation, automatic acceptance of blockers, or extra review rounds." VERDICT: MET

### Correctness

- correctness.1 V1. CLAIM: no factual errors is not met. EVIDENCE: diff-analysis false-claim list: "read by path from 81 source files (checked count)" not reproduced (58, V-28); "In the plugin build: yes" for `rules/prompts` overstated (V-12); NEW-1 and NEW-2 as NOTE examples contradicted by `gate1-cycle-control.md:9`; T6 "monotone in every input" untrue across UNSET (V-17). VERDICT: NOT MET
- correctness.1 V2. CLAIM: not met. EVIDENCE: diff-analysis false-claim list: "UNSET means 'send to a person'" is false for S = UNSET (108 FOLLOW_UP and 108 NOTE states, V-17), a safety-relevant error; "Eight test modules pin the rule" incomplete (V-20, V-21). VERDICT: NOT MET
- correctness.1 V3. CLAIM: no factual error that matters. EVIDENCE: the one diff-analysis entry (`.claude/REVIEW-SEVERITY.md` as "the explicit development surface") is a proposed surface that V3 itself qualifies: "Neither currently gains a new file from this proposal" and "The implementation plan must add generation and parity checks"; its counts are confirmed (11 files, 12 files, 22 files and 120 lines, V-01, V-02, V-06) and its sketch claims are confirmed ("It can also return FOLLOW_UP with S UNSET", V-17; `wrong()` disagreement, V-18). VERDICT: MET
- correctness.2 V1. CLAIM: approach feasible within constraints. EVIDENCE: 5.1 "installed primitives must reach package behaviour through the `superclaude` CLI, never by a `src/superclaude/` path"; the `review` click group exists (V-29); the skill folder is synced by `make sync-dev` (V-09). VERDICT: MET
- correctness.2 V2. CLAIM: met. EVIDENCE: 9.1 option 1 `core/REVIEW-SEVERITY.md` "a new name is copied even on an existing install without `--force`" (confirmed V-11). VERDICT: MET
- correctness.2 V3. CLAIM: met. EVIDENCE: 7 "The core installer already globs Markdown files ... However the live development sync omits core, and plugin packaging copies rules but not core. The implementation plan must add generation" (consistent with V-09, V-11, V-12). VERDICT: MET
- correctness.3 V1. CLAIM: terminology consistent. EVIDENCE: 0 "Words used in this document" defines Gate, Primitive, Digest block, Shared rule package, Follow-up, Judge; FOLLOW_UP and NOTE are used for the two classes throughout sections 3 to 12. VERDICT: MET
- correctness.3 V2. CLAIM: terminology consistent is not met. EVIDENCE: 0 defines "R2" as "the run-2 task folder"; 14 reuses it as a risk id ("| R2 | The decision basis does not exist at upstream gates"), and section 4.3 uses "D" both for the classifier question and the decision ids D1-D13. VERDICT: NOT MET
- correctness.3 V3. CLAIM: met. EVIDENCE: 5.2 "UNSET, meaning not supplied or not answered" used the same way in 5.3; Items table "kind | `follow-up` or `note`" matches 3 ("follow-up", "notes"). VERDICT: MET
- correctness.4 V1. CLAIM: no internal contradictions is not met. EVIDENCE: IC table, 2 contradictions (3 NOTE example versus 3 table-shape rule; 6 R4 versus 5.2 `wrong()` endorsement). VERDICT: NOT MET
- correctness.4 V2. CLAIM: not met. EVIDENCE: IC table, 2 contradictions (4.2 `consumer-unknown` Medium versus 7.3 "UNSET means 'send to a person'"; 11 "nine paths below" versus 8 rows). VERDICT: NOT MET
- correctness.4 V3. CLAIM: met. EVIDENCE: IC table, 0 contradictions in the 30-claim sample and the X-001 to X-013 rows; e.g. 3 "Unknown is not no" agrees with 5.3 "Missing decisive inputs ... produce SHOW_USER". VERDICT: MET
- correctness.5 V1. CLAIM: claims supported. EVIDENCE: 0 "facts I re-checked live are marked '(checked)' and listed in section 15"; 15.1 table of 17 checks with method and result. VERDICT: MET
- correctness.5 V2. CLAIM: met. EVIDENCE: 0 evidence labels "[V] ... [E] ... [J] ... [U]" on every repository statement; 16.1 table of 18 spot checks. VERDICT: MET
- correctness.5 V3. CLAIM: met. EVIDENCE: 14 table of 12 load-bearing claims "spot-checked directly against live source in this session", plus "Corrections to inputs". VERDICT: MET

### Structure

- structure.1 V1. CLAIM: logical order. EVIDENCE: headings 1 problem, 2 goals, 3 rule, 4 record-and-offer, 5 classifier, 6 guardrails, 7 source of truth, 8 extension, 9 files, 10 tests, 11 rollout, 12 metrics, 13 risks, 14 decisions, 15 verified. VERDICT: MET
- structure.1 V2. CLAIM: met. EVIDENCE: 2 root cause precedes 3 goals and 4 rule; 5 worked examples follow the rule they apply; 15b order of work follows the decisions. VERDICT: MET
- structure.1 V3. CLAIM: met. EVIDENCE: headings 1 problem to 14 verification follow the seed brief order (3 rule before 4 record-and-offer before 5 classifier). VERDICT: MET
- structure.2 V1. CLAIM: consistent depth, no orphans. EVIDENCE: subsections 4.1-4.5, 5.1-5.5, 7.1-7.5, 8.1-8.5, 9.1-9.2, 10.1-10.2, 15.1-15.3; no section has a single child. VERDICT: MET
- structure.2 V2. CLAIM: met. EVIDENCE: subsections 2.1-2.3, 4.1-4.5, 6.1-6.7, 7.1-7.6, 8.1-8.4, 9.1-9.3, 10.1-10.4, 13.1-13.2, 16.1-16.3; no single-child section. VERDICT: MET
- structure.2 V3. CLAIM: met. EVIDENCE: subsections 4.1-4.6 and 5.1-5.5; section 2 has two H3 children (Goals, Non-goals); others flat. VERDICT: MET
- structure.3 V1. CLAIM: separation of concerns. EVIDENCE: 7 (where the rule lives) is separate from 8 (extension contracts) and 9 (file list); 6 guardrails table is separate from 5 classifier. VERDICT: MET
- structure.3 V2. CLAIM: met. EVIDENCE: 4 rule, 5 worked examples, 6 record-and-offer, 7 classifier, 8 guardrails each hold one concern; loop changes sit in 4.4 with a cause column. VERDICT: MET
- structure.3 V3. CLAIM: met. EVIDENCE: 4 record-and-offer (ledger contract, states, mapping, offer, worker contract) is separate from 5 classifier and 6 guardrails. VERDICT: MET
- structure.4 V1. CLAIM: navigation aids present. EVIDENCE: 0 "How to read this variant" names the weight-bearing sections "(7), ... (8), ... (9) and ... (11)"; 20 numbered internal cross-references, all resolving (DC table). VERDICT: MET
- structure.4 V2. CLAIM: met. EVIDENCE: 0 "Short names used below" glossary and "Section 16 lists the spot checks"; 64 numbered internal cross-references (63 resolve). VERDICT: MET
- structure.4 V3. CLAIM: navigation aids is not met. EVIDENCE: No evidence found: no table of contents, no index, zero numbered cross-references (DC count 0/0); searched all 14 sections; only four "below" pointers (lines 24, 104, 134, 458). VERDICT: NOT MET
- structure.5 V1. CLAIM: follows spec conventions. EVIDENCE: 0 "Kind of document: requirements and design options only. No code."; numbered goals, requirements tables, decisions and verification sections. VERDICT: MET
- structure.5 V2. CLAIM: met. EVIDENCE: 0 "This is a requirements and design-options spec. It contains no implementation code."; numbered sections with goal, test, rollout and decision tables. VERDICT: MET
- structure.5 V3. CLAIM: met. EVIDENCE: header "Requirements and design options only."; 4.2 "Ledger contract, version 1" with required fields; 13 decisions table. VERDICT: MET

### Clarity

- clarity.1 V1. CLAIM: unambiguous language. EVIDENCE: Grep for "should consider", "as appropriate", "as needed", "might" finds one hit, 4.1 step 4 "because they might be blocking", which states the uncertainty that triggers SHOW_USER, not a hedged instruction. VERDICT: MET
- clarity.1 V2. CLAIM: met. EVIDENCE: the same Grep finds no hit; judgments are marked [J] instead of hedged (e.g. 2.3 "My reading, not a measurement [J]"). VERDICT: MET
- clarity.1 V3. CLAIM: not met. EVIDENCE: 3 "A real weakness without these consequences is a follow-up, called Medium where useful." and "a cosmetic pipe defect need not" leave when each applies undefined. VERDICT: NOT MET
- clarity.2 V1. CLAIM: concrete. EVIDENCE: 5.2 "auto-downgrade needs confidence at least 0.85; auto-confirm blocking needs 0.70"; SR 0.946. VERDICT: MET
- clarity.2 V2. CLAIM: met. EVIDENCE: 7.6 "with n = 30 and 27 agreements (90 percent), the 95 percent Wilson interval is about 74 to 96 percent"; SR 1.000. VERDICT: MET
- clarity.2 V3. CLAIM: met. EVIDENCE: 5.4 "a 10-second attempt, one retry for transient errors, and a 30-second total classifier budget per finding"; 4.2 fixed column lists; SR 0.714 (majority concrete). VERDICT: MET
- clarity.3 V1. CLAIM: each section has a clear purpose. EVIDENCE: 5 opens "This section adopts the design in `jev-uses.md` and adds only the architecture"; 8 opens "Every extension is 'add a row, satisfy a contract, the existing tests pick it up'". VERDICT: MET
- clarity.3 V2. CLAIM: met. EVIDENCE: 2.2 closes "Consequence for the design: a rewrite of `pragmatic.md:225` fixes RC1 only"; 8 opens "The failure to prevent: a real, decision-bearing defect is graded Medium or Note". VERDICT: MET
- clarity.3 V3. CLAIM: met. EVIDENCE: 1 "The intended result is a common decision contract, not a universal severity vocabulary."; 5.1 "A judge supplies language judgments; a local table decides their consequences." VERDICT: MET
- clarity.4 V1. CLAIM: acronyms defined on first use is not met. EVIDENCE: "MDTM templates" (7.3 table) and "synthetic DNSP HIGH" (7.5 table) are never defined; "Jev" first appears in 0 without a definition. VERDICT: NOT MET
- clarity.4 V2. CLAIM: not met. EVIDENCE: 0 defines Jev, Noul, Score, F_0, R2, PF, but "the MDTM templates 01 and 02" (4.4 L4) and "WC-2", "WC-4" (6.4) are used undefined. VERDICT: NOT MET
- clarity.4 V3. CLAIM: not met. EVIDENCE: "SHOW_USER" is first used in 5.3 ("Missing decisive inputs ... produce SHOW_USER") with no definition. VERDICT: NOT MET
- clarity.5 V1. CLAIM: decision points identified. EVIDENCE: 14 table D1-D11, each with a recommendation (e.g. D10 "Delegate-only skill `sc-review-severity`"). VERDICT: MET
- clarity.5 V2. CLAIM: met. EVIDENCE: 15 table D1-D13 with "Recommendation" and "Why"; 15b "Order of work (for the `/sc:workflow` plan)". VERDICT: MET
- clarity.5 V3. CLAIM: met. EVIDENCE: 13 table of 10 decisions with "Recommendation and consequence". VERDICT: MET

### Risk coverage

- risk.1 V1. CLAIM: at least 3 risks with probability and impact. EVIDENCE: 13 table columns "Risk | Likelihood | Impact | Mitigation", K1 to K11 (e.g. K2 "high at first | medium"). VERDICT: MET
- risk.1 V2. CLAIM: not met. EVIDENCE: 14 table columns "Risk | Evidence | Mitigation"; R1 to R13 carry no probability or impact rating. VERDICT: NOT MET
- risk.1 V3. CLAIM: not met. EVIDENCE: 12 table columns "Failure | Required response"; no likelihood or impact (diff-analysis S-012: "11 failure modes with a required response, no likelihood"). VERDICT: NOT MET
- risk.2 V1. CLAIM: mitigation per risk. EVIDENCE: 13 "Mitigation" filled for K1 to K11 (e.g. K6 "T2 reverse scan finds unregistered copies"). VERDICT: MET
- risk.2 V2. CLAIM: met. EVIDENCE: 14 "Mitigation" filled for R1 to R13 (e.g. R4 "one offer per run, counts plus five rows, M7, RT8"). VERDICT: MET
- risk.2 V3. CLAIM: met. EVIDENCE: 12 "Required response" filled for all 11 rows (e.g. "Concurrent writer or resume overlap | Revision conflict; re-read and reconcile"). VERDICT: MET
- risk.3 V1. CLAIM: failure modes and recovery. EVIDENCE: 11 "Revert per stage: stage 1 is deletion of new files only. Stage 2 and 3 are 'set the affected registry rows back to v1 ...'". VERDICT: MET
- risk.3 V2. CLAIM: met. EVIDENCE: 12 stage table "Rollback" column ("restore the old block from git; keep the ledger"); 13.2 "A revert means: restore the previous block for the stage in force". VERDICT: MET
- risk.3 V3. CLAIM: met. EVIDENCE: 4.3 "A crash leaves either the old complete ledger or the new one"; 4.5 "After a timeout or crash, enter reconcile and search for that exact batch marker." VERDICT: MET
- risk.4 V1. CLAIM: external dependencies and their failure. EVIDENCE: 5.4 "Everything except `JevJudge` works without a key"; K8 privacy of TypeSafe; K5 plugin-only install. VERDICT: MET
- risk.4 V2. CLAIM: met. EVIDENCE: 14 R7 "Privacy, availability and cost of Jev ... the judge chain with a fallback; classifier advisory so an outage costs nothing". VERDICT: MET
- risk.4 V3. CLAIM: met. EVIDENCE: 5.4 "Privacy denial skips all unapproved external judges"; "Authentication failures skip retries; a run-local circuit breaker". VERDICT: MET
- risk.5 V1. CLAIM: monitoring for risk detection. EVIDENCE: 12 M3 "escaped-defect rate ... sampled audit R6", M7 "drift test failures on master". VERDICT: MET
- risk.5 V2. CLAIM: met. EVIDENCE: 8.2 measured false-negative audit with strata and sample size; 13.2 RT1 to RT8. VERDICT: MET
- risk.5 V3. CLAIM: met. EVIDENCE: 11 "Proposed pilot audit: all safety disagreements plus at least ten non-blockers per pilot run". VERDICT: MET

### Invariant and edge case coverage

- invariant.1 V1. CLAIM: collection boundaries. EVIDENCE: 4.3 "when F is 0 and M is under a threshold (owner decision D5, recommended 10) the offer is one line"; 4.5 "above a small count (recommended 5) the session should suggest option 2". VERDICT: MET
- invariant.1 V2. CLAIM: met. EVIDENCE: 6.2 "The offer shows counts and the first five rows, never the whole list"; Note rows short "so the file does not grow into the 838-line marker pile". VERDICT: MET
- invariant.1 V3. CLAIM: met. EVIDENCE: 4.1 "A header-only ledger is valid and records zero findings"; 4.2 "This table exists even for a single finding"; 11 "or all when fewer exist". VERDICT: MET
- invariant.2 V1. CLAIM: state interactions across components. EVIDENCE: 4.1 step 5 "The user's answer is written back into each row's `status` column, so a re-run never offers or files a row twice"; ledger header `rule_version`; K9 per-carrier versions. VERDICT: MET
- invariant.2 V2. CLAIM: met. EVIDENCE: 6.2 "`FU-<gate>-<n>`, stable across reviews of the same gate"; 4.4 L5 "A fix that touches a Medium row's location does not reopen it". VERDICT: MET
- invariant.2 V3. CLAIM: met. EVIDENCE: 4.3 "Each rewrite checks expected revision ... A stale writer reads the current revision before retrying; it never overwrites newer answers." VERDICT: MET
- invariant.3 V1. CLAIM: guard gaps identified. EVIDENCE: 5.2 "The sketch's `wrong()` ... returns N when one of W and E is N and the other is UNSET"; 6 R8 "unverified evidence cannot support an auto-downgrade". VERDICT: MET
- invariant.3 V2. CLAIM: met. EVIDENCE: 7.3 "The check skips every transition that starts or ends at UNSET"; 8.1 GR2 "A finding without `rests_on` is invalid". VERDICT: MET
- invariant.3 V3. CLAIM: met. EVIDENCE: 5.3 "It can also return FOLLOW_UP with S UNSET because only unsettled S is lifted"; 5.2 "Accept only finite probabilities between zero and one". VERDICT: MET
- invariant.4 V1. CLAIM: count divergence covered. EVIDENCE: 9.1 "The 21 is a count of listed paths, not of copies ... 8 do not carry the definition"; P6 row "22 | 120 lines". VERDICT: MET
- invariant.4 V2. CLAIM: met. EVIDENCE: 2.2 RC5 "838 times (825 matching lines) ... raw counts, not de-duplicated"; 13.2 RT2 "3 of 60 gives a lower bound of about 1.7 percent; 4 of 60 about 2.6 percent". VERDICT: MET
- invariant.4 V3. CLAIM: met. EVIDENCE: 5.3 "Thresholds and their inclusive boundaries must be versioned"; 8 "22 files and 120 matching lines, not 120 literal occurrences"; 6 "do not lower counts by relabeling duplicates". VERDICT: MET
- invariant.5 V1. CLAIM: feature interaction effects. EVIDENCE: 13 K9 "Mixed meanings during rollout (stage 2 carriers on v2, templates on v1)"; 6 R9 re-review only when a fix edits a blocking span. VERDICT: MET
- invariant.5 V2. CLAIM: met. EVIDENCE: 2.2 RC2 "With 15 reviewers per gate, the chance that at least one calls a borderline item blocking approaches 1"; 14 R10 "A machine can hold the new shared document and an old `pragmatic.md`". VERDICT: MET
- invariant.5 V3. CLAIM: met. EVIDENCE: 7 "A consumer missing the required version retains the old gate"; "Existing non-forcing installs can keep stale consumers; mixed versions must be detected." VERDICT: MET

## Subtotals

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4/5 | 4/5 | 4/5 |
| Correctness | 3/5 | 2/5 | 5/5 |
| Structure | 5/5 | 5/5 | 4/5 |
| Clarity | 4/5 | 4/5 | 3/5 |
| Risk coverage | 5/5 | 4/5 | 4/5 |
| Invariant and edge case | 5/5 | 5/5 | 5/5 |
| Total | 26/30 | 24/30 | 25/30 |
| qual_score | 0.867 | 0.800 | 0.833 |

Pass-1 combined, for reference only (0.5 x quant + 0.5 x qual; the final combined score uses the reconciled pass 1 and pass 2 verdicts): V1 0.905, V2 0.883, V3 0.871.

## Edge case floor

| Variant | Invariant dimension | Floor (at least 1 of 5) | Eligible as base |
|---|---|---|---|
| V1 | 5/5 | met | yes |
| V2 | 5/5 | met | yes |
| V3 | 5/5 | met | yes |

No variant is below the floor; the floor is not suspended.

Caveat for the reconciler: the invariant criteria score whether a variant addresses each class, not whether it closes the gaps `invariant-probe.md` found; INV-007 (unanswered E), INV-023 (pipe codec) and INV-026 (posted body and batch marker) remain open across all three.
