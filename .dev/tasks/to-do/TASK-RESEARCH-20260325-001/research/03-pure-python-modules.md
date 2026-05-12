# Research: Pure Python Analysis Modules

**Investigation type:** Code Tracer + Integration Mapper
**Scope:** spec_parser.py, fidelity_checker.py, integration_contracts.py, fingerprint.py, obligation_scanner.py
**Status:** Complete
**Date:** 2026-03-25

---

## Module: `spec_parser.py`

**File:** `src/superclaude/cli/roadmap/spec_parser.py`

### Exported functions
- `parse_frontmatter(text, warnings) -> dict[str, Any]`
- `extract_tables(text, warnings) -> list[MarkdownTable]`
- `extract_code_blocks(text, warnings) -> list[CodeBlock]`
- `extract_requirement_ids(text) -> dict[str, list[str]]`
- `extract_function_signatures(code_blocks) -> list[FunctionSignature]`
- `extract_literal_values(code_blocks) -> list[list[str]]`
- `extract_thresholds(text) -> list[ThresholdExpression]`
- `extract_file_paths(text) -> list[str]`
- `extract_file_paths_from_tables(tables) -> list[str]`
- `split_into_sections(text) -> list[SpecSection]`
- `parse_document(text) -> ParseResult`

### `parse_document()` output schema (ParseResult)
- `frontmatter: dict[str, Any]`
- `tables: list[MarkdownTable]`
- `code_blocks: list[CodeBlock]`
- `requirement_ids: dict[str, list[str]]`
- `function_signatures: list[FunctionSignature]`
- `literal_values: list[list[str]]`
- `thresholds: list[ThresholdExpression]`
- `file_paths: list[str]`
- `sections: list[SpecSection]`
- `warnings: list[ParseWarning]`

### YAML Frontmatter with TDD Schema
- `parse_frontmatter()` is generic — does NOT validate or normalize against a spec template schema
- Matches any `---...---` YAML block; falls back to line-by-line `key: value` extraction
- TDD frontmatter fields (`id`, `title`, `version`, `status`, `type`, `priority`, `autogen`, `coordinator`, `parent_doc`, `depends_on`, `tags`) will be extracted correctly

### Schema mismatch risks
- `ParseResult.frontmatter` is an untyped generic dict — no risk from parser itself
- `DIMENSION_SECTION_MAP` encodes spec-oriented section headings (e.g., "3. Functional Requirements", "4. File Manifest") — downstream code using this map may not map cleanly to TDD headings

### `extract_requirement_ids()` with TDD content
- Regex families: `FR-\d+(?:\.\d+)?`, `NFR-\d+(?:\.\d+)?`, `SC-\d+`, `G-\d+`, `D-?\d+`
- Scans entire text, deduplicates, sorts by family
- Will find TDD §5 FR-xxx IDs regardless of surrounding content — **compatible**

### TypeScript interface extraction
- `extract_code_blocks()` captures fenced blocks of ANY language — TypeScript blocks captured as `CodeBlock`
- `extract_function_signatures()` only parses blocks with language `python`, `py`, or empty string — **TypeScript `interface Foo {}` NOT extracted into function_signatures**
- No TypeScript interface semantic parser exists

### TDD compatibility: **PARTIAL** — basic parsing compatible; no TypeScript semantic extraction; spec-oriented section mapping risk

---

## Module: `fidelity_checker.py`

**File:** `src/superclaude/cli/roadmap/fidelity_checker.py`

### Exported functions
- `run_fidelity_check(spec_path, source_dir, allowlist=None) -> list[Finding]`

### Core behavior
Checks whether FRs in the spec have matching code evidence in the codebase.

FR extraction: `_FR_HEADING_RE` matches headings containing `FR-\d+(?:\.\d+)?`; also uses `parsed.requirement_ids.get("FR", [])` from `parse_document()`.

