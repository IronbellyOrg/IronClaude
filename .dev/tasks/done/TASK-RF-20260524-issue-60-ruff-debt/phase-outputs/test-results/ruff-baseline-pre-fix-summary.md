# Ruff Pre-Fix Baseline Summary

**Timestamp:** 2026-05-25 03:10
**Command:** `uv run ruff check . --output-format=concise`
**Branch:** `fix/issue-60-ruff-debt` (off latest master)

## Total Error Count

**441 errors** (close match to predicted ~442; difference is 1 error count drift since task creation).

`Found 441 errors.`
`[*] 171 fixable with the --fix option (110 hidden fixes can be enabled with the --unsafe-fixes option).`

## Per-Rule Breakdown

| Rule | Count | Description |
|------|-------|-------------|
| TID252 | 101 | Relative imports (banned by flake8-tidy-imports) |
| I001 | 93 | Import block unsorted/unformatted |
| N802 | 81 | Function name should be lowercase |
| F401 | 49 | Imported but unused |
| E402 | 38 | Module-level import not at top |
| F541 | 29 | f-string without placeholders |
| F821 | 18 | Undefined name (REAL BUGS — never noqa) |
| N801 | 9 | Class name should use CapWords |
| F841 | 6 | Local variable assigned but never used |
| FR-G1 | 5 | Custom: `anthropic` banned-api (must preserve byte-identical) |
| N999 | 4 | Invalid module name |
| E741 | 3 | Ambiguous variable name |
| E731 | 3 | Lambda assigned to name |
| N806 | 2 | Variable in function should be lowercase |
| **TOTAL** | **441** | |

## Per-Directory Breakdown

| Directory | Count |
|-----------|-------|
| `.dev/releases/` | 182 |
| `src/superclaude/` | 125 |
| `tests/cli/` | 60 |
| `.dev/eval-workspaces/` | 29 |
| `tests/audit/` | 13 |
| `tests/sprint/` | 11 |
| `scripts/` | 5 |
| `tests/pipeline/` | 7 |
| `tests/roadmap/` | 3 |
| `.dev/research/` | 3 |
| `tests/cli_portify/` | 1 |
| **TOTAL** | **441** |

## .dev/ Subtotal (will drop after exclusion)

182 + 29 + 3 = **214 errors** removable via `.dev/` extend-exclude in Phase 2.
Post-exclusion expected count: **441 - 214 = 227 errors**.

## FR-G1 Investigation

5 `FR-G1` entries are the `flake8-tidy-imports.banned-api` rule banning `anthropic` imports. These appear as **errors** in the count but the BAN is the intended behavior — the imports themselves are flagged by the custom rule. If these are in production code, they may be legitimate violations that need to be removed; if they're in test fixtures meant to demonstrate the ban, they may need `# noqa: FR-G1` allowing-the-test. Will investigate in Phase 4 or Phase 6.

## Raw Output

See `ruff-baseline-pre-fix.txt` for the complete capture.
