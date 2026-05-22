# Fix-2 — Fix-1 PLUS defensive guard inside `resolve_scratch_root`

**Author**: root-cause-analyst
**Surface area**: 1 call site + 1 helper change + 1 special-case for `containment_guard`

## Problem statement

Same as Fix-1. Additional concern: even after fixing the call site, the `resolve_scratch_root` API still accepts the tautology pattern silently. A future caller can re-introduce the same bug. Defense at the API boundary closes the entire class.

## Proposed change

1. Same call-site change as Fix-1.
2. In `src/superclaude/cli/eval/config.py`, modify `resolve_scratch_root` (snapshot lines 217-238). After computing `resolved`, before returning, check that the resolved candidate is not equal to the resolved `output_dir=` extension:

```python
candidate = Path(path)
resolved = candidate.expanduser().resolve(strict=False)

if output_dir is not None:
    resolved_extension = _resolve_prefix(Path(output_dir))
    if resolved == resolved_extension:
        # Anti-tautology guard: refuse to validate a path against
        # itself via the output_dir= kwarg.
        raise ScratchRootViolation(candidate, resolved, allowed)
```

3. `containment_guard` (`isolation.py:307-318`) currently calls `resolve_scratch_root(scratch_root, config=config)` — no `output_dir=` kwarg — so it is unaffected. But if any future re-check legitimately needs to allow tautology, it must explicitly opt in (e.g. `allow_same_path=True`).

## Evidence

- Same as Fix-1.
- Snapshot `config.py:237-238` — the extension step has no anti-tautology check.

## Risks

- API surface change: any caller currently relying on `resolve_scratch_root(p, output_dir=p)` semantics will break. Live grep shows no such caller, but a careful audit is required before merge.
- The opt-in special case adds API complexity.

## Test plan

- All Fix-1 tests.
- Unit: `test_resolve_scratch_root_rejects_same_path_tautology` asserts the new exception.

## Rollback

Revert the helper change; the call-site fix from Fix-1 still stands. Two commits, easy partial revert.