Name extraction patterns (from FR section text):
- Function: `` `name()` ``, `` `name` function ``
- Class: `` `Name` class ``, `class `Name``
- Code defs: `def Name`, `class Name`

### Evidence search
- Scans `.py` files ONLY via AST (`ast.FunctionDef`, `ast.AsyncFunctionDef`, `ast.ClassDef`) + regex fallback
- Exact name matching — no NLP, fuzzy, or semantic matching
- Fail-open: ambiguous matches treated as FOUND

### TDD §5 FR IDs
- Yes — TDD uses `FR-xxx` format; processed identically to spec FR IDs

### Hardcoded frontmatter field names
- No direct frontmatter field-name dependency found
- Uses `parsed.requirement_ids` only, not specific frontmatter keys

### TDD risks
- Evidence scanning is Python-only — TDD requirements implemented in TypeScript/other languages produce blind spots
- TDD sections with TypeScript interface names may produce ambiguous matches (fail-open)

### TDD compatibility: **PARTIAL** — FR IDs compatible; Python-only evidence search is a fundamental limitation for TDD content

---

## Module: `integration_contracts.py`

**File:** `src/superclaude/cli/roadmap/integration_contracts.py`

### Exported functions
- `extract_integration_contracts(spec_text) -> list[IntegrationContract]`
- `check_roadmap_coverage(contracts, roadmap_text) -> IntegrationAuditResult`

### All 7 DISPATCH_PATTERNS categories

| # | Category | Pattern Match Examples |
|---|---|---|
| 1 | Dict dispatch tables | `dispatch_table`, `RUNNERS`, `HANDLERS`, `DISPATCH`, `routing_table`, `command_map`, `plugin_registry` |
| 2 | Plugin registry / explicit wiring | `populate implementations`, `register handlers`, `wire plugins`, `inject commands`, `bind runners`, `route handlers` |
| 3 | Callback injection / constructor injection | `accepts a Callable`, `requires Protocol`, `expects Interface`, `takes Factory`, `Provider`, `Registry` |
| 4 | Type annotations for dispatch | `Dict[str, Callable`, `Mapping[str, Awaitable`, `dict[str, Coroutine` |
| 5 | Strategy pattern | `Context(strategy=`, `Strategy`, `set_strategy`, `get_strategy` |
| 6 | Middleware chain | `middleware`, `app.use`, `pipeline.add`, `add_middleware`, `use_middleware` |
| 7 | Event binding / DI container | `emitter.on`, `addEventListener`, `subscribe`, `on_event`, `container.bind`, `container.register`, `Injector`, `inject_dependency` |

### TDD §6 Architecture compatibility
- Likely YES — architecture prose describing registries, wiring, DI, middleware, event listeners, handler maps, callable/provider/protocol patterns will trigger patterns

### TDD §8 API Specifications compatibility
- Partial — plain endpoint tables (`GET /users`) will NOT trigger patterns
- API sections trigger only if they mention wiring mechanisms (handlers, middleware, route maps, DI)

### TDD compatibility: **MOSTLY YES** — format-agnostic; works on any text; architecture content fits well

---

## Module: `fingerprint.py`

**File:** `src/superclaude/cli/roadmap/fingerprint.py`

### Exported functions
- `extract_code_fingerprints(content) -> list[Fingerprint]`
- `check_fingerprint_coverage(spec_content, roadmap_content, min_coverage_ratio=0.7) -> tuple[int, int, list[str], float]`
- `fingerprint_gate_passed(spec_content, roadmap_content, min_coverage_ratio=0.7) -> bool`

### 3 extraction methods

| Method | Regex | Category | Min Length |
|---|---|---|---|
| Backtick identifiers | `` `([a-zA-Z_]\w*(?:\(\))?)` `` (strips `()`) | `"identifier"` | 4 chars |
| Code block definitions | `def|class \w+` inside fenced blocks | `"definition"` | — |
| ALL_CAPS constants | `\b([A-Z][A-Z_]{3,})\b` | `"constant"` | 4 chars via `{3,}` |

