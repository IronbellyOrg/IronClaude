# Adversarial Debate: Should Path A Include a Result File Contract?

## Metadata
- Generated: 2026-04-03
- Depth: quick (1 round)
- Topic: Per-task result file contract for Sprint CLI Path A
- Variants: 2 (FOR adding contract vs AGAINST adding contract)
- Debate scope: executor.py Path A (lines 1064-1068) vs Path B (process.py lines 197-203)

---

## Diff Analysis

### Current State Summary

**Path A** (per-task subprocess at `executor.py:1064-1068`):
```python
prompt = (
    f"Execute task {task.task_id}: {task.title}\n"
    f"From phase file: {phase.file}\n"
    f"Description: {task.description}\n"
)
```
Status classification at `executor.py:999-1005`:
```python
if exit_code == 0:
    status = TaskStatus.PASS
elif exit_code == 124:
    status = TaskStatus.INCOMPLETE
else:
    status = TaskStatus.FAIL
```
Phase aggregation at `executor.py:1215-1216`:
```python
all_passed = all(r.status == TaskStatus.PASS for r in task_results)
status = PhaseStatus.PASS if all_passed else PhaseStatus.ERROR
```

**Path B** (freeform phase at `process.py:197-203`):
```
## Result File
- When all tasks in this phase are complete, write the result file to:
  `<path>`
- The file content must be exactly: `EXIT_RECOMMENDATION: CONTINUE`
- Write this file as the final action of this phase
- If a STRICT-tier task fails and you are halting, write instead:
  `EXIT_RECOMMENDATION: HALT`
```
Status classification: `_determine_phase_status()` at `executor.py:1765-1846` uses a 7-priority chain including result file parsing.

### Structural Differences

| # | Area | Path A | Path B | Severity |
|---|------|--------|--------|----------|
| S-001 | Prompt complexity | 3-line minimal prompt | ~80-line structured prompt with rules, context, and completion protocol | Medium |
| S-002 | Status classification | Pure exit-code mapping (3 branches) | 7-priority chain with file parsing, regex, and fallback hierarchy | High |
| S-003 | Granularity | One subprocess per task | One subprocess per phase (all tasks) | High |

### Content Differences

| # | Topic | Path A Approach | Path B Approach | Severity |
|---|-------|-----------------|-----------------|----------|
| C-001 | Semantic success signal | Exit code 0 = PASS (no nuance) | EXIT_RECOMMENDATION: CONTINUE/HALT (binary semantic signal) | High |
| C-002 | Post-task validation | Wiring hook + anti-instinct hook run after each task | No per-task hooks; single result file after all tasks | Medium |
| C-003 | Failure granularity | Per-task PASS/FAIL/INCOMPLETE known to orchestrator | Aggregate PASS/FAIL known; individual task outcomes opaque | Medium |

### Contradictions

| # | Point of Conflict | Path A Position | Path B Position | Impact |
|---|-------------------|-----------------|-----------------|--------|
| X-001 | "Exit code 0 = success" assumption | Treats exit 0 as unconditional PASS | Treats exit 0 as prerequisite, then checks result file for HALT override | High |

### Shared Assumptions

| # | Assumption | Classification | Impact |
|---|-----------|----------------|--------|
| A-001 | Claude Code subprocess exit code 0 reliably means "process completed without crash" | STATED | Foundation for both paths |
| A-002 | Exit code 0 from Claude Code means "the LLM completed its task successfully" | UNSTATED | Path A depends on this entirely; Path B adds a second check layer |
| A-003 | Per-task subprocesses will always terminate (no zombie processes) | UNSTATED | Both paths assume this |

---

## Round 1: Advocate Statements

### Advocate FOR Adding Result File Contract

**Position Summary**: Exit code 0 is a process-level signal, not a semantic-level signal. A task subprocess that exits cleanly may have encountered test failures, partial implementations, or known-bad states that it could not express through exit code alone. Adding a result file contract closes this semantic gap.

**Steelman of AGAINST position**: The opposition correctly identifies that Path A already has two post-task validation layers (wiring hook and anti-instinct hook) that Path B lacks entirely. These hooks provide genuine semantic validation that a result file alone cannot match. The opposition is also right that 10 result files per phase introduces filesystem complexity and parsing overhead that the current architecture does not need. The simplicity argument is real: fewer moving parts means fewer failure modes.

