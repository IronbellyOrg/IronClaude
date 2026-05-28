# Research: File Inventory
**Topic type:** File Inventory
**Scope:** integration_contracts.py + test_integration_contracts.py
**Status:** Complete
**Date:** 2026-05-25
---

## Files Touched by Fix B Merged Refactor

Two files in scope:
- `src/superclaude/cli/roadmap/integration_contracts.py` (357 lines)
- `tests/roadmap/test_integration_contracts.py` (277 lines)

Legend for "Refactor disposition":
- **MODIFIED** = body changed by merged-output.md §2.1–§2.4
- **REFERENCED** = relied on by new logic but body unchanged
- **UNTOUCHED** = neither modified nor newly referenced
- **NEW** = added by the refactor

---

## Section A — `src/superclaude/cli/roadmap/integration_contracts.py`

### A.1 Module-level constants (compiled regex patterns)

| Element | Lines | Purpose | Refactor disposition |
|---|---|---|---|
| `DISPATCH_PATTERNS` (list) | 20-73 | List of 8 compiled regexes for dispatch-pattern categories scanned by `extract_integration_contracts`. | **MODIFIED** — index [0] rewritten per §2.2; indices [1]–[7] unchanged. |
| `DISPATCH_PATTERNS[0]` — Category 1 dict dispatch tables | 22-27 | Regex matching `dispatch[_\s]?table`, `RUNNERS`, `_RUNNERS`, `HANDLERS`, bare `DISPATCH`, `routing[_\s]?table`, `command[_\s]?map`, `step[_\s]?map`, `plugin[_\s]?registry`. | **MODIFIED** (§2.2): drop bare `DISPATCH`, add explicit `DISPATCH_TABLE`, add compound-noun arm for `(?:[a-z]+-)?(?:class-priority|priority|named-theme|role-keyed|theme|severity-keyed|module-tier|subprocess|gRPC)[\s_-]?dispatch`. |
| `DISPATCH_PATTERNS[1]` — Category 2 plugin registry/explicit wiring | 29-34 | Verb+noun regex (`populate`/`register`/`wire`/`inject`/`bind`/`map`/`route` + `implementations`/`runners`/…). | REFERENCED (unchanged). |
| `DISPATCH_PATTERNS[2]` — Category 3 callback injection | 36-40 | Regex for `(accepts|takes|requires|expects) a (Callable|Protocol|ABC|Interface|Factory|Provider|Registry)`. | REFERENCED. |
| `DISPATCH_PATTERNS[3]` — Category 3 type annotations for dispatch | 42-45 | Regex for `Dict[str, Callable]`-style annotations. | REFERENCED. |
| `DISPATCH_PATTERNS[4]` — Category 4 Strategy pattern (code-specific) | 49-54 | Regex for `Context(strategy=`, `ConcreteStrategy`, `set_strategy`, `get_strategy`, `StrategyPattern`, `strategy_registry`, `STRATEGY_MAP`, `AbstractStrategy`. | REFERENCED. |
| `DISPATCH_PATTERNS[5]` — Category 5 middleware chain | 56-60 | Regex for `middleware`, `app.use`, `pipeline.add`, `add_middleware`, `use_middleware`. | REFERENCED. |
| `DISPATCH_PATTERNS[6]` — Category 6 event binding | 62-66 | Regex for `emitter.on`, `addEventListener`, `subscribe`, `on_event`, `event_handler`, `add_listener`. | REFERENCED. |
| `DISPATCH_PATTERNS[7]` — Category 7 DI container | 68-72 | Regex for `container.bind`, `container.register`, `Provider`, `Injector`, `inject_dependency`, `DependencyContainer`. | REFERENCED. |
| `WIRING_TASK_PATTERNS` (list) | 76-107 | List of 4 compiled regexes for verb-anchored wiring task coverage; iterated in `check_roadmap_coverage`. | UNTOUCHED. Contents stay verbatim. |
| `WIRING_TASK_PATTERNS[0]` — explicit creation/population | 78-85 | Regex for `create|build|...register` + `dispatch|routing|...` + `table|map|...`. | UNTOUCHED. |
| `WIRING_TASK_PATTERNS[1]` — explicit wiring into mechanisms | 87-93 | Regex for `wire|connect|bind|...` + implementations/runners/… + `into|to|with|in`. | UNTOUCHED. |
| `WIRING_TASK_PATTERNS[2]` — named mechanism constants | 95-98 | Regex for literal tokens `PROGRAMMATIC_RUNNERS`, `DISPATCH_TABLE`, `HANDLER_REGISTRY`, `MIDDLEWARE_CHAIN`, `EVENT_BINDINGS`, `ROUTE_MAP`. | UNTOUCHED. |
| `WIRING_TASK_PATTERNS[3]` — strategy/middleware/event setup verbs | 100-106 | Regex for `configure|set up|initialize|bootstrap` + mechanism nouns. | UNTOUCHED. |

