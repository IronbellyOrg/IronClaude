---
title: Sprint CLI - PM Agent Integration
generated: 2026-04-03
scope: pm_agent/, pytest_plugin.py, execution/
---

# PM Agent Integration

## Architecture: Three Parallel Systems

The codebase contains three conceptually aligned but **not fully runtime-wired** systems:

```
+---------------------------+     +---------------------------+     +---------------------------+
| PM Agent Modules          |     | Sprint Runtime            |     | Execution Engine          |
| pm_agent/*.py             |     | cli/sprint/*              |     | execution/*               |
|                           |     |                           |     |                           |
| - ConfidenceChecker       |     | - Task parsing            |     | - ParallelExecutor        |
| - SelfCheckProtocol       |     | - Subprocess orchestration|     | - ReflectionEngine        |
| - ReflexionPattern        |     | - Gate validation         |     | - SelfCorrectionEngine    |
|                           |     | - /sc:task-unified prompts|     | - intelligent_execute()   |
+---------------------------+     +---------------------------+     +---------------------------+
         |                                  |                                  |
         v                                  v                                  v
   Pytest plugin +              Claude subprocess with            Standalone subsystem
   explicit test usage          protocol-driven confidence        (not called from sprint)
```

**Key insight**: PM Agent Python modules are tightly integrated with the pytest plugin for test-time use. Sprint runtime achieves similar goals through prompt-driven behavior (e.g., `/sc:task-unified` includes confidence classification in its protocol spec).

## PM Agent Module: ConfidenceChecker

**File**: `src/superclaude/pm_agent/confidence.py`

### Class: `ConfidenceChecker` (line 26)

**API**: `assess(context: dict) -> float` (line 42)

Scoring weights:
| Check | Weight | Context Key |
|-------|--------|-------------|
| No duplicates | 25% | `duplicate_check_complete` |
| Architecture compliance | 25% | `architecture_check_complete` |
| Official docs verified | 20% | `official_docs_verified` |
| OSS reference | 15% | `oss_reference_complete` |
| Root cause identified | 15% | `root_cause_identified` |

**Thresholds**:
- `>= 0.9`: High confidence, proceed
- `>= 0.7`: Medium confidence, present alternatives
- `< 0.7`: Low confidence, ask questions

**Recommendation**: `get_recommendation(confidence: float) -> str` (line 257)

**Side effect**: Writes `context["confidence_checks"]` dict (line 98)

## PM Agent Module: SelfCheckProtocol

**File**: `src/superclaude/pm_agent/self_check.py`

### Class: `SelfCheckProtocol` (line 19)

**API**: `validate(implementation: dict) -> tuple[bool, list[str]]` (line 64)

Validation dimensions:
1. **Tests passing** with actual output (109-128)
2. **Requirements coverage** (129-145)
3. **Assumptions verified** (146-162)
4. **Evidence exists**: `test_results`, `code_changes`, `validation` keys (163-185)
5. **Hallucination red flags**: scans for "probably", "maybe", "should work", "might work" (187-229)

**Report**: `format_report(passed: bool, issues: list[str]) -> str` (line 231)

No numeric score — fail-fast issue accumulation.

## PM Agent Module: ReflexionPattern

**File**: `src/superclaude/pm_agent/reflexion.py`

### Class: `ReflexionPattern` (line 32)

**API**:
- `get_solution(error_info: dict) -> Optional[dict]` (line 76)
- `record_error(error_info: dict) -> None` (line 102)
- `get_statistics() -> dict` (line 310)

**Storage**: `docs/memory/solutions_learned.jsonl` (line 69)

**Matching logic**:
1. Build signature from error type/message/test name (130-163)
2. Search JSONL for matches (178-212)
3. Token overlap similarity with threshold `0.7` (213-237)

**Side effects**:
- Appends to `solutions_learned.jsonl` (123-125)
- Writes detailed `docs/mistakes/*.md` when root-cause/solution present (127-129, 238-309)

