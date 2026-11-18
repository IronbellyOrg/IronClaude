# Base Selection Report

Slot C-10 (pr-review-wire-format-and-slot). Variant A = `variant-1-original.md` (Proposal A, adapter now, separate pre-step). Variant B = `variant-2-original.md` (Proposal B, one wire format, panel as third reviewer). Scored as written (the original proposals); debate results enter through Correctness evidence and the tiebreaker. Three scorers: Pass 1 (`scoring-pass1.md`, input order A then B), Pass 2 (`scoring-pass2.md`, reverse order B then A) and a re-evaluation scorer (`scoring-reeval.md`) that settled every disagreement and re-computed the quantitative layer once under one counting rule per metric. The full Claim-Evidence-Verdict tables of Pass 1 and Pass 2 are reproduced in Appendix 1 and Appendix 2 below.

## Quantitative Scoring (50% weight)

Why a re-computation was needed: the metrics are meant to be mechanical, but Pass 1 and Pass 2 used different units (Pass 1: A 98 claims, B 110; Pass 2: A 58, B 56) and different standards for R-14 and R-16. Pass 1 gave quant A 0.9509, B 0.9846; Pass 2 gave A 0.9193, B 0.9437. The re-evaluation applied one rule per metric to both variants (rules in `scoring-reeval.md`, "Final quantitative"): RC = explicit content for every element of a requirement (binary); IC unit = one list item, table row or body paragraph with a falsifiable claim; SR = the protocol's grep-checkable vague-indicator list; DC = internal references, a bare label the document never defines counts as unresolved; SC = H2 count over the maximum.

| Metric | Weight | Variant A (adapter now) | Variant B (one wire format) |
|--------|--------|-------------------------|-----------------------------|
| requirement_coverage | 0.30 | 0.9412 (16 of 17; R-16 missing: reply, resolve and bots-silent case not addressed) | 0.8824 (15 of 17; R-14 missing: the research/13 lean "adapter now, extensible v2 later" never stated; R-16 missing: reply and resolve) |
| internal_consistency | 0.25 | 0.9322 (4 contradictions in 59 units) | 0.9552 (3 contradictions in 67 units) |
| specificity_ratio | 0.15 | 1.0000 (59 concrete, 0 vague) | 1.0000 (67 concrete, 0 vague) |
| dependency_completeness | 0.15 | 0.8333 (10 of 12 references resolve; unresolved "S1-S5", "M10") | 0.8824 (30 of 34 resolve; unresolved "M10" and the M2 label collision, 3 references) |
| section_coverage | 0.15 | 0.8889 (8 H2 of max 9) | 1.0000 (9 H2 of max 9) |
| **quant_score** | | **0.9237** | **0.9359** |

Contradictions counted (agreed by both passes and the re-evaluation): A1 the adapter reads "the highest member severity" from a cluster record that holds none (X-001, code-contradicted); A2 "no existing test edited" versus "add the module to the static no-shell-token check"; A3 "downstream only reads four fields" versus A's own citation of `fsm.py:902-906`; A4 `confidence` set from `disputed` versus the CRITICAL-never-lowered rule. B1 "a third name reuses this bookkeeping" versus its own exclusion of the panel from the re-trigger path; B2 "does not call `merge_round`" versus deriving `incomplete` from a C-03 quorum refusal that lives there; B3 "any converter drops the quote and second citation" versus its own slot-less reader.

Sensitivity (from `scoring-reeval.md`): with the Pass 1 reading of RC (B 17 of 17) the combined margin is 0.0404; with the other four variants named there it stays between 0.0206 and 0.0280. All are below 0.05 and B leads in every row.

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Final verdicts (agreed by both passes, or settled by the re-evaluation). `MET` needs a direct quote or section reference. Where the passes agreed, the CEV text is in Appendix 1 and Appendix 2; the seven re-evaluated pairs are in the Position-Bias section.

| Dimension | Criterion | Variant A | Variant B | Basis |
|---|---|---|---|---|
| Completeness | 1 Covers all explicit requirements | NOT MET | NOT MET | agreed (A misses R-16; B misses R-14 and R-16) |
| Completeness | 2 Edge cases and failure scenarios | MET | MET | agreed |
| Completeness | 3 Dependencies and prerequisites | MET | MET | agreed |
| Completeness | 4 Success or completion criteria | MET | MET | agreed |
| Completeness | 5 Out of scope stated | MET | MET | agreed |
| Correctness | 1 No factual errors | NOT MET | NOT MET | agreed (A: X-001 cluster record, "50 files", A-004; B: B4 partly contradicted, reflect `parse_block` claim not found in code, X-009) |
| Correctness | 2 Feasible within stated constraints | NOT MET | MET | agreed (A's stated adapter input cannot supply severity or category; B's carve-outs are buildable) |
| Correctness | 3 Terminology consistent | MET | NOT MET | agreed (B uses M1 to M3 in two senses) |
| Correctness | 4 No internal contradictions | NOT MET | NOT MET | agreed (A 4, B 3) |
| Correctness | 5 Claims supported | MET | MET | agreed |
| Structure | 1 to 5 | MET x5 | MET x5 | agreed |
| Clarity | 1 Unambiguous language | MET | MET | re-evaluated (A and B) |
| Clarity | 2 Concrete rather than abstract | MET | MET | agreed |
| Clarity | 3 Clear section purpose | MET | MET | agreed |
| Clarity | 4 Terms defined on first use | NOT MET | MET | re-evaluated (A fails on the unglossed "S1-S5") |
| Clarity | 5 Actionable next steps | MET | MET | agreed |
| Risk Coverage | 1 At least 3 risks with probability and impact | NOT MET | NOT MET | agreed (no probabilities in either) |
| Risk Coverage | 2 Mitigation for each risk | NOT MET | NOT MET | agreed |
| Risk Coverage | 3 Failure modes and recovery | MET | MET | re-evaluated (A); B agreed |
| Risk Coverage | 4 External dependencies and failure | MET | MET | re-evaluated (A); B agreed |
| Risk Coverage | 5 Monitoring or validation mechanism | MET | MET | agreed |
| Invariant & Edge Case | 1 Collection boundaries | MET | MET | agreed |
| Invariant & Edge Case | 2 State interactions across components | MET | MET | re-evaluated (A); B agreed |
| Invariant & Edge Case | 3 Guard condition gaps | MET | MET | agreed |
| Invariant & Edge Case | 4 Count divergence | MET | MET | agreed |
| Invariant & Edge Case | 5 Interaction effects | MET | MET | agreed |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 4/5 | 4/5 |
| Correctness | 2/5 | 2/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 5/5 |
| Risk Coverage | 3/5 | 3/5 |
| Invariant & Edge Case | 5/5 | 5/5 |
| **qual_score** | **23/30 = 0.7667** | **24/30 = 0.8000** |

