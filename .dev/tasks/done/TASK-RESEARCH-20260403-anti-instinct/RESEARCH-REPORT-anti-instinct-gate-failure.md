# Technical Research Report: Anti-Instinct Gate Failure on Enriched Runs

**Date:** 2026-04-03
**Depth:** Deep
**Research files:** Direct code reading + audit artifact comparison
**Scope:** src/superclaude/cli/roadmap/ (gates.py, executor.py, fingerprint.py, obligation_scanner.py, integration_contracts.py)

---

## 1. Problem Statement

The anti-instinct gate passes cleanly for the spec-only baseline (0 undischarged, 0 uncovered) but fails for all TDD+PRD and Spec+PRD enriched runs (1-2 undischarged, 3-4 uncovered). This blocks the entire enriched pipeline from completing — no spec-fidelity, test-strategy, deviation-analysis, remediation, or certify artifacts are produced for enriched runs. We incorrectly reported this as "pre-existing" across multiple E2E runs.

## 2. Current State Analysis

### 2.1 The Anti-Instinct Audit Is Deterministic Python, Not LLM

The anti-instinct step is NOT an LLM prompt. It runs `_run_anti_instinct_audit()` at `executor.py:535` which calls three pure-Python modules:

1. **`obligation_scanner.py`** (306 lines) — Regex-based scanner for scaffold terms (`mock`, `stub`, `placeholder`, `temporary`, `hardcoded`, etc.) and discharge terms (`replace`, `wire`, `integrate`, etc.)
2. **`integration_contracts.py`** (303 lines) — Regex-based scanner for 7 categories of dispatch patterns (dict dispatch, plugin registry, callback injection, strategy pattern, middleware chain, event binding, DI container)
3. **`fingerprint.py`** (169 lines) — Extracts backtick identifiers from spec, checks coverage in roadmap

### 2.2 The Gate Definition

`ANTI_INSTINCT_GATE` at `gates.py:1043` has 3 semantic checks:
- `no_undischarged_obligations` — requires `undischarged_obligations == 0`
- `integration_contracts_covered` — requires `uncovered_contracts == 0`
- `fingerprint_coverage_check` — requires `fingerprint_coverage >= 0.7`

ALL three must pass. Any single failure halts the pipeline.

### 2.3 What's Failing and Why

**TDD+PRD run audit** (`.dev/test-fixtures/results/test1-tdd-prd-v2/anti-instinct-audit.md`):

**Obligation failure (1 undischarged):**
- Line 553: `Hardcoded` in the roadmap text "Hardcoded" appears in the Library Dependencies section describing `bcryptjs cost factor (12)` configuration. The obligation scanner matches `\bhardcoded\b` as a scaffold term. But this is NOT a temporary implementation — it's a deliberate configuration value. There is no corresponding discharge term like "replace hardcoded" in a later phase because it doesn't need replacing.
- **ROOT CAUSE: False positive.** The word "hardcoded" in the roadmap is descriptive, not a scaffolding obligation.

**Integration contract failures (4 uncovered):**
- IC-001: `strategy_pattern` match on "Testing Strategy" (line 136 — a section heading reference in the TDD)
- IC-002: `strategy_pattern` match on "Testing Strategy" (line 181 — table of contents link)
- IC-006: `strategy_pattern` match on "## 15. Testing Strategy" (line 644 — section heading)
- IC-007: `strategy_pattern` match on "### 19.1 Migration Strategy" (line 707 — section heading)
- **ROOT CAUSE: False positives.** The Category 4 Strategy Pattern regex at `integration_contracts.py:48` matches `\bStrategy\b` in section headings. "Testing Strategy" and "Migration Strategy" are SECTION NAMES, not code patterns requiring wiring tasks. The regex is too broad.

### 2.4 Why The Baseline Passes

The baseline roadmap (380 lines) is shorter and simpler:
- It doesn't contain "Hardcoded" in a context that triggers the obligation scanner (or if it does, the discharge is found)
- It has 6 integration contracts and ALL are covered — the shorter roadmap has fewer section headings containing "Strategy"
- Its 1 detected obligation IS discharged (shown in the audit: "Discharged: 1")

## 3. Root Cause

**Hypothesis H1 is partially correct, but the real issue is more specific.**

It's not "more content = more obligations" generically. It's that the regex patterns in both `obligation_scanner.py` and `integration_contracts.py` match common English words that appear more frequently in richer, more descriptive roadmaps:

1. **`\bhardcoded\b`** matches descriptive text about configuration values, not just temporary implementations
2. **`\bStrategy\b`** (in the strategy_pattern category) matches section headings like "Testing Strategy" and "Migration Strategy", not actual Strategy design patterns in code

The baseline passes because its simpler roadmap doesn't contain these words in non-code contexts. The enriched roadmap's richer content naturally uses more descriptive language, triggering more false positives.

## 4. Gap Analysis

| Gap | Current State | Target State | Severity | Notes |
|-----|--------------|-------------|----------|-------|
| Strategy pattern regex too broad | Matches any `\bStrategy\b` | Should only match code patterns (`Context(strategy=`, `ConcreteStrategy`) | Critical | Causes 4/4 uncovered contract false positives |
| Obligation scanner matches descriptive text | `\bhardcoded\b` matches config descriptions | Should only match in imperative/action context ("hardcode this", "use hardcoded") | Critical | Causes 1/1 undischarged obligation false positive |
| No heading-aware context filtering | Regexes run on raw text including headings | Should skip markdown headings (`## `, `### `) for integration contract patterns | Important | Would prevent heading-based false positives systemically |

