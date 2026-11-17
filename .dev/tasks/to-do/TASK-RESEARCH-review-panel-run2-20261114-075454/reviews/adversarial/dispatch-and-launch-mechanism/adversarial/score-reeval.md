# Position-bias re-evaluation: slot C-07 (dispatch-and-launch-mechanism)

Scope: the 8 criterion-variant pairs on which Pass 1 (input order) and Pass 2 (reverse order) disagreed. Variant 1 = Proposal A (`variant-1-original.md`), Variant 2 = Proposal B (`variant-2-original.md`). Each variant is scored as written. A defect found in the debate and confirmed against the code counts against the variant as written; the hybrid the debate produced later is not credited. Section numbers `sN` are the variant's own H2 sections. Rule applied: MET (1) only with a specific cited evidence, otherwise NOT MET (0). The verdict is final.

Code facts checked in this re-evaluation: `src/superclaude/cli/review/panel.py:137-157` (`_check_reflect_resolution` reads only `r["launch"]`, no `read_only` or `adapter` field exists), `panel.py:360-372` (`launch` must be a dict of str to str: a model id maps to exactly one launcher string). Text checks: grep of `variant-1-original.md` for `family`, `GQ-049`, `swarm`, `r03`, `r06`, `r07` returns 0 hits each; grep of `variant-2-original.md` and `variant-1-original.md` for hedge phrases.

## Result table

| # | Criterion | Variant | Pass 1 | Pass 2 | Final | Deciding evidence |
|---|---|---|---|---|---|---|
| 1 | C1 Covers all explicit requirements from source input | Variant 1 | 0 | 1 | NOT MET (0) | The C-07 row's "Why undecidable" names the family-alias resolution "not verified" and cites GQ-049 and research 04, 03, 06, 07, 13; Variant 1 has no `family`, `GQ-049`, `r03`, `r06` or `r07` anywhere (0 grep hits each). |
| 2 | S3 Clear separation of concerns between sections | Variant 1 | 1 | 0 | NOT MET (0) | s4 "Invariants" carries a five-item "Dependencies on adjudicated slots" block (C-01, C-02, C-03, C-06, C-08), which are not invariants; s3 point 6 puts design rules in the evidence list. Variant 2 gives dependencies their own sections (s8, s9). |
| 3 | L1 Unambiguous language | Variant 1 | 0 | 1 | NOT MET (0) | The ceiling gate is worded two non-equivalent ways: s1 "when the process is mechanically restricted to a read-only tool set" versus s2 "accepts a reviewer whose `launch` is a class word or whose `adapter` is `claude-p`"; no precedence between `launch` and `adapters`; hedges "an extra key should not move parity" (s4) and "a possible source for `requested`" (s4). |
| 4 | L4 Acronyms and domain terms defined on first use | Variant 1 | 1 | 0 | NOT MET (0) | First use of INV-L is s2 ("which respects INV-L") with no gloss; the gloss comes in s4. "the Fable rule and the `classes` rule" (s2), "D3" (s2), "tier-2b" (s3 point 3), "shadow", "Stage 3" and "legacy rotation" are used without definition. |
| 5 | R1 Identifies at least 3 risks with probability and impact assessment | Variant 1 | 1 | 0 | MET (1) | Three risks carry an observed frequency and a stated impact: class-word drift (s3 point 4: `haiku` served `gpt-6.1-sol` in five reviewer calls, `opus` served `gpt-6-luna` in D1-D3 and E1-E3), orchestrator collapse (s3 point 4: run A-r3, three reviewers and three calibrators on one model, contract still `calibrator_diversity: full`), shim swap (s3 point 5: two `b4-muse-luna2` runs served by `terra`); s4 adds four rated items (INV-G HIGH; INV-K, INV-E, INV-L MEDIUM). |
| 6 | K4 No internal contradictions | Variant 2 | 1 | 0 | MET (1) | No two statements in the text assert opposite things; `diff-analysis.md` lists intra-variant contradictions only for Variant 1 (X-008, X-009); `quant-score-output.json` IC for Variant 2 is 0 over 28 tagged claims. The Pass 2 items are feasibility defects (K2), not contradictions. |
| 7 | L4 Acronyms and domain terms defined on first use | Variant 2 | 1 | 0 | NOT MET (0) | The header (line 5) uses INV-G, INV-L, INV-F and C-S6, CO-10, FX-13 before any gloss; the glosses sit later in the s4 table, and s4 also says "Definitions are those of synth-06 6.12.0" (an external pointer). "sidechain" and "shim" are used without definition. |
| 8 | R3 Addresses failure modes and recovery procedures | Variant 2 | 1 | 0 | MET (1) | s5 item 6 "Fall-back trigger for the position itself": trigger (more than three reviewers or four distinct served models needed, or a workspace cannot export the class map before the session starts), action (raw-id reach for that panel), owner (the engine, not the core); plus s2 "a missing argument is a dispatch error, not a fallback" and s4 INV-I "recorded, not blocked". |