### A.2 Dataclasses

| Element | Lines | Purpose | Refactor disposition |
|---|---|---|---|
| `IntegrationContract` (dataclass) | 113-122 | Holds a single integration point with fields `id: str`, `mechanism: str`, `spec_evidence: str`, `spec_location: str`, `description: str`, `requires_explicit_wiring: bool`. | **MODIFIED** (§2.1): add new field `mechanism_signature: tuple[str, frozenset[str]] = field(default=(("", frozenset())))`. Must remain backward-compat for direct constructors. |
| `WiringCoverage` (dataclass) | 125-132 | Holds `contract: IntegrationContract`, `covered: bool`, `roadmap_evidence: str`, `roadmap_location: str`. | UNTOUCHED. Carries the modified `IntegrationContract` transitively. |
| `IntegrationAuditResult` (dataclass) | 135-147 | Holds `contracts: list[IntegrationContract]`, `coverage: list[WiringCoverage]`, `uncovered_count: int = 0`, `total_count: int = 0`; plus `all_covered` property. | UNTOUCHED. |
| `IntegrationAuditResult.all_covered` (property) | 144-147 | Returns `self.uncovered_count == 0`. | UNTOUCHED. |

### A.3 Public API functions

| Element | Lines | Signature | Refactor disposition |
|---|---|---|---|
| `extract_integration_contracts(spec_text)` | 153-202 | `def extract_integration_contracts(spec_text: str) -> list[IntegrationContract]` — scans spec text via `DISPATCH_PATTERNS`, dedups by raw evidence line, emits sequential IC-### IDs. | **MODIFIED** (§2.3): replace per-evidence-line dedup with signature-based dedup using new helper `_signature_subsumed`; compute `idents = frozenset(_extract_identifiers(context))`, build `signature = (mechanism, idents)`, persist via new `mechanism_signature=` constructor arg; add `break` after appending so one contract per line max. |
| `check_roadmap_coverage(contracts, roadmap_text)` | 205-311 | `def check_roadmap_coverage(contracts: list[IntegrationContract], roadmap_text: str) -> IntegrationAuditResult` — three-tier coverage check: WIRING_TASK_PATTERNS → identifier matching → FR-MOD2.7 broad mechanism-term + impl-verb fallback. | **MODIFIED** (§2.4): rewrite the FR-MOD2.7 fallback block (lines 261-297) into 3 layers — Layer 1 dispatch-family regex, Layer 2 existing literal-term + 3-line-window check, Layer 3 NEW generic stem-fallback constrained by identifier-overlap against `contract.mechanism_signature[1]`. Also add `populate` to `impl_verbs` alternation. |

Sub-blocks inside `check_roadmap_coverage` worth listing separately because they're touched independently:

| Sub-block | Lines | Behavior | Disposition |
|---|---|---|---|
| Initialization + WIRING_TASK_PATTERNS loop | 218-239 | Builds `IntegrationAuditResult`, iterates wiring patterns. | UNTOUCHED. |
| FR-MOD2.4 identifier matching | 241-252 | Calls `_extract_identifiers(contract.spec_evidence)` and substring-matches. | UNTOUCHED. |
| FR-MOD2.7 broad mechanism + impl_verbs fallback | 254-297 | Builds `raw_terms`, compiles `impl_verbs`, scans roadmap with same-line + 3-line window. | **MODIFIED** (§2.4): expanded into 3 layers (see above). `impl_verbs` regex (currently lines 270-275) gains `populate`. |
| Append `WiringCoverage` + bump uncovered_count | 299-309 | Appends result row, increments `uncovered_count` when not covered. | UNTOUCHED. |
| Return result | 311 | `return result`. | UNTOUCHED. |

