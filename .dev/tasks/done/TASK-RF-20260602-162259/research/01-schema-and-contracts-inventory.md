# Research 01 — File Inventory + Integration Points (Schema ↔ Contracts SoT)

**Task:** TASK-RF-20260602-162259 — durable fix for drift between `superclaude.contracts.ID_PATTERNS` and the 4 tool-write JSON schemas' `roadmap_ids` patterns.
**Branch:** `refactor/roadmap-pipeline-r0-r1-rewrite`
**Scope (this researcher):** contracts SoT, the 4 tool-write schemas, the tool_writer/executor runtime path that validates roadmap_ids, arch_lint scan scope.
**Status:** In Progress

All line numbers verified by direct `Read` of files on 2026-06-02. Other researchers cover: intentional-vs-drift git investigation; guard tests + fixtures; MDTM template — NOT duplicated here.

---

## 1. The SoT — `src/superclaude/contracts/__init__.py`

### 1.1 `ID_PATTERNS` dict — exact bodies + ordering

Defined at **`src/superclaude/contracts/__init__.py:64-77`** (the `Final[dict[str, str]]` declaration spans those lines). Verbatim bodies and ordering:

| Order | Family | Body (verbatim regex) | Line |
|---|---|---|---|
| 1 | `MD` | `M\d+-D-?\d+` | 71 |
| 2 | `FR` | `FR-\d+(?:\.\d+)?` | 72 |
| 3 | `NFR` | `NFR-\d+(?:\.\d+)?` | 73 |
| 4 | `SC` | `SC-\d+` | 74 |
| 5 | `G` | `G-\d+` | 75 |
| 6 | `D` | `D-?\d+` | 76 |

- **6 families**, anchor-free bodies (no `\b…\b` — comment at `:59-62` documents that consumers wrap at compile time).
- **MD ordered BEFORE D** is deliberate (comment `:65-70`): "MD ordered BEFORE D … milestone-prefixed deliverable IDs (M{n}-D{nn}) form their own family rather than being silently collapsed under the bare-D family." Ported from PR #111 / commit `861047c2`.
- **The MD⊂D substring trap is real and confirmed:** `D-?\d+` (the `D` body) is a literal substring of `M\d+-D-?\d+` (the `MD` body). Any substring-containment guard test will FALSELY PASS for `MD`. This is the central correctness hazard the task must defeat with arm-level/exact matching.
- `NFR` body is the broader `NFR-\d+(?:\.\d+)?` (sub-ID variant), intentional per header comment `:52-56`.

### 1.2 `__all__` export list

At **`src/superclaude/contracts/__init__.py:209-217`**:

```python
__all__ = [
    "ID_PATTERNS",
    "CONVERGENCE_THRESHOLDS",
    "GATE_FIELD_NAMES",
    "THRESHOLDS",
    "UnaddressedInvariant",
    "AdversarialReturn",
    "RETURN_CONTRACTS",
]
```

A new family-set SoT constant + `roadmap_ids_pattern()` assembler (per the BUILD-REQUEST DESIGN DECISION option (a)) must be **appended here** so arch_lint's `__all__` discovery picks it up automatically (see §6).

### 1.3 Existing assembler/helper for patterns — NONE

- **Confirmed: there is NO `roadmap_ids_pattern()` helper today.** `grep -n "roadmap_ids_pattern\|def .*pattern\|join(" src/superclaude/contracts/__init__.py` → no function defs; the module is pure data (`ID_PATTERNS`, `CONVERGENCE_THRESHOLDS`, `GATE_FIELD_NAMES`, `THRESHOLDS`) plus two dataclasses (`UnaddressedInvariant`, `AdversarialReturn`) and one registry (`RETURN_CONTRACTS`).
- **No existing constant for tool-write-only families** (`DM/API/COMP/TEST/MIG/OPS/OQ`) exists anywhere in `contracts/`. This is the new SoT surface the task creates.
- There is no `^(...)$` wrap helper anywhere in the module — the anchor-free→anchored wrap is currently each consumer's responsibility (e.g. `spec_parser` wraps with `\b…\b`). The new assembler must do the `^(` + `|`.join + `)$` wrap deterministically.