## Pytest Plugin Integration

**File**: `src/superclaude/pytest_plugin.py`

**Registration**: `pyproject.toml:67-68` as entry point `pytest11`

### Fixtures Provided

| Fixture | Line | Returns |
|---------|------|---------|
| `confidence_checker` | 46 | `ConfidenceChecker()` |
| `self_check_protocol` | 58 | `SelfCheckProtocol()` |
| `reflexion_pattern` | 71 | `ReflexionPattern(memory_dir)` |
| `token_budget` | 84 | Budget object (simple:200, medium:1000, complex:2500) |
| `pm_context` | 105 | Combined context dict |

### Hooks

**`pytest_runtest_setup`** (line 136-157):
- If test marked `@pytest.mark.confidence_check`:
  - Build context from test metadata
  - Run `ConfidenceChecker.assess(context)`
  - Skip test if confidence `< 0.7`

**`pytest_runtest_makereport`** (line 160-185):
- If test marked `@pytest.mark.reflexion` and fails:
  - Build `error_info` from exception
  - Call `ReflexionPattern.record_error(error_info)`

**`pytest_collection_modifyitems`** (line 194-217):
- Auto-marks tests by path: `/unit/` -> `unit`, `/integration/` -> `integration`

### Data Flow in Pytest Path

```
Test marked @confidence_check
  -> build context (test_name, test_file, markers)
  -> ConfidenceChecker.assess(context)
  -> skip if < 0.7

Test marked @reflexion + FAILS
  -> build error_info (type, message, traceback)
  -> ReflexionPattern.record_error(error_info)
  -> Written to docs/memory/solutions_learned.jsonl

Test using self_check_protocol fixture
  -> Explicit invocation in test body required
  -> validate(implementation) -> (passed, issues)
```

## Sprint Runtime Integration Status

### What IS wired

The sprint runtime achieves PM-agent-like behavior through **protocol-driven prompts**:

- `src/superclaude/cli/sprint/process.py:170-173`: Prompt includes `/sc:task-unified`
- `src/superclaude/commands/task-unified.md:91`: Protocol spec includes `<0.70` confidence override
- Sprint gates (wiring, anti-instinct) provide deterministic quality checks

### What is NOT wired

| PM Agent Component | Sprint Runtime Call | Status |
|---|---|---|
| `ConfidenceChecker.assess()` | None | **Not called** from sprint executor |
| `SelfCheckProtocol.validate()` | None | **Not called** post-task |
| `ReflexionPattern.record_error()` | None | **Not called** on task failure |
| `ReflexionPattern.get_solution()` | None | **Not called** pre-task |
| `intelligent_execute()` | None | **Not called** from sprint |
| `ReflectionEngine.reflect()` | None | **Not called** pre-phase |

### Execution Engine (`execution/`) Status

The standalone execution subsystem provides:
- `ReflectionEngine` with 3-stage confidence scoring (clarity 0.5, mistakes 0.3, context 0.2)
- `ParallelExecutor` with dependency-wave batching
- `SelfCorrectionEngine` with error categorization and learning persistence

**None of these are called from the sprint CLI runtime.** They exist as a separate, independently usable framework.

## Configuration Thresholds Summary

| System | Threshold | Source |
|--------|-----------|--------|
| PM confidence gate | `>= 0.9` high, `>= 0.7` medium, `< 0.7` low | `pm_agent/confidence.py` |
| Pytest confidence skip | `< 0.7` skip | `pytest_plugin.py:156-157` |
| Reflexion similarity match | `0.7` overlap | `pm_agent/reflexion.py:213` |
| Token budget: simple | 200 tokens | `pm_agent/token_budget.py` |
| Token budget: medium | 1000 tokens | `pm_agent/token_budget.py` |
| Token budget: complex | 2500 tokens | `pm_agent/token_budget.py` |
| Execution reflection block | `< 0.7` block | `execution/reflection.py:80` |
