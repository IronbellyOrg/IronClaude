# Base Selection — Proposal A vs B

## Combined Scoring

| Dimension (weight) | Proposal A | Proposal B | Evidence |
|---|---|---|---|
| Contract #6 satisfaction (one parser) | 1.0 | 1.0 | Both collapse to one canonical parser |
| §MVR §1 fidelity (substrate inversion, 8-field canon) | 0.95 | 0.55 | B is structurally coupled to the illegal `frontmatter` field (INV-005); A can shed it |
| Blast radius / regression surface (lower=better) | 0.95 | 0.30 | A: 1 module + deletions; B: 8 SemanticCheck modules (63 callsites) + sprint + generic executor reorder |
| Feasibility at gate time | 1.0 | 0.35 | INV-001/002: envelope not at dispatch; B needs generic-pipeline surgery + reorder |
| Tier-model fit (SemanticCheck vs CodeAssertion) | 0.95 | 0.40 | INV-002: CodeAssertion is the sanctioned envelope-aware tier; B duplicates it |
| NFR-007 safety (pipeline ⊥ roadmap import) | 1.0 | 0.55 | B pushes PipelineEnvelope into pipeline/models.py SemanticCheck |
| **Combined** | **≈0.97** | **≈0.45** | |

## Edge-case floor
- A passes (handles the empty/illegal-field boundary by NOT adding the field).
- B fails the boundary it created (the field-add breaks `test_pipeline_envelope.py:312`).

## Selected Base: **Proposal A**, with one mandatory modification

**Modification (from the fault-finder, independently re-verified):** DROP the `frontmatter`-field sub-step. The relocated canonical parser is a FUNCTION in the envelope module; no field is added to the frozen 8-field `PipelineEnvelope`.

### Strengths preserved from A
- One canonical parser function, owned by the envelope/post-extractor module (§MVR §1 "one parser").
- 24 in-gate callsites repointed to it; 5 duplicate parser defs deleted (Contract #6).
- `test_parser_consistency.py` added (determinism of the one parser).
- SemanticCheck/gate dispatch unchanged; sprint + 7 other gate modules untouched.
- Escape hatch: any genuinely cross-step check → `CodeAssertion` (R1.3 tier).

### Strengths incorporated from the fault-finder
- Removal of the contract-violating, consumer-less `frontmatter` field (also corrects task Step 11.2(a)).