---

## 2. The 4 tool-write schemas — exact `roadmap_ids.items.pattern`

All four live under `src/superclaude/cli/roadmap/templates/tool_schemas/`. JSON path to the pattern in every file: **`properties.roadmap_ids.items.pattern`**. Verbatim strings (as stored in JSON, i.e. with `\\d` double-backslash escaping; the effective regex is single-backslash):

### 2.1 `generate.schema.json:140`
JSON-escaped:
```
^(FR-\\d+(?:\\.\\d+)?|NFR-\\d+(?:\\.\\d+)?|SC-\\d+|G-\\d+|D-?\\d+|DM-\\w+|API-\\w+|COMP-\\w+|TEST-\\w+|MIG-\\w+|OPS-\\w+|OQ-\\w+)$
```
Effective regex families (in order): `FR, NFR, SC, G, D, DM, API, COMP, TEST, MIG, OPS, OQ` (12 arms).

### 2.2 `merge.schema.json:156`
JSON-escaped — **byte-identical to generate**:
```
^(FR-\\d+(?:\\.\\d+)?|NFR-\\d+(?:\\.\\d+)?|SC-\\d+|G-\\d+|D-?\\d+|DM-\\w+|API-\\w+|COMP-\\w+|TEST-\\w+|MIG-\\w+|OPS-\\w+|OQ-\\w+)$
```
Same 12 arms as generate. (A guard test pins merge==generate per BUILD-REQUEST; other researcher covers test files.)

### 2.3 `extract.schema.json:134`
JSON-escaped:
```
^(FR-\\d+(?:\\.\\d+)?|NFR-\\d+(?:\\.\\d+)?|SC-\\d+|G-\\d+|D-?\\d+|COMP-\\w+|DM-\\w+)$
```
Families (in order): `FR, NFR, SC, G, D, COMP, DM` (7 arms). **Note the ordering anomaly: `COMP` before `DM`** here, whereas generate/merge/extract_tdd list `DM` before `COMP`. **Omits** `API, TEST, MIG, OPS, OQ`.

### 2.4 `extract_tdd.schema.json:218`
JSON-escaped:
```
^(FR-\\d+(?:\\.\\d+)?|NFR-\\d+(?:\\.\\d+)?|SC-\\d+|G-\\d+|D-?\\d+|DM-\\w+|API-\\w+|COMP-\\w+|TEST-\\w+|MIG-\\w+|OPS-\\w+)$
```
Families (in order): `FR, NFR, SC, G, D, DM, API, COMP, TEST, MIG, OPS` (11 arms). **Omits** `OQ` only.

### 2.5 Family-set membership matrix

| Family | SoT `ID_PATTERNS` | extract | extract_tdd | generate | merge |
|---|:---:|:---:|:---:|:---:|:---:|
| FR | ✓ | ✓ | ✓ | ✓ | ✓ |
| NFR | ✓ | ✓ | ✓ | ✓ | ✓ |
| SC | ✓ | ✓ | ✓ | ✓ | ✓ |
| G | ✓ | ✓ | ✓ | ✓ | ✓ |
| D | ✓ | ✓ | ✓ | ✓ | ✓ |
| **MD** | ✓ | **✗** | **✗** | **✗** | **✗** |
| DM | ✗ | ✓ | ✓ | ✓ | ✓ |
| API | ✗ | ✗ | ✓ | ✓ | ✓ |
| COMP | ✗ | ✓ | ✓ | ✓ | ✓ |
| TEST | ✗ | ✗ | ✓ | ✓ | ✓ |
| MIG | ✗ | ✗ | ✓ | ✓ | ✓ |
| OPS | ✗ | ✗ | ✓ | ✓ | ✓ |
| OQ | ✗ | ✗ | ✗ | ✓ | ✓ |