## Standard applied to L4 (pairs 4 and 7, one standard for both variants)

A term is "defined on first use" when its first occurrence in the document carries an inline gloss, an appositive description, or a legend entry that precedes or sits at that occurrence. A definition that comes later, or a pointer to a document outside the variant, does not count. A bare identifier used only as a citation pointer and followed by a source locator (for example `FX-8, s06:103`) is exempt. A term the argument depends on is not exempt. Under this standard a single load-bearing term used undefined at first occurrence makes the criterion NOT MET for either variant.

## CEV per pair

### 1. C1, Variant 1 (Pass 1: 0, Pass 2: 1) -> NOT MET

CLAIM: "Covers all explicit requirements from source input" is not met in Variant 1.
EVIDENCE: The C-07 row (`phase-outputs/discovery/undecidable-conflicts.md`, line 24) gives, under "Why undecidable": Claude Code behaviours not pinned (Agent enum, `resolvedModel`, "family-alias resolution 'not verified'"), no cost or quality comparison, E2 sessions leave Bash open; and names research 04, 03, 06, 07, 13 and GQ-049. Variant 1 covers the Agent enum (s3 point 3), `resolvedModel` (s7), cost (s5, M-4) and Bash open (s3 point 6b). It does not mention the family-alias clause (0 grep hits for `family`), does not cite GQ-049 (0 hits), and cites none of research 03, 06, 07 (0 hits each; only r04 and r13 appear). Variant 2 covers these (s9 "family-alias edge case ... (GQ-049, r04 gap 3)"). Pass 2 checked the sections that exist and did not test the explicit row elements.
VERDICT: NOT MET. The criterion says "all"; at least three explicit elements of the row are absent.

### 2. S3, Variant 1 (Pass 1: 1, Pass 2: 0) -> NOT MET

CLAIM: "Clear separation of concerns between sections" is not met in Variant 1.
EVIDENCE: s4 is titled "Invariants" and holds three blocks: "Preserved", "Endangered", and "Dependencies on adjudicated slots, stated exactly" (C-01, C-02, C-03, C-06, C-08). The last block is a different concern (cross-slot dependencies and interface constraints, for example C-06 "a bounded re-ask ... needs a persisted session") under a heading that names invariants. The blocks are plain-text labels, not headings. s3 point 6 ("Two defects in that script the proposal must not inherit") puts design instructions into the evidence list. Pass 1 itself records "The mix inside s4" and rates it Low (`diff:S-002`). Variant 2 puts the same material in s8 (consistency with C-01 to C-03) and s9 (open facts), separate from its s4.
VERDICT: NOT MET. A second substantial concern with its own subject sits inside a section whose heading names another.

### 3. L1, Variant 1 (Pass 1: 0, Pass 2: 1) -> NOT MET

