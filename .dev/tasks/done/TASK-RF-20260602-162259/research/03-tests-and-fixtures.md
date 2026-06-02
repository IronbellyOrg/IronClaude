# Research 03 — Test & Verification (tool-write schema ID SoT)

**Task:** TASK-RF-20260602-162259
**Topic:** Test & Verification — the 4 broken guard tests, the 55 extra-family fixture usages, rebuild/verify.
**Branch:** refactor/roadmap-pipeline-r0-r1-rewrite
**Date:** 2026-06-02
**Status:** Complete (see end-of-file summary)

All file:line citations re-verified by Read/grep this session unless marked `[UNVERIFIED]`.

---

## 0. Quick map of relevant files

| File | Role |
|---|---|
| `tests/roadmap/test_tool_write_step_extract.py` | guard test + extract fixtures |
| `tests/roadmap/test_tool_write_step_extract_tdd.py` | guard test + extract_tdd fixtures |
| `tests/roadmap/test_tool_write_step_generate.py` | guard test + generate fixtures + id-check render test |
| `tests/roadmap/test_tool_write_step_merge.py` | guard test + merge==generate pin + id-check render test |
| `tests/roadmap/test_merge_completeness.py` | uses `OQ-` family |
| `tests/roadmap/test_cosmetic_remediator.py` | uses `OQ-` family |
| `src/superclaude/cli/roadmap/tool_writer.py` | `load_schema` (L67), `validate_tool_output` (L94) |
| `src/superclaude/contracts/__init__.py` | `ID_PATTERNS` SoT (L64-78) |

### ID_PATTERNS SoT (verified `src/superclaude/contracts/__init__.py` L64-78)

```python
ID_PATTERNS: Final[dict[str, str]] = {
    "MD": r"M\d+-D-?\d+",     # ordered BEFORE D
    "FR": r"FR-\d+(?:\.\d+)?",
    "NFR": r"NFR-\d+(?:\.\d+)?",
    "SC": r"SC-\d+",
    "G": r"G-\d+",
    "D": r"D-?\d+",
}
```

Keys order: `MD, FR, NFR, SC, G, D` (6 families). **The MD⊂D substring trap is real:** the `D` body `D-?\d+` is a literal substring of the `MD` body `M\d+-D-?\d+`.

### How tests load the schema + extract the pattern (verified, all four identical)

```python
from superclaude.cli.roadmap.tool_writer import load_schema, validate_tool_output
from superclaude.contracts import ID_PATTERNS
schema  = load_schema("<name>.schema.json")
pattern = schema["properties"]["roadmap_ids"]["items"]["pattern"]
```

`load_schema` (`tool_writer.py` L67-91) = `json.loads((TOOL_SCHEMAS_DIR / name).read_text())`; `TOOL_SCHEMAS_DIR = TEMPLATES_DIR / "tool_schemas"` (L38). It is a plain file read — the test reads the **same on-disk JSON** the runtime validates against, so a guard test that recomposes the pattern from the live SoT and exact-matches the on-disk arm is a true drift gate.

`validate_tool_output(output, schema)` (`tool_writer.py` L94-117) compiles a `jsonschema` validator from `$schema` and returns a list of error strings; **empty list = PASS**. This is the helper a positive `M1-D01` check should call.

---

## 1. The four guard tests `test_*_schema_id_pattern_matches_contracts`

### 1a. extract — `test_extract_schema_id_pattern_matches_contracts` (L130-143)

```python
def test_extract_schema_id_pattern_matches_contracts() -> None:
    schema = load_schema("extract.schema.json")
    pattern = schema["properties"]["roadmap_ids"]["items"]["pattern"]
    for family in ("FR", "NFR", "SC", "G", "D"):
        assert ID_PATTERNS[family] in pattern, (
            f"ID_PATTERNS['{family}'] body {ID_PATTERNS[family]!r} "
            f"missing from roadmap_ids pattern {pattern!r}"
        )
```

Frozen tuple `("FR","NFR","SC","G","D")` — **MD absent**. Uses substring `ID_PATTERNS[family] in pattern`. No `prefix` loop (extract guard does not assert the extra families at all).

### 1b. extract_tdd — `test_extract_tdd_schema_id_pattern_matches_contracts` (L206-225)