### A.4 Internal helpers

| Element | Lines | Signature | Refactor disposition |
|---|---|---|---|
| `_classify_mechanism(matched_text)` | 317-344 | `def _classify_mechanism(matched_text: str) -> str` — maps regex-matched text to one of `dispatch_table`, `registry`, `dependency_injection`, `explicit_wiring`, `routing`, `strategy_pattern`, `middleware_chain`, `event_binding`, `di_container`, or fallback `integration_point`. | UNTOUCHED (used by refactored extractor). |
| `_extract_identifiers(text)` | 347-356 | `def _extract_identifiers(text: str) -> list[str]` — returns concat of `UPPER_SNAKE_CASE` (`[A-Z][A-Z0-9_]{2,}`) and PascalCase (`[A-Z][a-z]+(?:[A-Z][a-z]+)+`) regex matches. | REFERENCED (now called with `context` not `spec_evidence`; output feeds `frozenset` for `mechanism_signature`). Note the secondary counter-argument in §6 of merged-output.md: single-PascalCase tokens like `Interactive`/`Bulk` do NOT match the multi-cap PascalCase regex — out of scope but flagged. |
| `_signature_subsumed(sig, seen)` | NEW | `def _signature_subsumed(sig: tuple[str, frozenset[str]], seen: dict[tuple[str, frozenset[str]], int]) -> bool` — returns True if `sig` shares mechanism with a seen sig AND its identifier-set is a subset that shares ≥1 identifier; falls back to exact-match dedup for empty-identifier sigs. | **NEW** (§2.3). Body specified verbatim in merged-output.md lines 144-161. |

### A.5 Module-level imports / file header

| Element | Lines | Purpose | Refactor disposition |
|---|---|---|---|
| Module docstring | 1-11 | Describes module, references FR-MOD2.1 through FR-MOD2.6. | UNTOUCHED. (Optional polish: bump to FR-MOD2.7 — not required by spec.) |
| `from __future__ import annotations` | 13 | Postponed evaluation for type hints. | UNTOUCHED. |
| `import re` | 15 | Used by all regex compilation. | UNTOUCHED. |
| `from dataclasses import dataclass, field` | 16 | Used by all 3 dataclasses; `field` newly load-bearing for `mechanism_signature` default. | REFERENCED. |
| Section comments (`# --- FR-MOD2.x ---`) | 18, 75, 110, 150, 314 | Visual separators. | UNTOUCHED. |

---

## Section B — `tests/roadmap/test_integration_contracts.py`

### B.1 Imports

| Element | Lines | Purpose | Refactor disposition |
|---|---|---|---|
| `from superclaude.cli.roadmap.integration_contracts import (IntegrationAuditResult, check_roadmap_coverage, extract_integration_contracts)` | 12-16 | Pulls the public API. | UNTOUCHED. New test class `TestHubDispatchRegression` uses these same symbols. |

### B.2 Module-level string fixtures (test corpus)

All are `str` constants used by multiple test methods. None edited; t6/t7 in §3 of merged-output.md define new inline-string fixtures within the test methods themselves.