### Edge Case Floor Check

Variant A 5/5 and Variant B 5/5 on Invariant & Edge Case Coverage; both at or above the 1/5 floor, both eligible as base. The floor is not suspended and no warning applies.

## Position-Bias Mitigation

Pass 1 evaluated in input order (A, B); Pass 2 in reverse order (B, A); the re-evaluation scorer then decided every differing pair with the explicit comparison prompt (its verdict is final). Disagreements are listed per criterion and variant.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Clarity 1 Unambiguous language | A | MET | NOT MET | DISAGREE | MET |
| Clarity 4 Terms defined on first use | A | MET | NOT MET | DISAGREE | NOT MET |
| Risk 3 Failure modes and recovery | A | NOT MET | MET | DISAGREE | MET |
| Risk 4 External dependencies and failure | A | NOT MET | MET | DISAGREE | MET |
| Invariant 2 State interactions across components | A | NOT MET | MET | DISAGREE | MET |
| Clarity 1 Unambiguous language | B | MET | NOT MET | DISAGREE | MET |
| Clarity 4 Terms defined on first use | B | MET | NOT MET | DISAGREE | MET |

Disagreements re-evaluated: 7 of 60 criterion-variant pairs (53 agreed). Final verdicts that differ from at least one pass: 7 (4 depart from Pass 1: A Clarity 4, A Risk 3, A Risk 4, A Invariant 2; 3 depart from Pass 2: A Clarity 1, B Clarity 1, B Clarity 4). The re-evaluation's reasons: Clarity 1 tests wording against the protocol's hedge list (0 hits in either file; open choices are scored under Clarity 5); Clarity 4 is NOT MET for A only because "S1-S5" is defined nowhere in A, while every project label in B is glossed in its first clause; Risk 3, Risk 4 and Invariant 2 are MET for A because A names a failure state, a dependency and a state rule with the same depth that B's agreed MET rests on.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (adapter now) | 0.4619 | 0.3833 | **0.8452** | 9 of 49 diff points won (18.4%) |
| B (one wire format) | 0.4679 | 0.4000 | **0.8679** | 6 of 49 diff points won (12.2%) |

**Margin**: 2.27% (0.0227; below the 5% threshold). B scores higher on the weighted layers: the lead comes from Clarity 4 (A fails on "S1-S5") and from IC, DC and SC; A is ahead on RC only (R-14).
**Tiebreaker applied**: Yes, level 1 (debate performance). Step 2 scoring matrix, final winners over 49 diff points: Variant A 9, Variant B 6, Hybrid 16, Neither 18 (`debate-transcript.md`, "Scoring Matrix"). Variant A won 9 points against 6 for Variant B; the gap of 3 points is 6.1 percentage points of 49, above the 5% band, so level 1 decides and levels 2 and 3 are not needed. (For the record, level 2 would have tied: Correctness criteria met are A 2, B 2.) The debate's winners for A are S-003, C-003, C-004, C-005, C-015, C-016, X-006, X-008 and C-009; for B S-006, S-009, S-010, X-001, X-002, X-003 (the points where the debate verified a defect in A or a correction by B).

## Selected Base: Variant A (Proposal A, `variant-1-original.md`; default model, default persona)

### Selection Rationale