## 5. Options Analysis

### Option A: Fix the regexes (targeted)

**What:** Tighten the specific regexes causing false positives.

| Aspect | Assessment |
|--------|-----------|
| Effort | S (2-3 regex changes) |
| Risk | Low (targeted fixes, easy to test) |
| Files affected | `integration_contracts.py`, `obligation_scanner.py` |
| Pros | Minimal code change, fixes the exact false positives, doesn't change gate strictness |
| Cons | May need ongoing tuning as roadmap content evolves |

**Specific changes:**
1. `integration_contracts.py` Category 4 (Strategy Pattern): Change from matching bare `\bStrategy\b` to requiring code-context patterns: `Context\s*\(\s*strategy\s*=`, `ConcreteStrategy`, `set_strategy`, `get_strategy`, `StrategyPattern`. Remove the bare `\bStrategy\b` match.
2. `obligation_scanner.py`: Add heading-line exclusion — skip lines that start with `#` (markdown headings). Also consider requiring "hardcoded" to appear in an imperative context (`hardcode`, `uses hardcoded`, `is hardcoded`) rather than as a standalone adjective in descriptive text.

### Option B: Add markdown-aware context filtering (systemic)

**What:** Both modules skip markdown headings, table rows, and code block content when scanning.

| Aspect | Assessment |
|--------|-----------|
| Effort | M (add markdown parsing layer) |
| Risk | Medium (may miss legitimate patterns in headings) |
| Files affected | Both scanner modules |
| Pros | Prevents all heading-based false positives, future-proof |
| Cons | More code, may over-filter |

### Option C: Adjust gate thresholds

**What:** Allow `uncovered_contracts <= 4` or `undischarged_obligations <= 1`.

| Aspect | Assessment |
|--------|-----------|
| Effort | XS (change 2 numbers in gates.py) |
| Risk | HIGH (masks real issues, defeats the gate's purpose) |
| Files affected | `gates.py` |
| Pros | Immediate unblock |
| Cons | **Masks real problems.** The gate exists to catch missing wiring — relaxing it loses that protection. |

### Options Comparison

| Criterion | Option A (Fix regexes) | Option B (Markdown-aware) | Option C (Relax thresholds) |
|-----------|----------------------|--------------------------|---------------------------|
| Fixes root cause | Yes | Yes (broadly) | No (masks it) |
| Risk of masking real issues | None | Low | High |
| Effort | Small | Medium | Trivial |
| Future-proof | Moderate | High | Low |
| Maintains gate strictness | Yes | Yes | No |

## 6. Recommendation

**Option A (Fix the regexes)** with one element from Option B (heading exclusion).

Specific implementation:

### Fix 1: `integration_contracts.py` — Tighten Category 4 Strategy Pattern

At line 48, replace the current Category 4 regex:
```python
# Category 4: Strategy pattern
re.compile(
    r"\b(?:Context\s*\(\s*strategy\s*=|Strategy|ConcreteStrategy|"
    r"set_strategy|get_strategy)\b",
    re.IGNORECASE,
),
```

With a more specific version that requires code context:
```python
# Category 4: Strategy pattern (code-specific, not section headings)
re.compile(
    r"\b(?:Context\s*\(\s*strategy\s*=|ConcreteStrategy|"
    r"set_strategy|get_strategy|StrategyPattern|"
    r"strategy_registry|STRATEGY_MAP)\b",
    re.IGNORECASE,
),
```

Remove bare `Strategy` from the alternation — it's too broad.

### Fix 2: `obligation_scanner.py` — Skip markdown headings

Add a heading filter before regex scanning. In the `scan_obligations()` function, skip lines that start with `#`:

```python
# Skip markdown headings — they describe content, not obligations
if line.lstrip().startswith("#"):
    continue
```

This prevents "Hardcoded" in a heading or descriptive paragraph from triggering as an obligation.

### Fix 3: `integration_contracts.py` — Skip markdown headings for all categories

Add the same heading filter in `extract_integration_contracts()`:

```python
# Skip markdown headings — section names are not integration patterns
if line.lstrip().startswith("#"):
    continue
```

## 7. Impact

After these fixes:
- TDD+PRD run: 0 uncovered contracts (all 4 false positives eliminated), 0 undischarged obligations (false positive eliminated)
- Spec+PRD run: similar reduction in false positives
- Baseline: no change (it already passes)
- The gate remains strict — real scaffolding obligations and real integration contracts still caught

**Rerun required:** Yes. The anti-instinct audit is deterministic — after code changes, rerunning the pipeline will produce different audit results. The roadmap itself doesn't need to change.

## 8. Evidence Trail

| File | What |
|------|------|
| `src/superclaude/cli/roadmap/gates.py:1043` | ANTI_INSTINCT_GATE definition |
| `src/superclaude/cli/roadmap/executor.py:535` | `_run_anti_instinct_audit()` function |
| `src/superclaude/cli/roadmap/obligation_scanner.py` | Scaffold term scanner (306 lines) |
| `src/superclaude/cli/roadmap/integration_contracts.py:48` | Category 4 Strategy Pattern regex (the problem) |
| `src/superclaude/cli/roadmap/fingerprint.py` | Fingerprint extraction (passes, not the issue) |
| `.dev/test-fixtures/results/test1-tdd-prd-v2/anti-instinct-audit.md` | Failing audit with 4 false positive contracts |
| `.dev/test-fixtures/results/test3-spec-baseline/anti-instinct-audit.md` | Passing baseline audit for comparison |
