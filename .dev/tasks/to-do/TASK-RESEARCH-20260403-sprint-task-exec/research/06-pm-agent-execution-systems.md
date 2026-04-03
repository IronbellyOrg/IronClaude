# Research: PM Agent and Execution Systems

**Status**: Complete
**Date**: 2026-04-03
**Investigation Type**: Integration Mapper
**Research Question**: What do the pm_agent/ and execution/ modules provide, are they used by any part of the system, and were they designed to be pluggable into sprint?

---

## 1. Module Inventory and Purpose

### 1.1 pm_agent/ — Pytest-Oriented Verification Primitives

These four modules are designed as **pytest fixtures and markers**, not as sprint execution components.

#### ConfidenceChecker (`src/superclaude/pm_agent/confidence.py`)
- **Purpose**: Pre-implementation confidence assessment. Scores a task 0.0-1.0 across five weighted dimensions: no duplicates (25%), architecture compliance (25%), official docs verified (20%), OSS reference found (15%), root cause identified (15%).
- **API**: `ConfidenceChecker().assess(context: Dict) -> float` where context is a dict with keys like `duplicate_check_complete`, `architecture_check_complete`, `official_docs_verified`, `oss_reference_complete`, `root_cause_identified`.
- **Key detail**: Most internal check methods are **placeholder stubs** that simply read boolean flags from the context dict. The `_has_official_docs()` method does real filesystem checks (looks for README.md, CLAUDE.md, docs/ in parent directories), and `_has_existing_patterns()` / `_has_clear_path()` do real analysis, but these are NOT called by `assess()` — they appear to be leftover or auxiliary methods.
- **Lines**: 273 lines total.

#### SelfCheckProtocol (`src/superclaude/pm_agent/self_check.py`)
- **Purpose**: Post-implementation validation through "The Four Questions": (1) tests passing with evidence, (2) all requirements met, (3) assumptions verified, (4) evidence provided. Also detects 7 hallucination red flags.
- **API**: `SelfCheckProtocol().validate(implementation: Dict) -> Tuple[bool, List[str]]` where implementation contains keys like `tests_passed`, `test_output`, `requirements`, `requirements_met`, `assumptions`, `evidence`, etc.
- **Key detail**: Purely data-driven. Caller must populate the implementation dict with all evidence; the protocol just validates that evidence exists and is consistent. Does not run tests or check code itself.
- **Lines**: 250 lines total.

#### ReflexionPattern (`src/superclaude/pm_agent/reflexion.py`)
- **Purpose**: Error learning and prevention. Stores error solutions in `docs/memory/solutions_learned.jsonl` (JSONL append-only log) and detailed mistake docs in `docs/mistakes/`. Provides lookup by error signature matching (Jaccard word overlap, threshold 0.7).
- **API**: `ReflexionPattern(memory_dir=None)`, `.get_solution(error_info) -> Optional[Dict]`, `.record_error(error_info)`, `.get_statistics()`.
- **Key detail**: `_search_mindbase()` is a TODO stub returning None. The file-based search is functional. Creates directories on init.
- **Lines**: 345 lines total.

#### TokenBudgetManager (`src/superclaude/pm_agent/token_budget.py`)
- **Purpose**: Token allocation management with three complexity tiers: simple=200, medium=1000, complex=2500.
- **API**: `TokenBudgetManager(complexity="medium")`, `.allocate(amount) -> bool`, `.use(amount) -> bool`, `.remaining -> int`, `.reset()`.
- **Key detail**: Simple counter with a ceiling. No integration with any real token-counting system. The `use()` method is documented as a "backward compatible helper" for "historical CLI usage" but no such CLI usage exists in the codebase.
- **Lines**: 86 lines total.

### 1.2 execution/ — Standalone Execution Engine (Never Wired In)

These three modules form a self-contained "intelligent execution engine" with a top-level orchestrator in `execution/__init__.py`.