**Strengths claimed**:

1. **Semantic gap is real (A-002)**: Exit code 0 from `claude -p` means "the Claude process terminated normally," not "the task was accomplished correctly." A task worker could exit 0 after writing code that fails tests, implementing the wrong thing, or hitting an ambiguous state it chose to resolve silently. The exit code cannot distinguish these.

2. **Precedent in Path B exists for a reason**: The `_determine_phase_status()` function at executor.py:1765 was designed with a 7-priority chain precisely because exit codes proved insufficient. The PASS_NO_SIGNAL and PASS_NO_REPORT statuses (lines 1836, 1844) exist as explicit acknowledgment that exit-code-only classification produces ambiguous outcomes.

3. **Aggregation loses information**: At executor.py:1215-1216, `all_passed = all(r.status == TaskStatus.PASS for r in task_results)` reduces a list of binary pass/fail to a single boolean. If a task exits 0 but semantically failed, the orchestrator propagates a false PASS up to the phase level.

**Weaknesses identified in own position**:

- The wiring hook already reads task output and can detect semantic failures, partially closing the gap this proposal addresses.
- Instructing every per-task subprocess to write a result file adds LLM prompt overhead and risks the worker spending turns on file I/O instead of task execution.

**Concessions**:

- For tasks where the wiring hook and anti-instinct hook are both active and in `full` enforcement mode, the semantic gap is substantially narrowed even without a result file.

### Advocate AGAINST Adding Result File Contract

**Position Summary**: Path A's exit-code classification is deliberately minimal because per-task granularity already provides three independent validation layers (exit code, wiring hook, anti-instinct hook) that collectively exceed the single result-file signal Path B uses. Adding a result file contract would introduce complexity without proportionate benefit.

**Steelman of FOR position**: The FOR position correctly identifies that exit code 0 is semantically imprecise. A-002 (the unstated assumption that exit 0 = semantic success) is a genuine architectural assumption, and making it explicit would improve system transparency. The precedent in `_determine_phase_status()` does show that exit-code-only classification was insufficient for the phase-level path — that is a legitimate data point.

**Strengths claimed**:

1. **Three-layer validation already exists**: Per-task execution at executor.py:1028-1038 runs `run_post_task_wiring_hook()` and `run_post_task_anti_instinct_hook()` after every task. These hooks read the actual task output, analyze what was produced, and can reclassify status. This is semantically richer than a binary CONTINUE/HALT file because the hooks examine evidence, not self-report.

2. **Result files are self-report, hooks are third-party audit**: A result file contract asks the LLM worker to self-assess. The wiring hook and anti-instinct hook are orchestrator-side analysis of the worker's actual output. Self-report is inherently less reliable than third-party validation. Path B uses self-report because it has no hooks; Path A already has the superior alternative.

3. **Filesystem complexity scales badly**: A phase with 10 tasks would produce 10 result files. The current `_determine_phase_status()` is designed for one result file per phase. Adding per-task result files requires either: (a) a new `_determine_task_status()` parser, or (b) repurposing the existing parser with per-task paths. Both add code surface area, test burden, and failure modes (stale files, partial writes, path collisions).

4. **Aggregation already handles the failure case**: At executor.py:1215-1216, if ANY task fails (exit != 0), the phase is classified ERROR. The orchestrator does not silently swallow failures. The remaining question is only about the exit-0-but-semantically-failed edge case — which the wiring hook addresses.

5. **Prompt overhead is non-trivial**: Path A's 3-line prompt is intentionally minimal. Adding result file instructions would roughly double the prompt size and consume worker turns on file I/O. For a 10-task phase, this is 10x the overhead versus Path B's single instruction.

**Weaknesses identified in own position**:

- The wiring hook is gated by `config.wiring_gate_mode` and may be in `shadow` or `soft` mode rather than `full`. In shadow mode, it collects metrics but does not reclassify status — meaning the semantic gap is only monitored, not closed.
- If both hooks are disabled (possible in test or lightweight configurations), exit code is the ONLY signal, and A-002 becomes a single point of failure.

**Concessions**:

- When wiring hook is in `shadow` mode, the semantic gap identified by the FOR position is real and unmitigated. The system's resilience depends on hook enforcement mode.

