---
artifact: schema-sot-decision
phase: 3
gate: design-decision
verdict_source: research/02-intentional-vs-drift-investigation.md
decision: PROCEED
---

# Schema-SoT Design Decision

**Date:** 2026-06-02
**Evidence inputs:** `phase-outputs/discovery/schema-md-omission.md`, `phase-outputs/discovery/per-step-family-mapping.md`, `research/02-intentional-vs-drift-investigation.md`

## Decision criterion (evaluated)

- **Do the four schemas omit MD?** YES — Step 2.1 probe: all four print `re.match(pattern, "M1-D01") == False`; no schema carries the `M\d+-D-?\d+` arm.
- **Does the per-step entity-array mapping hold?** YES — Step 2.2 reproduced research file 02's mapping exactly from the live schemas (extract→component_inventory only; extract_tdd→all 6 arrays; generate/merge→`open_questions[].id` present).

Both conditions hold → **EXPECTED path → `decision: PROCEED`**.

## (a) VERDICT

The per-schema `roadmap_ids` family-set differences are **INTENTIONAL per-step semantics, NOT drift**. Each step's family set tracks the typed inventories it structurally produces (extract_tdd's 6 entity arrays; extract's component_inventory) or consumes/mints (generate/merge consume upstream entity deliverable IDs and mint OQ from `milestones[].open_questions[].id`). Therefore the assembler MUST be **per-step-aware**. A single flat "one pattern for all four" is **REJECTED** — it would let extract emit API/TEST/MIG/OPS IDs it has no structured inventory to back, eroding the extract-vs-extract_tdd distinction the pipeline relies on.

## (b) Family-SoT SHAPE (lives in `superclaude.contracts`)

1. **`ID_PATTERNS` — UNTOUCHED.** Remains the six-spec-family SoT: `MD, FR, NFR, SC, G, D` (MD ordered before D). This keeps `spec_parser.extract_requirement_ids` regex extraction seeing ONLY the 6 spec families.
2. **NEW `ROADMAP_ENTITY_ID_FAMILIES: Final[dict[str, str]]`** — entity prefix → body registry holding `{COMP, DM, API, TEST, MIG, OPS, OQ}` as `<PREFIX>-\w+` bodies (`COMP-\w+`, `DM-\w+`, `API-\w+`, `TEST-\w+`, `MIG-\w+`, `OPS-\w+`, `OQ-\w+`).
3. **NEW `TOOL_WRITE_ROADMAP_ID_FAMILIES: Final[dict[str, tuple[str, ...]]]`** — per-step ordered entity-prefix tuples:
   - `extract`     → `(DM, COMP)`  *(reconciled to canonical DM-before-COMP order)*
   - `extract_tdd` → `(DM, API, COMP, TEST, MIG, OPS)`
   - `generate`    → `(DM, API, COMP, TEST, MIG, OPS, OQ)`
   - `merge`       → `(DM, API, COMP, TEST, MIG, OPS, OQ)`  *(≡ generate)*
4. **NEW `roadmap_ids_pattern(step: str) -> str`** — assembler emitting `"^(" + "|".join(spec_bodies + entity_bodies) + ")$"` where `spec_bodies = list(ID_PATTERNS.values())` (so MD is included and MD-before-D ordering is preserved — bodies are READ from `ID_PATTERNS`, never re-inlined: Contract #8 / arch-lint Rule 2) and `entity_bodies = [ROADMAP_ENTITY_ID_FAMILIES[p] for p in TOOL_WRITE_ROADMAP_ID_FAMILIES[step]]`. Raises for an unknown step.
5. All three new names exported in `__all__`.

MD lands in EVERY step's pattern automatically because it is in `ID_PATTERNS` (the spec-family base every step includes).

## (c) REJECTED alternative

**Promoting the entity extras into `ID_PATTERNS`** is REJECTED. `ID_PATTERNS` is consumed by `spec_parser.extract_requirement_ids`, which regex-scans raw spec/markdown text for requirement IDs. Promoting COMP/DM/API/TEST/MIG/OPS/OQ would make that regex match roadmap-internal entity IDs as if they were spec requirements — polluting the spec-extraction universe, inflating `total_requirements`, and corrupting the `spec_ids` set `validate_id_subset` checks against. Spec families and tool-write entity families are deliberately distinct universes and must stay separate constants.

## (d) RECONCILIATION rules (applied while unifying)

- **KEEP** extract's `DM` arm — fixture-backed (`test_tool_write_step_extract.py` roadmap_ids fixture includes `DM-extraction`). The "unbacked array" is cosmetic; the fixture establishes DM as a real extract family.
- **FIX** extract's ordering anomaly: change `COMP`-before-`DM` to canonical **DM-before-COMP**.
- **ADD** MD to ALL four schemas (via the spec-family base in the assembler).
- **PRESERVE** merge ≡ generate (identical family sets → identical assembler output).

## (e) CARRY-FORWARD — Phase 4 items that apply (decision = PROCEED → ALL apply)

- **4.1** — Add `ROADMAP_ENTITY_ID_FAMILIES` + `TOOL_WRITE_ROADMAP_ID_FAMILIES` + `roadmap_ids_pattern(step)` to `superclaude.contracts`, exported in `__all__`; `ID_PATTERNS` untouched.
- **4.2** — Verify the contracts module imports and the assembler emits the expected per-step patterns (M1-D01 matches; MD is an exact arm; merge==generate).
- **4.3** — Regenerate `extract.schema.json` `roadmap_ids.items.pattern` from `roadmap_ids_pattern('extract')` (DM-before-COMP, +MD).
- **4.4** — Regenerate `extract_tdd.schema.json` from `roadmap_ids_pattern('extract_tdd')` (no OQ, +MD).
- **4.5** — Regenerate `generate.schema.json` from `roadmap_ids_pattern('generate')` (full set, +MD).
- **4.6** — Regenerate `merge.schema.json` from `roadmap_ids_pattern('merge')` (≡ generate, +MD).
- **4.7** — Verify on-disk schemas accept `M1-D01` and `merge==generate` holds.

Phase 5 (guard-test rebuild + MD regression) and Phase 6 (lint/sync/full-suite) follow.