**Key findings:**
- **ALL FOUR schemas omit `MD`** — confirmed by inspection of each `pattern` string (none contains `M\d+-D` / `M\\d+-D`). This is the genuine missing-family bug the task closes (a `M1-D01` roadmap_id is currently rejected at schema validation in tool-write mode).
- **The 5 spec families FR/NFR/SC/G/D are present in all four** schemas (and match the SoT bodies verbatim, including `D-?\d+` and the `(?:\.\d+)?` sub-ID tails).
- **Inter-schema differences (precise):**
  - `generate` ≡ `merge` (12 arms, identical, OQ included).
  - `extract_tdd` = generate minus `OQ` (11 arms).
  - `extract` = the smallest set: only `COMP` + `DM` of the tool-write-only families (7 arms); omits `API/TEST/MIG/OPS/OQ`; and lists `COMP` before `DM` (reversed order vs the others).
- The per-schema H3/content sections corroborate the difference: `extract_tdd` defines `data_models`, `api_specifications`, `testing_strategy`, `migration_plan`, `operational_readiness` (hence DM/API/TEST/MIG/OPS), while `extract` defines only `component_inventory` (hence COMP) + `data_models`-less surface. `extract` has no `data_models`/`api`/`testing`/`migration`/`operational` arrays — yet its pattern still allows `DM` (a minor inconsistency; the intentional-vs-drift researcher should weigh this). **Unverified by me:** whether these differences are intentional per-step semantics or drift — that is the other researcher's git/`$comment` investigation. I only record the observable difference.

---

## 3. Tool-write-only family bodies — exact regex fragments (as they appear in the schemas)

Extracted verbatim from the schema `pattern` strings (effective single-backslash form):

| Family | Regex fragment (in schema) | First appears in |
|---|---|---|
| `DM` | `DM-\w+` | extract, extract_tdd, generate, merge |
| `API` | `API-\w+` | extract_tdd, generate, merge |
| `COMP` | `COMP-\w+` | extract, extract_tdd, generate, merge |
| `TEST` | `TEST-\w+` | extract_tdd, generate, merge |
| `MIG` | `MIG-\w+` | extract_tdd, generate, merge |
| `OPS` | `OPS-\w+` | extract_tdd, generate, merge |
| `OQ` | `OQ-\w+` | generate, merge only |

