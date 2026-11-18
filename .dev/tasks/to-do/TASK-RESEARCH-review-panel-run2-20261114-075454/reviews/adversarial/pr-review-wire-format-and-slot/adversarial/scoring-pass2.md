# Scoring Pass 2 (reverse order): slot C-10 pr-review-wire-format-and-slot

Scorer: Pass 2, neutral and independent. Order of evaluation: Variant B (`variant-2-original.md`) read and scored first, then Variant A (`variant-1-original.md`). Evidence inputs read: `diff-analysis.md`, `debate-transcript.md`, `invariant-probe.md`, the scoring protocol. Pass 1 file not read. Nothing was executed; repository facts are taken from the verified rows of the diff analysis and the debate.

Counting rules used for both variants (same rules, stated once):
- Scorable claim (IC): one numbered or bulleted design, evidence, invariant, test or objection item, or one table row, that states a specific falsifiable fact or commitment. Headings, status lines, the Limits section of B and header metadata are excluded.
- Concrete or vague (SR): each scorable claim is classed concrete when its main assertion carries a number, file and line, named entity or threshold, and vague when its main assertion is left undecided, unquantified or unspecified.
- Internal reference (DC): a reference to a section, numbered item, evidence row, test, measurement or invariant defined in the same file. References to other documents (research files, adjudication results, other slots) are excluded.
- RC: a variant matches a requirement when a section explicitly addresses it. R-14 needs both open questions and the "adapter now, extensible v2 later" lean. R-16 needs Wave 2-4 flow plus at least one of (reply and resolve, bots-silent case).

## Quantitative

| Metric | Weight | Variant A raw counts | Variant A score | Variant B raw counts | Variant B score |
|---|---|---|---|---|---|
| RC requirement coverage | 0.30 | 16 of 17 matched (R-16 not matched) | 0.9412 | 16 of 17 matched (R-14 not matched) | 0.9412 |
| IC internal consistency | 0.25 | 58 scorable claims, 4 contradictions | 0.9310 | 56 scorable claims, 3 contradictions | 0.9464 |
| SR specificity ratio | 0.15 | 52 concrete, 6 vague | 0.8966 | 52 concrete, 4 vague | 0.9286 |
| DC dependency completeness | 0.15 | 11 internal references, 10 resolve | 0.9091 | 31 internal references, 28 resolve | 0.9032 |
| SC section coverage | 0.15 | 8 H2 of max 9 | 0.8889 | 9 H2 of max 9 | 1.0000 |
| quant_score | 1.00 | RC 0.2824 + IC 0.2328 + SR 0.1345 + DC 0.1364 + SC 0.1333 | 0.9193 | RC 0.2824 + IC 0.2366 + SR 0.1393 + DC 0.1355 + SC 0.1500 | 0.9437 |

### RC detail (source requirements R-01 to R-17 from diff-analysis.md)

| Req | Variant A (section) | Variant B (section) |
|---|---|---|
| R-01 | Match: section 1 and INV-E in section 4 (Finding, Severity, FSM, `REVIEWERS`, no gh or git in core) | Match: section 1 last sentence and INV-E row in section 5 |
| R-02 | Match: section 3.3 (12 lines in 3 files, no row pin, the 50 files "not run") | Match: B11 and T2 (static reading, no pytest run) |
| R-03 | Match: section 6 item 6 (GQ-177, cost unmeasured, how to measure) | Match: section 6 M1 (cost per round on 3 to 5 PR diffs) |
| R-04 | Match: section 4 (INV-E HIGH, INV-F MEDIUM, INV-C) | Match: section 5 (INV-E, INV-F, INV-C rows) |
| R-05 | Match: section 2 (FX-5, per-module mapping tables, is_groundable fail-closed) | Match: section 3.1 item 1 (module-declared vocabularies), B5, B6 |
| R-06 | Match: section 5 (C-01, C-02, C-03 with dependencies) | Match: section 2 table (C-01, C-02, C-03) |
| R-07 | Match: section 2 last bullet, INV-I in section 4, section 5 C-03 (complete_reviewers, invalid_reviewers, valid_blocks) | Match: section 3.2 item 6 (derivation from COMPLETION_STATES), B10 |
| R-08 | Match: section 2 "main-session only (SKILL.md:47-49)" | Match: section 3.3 |
| R-09 | Match: section 6 (seven falsifiable claims) | Match: section 6 (T1 to T4, M1 to M3) |
| R-10 | Match: section 7 | Match: section 7 |
| R-11 | Match: section 8 | Match: section 8 |
| R-12 | Match: section 5 last bullet of C-03 ("requested, not served") | Match: section 2 C-03 row condition 5, section 5 row |
| R-13 | Match: INV-F in section 4 | Match: INV-F row in section 5 |
| R-14 | Match: header "adapter now", section 1 last sentence ("a later move to one wire format stays open"), section 8 (promote to core when a second consumer needs it); both questions addressed | Not matched: both questions are argued in sections 1 and 8, but the research/13 lean "adapter now, extensible v2 later" is never named and GQ-179 and GQ-182 are not cited |
| R-15 | Match: section 2 pr_submit bullets, section 3.4 | Match: section 1, section 3.2 item 2, M2 |
| R-16 | Not matched: section 3.7 says panel findings "enter that same path" but reply, resolve and the bots-silent case are not addressed (debate concession 6, items c and d) | Match: section 3.3 (Wave 2 to 4 chain) and O3 (bots-silent case, stated as OPEN); reply and resolve not addressed |
| R-17 | Match: line 7 states no run-1 file cited; none cited | Match: no run-1 file cited |

### IC detail