#### ReflectionEngine (`src/superclaude/execution/reflection.py`)
- **Purpose**: 3-stage pre-execution confidence check: (1) requirement clarity analysis (text heuristics on task description), (2) past mistake pattern detection (reads `docs/memory/reflexion.json`), (3) context sufficiency validation (checks for `project_index`, `current_branch`, `git_status` in context dict; checks `PROJECT_INDEX.md` freshness).
- **API**: `ReflectionEngine(repo_path).reflect(task: str, context: Dict) -> ConfidenceScore`. Also has singleton accessor `get_reflection_engine()` and convenience function `reflect_before_execution()`.
- **Key detail**: Uses weighted scoring (clarity 50%, mistakes 30%, context 20%) with a 70% threshold. Prints emoji-decorated output to stdout. Reads `docs/memory/reflexion.json` (the same file SelfCorrectionEngine writes to).
- **Lines**: 401 lines total.

#### SelfCorrectionEngine (`src/superclaude/execution/self_correction.py`)
- **Purpose**: Failure detection, root cause analysis, and prevention rule generation. Categorizes failures into types (validation, dependency, logic, assumption, type) via keyword matching. Stores failures in `docs/memory/reflexion.json` with dedup by MD5 hash.
- **API**: `SelfCorrectionEngine(repo_path)`, `.detect_failure(result) -> bool`, `.analyze_root_cause(task, failure) -> RootCause`, `.learn_and_prevent(...)`, `.get_prevention_rules()`, `.check_against_past_mistakes(task)`. Singleton via `get_self_correction_engine()`.
- **Key detail**: Prevention rules are generic strings like "ALWAYS validate inputs before processing". Validation tests are also generic checklists, not executable code. Root cause analysis is purely keyword-based.
- **Lines**: 426 lines total.

#### ParallelExecutor (`src/superclaude/execution/parallel.py`)
- **Purpose**: Dependency-aware parallel execution via topological sort + ThreadPoolExecutor. Builds execution plans with parallel groups.
- **API**: `ParallelExecutor(max_workers=10)`, `.plan(tasks: List[Task]) -> ExecutionPlan`, `.execute(plan) -> Dict[str, Any]`. Also provides `parallel_file_operations()` and `should_parallelize()` convenience functions.
- **Key detail**: The Task dataclass requires a `Callable` as its execute function. This is designed for Python-callable operations, not for orchestrating external processes like Claude CLI sessions. The sprint executor manages subprocess-based Claude sessions — a fundamentally different execution model.
- **Lines**: 330 lines total.

#### intelligent_execute (`src/superclaude/execution/__init__.py`)
- **Purpose**: Top-level orchestrator combining all three engines: Reflect -> Plan -> Execute -> Self-Correct.
- **API**: `intelligent_execute(task, operations: List[Callable], context, repo_path, auto_correct) -> Dict`.
- **Key detail**: Assumes all operations are independent (hardcoded `depends_on=[]`). This is the intended "entry point" but nothing in the codebase calls it.
- **Lines**: 228 lines total.

---

## 2. Usage Analysis — Where Are These Modules Actually Used?

### 2.1 pm_agent/ modules — Used ONLY by pytest plugin and unit tests

**Consumers found**:
1. `src/superclaude/pytest_plugin.py` (lines 14-17): Imports all four pm_agent classes. Provides them as pytest fixtures (`confidence_checker`, `self_check_protocol`, `reflexion_pattern`, `token_budget`). Also uses `ConfidenceChecker` in the `pytest_runtest_setup` hook (skips tests with <70% confidence) and `ReflexionPattern` in `pytest_runtest_makereport` hook (records failed test errors).
2. `src/superclaude/__init__.py` (lines 12-14): Re-exports `ConfidenceChecker`, `SelfCheckProtocol`, `ReflexionPattern` as top-level package symbols.
3. `src/superclaude/pm_agent/__init__.py` (lines 11-13): Re-exports the three classes.
4. `tests/unit/test_confidence.py`: 13 test methods exercising ConfidenceChecker.
5. `tests/unit/test_self_check.py`: 13 test methods exercising SelfCheckProtocol.
6. `tests/unit/test_reflexion.py`: 8 test methods exercising ReflexionPattern.
7. `tests/unit/test_token_budget.py`: 8 test methods exercising TokenBudgetManager.

**NOT used by**: Any CLI command, sprint executor, roadmap executor, pipeline executor, or any runtime code outside the pytest plugin.