The weighted layers favour B (0.8679 against 0.8452, margin 2.27%, inside the 5% tie band), so the protocol's tiebreaker decides, and Step 2 debate performance favours A (9 points won against 6). The ordering of the debate agrees with the tiebreaker on the slot axis: B itself conceded the slot axis (S-002 to S-004, C-004, C-005; third `REVIEWERS` name, five edited functions, three prose copies) and withdrew its model-emitted line keys, its `finding_from_v2` placement in `severity_router.py` and the harness-injection of keys. The topology that survives the debate is A's: separate main-session pre-step, a pure converter module on the `pr_submit` side, no `REVIEWERS` entry, no `merge_wait` change, a sibling `panel` field. B's lead on the weighted layers comes from Clarity 4 (A's unglossed "S1-S5") and from IC, DC and SC (the re-evaluation's own statement); A's verified defects (cluster record lacks severity and category; "downstream reads four fields"; "50 files") are repaired in the refactoring plan from the debate's own Round 2 content. Neither proposal won as written: both advocates, after Round 2, named the same superior approach on all 49 points by label (Variant A 9, Variant B 6, Hybrid 16, Neither 18), with the resolution C10-R (A's Round 2) and its amended form C10-R-B (B's Round 2: C10-R plus AM-1 to AM-6, not answered by A at standard depth).

### Strengths to Preserve from Base

1. Two-stage topology: the panel is a main-session pre-step before the snapshot gate; the single executable snapshot-gate python block (pinned in four test files) is untouched.
2. Zero edits to `Finding`, `Severity`, the FSM, `REVIEWERS`, `reviewer_activity`, `merge_wait`, `reviewers.py` (INV-E held by construction).
3. The converter is the only place where "PR" and "panel" meet; `reviewer = "panel"` set by code, not by a model.
4. Panel standing reported beside, never inside, the `reviewers` object; "panel did not complete" is never read as clean (INV-I).
5. The equivalence experiment (U-001), the groundability measurement (U-006), the dormant router steps 3 and 4 observation (U-002), the CRITICAL row restated in the table (U-004), "requested, not served" independence.
6. The prior-slot consistency section (C-01, C-02, C-03) and the "what A concedes" list.

### Strengths to Incorporate from Non-Base Variants

1. From B, adopted by both advocates: the converter reads the source findings and joins on `(reviewer_id, id)` (X-001); the strict `incomplete` rule "any requested reviewer not complete"; `body` is the representative's claim verbatim (fix_key stability); the standing carries the reviewed head SHA and is stale after a fix push (A-008); the T3 pin that `terminal_augment_no_response` stays keyed to the two bots; T1 parity, T4 grounding, M1 cost, M2 and M3 measurements; severity route-cost warning (U-009); `ROLES` already holds `diff` and `source` (U-010); the corrected census (47 `test_*.py` files; no test pins the Output Contract `reviewers` row); B's "Limits" section and open items O3, O4.
2. From B, adopted by A in Round 2 as defaults: first release report-only; thread-less findings on promotion; per-cluster conversion with a dropped list; new module in a new file; `confidence` and `original_line` unset.
3. From B's Round 2 amendments, not answered by A at standard depth (carried as contested, with the invariant probe's findings): AM-1 one Finding per (cluster, category); AM-2 side record of reviewer severity and "never lowers a CRITICAL" struck; AM-3 missing `changed_ranges` degrades instead of dropping; AM-4 standing rule for zero clusters plus `blocking_clusters` and the "not clean" wording; AM-5 append the module to `CORE_PURE_FILES`; AM-6 FX-5 prerequisite is the category set only and `snapshot_file_list` is the PR head tree.

---

Appendix 1 and 2 follow: the Qualitative sections of Pass 1 and Pass 2 reproduced unedited (full CEV evidence per criterion and variant).


## Appendix 1: Pass 1 qualitative CEV tables (input order)

### Qualitative (Pass 1)

Rule applied: MET only with a direct quote or section reference; otherwise NOT MET. Factual errors verified by the diff analysis, the debate, or my re-checks are applied in Correctness. Section numbers refer to each variant's own H2 numbering.

#### Completeness

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|---|---|---|---|---|
| 1. Covers all explicit requirements from source input | NOT MET | CLAIM: A covers all 17 requirements. EVIDENCE: 16 of 17 (RC matrix); R-16 is missing: A 3.7 only says panel findings "enter that same path"; reply, resolve, and the bots-silent case are not in A (A advocate conceded them as unspecified, debate Concession 6). | NOT MET | CLAIM: B covers all. EVIDENCE: B 3.3 and 8 O3 cover the Wave 2-4 flow and the bots-silent case (as OPEN), but reply and resolve for a thread-less panel finding (A-006) appear nowhere in B; B 8 O3 itself says "OPEN". |
| 2. Addresses edge cases and failure scenarios | MET | A 2: "'panel did not complete' is a third state that is never read as 'clean' (INV-I)"; A 6.2 lists fixtures for "`line_start` missing; `unresolved` citation; `disputed`; non-blocking MAJOR; CRITICAL non-blocking" and "the drop case (no integer line, `is_groundable` false)". | MET | B 5 row "Endangered by B: `terminal_augment_no_response` meaning" and 3.2 item 3(b) (a local always-answering reviewer would make the status unreachable); B 6 T3 and T4 (citation-less line dropped). |
| 3. Includes dependencies and prerequisites | MET | A 5: "A depends on it" (C-01, C-03); A 5 names the quorum helper as "an addition A needs, not as something R-C03 concluded"; A 2 lists the FX-5 vocabulary exposures as needed under both positions. | MET | B 2 table: "DEPENDS on 'unknown keys open'", "DEPENDS on C-06 (repair policy)", "DEPENDS on the completion states and the quorum refusal"; B 3.1 item 1 (vocabulary parameters). |
| 4. Defines success or completion criteria | MET | A 6 item 1: "`uv run pytest tests/pr_submit -q` passes with no edit to any existing test file ... A is wrong as soon as an existing test must be edited"; items 2-7 each state what would show A right or wrong. | MET | B 6 T2: "Right if zero edits to existing tests are needed; wrong if any existing test must change"; T1: "Fails if B's reader needs any logic beyond renaming". |
| 5. Specifies what is explicitly out of scope | MET | A 5: "A takes no position on the repair policy (slot C-06)"; A 4 INV-G: "Which launch path is used is slot C-07, and A does not change it"; A 4 "Endangered or left open by A (stated, not resolved here)". | MET | B 2 table: "B does not reopen C-02"; B 3.4: "B leaves `blocking` as a recorded field that `pr_submit` does not route on"; B 9 "Limits of this proposal" lists what was not read or traced. |

Subtotal Completeness: A 4/5, B 4/5.

