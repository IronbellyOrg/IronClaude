# Overlap Analysis: Anti-Instincts Gate (Primary)

**Date**: 2026-03-17
**Analyst scope**: Three spec files compared for redundancy, waste, and contradiction.

**File key**:
- **Wiring Verification**: `v3.0_fidelity-refactor_/wiring-verification-gate-v1.0-release-spec.md`
- **Anti-Instincts**: `v3.05_Anti-instincts_/anti-instincts-gate-unified.md` (PRIMARY)
- **Unified Audit Gating**: `v3.1_unified-audit-gating-v1.2.1/spec-refactor-plan-merged.md`

---

## 3x3 Overlap Matrix

|                        | Wiring Verification | Anti-Instincts | Unified Audit Gating |
|------------------------|:-------------------:|:--------------:|:--------------------:|
| **Wiring Verification** | N/A (self)         | 5/10 (50%)     | 4/10 (40%)           |
| **Anti-Instincts**      | 5/10 (50%)         | N/A (self)     | 3/10 (30%)           |
| **Unified Audit Gating**| 4/10 (40%)         | 3/10 (30%)     | N/A (self)           |

---

## Detailed Overlap Justification

### 1. Wiring Verification <-> Anti-Instincts: 5/10 (50%)

This is the highest overlap pair. Both specs respond to the same incident (cli-portify executor no-op bug) and target similar failure modes, but they operate at different pipeline stages and on different artifact types.

#### Overlap Instance 1.1: Unwired Registry / Dispatch Table Detection

**Wiring Verification** (Section 4.2.3, "Unwired Registry Analysis"):
> "Detect dictionary constants with naming patterns indicating dispatch registries (`REGISTRY`, `DISPATCH`, `RUNNERS`, `HANDLERS`, `ROUTER`) whose values reference functions that cannot be resolved via import."

**Anti-Instincts** (Section 5, Module 2: Integration Contract Extractor, `DISPATCH_PATTERNS`):
> Detection of "dispatch_table", "RUNNERS", "HANDLERS", "DISPATCH", "routing_table", "command_map", "step_map", "plugin_registry" patterns in spec text, with verification that each has a corresponding explicit wiring task in the roadmap.

**Why redundant**: Both detect the same class of integration failure -- dispatch tables/registries that are defined but not connected. They use similar regex patterns matching similar naming conventions (`RUNNERS`, `DISPATCH`, `HANDLERS`, `REGISTRY`).

**Why NOT fully redundant**: They operate on different artifacts at different pipeline stages. Wiring Verification runs **post-implementation** against Python source code (AST analysis of actual `.py` files). Anti-Instincts runs **pre-implementation** against spec and roadmap text (regex analysis of markdown). Wiring Verification catches bugs in code that was already written; Anti-Instincts prevents the roadmap from omitting the wiring task in the first place.

**Which is more complete**: Each is more complete in its own domain. Anti-Instincts covers 7 integration mechanism categories (dispatch tables, registries, callback injection, strategy pattern, middleware, events, DI containers) compared to Wiring Verification's 3 analyzers (unwired callables, orphan modules, unwired registries). However, Wiring Verification is concrete -- it analyzes actual code with AST parsing, while Anti-Instincts analyzes natural-language plans with regex.

#### Overlap Instance 1.2: Unwired Callable / Constructor Injection Detection

**Wiring Verification** (Section 4.2.1, "Unwired Callable Analysis"):
> "Detect constructor parameters typed `Optional[Callable]` (or `Callable | None`) with default `None` that are never explicitly provided at any call site in the codebase."

**Anti-Instincts** (Section 5, `DISPATCH_PATTERNS` Category 3):
> Pattern matching `accepts?|takes?|requires?|expects?` followed by `Callable|Protocol|ABC|Interface|Factory|Provider|Registry` in spec text.