CLAIM: "Unambiguous language" is not met in Variant 1.
EVIDENCE: The rule that defines the position is stated two non-equivalent ways. s1: the ceiling widens "to the `claude-p` adapter when the process is mechanically restricted to a read-only tool set". s2: `_check_reflect_resolution` "accepts a reviewer whose `launch` is a class word or whose `adapter` is `claude-p`". Code check: `panel.py:153-156` reads only `launch`, and no `read_only` field exists, so the s2 wording admits an unrestricted `claude-p` reviewer, which s1 does not (`diff:X-009`). s2 also adds an `adapters` map beside `launch` and states no precedence when a model has both (`debate:R2/advocate-A` B-W4). Hedges: s4 "so an extra key should not move parity", s4 "are a possible source for `requested`". Pass 2 cited firm sentences from s2 and s4 but did not weigh the two-way gate.
VERDICT: NOT MET. The central gate is ambiguous as written.

### 4. L4, Variant 1 (Pass 1: 1, Pass 2: 0) -> NOT MET

CLAIM: "Acronyms and domain terms defined on first use" is not met in Variant 1 under the standard above.
EVIDENCE: Defined at first use: INV-G (s1 gloss "mechanically read-only reviewers"), the two adapters (s1 inline), "E1 path" and "E2's path" (s1 appositives that name the path), D4 (s2 "sends a cell with a null `launch` to the legacy rotation"), INV-A, INV-B, INV-F, INV-I (glossed at their s4 first use). Not defined at first use: INV-L first appears in s2 ("which respects INV-L") with its gloss only in s4; "the Fable rule and the `classes` rule" (s2), "D3 says that ships in Stage 3" (s2), "tier-2b, tier-3 and tier-4" (s3 point 3), "shadow" and "legacy rotation" (s2) have no definition anywhere in the variant.
VERDICT: NOT MET. Most terms are glossed, but load-bearing ones (INV-L, the ceiling rules, the tier names) are not.

### 5. R1, Variant 1 (Pass 1: 1, Pass 2: 0) -> MET

CLAIM: "Identifies at least 3 risks with probability and impact assessment" is met in Variant 1.
EVIDENCE: Risk 1, class-word binding drift: s3 point 4 "the `haiku` class was served `gpt-6.1-sol` in five reviewer calls and the `opus` class served `gpt-6-luna` in D1-D3 and E1-E3" (frequency), impact "A class word is not the model a reader assumes". Risk 2, orchestrator collapse: s3 point 4 "run A-r3 collapsed three reviewers and three calibrators onto `claude-sonnet-5-5` ... its contract still reports `calibrator_diversity: full`" (one run; impact stated). Risk 3, silent swap through the ladder or shim: s3 point 5 "two `b4-muse-luna2` runs served by `terra`" and s3 point 7 (impact: only the identity check catches it). s4 also rates four items for the position's own risks (INV-G HIGH; INV-K, INV-E, INV-L via golden files MEDIUM) with triggers ("They would break if the same value were put in `gateway.launch`"; "[UNVERIFIED which pins compare whole objects]"). Pass 2 discounted points 4 and 5 as harms of the existing path; the criterion does not limit risks to those of the author's own position, and the standard Variant 2's R1 verdict rests on (E11 frequency "1 of 15", E7 "2 runs") is the same kind of evidence.
VERDICT: MET. The likelihood part is weaker for the position's own risks, but three risks have an observed frequency and a stated impact.

### 6. K4, Variant 2 (Pass 1: 1, Pass 2: 0) -> MET

CLAIM: "No internal contradictions" is met in Variant 2.
EVIDENCE: Pass 2 raised two items. (a) s2 prescribes a model-to-class-word map, while E4 reports `haiku` served `claude-haiku-5-5` in D1-D3 and `gpt-6-luna` in E1-E3, and `opus` and `haiku` both served `gpt-6-luna` in E1-E3. Code check: `panel.py:364-368` requires `launch` to be a model id to one string, so environment E cannot be written as a map. Variant 2 never states that the map is complete or one-to-one, and s3.2 says "the same word keeps ... a different model outside a ccsession tier workspace" and s2 says the pairs are those "that the launching environment exports". The text reports data and prescribes a map that cannot hold it; that is a feasibility defect (counted under K2, already NOT MET), not two statements that conflict. (b) s2 "a missing argument is a dispatch error, not a fallback to the agent default" and `model: sonnet` staying in the agent file (s2 row for `reflect-reviewer.md`). The rule governs the orchestrator's call; the file default is the agent definition. E11 is why the rule exists. They do not assert opposite things; that the rule has no enforcer is a sufficiency point (INV-017), not a contradiction. `diff:` records no intra-variant contradiction for Variant 2, and IC is 0 of 28.
VERDICT: MET. Counting a code-confirmed feasibility defect again under K4 would score one defect twice.

