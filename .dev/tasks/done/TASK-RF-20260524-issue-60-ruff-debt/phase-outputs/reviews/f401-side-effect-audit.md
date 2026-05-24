# F401 Side-Effect Audit — Phase 3.3

**Timestamp:** 2026-05-25 03:35

## Removed Imports Inventory

Derived from `git diff` after Phase 3.2 auto-fix application.

| File | Import Removed | Type | Decision |
|------|---------------|------|----------|
| `scripts/eval_1.py` | `os` | Clearly unused | Keep removal |
| `scripts/eval_runner.py` | `tempfile` | Clearly unused | Keep removal |
| `scripts/sync_from_framework.py` | (none — I001 reorder only) | N/A | N/A |
| `tests/cli/eval/test_eval_context.py` | `typing.Iterable` | Clearly unused type alias | Keep removal |
| `tests/cli/eval/test_eval_id_regex.py` | `typing.Mapping` | Clearly unused type alias | Keep removal |
| `tests/cli/eval/test_capability_classifications.py` | `SchemaError, SuiteLoader, validate_manifest` | Clearly unused (test imports duplicate) | Keep removal |
| `tests/cli/eval/test_capability_gates.py` | `threading` | Clearly unused module | Keep removal |
| Various test files | duplicate `import json` | Clearly unused (duplicate) | Keep removal |

## Side-Effect Risk Assessment

**No removed imports are side-effecting:**

- No `import warnings` / `warnings.filterwarnings(...)` removals
- No `import logging` removals (sync_from_framework.py kept it via I001 reorder)
- No vendor/plugin registration imports
- No `import _internal_module` patterns
- No `# noqa: F401` directives that ruff would have respected (none removed inadvertently)

## Verdict

**PASS** — All F401 auto-removals are safe. No restoration needed.