**Why redundant**: Both detect the same root cause from the forensic report -- the `step_runner: Optional[Callable] = None` pattern in `PortifyExecutor`. Both specifically cite this as their motivating example.

**Why NOT fully redundant**: Same distinction as 1.1. Wiring Verification detects the bug in actual Python code via AST parsing. Anti-Instincts detects that the roadmap failed to include a wiring task for an injectable dependency described in the spec. They are defense-in-depth at different pipeline stages.

**Which is more complete**: Wiring Verification is more precise for this specific pattern (AST-based, exact parameter matching, call-site verification). Anti-Instincts is broader but less precise (regex on natural language).

#### Overlap Instance 1.3: Orphan Module Detection

**Wiring Verification** (Section 4.2.2, "Orphan Module Analysis"):
> "Detect Python files in conventionally-structured directories (`steps/`, `handlers/`, `validators/`) whose exported functions are never imported by any consumer module."

**Anti-Instincts** (Section 6, Module 3: Fingerprint Extraction):
> Extracts code-level identifiers from spec content (backtick-delimited names, code-block definitions, ALL_CAPS constants) and verifies minimum coverage ratio in roadmap.

**Why partially redundant**: Both would catch the case where `steps/validate_config.py::run_validate_config` is defined but never connected. Wiring Verification catches it in code; Anti-Instincts catches it when the roadmap drops the identifier entirely.

**Why NOT fully redundant**: Fingerprint extraction is not specifically about orphan modules -- it is about wholesale identifier omission. It would catch many things Wiring Verification would not (dropped class names, constants, test names), while Wiring Verification catches things Fingerprint extraction would not (modules that exist in code but have no importers, regardless of what the spec said).

**Which is more complete**: Different domains entirely. Not directly comparable.

#### Overlap Instance 1.4: Shared Forensic Origin and Evidence

Both specs cite the exact same forensic evidence:
- `step_runner=None` no-op default
- Steps existing but never imported
- `STEP_REGISTRY` as metadata-only with no function references
- "Link 3 does not exist" finding
- The "defined but not wired" recurring pattern

**Why this matters**: If both specs are implemented, the same bug would be caught by multiple redundant mechanisms. This is either defense-in-depth (positive) or wasted engineering effort (negative), depending on whether both specs are needed.

#### Overlap Instance 1.5: GateCriteria / SemanticCheck Integration

**Wiring Verification** (Section 4.4): Defines `WIRING_GATE = GateCriteria(...)` with `SemanticCheck` instances, evaluated by `gate_passed()`.

**Anti-Instincts** (Section 8): Defines `ANTI_INSTINCT_GATE = GateCriteria(...)` with `SemanticCheck` instances, evaluated by `gate_passed()`.

**Why not contradictory**: Both correctly use the existing gate infrastructure pattern without modifying it. They define separate gates with separate check functions. No conflict exists; they coexist cleanly.

---

### 2. Wiring Verification <-> Unified Audit Gating: 4/10 (40%)

#### Overlap Instance 2.1: Spec Fidelity Deterministic Checks D-03/D-04

**Wiring Verification** (Section 4.2.3, Unwired Registry Analysis):
> Detects dictionary constants matching `STEP_REGISTRY`, `STEP_DISPATCH`, `PROGRAMMATIC_RUNNERS`, `*_REGISTRY`, `*_DISPATCH` whose values reference unresolvable functions.

**Unified Audit Gating** (SS13.4, Check D-03):
> "`_DISPATCH_TABLE_PATTERN` regex finds `UPPER_CASE_NAME = {` or `dict(` in spec; verifies each found name appears anywhere in roadmap text."

**Why partially redundant**: Both detect the `PROGRAMMATIC_RUNNERS` dispatch table failure. D-03 checks that named dispatch tables from the spec appear in the roadmap. Wiring Verification checks that dispatch registry entries in code resolve to importable functions.

