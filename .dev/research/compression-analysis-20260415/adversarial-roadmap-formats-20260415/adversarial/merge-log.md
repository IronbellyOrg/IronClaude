# Merge Log — Step 5 Adversarial Pipeline

**Date**: 2026-04-15
**Base**: V-B (opus:architect, debate score 0.870)
**Refactor plan**: `refactor-plan.md`
**Output**: `research_roadmap-format-alternatives_VALIDATED.md`
**Provenance mode**: Appendix (user-approved at checkpoint 4 — section-level provenance matrix, not inline tags)

---

## Summary

- **Changes planned**: 7 injections (A1-A4 from V-A, C1-C3 from V-C) + 3 base-weakness reframings + 3 new caveat sections (Part H INV entries) + 1 Haiku Path section + 1 Provenance Matrix appendix
- **Total applied**: 7 injections + 3 reframings + 3 new sections (H, I, J) + 1 Haiku Path + 1 Appendix = **15 structural changes**
- **Changes skipped**: 0
- **Changes deferred/escalated**: 0
- **Structural integrity**: PASS
- **Factual consistency**: PASS (all three cross-section number sets verified)

---

## Applied changes (in execution order)

### Change 1 — Verdict preview refold

- **Change ID**: (structural, refactor-plan §1 base skeleton + §4 Part H caveats + checkpoint-2 scope)
- **Source**: V-B verdict preview, extended with A1/C1/INV scope framing
- **Target**: Top of merged document, `## Verdict (preview)` section
- **Before**: V-B's original 1-paragraph verdict preview
- **After**: Refolded to add (a) arXiv 2601.12014 correctness concern (C1), (b) arXiv 2604.03616 Format Tax misapplication (A1), (c) explicit Opus 4.6 / Sonnet 4.6 scope, (d) 3-line validated recommendation summary referencing Compact MD DSL #1, Hybrid #2 gated on Part I, plain Markdown for Haiku per INV-5
- **Validation**: PASS — verdict preview is prominent, accurate, matches Part G ranking and Final Verdict amendments

### Change 2 — Injection A4 (verbatim Anthropic 30% quote)