### Correctness

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|---|---|---|---|---|
| 1. No factual errors or hallucinated claims | NOT MET | CLAIM: no factual errors. EVIDENCE of errors: A 2 and 3.5 ("Cluster output already holds what the adapter reads: `primary_citation`, `claim`, ...", "highest member severity") is [CODE-CONTRADICTED] (X-001: cluster keys at `cluster.py:352-378` have no severity or category; `primary_citation` is per member); A 8 "downstream only reads path, line, body, category and the route" is contradicted by `fsm.py:902-906` (A-004); A 3.3, 6.1, 8 "the 50 test files" is wrong, 47 (X-003); A 6.1 says a third-name design changes the keys `reviewer_activity` returns and breaks the pins at `test_codex_reviews.py:285-295, :705`, which holds only for a B that edits `reviewer_activity`, and B does not (X-002). | NOT MET | CLAIM: no factual errors. EVIDENCE of errors: B 4 row B4 ("the four keys are the common record of the two existing code-review consumers") is partly [CODE-CONTRADICTED] (X-006: `auggie-reviewer.md:54-67` emits two of the four keys, `file` not `path`, no `reviewer`, no `original_line`); B 3.1 item 1 and B 5 row 1 say reflect "calls `parse_block` with `lens=...`", but no file under `src/superclaude/cli/reflect` references `findings_v2` or `parse_block` (my grep; also invariant-probe INV-017 note); B 4 row B10 ("the run can end `terminal_clean` with the panel never having answered") holds only for an A without A's `panel` field (X-005). Fewer and less load-bearing than A's, but not zero. |
| 2. Technical approaches are feasible with stated constraints | NOT MET | A 2 specifies the adapter input as the cluster record plus "highest member severity" while promising no edit to `cluster.py`; X-001 shows the record cannot supply severity or category, so the approach as written is not implementable under A's own constraint (the repair, a `(reviewer_id, id)` join to source blocks, is outside the variant text). A 2 also builds `in_diff` "from the diff the pre-step already holds"; `pr_submit` has no hunk parser and the poll payload has no diff keys (X-010, C-002). | MET | B 3.2 gives an implementable path: `finding_from_v2` next to `finding_from_comment` (`severity_router.py:61-119` already validates the nine keys), and B 3.2 item 3 (a), (a2), (b), (c) names the `reviewers.py` hazards and handles them (empty-identity branch, optional third `merge_wait` pair defaulting to `None`, `no_response` kept keyed to the two bots; all ten call sites stay source-compatible, diff-analysis ledger). Caveat recorded: the early pending return at `reviewers.py:412` also needs a guard (conceded in debate, C-004); this is an omission, not an infeasibility. |
| 3. Terminology used consistently and accurately throughout | MET | A uses "adapter", "pre-step", "panel presence state (present, absent, incomplete)" with one meaning each in 1, 2, 4, 6 item 7, 8; `reviewer = "panel"` is stated the same way in 2, 3.2, 3.3. (The cluster-versus-member field confusion is a factual error and is scored under criterion 1, not double-counted here.) | NOT MET | B reuses the labels M1, M2, M3 for two different things: B 1 and B 7 use them for the research/13 module exposures ("what M2 already requires", "because M2 is a decided requirement"), while B 6 defines M1 (cost), M2 (`in_diff` precision), M3 (what an adapter would drop); B 7 uses both senses within one paragraph (line 108 M1 = cost, line 110 M2 = module exposure). |
| 4. No internal contradictions (cross-validated with IC) | NOT MET | 4 contradictions found (IC section): A 2 versus 3.5 on the adapter input; A 6.1 versus 6.2/4 on "no existing test edited"; A 8 versus 3.4 on what downstream reads; A 2 (`confidence` from `disputed`) versus A 5 (CRITICAL never lowered). | NOT MET | 3 contradictions found (IC section): B9 versus 3.2 (a2); 2/3.2 item 6 quorum refusal versus "B does not call `merge_round`"; B1 versus B8 on what travels in `Finding`. |
| 5. Claims supported by evidence or rationale within the document | MET | Every substantive claim carries a file:line and a tag: 38 `name.ext:line` citations, 25 CODE-VERIFIED and 12 UNVERIFIED tags; A 3.1-3.7 give the read evidence per claim, A 6 gives the checks. | MET | B 4 is a 14-row table with source and tag per claim; 60 `name.ext:line` citations; B 9 lists what was carried and not re-read. |

Subtotal Correctness: A 2/5, B 2/5.

### Structure

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|---|---|---|---|---|
| 1. Logical section ordering (prerequisites before dependents) | MET | A: 1 position, 2 design consequence, 3 evidence, 4 invariants, 5 consistency with C-01..C-03, 6 test, 7 effect, 8 objection; later sections cite earlier ones ("(3.1)", "(6.2)"). | MET | B: 1 position, 2 consistency with prior slots (dependencies first), 3 design, 4 evidence, 5 invariants, 6 tests, 7 effect, 8 objection, 9 limits. Forward reference from 2 to "section 3.2 item 3 and 6" is a minor ordering cost. |
| 2. Consistent hierarchy depth (no orphaned subsections) | MET | A is flat: 8 H2, 0 H3; the 3.1-3.7 items are numbered paragraphs, none orphaned. | MET | B has 9 H2 and 5 H3 (3.1-3.5), all under H2 3; no single-child subsection. |
| 3. Clear separation of concerns between sections | MET | A 2 splits "Shared core", "`pr_submit`", "Skill and call site"; evidence (3), invariants (4), prior slots (5), tests (6) are separate sections. | MET | B 3.1 core, 3.2 `pr_submit`, 3.3 panel and skill, 3.4-3.5 sub-decisions; B 8 point 3 separates wire-format evidence (B1-B8) from slot evidence (B9, B10, B13). |
| 4. Navigation aids present | MET | A header line 9 defines the citation shorthand (r13, S05, S06, UC, R-C01..R-C03); numbered cross-references "(3.5)", "(6.2)", "per 3.3". | MET | B 4 numbered rows B1-B14 cross-referenced from 8 ("B2", "B13", "B10"); T1-T4, M1-M3, O2-O6 labels; header "Tags" legend. |
| 5. Follows conventions of the artifact type | MET | A has a status line, tagged evidence, invariants, consistency with prior slots, test, effect on PR review and rf-qa, strongest objection (all items the task asked for). | MET | B has the same set plus "Limits of this proposal" and a status line. |

Subtotal Structure: A 5/5, B 5/5.

