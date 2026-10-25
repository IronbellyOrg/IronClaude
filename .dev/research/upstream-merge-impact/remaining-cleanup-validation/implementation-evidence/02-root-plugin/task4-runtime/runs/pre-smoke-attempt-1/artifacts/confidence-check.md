# sc:confidence-check (lightweight form) — Wave 5 chat recommendations
Scope: R-01..R-05 are plan-text edits to proposed.md; no code implementation.
- File/line targets (proposed.md:4/:7/:9/:10, spec.md:9): verified by Read + evidence-validator.
- R-02 verifier `grep -n 'Hello, Ada!' proposed.md`: run now, exit 1 (no hit) — expected, the gap is open.
- R-03 `pytest.raises(ValueError)`: [UNVERIFIED] framework — neither spec.md nor proposed.md names a test framework (grep pytest|unittest: no hits). Reworded as conditional ("or the chosen framework's equivalent").
- Checks 3/4 (official docs, OSS references): not performed (--no-mcp, no external lookup); not load-bearing for plan-text wording.
Result: recommendations shippable with the [UNVERIFIED] framework marker; blocked_by_low_confidence: false.
