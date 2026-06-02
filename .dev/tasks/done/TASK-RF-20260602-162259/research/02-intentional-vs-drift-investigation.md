# Research 02 — Doc/Intent Cross-Validation: Intentional vs Drift

**Task:** TASK-RF-20260602-162259
**Topic:** Are the per-schema `roadmap_ids` family-set differences INTENTIONAL (per-step semantics) or DRIFT?
**Branch:** refactor/roadmap-pipeline-r0-r1-rewrite
**Date:** 2026-06-02
**Status:** In Progress

## Scope

Determine whether the 4 tool-write schemas legitimately accept different family sets, and
recommend where the tool-write-only family SoT should live. Do NOT duplicate schema/contracts
inventory, guard tests, or MDTM template work (other researchers).

## The observed family sets (VERIFIED by Read this session)

| Schema | roadmap_ids family set | file:line |
|---|---|---|
| generate | FR, NFR, SC, G, D, **DM, API, COMP, TEST, MIG, OPS, OQ** | generate.schema.json:140 |
| merge | FR, NFR, SC, G, D, **DM, API, COMP, TEST, MIG, OPS, OQ** (== generate) | merge.schema.json:156 |
| extract | FR, NFR, SC, G, D, **COMP, DM** (omits API/TEST/MIG/OPS/OQ) | extract.schema.json:134 |
| extract_tdd | FR, NFR, SC, G, D, **DM, API, COMP, TEST, MIG, OPS** (omits OQ) | extract_tdd.schema.json:218 |

None contains `MD` (`M\d+-D-?\d+`). Confirmed by inspection of all four patterns.

## Finding 1 — `$comment` fields explain step ROLE, not the family SET (VERIFIED)

Quoting the relevant `$comment` from each schema (Read this session):

- **extract.schema.json:5** — *"roadmap_ids carries the IDs the extract step surfaces. Extract is the SOURCE of spec_ids (it DEFINES the universe)…"*
- **extract_tdd.schema.json:5** — *"TDD-input variant of the extract step… Extract is the SOURCE of spec_ids (it DEFINES the universe)…"*
- **generate.schema.json:5** — *"roadmap_ids is the generator-side phantom-ID surface (Contract #3)… the SET-membership constraint (roadmap_ids ⊆ spec_ids ∪ accepted_deviations) is enforced at runtime by tool_writer.validate_id_subset against the envelope's spec_ids…"*
- **merge.schema.json:5** — *"Merge is the SECOND primary phantom-ID source… roadmap_ids is the generator-side phantom-ID surface…"*

**Conclusion on the comments:** No `$comment` explicitly justifies a narrower or broader *family set* per step. They explain the **subset-validation role** (extract DEFINES the universe; generate/merge are GENERATORS validated against it). So the comments are SILENT on the intent question — the intent must be read off the schema STRUCTURE, not the prose. (Marked: the prose does not directly answer the question; structural evidence below does.)

## Finding 2 — Git history: authored together in ONE commit, not piecemeal (VERIFIED)

- `git log --oneline -- <each schema>`: all four `roadmap_ids` patterns originate in **`c542b6bf`** ("feat(roadmap): R1.4 tool-write migrations (Steps 9.1-9.9)").
- `git show c542b6bf` confirms the four patterns were written **with their differences already present** at creation:
  - extract (commit line 370): `…|D-?\d+|COMP-\w+|DM-\w+)$` (COMP,DM only — note order COMP-before-DM)
  - extract_tdd (line 597): `…|DM-\w+|API-\w+|COMP-\w+|TEST-\w+|MIG-\w+|OPS-\w+)$` (no OQ)
  - generate (line 747) / merge (line 913): `…|DM…|API…|COMP…|TEST…|MIG…|OPS…|OQ-\w+)$` (full + OQ)
- The only later commit touching extract/extract_tdd (`d191d161`, "R1.4 PG9 gate close") changed **only** the `extraction_mode` enum→regex (`^(standard|chunked.*)$`), **NOT** `roadmap_ids` (verified via `git show d191d161 … | grep`).

