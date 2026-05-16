# Spec Panel Focus Report

> Focus: correctness, architecture
> Spec: `portify-release-spec.md`
> Date: 2026-04-12

---

## Fowler (Architecture) Findings

### F-001
- **Severity**: MAJOR
- **Expert**: Fowler
- **Location**: Section 4.6 (Implementation Order), Section 5.2 (Gate Criteria)
- **Issue**: `gates.py` is listed as depending only on `pipeline.models`, but several semantic check functions (`_check_task_phases_present`, `_check_b2_self_contained`, `_check_parallel_instructions`) contain regex patterns tightly coupled to the PRD skill's MDTM format. If the task file format evolves, gates.py must change. This coupling is implicit -- there is no interface boundary between "pipeline gate infrastructure" and "PRD-specific gate logic".
- **Recommendation**: Split gates.py into two layers: `gates_base.py` (reusable gate infrastructure: `_check_verdict_field`, `_check_no_placeholders`) and `gates_prd.py` (PRD-specific checks: task phase validation, B2 pattern, parallel instructions). This makes the coupling explicit and gates_base reusable for future portified pipelines.

### F-002
- **Severity**: MAJOR
- **Expert**: Fowler
- **Location**: Section 2.2 (Data Flow), Section 3 (FR-PRD.13)
- **Issue**: The data flow shows synthesis agents consuming research files, but the filtering logic (`_filter_research_for_sections`) is described in `filtering.py` while the synthesis mapping is in `inventory.py` (`load_synthesis_mapping`). The synthesis step builder in `executor.py` must coordinate both. This creates a hidden dependency chain: executor -> filtering -> inventory, with the mapping table as a shared data structure that must stay consistent with `refs/synthesis-mapping.md`.
- **Recommendation**: Move `load_synthesis_mapping()` to `filtering.py` alongside `_filter_research_for_sections()` so the mapping and filtering logic colocate. The synthesis step builder then has a single dependency for its data flow.

### F-003
- **Severity**: MINOR
- **Expert**: Fowler
- **Location**: Section 4.5 (Data Models)
- **Issue**: `PrdPipelineResult` has both `outcome: str` and per-step `PrdStepStatus` enums. The outcome is a string literal (`"success" | "halted" | "interrupted" | "error"`) while step status is a typed enum. This inconsistency means callers must handle two different status representations.
- **Recommendation**: Define `PipelineOutcome` as an enum alongside `PrdStepStatus` for consistency.

### Pipeline Quantity Flow Diagram

```
Step 2: 1 user request -> 1 parsed-request.json           (1:1)
Step 3: 1 parsed-request -> 1 scope-discovery              (1:1)
Step 4: 1 scope-discovery -> 1 research-notes              (1:1)
Step 10: 1 research-notes -> N research files               (1:N, N=2-10+)
         [spec accounts for N via tier-based caps]
Step 11: N research files -> 2 QA reports + 1 gaps file     (N:3)
         [spec accounts for N via partitioning at >6]
Step 12: 1 gaps file -> M web research files                (1:M, M=0-4)
         [spec accounts for M via tier caps]
Step 13a: N+M research files -> 9 synth files               (N+M:9)
          [spec accounts via mapping table; DIVERGENCE: 
           if N+M > expected, _filter_research_for_sections 
           must handle unmapped files -- UNSPECIFIED]
Step 13b: 9 synth files -> 2 QA reports                     (9:2)
          [spec accounts via partitioning at >4]
Step 14a: 9 synth files -> 1 assembled PRD                  (9:1)
Step 14b-c: 1 PRD -> 2 QA reports                           (1:2)
```

**Divergence found**: Step 13a's `_filter_research_for_sections` is not specified for the case where research files exist that don't match any synthesis mapping entry's `source_topics`. These orphan files would be silently dropped.

---

## Nygard (Reliability/Failure Modes) Findings

### F-004
- **Severity**: CRITICAL
- **Expert**: Nygard
- **Location**: Section 3 (FR-PRD.10), Section 6 (NFR-PRD.7)
- **Issue**: The spec defines `ThreadPoolExecutor(max_workers=min(len(steps), 10))` but does not specify what happens when a Claude subprocess hangs past its timeout. The `timeout_seconds` field on Step objects is defined but the mechanism for enforcing it is unspecified. `ThreadPoolExecutor.submit()` returns a `Future` -- but `Future.result(timeout=N)` only times out the *wait*, it doesn't kill the subprocess. A hung Claude process would leak resources.
- **Recommendation**: Specify that `PrdClaudeProcess` uses `subprocess.Popen` with an external watchdog timer. On timeout: (1) send SIGTERM to subprocess, (2) wait 5s, (3) send SIGKILL. The `_execute_claude_step` function must handle `TimeoutError` from the watchdog and return `PrdStepStatus.TIMEOUT`.

