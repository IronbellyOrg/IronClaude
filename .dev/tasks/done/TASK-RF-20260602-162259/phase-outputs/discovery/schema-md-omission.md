# Schema MD-Omission Inventory (Step 2.1)

**Captured:** 2026-06-02 17:53 (current tree, branch `refactor/roadmap-pipeline-r0-r1-rewrite`)
**JSON key location (all four):** `properties.roadmap_ids.items.pattern`
**Runtime loader:** `superclaude.cli.roadmap.tool_writer.load_schema`

## Verbatim patterns + MD-arm + M1-D01 match

| Schema | Resolved file path | Pattern line | Current `roadmap_ids.items.pattern` (verbatim) | Contains MD arm `M\d+-D-?\d+`? | `re.match(pattern, "M1-D01")` |
|--------|--------------------|--------------|-----------------------------------------------|-------------------------------|-------------------------------|
| extract | `src/superclaude/cli/roadmap/templates/tool_schemas/extract.schema.json` | 134 | `^(FR-\d+(?:\.\d+)?\|NFR-\d+(?:\.\d+)?\|SC-\d+\|G-\d+\|D-?\d+\|COMP-\w+\|DM-\w+)$` | NO | False |
| extract_tdd | `src/superclaude/cli/roadmap/templates/tool_schemas/extract_tdd.schema.json` | 218 | `^(FR-\d+(?:\.\d+)?\|NFR-\d+(?:\.\d+)?\|SC-\d+\|G-\d+\|D-?\d+\|DM-\w+\|API-\w+\|COMP-\w+\|TEST-\w+\|MIG-\w+\|OPS-\w+)$` | NO | False |
| generate | `src/superclaude/cli/roadmap/templates/tool_schemas/generate.schema.json` | 140 | `^(FR-\d+(?:\.\d+)?\|NFR-\d+(?:\.\d+)?\|SC-\d+\|G-\d+\|D-?\d+\|DM-\w+\|API-\w+\|COMP-\w+\|TEST-\w+\|MIG-\w+\|OPS-\w+\|OQ-\w+)$` | NO | False |
| merge | `src/superclaude/cli/roadmap/templates/tool_schemas/merge.schema.json` | 156 | `^(FR-\d+(?:\.\d+)?\|NFR-\d+(?:\.\d+)?\|SC-\d+\|G-\d+\|D-?\d+\|DM-\w+\|API-\w+\|COMP-\w+\|TEST-\w+\|MIG-\w+\|OPS-\w+\|OQ-\w+)$` | NO | False |

> Note: the table renders `\\d` (JSON double-backslash) as `\d` (regex single-backslash). The on-disk JSON uses double-backslash escaping (`\\d`, `\\w`, `\\.`).

## Probe output (literal)

```
extract False
extract_tdd False
generate False
merge False
```

Command: `uv run python -c "import re;from superclaude.cli.roadmap.tool_writer import load_schema;[print(n, bool(re.match(load_schema(n+'.schema.json')['properties']['roadmap_ids']['items']['pattern'],'M1-D01'))) for n in ['extract','extract_tdd','generate','merge']]"`

## Findings

- **Drift CONFIRMED on current tree.** All four schemas omit the MD arm; all four reject `M1-D01`. No schema has been partially fixed.
- **Ordering anomaly CONFIRMED** in `extract`: it lists `COMP-\w+` BEFORE `DM-\w+`, opposite to the canonical DM-before-COMP order used by extract_tdd/generate/merge. Phase 4 regeneration corrects this to DM-before-COMP.
- **merge ≡ generate CONFIRMED**: byte-identical patterns today (both carry the OQ arm). The invariant must be preserved post-regeneration.
- Pattern lines match the research-recorded historical lines (extract:134, extract_tdd:218, generate:140, merge:156) — no drift in line numbers on this read.