Same frozen tuple `("FR","NFR","SC","G","D")` + substring check, PLUS a second loop:
```python
    for prefix in ("DM-", "API-", "COMP-", "TEST-", "MIG-", "OPS-"):
        assert prefix in pattern, (...)
```
(6 prefixes — `OQ-` absent from this assertion list.)

### 1c. generate — `test_generate_schema_id_pattern_matches_contracts` (L219-236)

Identical structure to extract_tdd: frozen `("FR","NFR","SC","G","D")` substring loop + `("DM-","API-","COMP-","TEST-","MIG-","OPS-")` `prefix in pattern` loop. (`OQ-` not asserted here either, though generate.schema **does** contain OQ — see §3.)

### 1d. merge — `test_merge_schema_id_pattern_matches_contracts` (L250-268)

Identical structure to generate: same two loops, same 5-family frozen tuple, same 6 prefixes.

### WHY all four silently passed the MD drift (two independent reasons)

1. **MD not in the frozen tuple.** The loop iterates `("FR","NFR","SC","G","D")` — a hand-frozen literal that never included `MD`. `ID_PATTERNS["MD"]` is never looked up, so a schema omitting MD is never challenged. This is the primary bug.
2. **Substring containment would falsely pass even if MD were added.** If someone "fixed" bug 1 by iterating `ID_PATTERNS.keys()` while keeping `ID_PATTERNS[family] in pattern`, the MD check would be `r"M\d+-D-?\d+" in pattern`. The schemas contain the `D` arm `D-?\d+` but **not** the MD arm — so this naive fix still FALSELY PASSES is *the wrong way round*: actually `r"M\d+-D-?\d+"` is NOT a substring of a schema that lacks MD, so a keys-driven substring check WOULD correctly fail-to-find MD. **The real trap is the reverse:** once MD *is* added to the schema, the bare-`D` family check `r"D-?\d+" in pattern` passes trivially because `D-?\d+` is a substring of the MD arm `M\d+-D-?\d+` — so substring matching can no longer distinguish "D arm present" from "only MD arm present." Substring is one-directional and blind to arm boundaries; it cannot assert that each family is its OWN alternation arm. That is why the rebuild must use exact/arm-level matching, not substring. `[NOTE: builder should confirm both directions — the durable requirement is arm-level matching regardless.]`

---

## 2. `test_merge_schema_matches_generate_id_pattern` (merge L271-279)

```python
def test_merge_schema_matches_generate_id_pattern() -> None:
    """Merge reuses the SAME roadmap_ids pattern as generate (no divergence)."""
    merge_pattern = load_schema("merge.schema.json")[
        "properties"
    ]["roadmap_ids"]["items"]["pattern"]
    generate_pattern = load_schema("generate.schema.json")[
        "properties"
    ]["roadmap_ids"]["items"]["pattern"]
    assert merge_pattern == generate_pattern
```

Pins **exact string equality** of merge's and generate's `roadmap_ids.items.pattern`. This is the ONLY exact-match guard among the five tests, and it covers only the merge==generate pair. Nothing currently pins extract or extract_tdd to anything (no cross-schema equality test). Because merge==generate is exact equality, when the builder adds MD to **both** it stays green; if MD lands in only one, this test fails (useful collateral guard). The builder should consider extending this into a parametrized "all four derive from the same assembler" pin (see §4).

---

## 3. The 55 extra-family fixture usages (enumerated)

Grand total **55** occurrences of `"(DM|API|COMP|TEST|MIG|OPS|OQ)-…"` string literals across the six files (verified by grep this session):

| File | Count | Families present (as literals) |
|---|---|---|
| `test_tool_write_step_extract.py` | 5 | COMP, DM |
| `test_tool_write_step_extract_tdd.py` | 19 | API, COMP, DM, MIG, OPS, TEST |
| `test_tool_write_step_generate.py` | 5 | API, COMP, DM, MIG, OPS, OQ, TEST |
| `test_tool_write_step_merge.py` | 23 | API, COMP, DM, MIG, OPS, OQ, TEST |
| `test_merge_completeness.py` | 2 | OQ |
| `test_cosmetic_remediator.py` | 1 | OQ |

**CRITICAL nuance — not every literal is a `roadmap_ids` entry:**