| Fixture | Lines | First line / description | Disposition |
|---|---|---|---|
| `DISPATCH_TABLE_SPEC` | 20-26 | `"The executor uses a PROGRAMMATIC_RUNNERS dispatch table that maps step IDs..."` — used by category-1 + regression + new t4. | REFERENCED by new t4. |
| `REGISTRY_SPEC` | 28-31 | `"Components register themselves via plugin_registry.register()..."`. | UNTOUCHED. |
| `CALLBACK_INJECTION_SPEC` | 33-36 | `"The executor accepts a Callable for step processing..."`. | UNTOUCHED. |
| `STRATEGY_SPEC` | 38-41 | `"Use the Strategy pattern: Context(strategy=ConcreteStrategy())..."`. | UNTOUCHED. |
| `MIDDLEWARE_SPEC` | 43-46 | `"Configure middleware chain: app.use(auth_middleware)..."`. | UNTOUCHED. |
| `EVENT_BINDING_SPEC` | 48-51 | `"Events are bound via emitter.on('change', handler)..."`. | UNTOUCHED. |
| `DI_CONTAINER_SPEC` | 53-56 | `"Dependencies registered with container.bind(Service, impl)..."`. | UNTOUCHED. |
| `ALL_CATEGORIES_SPEC` | 58-72 | Concatenation of all category specs above (joined with `"\n"`). | REFERENCED (used by deduplication test; behavior must still pass per §4 backward-compat matrix). |
| `GOOD_ROADMAP` | 74-84 | `"## Phase 1: Setup\\n\\nCreate the dispatch table for step routing..."`. | REFERENCED (covered-roadmap test must still pass). |
| `BAD_ROADMAP` | 86-95 | `"## Phase 1: Setup\\n\\nSet up project structure..."`. | REFERENCED (uncovered-roadmap test must still pass — no dispatch-family or stem+overlap hits). |
| `CLI_PORTIFY_SPEC` | 97-111 | `"Three-way dispatch: _run_programmatic_step(), _run_claude_step(), _run_convergence_step()..."` — multi-line code-fenced PROGRAMMATIC_RUNNERS dict. | REFERENCED by new t5. |
| `CLI_PORTIFY_BAD_ROADMAP` | 113-127 | `"## Phase 1: Foundation\\n\\nSet up project structure and configuration..."`. | REFERENCED by new t5. |

**New fixtures from §3** (defined at module scope before `TestHubDispatchRegression`):
- `TUIBBS_HUB_SPEC` — 30-40 line excerpt from real epics.md lines 200, 249, 373, 430, 1001, 1031 concatenated with 3-line windows. Note: user did NOT specify identifier-set contents — researcher to flag.
- `TUIBBS_HUB_ROADMAP` — excerpt from roadmap.md lines 392, 396, 436.

### B.3 Test classes and methods

| Class / method | Lines | What it asserts | Disposition |
|---|---|---|---|
| `TestDispatchPatternDetection` (class) | 130-179 | FR-MOD2.1: 7-category dispatch detection. | REFERENCED — all 8 methods must remain green per §4 backward-compat matrix. |
| `.test_category1_dispatch_table` | 133-137 | `DISPATCH_TABLE_SPEC` yields ≥1 contract with mechanism `dispatch_table`. | REFERENCED (passes; explicit `DISPATCH_TABLE` arm + `dispatch[_\s]?table` arm cover this). |
| `.test_category2_plugin_registry` | 139-143 | `REGISTRY_SPEC` yields ≥1 contract with mechanism in `{registry, explicit_wiring}`. | REFERENCED. |
| `.test_category3_callback_injection` | 145-149 | `CALLBACK_INJECTION_SPEC` yields ≥1 contract with mechanism `dependency_injection`. | REFERENCED. |
| `.test_category4_strategy_pattern` | 151-155 | `STRATEGY_SPEC` yields ≥1 contract with mechanism `strategy_pattern`. | REFERENCED. |
| `.test_category5_middleware_chain` | 157-161 | `MIDDLEWARE_SPEC` yields ≥1 contract with mechanism `middleware_chain`. | REFERENCED. |
| `.test_category6_event_binding` | 163-167 | `EVENT_BINDING_SPEC` yields ≥1 contract with mechanism `event_binding`. | REFERENCED. |
| `.test_category7_di_container` | 169-173 | `DI_CONTAINER_SPEC` yields ≥1 contract with mechanism in `{di_container, dependency_injection}`. | REFERENCED. |
| `.test_all_categories_detected` | 175-179 | `ALL_CATEGORIES_SPEC` yields ≥4 distinct mechanisms. | REFERENCED. |
| `TestWiringCoverage` (class) | 182-208 | FR-MOD2.3, FR-MOD2.5: wiring coverage. | REFERENCED — all 4 methods must remain green. |
| `.test_covered_roadmap_passes` | 185-189 | `GOOD_ROADMAP` covers `DISPATCH_TABLE_SPEC` contracts. | REFERENCED. |
| `.test_uncovered_roadmap_fails` | 191-195 | `BAD_ROADMAP` does NOT cover `DISPATCH_TABLE_SPEC` contracts. | REFERENCED — Layer 3 stem-fallback must NOT regress this (no `Interactive`/`Coalescible`/`Bulk` identifiers in fixture). |
| `.test_empty_contracts_passes` | 197-200 | Empty contracts list → `all_covered`. | REFERENCED. |
| `.test_coverage_evidence_recorded` | 202-208 | Covered entries have non-empty `roadmap_evidence` / `roadmap_location`. | REFERENCED. |
| `TestDeduplication` (class) | 211-227 | FR-MOD2.2: dedup by evidence. | REFERENCED — critical case for §2.3 backward-compat. |
| `.test_duplicate_lines_deduplicated` | 214-222 | 3 identical lines → 1 contract. | REFERENCED. Key invariant: `_signature_subsumed` empty-identifier branch (`if not idents: return sig in seen`) preserves this exact-match behavior. |
| `.test_sequential_id_assignment` | 224-227 | Each contract's `id == f"IC-{i+1:03d}"` (positional within iteration). | REFERENCED — passes despite dedup reducing count; numbering of kept items is still sequential (§4 "soft risk" note). |
| `TestNamedMechanismMatching` (class) | 230-242 | FR-MOD2.4: named identifier matching. | REFERENCED. |
| `.test_upper_snake_case_detected` | 233-236 | `PROGRAMMATIC_RUNNERS` appears in extracted `spec_evidence`. | REFERENCED. |
| `.test_named_mechanism_in_roadmap_coverage` | 238-242 | Roadmap mentioning `PROGRAMMATIC_RUNNERS` covers `CLI_PORTIFY_SPEC` contracts. | REFERENCED. |
| `TestCliPortifyRegression` (class) | 245-260 | SC-003 regression. | REFERENCED. |
| `.test_detects_programmatic_runners_without_wiring` | 248-256 | `CLI_PORTIFY_BAD_ROADMAP` leaves PROGRAMMATIC_RUNNERS uncovered. | REFERENCED — must still fail coverage post-refactor. |
| `.test_total_contracts_detected` | 258-260 | `CLI_PORTIFY_SPEC` yields ≥1 contract. | REFERENCED. |
| `TestIntegrationAuditResult` (class) | 263-276 | FR-MOD2.6: `IntegrationAuditResult` properties. | UNTOUCHED. |
| `.test_all_covered_true_when_zero_uncovered` | 266-268 | `IntegrationAuditResult(uncovered_count=0, total_count=3).all_covered` is True. | UNTOUCHED. |
| `.test_all_covered_false_when_uncovered` | 270-272 | `IntegrationAuditResult(uncovered_count=1, total_count=3).all_covered` is False. | UNTOUCHED. |
| `.test_empty_result_is_covered` | 274-276 | Default `IntegrationAuditResult().all_covered` is True. | UNTOUCHED. |

