# Per-Step Entity-Array → Family-Set Mapping (Step 2.2)

**Captured:** 2026-06-02 17:54 (live schema files, branch `refactor/roadmap-pipeline-r0-r1-rewrite`)
**Verdict source:** `research/02-intentional-vs-drift-investigation.md` (INTENTIONAL per-step)
**Method:** programmatic enumeration of `properties` typed arrays + `milestones[].open_questions[].items` shape via `load_schema`.

## Confirmation matrix

| Step | Entity arrays declared (live) | `open_questions[].id` present? | Expected ENTITY families | Expected FULL roadmap_ids family set (spec MD/FR/NFR/SC/G/D ∪ entity) |
|------|-------------------------------|-------------------------------|--------------------------|------------------------------------------------------------------------|
| extract | `component_inventory` | No (open_questions absent / not id-bearing) | `{COMP, DM}` (DM fixture-backed — see note) | MD,FR,NFR,SC,G,D ∪ {DM, COMP} |
| extract_tdd | `component_inventory, data_models, api_specifications, testing_strategy, migration_plan, operational_readiness` (all 6) | No | `{DM, API, COMP, TEST, MIG, OPS}` | MD,FR,NFR,SC,G,D ∪ {DM, API, COMP, TEST, MIG, OPS} |
| generate | none (consumer, not inventory producer) | **Yes** (`id` field present) | `{DM, API, COMP, TEST, MIG, OPS, OQ}` | MD,FR,NFR,SC,G,D ∪ {DM, API, COMP, TEST, MIG, OPS, OQ} |
| merge | none | **Yes** (`id` field present) | `{DM, API, COMP, TEST, MIG, OPS, OQ}` (≡ generate) | MD,FR,NFR,SC,G,D ∪ {DM, API, COMP, TEST, MIG, OPS, OQ} |

## Literal probe output

```
extract | arrays= ['component_inventory'] | open_questions[].id= absent
extract_tdd | arrays= ['component_inventory', 'data_models', 'api_specifications', 'testing_strategy', 'migration_plan', 'operational_readiness'] | open_questions[].id= absent
generate | arrays= [] | open_questions[].id= id
merge | arrays= [] | open_questions[].id= id
```

## Findings

- **No divergence from research file 02.** The live structural evidence reproduces the claimed mapping exactly:
  - `extract_tdd` → its 6 typed arrays map 1:1 to {DM,API,COMP,TEST,MIG,OPS}. INTENTIONAL.
  - `extract` → only `component_inventory` (→COMP). DM has **no `data_models` array** but is **fixture-backed** (`test_tool_write_step_extract.py` roadmap_ids fixture includes `DM-extraction` per research file 03 §3b) → **KEEP DM** in extract's set.
  - `generate ≡ merge` → no producer arrays but `open_questions[].id` present (OQ source) plus they consume upstream entity IDs → full {DM,API,COMP,TEST,MIG,OPS,OQ}.
- **OQ correctly absent from extract/extract_tdd** — their `open_questions` is not an id-bearing object array (probe: `absent`), so no OQ-prefixed roadmap_id can legitimately arise at extract time.
- This confirms the assembler MUST be **per-step-aware** (4 family sets, with generate≡merge), NOT one flat pattern. Feeds the Phase 3 decision and the Phase 4 `TOOL_WRITE_ROADMAP_ID_FAMILIES` map.
