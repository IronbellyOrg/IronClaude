# E2 prefilter revision (written BEFORE the Stage 0 rerun; a priori, not fitted to case outcomes)

Trigger: Stage 0 gave GO-REPLAY (H=3) with candidate-pool misses 11 > 2, so the pre-registered rule requires raising pool_cap or extending the prefilter and rerunning Stage 0 (labels unchanged).

Chosen extension (exactly ONE): **small-document rare-word rule.** When a document has at most `small_doc_max_passages = 40` eligible passages, one shared rare content word admits a pair (`small_doc_min_shared_rare_words = 1`); larger documents keep the two-word rule.

Design reason: the "2 shared rare words" requirement exists to limit chance matches in large documents (hundreds of passages, where a single shared word is weak evidence). In a mini-spec of 25-30 passages a word shared by only two passages (the rare definition is document frequency exactly 2 when n is small) is already a strong and cheap-to-check link, and requiring two such words discards novel-defect pairs that are linked by one distinctive term. The rule is size-conditioned, uses no per-case clause, and the constant 40 is a round number just above the largest mini-spec size in the design (400-1,200 words), chosen from the document-size design, not from case labels.

Not changed: pool_cap (150) and all weights. Candidate pool misses on the large S1-based documents come from cap truncation and absence of lexical links; the plan allows only one lever here and the cap is also the cost lever (replay ceiling 30M tokens / $5), so it is left frozen. If the gate still reports misses > 2 or NO-GO-OFFLINE, that is reported as is.