**Why NOT fully redundant**: D-03 operates at spec-to-roadmap fidelity level (text matching). Wiring Verification operates at code-level (AST analysis). Different pipeline stages, different artifact types.

**Which is more complete**: D-03 is narrower (presence check only -- does the name appear?). Wiring Verification is deeper (are the registry entries actually importable?).

#### Overlap Instance 2.2: D-04 Pseudocode Function Preservation vs. Orphan Module Detection

**Wiring Verification** (Section 4.2.2): Detects functions in `steps/` directories with zero importers.

**Unified Audit Gating** (SS13.4, Check D-04):
> "`_STEP_DISPATCH_CALL` regex finds `_run_*()` or `step_result = ` patterns in spec code fences; verifies at least one found function name appears in roadmap."

**Why partially redundant**: Both would flag `_run_programmatic_step` as missing/orphaned. D-04 catches it at the roadmap stage; Wiring Verification catches it in the implemented code.

#### Overlap Instance 2.3: Silent Success Detection vs. Shadow Mode Non-Interference

**Wiring Verification** (Section 8, Phase 1): Shadow mode that logs but does not affect pipeline flow.

**Unified Audit Gating** (SS13.2): Silent Success Detection that detects pipelines producing no real work despite `outcome: SUCCESS`.

**Why partially overlapping**: Silent Success Detection would catch the no-op executor at runtime. Wiring Verification's shadow mode would log the same underlying bug (unwired callables) statically. Both are mechanisms for detecting the same root cause from different angles.

**Why NOT fully redundant**: Silent Success Detection is behavioral (did the pipeline actually do anything?). Wiring Verification is structural (are the code dependencies connected?). They complement each other -- Silent Success Detection catches no-ops from ANY cause, while Wiring Verification specifically identifies the structural reason.

#### Overlap Instance 2.4: Deviation Count Reconciliation

**Wiring Verification** (Section 4.6, "Companion: Deviation Count Reconciliation"):
> "Single function `_deviation_counts_reconciled(content: str) -> bool` added to `SPEC_FIDELITY_GATE.semantic_checks`."

**Unified Audit Gating** (SS10.1, Phase 0):
> "Wire `deviation-analysis` step into roadmap `_build_steps()`."

**Why partially overlapping**: Both modify the same area of the codebase (`roadmap/gates.py` for deviation handling). Wiring Verification adds a frontmatter/body reconciliation check. Unified Audit Gating wires the deviation-analysis step into the pipeline.

**Why NOT contradictory**: These are different features in the same module. The reconciliation check validates consistency within the deviation report. The pipeline wiring ensures the deviation step runs. They would need to be coordinated at implementation time but are not redundant.

---

### 3. Anti-Instincts <-> Unified Audit Gating: 3/10 (30%)

#### Overlap Instance 3.1: Dispatch Table / Registry Detection in Spec Fidelity

**Anti-Instincts** (Section 5, Integration Contract Extractor):
> Extracts integration contracts from spec text for dispatch tables, registries, injection points and verifies each has a corresponding explicit wiring task in the roadmap.

**Unified Audit Gating** (SS13.4, D-03):
> Named dispatch table preservation check: verifies `UPPER_CASE_NAME = {` patterns from spec appear in roadmap text.

**Why partially redundant**: Both check that dispatch tables defined in the spec are preserved in the roadmap. D-03 does a name-presence check. Anti-Instincts does a more thorough wiring-task check (verifying not just that the name appears, but that there is an explicit wiring task using verb-anchored patterns like "create", "populate", "wire").

**Which is more complete**: Anti-Instincts is significantly more complete. D-03 only checks name presence (the roadmap could mention `PROGRAMMATIC_RUNNERS` without planning a task to populate it, and D-03 would pass). Anti-Instincts' contract extractor specifically checks for wiring verbs, catching the "mentioned is not planned" gap that D-03 misses. The Anti-Instincts spec explicitly acknowledges this distinction in Section 6 (A-009 interaction discussion).