### F-005
- **Severity**: MAJOR
- **Expert**: Nygard
- **Location**: Section 5.2 (Gate Criteria), Section 3 (FR-PRD.4)
- **Issue**: The STRICT gate on research notes validates 7 required sections via `_check_research_notes_sections`, which uses string matching against section header text. But the spec does not define behavior when the file exists, passes min_lines (100), has valid frontmatter, but the semantic check function itself throws an exception (e.g., the content is binary garbage, or the regex engine hits catastrophic backtracking on adversarial input).
- **Recommendation**: Wrap all semantic check functions in a try/except handler at the gate_passed() level. If a semantic check raises an exception, return `(False, f"Semantic check '{name}' crashed: {error}")` rather than propagating the exception and crashing the pipeline.

### F-006
- **Severity**: MAJOR
- **Expert**: Nygard
- **Location**: Section 3 (FR-PRD.11), Section 6 (NFR-PRD.4)
- **Issue**: Fix cycle budget accounting is underspecified. Each fix cycle spawns gap-filling agents + re-runs QA. With 3 fix cycles and 3 gap-fillers each, that's up to 12 additional subprocess launches beyond the base pipeline. The spec says TurnLedger guards every launch, but doesn't specify whether fix cycle turns are deducted from the main budget or from a separate fix cycle reserve.
- **Recommendation**: Fix cycle turns should be deducted from the main TurnLedger budget. The executor should check `ledger.can_launch()` before each gap-filler and each re-QA launch. If budget is exhausted mid-fix-cycle, the pipeline halts with `QA_FAIL_EXHAUSTED` and includes the partial fix cycle results in the resume state.

### Guard Condition Boundary Table

| Guard | Zero/Empty | Negative | At Min | At Max | Above Max |
|-------|-----------|----------|--------|--------|----------|
| `min_lines` (research notes: 100) | 0 lines -> FAIL (LIGHT gate catches empty) | N/A | 100 lines -> PASS | N/A | N/A |
| `min_lines` (task file, standard: 400) | 0 -> FAIL | N/A | 400 -> PASS | N/A | N/A |
| `partition_threshold` (research: 6) | 0 files -> single empty partition | N/A | 6 files -> single partition | 7 files -> 2 partitions | 100 files -> 17 partitions (UNSPECIFIED cap) |
| `max_research_fix_cycles` (3) | 0 -> no fix cycles | N/A | FAIL on cycle 1 -> try 3 | FAIL on cycle 3 -> EXHAUSTED | N/A |
| `max_workers` (10 cap) | 0 steps -> **UNSPECIFIED** (ThreadPoolExecutor with 0 workers?) | N/A | 1 step -> 1 worker | 10 steps -> 10 workers | 15 steps -> 10 workers |
| `stall_timeout` (120s) | 0 events, 0s elapsed -> "waiting..." | N/A | 0 events, 120s -> STALLED | N/A | N/A |
| `budget (max_turns: 300)` | 0 remaining -> halt | N/A | `minimum_allocation` remaining -> last launch | N/A | N/A |

**Critical boundary**: `partition_files()` with 0 files returns `[[]]` (single partition with empty list). Downstream QA agents would receive an empty file list and produce meaningless reports. Spec should define: if `discover_research_files()` returns empty list, halt pipeline before QA step.

---

## Whittaker (Adversarial) Findings

