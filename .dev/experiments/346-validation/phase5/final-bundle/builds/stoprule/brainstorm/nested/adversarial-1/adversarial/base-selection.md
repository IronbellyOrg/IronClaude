# Base Selection Report

## Metadata

- Generated: 2026-11-08T15:40:00Z
- Variants: A = `variant-1-opus-architect.md` (opus:architect), B = `variant-2-sonnet-analyzer.md` (sonnet:analyzer), C = `variant-3-haiku-devops.md` (haiku:devops)
- Source: `.dev/brainstorms/346-stoprule/seed-brief.md`
- Debate status: BLOCKED_BY_INVARIANTS at 92% agreement (`debate-transcript.md`, Convergence Assessment). Depth is standard, so the base is force-selected by the score below.
- Algorithm: `refs/scoring-protocol.md` A.1-A.5 (quant 50%, qual 50% over 30 binary criteria, dual-pass position-bias check, 5% tiebreaker).
- Scope note: variants are scored as written (their original text). Debate concessions are not credited to a variant's score. They feed the refactoring plan.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (opus:architect) | Variant B (sonnet:analyzer) | Variant C (haiku:devops) |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 1.000 (17 of 17) | 1.000 (17 of 17) | 1.000 (17 of 17) |
| internal_consistency | 0.25 | 0.991 (2 contradictions / 230 claims) | 0.983 (4 / 234) | 0.979 (3 / 141) |
| specificity_ratio | 0.15 | 0.830 (230 / 277 statements) | 0.836 (234 / 280) | 0.603 (141 / 234) |
| dependency_completeness | 0.15 | 1.000 (39 / 39 references) | 0.969 (31 / 32) | 1.000 (3 / 3) |
| section_coverage | 0.15 | 1.000 (8 H2 / 8) | 1.000 (8 / 8) | 1.000 (8 / 8) |
| **quant_score** | | **0.972** | **0.966** | **0.935** |

Formula: `quant = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC`. Unrounded: A 0.97238, B 0.96640, C 0.93507.

### Requirement list for RC (17 items, from the seed brief)

The seed brief has no formal requirement ids, so RC uses its 5 Constraints bullets, its 4 Success Criteria bullets and the 8 required sections. Each item was matched by keyword in the variant text.

| ID | Requirement (seed brief) | A | B | C |
|---|---|---|---|---|
| K1 | Additive variant `spec-panel-stoprule`; never edit `spec-panel.md`; builds on the 427 text | 3, 4 | 3.1, 3.6 | 3, 4 |
| K2 | Prefer mechanical enforcement; name the residual prose risk | 6.3 risk 7 | 2.6 table | 6 last paragraph |
| K3 | Canonical cap text; no `src/superclaude/` paths in installed primitives; UV for Python | 2.5, 3.6, 3.3, 4 | 2.5, 3.4, 2.3 | 2.5, 3 |
| K4 | Measurable on S1 with the same briefs plus a one-line name substitution | 4 | 4 (`perl` one-liner) | 4, 5 |
| K5 | Cost stated: extra agent calls, sessions, wall time | 6.2 | 6.1 | 6 |
| K6 | R3 open critical+major <= 3 in both replicates, or a clean PASS before review 3 | 5 | 5.3 | 5 |
| K7 | Growth after two fix cycles <= 44.4% | 5 | 5.3 | 5 |
| K8 | Verdict line reproducible by a script from the finding file alone | 5 falsifier 6 | 2.3 S10 | 2.5 |
| K9 | Sampled audit; the second grader demotes no more than a stated share of real defects | 5 (<= 20%) | 5.4 F2 (< 25%) | 5 (<= 10%) |
| K10-K17 | Sections 1-8 as required | all 8 | all 8 | all 8 |

RC does not separate the variants: all three reference every item. Whether a variant actually satisfies K4 under the saved briefs is a correctness question (X-001, X-011), scored in the qualitative layer.

### Computation notes

