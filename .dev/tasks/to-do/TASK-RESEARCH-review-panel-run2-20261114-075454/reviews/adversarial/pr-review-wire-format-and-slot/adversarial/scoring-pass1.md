# Scoring Pass 1 (input order: A then B), slot C-10 pr-review-wire-format-and-slot

Scorer: Pass 1, neutral, independent. Variants scored as written (the originals): Variant A = `variant-1-original.md` (adapter now, separate pre-step); Variant B = `variant-2-original.md` (one wire format, panel as third reviewer). Evidence inputs: `diff-analysis.md` (verified facts, R-01..R-17), `debate-transcript.md` (code-verified defects), `invariant-probe.md`. Pass 2 file was not read. Nothing was executed; code claims were read at HEAD. Two code facts were re-checked by me for this pass: (1) `grep findings_v2|parse_block src/superclaude/cli/reflect` returns no hit, so B's statement "reflect (which calls parse_block with lens=...)" (B 3.1 item 1, B 5 row 1) is code-contradicted; (2) `src/superclaude/pr_submit/fsm.py:900-908` reads `f.in_diff`, so A's section 8 claim that downstream reads only path, line, body, category and route is contradicted by A's own 3.4 citation of `fsm.py:902-906`. `tests/pr_submit/test_*.py` count is 47 (A says 50).

## Quantitative

Counting rules (deterministic, from the text):
- RC: the 17 items R-01..R-17 of `diff-analysis.md`. A variant matches an item when it explicitly addresses it (section cited in the matrix below). R-17 is a prohibition; compliance was checked by search for run-1 file citations (none in either variant).
- IC: scorable claim = one falsifiable assertion carrying a file:line, count, named function, or an explicit design commitment, counted per bullet or table row (a bullet with several independent tagged facts counts each). Vague statements are not scorable. Contradiction = opposing claims about one subject inside the same variant, or a requirement-constraint conflict inside the variant (cited below).
- SR: substantive statements with at least one concrete indicator (number, file:line, named entity, threshold) versus statements whose support is only a vague indicator word (protocol list plus unmeasured adjectives found by grep: A line 45 "cheap", line 103 "some", line 120 "small"; B none).
- DC: internal references (section cross-references such as "(3.5)", "per 3.3", INV and B/T/M/O labels used inside the document) that resolve to a definition inside the same document. External document references (r13, S05, UC, R-C01..R-C03, research sections) are excluded.
- SC: H2 count (A 8, B 9), max = 9.

### Requirement coverage matrix (RC)

| Req | Variant A (matched, where) | Variant B (matched, where) |
|---|---|---|
| R-01 | yes, A 1 and 4 (INV-E) | yes, B 1 and 5 (INV-E row) |
| R-02 | yes, A 3.3 last two bullets (Grep counts, "I have not run any of these tests") | yes, B 4 row B11 and B12 ("Static reading only: no pytest run") |
| R-03 | yes, A 4 last bullet and 6 item 6 (GQ-177, OQ-9) | yes, B 6 M1 (OQ-18 / GQ-177) |
| R-04 | yes, A 4 (INV-E, INV-F, INV-C stated) | yes, B 5 table (INV-E, INV-F, INV-C rows) |
| R-05 | yes, A 2 (is_groundable fail-closed, per-module severity table, FX-5), 3.1 | yes, B 3.1 item 1 (vocabulary parameters), 3.2 item 2 (is_groundable), 4 row B6 |
| R-06 | yes, A 5 (C-01, C-02, C-03 each with dependency) | yes, B 2 table (C-01, C-02, C-03 each with dependency) |
| R-07 | yes, A 2, 4 (INV-I), 5 (C-03 derivation from complete_reviewers, invalid_reviewers, valid_blocks) | yes, B 3.2 item 6 (standing from COMPLETION_STATES), 6 T3 |
| R-08 | yes, A 2 last paragraph (SKILL.md:47-49) | yes, B 3.3 (SKILL.md:47-49) |
| R-09 | yes, A 6 (seven falsifiable claims) | yes, B 6 (T1-T4, M1-M3) |
| R-10 | yes, A 7 | yes, B 7 |
| R-11 | yes, A 8 | yes, B 8 |
| R-12 | yes, A 5 last bullet ("requested, not served") | yes, B 2 C-03 row and 5 row "C-03 condition 5" |
| R-13 | yes, A 4 INV-F | yes, B 5 INV-F row |
| R-14 | yes by content, A 1, 3.1, 3.3, 8 (wire format versus adapter; third name versus pre-step); GQ-179 and GQ-182 are not named | yes by content, B 1, 3, 8 (same two axes); GQ ids and the research/13 lean are not named |
| R-15 | yes, A 2 (adapter owns in_diff, original_line, reviewer, confidence), 3.4 | yes, B 3.2 item 1-2, 4 rows B2-B3, 6 M2 |
| R-16 | NO: A 3.7 says panel findings "enter that same path"; reply, resolve and the bots-silent case are absent (the A advocate conceded these as unspecified, debate Concession 6) | yes: B 3.3 (Wave 2 to Wave 4 chain) and 8 O3 (bots silent, OPEN); reply and resolve for a thread-less finding are absent (carried into Qualitative Completeness 1) |
| R-17 | yes (complies; A header line 7 states it) | yes (complies; no run-1 citation by search) |
| Total | 16 of 17 | 17 of 17 |