### Clarity

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|---|---|---|---|---|
| 1. Unambiguous language | MET | Search for the protocol hedge list (should consider, might, as appropriate, as needed, properly, adequate, various, etc.) returns 0 hits; unknowns are stated as unknowns ("was not searched", "I did not open it and do not state what it asserts"). | MET | Same search returns 0 hits; open decisions are labelled OPEN (B 8 O3) rather than hedged. |
| 2. Concrete rather than abstract | MET | A 2 lists what the adapter owns: "citation to (`path`, `line`); the module severity mapping table ...; `in_diff` and `original_line` ...; `reviewer = "panel"` ...; `confidence`"; A 6.2 lists eight named fixture cases. (The module name and the injection point are not named; recorded under Completeness and Correctness, not here.) | MET | B 3.2 item 1 names `finding_from_v2(obj, *, default_reviewer)` in `severity_router.py`; item 3 names `reviewer_identities`, `list_review_threads`, `merge_wait` optional third parameter; item 4 names `SKILL.md:271`, `:277`, `commands/pr-submit.md:60`. |
| 3. Each section has a clear purpose or can be summarized in one sentence | MET | A 1 "The position (A, in one paragraph)"; headings state purpose ("The test or measurement that would show A right or wrong"). | MET | B 1 "The position in one paragraph"; headings "The test or measurement that would show B right or wrong", "Limits of this proposal". |
| 4. Acronyms and domain terms defined on first use | MET | A header defines shorthand (line 9); first uses carry a gloss: "module-declared category, lens and severity sets (FX-5, decided; S06:100)", "cost unmeasured (GQ-177, OQ-9)", "convergence trigger T-a ('a module needs re-review rounds ...')". | MET | B header defines tags; first uses carry a gloss: "CO-27 (wire format), CO-29 (slot)", "INV-E" with its content in 1, "C-06 (repair policy)", "(OQ-18 / GQ-177; never measured)", "R13 is research/13". |
| 5. Actionable next steps or decision points clearly identified | MET | A 4: "if the owner wants a panel re-run after each fix push, the pre-step needs a cycle id and the cost data first"; A 8: "If the owner wants one reporting surface, A can add a `panel` field beside `reviewers`". | MET | B 3.4: "B recommends (i) only if the owner wants Medium reachable"; B 8 O3: "the Wave 8 wait-only branch (`SKILL.md:77, 365`) is where it must be decided"; B 8 point 2 names M1 and research/13 Q4 as the deciders. |

Subtotal Clarity: A 5/5, B 5/5.

### Risk Coverage

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|---|---|---|---|---|
| 1. At least 3 risks with probability and impact assessment | NOT MET | A 4 gives severity labels (INV-E HIGH, INV-F MEDIUM, INV-G HIGH, INV-J MEDIUM) but no probability for any risk; the "endangered or left open" items (prose-level guard, per-round cost) carry neither. | NOT MET | B 5 and 8 list risks and hazards ("Endangered by B: `terminal_augment_no_response` meaning", O2-O6) with no probability and no impact grade. |
| 2. Mitigation strategy for each identified risk | NOT MET | A 4: INV-G is "not changed" and deferred to slot C-07 (HIGH risk without a mitigation); INV-J "must be written once and reviewed against S1-S5" and the cost item "needs ... the cost data first" are mitigations, but INV-G is not. | NOT MET | B 8 O3 ("OPEN") and O4 ("a reader decision B does not make here") have no mitigation; O2, O5, O6 and the `terminal_augment_no_response` hazard (T3) do. |
| 3. Failure modes and recovery procedures | NOT MET | A 2 and 4 INV-I give a failure state (incomplete, never clean) but no recovery or resume path for the panel result; A 4 last bullet only says a re-run "needs a cycle id". Staleness after a fix push and durable state are not addressed (A-008). | MET | B 3.2 item 6 maps `truncated`, `invalid`, `failed`, `timed_out` or a quorum refusal to `incomplete`, and says the `absent_reviewers` fold in `run_log.py` means "a third name needs no new state" (a resume path through the run log); B 3.2 item 3 (a2) binds presence to "it ran on this head SHA". (Debate X-008 and probe INV-002 show the reuse is weaker than B states; the failure and recovery path is still addressed.) |
| 4. External dependencies and their failure scenarios | NOT MET | A 3.3 describes the bots as external actors with silence deadlines, but the bots-silent case with panel findings is absent from A (C-008; R-16 missing). | MET | B 8 O3 (bots silent, panel has findings, with the open decision site) and 5 row on `terminal_augment_no_response`; B 2 C-03 row ("requested", not "served", until C-08). |
| 5. Monitoring or validation mechanism for risk detection | MET | A 6 items 1-7, e.g. item 7: "a test that a pre-step failure, a quorum shortfall and a clean panel produce three different outputs, and that none of them changes the existing `reviewers` object"; item 5 groundability share. | MET | B 6 T1-T4 and M1-M3, e.g. T3 status pin "written down before the code", M2 `in_diff` precision, M3 count of later-wave use. |

Subtotal Risk Coverage: A 1/5, B 3/5.

