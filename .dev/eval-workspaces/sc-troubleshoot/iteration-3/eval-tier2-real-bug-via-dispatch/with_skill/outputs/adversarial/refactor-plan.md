# Refactor Plan (folded into FIX-A merged output)

FIX-A is a one-line removal; no refactor needed. The merged output retains:

1. The single-line change at `commands.py:1476`.
2. The regression test from FIX-A test plan.
3. The cross-module parity test from quality-engineer's card.
4. A docstring note on `resolve_scratch_root`'s `output_dir` kwarg recommending against passing the candidate-being-validated — adopted from FIX-B's spirit without breaking the API.

**Deferred to follow-up task** (not part of this merged fix):
- Full FIX-B (kwarg removal) with deprecation cycle.
- Wider audit of every `resolve_scratch_root` call site for misuse patterns.
