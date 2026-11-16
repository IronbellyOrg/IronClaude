# V1 — Round 2 rebuttal

SW, RL and MR are the absolute roots defined in `work/evidence-pack.md`.

## 1. What changed

**PASS retained, reasoning tightened.** CORR-2 establishes no-source documents as a designed case, not merely a hypothetical omission. My Round 1 defense overstressed absence of measured harm: a demonstrated requirement contradiction could block without model runs. Here the applicability/reporting gap warrants a note, but the lead-in neither demands C2 findings nor changes scoring.

## 2. Claims rejected

- V3 says the time-boundary ambiguity cannot affect D7 because time is not an input. Wrong inference: reallocating a fixed clock can change discoveries, which change found fraction (`analysis/analyze.py`, `found_fraction`, `gate_d7`).
- V2's guessed 0.01–0.02 effect and claim that it is below resolution have no supporting calculation. Neither establishes harmlessness. Any shift can flip a sufficiently close D7 result; the conditional 0.08 bound concerns K's total gain, not the wording shift required (MR 5.7).
- V3's card-edit remedy does not itself implement conditional applicability: `k_paragraph` always prints every definition (`scaffold/briefs.py`). V2's ninth-card scenario is caught immediately by `tests/test_briefs.py`'s eight-card assertion, as CORR-1 states.

## 3. Route rulings

- **R-A — NOTE.** Strongest YES: deliberately softening K would inflate SS−K and could decide adoption without any minimum effect size. But “to look for” already instructs inspection; an imperative's superiority, and thus the alleged directional bias, remains conditional rather than established. With D2 passing, D7 failure requires K−Z0 > SS−Z0−0.04 ≥ 0.08. If MR 120's adjacent human evidence transfers and K−Z0≈0, D7 rarely binds; K still measures this paragraph's prompting share (REQ-40), not an optimal checklist's potential.
- **R-B — NOT BLOCKING.** “Apply each one” alone does not create SS's document-specific coverage units: MR 36 also requires enumerated locations, class-keyed questions and written ledger answers. It remains a plausible plain-checklist wording, not necessarily SS-lite; equally, MR 1035 requires naming checks, not that imperative. The draft is within that definition.
- **R-C — NOTE.** DESIGN 4.6/10 explicitly makes C2 inapplicable without a source. Searching `analysis/analyze.py` found neither `no_source` nor “not applicable”: `found_fraction` uses covered IDs/total; `class_reach` tallies supplied item-class mappings without applicability filtering. If C2 is absent there, no C2 trials appear; if incorrectly present, figures can be wrong. Neither input condition is verified. K could waste time seeking an unnamed source or invent a finding; neither follows necessarily from its generic definition. A reporting implementation gap is not repaired by approving or rejecting this lead-in.
- **R-D — NOTE.** An integrated-review reading may concentrate K on checklist classes; a CB-5-separated reading preserves independent inspection time. Either could improve coverage or displace other findings. Model-specific likelihoods and net directions are UNVERIFIED. Removing “in your own review” can clarify the boundary without editing verbatim CB-5, but does not prove better behavior.
- **R-E — NOT BLOCKING.** Approval concerns line 2 only, not unfinished definitions. Record owner confirmation and exact approved revision in SW's `results/owner-decisions.md`, remove its open item, and carry the decision into `config/owner-values.json` at IMPLEMENTATION 14.3. AO-5/REQ-33 still require the later freeze/tag before hold-out authorship. The test-pinned, unsent draft comment is bookkeeping, not unmet reviewer requirements.
- **R-F — NOT BLOCKING.** A FAIL could identify a local replacement, but cannot complete RL synchronization within scope. RL DR-12/16 and debate 2 section 3 require matching controls for pooling; divergence forfeits that premise. Coordination cost is not evidence that a defective default passes.
- **R-G — NOTE.** Eight is currently correct and test-enforced; DESIGN 13.2 incompletely describes extension work. Last-position emphasis differs from SS's item directive, but required arm structures differ already; no demonstrated invalidating effect.

## 4. Final

**Blocking: NO. BD: none.** Retain N-1 attention/wording uncertainty; N-2 package-only causal interpretation; N-3 stale draft label. Add N-4 no-source applicability/reporting gap and N-5 extension documentation incompleteness. Approval is not proof of harmless wording or approval of the eventual definitions.
