# Tasklist (fixture) — serena-type-hierarchy (FR-1)

# Drives the type_hierarchy variants. OO-codebase fixture has a BaseAgent with subtypes;
# the tasklist claims only some subtypes are registered.
- Task 1: hierarchy-capable backend + --with-hierarchy → step 4.5 runs; subtype coverage computed
- Task 2: LSP-disabled variant — backend lsp, no generic type_hierarchy → skip, NO degrade
- Task 3: explicit backend-error variant → degraded:["type_hierarchy:backend_error"] + fallback
- Task 4: Wave 1B.3 shared BaseAgent hotspot → HIGH edge only after lineage confirmed