- **IC.** Scorable claims = the concrete statements counted for SR. Contradictions are the intra-variant conflicts the diff analysis and debate surfaced:
  - A (2): 2.1 "The coordinator's brief is unchanged apart from the command name" against 2.2's loop-directory files under the briefs' write-only-the-report rule (X-001, a requirement-constraint conflict); 6.1 "Minor-applying removed" against open question 3 (the reviser still reads the whole report, which shows the minor findings).
  - B (4): option (g) "authorize one extra cycle" against `begin` exit 4 (X-012); FR-8/FR-9 "MAJOR severity minimum" kept in the file against bullet 2 "not an automatic MAJOR" (X-005); open Q1 rejects a judged anchor while S5 adds the judged Q2 demotion (R1-A weakness 5, conceded in R2-B §1 A-5); section 8 reuses "the ratchet idea" while late blockers keep blocking (X-017, conceded in R2-B §1 A-8).
  - C (3): section 4 "no other review-brief edit" against 2.6's 13 files per round under write-only briefs (X-001); section 5 "Only substitute the command name" against 2.5's `fix-packet.md` routing (X-011, A-017); 2.1 "Copy these bytes unchanged into every reviewer, grader, and reviser brief" against the same "no other review-brief edit".
- **SR.** Table definition (concrete statements / all substantive statements). Statements are sentences or bullets of at least 4 words outside headings and code fences, with wrapped lines joined first. A statement is concrete if it holds a digit, inline code, a file name, a percent or comparison sign, an ALL-CAPS token of 3 or more characters, or a hyphenated identifier. The YAML alternative in the protocol (concrete / (concrete + vague)) gives A 1.000, B 0.991, C 0.954 and does not change the order. C's lower SR partly reflects prose without code formatting. It is a measured property of the text, not a judgement of C's ideas.
- **DC.** Internal references = section references (`section N`, `§N`, `(N.N)`), step ids (S0-S10) and risk or question numbers. External documents are excluded (B's "section 11" refers to `spec-panel-review-loop.md`). B's one unresolved reference is the term `asserted` in the 2.4 verdict code, which is used and never defined. C's 3 references all resolve: "described below" goes to section 5, "section 2.1", and the "M1-M5 definitions" are listed inline.
- **SC.** All three variants have exactly 8 H2 sections.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

CEV format per cell: the verdict (MET = 1, NOT MET = 0), then the evidence (a quote or section reference, or "no evidence found" with the sections searched). The claim is implied by the row ("<criterion> is met in Variant X"). A MET without citable evidence defaults to NOT MET.

### Completeness (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| Covers all explicit requirements | MET | All 17 RC items referenced (Quantitative table). | MET | All 17 RC items referenced. | MET | All 17 RC items referenced. |
| Addresses edge cases and failures | MET | 6.3 risks 1-11; S1 exit codes 3/5; "A card without a parsable line gets one re-spawn" (S5). | MET | 6.2 "Ways it could make the loop worse (each with its check)", 10 items; 3.4 failure cases. | MET | Section 6 failure table, 7 rows ("Helper crash, ENOSPC ..." to "Deadline/cap exhausted"). |
| Includes dependencies and prerequisites | MET | Section 4 "Host requirement: `uv` on the worker's PATH"; install path and Arm B briefs. | MET | 2.3 skill-base lookup order; section 4 install routes; open Q4 Agent `model` and `/tmp` preconditions. | MET | Section 4 deployment steps 1-7 ("Owner authorizes only these two destinations"). |
| Defines success or completion criteria | MET | Section 5 bar column and 6 falsifiers. | MET | 5.3 bar column, 5.4 F1-F7. | MET | Section 5 bars, "Acceptance ceiling: <=10% ...", falsification sentence. |
| Specifies out-of-scope items | MET | 3 "Not changed: `spec-panel.md` ... `HOW-WE-WORK.md` ... `plugins/superclaude/`"; 8 "reviews of code diffs ... are out of scope for v1". | MET | 3.6 "Not changed"; 3.5 "No `HOW-WE-WORK.md` row, no `/sc:help` entry and no plugin mirror". | MET | 3 "The existing original command, its tests, and installer implementation stay unchanged"; 8 "No claim is made that this additive variant addresses the four other incident toolchains". |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| No factual errors or hallucinated claims | NOT MET | Section 4: "reviser briefs are untouched (their 'apply confirmed findings' now resolves to the script-written list)". The T08 template fills its own id range, and flg-r2 applied N1-N11 while the report's brief named N1-N6 (R2-A §3.1, which A itself concedes). | NOT MET | 1 point 3 and 6.1 repeat "15 of 15 findings, 9 of them minor"; B's own concession 9 (R1-B) says `disposition-round2.md:35` totals 11 findings plus 4 citation rows. 3.1 bullet 6 "notes are not instructions" is defeated by the same T08 evidence (R2-B §1 A-9). | NOT MET | Section 4 "no other review-brief edit" while 2.5 requires the reviser to receive `fix-packet.md`; the saved T06/T08 name the report (X-011, conceded in R2-C §1 item 3). |
| Technical approach feasible under the stated constraints | NOT MET | 2.2 writes `findings-r<N>.json`, ledgers, cards and verdict files into a loop directory, while the S1 briefs say "write ONLY your output file" (X-001, conceded in R1-A concession 1). | MET | 2.0: "the report file is the only repository file written ... so the S1 briefs' 'write only this file' holds"; `/tmp` marked UNVERIFIED with a fail-closed exit 5 (6.2 risk 9). | NOT MET | 13 files per round under `.spec-panel-stoprule/<run-id>/` (2.6) and ERROR/HOLD terminal states against the brief's "binary PASS or FAIL verdict" (R1-B weakness 2a); the skill name `sc-spec-panel-stoprule` is removed by `install_skills.py:88-98` (S-005). |
| Terminology consistent | MET | `final` values `blocking`, `demoted`, `late-found`, `minor`, `reinstated` used the same way in S6, 2.6, 3.4 and 6.1. | MET | Claim statuses `confirmed`, `minor-form`, `late-found`, `minor`, `unconfirmed` (2.2) used consistently in 2.4, 2.6, 3.4. | MET | `claimed_severity`, `final_class`, `late-found`, ERROR, HOLD used consistently in 2.3-2.5 and section 6. |
| No internal contradictions (cross-check with IC) | NOT MET | IC found 2 (Computation notes). | NOT MET | IC found 4. | NOT MET | IC found 3. |
| Claims supported by evidence or rationale | MET | Dense `file:line` support, for example "`qa.md:141` ('The parent writes `sev=` ...')" (2.4) and `install_skills.py:13-21` (3.1 item 3). | MET | 5.1 replay table with per-claim baseline checks ("4.3 of 8") and arithmetic in 5.3. | NOT MET | Section 5 "PREDICTED, not measured: R3 confirmed critical+major = 2 and 3" with no count or replay behind it (R1-B weakness 3, conceded in R2-C §1 item 11). |
| **Subtotal** | **2/5** | | **3/5** | | **1/5** | |

### Structure (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| Logical section ordering | MET | Sections 1-8 in the required order; 2.1 architecture before 2.3 steps. | MET | Sections 1-8; 2.0 decisions before 2.1 parts and 2.3 steps. | MET | Sections 1-8; 2.1 rubric before 2.2-2.6 mechanics. |
| Consistent hierarchy depth | MET | H2 sections with H3 subsections 2.1-2.6, 3.1-3.7, 6.1-6.3; no orphaned H4. | MET | H3 subsections 2.0-2.7, 3.1-3.6, 5.1-5.4, 6.1-6.2; no orphans. | MET | H3 only under section 2 (2.1-2.6); no orphaned subsections. |
| Clear separation of concerns | MET | 2.1 role table: "Writes" and "Never writes" per role. | MET | 2.6 table "What is mechanical and what is prose". | MET | Separate subsections for rubric (2.1), snapshot (2.2), contract (2.3), gate (2.4), result (2.5), audit trail (2.6). |
| Navigation aids (cross-references) | MET | 39 internal references (section numbers, S0-S7 step ids, risk numbers). | MET | 31 resolved internal references, S0-S10 step ids. | NOT MET | 3 internal references in 420 lines and no step ids (DC computation). |
| Follows artifact-type conventions | MET | The 8 required sections, each titled as briefed. | MET | Same. | MET | Same. |
| **Subtotal** | **5/5** | | **5/5** | | **4/5** | |

### Clarity (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| Unambiguous language | MET | Rules stated as conditions with exit codes (S1-S6); estimates are labelled UNVERIFIED (6.2), not hedged. | MET | Exact field limits ("<=300 chars", "at least 8 words", "within 3 lines", S2). | NOT MET | 2.4 step 4 "Prefer a different available model class"; step 5 "when the dispatch supports that". |
| Concrete rather than abstract | MET | Literal rubric (3.2), schema (2.4), function list (3.4). | MET | Literal rubric (3.2), ledger schema (2.2), verdict code (2.4). | MET | Literal rubric (2.1), JSON schema (2.3), exit contract "0=completed PASS, 1=completed FAIL, 2=ERROR, 3=audit HOLD" (3). |
| Each section has a clear purpose | MET | Each H2 maps to one required section; 2.1 states the design in one table. | MET | 2.0 states the 4 decisions the variant commits to. | MET | Section 1 last bullet states the choice in one sentence. |
| Acronyms and domain terms defined on first use | NOT MET | Section 1 uses "R3", "427" and "S1" before any definition (S1 is described only in section 5). | NOT MET | Section 1 point 1 uses "R3" and "427" undefined; M1-M7 are defined, but only in 5.2. | NOT MET | Section 1 uses "S1", "R2/R3", "427"; section 5 cites "D10/D11" and "SLOs" without definition. |
| Actionable next steps or decision points | MET | 2.5 item 5 decision prompt per open finding; 8 promotion and retirement path. | MET | 5.1 "Gate before any live run: replay all six existing R3 reports"; 2.5 (g) decisions. | MET | Section 4 deployment steps 1-7 and rollback runbook. |
| **Subtotal** | **3/5** | | **3/5** | | **2/5** | |

### Risk Coverage (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| At least 3 risks with probability and impact | NOT MET | 11 risks with impact (6.3), but a probability only for risk 1 ("missed about half the time"). | NOT MET | 10 risks with checks (6.2), none with a probability; the 5.3 "chance bar met" column is about outcomes, not risks. | NOT MET | Failure table and risk paragraph (6) give results and actions, no probabilities. |
| Mitigation for each risk | MET | Each 6.3 item names a bound or a measure (for example risk 8 "`init` refuses a review 1 ... exit 9"). | MET | 6.2: every item ends with its check. | MET | Section 6 table: "Fail-safe result and operator action" per failure. |
| Failure modes and recovery | MET | S1 exits 3/5, S5 one re-spawn, S7 escalation. | MET | S2 "exit 3 once", S5 "A wrong canary rejects that batch (rerun once)". | MET | Section 6 table rows on helper crash, malformed envelope, grader unavailable, with recovery. |
| External dependency failures | MET | `grade=missing` (S5); `uv` requirement (4); grader `Read` access (6.3 risk 2). | MET | 3.2 "Agent tool unavailable -> ... verdict FAIL"; 6.2 risk 9 `/tmp` blocked. | MET | Section 7 transport and cancellation UNVERIFIED; section 6 ENOSPC and grader timeout. |
| Monitoring or validation mechanism | MET | 2.6 offline audit with `audit-report`; falsifier 6 re-runs the verdict. | MET | S10 `check`; M3 compliance metric; canaries. | MET | `events.jsonl` (2.6); SLOs and exports from result/events files (6). |
| **Subtotal** | **4/5** | | **4/5** | | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| Boundary conditions for collections | MET | S4 "With zero candidates S4 and S5 are skipped"; 3.6 "zero blocking gives PASS". | MET | S0 "First review: no baseline, no ratchet, no hunk list"; S3 "batches of at most 6 plus 2 canaries". | MET | 2.3 "more than 100 findings, or an input larger than 1 MiB as infrastructure ERROR"; 6 "skip an empty grader/audit batch". |
| State interactions across component boundaries | MET | S4 carried blockers "status is frozen"; S0 rubric hash per loop; 2.4 `spec_sha256` binds quotes to the reviewed text. | MET | S0 reads the prior sentinel for N, verdict and rubric hash; S2 seal hash. | MET | 2.2 binds run id, target, command, skill, rubric and model hashes per review. |
| Guard condition gaps identified | MET | S3 prior-status guard forces `open`; exit 7 `spec-mismatch`. | MET | S2 `resolved_by` must sit inside changed tokens, "else the status is forced to `open`"; S9 refuses a hand-typed verdict. | MET | 2.3 rejects duplicate keys, unknown fields, non-UTF-8; 3 rejects traversal and symlink escapes. |
| Count divergence (off-by-one, inclusive/exclusive) | MET | S1 exit 3 when "prior review is 3 (or higher) with FAIL"; S3 "the line before and after each pure deletion". | MET | S0 "N = prior N + 1, or 1"; S2 evidence "within 3 lines". | MET | 2.2 "N starts at 1 and cannot exceed 3"; "A crashed review consumes its reservation". |
| Interaction effects when features combine | MET | 6.3 risk 3 (ratchet laundering through an unrelated changed line) and risk 10 (FR-8/FR-9 relaxation with guard gaps). | MET | 6.2 risk 2 (quote rule with omission defects); open Q6 (`sites` may raise growth). | MET | 2.4 carried blockers with deleted quotes "stays as a historical carry anchor". |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B | Variant C |
|---|---|---|---|
| Completeness | 5/5 | 5/5 | 5/5 |
| Correctness | 2/5 | 3/5 | 1/5 |
| Structure | 5/5 | 5/5 | 4/5 |
| Clarity | 3/5 | 3/5 | 2/5 |
| Risk Coverage | 4/5 | 4/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 | 5/5 |
| **qual_score** | **24/30 = 0.800** | **25/30 = 0.833** | **21/30 = 0.700** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case score | Floor (>= 1/5) | Eligible as base |
|---|---|---|---|
| A | 5/5 | met | yes |
| B | 5/5 | met | yes |
| C | 5/5 | met | yes |

Note: every variant meets all five edge-case criteria as written. The 30 invariant-probe findings concern the merged consensus design, not any single variant, so they do not lower these scores. They are handled in `refactor-plan.md`.

## Position-Bias Mitigation

Pass 1 evaluated the variants in input order (A, B, C). Pass 2 evaluated them in reverse order (C, B, A) with fresh reads of the cited sections. 90 verdicts per pass (30 criteria x 3 variants). Pass 2 agreed with Pass 1 on 86. The 4 disagreements were each re-evaluated against both passes' evidence:

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final (re-evaluation) |
|---|---|---|---|---|---|
| Structure 4: navigation aids | C | NOT MET | MET | DISAGREE | NOT MET. Pass 2 credited C's numbered sections after reading B. Re-check: section numbers alone are not cross-references; C has 3 internal references in 420 lines and no step ids, against 31 in B and 39 in A. |
| Risk 1: probability and impact | B | NOT MET | MET | DISAGREE | NOT MET. Pass 2 read the 5.3 "Chance bar met" column (0.5, 0.8, 0.9) as risk probabilities. Re-check: those are outcome chances for the bars, not probabilities attached to the 6.2 risks. |
| Correctness 2: feasible under constraints | B | MET | NOT MET | DISAGREE | MET. Pass 2 applied B's own Round 2 admission that `/tmp` is outside the brief's letter (R2-B §3.4). Re-check: debate concessions are not scored (Metadata). As written, B marks `/tmp` UNVERIFIED, gives precedent (ctl-r1 R3 used `/tmp/ironclaude-batch.*`) and fails closed with exit 5 (6.2 risk 9). The criterion is met as written. |
| Correctness 5: claims supported | C | NOT MET | MET | DISAGREE | NOT MET. Pass 2 credited the evidence list in C section 1. Re-check: that list names reports but gives no count behind the section 5 predictions ("PREDICTED, not measured"), which the criterion requires. |

Disagreements re-evaluated: 4
Final verdicts changed from Pass 1: 0

### Note on order sensitivity

Pass 2 leaned toward MET on criteria where the previously read variant was weaker (reading C first made B's outcome probabilities and C's numbering look stronger). All four re-evaluations returned to the Pass 1 verdict, so position had no effect on the totals.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---|---|---|---|---|
| A (opus:architect) | 0.486 | 0.400 | **0.886** | 19 of 65 diff points won (29.2%) |
| B (sonnet:analyzer) | 0.483 | 0.417 | **0.900** | 32 of 65 diff points won (49.2%) |
| C (haiku:devops) | 0.468 | 0.350 | **0.818** | 6 of 65 diff points won (9.2%) |

Unrounded: A 0.88619, B 0.89987, C 0.81753.

**Margin**: B over A = 0.0137 (1.37 points), below the 5% (0.05) threshold. B over C = 0.0823, above it.
**Tiebreaker applied**: Yes (A.4 step 1, debate performance). B won 32 diff points and A 19 (`debate-transcript.md` Scoring Matrix; the 3 assumption dispositions and 5 unresolved points belong to no variant). The gap of 20.0 points (49.2% against 29.2%) is not within 5%, so step 1 decides: **B**. Steps 2 (correctness count, B 3/5 against A 2/5) and 3 (input order) were not needed. Step 2 would also have picked B.

Sensitivity: A leads B on quant by 0.006 and B leads A on qual by 0.033 (one rubric point). The base decision therefore rests on B's one extra correctness point (a feasible footprint under the S1 briefs) and on the debate outcome, which agrees with it.

## Selected Base: Variant B (sonnet:analyzer)

### Selection Rationale

- **Score.** B has the highest combined score (0.900), 0.014 above A (0.886) and 0.082 above C (0.818). The A/B margin is inside 5%, so the debate-performance tiebreaker decides it, and B won 32 diff points to A's 19.
- **Why B wins on the qualitative layer.** B is the only variant whose repository footprint fits the S1 briefs' "write ONLY your output file" rule: "the report file is the only repository file written" (B 2.0). A and C fail that correctness criterion (X-001, unanimous for B in both rounds). B is also the only variant whose predictions come from a count on the real R3 reports (5.1 replay, "4.3 of 8"), which A and C both adopted in Round 2 (R2-A §5 (d), R2-C §1 item 11).
- **Why the debate agrees.** Two of three advocates chose B as base (R2-B §5, R2-C §5), and the invariant-probe consensus describes the merged design as "B's storage and coverage, A's lifecycle guards, C's failure semantics" (`invariant-probe.md`, Emerging consensus).
- **Caveat.** A leads on the quantitative layer (0.972 against 0.966) because B has more intra-document contradictions (4 against 2). Three of B's four were conceded in Round 2 and are fixed by planned changes (X-005, X-012, X-017); the fourth (Q2) becomes advisory. The base is selected while convergence is BLOCKED_BY_INVARIANTS, so the merged spec must carry the 8 HIGH invariants (`refactor-plan.md`).

### Strengths to Preserve from Base

1. Report as the only file written, ledger embedded with a seal and sentinel, `finalize` writing the last line and refusing a hand-typed `verdict:`, and `check` re-deriving every status (B 2.0, 2.3 S9-S10). Adopt B's Round 2 in-report mode, which drops the `/tmp` scratch (R2-B §3.4).
2. Hunk coverage: every changed hunk needs a claim or a `checked` line, so silence never passes (B 2.3 S1-S2, 2.4; X-015).
3. One counted repair of form fields, exit 3 once, the second `seal` final (B S2; X-014).
4. A ledger whose grading path reads no reviewer severity word (B 2.2; X-006).
5. Canaries in every grader batch: 2 per batch from `refs/canaries.json` (4 blocking, 4 minor), wrong canary rejects the batch (B S3, S5, 3.2; U-011).
6. Measurement design: the 472-line Arm B base copy (sha256[:12] `c8d80346a96c`), the 5.1 replay with its gate ("a grader that demotes more than 3 of those 9 is miscalibrated"), the M1c unmodified probe review, and F1-F7 (B 4, 5.1-5.4; X-009, U-014, U-015).
7. Honest enforcement accounting: 2.6 "What is mechanical and what is prose" and 2.7 "Measured causes: removed and left".
8. `ratchet=off` recorded when `--baseline` is missing (B S0, section 4; X-010).
9. The one-line `perl` brief substitution with its `grep -c` check (B section 4).

### Strengths to Incorporate from Non-Base Variants

1. From A 2.3 S4: carried confirmed blockers are frozen and never re-graded (X-003, unanimous).
2. From A 2.3 S1 (U-002): recompute the prior review's verdict before review N, done in B as `check` on the prior report at `begin` (R2-B §5 item 1).
3. From A 3.1 item 4: edit the FR-8/FR-9 "MAJOR severity minimum" text in the copy and replace bullet 2 (`spec-panel.md:259`); keep FR-10 (X-005, unanimous).
4. From A 2.4: a `claimed` label kept for reporting only, so the recorder proxy survives (X-006 resolution, A-011).
5. From A 3.5 and 2.6: a grader model pinned in frontmatter, with `same-class` recorded; drop B's "a class different from your own" prose (X-016, unanimous).
6. From A 3.6 (U-006): the computed-diff drift test against `spec-panel.md`.
7. From A section 4 and B's R2 install check: plain `superclaude install` without `--force` for the `-protocol` skill (X-008), plus C 4's absence check and skill-first, command-last order.
8. From A section 8: "Do not reuse the stop rule" for `/sc:implement` (X-017).
9. From A R2 §3.1: confirmed ids numbered first and contiguously, the coordinator filling the T08 range and citation count from the script's brief; and from A R2 §3.6, the metric reads only the script's last line with the brief-rule verdict as a covariate.
10. From A 2.6 and C 5: a separate fresh auditor with the full spec and no grader reason; a reinstatement at a PASS candidate recomputes FAIL (X-007); C's two-sided offline sample that also covers confirmed blockers (U-026).
11. From C 3 and 4: fail closed with `E-SKILL-MISSING`, replacing B's 427 fallback (X-013).
12. From C 2.5: a user-authorized restart is a new run with the old run id as parent, replacing B's option (g) (X-012).
13. From C 6: infrastructure failure is not a document defect, expressed as FAIL reason codes inside the binary verdict; unconfirmed items never reach the reviser (X-002).
14. From C 2.4 step 2 (U-027): a prior link is valid only with an identical outcome hash and either an identical quote hash or a changed anchor.
15. From C 2.4 step 3: late-found claims graded in the same batch for the escalation, never blocking (X-004).
16. From C 2.5 (U-024): a fix-to-id disposition check against the `disposition-round2.md` the brief already requires, keeping the citation rows T08 demands (R2-C §3.1).
17. From C 2.3: "For an omission, quote the requirement or guard whose promised behavior is incomplete."