### 2.2 execution/ modules — Used ONLY within execution/ itself

**Consumers found**:
1. `src/superclaude/execution/__init__.py`: Imports and wires together all three engines in `intelligent_execute()`.
2. Each module references only itself (singleton patterns, example functions).

**NOT used by**: Any file outside the `execution/` directory. Zero imports from `src/superclaude/cli/`, `tests/`, or any other module.

### 2.3 pyproject.toml entry points

The only relevant entry point is the pytest plugin:
```
[project.entry-points.pytest11]
superclaude = "superclaude.pytest_plugin"
```
This loads the pm_agent classes as pytest fixtures. The execution/ module has NO entry point.

---

## 3. Relationship Between pm_agent/ and execution/

These two subsystems are **completely independent** despite overlapping in concept:

| Aspect | pm_agent/ | execution/ |
|--------|-----------|------------|
| **Primary consumer** | pytest plugin (fixtures/hooks) | Nothing (self-contained demo) |
| **Confidence checking** | `ConfidenceChecker` — boolean flags in dict | `ReflectionEngine` — text heuristics + file checks |
| **Error learning** | `ReflexionPattern` — JSONL file (`solutions_learned.jsonl`) | `SelfCorrectionEngine` — JSON file (`reflexion.json`) |
| **Overlap** | They both implement confidence checking and error learning but with different APIs, different storage formats, and different file paths |
| **Cross-references** | None — they do not import each other |

The `ReflectionEngine` reads from `reflexion.json` which the `SelfCorrectionEngine` writes to, creating an implicit coupling. But `ReflexionPattern` (pm_agent) uses a completely separate file (`solutions_learned.jsonl`).

---

## 4. Sprint Integration Feasibility Assessment

### 4.1 Sprint Executor Architecture (for comparison)

The sprint executor (`src/superclaude/cli/sprint/executor.py`) orchestrates:
- External `claude` CLI subprocess sessions via `ClaudeProcess`
- Phase-based task execution with gates and monitors
- TUI-based progress display
- Tmux session management
- Pipeline integration via `TrailingGatePolicy` and `Step`/`StepResult` models

Sprint operates at the **process orchestration** level — it spawns and monitors external processes, not Python callables.

### 4.2 Could pm_agent/ be plugged into sprint?

**ConfidenceChecker**: Theoretically yes, as a pre-task validation step. But its API requires the caller to pre-populate boolean flags (`duplicate_check_complete`, etc.) — it doesn't DO the checking, just validates that someone already did. Sprint would need to run actual checks and populate the dict, making the ConfidenceChecker a thin validation layer of questionable value.

**SelfCheckProtocol**: Theoretically yes, as a post-task validation step. Similar limitation — requires pre-populated evidence dict. Sprint already has its own gate/monitor system for post-task validation.

**ReflexionPattern**: Most plausible integration point. Sprint could record task failures via `record_error()` and check for known solutions via `get_solution()` before retrying. However, sprint already has `DiagnosticCollector` and `FailureClassifier` for this purpose.

**TokenBudgetManager**: Not applicable. Sprint doesn't manage token budgets programmatically — token limits are configured via Claude CLI `--max-turns` flags.

### 4.3 Could execution/ be plugged into sprint?

**ReflectionEngine**: Could provide a pre-sprint reflection step, but sprint operates on task descriptions from markdown files, not free-text task strings. The text heuristic analysis (checking for "specific verbs") would provide little value for structured MDTM task inputs.

**ParallelExecutor**: **Incompatible architecture**. Sprint manages external subprocesses; ParallelExecutor manages Python callables via ThreadPoolExecutor. Sprint already has its own parallelism via tmux sessions and its own dependency-tracking via phase ordering.

**SelfCorrectionEngine**: Could supplement sprint's failure handling, but sprint already has `FailureClassifier` and `DiagnosticCollector` that are specifically designed for Claude session failures, not generic Python execution failures.

**intelligent_execute**: Cannot wrap sprint's execution model. It assumes operations are `Callable` objects with no dependencies — fundamentally different from sprint's subprocess-based, multi-turn, gate-guarded execution.

---

## 5. Design Intent Analysis

Based on code comments, docstrings, and architecture:

1. **pm_agent/ was designed as a pytest testing framework enhancement** — providing fixtures that test authors can use to validate their own confidence, self-checks, and error learning. It was NOT designed for runtime sprint integration.

2. **execution/ was designed as a standalone "intelligent execution engine"** concept — a prototype for combining reflection, parallelism, and self-correction into a single orchestration flow. The `if __name__ == "__main__"` block in `parallel.py` and the detailed example functions suggest this was developed as a standalone demo or proof-of-concept. It was designed to be pluggable (singleton pattern, convenience functions) but for a **Python-callable execution model**, not for the subprocess-based sprint executor.

3. **Both subsystems predate the sprint CLI**. The sprint executor has its own purpose-built equivalents: `DiagnosticCollector` for error analysis, `FailureClassifier` for root cause categorization, phase gates for confidence checking, and tmux sessions for parallelism.

---

## Gaps and Questions

1. **Redundancy**: The codebase has THREE separate error-learning systems: `ReflexionPattern` (pm_agent), `SelfCorrectionEngine` (execution), and `DiagnosticCollector`/`FailureClassifier` (sprint). Are all three needed?

2. **Dead code risk**: The entire `execution/` package (`intelligent_execute`, `ReflectionEngine`, `SelfCorrectionEngine`, `ParallelExecutor`) has zero external consumers. It is effectively dead code from a runtime perspective.

3. **Dual confidence systems**: `ConfidenceChecker` (pm_agent) and `ReflectionEngine` (execution) both do pre-execution confidence assessment with different APIs and different scoring logic. Neither is used by sprint.

4. **Storage format divergence**: `ReflexionPattern` uses JSONL (`solutions_learned.jsonl`), `SelfCorrectionEngine` uses JSON (`reflexion.json`), and sprint's diagnostics use their own format. A unified error-learning storage would reduce complexity.

5. **Would sprint benefit from any of these?** The most useful would be a **cross-session error memory** (recording that a specific task pattern failed and what fixed it). `ReflexionPattern.get_solution()` provides this conceptually, but sprint would need an adapter to translate its `TaskResult` failures into the `error_info` dict format.

---

## Summary

**pm_agent/** (ConfidenceChecker, SelfCheckProtocol, ReflexionPattern, TokenBudgetManager) are **pytest fixtures** used exclusively by the pytest plugin and their own unit tests. They provide test-time verification primitives, not runtime execution capabilities. They have comprehensive test coverage (4 test files, ~42 test methods total).

**execution/** (ReflectionEngine, ParallelExecutor, SelfCorrectionEngine, intelligent_execute) is an **unused standalone prototype** for a Python-callable intelligent execution engine. Zero external imports exist. No tests exist for these modules. The architecture is fundamentally incompatible with sprint's subprocess-based execution model.

**Neither subsystem is wired into sprint, and neither was designed for sprint's execution model.** Sprint has built its own purpose-specific equivalents (DiagnosticCollector, FailureClassifier, phase gates, tmux parallelism). The most plausible integration point would be adapting `ReflexionPattern` as a cross-session error memory for sprint, but this would require an adapter layer and the value proposition is unclear given sprint's existing diagnostics infrastructure.

**Key files investigated**:
- `src/superclaude/pm_agent/confidence.py` — ConfidenceChecker (pytest fixture only)
- `src/superclaude/pm_agent/self_check.py` — SelfCheckProtocol (pytest fixture only)
- `src/superclaude/pm_agent/reflexion.py` — ReflexionPattern (pytest fixture only)
- `src/superclaude/pm_agent/token_budget.py` — TokenBudgetManager (pytest fixture only)
- `src/superclaude/execution/reflection.py` — ReflectionEngine (unused)
- `src/superclaude/execution/self_correction.py` — SelfCorrectionEngine (unused)
- `src/superclaude/execution/parallel.py` — ParallelExecutor (unused)
- `src/superclaude/execution/__init__.py` — intelligent_execute orchestrator (unused)
- `src/superclaude/pytest_plugin.py` — sole runtime consumer of pm_agent/ classes
- `src/superclaude/cli/sprint/executor.py` — confirmed zero imports from either subsystem