### `check_fingerprint_coverage()` return value
4-tuple: `(total: int, found: int, missing: list[str], ratio: float)`

### TypeScript interface names in backticks?
- YES — `` `UserProfile` ``, `` `AuthToken` `` (both ≥4 chars) would be extracted via backtick method
- TDD has MORE backtick identifiers than spec (TypeScript types, component names, endpoint constants)

### Endpoint paths extracted?
- NO — paths like `` `/users/{id}` ``, `` `GET /api/foo` `` do not match identifier regex (requires letter/underscore start + word chars only)
- API endpoint paths largely invisible to fingerprint extraction

### Is 0.7 threshold hardcoded?
- Default parameter `min_coverage_ratio=0.7` — **configurable** but defaulted
- `check_fingerprint_coverage()` calculates and returns the ratio; `fingerprint_gate_passed()` applies the threshold

### TDD impact on fingerprint coverage
- TDD with many backticked names and TypeScript constants likely produces MORE total fingerprints → possible improvement in coverage ratio
- Endpoint paths (a significant TDD artifact type) remain undetectable

### TDD compatibility: **MOSTLY YES** — format-agnostic; TDD may actually perform better on fingerprint extraction; endpoint paths are a gap

---

## Module: `obligation_scanner.py`

**File:** `src/superclaude/cli/roadmap/obligation_scanner.py`

### Exported functions
- `scan_obligations(content) -> ObligationReport`

### Confirmed scope
- Scans ROADMAP text only — never reads spec/TDD file
- Does not import `spec_parser`; has no spec file dependency

### `scan_obligations(roadmap_text)` returns `ObligationReport` with:
- `total_obligations`, `discharged`, `undischarged`
- `obligations: list[Obligation]` (phase, term, component, context, line_number, severity, discharged, exempt, discharge_phase, discharge_context)
- Properties: `undischarged_count`, `has_undischarged`

### TDD compatibility: **N/A** — roadmap-only scanner; completely unaffected by TDD input format

---

## Module Compatibility Table

| Module | TDD Compatible? | Risk Level | Changes Required | Notes |
|---|---|---|---|---|
| `spec_parser.py` | Partial | Medium | Likely yes for richer TDD support | Generic parsing works; no TS interface extraction; spec-oriented section mapping |
| `fidelity_checker.py` | Partial | High | Likely yes | FR IDs work; Python-only evidence scan is fundamental limitation |
| `integration_contracts.py` | Mostly yes | Low-Medium | Maybe | Architecture prose fits; plain API endpoint tables don't trigger patterns |
| `fingerprint.py` | Mostly yes | Low | Maybe | TDD's richer identifiers help; endpoint paths undetectable |
| `obligation_scanner.py` | N/A | Low | No | Roadmap-only; unaffected |

---

## Gaps and Questions

1. Downstream frontmatter consumers relying on spec-template field names were not investigated in this slice
2. TypeScript interface extraction is absent — `spec_parser.py` captures TS code blocks but does not semantically parse `interface Foo {}` definitions
3. API endpoint coverage is uneven — `integration_contracts.py` only catches API content when described as wiring/handlers/middleware; `fingerprint.py` does not extract URL paths
4. `DIMENSION_SECTION_MAP` reflects classic spec headings — may not map cleanly to TDD headings without adaptation

## Summary

The five modules are genuine pure-Python analyzers with varying TDD readiness:
- **Good TDD fit:** `integration_contracts.py` (text-driven), `fingerprint.py` (identifier-based), `obligation_scanner.py` (roadmap-only)
- **Usable but incomplete:** `spec_parser.py` (generic parsing works; no TS semantic extraction)
- **Most likely to require adaptation:** `fidelity_checker.py` (Python-only evidence scan blind to TypeScript/API TDD content)