### Internal consistency (IC): claims and contradictions

Claims counted (rule above), by section.
- Variant A: 1-2 = 17; 3.1 = 3; 3.2 = 5; 3.3 = 12; 3.4 = 5; 3.5 = 4; 3.6 = 3; 3.7 = 4; 4 = 11; 5 = 14; 6 = 7; 7 = 5; 8 = 8. Total 98.
- Variant B: 1 = 6; 2 = 13; 3.1 = 6; 3.2 = 18; 3.3 = 2; 3.4 = 6; 3.5 = 4; 4 (B1-B14) = 14; 5 = 13; 6 = 7; 7 = 7; 8 = 8; 9 = 6. Total 110.

Contradictions found, Variant A (4):
1. A 2 says the adapter reads "the highest member severity" from the cluster record and changes no core file ("No change to `findings.py`, `findings_v2.py`, `cluster.py`"), while A 3.5 lists the cluster keys the adapter reads without any severity or category. The adapter input in A 2 is not available from the record A 3.5 lists (requirement-constraint conflict; also code-contradicted, X-001).
2. A 6.1 says the isolation claim holds only if no existing test file is edited ("only new test files added"); A 6.2 and 4 (INV-E) say to add the adapter module to the static no-shell-token check, which is an edit of the module list in `tests/pr_submit/test_static_grep.py` (self-conceded in debate, Concession 7).
3. A 8 says downstream "only reads `path`, `line`, `body`, `category` and the route", while A 3.4 itself cites `fsm.py:902-906` as a reader of `in_diff` (and `in_diff` is one of the keys A makes the adapter set).
4. A 2 sets `confidence` "from cluster facts (for example `disputed`)", while A 3.4 says router step 3 (low confidence) drops a tier and A 5 (C-02) says a CRITICAL is never lowered; a `disputed`-derived low confidence would lower a CRITICAL (router step 3, `severity_router.py:173-175`; debate C-010 outcome).

Contradictions found, Variant B (3):
1. B 4 row B9 says "A third name reuses this bookkeeping", while B 3.2 item 3 (a2) excludes the panel from the re-trigger path and from `reviewer_activity`; only the name-agnostic absent fold remains reusable (X-008, conceded by B in debate).
2. B 2 (C-03 row) and B 3.2 item 6 derive `incomplete` from "a C-03 quorum refusal", while the same row says "B does not call `merge_round`" where that refusal lives; the rule is not reachable on B's own path (X-009; no quorum in `cli/review` at HEAD).
3. B 4 rows B1 and B8: B1 says "Any converter that builds a `Finding` drops them [citation flags, quote, second citation] at the conversion point", while B8 says that under an adapter the citation-check result "cannot travel in `Finding` (B1)" as if that were specific to the adapter; B's own reader ends in the same slot-less `Finding` (X-007, C-012).

