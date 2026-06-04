---
fixture: cross_refs_resolve_stub_case
failure_class: fragility_stub
contract: 5
master_recurrence_row: 8
---

# Recurrence #8 — `_cross_refs_resolve` Always-True Fragility Stub

> **Documented incident** (master:§Recurrence Matrix row #8):
> *"`_cross_refs_resolve` / cross-reference gate always-True stub."*
> Partition findings: `A9:F-A9-005`, `A11:F-A11-031`, `A4:F-A4-010`.

## What happened

The merge step's `_cross_refs_resolve()` cross-reference check **always returned
True** with a fragility comment, shipping a non-enforcing gate to production.
Verbatim (`A9:F-A9-005`, quoted in master:§merge hot spot):

> `_cross_refs_resolve()` "always returns True; the cross-reference check is
> non-enforcing — `# Don't fail on this — it's too fragile for now`"

First seen at A9 (v2.20 "too fragile for now"); still BACKLOG at A11 (C-108).
The stub is the canonical "silent skip on uncertainty institutionalised as
design" shape: rather than implement the check fail-closed, the author wired it
to pass unconditionally and annotated the reason in a comment.

## The anti-pattern (pre-fix)

```python
def _cross_refs_resolve(content: str) -> bool:
    # ... cross-reference validation deemed hard to get right ...
    return True  # Don't fail on this — it's too fragile for now
```

## The invariant (post-fix — Contract #5)

R1.6 **deleted** the `_cross_refs_resolve` stub from `roadmap/gates.py` and audited
every other `return True` site in `src/superclaude/cli`, confirming the rest are
legitimate early-exit heuristics. The Contract #5 CI lint
(`tests/roadmap/test_no_fragility_stubs.py`) walks the entire
`src/superclaude/cli` tree and asserts ZERO `return True` statements carrying a
fragility marker (`fragile` / `too hard` / `for now`) in an immediately-following
`#` comment or `"""` note.

**This fixture's test feeds the pre-fix snippet (the fenced block above) to the
Contract #5 regex `_FRAGILITY_STUB_RE` and asserts it MATCHES (the stub would have
been flagged), then asserts the live `src/superclaude/cli` tree contains ZERO
fragility stubs (the stub was deleted in R1.6).** See `.expected.json` for the
verified values.