#### Overlap Instance 3.2: Fingerprint Coverage vs. D-04 Function Name Preservation

**Anti-Instincts** (Section 6, Fingerprint Extraction):
> Extracts backtick-delimited identifiers, code-block definitions, ALL_CAPS constants from spec; checks 70% coverage ratio in roadmap.

**Unified Audit Gating** (SS13.4, D-04):
> Checks that `_run_*()` and `step_result = ` patterns from spec code fences appear in roadmap.

**Why partially redundant**: D-04 is a narrow subset of what fingerprint extraction does. Fingerprint extraction catches ALL backtick identifiers, ALL function definitions in code blocks, and ALL ALL_CAPS constants. D-04 catches only a specific naming pattern (`_run_*`, `step_result`).

**Which is more complete**: Anti-Instincts fingerprint extraction is strictly more comprehensive. D-04 is a targeted check for one specific pattern family. If fingerprint extraction is deployed, D-04 would catch only edge cases where fingerprint extraction might miss (if the coverage ratio is above 0.7 despite missing the specific dispatch functions -- possible but unlikely for specs with few total fingerprints).

#### Overlap Instance 3.3: Prompt-Level Integration Wiring

**Anti-Instincts** (Section 10, Change 2):
> Adds `INTEGRATION_WIRING_DIMENSION` as 6th comparison dimension to `build_spec_fidelity_prompt()`.

**Unified Audit Gating** (SS13.4):
> D-03 and D-04 add deterministic checks to `SPEC_FIDELITY_GATE`.

**Why partially overlapping**: Both modify the spec-fidelity validation pipeline. Anti-Instincts adds a prompt dimension (influencing the LLM's fidelity review). Unified Audit Gating adds deterministic checks (bypassing the LLM entirely).

**Why NOT contradictory**: These are complementary. The prompt dimension helps the LLM notice integration wiring issues. The deterministic checks catch failures regardless of what the LLM notices. The Unified Audit Gating spec explicitly states: "The deterministic checks are not overridable by LLM output."

---

## Summary Assessment

### Wiring Verification vs. Anti-Instincts (5/10): Highest overlap

The overlap is real but the specs operate at fundamentally different pipeline stages:
- **Anti-Instincts**: Pre-implementation. Validates spec-to-roadmap fidelity. Catches planning omissions before code is written.
- **Wiring Verification**: Post-implementation. Validates code-level wiring. Catches bugs in code that was already written.

Implementing both creates defense-in-depth. The redundancy is intentional and valuable -- Anti-Instincts prevents the bug from being planned; Wiring Verification catches it if it gets through anyway. However, if resources are constrained, Anti-Instincts provides broader coverage (4 detection modules across 7 mechanism categories) while Wiring Verification provides deeper analysis (AST-level precision on 3 specific patterns).

### Wiring Verification vs. Unified Audit Gating (4/10): Moderate overlap

The overlap is concentrated in the D-03/D-04 checks and the deviation-analysis wiring. Both modify `roadmap/gates.py`. Implementation coordination is needed to avoid merge conflicts, but the features themselves are complementary rather than redundant.

### Anti-Instincts vs. Unified Audit Gating (3/10): Low overlap

The overlap is limited to D-03/D-04 being a narrow subset of what Anti-Instincts' fingerprint extraction and integration contract extractor already do. If Anti-Instincts is implemented, D-03 and D-04 provide marginal additional value (they are simpler, faster, and independently deployable, which is their stated advantage in the Unified Audit Gating spec: "deployable in ~6h, no Phase 1 dependency").

### No contradictions found

None of the three specs contradict each other. They define separate gates (`WIRING_GATE`, `ANTI_INSTINCT_GATE`, `SMOKE_TEST_GATE` / `SilentSuccessDetector`), target different pipeline positions, and use the same `GateCriteria`/`SemanticCheck` infrastructure without modifying it. All three can be implemented and coexist.