- The `roadmap_ids` arrays that the schema's `roadmap_ids.items.pattern` actually validates contain DM/API/COMP/TEST/MIG/OPS (NOT OQ). The OQ literals are elsewhere:
  - `generate.py:118` and `merge.py:143`: `"id": "OQ-1"` is inside `open_questions[].id` — a DIFFERENT schema field, not `roadmap_ids` (verified context).
  - `test_merge_completeness.py:126` / `test_cosmetic_remediator.py:140`: `"OQ-xxx"`, `"OQ-002"` are assertions about *missing*/semantic-violation IDs, not schema `roadmap_ids` validation.
- So although `generate.schema.json` and `merge.schema.json` DO carry `OQ-\w+` in their `roadmap_ids` pattern (verified on disk, §3a), **no fixture feeds an OQ value through `roadmap_ids`.** `[IMPLICATION: the OQ arm in generate/merge roadmap_ids is unexercised-as-roadmap_id today; defer the "does OQ belong in roadmap_ids" call to the intentional-vs-drift researcher.]`

### 3a. On-disk schema `roadmap_ids.items.pattern` (verified)

```
extract     (L134): ^(FR-\d+(?:\.\d+)?|NFR-\d+(?:\.\d+)?|SC-\d+|G-\d+|D-?\d+|COMP-\w+|DM-\w+)$
extract_tdd (L218): ^(FR-…|NFR-…|SC-\d+|G-\d+|D-?\d+|DM-\w+|API-\w+|COMP-\w+|TEST-\w+|MIG-\w+|OPS-\w+)$
generate    (L140): ^(FR-…|NFR-…|SC-\d+|G-\d+|D-?\d+|DM-\w+|API-\w+|COMP-\w+|TEST-\w+|MIG-\w+|OPS-\w+|OQ-\w+)$
merge       (L156): ^(…identical to generate…|OQ-\w+)$
```

None contain `MD`. **Positive check confirmed this session:** `re.match(pattern, "M1-D01")` is `False` for all four (run via `uv run python`). This is the live bug — a tool-write `roadmap_ids` containing `M1-D01` is rejected.

### 3b. Representative `roadmap_ids` arrays the builder must keep passing

**extract** (fixture L108-114) — `COMP-extractor`, `DM-extraction`:
```python
"roadmap_ids": ["FR-1","FR-2.1","NFR-1","COMP-extractor","DM-extraction"]
```
**extract_tdd** (fixture L177-186) — full extra set:
```python
"roadmap_ids": ["FR-1","FR-2.1","NFR-1","DM-001","API-001","COMP-001","TEST-001","MIG-001","OPS-001"]
```
**generate** (fixture L206) — FR-only:
```python
"roadmap_ids": ["FR-1","FR-2","FR-3","FR-4","FR-5"]
```
**merge** (fixture L228-233) — broad extra set:
```python
"roadmap_ids": ["FR-1","FR-2","FR-3","COMP-loader","DM-config","API-load",
                "FR-4","FR-5","FR-6","API-render","DM-roadmap","COMP-renderer",
                "FR-7","FR-8","FR-9","API-merge","TEST-integration","MIG-cutover",
                "FR-10","FR-11","FR-12","OPS-metrics","TEST-e2e","NFR-1"]
```

These arrays are asserted via `test_valid_output_passes_schema` → `assert validate_tool_output(<fixture>, schema) == []` (extract L148, extract_tdd L230, generate L241, merge L284). **The new schema pattern MUST keep DM/API/COMP/TEST/MIG/OPS matching** or these turn red. The merge fixture's `roadmap_ids` is also iterated in the id-check render test (`for rid in merge_fixture["roadmap_ids"]`, merge L326; generate L285) where each rid must appear in rendered markdown and pass `validate_id_subset`. So the extra families are load-bearing in BOTH the schema-validation path AND the subset-gate/render path.

---

## 4. Proposed NEW regression: MD as its OWN alternation arm + keys-driven exact guards

### 4a. The arm-level assertion (defeats the MD⊂D trap)

Two complementary assertions the builder should add to each of the four guard tests (or a shared parametrized test):