### F-007
- **Severity**: MAJOR
- **Expert**: Whittaker
- **Location**: Section 3 (FR-PRD.11), Executor Design
- **Issue (Sentinel Collision)**: The `_determine_status()` function searches for `EXIT_RECOMMENDATION: HALT` and `EXIT_RECOMMENDATION: CONTINUE` in subprocess output. If a research agent quotes these strings when documenting the PRD skill's own behavior (since the PRD skill *is* the product being documented), the status classifier would misinterpret the quoted sentinel as an actual recommendation.
- **Recommendation**: Require sentinels to appear on a line by themselves (not inside code blocks or quotes). Change regex to: `^EXIT_RECOMMENDATION: (CONTINUE|HALT)$` with `re.MULTILINE`. Additionally, the sentinel should not be inside a fenced code block -- add a check that the sentinel line is not between ` ``` ` markers.

### F-008
- **Severity**: MAJOR
- **Expert**: Whittaker
- **Location**: Section 3 (FR-PRD.1), inventory.py
- **Issue (Divergence)**: `check_existing_work()` uses `config.product_name.lower() not in content.lower()` as the matching heuristic. If the product name is very short (e.g., "cli"), it would match unrelated task dirs (e.g., a PRD about "CLI migration" would match a request for "CLI audit"). Conversely, if the product name contains special characters, the substring match could fail unexpectedly.
- **Recommendation**: Add minimum product name length check (>= 3 chars). For short names, require the match to appear in the frontmatter's `title` or `product_name` field specifically, not anywhere in the file content.

### F-009
- **Severity**: MINOR
- **Expert**: Whittaker
- **Location**: Section 5.2 (Gate Criteria), gates.py
- **Issue (Accumulation)**: `_check_no_placeholders()` checks for `TODO`, `TBD`, `PLACEHOLDER`, `[INSERT`. The string `TODO` appears legitimately in many contexts (e.g., "TODO items are tracked in...", section about TODO management). This would false-positive on content-appropriate uses.
- **Recommendation**: Restrict placeholder detection to specific patterns: `[TODO]`, `[TBD]`, `{{PLACEHOLDER}}`, `[INSERT HERE]`. Or require placeholders to be at the start of a line / in a specific format.

### F-010
- **Severity**: MINOR
- **Expert**: Whittaker
- **Location**: Section 3 (FR-PRD.5)
- **Issue (Zero/Empty)**: If `sufficiency-review.json` returns `{"verdict": "FAIL", "gaps": []}` -- a FAIL verdict with an empty gaps list -- the fix cycle has nothing to fix but the verdict blocks progress. The spec doesn't define this degenerate case.
- **Recommendation**: If verdict is FAIL but gaps list is empty, treat as PASS with warning (the reviewer found no specific issues but felt uneasy -- not actionable).

---

## Crispin (Testing) Findings

### F-011
- **Severity**: MAJOR
- **Expert**: Crispin
- **Location**: Section 8.1 (Unit Tests)
- **Issue**: No unit tests specified for `prompts.py` -- the largest module (~400 lines, 19 functions). Prompt builders are critical for subprocess behavior and contain conditional logic (tier-dependent content, context injection, file truncation).
- **Recommendation**: Add test cases: `test_build_investigation_prompt_includes_staleness_protocol`, `test_build_synthesis_prompt_includes_template_reference`, `test_prompt_size_under_100kb_limit`, `test_read_file_truncation_at_50kb`.

### F-012
- **Severity**: MAJOR
- **Expert**: Crispin
- **Location**: Section 8.2 (Integration Tests)
- **Issue**: No integration test for the full dynamic step generation flow: research notes -> `build_investigation_steps()` -> Step objects with correct counts and file assignments. This is a critical correctness path.
- **Recommendation**: Add `test_build_investigation_steps_standard_tier` and `test_build_investigation_steps_heavyweight_tier` that provide synthetic research notes and verify the correct number of Step objects with correct output paths.

### F-013
- **Severity**: MINOR
- **Expert**: Crispin
- **Location**: Section 8.1 (Unit Tests)
- **Issue**: `test_check_verdict_field` tests for PASS/FAIL but the spec mentions both JSON format (`"verdict": "PASS"`) and markdown format (`verdict: PASS`). The test should cover both formats explicitly.
- **Recommendation**: Split into `test_check_verdict_field_json_format` and `test_check_verdict_field_markdown_format`.

---

## Quality Dimension Scores

```json
{
  "clarity": 8.2,
  "completeness": 7.8,
  "testability": 7.5,
  "consistency": 8.0
}
```

**Clarity (8.2)**: Spec is well-structured with clear section organization, consistent formatting, and explicit acceptance criteria. Minor deductions for some implicit coupling (F-001, F-002) and underspecified boundary behavior.

**Completeness (7.8)**: Core pipeline fully specified. Deductions for: missing subprocess timeout enforcement mechanism (F-004), underspecified fix cycle budget accounting (F-006), missing prompt builder tests (F-011), missing dynamic step generation integration test (F-012).

**Testability (7.5)**: Good unit test coverage for models, gates, inventory, filtering. Deductions for: no prompt builder tests (F-011), no dynamic step generation tests (F-012), some acceptance criteria lack boundary conditions.

**Consistency (8.0)**: Internal cross-references are generally correct. Deductions for: outcome string vs enum inconsistency (F-003), sentinel detection vulnerability (F-007).