### 7. L4, Variant 2 (Pass 1: 1, Pass 2: 0) -> NOT MET

CLAIM: "Acronyms and domain terms defined on first use" is not met in Variant 2 under the standard above.
EVIDENCE: Defined at first use: the class words (s1 inline list), "Dispatch contract" (s2 "the resolution JSON plus one rule"), `live7` (s7 "a seven-reviewer `live7` panel"), the citation forms (line 7 legend). Not defined at first use: the header (line 5) uses "INV-G (HIGH), INV-L (MEDIUM), INV-F (MEDIUM)" before any gloss; the gloss comes in the s4 table, and s4 states "Definitions are those of synth-06 6.12.0", an external pointer that the standard does not accept. "sidechain" (s1, E4) and "shim" (E5, E7) are domain terms the argument turns on and have no definition anywhere in the variant. Same standard and same kind of finding as pair 4.
VERDICT: NOT MET. Same outcome as Variant 1, by the same test.

### 8. R3, Variant 2 (Pass 1: 1, Pass 2: 0) -> MET

CLAIM: "Addresses failure modes and recovery procedures" is met in Variant 2.
EVIDENCE: Failure modes named: orchestrator drops the argument (E11), served model differs from intended (E7, s4 INV-I), shim failover (E5, E7), workspace cannot export the class map (s7 point 6). Recovery: s5 item 6, "Fall-back trigger for the position itself", gives a trigger ("a panel the owner wants needs more than three (reflect) or four (any) distinct served models, or a workspace cannot export the class map before the session starts"), an action ("raw-id reach is needed for that panel") and an owner ("the engine, not the core, under B"). Dispatch-time handling is also stated: "a missing argument is a dispatch error, not a fallback" (s2) and a mismatch "is recorded, not blocked" (s4 INV-I). Pass 2 is right that the runtime handling is detect-or-record rather than re-dispatch; it did not count item 6, which is a concrete route change with a trigger. This is the same kind of design-level fallback that Variant 1's M-2 supplies ("A narrows to `agent-class`").
VERDICT: MET, on item 6. The criterion does not require the recovery to be a runtime retry.

## Subtotal effect (for the merge step)

Pairs flipped to the final value relative to each pass are listed in the count line below. Dimension subtotals after the final verdicts (Pass 1 values in brackets, only dimensions that move are marked): Variant 1 Completeness 4/5, Correctness 1/5, Structure 4/5 [5/5], Clarity 3/5 [4/5], Risk 5/5, Invariant and Edge Case 5/5; Variant 2 Completeness 5/5, Correctness 3/5, Structure 5/5, Clarity 4/5 [5/5], Risk 4/5, Invariant and Edge Case 5/5. Final totals recomputed from Pass 1 with the three changed pairs applied: Variant 1 = 24 - 1 (S3) - 1 (L4) = 22/30; Variant 2 = 27 - 1 (L4) = 26/30. Cross-check against Pass 2 (Variant 1 23/30, Variant 2 24/30): Variant 1 = 23 - 1 (C1) - 1 (L1) + 1 (R1) = 22/30; Variant 2 = 24 + 1 (K4) + 1 (R3) = 26/30. Both routes agree: Variant 1 22/30 (qual_score 0.733), Variant 2 26/30 (qual_score 0.867).

Disagreements re-evaluated: 8; final verdicts changed from Pass 1: 3; from Pass 2: 5
