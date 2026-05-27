# structural_checkers.py — Current Line Map

Captured: 2026-05-27 06:25 UTC
File: `/config/workspace/IronClaude/src/superclaude/cli/roadmap/structural_checkers.py`
Total LOC: **988**

## Key sections (current actual lines)

| Section / Symbol | Research cite | Actual line range |
|---|---|---|
| `SEVERITY_RULES` (start → end) | 42-67 | **31 → 56** |
| `("signatures", "phantom_id"): "HIGH"` entry | — | **33** |
| `get_severity` helper | — | 59-65 |
| `FIX_GUIDANCE_TEMPLATES` (start → end) | 155-176 | **98 → 177** |
| `"phantom_id"` template entry | — | **115-118** |
| `_make_finding` helper | ~260 | **255-286** |
| `check_signatures` function start | — | **355** |
| `phantom_id` block in `check_signatures` | 372-391 | **371-391** |
| Raw set-difference comparator | 380 | **380** (`phantom_ids = roadmap_ids - spec_ids`) |

## Notes

- `requirement_ids` is keyed by family: `dict[str, set[str]]`. The current `check_signatures` flattens all families into one `spec_ids`/`roadmap_ids` set, losing the family context needed for canonicalization. The fix must iterate families on both sides and call `_canonicalize_requirement_id(family, raw)` per ID.
- `_make_finding` accepts `severity_override: str | None = None`, which is the hook the new MEDIUM `id_schema_drift` emission will use (`severity_override="MEDIUM"`).
- Insertion point for `_canonicalize_requirement_id`: immediately after `_make_finding` (after line 286, before line 289 `# ---------- S5: Context-Aware NFR Severity ----------`).
- Line drift from research: `SEVERITY_RULES` shifted from cited 42-67 to actual 31-56 (-11 lines); `FIX_GUIDANCE_TEMPLATES` shifted from cited 155-176 to actual 98-177 (-57 lines start, +1 line end); `phantom_id` block shifted from cited 372-391 to actual 371-391 (-1 line start). All Phase 2-3 line references must use these actual lines.