### B.4 New test class — `TestHubDispatchRegression`

Per §3 of merged-output.md, append after `TestIntegrationAuditResult` (around line 277). Contains 7 new methods (t1–t7) plus 2 new fixtures.

| New element | Source ref | Purpose |
|---|---|---|
| `TUIBBS_HUB_SPEC` (fixture) | §3 line 290 | 30-40 line excerpt of TUIBBS-scp epics.md hub-dispatch blocks. Must include Interactive/Coalescible/Bulk identifiers in 3-line windows. |
| `TUIBBS_HUB_ROADMAP` (fixture) | §3 line 292 | Excerpt of roadmap.md hub block (lines 392/396/436). |
| `TestHubDispatchRegression` (class) | §3 lines 294-296 | Anti-instinct gate must produce 1 hub-dispatch contract not 4, and must find it covered. |
| `.test_t1_one_contract_per_hub_mechanism` | §3 lines 298-304 | 4 epic lines mentioning hub dispatch → 1 contract. Exercises §2.3 subsumption. |
| `.test_t2_class_priority_dispatch_covers_hub` | §3 lines 306-310 | Roadmap phrase 'class-priority dispatch' covers hub contract via §2.4 Layer 1. |
| `.test_t3_prose_dispatch_not_extracted_alone` | §3 lines 312-316 | 'priority dispatch cannot be undermined' prose → ≤1 contract (§2.2 over-capture guard). |
| `.test_t4_existing_dispatch_table_test_still_passes` | §3 lines 318-321 | `DISPATCH_TABLE_SPEC` still yields a `dispatch_table` contract (regression sentry). |
| `.test_t5_cli_portify_regression_still_blocks` | §3 lines 323-327 | SC-003 still produces `uncovered_count >= 1`. |
| `.test_t6_stem_fallback_with_ident_overlap_covers` | §3 lines 331-344 | Layer 3 stem-fallback + identifier overlap → covered. Inline `spec` / `roadmap` fixtures. |
| `.test_t7_stem_fallback_without_ident_overlap_uncovers` | §3 lines 346-361 | Layer 3 stem-fallback without identifier overlap → uncovered (false-positive guard). |

