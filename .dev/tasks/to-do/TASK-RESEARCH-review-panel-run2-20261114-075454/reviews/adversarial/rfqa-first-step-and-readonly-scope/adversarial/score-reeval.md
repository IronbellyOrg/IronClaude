# Position-bias re-evaluation: criterion n=16 (Clarity 1), Variant B

Artifact: `variant-2-original.md` (read in full, 120 lines).
Criterion: "Unambiguous language (no 'should consider', 'might', 'as appropriate')". Additive binary; MET only with specific evidence.

## CEV

CLAIM: Variant B is written in unhedged, committed language. The few hedge-class words in the file are inside quotations or inside explicitly tagged open items, and the two passages Pass 2 cites are positions stated as open or deferred with a stated rule, not ambiguous wording.

EVIDENCE:
- Hedge sweep (Grep, case-insensitive, over the variant for `should consider|might|as appropriate|as needed|may |could|perhaps|possibly|probably|likely|if appropriate|where appropriate|ideally|generally|typically|etc`): matches only on lines 29, 53 and 102. Line 29: "may have failed silently" is a verbatim quote of `task/SKILL.md:260`. Line 53: "could be asked" sits in a sentence that ends "I did not test that [UNVERIFIED]", an explicitly tagged open question. Line 102: "could include it" is inside the quoted opposing objection. None of the listed hedges ("should consider", "might", "as appropriate", "as needed") occurs in B's own voice.
- B's own claims use committed verbs: "should not replace ... should enter rf-qa at the document-type level" (B:10), "applies to every reviewer the panel adds" (B:10), "stay byte-identical" (B:10), "B defers it until a consumer needs the core" (B:16), "Disagreement with any of the three outcomes: none" (B:59).
- Pass 2's cite B:10 "for example PRD, TDD, technical reference or README": the set is bounded by a definite rule on the same line, "a document type that rf-qa-qualitative already reviews", with three stated properties (one file, one candidate text, fits C-01 without a new locator). The examples illustrate a defined set; they do not soften it.
- Pass 2's cite B:10 "weaker alternative ... a skill's spawn sites": the alternative is resolved with an explicit rule at B:109: "I keep the spawn-site variant only as a fallback if no document type has a usable seeded-defect set."
- Pass 2's cite B:116: "Which document type is best for the first gate; it is a design detail, not an evidence-backed choice here." This is an explicit, labelled deferral in the "What I did not verify" section, not hedged phrasing.
- Measurement rules are fixed in advance with binary outcomes: "Rule fixed before the audit: zero writes ... supports ...; one write ... shows B-3 wrong" (B:84); "B is shown wrong if ..." (B:86).
- Minor note, not decisive: B:86 "costs about the same to build and gives a stable result" is an approximate threshold in one falsifier; B:10 "about 175 prose lines" is an approximate count with its source named at B:96. Neither is a hedge of the "should consider / might / as appropriate" class.

VERDICT: MET

## Reasoning

Pass 1's evidence checks out: the grep hits are a quote (B:29), a tagged untested question (B:53) and the opponent's quoted objection (B:102), so none is B hedging its own position. Pass 2's evidence is real but measures a different property: whether the position is fully decided. The criterion targets ambiguous wording. B:10's example list is anchored to a defined set, the spawn-site alternative is closed by a stated fallback rule at B:109, and B:116 openly names the document-type choice as deferred. An explicitly stated, rule-bounded open item is the opposite of vague language, so it does not make the wording ambiguous. The only imprecise phrase found ("about the same", B:86) is a single approximate threshold, not a hedge of the listed kind, and does not outweigh the specific evidence of committed language throughout. The criterion is MET.

FINAL: n=16 B MET
Status: Complete