### Invariant & Edge Case Coverage

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|---|---|---|---|---|
| 1. Boundary conditions for collections (empty, single-element, maximum size) | MET | A 6.2 fixtures "single-reviewer; multi-reviewer"; A 5 (R-C03 INV-007): "`requested` can collapse to 1 when slots are dropped without `skipped_slots`". | MET | B 2 C-01 row: "a `claim` over 300 characters is rejected by `check_finding` (`findings_v2.py:111`)" (maximum size); B 3.2 item 6 "no panel run -> `absent`"; B 3.2 item 3(b) optional third pair defaulting to `None`. |
| 2. State variable interactions across component boundaries | NOT MET | A 2 keeps the panel standing in a sibling field beside `reviewers` (separation of state), but head-SHA binding and staleness after a fix push are not specified (A-008: STATED in B, UNSTATED in A) and the interaction of an incomplete panel with `terminal_clean` is untraced (A 4 and debate X-005). | MET | B 3.2 item 3 (a2): presence is "'it ran on this head SHA', set by the main session, not read from the PR snapshot"; item 3(b): `no_response` stays keyed to the two bots so the new state cannot make `terminal_augment_no_response` unreachable. (B also did not trace `terminal_clean`, B 9.) |
| 3. Guard condition gaps (missing validation, unguarded type assumptions) | MET | A 3.2: `finding_from_comment` "fails closed: non-object, empty `path` or `body`, a non-positive integer `line` ... each raise `ValueError`"; A 2 "no integer line, no finding (`is_groundable`)"; A 4 INV-I "the adapter never maps 'no result' to 'no findings'". | MET | B 3.2 item 3(a): `reviewer_identities` and `retrigger_phrase` "raise `ValueError` for an unknown name"; B 6 T4 (anchor-only line dropped by `is_groundable`); B 3.2 item 2. |
| 4. Count divergence scenarios (off-by-one, inclusive or exclusive ranges) | MET | A 5 (R-C03 INV-007): "the pre-step has to pass the resolution so that `requested` is the dispatched count". Recorded caveat: the invariant probe (INV-007, citing the A text) shows that "dispatched count" is the faulty quantity (a slot that fails to launch is not counted); the scenario is identified, its fix is defective. | MET | B 3.2 item 3(b): "`no_response` is `len(absent) == len(pairs)` (`reviewers.py:395-424`) ... otherwise a local panel that always answers makes `terminal_augment_no_response` unreachable" (pair-count change from 2 to 3). |
| 5. Interaction effects when features or components combine | MET | A 3.2: a finding with `reviewer = "panel"` flows through `dedup_groups` ("groups by `(path, line)` across reviewers") and `seed_troubleshoot`; A 3.3 third name versus the single-python-block gate test. | MET | B 3.2 item 5: "a panel finding on the same line as an Augment or Codex finding joins the existing group with no code change"; B 5 row on `terminal_augment_no_response`. |

Subtotal Invariant & Edge Case: A 4/5, B 5/5.

### Qualitative summary (Pass 1)

| Dimension | Variant A (of 5) | Variant B (of 5) |
|---|---|---|
| Completeness | 4 | 4 |
| Correctness | 2 | 2 |
| Structure | 5 | 5 |
| Clarity | 5 | 5 |
| Risk Coverage | 1 | 3 |
| Invariant & Edge Case | 4 | 5 |
| Total met | 21 | 24 |
| qual_score (met / 30) | 0.7000 (21/30) | 0.8000 (24/30) |

