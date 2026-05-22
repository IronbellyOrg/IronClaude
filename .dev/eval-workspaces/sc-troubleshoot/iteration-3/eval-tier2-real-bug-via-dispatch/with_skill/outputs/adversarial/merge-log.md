# Merge Log

- Base: FIX-A
- Folded in from FIX-B: a docstring warning on the kwarg (non-breaking).
- Folded in from quality-engineer card: parity test (additive).
- Deferred to follow-up: full FIX-B kwarg removal with deprecation cycle.

**Self-review (sanity check on merged output)**:
- Tests? Yes — regression test + parity test specified.
- Edge cases? Considered — symlink resolution unchanged (already handled by `_resolve_prefix`); empty allowlist preserved; downstream `runtime_allowed` extension at commands.py:1490 unaffected.
- Requirements? OPS-002 cross-module consistency restored.
- Follow-up? Captured: FIX-B kwarg-removal refactor; documentation note on kwarg docstring.

**Verdict**: OK. No blockers. Proceed to Wave 5.