IC: A = 1 - 4/98 = 0.9592; B = 1 - 3/110 = 0.9727.

### Specificity ratio (SR)

- A: 98 substantive statements; 3 carry only vague indicators (line 45 "the cheap part of B", line 103 "some fixture", line 120 "a named, small key set"); concrete = 95. SR = 95/98 = 0.9694. Protocol hedge words (should consider, might, as appropriate, as needed, properly, adequate, various, etc., best practices) found: 0. Concrete anchors: 38 `name.ext:line` citations, 25 CODE-VERIFIED tags.
- B: 110 substantive statements; 0 carry vague indicators; concrete = 110. SR = 1.0000. Concrete anchors: 60 `name.ext:line` citations, 25 CODE-VERIFIED tags.

### Dependency completeness (DC)

- A: 10 internal references (section refs "per 3.3" in 4, "(3.1)" in 5, "(3.5) (3.2) (6.2) (3.1) (3.4)" in 8, "(3.3)" in 8, INV-I used in 2, INV-E used in 7); all resolve. DC = 10/10 = 1.0000.
- B: 35 internal references (B-row references B1-B14 about 18; T and M labels 5; section references 7 including "section 3.2 item 3b", "section 3.5", "section 3.4", "section 6", "section 8"; INV references 4; O labels 1). Two do not resolve unambiguously: B 7 says "what M2 already requires (module-declared category, lens and severity sets)" and "because M2 is a decided requirement", while B 6 defines its own M2 as the `in_diff` precision measurement (label collision with research/13 M2; same collision for M1, where B 7 line 108 uses M1 for the B 6 cost measurement). DC = 33/35 = 0.9429.

### Section coverage (SC)

- A: 8 H2 (1 position, 2 design consequence, 3 evidence, 4 invariants, 5 consistency, 6 test, 7 effect, 8 objection). SC = 8/9 = 0.8889.
- B: 9 H2 (1-8 as above plus 9 limits). SC = 9/9 = 1.0000.

### Quantitative table

| Metric | Weight | Variant A raw counts | Variant A score | Variant B raw counts | Variant B score |
|---|---|---|---|---|---|
| RC | 0.30 | 16 of 17 matched | 0.9412 | 17 of 17 matched | 1.0000 |
| IC | 0.25 | 4 contradictions in 98 claims | 0.9592 | 3 contradictions in 110 claims | 0.9727 |
| SR | 0.15 | 95 concrete, 3 vague (of 98) | 0.9694 | 110 concrete, 0 vague (of 110) | 1.0000 |
| DC | 0.15 | 10 of 10 references resolve | 1.0000 | 33 of 35 references resolve | 0.9429 |
| SC | 0.15 | 8 H2 of max 9 | 0.8889 | 9 H2 of max 9 | 1.0000 |
| quant_score | | 0.2824 + 0.2398 + 0.1454 + 0.1500 + 0.1333 | 0.9509 | 0.3000 + 0.2432 + 0.1500 + 0.1414 + 0.1500 | 0.9846 |

## Qualitative (Pass 1)

Rule applied: MET only with a direct quote or section reference; otherwise NOT MET. Factual errors verified by the diff analysis, the debate, or my re-checks are applied in Correctness. Section numbers refer to each variant's own H2 numbering.

### Completeness

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

## Qualitative summary (Pass 1)

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

## Edge case floor check

| Variant | Invariant & Edge Case score | Floor (at least 1/5) | Eligible as base |
|---|---|---|---|
| A | 4/5 | passed | yes |
| B | 5/5 | passed | yes |

No variant scores 0/5, so the floor is not suspended and no warning is needed.

SCORES_PASS1
quant_A=0.9509
quant_B=0.9846
qual_A=21/30
qual_B=24/30
verdicts_A=Completeness:01111;Correctness:00101;Structure:11111;Clarity:11111;Risk:00001;Invariant:10111
verdicts_B=Completeness:01111;Correctness:01001;Structure:11111;Clarity:11111;Risk:00111;Invariant:11111
END