Variant A, 58 claims (section 1: 1; section 2: 7; section 3: 16; section 4: 11; section 5: 11; section 6: 7; section 8: 5). Contradictions found, 4:
1. Section 2 (line 20) says the adapter reads "the highest member severity" from the cluster output; section 3.5 (line 54) lists what cluster output holds (`primary_citation`, `claim`, `blocking_any`, `disputed`, `reviewers`, `members[]`) and severity is not in it. The debate verified the cluster record has no severity or category (diff-analysis X-001, [CODE-CONTRADICTED]).
2. Section 6 item 1 (line 101) says no existing test file is edited; section 6 item 2 (line 102) says "Add the module to the static no-shell-token check", an edit to the module list in `test_static_grep.py` (A concedes this, debate concession 7); section 4 (line 66) repeats it.
3. Section 8 (line 121) says downstream "only reads path, line, body, category and the route"; section 3.4 (line 49) itself lists `fsm.py:902-906` and router steps 3 and 4 as readers of `in_diff` and `confidence`. Verified false in the debate (diff-analysis A-004).
4. Section 3.4 (line 50) objects that a fourth `confidence` meaning would need a type chosen; section 2 (line 24) has the adapter set `confidence` "from cluster facts (for example `disputed`)", which is a fourth meaning (B Round 1 weakness 2, conceded by A).

Variant B, 56 claims (section 1: 1; section 2: 3; section 3: 13; section 4: 14; section 5: 9; section 6: 7; section 8: 9). Contradictions found, 3:
1. B9 (line 66) says a third name "reuses this bookkeeping"; section 3.2 item 3 (a2) (line 35) excludes the panel from the re-trigger path and from `reviewer_activity`, leaving only the name-agnostic absent fold (diff-analysis X-008, conceded by B).
2. Section 2 C-03 row (line 20) says "B does not call `merge_round`"; section 3.2 item 6 (line 38) derives `incomplete` from "a C-03 quorum refusal", which C-03 defines as a ledger merge-time refusal. B never says where the refusal runs on the PR path. The rule does not exist at HEAD (diff-analysis X-009, conceded by B).
3. B1 (line 58) argues that "any converter" drops `quote`, the second citation and `blocking` at the conversion point; section 3.2 items 1 and 2 (lines 33 and 34) have B's own reader build a slot-less `Finding` from `citations[0]` and `claim`, dropping the same fields (diff-analysis C-012).

### SR detail

Vague claims, A (6): section 2 `confidence` "from cluster facts or left None"; section 4 INV-E "natural place ... I did not open it and do not state what it asserts"; section 4 INV-J table "a PR-module choice"; section 4 per-round cost "if the owner wants"; section 5 C-03 "applies the PR profile's floor" (value unspecified); section 6 item 5 "a large share". Vague claims, B (4): section 3.5 threshold "does not decide"; section 6 M2 "a pre-registered fraction of lines"; section 8 O3 "OPEN"; section 8 O4 "a reader decision B does not make here".

### DC detail

Variant A, 11 internal references: INV-I (section 2 to 4), "per 3.3" (section 4), "(3.1)" (section 5), INV-E (section 7), "(3.5)", "(3.2)", "(3.1)", "(3.4)", "(3.3)", "(6.2)" (section 8), "S1-S5" (section 4, INV-J). Unresolved: "S1-S5" is defined nowhere in the file (10 of 11 resolve).

Variant B, 31 internal references: INV-E, "section 3.2 item 3 and 6" (2), (i) and (ii), B1, B13 (section 3.2), item 3b, section 6 T3, section 8 objection 3 (resolves to O3), B5 and B6, B1 in M3, B4, M1, B2, B1, B14, B13, B10, B9, M1, "B1 to B8", "B9, B10, B13", item 3b, section 3.5, section 3.4, M2 (in O2), B11, B10, and the unprefixed "M2" twice in section 7 and "(M10)" in section 3.1 item 4. Unresolved (3): section 7 "what M2 already requires" and "M2 is a decided requirement" point at research/13 M2 (module-declared sets) but resolve inside the file to B's own section 6 M2 (in_diff precision); "(M10)" in section 3.1 item 4 is defined nowhere in the file. 28 of 31 resolve.

## Qualitative (Pass 2)

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

## Qualitative summary

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

Reading of the result: the two variants tie on the qualitative layer in Pass 2, but for different reasons. Variant A fails Correctness criteria 1, 2 and 4 (verified defects: cluster record lacks severity and category, "downstream reads only four fields" is false, 50 files is wrong, the adapter input is insufficient as written). Variant B fails Correctness criteria 1, 3 and 4 (verified defects: B4 overstated, a quorum refusal that does not exist, an M2 label collision, three internal contradictions) but its design is buildable as stated. The quantitative layer separates them slightly: B leads on IC (0.9464 against 0.9310), SR (0.9286 against 0.8966) and SC (1.0000 against 0.8889); A leads on DC by 0.0059; RC ties at 0.9412. Combined with equal qual_score, B is ahead by about 0.0122 on the unweighted half-sum (quant 0.9437 against 0.9193), inside the 5 percent tiebreaker band.

## Edge case floor check

Rule: a variant scoring below 1 of 5 on Invariant and Edge Case Coverage is ineligible as base.

| Variant | Invariant and Edge Case score | Eligible as base |
|---|---|---|
| A | 5 of 5 | Yes |
| B | 5 of 5 | Yes |

No variant scores 0 of 5, so the floor is not suspended and no warning applies.

## Machine-readable block

```
SCORES_PASS2
quant_A=0.9193
quant_B=0.9437
qual_A=22/30
qual_B=22/30
verdicts_A=Completeness:01111;Correctness:00101;Structure:11111;Clarity:01101;Risk:00111;Invariant:11111
verdicts_B=Completeness:01111;Correctness:01001;Structure:11111;Clarity:01101;Risk:00111;Invariant:11111
END
```
