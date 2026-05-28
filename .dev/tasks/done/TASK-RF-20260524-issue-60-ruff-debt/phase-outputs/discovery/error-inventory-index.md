# Per-Rule Error Inventory Index

**Generated:** 2026-05-25 03:14
**Source:** `uv run ruff check . --output-format=concise` baseline

| Rule | Count | Inventory File | Description | Expected Fix Approach |
|------|-------|----------------|-------------|----------------------|
| TID252 | 101 | `errors-TID252.txt` | Relative imports prohibited | **Manual** — convert `from .x` → `from superclaude.pkg.x` (Phase 7) |
| I001 | 93 | `errors-I001.txt` | Import block unsorted/unformatted | **Auto-fix** via `ruff --fix` (Phase 3) |
| N802 | 81 | `errors-N802.txt` | Function name should be lowercase | **Per-instance** — noqa for test-method/external-API; rename in src/ (Phase 5) |
| F401 | 49 | `errors-F401.txt` | Imported but unused | **Auto-fix** via `ruff --fix`, then audit for side-effects (Phase 3) |
| E402 | 38 | `errors-E402.txt` | Module-level import not at top | **Per-instance** — move pytestmark, noqa for sys.path/conditional (Phase 4) |
| F541 | 29 | `errors-F541.txt` | f-string without placeholders | **Auto-fix** via `ruff --fix` (Phase 3) |
| F821 | 18 | `errors-F821.txt` | Undefined name (REAL BUGS) | **Per-instance investigation** — never blanket noqa (Phase 6) |
| N801 | 9 | `errors-N801.txt` | Class name should use CapWords | **Per-instance** — noqa for INV/PR/FR-CONV encoders; rename accidentals (Phase 5) |
| F841 | 6 | `errors-F841.txt` | Local variable assigned but never used | **Per-instance** — delete/rename-underscore/strip-assignment (Phase 4) |
| FR-G1 | 5 | `errors-FR-G1.txt` | `anthropic` banned-api (custom rule) | **Investigation** — confirm legitimate violations vs test fixtures (Phase 6 follow-up) |
| N999 | 4 | `errors-N999.txt` | Invalid module name | **File-level noqa** — encode FR/INV/PR identifiers (Phase 5) |
| E741 | 3 | `errors-E741.txt` | Ambiguous variable name (l/I/O) | **Rename in scope** (Phase 4) |
| E731 | 3 | `errors-E731.txt` | Lambda assigned to name | **Rewrite as def** (Phase 4) |
| N806 | 2 | `errors-N806.txt` | Variable should be lowercase | **Rename or noqa for math conventions** (Phase 4) |
| **TOTAL** | **441** | | | |

## Note: FR-G1 (anthropic banned-api)

5 violations appearing in baseline. Per Objective 5, FR-G1 rules must be preserved byte-identical. The errors themselves indicate code that legitimately imports `anthropic` and gets flagged. These must be investigated:
- If they're in production code that shouldn't import anthropic → fix the imports
- If they're test fixtures demonstrating the ban behavior → add `# noqa: FR-G1  # intentional: test fixture for banned-api ruleset` 
- If they're in `.dev/` → will be auto-excluded in Phase 2

Will revisit after Phase 2 to determine if any FR-G1 remain post-exclusion.
