# Restriction #2 — Pure-function contract on `_canonicalize_requirement_id`

**Verdict:** **PASS**

## Function signature

```python
def _canonicalize_requirement_id(family: str, raw: str) -> str:
```

Location: `src/superclaude/cli/roadmap/structural_checkers.py:295`

## Pure-function criteria

| # | Criterion | Result |
|---|---|---|
| a | Signature is exactly `(family: str, raw: str) -> str` | ✅ YES |
| b | Function body contains no I/O calls (no `open()`, `print()`, `sys.stdout`, `requests`, `Path.read_*`, etc.) | ✅ YES — body only uses `re.match`, `re.compile`-equivalent inline pattern, and f-string formatting |
| c | Function body modifies no module-level state (no global assignment, no class-attribute mutation) | ✅ YES — no `global`, no class scope, no module dict mutation |
| d | Function body has no closures over mutable state from enclosing scope | ✅ YES — only references the local `match`, `prefix`, `_input_sep`, `num`, `rest`, `sep`, `family`, `raw` |
| e | Function is deterministic — identical inputs → identical output | ✅ YES — regex match + string format is deterministic |
| f | Function is idempotent — `f(family, f(family, raw)) == f(family, raw)` | ✅ YES — confirmed by inspection (canonical outputs match the regex idempotently) AND by the test `test_phantom_id_idempotent_on_unpadded` which exercises the property end-to-end |

## Notes

- The `family` parameter is declared (per the locked signature from research/03-refactor-plan-concrete-changes.md Change 1) but the body re-derives the prefix from `raw` itself via regex. This is consistent with the signature contract — the function still returns a deterministic, idempotent canonical string for any `(family, raw)` input pair. No purity violation.
- The lazy `import re` at line 323 follows the file's existing convention (cf. lines 527, 575, 679, 767 of the pre-existing code).

## Verdict: PASS — all 6 criteria satisfied.