---

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | AGAINST | 75% | Minimal prompt is a design strength, not a gap |
| S-002 | Neutral | 50% | Both classification approaches serve their granularity level |
| S-003 | AGAINST | 70% | Per-task granularity is the reason simpler classification works |
| C-001 | FOR | 65% | Exit code 0 genuinely lacks semantic precision |
| C-002 | AGAINST | 80% | Post-task hooks are richer than result-file self-report |
| C-003 | AGAINST | 70% | Per-task exit codes already provide individual outcomes |
| X-001 | FOR | 60% | The assumption is real, but hooks partially mitigate it |
| A-001 | Neutral | 50% | Shared foundation, not contested |
| A-002 | FOR | 72% | Unstated assumption; hooks mitigate but do not eliminate |
| A-003 | Neutral | 50% | Shared assumption, not contested |

**Resolved**: 7/10 points (70%)
**FOR wins**: 3 points (C-001, X-001, A-002)
**AGAINST wins**: 4 points (S-001, S-003, C-002, C-003)
**Neutral**: 3 points

---

## Convergence Assessment

- Points resolved: 7 of 10
- Alignment: 70%
- Status: Sufficient for quick-depth ruling

---

## Base Selection

**Winner: AGAINST adding a result file contract to Path A**

### Quantitative Assessment

| Metric | FOR | AGAINST |
|--------|-----|---------|
| Diff points won | 3 | 4 |
| Concessions made by opponent | 1 (hook mode dependency) | 1 (shadow mode gap) |
| Architectural consistency | Lower (duplicates Path B pattern at wrong granularity) | Higher (leverages existing hook architecture) |

### Qualitative Assessment

The AGAINST position wins because:

1. **Architectural coherence**: Path A was designed with post-task hooks as the semantic validation layer. Adding a result file contract would create a redundant signal channel that competes with the hook system rather than complementing it.

2. **Self-report vs third-party audit**: The hooks examine actual output; a result file is LLM self-assessment. The hooks are the architecturally superior signal.

3. **Proportionality**: The semantic gap (exit 0 but task failed) is real but narrow. The existing hook system addresses it when properly configured. Adding filesystem I/O to every task subprocess is disproportionate to the residual risk.

---

## Ruling

**REJECT adding a result file contract to Path A.**

### Rationale

The per-task subprocess path (Path A) intentionally uses a different validation architecture than the freeform phase path (Path B). Where Path B relies on a single result file because it has no other semantic signal, Path A has two post-task hooks (wiring and anti-instinct) that provide richer, third-party validation of task outcomes. Adding a result file contract would:

- Duplicate an inferior signal alongside a superior one
- Increase prompt complexity for every task subprocess
- Require new parsing infrastructure (`_determine_task_status()`)
- Scale poorly (N result files per phase vs 1)

### Conditional Recommendation

The ruling comes with one condition: **the wiring hook must be enforced, not just shadowed.** The FOR position correctly identified that when `wiring_gate_mode` is `shadow`, the semantic gap between exit code 0 and actual task success is unmitigated. The proper fix is not to add a result file contract but to ensure the wiring hook operates in `soft` or `full` mode for production sprints. This closes the same semantic gap without the architectural downsides.

### Action Items

1. **No change to Path A prompt** — keep the 3-line minimal prompt.
2. **No change to per-task status classification** — exit-code mapping remains sufficient when hooks are active.
3. **Document the hook dependency** — add a note to the sprint CLI docs that per-task semantic validation depends on wiring hook enforcement mode. If hooks are disabled, exit code is the only signal.
4. **Consider default wiring mode** — evaluate whether `wiring_gate_mode` should default to `soft` instead of `shadow` for production sprints, ensuring the semantic gap is always covered.

### Unresolved Items

| ID | Item | Severity | Notes |
|----|------|----------|-------|
| A-002 | Unstated assumption that exit 0 = semantic success | MEDIUM | Mitigated by hooks when enforced; document as architectural assumption |

---

## Return Contract

```yaml
merged_output_path: "docs/generated/sprint-cli/debates/debate-result-file-contract.md"
convergence_score: 0.70
artifacts_dir: "docs/generated/sprint-cli/debates/"
status: "success"
base_variant: "AGAINST"
unresolved_conflicts: 0
fallback_mode: false
failure_stage: null
invocation_method: "skill-direct"
unaddressed_invariants: []
```
