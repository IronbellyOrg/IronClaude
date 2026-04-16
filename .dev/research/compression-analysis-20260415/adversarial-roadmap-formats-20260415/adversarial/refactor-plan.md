# Step 4: Refactoring Plan (V-B as Base)

**Date**: 2026-04-15
**Base variant**: V-B (opus:architect) — selected blind, score 0.870
**Refactor donors**: V-A (opus:analyzer, 0.832, floor-ineligible) and V-C (sonnet:scribe, 0.771)
**Checkpoint-2 disposition**: Accept with caveats (INV-1, INV-3, INV-5 carry-forward)
**Scope framing**: Recommendation explicitly scoped to Opus 4.6 / Sonnet 4.6; Haiku 4.5 gated to plain Markdown until A/B ships

---

## 1. Base variant skeleton (V-B)

V-B's existing structure is preserved in the merge and forms the load-bearing skeleton. Section list:

- **Verdict (preview)** — V-B's headline framing ("narrower form than source claims"; hybrid defensible for reliability + selective loading, not raw compression)
- **Part A: Pillar 1 — XML Trained Priors in Claude**
- **Part B: Pillar 2 — TOON Tabular Compression**
- **Part C: Pillar 3 — Markdown Prose Fidelity**
- **Part D: Honest Weaknesses & Reinforcement** (Weakness 1: compression baseline; Weakness 2: Haiku accuracy)
- **Part E: Concrete Prototype** — the tiktoken `cl100k_base` measurements on the Phase 2 slice (350 / 308 / 316 / 233 token table)
- **Part F: Haiku Risk — Killer or Bounded Concern?**
- **Part G: Independent Ranked Format List** (Compact MD DSL #1, Hybrid #2, XML+MD #3, YAML-MD #4, pure TOON #5)
- **Final Verdict**
- **File path + Sources consulted**

The merge preserves this Parts A-G order. New sections (Part H: Known Gaps; Part I: Migration Path; Part J: Symmetric-Search Grid for future audits) are appended after Part G. The Final Verdict is rewritten to fold in injected material, but its five amendment bullets are kept as the spine.

---

## 2. Planned injections (from V-A)

### Injection A1 — D-5: Format Tax paper misapplication

- **Source**: V-A Part A row 11 + Part E item 3 (verbatim: *"most recent closed-weight models show little to no format tax, suggesting the problem is not inherent to structured generation but a gap that current open-weight models have yet to close"*)
- **Target**: V-B Part D, new sub-section **"Weakness 3: The Format Tax citation weakens, not strengthens, the case"** (inserted after V-B's existing Weakness 2)
- **Change**: Add a paragraph stating that arXiv 2604.03616 ("The Format Tax") — which the source report cited to justify format engineering — actually finds that closed-weight frontier models show little format tax. Since Sonnet 4.6 / Opus 4.6 are closed-weight frontier, the paper undercuts rather than supports the source's urgency. Include the verbatim quote.
- **Rationale**: Debate Round 2 convergence — V-A flagged this as a misapplication V-B missed entirely. V-B's Round 1 output did not engage D-5; the base-selection document lists this as an explicit V-B gap to be filled from V-A (see base-selection §6 "Known gaps V-B brings"). V-A's Round 2 position survived challenge.
- **Integration approach**: Add new sub-section under Part D. No rewrite of existing weaknesses.
- **Risk**: **LOW** — additive weakness entry in a section already structured around weakness enumeration.

### Injection A2 — D-6: arXiv 2603.03306 cherry-pick

- **Source**: V-A Part A row 12 + Part E item 4 (verbatim: *"Plain JSON generation shows the best one-shot and final accuracy, even compared with constrained decoding structured output"* and *"often reduced by the 'prompt tax' of instructional overhead in shorter contexts"*)
- **Target**: V-B Part B (Pillar 2 — TOON Tabular Compression), appended as a new paragraph at the end of "Steelman evidence" titled **"Counter-finding from the same paper"**
- **Change**: Note that arXiv 2603.03306, cited by the source as academic backing for TOON, actually says plain JSON generation shows the best one-shot and final accuracy and that TOON's efficiency is eroded by prompt tax in shorter contexts. Source report suppressed this finding.
- **Rationale**: Debate Round 2 — V-A's verbatim counter-quote was one of the 3 misattributions V-A caught and V-B missed. Base-selection §6 explicitly carries this forward.
- **Integration approach**: Append paragraph inside existing Part B subsection. Do not remove V-B's existing steelman evidence for TOON.
- **Risk**: **LOW** — text addition inside existing section; no flow disruption. V-B's Pillar 2 is already framed as "holds with amendments," so a counter-finding from the paper the source cited strengthens the amendment.

### Injection A3 — D-8: Direct composition measurement supersedes estimate

- **Source**: V-A Part C composition table — **25.4% tables, 47.7% bullets, 6.2% numbered, 4.9% headings** (vs source's 9% table estimate) and the derivation that the 9% table claim is implausibly narrow.
- **Target**: V-B Part D Weakness 1 ("The compression numbers are against the wrong baseline"), inserted as a new paragraph titled **"Direct composition measurement"** before the existing "My measurement" paragraph
- **Change**: Replace V-B's implicit acceptance of the source's composition breakdown with V-A's directly measured character shares. Explicit callout that source's "9% table scaffolding" is wrong under any reasonable accounting; tables are ~25% of the file.
- **Rationale**: V-A's measurement grounds V-B's arithmetic. V-B re-derives compression but assumes the source's composition; V-A re-measured composition directly. Combined, they close the arithmetic chain the source left open (base-selection §6).
- **Integration approach**: Insert paragraph at the top of Weakness 1 so V-B's existing reinforcement attempt still flows. Update V-B's final "Net: ~20% tokens, not 40%" sentence to reference V-A's measurement as the basis for the composition share.
- **Risk**: **LOW** — additive measurement row; does not contradict V-B's numbers (tiktoken 350→308 stands). Strengthens arithmetic provenance.

### Injection A4 — Verbatim Anthropic quote proving 30% misattribution

- **Source**: V-A Part E item 1 — verbatim quote: *"Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs"* and the explicit note that Anthropic attributes 30% to query placement, not XML tags.
- **Target**: V-B Part A ("Pillar 1 — XML Trained Priors in Claude"), replacing V-B's softer framing around item 3 (which currently says *"The 30% long-context number... presented in the context of XML-wrapped document structure"*)
- **Change**: Replace V-B's item-3 soft reading with V-A's verbatim quote and the explicit misattribution finding: Anthropic attributes the 30% gain solely to query placement at the end of the prompt, not to XML. XML is a separate bullet with no quantified gain. The source report's conflation is a misattribution, not a soft reading.
- **Rationale**: V-B's Part A currently frames this as "presented in the context of XML-wrapped document structure," which is directionally correct but soft. V-A has the verbatim counter-quote that proves the misattribution cleanly. Debate Round 2 — V-B conceded this framing was too soft. Base-selection §6 lists this as "V-B has the softer 'disclaimer' framing but not the verbatim counter-quote."
- **Integration approach**: Replace text (the existing paragraph labelled "3. **The 30% long-context number**"). Preserve V-B's downstream "Honest downgrade" paragraph.
- **Risk**: **MEDIUM** — this is a text replacement inside V-B's steelman argument. If mis-applied, it could break Pillar 1's "survives intact" framing. Mitigation: the replacement downgrades the evidence but keeps the pillar's disambiguation argument (canonical tags, prefill deprecation, 20k+ wrap guidance) untouched.

---

## 3. Planned injections (from V-C)

### Injection C1 — D-7: arXiv 2601.12014 counter-benchmark with full GCS breakdown

- **Source**: V-C Part B1 — arXiv 2601.12014 "Are LLMs Ready for TOON?" with the full numbers: TOON structural correctness (GCS) **38.9% lower than JSON, 30.9% lower than XML, 42.2% lower than YAML**; token savings 26.4% vs JSON but correctness penalty substantial; balanced scoring (gamma=0.5) keeps baseline formats ahead of TOON; larger models reduce but do not eliminate the gap.
- **Target**: V-B Part B (Pillar 2), appended as a new sub-section titled **"Independent counter-benchmark (arXiv 2601.12014)"** after the "honest confidence level" paragraph
- **Change**: Add the full 38.9%/30.9%/42.2% GCS breakdown with the verification note that V-A and V-B subsequently confirmed the paper exists and the numbers match the abstract (Round 2). Note that the gap narrows on larger models but does not close, so the correctness concern is not purely a Haiku problem.
- **Rationale**: V-C was the unique finder of this paper in Round 1. Debate Round 2 required V-A and V-B to fetch and verify; both confirmed the numbers verbatim. Base-selection §6 — "Missing arXiv 2601.12014 in Round 1. V-B verified in Round 2 with open-weight-only caveat — that verification must be preserved in the merge."
- **Integration approach**: Add new sub-section. Preserves V-B's existing Pillar 2 text.
- **Risk**: **MEDIUM** — introduces a genuinely adverse finding inside a pillar V-B labels "holds with amendments." The merge must make clear this is why Pillar 2 is demoted, not why it collapses. Mitigation: sub-section title says "counter-benchmark" not "refutation"; existing confidence downgrade (0.55) in V-B already accommodates it.

### Injection C2 — Migration path discipline (3-phase)

- **Source**: V-C Part F "Migration Path" — Phase 1 (adopt XML+MD now, measure on 3-5 real roadmap files, expected -10% to -20%), Phase 2 (A/B test vs XML+TOON+MD on both Sonnet and Haiku; measure tokens, extraction accuracy, parsing error rate), Phase 3 (conditional upgrade if Phase 2 shows ≥10% additional savings with ≤2% accuracy degradation)
- **Target**: New **Part I: Migration Path** appended after V-B's Final Verdict. Also updates V-B Part G's footnote "I would rerank the hybrid to #1 the moment per-phase loading ships" to cite the 3-phase gating.
- **Change**: Replace V-B's handwave ("I would rerank when per-phase loading ships") with V-C's disciplined 3-phase structure: adopt safe choice now → empirical A/B on real roadmap files → conditional upgrade with explicit pass criteria. Scope Phase 1 to Opus/Sonnet per checkpoint-2 framing.
- **Rationale**: V-B's reranking trigger is informal and untestable. V-C's migration path is testable and gated on measurable criteria (≥10% savings, ≤2% accuracy degradation). Base-selection §6 — V-C's migration path is V-B's gap filler. Checkpoint-2 framing requires the Haiku path to be gated on A/B completion; V-C's Phase 2 is exactly that gate.
- **Integration approach**: New section (Part I). Additionally modify V-B Part G paragraph "Why I reordered" item 3 to cross-reference Part I instead of the loose "per-phase loading" trigger.
- **Risk**: **MEDIUM** — adds a new section (structural change). Risk is that Part I duplicates Part G's decision rule. Mitigation: Part I is framed as "operational gating for when to switch recommendations," while Part G remains the current-state ranking. Cross-references keep them coherent.

### Injection C3 — Symmetric-search grid for future audits

- **Source**: V-C Part A benchmark inventory table (methodology match, symmetric search evidence, verdict columns) — the structural framework itself, not V-C's specific findings
- **Target**: New **Part J: Symmetric-Search Audit Grid** appended after Part I (Migration Path)
- **Change**: Add V-C's benchmark inventory column headers (Benchmark / Source, Cited in report, Methodology match, Symmetric search evidence, Verdict) as a reusable template for future format audits. Not populated with V-C's specific verdicts — the grid itself is the artifact.
- **Rationale**: V-C's methodological contribution (Round 1 unique) is a framework for detecting confirmation bias in benchmark selection. Base-selection §6 — "dimension 6d (N=1 generalization) not flagged" in V-B is partially addressed by V-C's sample-size discipline, and the audit grid is the artifact that operationalizes it for future use.
- **Integration approach**: New section (structural addition). Presented as a methodology contribution, explicitly attributed to V-C.
- **Risk**: **LOW** — appended at end; does not interact with existing sections. Worst case it is removed for length without breaking flow.

---

## 4. Planned caveats (Part H: Known Gaps)

New **Part H: Known Gaps / Unaddressed Risks** inserted between V-B's Final Verdict and Part I (Migration Path). The section is prominent per checkpoint-2 "Accept with caveats" disposition.

### INV-1 — Tokenizer generalization

- **ID**: INV-1
- **Description**: V-B's empirical backbone (Part E) uses `tiktoken cl100k_base`, which is OpenAI's tokenizer family, not Claude's native tokenizer. The -12.0% / -33.4% phase-slice measurements may drift when re-run against Anthropic's actual `count_tokens` endpoint. Direction of drift is unknown; prior community reports suggest Claude's tokenizer is close to cl100k on English prose but diverges on structured delimiters and code-adjacent content — exactly the content TOON and XML introduce.
- **Recommended resolution**: Re-run the Part E prototype (original Markdown, hybrid XML+TOON+prose, XML-only, Compact MD DSL) through Anthropic's `count_tokens` API on Claude Sonnet 4.6 and Opus 4.6. Publish a side-by-side table with cl100k_base vs native. If the delta between formats shifts by more than 3 percentage points, the Part G ranking must be revisited.
- **Status as of merge**: UNRESOLVED. The recommendation is conditionally valid under the cl100k_base assumption; final ranking is gated on the re-measurement.

### INV-3 — Consumer DAG unmapped

- **ID**: INV-3
- **Description**: The D-10 split (compression vs reliability) collapses when asked *"reliable for whom?"*. V-B Part F names the roadmap consumers (`sc:pm`, `sc:tasklist`, `sc:task-unified`, `sc:validate-roadmap`, `sc:adversarial`) but does not enumerate their actual read patterns — sequential full-file, selective per-phase, targeted section extraction, or iterative re-read. Without a consumer DAG, "selective loading wins" is a claim without a bound.
- **Recommended resolution**: Enumerate each of the five named consumers with: (a) current read pattern (full / phase-scoped / section-scoped), (b) token footprint per call, (c) frequency of roadmap ingest per pipeline run, (d) whether the consumer is Opus, Sonnet, or Haiku. Publish as a consumer-read-matrix. Selective-loading claims must cite specific cells in that matrix, not general "per-phase pipeline coming soon" language.
- **Status as of merge**: UNRESOLVED. V-B's Part F Haiku reasoning ("roadmap consumers are Sonnet/Opus-class; Haiku is auxiliary") is directionally defensible but not evidenced by a matrix. The merge should flag that the 10% Haiku-traffic estimate is an assertion, not a measurement.

### INV-5 — HAIKU UNTESTED

- **ID**: INV-5
- **Description**: All three candidate formats (Compact Markdown DSL, Hybrid XML+TOON+prose, XML+Markdown no TOON) have **zero direct Haiku 4.5 benchmark measurements on roadmap-shaped content**. V-B and V-A both extrapolate from webmaster-ramos per-format scores; V-C correctly notes hybrid formats may compound parsing difficulty and there is no hybrid-format benchmark anywhere in the evidence base. The 5.7 pp MD vs JSON gap on Haiku is from a non-roadmap extraction benchmark.
- **Recommended resolution**: Haiku A/B test with ≥20 retrieval prompts drawn from actual SuperClaude tasklist generation. Measure: token count, task extraction F1, parsing error rate per format. Candidates: (1) plain Markdown baseline, (2) Compact MD DSL, (3) Hybrid XML+TOON+prose, (4) XML+Markdown. Do not adopt any non-Markdown format on Haiku paths until this A/B completes.
- **Status as of merge**: UNRESOLVED. Per checkpoint-2 framing: **Haiku 4.5 pipelines must use plain Markdown until the A/B completes.** The recommendation in Part G is scoped to Opus 4.6 and Sonnet 4.6 only.

---

## 5. Base weaknesses acknowledged

Three V-B claims need softening or reframing due to Round 2 concessions and injection interactions:

1. **Part A item 3 (the 30% long-context number)** — softened to verbatim-quote form per Injection A4. V-B's phrasing "presented in the context of XML-wrapped document structure" is replaced; the 30% is now explicitly attributed to query placement, with XML as a separate unquantified recommendation.

2. **Part G item 3 of "Why I reordered" — "I would rerank the hybrid to #1 the moment per-phase loading ships"** — this reranking trigger is withdrawn in favor of Injection C2's 3-phase gating. Per base-selection §6 carry-forward and V-C's migration-path discipline, the rerank trigger becomes: *"Hybrid is reranked to #1 only after Part I Phase 2 A/B test shows ≥10% additional savings with ≤2% accuracy degradation on the target models."* The per-phase loading handwave is replaced with measurable criteria.

3. **Part F confidence numbers ("High 0.85 that Haiku risk is bounded")** — softened by Part H INV-5. The Haiku risk is bounded *conditional on the A/B test*, not bounded in absolute terms. V-B's Part F text remains but is flagged with a forward-reference to INV-5 ("see Part H, INV-5, for the unresolved benchmark gap"). The 0.85 number is not removed but is annotated as "conditional on A/B completion."

---

## 6. Changes NOT being made

Transparency section. Differences considered and rejected, with rationale.

1. **V-C's XML+MD #1 ranking is NOT adopted.** V-C's bias-aware Part F recommends "Hybrid XML + Markdown (without TOON)" as #1. This is rejected because V-B's direct tiktoken measurement (Compact MD DSL at -33.4% on the Phase 2 slice, XML-only at -9.7%) and V-A's independent top-rank agreement on Compact MD DSL constitute a 2-of-3 consensus that Compact MD DSL is #1. V-C did not run its own tokenizer measurement and its ranking rests on correctness-over-compression reasoning that the ranking already encodes in the #2 slot. Preserving V-B+V-A's Compact-MD-DSL #1 is the consensus; V-C's #1 is preserved as a footnote in Part H INV-5 (the Haiku-path caveat).

2. **V-C's format-switching cognitive-load argument is NOT carried forward.** V-C Part E2 Passage 1 and Part C both invoke "cognitive load of format-switching within a single document (XML → TOON → MD → XML → TOON)." V-C retracted this claim in Round 2 after V-B pointed out that format-switching load is not benchmarked anywhere and Anthropic's own docs are MD+XML hybrids used without reported issue. The cognitive-load framing does not appear in the merge. The correctness-penalty argument (via Injection C1 / arXiv 2601.12014) is kept; cognitive-load speculation is dropped.

3. **V-A's untested conventions-header claim is NOT carried forward.** V-A Part D "Decision rule" says *"a 60-token conventions header reliably closes"* the Haiku MD-vs-JSON 5.7 pp gap. V-A withdrew this in Round 2 — the conventions header is untested on Haiku and the "reliably closes" language is speculative. The Compact MD DSL recommendation is preserved (it survives on Sonnet/Opus grounds), but the claim that a conventions header fixes Haiku is dropped. Part H INV-5 is where this gap lives.

4. **V-A's "Hybrid will actually land at 3,700-4,000 tokens" prediction is NOT used to demote Hybrid further.** V-A made a specific falsifiable prediction that Hybrid would underperform Compact MD DSL on the full file. V-B's Part E measurement covers only the Phase 2 slice, not the full file. The prediction is directionally consistent with V-B Part G #1-vs-#2, but using V-A's unvalidated full-file projection to re-rank would exceed the evidence base. The merge keeps Part G's current ranking (Compact MD DSL #1, Hybrid #2) without sharpening the gap beyond what Part E measured.

5. **V-C's Part E2 "speculative neuroscience language" critique of V-B is NOT carried forward as a direct attack.** V-C critiqued the source report's *"activates trained structural priors"* framing. V-B Part A "Honest downgrade" already softens this to "unambiguous delimiter pairs resist confusion... Claude's RLHF extensively uses XML-tagged examples." The Round 2 softening is already in V-B; no additional attack surface is added.

6. **Full replacement of V-B's Part E prototype with V-A's Compact MD DSL derivation is NOT done.** V-A's Part D derives Compact MD DSL savings itemized (195 backtick tokens, 300 traceability duplicate tokens, etc.). This is complementary to V-B's tiktoken measurement, not a replacement. The merge keeps V-B's Part E (the direct measurement) and adds V-A's itemized breakdown as an appendix reference, but does not swap the empirical backbone.

---

## 7. Final merged structure

Ordered section list with source variant and role:

| # | Section | Source | Role |
|---|---------|--------|------|
| 1 | Verdict (preview) | V-B | Headline framing — hybrid holds in narrower form |
| 2 | Part A — Pillar 1 (XML) | V-B + **A4** | Steelman XML, with verbatim Anthropic quote correcting 30% misattribution |
| 3 | Part B — Pillar 2 (TOON) | V-B + **A2** + **C1** | Steelman TOON, with arXiv 2603.03306 cherry-pick counter + arXiv 2601.12014 counter-benchmark |
| 4 | Part C — Pillar 3 (Markdown prose) | V-B | Unmodified — strongest surviving pillar |
| 5 | Part D — Honest Weaknesses | V-B + **A3** + **A1** | Weakness 1 (compression baseline) grounded in V-A composition measurement; Weakness 2 (Haiku) unchanged; new Weakness 3 (Format Tax misapplication) from V-A |
| 6 | Part E — Concrete Prototype | V-B | Unmodified empirical anchor — tiktoken cl100k_base Phase 2 slice measurements |
| 7 | Part F — Haiku Risk | V-B (annotated) | Bounded-concern framing with forward-reference to INV-5 |
| 8 | Part G — Independent Ranked Format List | V-B (modified item 3 of "Why I reordered") | Compact MD DSL #1, Hybrid #2 — consensus ranking |
| 9 | Final Verdict | V-B (refolded) | Five amendment bullets spine, folds in injected material |
| 10 | **Part H — Known Gaps / Unaddressed Risks** | **Checkpoint-2 external** | INV-1 tokenizer, INV-3 consumer DAG, INV-5 Haiku untested — prominent caveat section |
| 11 | **Part I — Migration Path** | **V-C (C2)** | 3-phase disciplined migration: adopt safe now → A/B → conditional upgrade |
| 12 | **Part J — Symmetric-Search Audit Grid** | **V-C (C3)** | Reusable framework for future format audits |
| 13 | Sources consulted | V-B + additions from V-A/V-C | Anthropic long-context, arXiv 2604.03616, arXiv 2603.03306, arXiv 2601.12014, tiktoken prototype, webmaster-ramos, Workman, Syntax & Empathy |

**Structural delta from V-B base**: 3 new sections (H, I, J), 0 removed sections, 3 modified sections (Part A item 3, Part B Pillar 2 evidence, Part D Weakness 1 + new Weakness 3), 1 annotated section (Part F), 1 refolded section (Final Verdict), 1 modified paragraph (Part G "Why I reordered" item 3).

---

## 8. Provenance annotation plan

For Step 5 merge execution, section-level attribution is recorded in two places:

1. **Inline attribution footnotes** at the end of each section that contains injected material. Format:
   `> *Merged from V-B Parts A-G (skeleton). Section edits: injected A4 (verbatim Anthropic quote) from V-A Part E.*`

   Specifically:
   - Part A gets an inline note citing V-A Part E item 1 for the 30% verbatim quote
   - Part B gets an inline note citing V-A Part E item 4 and V-C Part B1
   - Part D gets an inline note citing V-A Part C (composition measurement) and V-A Part A row 11 (Format Tax)
   - Part G gets an inline note citing V-C Part F (migration rerank criteria)
   - Part H gets an inline note citing Round 2.5 invariant probe (INV-1, INV-3, INV-5)
   - Part I gets an inline note citing V-C Part F
   - Part J gets an inline note citing V-C Part A

2. **Provenance appendix** at the end of the merged document titled **"Appendix: Provenance Matrix"** with columns: `Section | Source variant(s) | Injection IDs | Role`. This gives a one-glance reviewability map. The matrix mirrors section 7 of this plan but in the merged document's own voice (i.e., without the V-A / V-B / V-C blind naming after de-blinding, or with it preserved if the merge remains blind per protocol).

3. **Blind-naming preservation**: Until Step 5's de-blinding decision is made, V-A / V-B / V-C naming is preserved throughout the merged output. If de-blinding occurs before Step 5 publication, the provenance matrix is the single place where the rename is applied; inline footnotes update automatically from the matrix.

4. **Injection IDs used**: A1 (Format Tax), A2 (arXiv 2603.03306 counter), A3 (composition measurement), A4 (verbatim 30% quote), C1 (arXiv 2601.12014 counter-benchmark), C2 (3-phase migration), C3 (symmetric-search grid). These IDs are referenced in the provenance appendix so that a reviewer can trace any merged claim back to its donor variant and the debate round that justified the injection.