**Conclusion:** The differences were a single deliberate authoring act, not accreted drift across commits. This *weakly* favors intent (they were written side-by-side, differently, on purpose) — but co-authorship alone does not prove correctness. Decisive evidence is the structural alignment below.

## Finding 3 — Structural alignment: families map to the typed inventories each step produces/consumes (VERIFIED, decisive)

Cross-tabulation (computed this session from the live schemas):

| step | roadmap_ids families | entity arrays defined in schema | OQ-id source (nested `milestones[].open_questions[].id`) |
|---|---|---|---|
| extract | FR,NFR,SC,G,D,**DM,COMP** | `component_inventory` (→COMP) only | No |
| extract_tdd | FR,NFR,SC,G,D,**DM,API,COMP,TEST,MIG,OPS** | `data_models,api_specifications,component_inventory,testing_strategy,migration_plan,operational_readiness` (all 6) | No |
| generate | FR,NFR,SC,G,D,DM,API,COMP,TEST,MIG,OPS,**OQ** | none (consumer, not inventory producer) | **Yes** (`milestones[].open_questions[].id`, e.g. fixture `OQ-1`) |
| merge | FR,NFR,SC,G,D,DM,API,COMP,TEST,MIG,OPS,**OQ** | none | **Yes** |

Interpretation per step:
- **extract_tdd** — family set EXACTLY matches its 6 typed entity arrays. A TDD has data models, API surfaces, components, test strategy, migration plan, operational readiness, so the LLM can emit DM/API/COMP/TEST/MIG/OPS IDs. **Perfectly grounded → INTENTIONAL.**
- **extract** (plain spec) — defines only `component_inventory`; a plain spec has no TDD-level data-model/API/test/migration/ops inventories, so omitting API/TEST/MIG/OPS is **semantically correct**. (Caveat: extract's pattern *accepts* `DM-` but the schema has **no `data_models` array** — extract.schema.json:`'data_models' in properties == False`. So DM in extract is *un-backed* — see Finding 4.)
- **generate/merge** — emit `milestones[].open_questions[].id` (OQ family; fixtures use `OQ-1` at generate L118 / merge L143) and **consume** the entity IDs minted upstream (deliverable IDs like `COMP-loader`, `API-merge`, `DM-config`, `TEST-e2e`, `MIG-cutover`, `OPS-metrics` — verified in test_tool_write_step_merge.py:158-180,229-231). So the full superset + OQ is grounded. **INTENTIONAL.**

This is the SUPERSET relationship the BUILD-REQUEST states, now confirmed at the per-step granularity: each step's family set tracks what that step structurally produces or consumes.

## Finding 4 — The two "differences" decomposed: ONE intentional axis + TWO small drift residues

The per-schema variation is NOT one homogeneous thing. Decompose:

**(A) extract_tdd vs extract: API/TEST/MIG/OPS present in tdd, absent in extract — INTENTIONAL.**
Grounded by structural arrays (Finding 3). A plain spec cannot surface TDD-level inventories; the TDD variant can. Keep distinct.

**(B) OQ in generate/merge, absent in extract/extract_tdd — INTENTIONAL.**
OQ-IDs come from `milestones[].open_questions[].id`, a structure that exists ONLY in generate/merge. In extract/extract_tdd, `open_questions` is a flat **array of plain strings** (`items: {type: string}`, no `id`) — verified — so no OQ-prefixed roadmap_id can legitimately arise at extract time. Omitting OQ from extract is correct.

**(C) DRIFT RESIDUE #1 — extract accepts `DM-` with no `data_models` array.**
extract.schema.json has `component_inventory` but NOT `data_models`, yet its `roadmap_ids` pattern includes `DM-\w+`. This DM arm is unbacked. It is harmless today (it only *permits* an ID family the LLM has no structured place to produce), but it is a genuine inconsistency — extract's family set does not perfectly track its arrays the way extract_tdd's does. **This is mild drift, not intent.**

**(D) DRIFT RESIDUE #2 — alternation ORDERING is inconsistent.**
extract orders `COMP-\w+|DM-\w+`; every other schema orders `DM-…|…|COMP-…`. Pure ordering noise from hand-authoring. Cosmetic, but it confirms these were hand-typed copies (drift surface), not machine-derived. A single assembler eliminates this.

**(E) MD missing from ALL four — DRIFT (separate, already mandated by BUILD-REQUEST).**
`MD` (`M\d+-D-?\d+`) is a SPEC family in `ID_PATTERNS` (contracts) and is unconditionally missing from all four `roadmap_ids` patterns (`grep 'M\d+-D'` → 0 hits, re-verified). This is unambiguous drift and must be added to all four regardless of the intentional/drift verdict on A–D.

## Finding 5 — Why `$comment` doesn't contradict intent, and the guard tests encode the intent ASYMMETRICALLY

The existing guard tests already *encode* a two-tier expectation, which corroborates that the difference is by-design:
- `test_extract_schema_id_pattern_matches_contracts` (test_tool_write_step_extract.py:130-143) asserts ONLY the 5 spec bodies `("FR","NFR","SC","G","D")` — it does NOT assert API/TEST/MIG/OPS (because extract isn't supposed to have them).
- `test_generate_schema_id_pattern_matches_contracts` (test_tool_write_step_generate.py:219-235) asserts the 5 spec bodies **PLUS** `("DM-","API-","COMP-","TEST-","MIG-","OPS-")` prefixes.

So the test authors deliberately checked a BROADER set for generate than for extract — independent corroboration that the per-step family difference is intentional, not accidental. (These tests are still structurally broken per the BUILD-REQUEST — frozen tuple, substring match, no MD — but their *asymmetry* reflects design intent.)

## RECOMMENDATION

### Verdict: INTENTIONAL (per-step semantics), with two small drift residues to clean up while unifying

The per-schema family-set differences are **predominantly INTENTIONAL**, grounded in what each
step structurally produces or consumes (Finding 3). The assembler MUST be **per-step-aware** — a
single flat "one pattern for all four" would be *wrong*: it would let extract emit
API/TEST/MIG/OPS IDs it has no structured inventory to back, eroding the extract-vs-extract_tdd
distinction the pipeline relies on.

Two residues are genuine drift and should be fixed *as part of* the unification (not by widening
everything to a common superset):
- **(C)** extract's unbacked `DM-` arm — decide deliberately: either DROP DM from extract (extract has no `data_models` array) OR ADD a `data_models` array to extract. Recommend **DROP DM from extract's family set** (least-change, matches its actual arrays: COMP only) unless the other researcher's fixture inventory shows extract fixtures emit DM IDs. NOTE: extract's own test fixture (test_tool_write_step_extract.py:108-114) DOES list `DM-extraction` in roadmap_ids — so dropping DM would break that fixture. Therefore: **KEEP DM in extract** and treat extract's legitimate set as {spec families} ∪ {COMP, DM}. The "unbacked array" is cosmetic; the fixture establishes DM as a real extract family. (Flagged for the implementer to confirm against the fixture-inventory researcher.)
- **(D)** ordering inconsistency — auto-resolved by deriving from an ordered SoT.
- **(E)** MD missing everywhere — add to all four (mandated).

### Design: per-step SoT mapping in `superclaude.contracts` (Option (a), per-step variant)

Establish in `superclaude.contracts`:

1. A spec-family pattern source = the existing `ID_PATTERNS` (FR/NFR/SC/G/D/MD) — **unchanged**,
   keeps `spec_parser.extract_requirement_ids` regex extraction seeing ONLY the 6 spec families.
2. A NEW tool-write-only family registry, e.g. `ROADMAP_ENTITY_ID_FAMILIES` mapping prefix→body:
   `{COMP, DM, API, TEST, MIG, OPS, OQ}` with bodies like `COMP-\w+`, `OQ-\w+`, etc.
3. A NEW **per-step family-set map**, e.g. `TOOL_WRITE_ROADMAP_ID_FAMILIES`:
   - `extract`      → spec families ∪ {COMP, DM}
   - `extract_tdd`  → spec families ∪ {DM, API, COMP, TEST, MIG, OPS}
   - `generate`     → spec families ∪ {DM, API, COMP, TEST, MIG, OPS, OQ}
   - `merge`        → spec families ∪ {DM, API, COMP, TEST, MIG, OPS, OQ}
   (Note `merge == generate`, preserving the existing merge==generate pin.)
4. An assembler `roadmap_ids_pattern(step) -> "^(" + "|".join(ordered family bodies) + ")$"`
   that wraps anchor-free bodies, preserves **MD-before-D** ordering, and emits a deterministic
   family order so the four schemas can be regenerated (eliminating drift residue D).

MD lands in EVERY step's pattern automatically because it is in `ID_PATTERNS` (the spec-family
base every step includes).

### Why REJECT promoting the extras into `ID_PATTERNS` (Option (b))

`ID_PATTERNS` is consumed by `spec_parser.extract_requirement_ids` (spec_parser.py:342-357),
which regex-scans the raw spec/markdown text for requirement IDs. Promoting
COMP/DM/API/TEST/MIG/OPS/OQ into `ID_PATTERNS` would make that regex **start matching
roadmap-internal entity IDs as if they were spec requirements** — polluting the spec-extraction
universe, inflating `total_requirements`, and corrupting the very `spec_ids` set that
`validate_id_subset` checks against. The spec families (what a SPEC declares) and the tool-write
entity families (what the LLM mints WHILE ELABORATING a roadmap) are deliberately distinct
universes (Finding 3 + the `$comment` "extract DEFINES the universe"). They must stay separate
constants. **REJECT (b).** The new per-step map (Option (a)) keeps them distinct while giving the
schemas a single derivation source.

### MD caveat (mandated regardless of verdict)

`MD` is a SPEC family — it belongs in `ID_PATTERNS` (already there) and flows into all four
schemas via the spec-family base. Do NOT add `MD` to the new entity-family registry. The guard
tests must assert MD is present as its OWN alternation arm in all four patterns, using
**arm-level / exact** matching (split the alternation on `|` and compare arms), NOT substring —
because `D-?\d+ ⊂ M\d+-D-?\d+` makes substring matching falsely pass (the MD⊂D trap).

### Net guidance to the task

- Assembler = **per-step** (4 family sets: extract, extract_tdd, generate≡merge), NOT one flat pattern.
- SoT = new per-step map + entity-family registry in `superclaude.contracts`; `ID_PATTERNS` untouched.
- Reconcile = regenerate all four from the map (fixes ordering D + adds MD E); KEEP the
  extract/extract_tdd/generate-vs-merge family differences (they are intentional A + B).
- Confirm the extract-DM question against the fixture-inventory researcher before finalizing
  extract's set (this report's read of test_tool_write_step_extract.py:108-114 says KEEP DM).

## Status: Complete

**Summary:** The per-schema `roadmap_ids` family differences are **INTENTIONAL per-step
semantics**, not drift. Each step's family set tracks the typed inventories it produces
(extract_tdd's 6 entity arrays; extract's component_inventory-only) or consumes/mints
(generate/merge consume entity deliverable IDs and mint OQ from `milestones[].open_questions[].id`).
Authored together in one commit (`c542b6bf`) with differences present from creation; the existing
guard tests already encode an asymmetric (broader-for-generate) expectation that corroborates
intent. Three true drift items ride alongside: extract's cosmetically-unbacked DM arm (KEEP per
fixture), inconsistent alternation ordering, and MD missing everywhere (add to all four).
**Recommendation: per-step-aware assembler** deriving from a NEW per-step family-set map in
`superclaude.contracts` (Option (a), per-step variant); **REJECT** promoting extras into
`ID_PATTERNS` (would pollute spec_parser regex extraction). `ID_PATTERNS` stays the SoT for the 6
spec families incl. MD; a separate entity-family registry holds COMP/DM/API/TEST/MIG/OPS/OQ.