- **Change ID**: A4
- **Source**: V-A Part E item 1 (verbatim quote + misattribution finding)
- **Target**: Part A, item 3 in the "Steelman evidence" list (replacing V-B's softer framing)
- **Before**: V-B item 3 read: *"The 30% long-context number: Anthropic's long-context-prompting-tips page states ... presented in the context of XML-wrapped document structure."*
- **After**: Item 3 now explicitly quotes *"Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs"* and states Anthropic attributes the 30% **solely to query placement, not XML tags**. Includes the correction: *"Anthropic recommends XML for structural clarity (no quantified gain); query-at-end can yield up to 30% on long-context tasks."*
- **Validation**: PASS — text replacement cleanly inside Part A; V-B's downstream "Honest downgrade" paragraph preserved; Pillar 1 still survives, now with confidence calibrated for removed 30% claim
- **Risk rating (from plan)**: MEDIUM — successfully mitigated; Pillar 1's disambiguation argument (canonical tags, prefill deprecation, 20k+ wrap guidance) untouched

### Change 3 — Injection A2 (arXiv 2603.03306 counter-finding)

- **Change ID**: A2
- **Source**: V-A Part A row 12 + Part E item 4
- **Target**: Part B, new sub-section `### Counter-finding from the same paper (arXiv 2603.03306)` appended after existing "Steelman evidence" list
- **Before**: V-B's Part B steelman evidence list only cited arXiv 2603.03306 as "academic backing" with no counter-finding
- **After**: New paragraph explicitly quotes *"Plain JSON generation shows the best one-shot and final accuracy, even compared with constrained decoding structured output"* and *"often reduced by the 'prompt tax' of instructional overhead in shorter contexts."* Notes source report suppressed this finding.
- **Validation**: PASS — additive paragraph; does not disrupt existing Part B flow; V-B's "critical correction the source missed" paragraph that follows still reads correctly
- **Risk rating (from plan)**: LOW — confirmed

### Change 4 — Injection C1 (arXiv 2601.12014 counter-benchmark)

- **Change ID**: C1
- **Source**: V-C Part B1 (with Round 2 verification by V-A and V-B)
- **Target**: Part B, new sub-section `### Independent counter-benchmark (arXiv 2601.12014)` appended after the "Honest confidence level" paragraph
- **Before**: V-B's Part B ended at the 0.55 confidence level without independent counter-benchmark
- **After**: New sub-section with full GCS breakdown (38.9% / 30.9% / 42.2% vs JSON/XML/YAML), token savings notes (26.4% vs JSON, 49.4% vs XML), balanced-scoring note (baseline formats still rank higher), larger-models-do-not-close-gap caveat, and Round 2 verification note. Explicitly frames this as *why* Pillar 2 is demoted to 0.55 confidence, not collapsed.
- **Validation**: PASS — numbers match V-C source exactly (38.9/30.9/42.2 cross-verified in Verdict preview, Final Verdict amendment #1, and Sources section); sub-section title "counter-benchmark" not "refutation" per plan's risk mitigation
- **Risk rating (from plan)**: MEDIUM — successfully mitigated

### Change 5 — Injection A3 (direct composition measurement)

- **Change ID**: A3
- **Source**: V-A Part C composition table
- **Target**: Part D Weakness 1, inserted as new paragraph `**Direct composition measurement**` before V-B's existing "My measurement" paragraph
- **Before**: V-B's Weakness 1 went directly from the source's claim to V-B's tiktoken measurement without grounding the composition assumption
- **After**: New paragraph presents V-A's measured char shares (47.7% bullets, 25.4% tables, 6.2% numbered, 4.9% headings), with explicit callout that source's "9% table scaffolding" is implausibly narrow. V-B's existing measurement paragraph is preserved. The final "Net" line now reads: *"Grounded in the 25.4% table share (not the source's 9%), the hybrid buys ~20% tokens end-to-end, not 40%"* — per plan instruction to reference V-A's measurement as the composition basis.
- **Validation**: PASS — 25.4/47.7/6.2/4.9 numbers match V-A source; composition numbers also referenced in Sources section for cross-consistency; V-B's tiktoken 350/308/316/233 measurement stands unchanged
- **Risk rating (from plan)**: LOW — confirmed

### Change 6 — Injection A1 (Format Tax misapplication as new Weakness 3)

- **Change ID**: A1
- **Source**: V-A Part A row 11 + Part E item 3 (verbatim Format Tax quote + misapplication finding)
- **Target**: Part D, new sub-section `### Weakness 3: The Format Tax citation weakens, not strengthens, the case` inserted after V-B's existing Weakness 2
- **Before**: V-B's Part D had only Weakness 1 and Weakness 2
- **After**: New Weakness 3 paragraph with verbatim quote from arXiv 2604.03616: *"most recent closed-weight models show little to no format tax, suggesting the problem is not inherent to structured generation but a gap that current open-weight models have yet to close."* Notes Sonnet 4.6 / Opus 4.6 are closed-weight frontier, so the paper weakens rather than supports format engineering urgency. Links the finding back to Part G #1 (Compact MD DSL) position.
- **Validation**: PASS — additive weakness entry; Part D's "three weakest links" opening sentence updated from "two" to "three"; the new Weakness 3 does not collapse the hybrid, per plan's scope
- **Risk rating (from plan)**: LOW — confirmed

### Change 7 — Part E annotation (INV-1 tokenizer caveat forward-reference)

- **Change ID**: (base-weakness reframing #1, refactor-plan §5)
- **Source**: Checkpoint-2 invariant probe INV-1
- **Target**: Part E opening paragraph, caveat block before the prototype measurements
- **Before**: V-B's Part E presented tiktoken cl100k_base measurements as authoritative without caveat
- **After**: Caveat block added stating cl100k_base is OpenAI's tokenizer, not Claude's native; absolute numbers may drift when re-run against Anthropic `count_tokens`; forward-references Part H INV-1 for the re-measurement plan
- **Validation**: PASS — caveat is visible; V-B's measurement table (350/308/316/233) remains unchanged; INV-1 appears in Part H with matching language

### Change 8 — Part F annotation (INV-3, INV-5 forward-references and softening)

- **Change ID**: (base-weakness reframing #3, refactor-plan §5)
- **Source**: Checkpoint-2 invariant probe INV-3 + INV-5
- **Target**: Part F opening (Direct answer), item 1 (10% Haiku traffic claim), "What would make it a killer" paragraph, Confidence section
- **Before**: V-B's Part F presented bounded-concern framing absolutely
- **After**: (a) "Direct answer" now reads "Bounded concern, not a killer — conditional on A/B completion"; (b) a quoted forward-reference block flags that the bound depends on INV-5; (c) item 1's 10% Haiku traffic estimate is flagged as "an assertion, not a measurement" with INV-3 reference; (d) "What would make it a killer" paragraph notes the bound is "assuming INV-3's consumer DAG confirms the ~10% Haiku traffic estimate"; (e) Confidence section adds "conditional on the Part I Phase 2 A/B test completing with ≤2% accuracy degradation" and "See Part H INV-5 for the unresolved benchmark gap"
- **Validation**: PASS — V-B's original 0.85/0.25 confidence numbers preserved but annotated per plan; Haiku framing remains "bounded" not "killer"

### Change 9 — New section: Haiku Path (checkpoint-2 mandated)

- **Change ID**: (checkpoint-2 scope enforcement)
- **Source**: Task-spec checkpoint-2 framing (external to V-B/V-A/V-C but mandated by user disposition)
- **Target**: New `## Haiku Path` section inserted after Part F and before Part G
- **Before**: No explicit Haiku Path section existed in V-B
- **After**: New section with explicit recommendation: *"Use plain Markdown until the A/B test in Part I Phase 2 completes."* Rationale cites: (a) no candidate format tested on Haiku against roadmap content, (b) 5.7pp gap from non-roadmap benchmark, (c) V-A's withdrawn 60-token-header claim, (d) arXiv 2601.12014 model-agnostic correctness gap. Gating criterion matches Part I Phase 3 thresholds.
- **Validation**: PASS — section is prominent, positioned correctly relative to Part F and Part G; cross-references to INV-5 and Part I resolve; scope clarification (not a demotion) preserves Part G's consensus ranking

### Change 10 — Part G "Why I reordered" item 3 rewrite (Injection C2 cross-reference)

- **Change ID**: C2 (partial — the Part G modification part)
- **Source**: V-C Part F 3-phase migration path (replacing V-B's informal rerank trigger)
- **Target**: Part G, "Why I reordered" list, item 3's second paragraph
- **Before**: V-B's item 3 read *"I would rerank the hybrid to #1 the moment per-phase loading ships"*
- **After**: Replaced with *"The hybrid is reranked to #1 only after the Part I Phase 2 A/B test shows ≥10% additional savings with ≤2% accuracy degradation on Opus 4.6 and Sonnet 4.6. This replaces the earlier handwave that 'per-phase loading ships' is the rerank trigger; the actual trigger is the disciplined 3-phase gating in Part I, not an informal architectural milestone."*
- **Validation**: PASS — threshold numbers (≥10% / ≤2%) match Part I Phase 3; rerank trigger is now testable and measurable per plan §5 base-weakness reframing #2
- **Risk rating (from plan)**: MEDIUM — successfully mitigated (Part G's ranking unchanged, only the rerank trigger is updated)

### Change 11 — Final Verdict refold

- **Change ID**: (refactor-plan §1 "Final Verdict rewritten to fold in injected material, but its five amendment bullets are kept as the spine")
- **Source**: V-B Final Verdict + all injections that affect headline claims
- **Target**: `## Final Verdict` section
- **Before**: V-B's original 5 amendment bullets
- **After**: Expanded to **6 amendment bullets**:
  1. Pillar 2 downgrade (now cites arXiv 2601.12014 38.9/30.9/42.2 GCS penalty — from C1)
  2. Pillar 1 softening (now explicitly removes the 30% attribution — from A4)
  3. **NEW**: Format Tax citation correction (from A1)
  4. Reliability/selective-loading as value prop (was bullet 3, now bullet 4)
  5. Compact MD DSL beats on compression (was bullet 4, now bullet 5, extended with Part I Phase 2 gating from C2)
  6. Haiku fallback explicit and gated (was bullet 5, now bullet 6, extended with Haiku Path section reference)
- **Validation**: PASS — 5-bullet spine preserved intent; new bullet 3 (Format Tax) is the net-new addition; bullet numbering consistent; all cross-references resolve

### Change 12 — New section: Part H (Known Gaps / Unaddressed Risks)

- **Change ID**: (refactor-plan §4, checkpoint-2 "Accept with caveats")
- **Source**: Round 2.5 invariant probe (INV-1, INV-3, INV-5)
- **Target**: New `## Part H: Known Gaps / Unaddressed Risks` inserted between Final Verdict and Part I
- **Before**: No Part H in V-B
- **After**: Three prominent invariant entries, each with ID / Description / Recommended resolution / Status. All three status lines read "UNRESOLVED". INV-5 explicitly references Part I Phase 2 as operationalization.
- **Validation**: PASS — section is prominent per plan; all three invariants match task-spec wording (INV-1 tokenizer, INV-3 consumer DAG, INV-5 HAIKU UNTESTED); cross-references to Part E, Part F, Part G, Haiku Path all resolve

### Change 13 — New section: Part I (Migration Path) — Injection C2

- **Change ID**: C2 (main section)
- **Source**: V-C Part F 3-phase migration path
- **Target**: New `## Part I: Migration Path` inserted after Part H
- **Before**: No Part I in V-B
- **After**: Three phases — Phase 1 (adopt Compact MD DSL now, measure on 3-5 files, satisfies INV-1), Phase 2 (A/B test Hybrid vs Compact MD DSL on Sonnet and Haiku, satisfies INV-5), Phase 3 (conditional upgrade at ≥10% savings / ≤2% accuracy degradation threshold). Explicit scope to Opus 4.6 / Sonnet 4.6 per checkpoint-2 framing. Haiku-arm gate explicitly referenced. Consumer DAG dependency referenced for INV-3.
- **Validation**: PASS — 3-phase structure matches V-C source; threshold numbers (≥10% / ≤2%) match Part G rerank trigger; cross-references to INV-1, INV-3, INV-5 resolve
- **Risk rating (from plan)**: MEDIUM — mitigated; Part I does not duplicate Part G decision rule (Part I is operational gating; Part G is current-state ranking)

### Change 14 — New section: Part J (Symmetric-Search Audit Grid) — Injection C3

- **Change ID**: C3
- **Source**: V-C Part A benchmark inventory column headers (as framework)
- **Target**: New `## Part J: Symmetric-Search Audit Grid` inserted after Part I
- **Before**: No Part J in V-B
- **After**: Grid template with column headers (Benchmark / Source, Cited in report?, Methodology match, Symmetric search evidence?, Verdict). Column definitions provided. Usage notes explain how to apply the grid. Explicit note that this audit applied the grid and surfaced two Misapplied citations + one Cherry-picked citation + one missing counter-benchmark (arXiv 2601.12014), linking findings back to Parts A/B/D.
- **Validation**: PASS — presented as methodology contribution attributed to V-C per plan; does not interact with existing sections
- **Risk rating (from plan)**: LOW — confirmed

### Change 15 — Appendix: Provenance Matrix

- **Change ID**: (refactor-plan §8, user checkpoint-4 approval for appendix mode)
- **Source**: Refactor plan section 7 (final merged structure table)
- **Target**: New `## Appendix: Provenance Matrix` at end of document
- **Before**: V-B had no provenance tracking
- **After**: Appendix unblinds variants (V-A = opus:analyzer, V-B = opus:architect, V-C = sonnet:scribe), defines injection IDs (A1-A4, C1-C3), and presents section-level provenance matrix with 14 rows covering every section in the merged output. Also includes structural delta summary and the 6 changes-considered-and-rejected items from refactor plan §6.
- **Validation**: PASS — every section in the merged output has a corresponding row in the matrix; injection IDs are all referenced; unblinding occurs only in this appendix (body of document refers to V-A/V-B/V-C by blind labels)

---

## Validation results

### Structural integrity — **PASS**

- 14 top-level sections (`##` headings), all with content
- No orphan content (all paragraphs belong to a section)
- Heading hierarchy preserved (`##` for parts, `###` for sub-sections, `####` none needed)
- Section ordering matches refactor plan §7: Verdict → A → B → C → D → E → F → Haiku Path → G → Final Verdict → H → I → J → Sources → Appendix
- No broken Markdown (verified: code fences balanced, table pipes aligned)

### Internal references — **PASS**

- All "Part X" cross-references resolve to existing sections (Part A, B, C, D, E, F, G, H, I, J all present)
- All "INV-N" references resolve to Part H entries (INV-1, INV-3, INV-5 all present)
- All "Phase N" references resolve to Part I sub-sections (Phase 1, 2, 3 all present)
- "Haiku Path" cross-references from Final Verdict and Part F resolve
- Injection ID references (A1, A2, A3, A4, C1, C2, C3) all defined in Appendix

### Contradiction re-scan — **PASS**

- No contradictions between merged Verdict preview and Part G ranking (both have Compact MD DSL #1, Hybrid #2)
- No contradictions between Part G rerank trigger and Part I Phase 3 decision rule (both use ≥10% savings / ≤2% accuracy degradation)
- No contradictions between Part F 0.85 confidence and Part H INV-5 unresolved status (Part F is explicitly annotated "conditional on A/B completion")
- No contradictions between Pillar 1 confidence (0.65 for "trained signal") and Final Verdict amendment #2 softening (both agree XML is disambiguation scaffold, not trained prior)
- No contradictions between Weakness 3 Format Tax finding and Pillar 1's reliance on Anthropic guidance (Format Tax weakens *urgency* but XML disambiguation on long-context inputs is a separate mechanism)

### Factual consistency — **PASS**

All three cross-section number sets verified to match:

- **arXiv 2601.12014 numbers (38.9 / 30.9 / 42.2)**: 4 occurrences, all consistent
  - Part B Independent counter-benchmark sub-section (line 96, 101)
  - Final Verdict amendment #1 (line 365)
  - Sources consulted (line 485)

- **Composition numbers (25.4 / 47.7 / 6.2 / 4.9)**: 6 occurrences, all consistent
  - Part D Weakness 1 composition table (lines 145-148)
  - Part D Weakness 1 Net line (line 160)
  - Sources consulted (line 491)

- **tiktoken numbers (350 / 308 / 316 / 233)**: 5 occurrences, all consistent
  - Part E side-by-side measurements table (lines 259-262)
  - Sources consulted (line 490)

---

## Unresolved issues / deferred decisions

None. All 15 planned changes applied without escalation. The three unresolved items tracked in the merged document (INV-1 tokenizer re-measurement, INV-3 consumer DAG, INV-5 Haiku A/B test) are **recommendations for post-merge work**, not deferred merge decisions — they are explicitly carried forward as Part H caveats per the checkpoint-2 "Accept with caveats" disposition, which was the intended outcome.

---

## Ready for return contract assembly

**Yes.**

- Merged artifact: `/config/workspace/IronClaude/claudedocs/adversarial-roadmap-formats-20260415/research_roadmap-format-alternatives_VALIDATED.md`
- Merge log: `/config/workspace/IronClaude/claudedocs/adversarial-roadmap-formats-20260415/adversarial/merge-log.md`
- Total word count: 7,937
- All 15 planned changes applied
- All four validation checks PASS