**(i) Behavioral — MD matches, and matches *as MD*:**
```python
import re
pattern = schema["properties"]["roadmap_ids"]["items"]["pattern"]
assert re.match(pattern, "M1-D01"), "M1-D01 must validate (MD family present)"
```
This is the simplest durable proof: today it fails on all four; after the fix it passes. Pair with a known-good bare-D value (`"D-1"`) and a value that MUST NOT match (`"XYZ-1"`) so the arm is bounded.

**(ii) Structural — MD is a literal alternation arm, not just a substring:**
The pattern is `^(arm1|arm2|…|armN)$`. Split it into arms and assert exact membership:
```python
from superclaude.contracts import ID_PATTERNS
inner = pattern[len("^("):-len(")$")]          # strip ^( … )$
arms = inner.split("|")
assert ID_PATTERNS["MD"] in arms, (
    f"MD body {ID_PATTERNS['MD']!r} not an exact alternation arm of {arms!r}"
)
```
Because `arms` is split on `|`, `ID_PATTERNS["MD"] in arms` is **exact arm equality** — `D-?\d+` will NOT spuriously satisfy the MD arm, and the MD arm `M\d+-D-?\d+` will NOT be satisfied by the presence of the bare-D arm. This is the immune-to-MD⊂D check the BUILD-REQUEST §66 demands. `[CAVEAT: split("|") assumes no family body itself contains a top-level "|". None of the 6 ID_PATTERNS bodies nor the 7 extras contain "|", verified by reading ID_PATTERNS and the on-disk patterns — safe today. If a future body adds an internal alternation it must be parenthesized; the builder's assembler should guarantee that.]`

### 4b. Making the four guard tests keys-driven + exact-arm

Replace the frozen tuple + substring with iteration over the LIVE family set and exact-arm membership:
```python
def test_<step>_schema_id_pattern_matches_contracts() -> None:
    schema = load_schema("<step>.schema.json")
    pattern = schema["properties"]["roadmap_ids"]["items"]["pattern"]
    inner = pattern[2:-2]                       # strip "^(" and ")$"
    arms = inner.split("|")
    # EVERY spec family (the live SoT, not a frozen tuple) is an exact arm:
    for family, body in ID_PATTERNS.items():    # iterates MD,FR,NFR,SC,G,D
        assert body in arms, f"{family} body {body!r} missing as arm in {arms!r}"
```
Iterating `ID_PATTERNS.items()` auto-covers any future family addition (the durability requirement). The exact-arm membership (`body in arms`) is immune to the substring trap. The extra (tool-write-only) families should be asserted from the *same* SoT the schema derives from — i.e. import the new `ROADMAP_ID_FAMILIES` / `TOOL_WRITE_EXTRA_ID_FAMILIES` constant (per the design-decision researcher) and assert those arms too, rather than re-freezing `("DM-","API-",…)`. That makes the guard fully keys-driven on BOTH halves of the union.

`[BUILDER NOTE: the per-step schemas differ (extract omits API/TEST/MIG/OPS/OQ; extract_tdd omits OQ). If the intentional-vs-drift researcher rules these per-step intentional, the guard must assert the per-step expected subset, not the full union — drive each test from a per-step family list exported by the assembler. If ruled drift→unify, all four assert the full union. Either way: keys-driven from the SoT, exact-arm, never a frozen literal.]`

---

## 5. Verification commands (exact)