---

## Section C — Summary Table

| File | NEW | MODIFIED | REFERENCED | UNTOUCHED |
|---|---|---|---|---|
| `integration_contracts.py` | 1 helper (`_signature_subsumed`) | 4 elements (`DISPATCH_PATTERNS[0]`, `IntegrationContract` dataclass, `extract_integration_contracts`, `check_roadmap_coverage` FR-MOD2.7 sub-block) | 5 (other DISPATCH_PATTERNS entries, `_extract_identifiers`, `_classify_mechanism`, `WiringCoverage`, `field` import) | rest (module docstring, `IntegrationAuditResult`, `WIRING_TASK_PATTERNS`, section comments) |
| `test_integration_contracts.py` | 2 fixtures + 1 class + 7 methods | 0 (existing test bodies untouched) | 22 existing tests across 5 classes (must remain green per §4 matrix) | `TestIntegrationAuditResult` class + 3 methods |

### C.1 Critical invariants per merged-output.md §4 backward-compat matrix

These existing tests MUST remain green; failures = refactor broken:
1. All 8 `TestDispatchPatternDetection.*` — dispatch family + categories 2-7 detection.
2. All 4 `TestWiringCoverage.*` — covered/uncovered paths, especially `test_uncovered_roadmap_fails` (no false-positive from Layer 3).
3. Both `TestDeduplication.*` — exact-match dedup via `_signature_subsumed` empty-idents branch + sequential numbering of kept items.
4. Both `TestNamedMechanismMatching.*` — identifier-based coverage.
5. Both `TestCliPortifyRegression.*` — SC-003 still blocks.
6. All 3 `TestIntegrationAuditResult.*` — property logic untouched.

### C.2 Soft risks flagged for task builder

- `_signature_subsumed` empty-identifier branch (`if not idents: return sig in seen`) is the single load-bearing line for `test_duplicate_lines_deduplicated`. Any future edit to dedup logic must preserve this branch.
- `_extract_identifiers` does NOT match single-PascalCase tokens (`Interactive`, `Bulk`). If `TUIBBS_HUB_SPEC` fixture uses only single-PascalCase identifiers in code spans/backticks, `mechanism_signature[1]` will be empty for those contracts, and Layer 3 stem-fallback's identifier-overlap guard short-circuits (admits matches). User did NOT specify exact `TUIBBS_HUB_SPEC` identifier content — task builder should require the fixture to include at least one UPPER_SNAKE_CASE or multi-cap PascalCase token (e.g. `InteractiveClass`, `MESSAGE_CLASSES`) OR explicitly accept the looser behavior in t6.
- `extract_integration_contracts` signature-based dedup uses `context` (3-line window) for identifier extraction, NOT `evidence` (single line). This is per §2.3 verbatim. Task builder must use the exact source given in merged-output.md lines 96-141.
- `impl_verbs` regex must include `populate` per §2.4 (merged-output.md line 198 comment + line 262 rationale).
- `check_roadmap_coverage` per-mechanism early-`break` semantics for Layers 1/2 must be preserved during Layer-3 insertion.

---

## Summary

The refactor touches 1 new helper, 1 new dataclass field, 1 modified extractor function, 1 modified coverage function, 1 modified DISPATCH_PATTERNS entry, and 1 new test class with 2 fixtures and 7 tests. Existing test bodies remain untouched but constitute the backward-compatibility surface — 22 existing test methods across 6 classes must remain green. The single most fragile interaction is `_signature_subsumed`'s empty-identifier branch (preserves `test_duplicate_lines_deduplicated`), and the single under-specified area is the `TUIBBS_HUB_SPEC` / `TUIBBS_HUB_ROADMAP` fixture contents — particularly whether the identifiers in the 3-line windows will be captured by the current `_extract_identifiers` (which requires UPPER_SNAKE_CASE or multi-cap PascalCase).
