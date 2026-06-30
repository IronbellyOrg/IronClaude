
## Generator-Constraint Considered

This PR touches validator/gate surfaces (`structural_checkers.py`, and — via the brittleness follow-ups — the roadmap generate/merge tool-write path), so per BUILD-REQUEST §Contract #3 the generator-side constraint was explicitly considered:

- **Area B is itself a generator-constraint hardening.** Generation-time phantom-ID *prevention* now sources the spec-ID universe from the always-written `spec_id_registry.json` (via `SpecIdRegistry.from_payload().union_of_known()`) and **fails shut** when the registry is missing/malformed, with `require_spec_ids=True` on the tool-write renderer. The generate/merge steps therefore cannot *emit* an out-of-spec `roadmap_id` at generation time — the generator-side half of Contract #3 — complementing (not replacing) the MERGE_GATE Contract #9 catch (defense-in-depth).
- **The merge-gate catch is preserved.** `gates.py` (`_roadmap_ids_within_spec`), `convergence.py`, and `semantic_layer.py` are **byte-unchanged**; the new generation-time check *fronts* the existing gate rather than weakening it.
- **`structural_checkers.py` change is comment-only.** At the master merge its executable code was byte-identical across both branches' PR #111 MD-family ports; only provenance comments were reconciled. `spec_parser.py` adopts master's PR #111 **span-aware** bare-D dedup (the authoritative generator-side ID-canonicalization constraint); the Contract #9 containment invariant is preserved and re-verified by the recurrence corpus.

No generator-side constraint was loosened; the net effect is a stronger generator-side phantom-ID guarantee plus preserved gate semantics.