All seven use the uniform `<PREFIX>-\w+` shape (distinct from the spec families' `\d+`-anchored bodies). These are the families the BUILD-REQUEST's decision-gate grep confirmed are REAL (55 fixture usages) — REMOVE is OFF. They are the candidate contents of a new `TOOL_WRITE_EXTRA_ID_FAMILIES` SoT constant (DESIGN DECISION option (a)).

---

## 4. Runtime path — `src/superclaude/cli/roadmap/tool_writer.py`

### 4.1 `load_schema` (`:67-91`)
- Resolves `schema_path = TOOL_SCHEMAS_DIR / name` where `TOOL_SCHEMAS_DIR = TEMPLATES_DIR / "tool_schemas"` (`:38`).
- Raises `FileNotFoundError` if missing (`:86-90`).
- **Loads via `json.loads(schema_path.read_text(encoding="utf-8"))` (`:91`)** — so any assembler-generated pattern must be written into the JSON files on disk; nothing is computed at load time. The schema pattern is therefore a build-time artifact, and a regeneration step (or a test that asserts on-disk == assembler output) is the durable-guard surface.

### 4.2 `validate_tool_output` (`:94-117`)
- Imports `jsonschema.validators` (`:105`), auto-selects the draft via `validators.validator_for(schema)` (`:107-108`), iterates `validator.iter_errors(tool_output)` (`:111-114`), returns a list of `"<json-path>: <message>"` error strings; **empty list == PASS**.
- **This is where the `roadmap_ids.items.pattern` regex is enforced** by jsonschema. A `roadmap_id` not matching the schema pattern produces an error here → the array element fails `pattern` validation.

### 4.3 `validate_id_subset` (`:344-370`)
- Pure set check: `allowed = set(spec_ids) | set(accepted_deviations or [])` (`:365`); returns one error per `rid not in allowed` (`:366-369`). **No regex** — purely membership of the already-parsed roadmap_ids against the spec universe.

### 4.4 Order: schema-validate BEFORE subset (CONFIRMED)
Front half is shared via `_parse_and_validate` (`:373-403`):
1. registry lookup (`:390-392`),
2. `json.loads` (`:394-397`),
3. `schema = load_schema(spec.schema_name)` (`:399`),
4. `errors = validate_tool_output(parsed, schema)` (`:400`) → **if errors, short-circuit `return spec, parsed, errors` (`:401-402`) — NO subset check, NO write.**

`render_step_tool_write_with_id_check` (`:455-496`):
- calls `_parse_and_validate` first (`:481`); if errors → `return errors` immediately (`:482-483`).
- **only then** runs `validate_id_subset` (guarded by `if spec_ids:`, `:487-493`).
- `_persist_and_render` (writes sidecar + markdown) runs **last**, only if both gates pass (`:495`).

**Conclusion (answers task item 4):** A `roadmap_id` that does NOT match the schema `pattern` is **rejected at `validate_tool_output` (the schema gate) BEFORE the subset check ever runs.** Therefore today, because all four schemas omit `MD`, a roadmap carrying `M1-D01` is rejected at schema validation in tool-write mode — exactly the bug. Adding `MD` to the schema pattern lets it pass the schema gate; the subset gate then independently constrains it to the spec universe. The two gates are orthogonal: schema = SHAPE, subset = SET-membership.

---

## 5. Executor wiring — `src/superclaude/cli/roadmap/executor.py`

Re-anchored by symbol (`render_step_tool_write_with_id_check`), not by stale line number.

- Imports both back-ends at **`:1235-1239`** (inside `if isinstance(config, RoadmapConfig):` block).
- Registry-key resolution at **`:1248-1254`**: `step.id == "extract" && config.input_type == "tdd"` → `"extract_tdd"`; `step.id.startswith("generate-")` → `"generate"`; else `step.id`.
- **The id-checked render is wired for `generate`/`merge` at `:1267-1294`:** `if _tw_key in ("generate", "merge"):` derives `_spec_ids` from the `extraction.json` sidecar (`:1278-1287`), then calls **`render_step_tool_write_with_id_check(_tw_key, _json_text, step.output_file, spec_ids=_spec_ids, accepted_deviations=None)` at `:1288-1294`.**
- The **else** branch (extract / extract_tdd) calls plain `render_step_tool_write` at `:1296-1298` (no subset check — extract DEFINES the universe, so subset is the identity).
- Both branches feed `_tw_errors`; non-empty → `StepResult(status=FAIL, …)` at `:1299-1308`.

So generate + merge are the two steps where the schema-pattern regex AND the subset gate both fire; extract + extract_tdd run schema-only. All four schemas' `roadmap_ids.items.pattern` is live (schema gate fires for all four).

---

## 6. arch_lint scope — `src/superclaude/tools/arch_lint.py` (the gap this task closes)

- **Scans only `.py`:** `_iter_python_files` (`:94-100`) yields `root` only if `root.suffix == ".py"` (`:97-98`) or, for dirs, `root.rglob("*.py")` (`:100`). **JSON schemas are never visited.** Confirmed.
- **Builds `canonical_pattern_bodies` from `ID_PATTERNS.values()`:** `_load_canonical_constants` (`:81-91`) does `id_patterns = getattr(module, "ID_PATTERNS", {})` (`:89`) then `canonical_pattern_bodies = set(id_patterns.values())` (`:90`). Rule 2 (`:194`, `:205`) flags any `.py` string literal whose value is in `canonical_pattern_bodies` (i.e. a re-inlined `ID_PATTERNS` body) unless allow-marked.
- **Implication / the gap:** arch_lint enforces "no `.py` re-inlines a SoT body" but is **blind to the JSON schemas** — the schema `roadmap_ids` patterns can drift from the SoT freely and arch_lint will never notice. This is precisely why the durable fix must add **guard tests** (Python tests that import `ID_PATTERNS` + the new family-set SoT, assemble the expected pattern, and assert the on-disk schema patterns match arm-by-arm). arch_lint cannot be the enforcement surface for JSON; the guard tests are. (The guard-test rebuild is the other researcher's scope; this researcher only confirms the arch_lint blind spot.)
- Note: the SoT bodies are anchor-free; the schema arms are the SAME bodies wrapped in `^(…|…)$`. A naive arch_lint extension to JSON would also have to account for the wrap — another reason the JSON guard belongs in dedicated pytest, not arch_lint.

---

## Summary (Status: Complete)

**SoT (`contracts/__init__.py`):** `ID_PATTERNS` (`:64-77`) = 6 anchor-free families `MD, FR, NFR, SC, G, D`, MD ordered before D (`MD = M\d+-D-?\d+`, `D = D-?\d+` — MD⊂D substring trap confirmed). `__all__` at `:209-217`. **No `roadmap_ids_pattern()` assembler and no tool-write-only family constant exist yet** — both are new surfaces the task creates; append the new constant + helper to `__all__`.

**4 schemas (`templates/tool_schemas/`):** pattern lives at `properties.roadmap_ids.items.pattern` in each. generate(`:140`) ≡ merge(`:156`) = 12 arms (incl OQ); extract_tdd(`:218`) = 11 arms (omits OQ); extract(`:134`) = 7 arms (only COMP+DM extras, COMP-before-DM order anomaly). **ALL FOUR OMIT `MD`** — the genuine bug; `M1-D01` is rejected at schema validation in tool-write mode. The 5 spec families FR/NFR/SC/G/D are present + match SoT bodies verbatim in all four.

**Tool-write-only family fragments:** `DM-\w+`, `API-\w+`, `COMP-\w+`, `TEST-\w+`, `MIG-\w+`, `OPS-\w+`, `OQ-\w+` (uniform `<PREFIX>-\w+`). Real (55 fixture usages per BUILD-REQUEST) — REMOVE is off; candidates for a new `TOOL_WRITE_EXTRA_ID_FAMILIES` SoT.

**Runtime (`tool_writer.py`):** `load_schema` `json.loads` from disk (`:91`) — patterns are on-disk artifacts. Order is `_parse_and_validate` → schema-validate (`validate_tool_output`, jsonschema, `:400`) → THEN subset (`validate_id_subset`, `:489`) → THEN persist+render. **Schema gate fires before subset — a roadmap_id not matching the schema pattern is rejected at `validate_tool_output` before subset is reached.** Confirmed.

**Executor (`executor.py`):** id-checked render wired for generate/merge at `:1288` (`render_step_tool_write_with_id_check`, spec_ids from `extraction.json` sidecar); extract/extract_tdd use plain `render_step_tool_write` (`:1296`).

**arch_lint (`arch_lint.py`):** scans `.py` only (`rglob("*.py")`, `:100`); `canonical_pattern_bodies` from `ID_PATTERNS.values()` (`:90`). **JSON schemas NOT covered** — the unguarded-drift gap the task closes via dedicated guard tests (not arch_lint).

**Net design implication:** BUILD-REQUEST option (a) is well-supported — add `TOOL_WRITE_EXTRA_ID_FAMILIES` (or `ROADMAP_ID_FAMILIES`) + `roadmap_ids_pattern()` assembler to `contracts`, export in `__all__`, regenerate all four schema patterns (MD lands here), and add pytest guards doing arm-level (NOT substring) comparison to defeat the MD⊂D trap, iterating the live family set. Per-step difference (extract's reduced set, extract_tdd's missing OQ) intentional-vs-drift is OUT of this researcher's scope (git/`$comment` researcher), but the assembler design must be capable of per-step sets if the answer is "intentional."
