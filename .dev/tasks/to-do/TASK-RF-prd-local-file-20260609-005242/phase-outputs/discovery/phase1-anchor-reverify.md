# Phase 1 Anchor Re-Verification (drift guard)

All anchors checked against LIVE source via Grep. **Result: every anchor CONFIRMED at its research-cited line — zero drift.**

## process.py (`src/superclaude/cli/prd/process.py`)
| Anchor | Cited | Live | Status |
|--------|-------|------|--------|
| refs `--file` emission `file_args.extend(["--file", str(ref_path)])` | :199 | :199 | CONFIRMED |
| spec `--file` emission `file_args.extend(["--file", spec_path])` | :204 | :204 | CONFIRMED |
| `def _build_file_args(` | :169-170 | :170 | CONFIRMED |
| call `file_args = self._build_file_args(` | :154-155 | :155 | CONFIRMED |
| `extra_args=file_args` kwarg | :166 | :166 | CONFIRMED |
| `_PHASE_ALLOWED_REFS` def | :95 | :95 | CONFIRMED (method-internal use :191) |
| `_FILE_SIZE_THRESHOLD` def | :115 | :115 | CONFIRMED (method-internal use :198) |
| `_SPEC_FILE_STEPS` def | :121 | :121 | CONFIRMED (method-internal use :201, docstring :180) |
| module docstring `--file` | :4, :11 | :4, :11 | CONFIRMED |
| class docstring bullet `Phase-aware --file arg construction (GAP-003)` | :133 | :133 | CONFIRMED |

Note: additional in-method docstring `--file` mentions at :171/:175/:181/:183 and the comment at :94/:119/:154 are removed implicitly when the method/branches/constants are deleted (Steps 2.2–2.6).

## prompts.py (`src/superclaude/cli/prd/prompts.py`)
| Anchor | Cited | Live | Status |
|--------|-------|------|--------|
| `_TRUNCATION_MARKER` | :34 | :34 | CONFIRMED |
| `def _read_file(` | :42 | :42 | CONFIRMED |
| `def _authoritative_specs_block(` | :120 | :120 | CONFIRMED |
| `if not spec_paths:` early return | :130-131 | :130 | CONFIRMED |
| docstring `Phase 1 (paths-only)` | :128 | :128 | CONFIRMED |
| call site scope-discovery | :247 | :247 | CONFIRMED |
| call site investigation | :919 | :919 | CONFIRMED |

**Verdict: no edit item needs line-number adjustment. Proceed to Phase 2 with the cited anchors.**