Dimension notes: Correctness is tied at 2/5 for different reasons. A fails on the load-bearing X-001 error (the adapter's input is not in the cluster record) and on feasibility as written; B fails on the partly contradicted B4 and the reflect `parse_block` claim, plus an M-label collision. Both fail the no-contradiction criterion (A 4 contradictions, B 3).

## Appendix 2: Pass 2 qualitative CEV tables (reverse order)

### Qualitative (Pass 2)

Evaluation order: Variant B first, Variant A second. Columns stay A then B. Line numbers are lines of the variant files. Evidence form: CLAIM (the criterion), EVIDENCE (quote or section), VERDICT.

### Completeness

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|---|---|---|---|---|
| 1. Covers all explicit requirements | NOT MET | Claim: all R-01 to R-17 covered. Evidence: RC detail shows R-16 unmatched; section 3.7 only says "Panel findings enter that same path"; reply, resolve and bots-silent are absent (searched sections 2, 3.7, 4, 5). Verdict: NOT MET | NOT MET | Claim: all R-01 to R-17 covered. Evidence: R-14 unmatched, the research/13 lean "adapter now, extensible v2 later" and GQ-179 and GQ-182 are not named in sections 1 to 9; reply and resolve are also not addressed. Verdict: NOT MET |
| 2. Edge cases and failure scenarios | MET | Section 6 item 2 lists fixtures "`line_start` missing; `unresolved` citation; `disputed`; non-blocking MAJOR; CRITICAL non-blocking" and the drop case; section 5 C-03 names INV-007 (`requested` collapsing); section 6 item 7 pre-step failure versus quorum shortfall. Verdict: MET | MET | Section 3.2 item 3 (a), (b), (c) lists `ValueError` for an unknown name, the `no_response` count, call-site compatibility; section 8 O3 (bots silent), O4 (300 character claim and `fix_key`); section 3.2 item 6 failure states. Verdict: MET |
| 3. Dependencies and prerequisites | MET | Section 5: "A depends on it" for C-01 and C-03; section 2 says FX-5 vocabularies and M4 lens "are needed under either position". Verdict: MET | MET | Section 2 table column "Where B depends on it or differs": "DEPENDS on" unknown keys open, ledger keys deferred, C-06 for over-limit lines, C-03 completion states. Verdict: MET |
| 4. Success or completion criteria | MET | Section 6 item 1: "A is wrong as soon as an existing test must be edited"; item 4 and 5 give falsifiers. Verdict: MET | MET | Section 6 T2: "Right if zero edits to existing tests are needed; wrong if any existing test must change"; T1 "Fails if B's reader needs any logic beyond renaming". Verdict: MET |
| 5. Out of scope stated | MET | Section 5: "A takes no position on the repair policy (slot C-06)"; section 4 INV-G: launch path "is slot C-07, and A does not change it". Verdict: MET | MET | Section 2 C-02 row: "B does not reopen C-02"; section 7: "B adds nothing for the read-only reviewer rule ... or the replay oracle"; section 6 T3: "B has NOT decided" the bots-silent handling. Verdict: MET |

### Correctness

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|---|---|---|---|---|
| 1. No factual errors or hallucinated claims | NOT MET | Claim: no verified factual error. Evidence: section 3.5 "Cluster output already holds what the adapter reads" is [CODE-CONTRADICTED] for severity and category (X-001); section 8 "downstream only reads path, line, body, category and the route" is false (A-004; `in_diff`, `verification_status`, `fix_key`, `comment_id`); "the 50 test files" is [CODE-CONTRADICTED] (X-003, 47 files); "OQ-9" differs from OQ-18 in the task source. Verdict: NOT MET | NOT MET | Claim: no verified factual error. Evidence: B4 "the same fields" is partly [CODE-CONTRADICTED] (X-006: `auggie-reviewer` carries two of the four keys, `file` not `path`); section 3.2 item 6 "a C-03 quorum refusal" names a rule absent at HEAD (X-009); section 3.1 item 1 says reflect calls `parse_block` with `lens=` which the probe could not find (INV-017 note). Verdict: NOT MET |
| 2. Technical approach feasible within stated constraints | NOT MET | Claim: the design can be built as stated. Evidence: section 2 promises no `cluster.py` edit and an adapter reading severity from cluster output, but the record has no severity or category (X-001), so the stated input is insufficient; "computed from the diff the pre-step already holds" has no hunk parser behind it (X-010, UNVERIFIED); the quorum helper is new code (X-009). Verdict: NOT MET | MET | Claim: the design can be built as stated. Evidence: section 3.2 item 3 states each carve-out (empty identity branch, skip in `list_review_threads`, optional third `merge_wait` parameter); diff-analysis C-004 verified all ten `merge_wait` call sites pass two pairs, so an optional third parameter is source-compatible; `finding_from_comment` reads all the keys (X-006 row, A-012). Open gaps (clustering not stated, C-001) are omissions, not infeasibility. Verdict: MET |
| 3. Terminology consistent and accurate | MET | Sections 1, 2 and 3.5 use "adapter", "cluster record", "cluster output" for one thing; "tri-state", "presence state" and the "`panel` field" in sections 2, 4 and 8 name one concept; `confidence` meanings are listed once in section 3.4. Verdict: MET | NOT MET | Claim: terms used consistently. Evidence: section 7 "what M2 already requires (module-declared ... sets)" and "M2 is a decided requirement" use M2 for research/13 M2, while section 6 defines M2 as the `in_diff` precision measurement; section 3.4 says "the position's four" keys then adds a fifth. Verdict: NOT MET |
| 4. No internal contradictions (cross-checked with IC) | NOT MET | IC found 4 contradictions (severity input versus cluster field list; "no existing test edited" versus "add the module to the static check"; "downstream only reads four fields" versus `fsm.py:902-906`; fourth `confidence` meaning). Verdict: NOT MET | NOT MET | IC found 3 contradictions (B9 versus a2; "does not call `merge_round`" versus "C-03 quorum refusal"; lossless claim B1 versus B's own slot-less reader). Verdict: NOT MET |
| 5. Claims supported by evidence or rationale | MET | Section 3 gives file and line with [CODE-VERIFIED] tags per bullet, e.g. section 3.3 "`reviewers.py:41`", "`test_codex_reviews.py:285-295`". Verdict: MET | MET | Section 4 is a 14-row table, each row claim, source and tag, e.g. B6 "`fsm.py:364-372`"; B12 corrects the file count to 47. Verdict: MET |

### Structure

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|---|---|---|---|---|
| 1. Logical section ordering | MET | Sections run position (1), design (2), evidence (3), invariants (4), slot consistency (5), tests (6), effect (7), objection (8); design precedes the evidence that supports it. Verdict: MET | MET | Sections run position (1), prior-slot consistency (2), design (3), evidence (4), invariants (5), tests (6), effect (7), objection (8), limits (9). Verdict: MET |
| 2. Consistent hierarchy depth | MET | Eight numbered H2 sections; sub-points 3.1 to 3.7 are uniformly numbered paragraphs, no orphan level. Verdict: MET | MET | Nine numbered H2 sections; H3 only in section 3 (3.1 to 3.5), no orphan. Verdict: MET |
| 3. Separation of concerns | MET | Evidence (3), invariants (4), slot consistency (5), tests (6) and effects (7) each have their own section. Verdict: MET | MET | Design (3), evidence (4), invariants (5), tests (6), limits (9) separate; section 8 notes wire-format evidence and slot evidence are separate sets. Verdict: MET |
| 4. Navigation aids | MET | Line 9 citation shorthand legend (r13, S05, S06, UC, R-C01 to R-C03); numeric cross-references "(3.5)", "(6.2)". Verdict: MET | MET | Line 6 tag legend; evidence rows numbered B1 to B14 and cross-cited ("(B1)", "section 3.2 item 3b"). Verdict: MET |
| 5. Follows artifact-type conventions | MET | Status line, position paragraph, evidence, invariants, test, objection and answer, closing Status line, as a debate proposal requires. Verdict: MET | MET | Same elements plus Limits; header "Status: Complete" and closing status line. Verdict: MET |

### Clarity

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|---|---|---|---|---|
| 1. Unambiguous language | NOT MET | Section 2 "set from cluster facts (for example `disputed`) or left `None`"; section 4 "that table is a PR-module choice and it must be written once and reviewed against S1-S5"; section 8 "A can add a `panel` field" (optional). Several choices left open. Verdict: NOT MET | NOT MET | Section 3.5 "B states both and does not decide the threshold"; section 8 O4 "a reader decision B does not make here"; section 6 M2 "a pre-registered fraction"; section 3.4 two options "(i) ... or (ii)". Verdict: NOT MET |
| 2. Concrete rather than abstract | MET | Section 3 cites functions and lines ("`severity_router.py:61-119`", "`reviewers.py:395-424`"); section 6 lists fixture cases. Verdict: MET | MET | Section 3.2 lists five named functions with lines; section 6 T1 to T4 give assertions. Verdict: MET |
| 3. Each section has a clear purpose | MET | Headings state purpose: "The position (A, in one paragraph)", "The test or measurement that would show A right or wrong". Verdict: MET | MET | "The position in one paragraph", "The strongest objection and my answer", "Limits of this proposal". Verdict: MET |
| 4. Terms and acronyms defined on first use | NOT MET | Line 9 defines only the citation shorthands; FX-5, M4, M10, M11, GQ-177, OQ-9, S1-S5, T-a, INV-G, INV-J, SARIF are used without a gloss (sections 2, 4, 7). Verdict: NOT MET | NOT MET | Line 6 defines only the tags; INV-E appears in section 1 before its definition in section 5; OQ-18, GQ-177, C-01 to C-08, M10, P1, P7, P8, P12, FSM are not defined. Verdict: NOT MET |
| 5. Actionable next steps or decision points | MET | Section 6 gives falsifiers; section 8 "If the owner wants one reporting surface, A can add a `panel` field"; section 4 lists open items with owners. Verdict: MET | MET | Section 6 gives pass and fail conditions; section 8 O3 "the Wave 8 wait-only branch ... is where it must be decided"; section 3.4 "B recommends (i) only if the owner wants Medium reachable". Verdict: MET |

### Risk Coverage

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|---|---|---|---|---|
| 1. At least 3 risks with probability and impact | NOT MET | Section 4 "Endangered or left open" names INV-G (HIGH), INV-J, a prose-level guard and per-round cost; impact tiers appear for invariants, probability for none. Verdict: NOT MET | NOT MET | Section 5 "Endangered by B" rows (`terminal_augment_no_response`, Output Contract copies) and section 8 O2 to O6 name risks with consequences; no probability and no grading. Verdict: NOT MET |
| 2. Mitigation for each identified risk | NOT MET | INV-G: "A does not change it; the same exposure exists under B", no mitigation; INV-J left to a table "reviewed against S1-S5". Verdict: NOT MET | NOT MET | Mitigations exist for the hazards (section 3.2 item 3, T3, O2 fallback, O5, O6 option (i)); O3 is "OPEN" with no mitigation and O4 is left as a reader decision. Verdict: NOT MET |
| 3. Failure modes and recovery | MET | Section 2 and INV-I: "never maps 'no result' to 'no findings'"; section 5: "visible, never clean"; section 6 item 7 pins three outputs (pre-step failure, quorum shortfall, clean). Verdict: MET | MET | Section 3.2 item 6 maps `truncated`, `invalid`, `failed`, `timed_out` to `incomplete`; section 6 M2 gives a deterministic fallback when reviewer-emitted `in_diff` is imprecise. Verdict: MET |
| 4. External dependencies and their failure | MET | Section 5 "If one of R-C01's convergence triggers fires ... A's claim ... would stop being a benefit"; INV-007 dependency on C-03; independence "requested, not served" until C-08. Verdict: MET | MET | Section 2: if C-01 had closed the keys "B would need a registered key list"; dependence on C-06 and C-08; section 5 last row: consumers outside the repository "[UNVERIFIED]". Verdict: MET |
| 5. Monitoring or validation mechanism | MET | Section 6 items 1 to 7: conformance fixtures, equivalence run, groundability share, tri-state test. Verdict: MET | MET | Section 6 T1 to T4 and M1 to M3; section 4 B8 `verify-citations` runs on the lines `pr_submit` reads. Verdict: MET |

### Invariant and Edge Case Coverage

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|---|---|---|---|---|
| 1. Collection boundary conditions (empty, single, max) | MET | Section 6 item 2 fixtures "single-reviewer; multi-reviewer; citation only"; section 5 INV-007 "`requested` can collapse to 1". Verdict: MET | MET | Section 3.2 item 3 (b) `no_response` is `len(absent) == len(pairs)`, changing from two to three pairs; section 8 O4 the 300-character `claim` limit; B6 citation-less line dropped. Verdict: MET |
| 2. State variable interactions across components | MET | Section 3.3 per-reviewer variables in the one executable gate block (`watermark`, `codex_watermark`, `review_state`) and the test namespace; section 4 "if a panel re-run after each fix push ... needs a cycle id". Verdict: MET | MET | Section 3.2 item 3 (a2) panel presence is "ran on this head SHA, set by the main session"; B9 `pending_retriggers` and the `absent_reviewers` fold; O4 `fix_key` hashing `body`. Verdict: MET |
| 3. Guard condition gaps | MET | Section 3.2 `finding_from_comment` raises `ValueError` for non-object, empty path, non-bool `in_diff`; `reviewer` is free text; `is_groundable` fails closed. Verdict: MET | MET | Section 3.2 item 3 (a) `reviewer_identities` and `retrigger_phrase` raise for an unknown name; section 3.1 item 2 core never validates the four keys, the reader does. Verdict: MET |
| 4. Count divergence | MET | Section 3.3 "12 lines in 3 files ... UC:58 counts one more hit"; section 5 INV-007 requested versus dispatched count. Verdict: MET | MET | B11 "12 lines in my grep; the conflict log counts 13"; B12 47 files versus 50; section 3.2 item 3 (b) `len(absent) == len(pairs)` with a third pair. Verdict: MET |
| 5. Interaction effects when components combine | MET | Section 3.2 a panel finding flows through `dedup_groups` across reviewers; section 4 INV-J non-blocking MAJOR against the merge guard; section 5 R-C03 INV-006 does not arise on the cluster path. Verdict: MET | MET | Section 3.2 item 5 a panel finding on a bot finding's line joins the existing dedup group; item 3 (b) a local reviewer would make `terminal_augment_no_response` unreachable; O3 bots silent with panel findings. Verdict: MET |

### Qualitative summary

| Dimension | Variant A (of 5) | Variant B (of 5) |
|---|---|---|
| Completeness | 4 | 4 |
| Correctness | 2 | 2 |
| Structure | 5 | 5 |
| Clarity | 3 | 3 |
| Risk Coverage | 3 | 3 |
| Invariant and Edge Case Coverage | 5 | 5 |
| Total met | 22 | 22 |
| qual_score (met / 30) | 0.7333 | 0.7333 |