| Goal | Command | Expected |
|---|---|---|
| Tool-write suite green (the 55 extra usages still pass) | `uv run pytest tests/roadmap/ -k tool_write -q` | baseline this session: **157 passed, 1 skipped, 1808 deselected**. Builder must keep ≥157 passing (new MD regressions add to count). |
| Run only the four guard + merge-pin tests | `uv run pytest tests/roadmap/ -k "schema_id_pattern or matches_generate_id_pattern" -q` | all green after fix |
| Architecture lint (Contract #8 / arch-lint Rule 2) | `make lint-architecture` | exit 0 |
| SoT↔mirror sync (NOTE below) | `make verify-sync` | clean |
| Positive MD validation (the acceptance proof) | `uv run python -c "from superclaude.cli.roadmap.tool_writer import load_schema,validate_tool_output; import copy,json; ..."` see snippet below | `[]` (PASS) for a roadmap_ids containing `M1-D01` |

**Positive `M1-D01` validation — which helper exercises it:** `validate_tool_output(tool_output, schema)` in `src/superclaude/cli/roadmap/tool_writer.py` L94-117 is the runtime validator; returns `[]` on PASS. The test surface that exercises a fixture through it is `test_valid_output_passes_schema` (extract L146-148, extract_tdd L228-230, generate L239-241, merge L283-284). The builder should add a fixture variant (or a dedicated test) that appends `"M1-D01"` to a `roadmap_ids` array and asserts `validate_tool_output(fixture_with_md, schema) == []`. Today, run directly, this FAILS for all four (confirmed: `re.match(pattern,"M1-D01")` → `False` ×4). After the fix it must return `[]`.

Single-line positive check the builder can paste (current = expect a non-empty error list today):
```
uv run python -c "import re;from superclaude.cli.roadmap.tool_writer import load_schema;[print(n, bool(re.match(load_schema(n+'.schema.json')['properties']['roadmap_ids']['items']['pattern'],'M1-D01'))) for n in ['extract','extract_tdd','generate','merge']]"
```

### verify-sync / sync-dev scope (IMPORTANT for the builder)

`make sync-dev` (Makefile L109+) copies `src/superclaude/{skills,agents,...}` → `.claude/`. It does **NOT** touch `src/superclaude/cli/roadmap/templates/tool_schemas/` (verified: the sync-dev body globs `src/superclaude/skills/*/` and agents, never `cli/`). Therefore:
- Editing the four `*.schema.json` under `tool_schemas/` produces **no `.claude/` mirror** — there is nothing to sync, and **nothing under `.claude/` should be staged** for this task.
- `make verify-sync` should remain clean because the schema edits are outside its scope; run it anyway as an acceptance gate (BUILD-REQUEST §74) to prove no incidental skill/agent drift.

### Baseline captured this session

- `uv run pytest tests/roadmap/ -k tool_write -q` → **157 passed, 1 skipped, 1808 deselected in 0.76s** (clean baseline; all 55 extra-family usages currently pass).
- `re.match(pattern, "M1-D01")` → `False` for extract/extract_tdd/generate/merge (the bug, reproduced).

---

## Status: Complete

### Summary for the builder
1. **Four guard tests** (`test_*_schema_id_pattern_matches_contracts`): extract L130-143, extract_tdd L206-225, generate L219-236, merge L250-268. All iterate a frozen `("FR","NFR","SC","G","D")` (MD absent) with substring `ID_PATTERNS[family] in pattern`; extract_tdd/generate/merge add a frozen `("DM-","API-","COMP-","TEST-","MIG-","OPS-")` `prefix in pattern` loop (extract has no extras loop). They silently passed MD drift because MD was never in the tuple, and substring matching is blind to arm boundaries (MD⊂D trap).
2. **`test_merge_schema_matches_generate_id_pattern`** (merge L271-279): the only exact-equality guard, pins merge.pattern == generate.pattern; nothing pins extract/extract_tdd.
3. **55 extra-family usages confirmed** (5/19/5/23/2/1 across the six files). The schema-validated `roadmap_ids` arrays carry DM/API/COMP/TEST/MIG/OPS; OQ appears only in `open_questions[].id` and completeness/cosmetic assertions, NOT in any validated `roadmap_ids`. Representative arrays quoted in §3b. New schema pattern MUST keep these passing via `test_valid_output_passes_schema` and the id-check render tests.
4. **New regression approach**: `re.match(pattern,"M1-D01")` truthy + structural `ID_PATTERNS["MD"] in pattern[2:-2].split("|")` (exact arm membership — immune to MD⊂D). Make all four guards keys-driven: iterate `ID_PATTERNS.items()` (auto-covers future families) with exact-arm membership, and assert the extra families from the same SoT constant rather than a frozen literal. Respect the per-step subset question (defer to intentional-vs-drift researcher).
5. **Verification**: `uv run pytest tests/roadmap/ -k tool_write -q` (baseline 157 passed/1 skipped — must stay green), `make lint-architecture` (exit 0), `make verify-sync` (clean; tool_schemas is NOT a sync-dev target so no `.claude/` staging), positive proof via `validate_tool_output(fixture_with_M1-D01, schema) == []`.
