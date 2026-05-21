# Agent A — Orchestration & Step Dispatch Findings

**Slice owner**: Agent A
**Files read in full**: `src/superclaude/cli/prd/executor.py` (1029 lines), `src/superclaude/cli/prd/commands.py` (192 lines)
**Cross-referenced**: `src/superclaude/cli/prd/gates.py`, `src/superclaude/cli/prd/models.py`, `src/superclaude/cli/prd/config.py`, `src/superclaude/cli/prd/inventory.py`, `src/superclaude/cli/prd/process.py`

---

### F-A-1: `_STEP_ARTIFACT_FILES` missing entry for `build-task-file` (anchor bug — Bug 1)
**Severity (preliminary)**: CRITICAL
**Pattern tags**: P1, P3, P6
**File:line**: `src/superclaude/cli/prd/executor.py:246-251`
**Evidence**:
```python
# executor.py:246-251
_STEP_ARTIFACT_FILES: dict[str, str] = {
    "parse-request": "parsed-request.json",
    "scope-discovery": "scope-discovery-raw.md",
    "research-notes": "research-notes.md",
    "sufficiency-review": "sufficiency-review.md",
}
```
And the consumer at 267-269:
```python
artifact_name = _STEP_ARTIFACT_FILES.get(step_id)
if not artifact_name:
    return ndjson_text          # ← silent fallback to subprocess stream
```
**Trace**:
- Writer: maintainer of `_STAGE_A_STEPS` (executor.py:301-316) added `build-task-file`, `verify-task-file`, `preparation`, but did not update the parallel `_STEP_ARTIFACT_FILES` registry.
- Reader: `_resolve_step_content` (executor.py:254-293) → `_run_subprocess_step` (executor.py:522) → `_evaluate_gate` (executor.py:587). For `build-task-file`, the lookup misses, `gate_content = ndjson_text` (the extracted assistant commentary from the NDJSON stream, ~30 lines), and the STRICT 400-line gate (gates.py:359-368) fails with "Min lines: 30/400" even though the subprocess wrote a 409-line file via the Write tool.
- Persistence path: `_persist_step_artifact` (executor.py:976-1004) also short-circuits at 988-989 (`if not artifact_name: return`), so the canonical `TASK-PRD-{slug}.md` is never copied to `task_dir`.
**Reproduction sketch**: `superclaude prd run "Build a user auth system" --product test-auth --tier standard` — pipeline reaches step 7, `_resolve_step_content("build-task-file", ...)` returns NDJSON commentary, gate fails STRICT, pipeline halts with halt_step="build-task-file". This is exactly the reported failure mode.
**Confidence (own)**: 0.99 — code path is direct, dict membership is verifiable by `grep`, gates.py confirms STRICT/400 lines.

---

### F-A-2: Dynamic artifact filename (`TASK-PRD-{slug}.md`) cannot be expressed in `_STEP_ARTIFACT_FILES` (Bug 2)
**Severity (preliminary)**: CRITICAL
**Pattern tags**: P3, P5
**File:line**: `src/superclaude/cli/prd/executor.py:246-293`, `src/superclaude/cli/prd/config.py:121-137`
**Evidence**:
```python
# executor.py:267-281 — static-key lookup, no interpolation
artifact_name = _STEP_ARTIFACT_FILES.get(step_id)
...
base_name = Path(artifact_name).name
...
for match in root.rglob(base_name):
```
Slug source — config.py:121-125:
```python
product_slug = _slugify(product_name) if product_name else ""
task_dir_name = f"prd-{product_slug}" if product_slug else "prd-task"
task_dir = output_path / task_dir_name
```
**Trace**:
- task-builder prompts the subprocess to Write to `TASK-PRD-{ID}.md` where ID is derived per-run (date/slug); the actual filename varies on every invocation.
- Static dict `_STEP_ARTIFACT_FILES` is keyed by step_id and stores a literal filename. There is no mechanism in `_resolve_step_content` to (a) interpolate slug variables, (b) accept a glob pattern, or (c) accept a callable. Adding `"build-task-file": "TASK-PRD-{slug}.md"` to the dict would search for a literal file named with curly braces.
- `Path(artifact_name).name` and `root.rglob(base_name)` both treat the value as an exact filename, not a pattern.
**Reproduction sketch**: Even a hypothetical fix that adds `"build-task-file": "TASK-PRD.md"` would miss `TASK-PRD-20260520-userauth.md` files; either the dict-value type must change or `_resolve_step_content` must support patterns.
**Confidence (own)**: 0.97 — verified by reading the resolve function end-to-end; no pattern/glob/interpolation hooks exist.

---

### F-A-3: No canonical Stage B step registry — orchestration list scattered across three builder methods
**Severity (preliminary)**: HIGH
**Pattern tags**: P1, P3
**File:line**: `src/superclaude/cli/prd/executor.py:301-316`, `707-762`, `630-705`
**Evidence**: The task brief refers to `_STAGE_B_STEPS`, but no such constant exists. Stage B step_ids are minted on the fly:
```python
# executor.py:727
step_id = f"investigation-{i + 1}"
# executor.py:745
f"web-research-{i + 1}",
# executor.py:757
f"synthesis-{i + 1}",
```
`gates.py:407,426,432` defines gates keyed `"investigation"`, `"web-research"`, `"synthesis"` (no numeric suffix).
**Trace**:
- Writer: `_build_investigation_steps`/`_build_web_research_steps`/`_build_synthesis_steps` produce dynamic step_ids.
- Reader: `_execute_step` → `_run_subprocess_step:530` calls `GATE_CRITERIA.get(step_id)`. For step_id=`"investigation-1"`, lookup returns `None` because GATE_CRITERIA has only the literal key `"investigation"`. No gate runs for any individual investigation, web-research, or synthesis agent. `_persist_step_artifact` also silently does nothing for these step_ids.
- TUI registration at executor.py:366-367 only registers Stage A; Stage B steps never appear in the TUI step list.
**Reproduction sketch**: Add `print(gate)` in `_run_subprocess_step` after `GATE_CRITERIA.get(step_id)` — every investigation-N / web-research-N / synthesis-N will print `None`. The "STANDARD" gates listed in gates.py for "investigation"/"web-research"/"synthesis" are dead code at the executor layer.
**Confidence (own)**: 0.95 — verified key strings in both files and the lookup site.

---

### F-A-4: `resume_from` config attribute defined but never consumed in executor — `superclaude prd resume` is a silent no-op
**Severity (preliminary)**: HIGH
**Pattern tags**: P2, P8
**File:line**: `src/superclaude/cli/prd/executor.py` (no occurrences), `src/superclaude/cli/prd/models.py:196`, `src/superclaude/cli/prd/config.py:57,93-95,143`, `src/superclaude/cli/prd/commands.py:180`
**Evidence**: `grep -rn "resume_from" src/superclaude/cli/prd/executor.py` returns 0 matches. Defined in models.py:196, validated in config.py:93-95, plumbed via commands.py:180 — and then dropped:
```python
# commands.py:174-187 (resume subcommand)
config = resolve_config(request="", ..., resume_from=step_id)
...
executor = PrdExecutor(config)
result = executor.run()      # ← run() ignores config.resume_from
```
`PrdExecutor.run()` (executor.py:344-415) iterates `_STAGE_A_STEPS` from index 0 unconditionally; there is no skip logic conditioned on `resume_from`.
**Trace**: Reader count = 0 in the executor. The `resume` CLI subcommand will rerun the full pipeline from step 1 every time, overwriting partial artifacts. Users are silently misled about resume semantics.
**Reproduction sketch**: `superclaude prd run "x" --product foo` (Ctrl-C after step 3) → `superclaude prd resume parse-request` re-runs check-existing AND parse-request AND every subsequent step from scratch, regardless of which step was named.
**Confidence (own)**: 0.95 — grep -rn shows zero readers; the only place it's used is config-resolution validation.

---

### F-A-5: `is_parallel` field in `_STAGE_A_STEPS` tuple has zero readers
**Severity (preliminary)**: LOW
**Pattern tags**: P2
**File:line**: `src/superclaude/cli/prd/executor.py:300-316,371`
**Evidence**:
```python
# 300
# Step tuples: (step_id, step_name, prompt_builder_name, is_parallel)
_STAGE_A_STEPS: list[tuple[str, str, str, bool]] = [
    ("check-existing", "Check Existing Work", "_check_existing", False),
    ...
]
# 371
for step_id, step_name, builder_name, _ in _STAGE_A_STEPS:
```
`grep -rn "is_parallel" src/superclaude/cli/prd/` returns ONE match — the comment at line 300. Zero readers.
**Trace**: The 4th tuple slot was reserved for parallelism control but the loop always discards it (`_`). If a future maintainer sets it `True` for some step, nothing happens.
**Reproduction sketch**: Change any tuple's `False` to `True`; observe no behavioral change.
**Confidence (own)**: 1.00 — verified by direct grep.

---

### F-A-6: Stage B steps and Step 15 never registered in TUI
**Severity (preliminary)**: MEDIUM
**Pattern tags**: P1, P8
**File:line**: `src/superclaude/cli/prd/executor.py:366-367`
**Evidence**:
```python
all_step_ids = [(s[0], s[1]) for s in _STAGE_A_STEPS]
self._tui.register_steps(all_step_ids)
```
`_STAGE_A_STEPS` has 9 entries (check-existing → preparation). Stage B (investigation-N, research-qa, web-research-N, synthesis-N, synthesis-qa, assembly, structural-qa, qualitative-qa) and Step 15 (`present-complete`) are never registered.
**Trace**: Reader: `PrdTUI.update_step` is called later (executor.py:429, 455, 538, 540, 879) with step_ids the TUI has never seen. Behavior depends on PrdTUI's tolerance for unknown step_ids (cross-reference to Agent D for tui.py). At minimum, the user-visible progress display is incomplete; at worst, calls silently no-op.
**Reproduction sketch**: Watch a real `prd run` with TUI enabled — progress display freezes at "Preparation" while Stage B runs underneath.
**Confidence (own)**: 0.85 — registration source is unambiguous; consumer behavior deferred to Agent D.

---

### F-A-7: `_handle_shutdown` accesses non-existent `last.step` attribute → AttributeError on signal interrupt
**Severity (preliminary)**: HIGH
**Pattern tags**: P1, P8
**File:line**: `src/superclaude/cli/prd/executor.py:957-970`, `src/superclaude/cli/prd/models.py:220-235`
**Evidence**:
```python
# executor.py:957-970
def _handle_shutdown(self, result: PrdPipelineResult) -> None:
    ...
    completed = [r for r in self._step_results if r.status.is_terminal]
    if completed:
        last = completed[-1]
        last_step = (
            getattr(last.step, "name", "unknown") if last.step else "unknown"
        )
```
But `PrdStepResult` (models.py:220-234) has NO `step` field:
```python
class PrdStepResult(StepResult):
    exit_code: int = 0
    output_bytes: int = 0
    error_bytes: int = 0
    artifacts_produced: list[str] = field(default_factory=list)
    agent_type: str = ""
    fix_cycle: int = 0
    qa_verdict: Optional[str] = None
```
`StepResult` (defined in pipeline.models — cross-reference to Agent C) likely has no `step` field either; if it did, the executor never assigns `step_result.step = ...` anywhere in `_run_subprocess_step` or `_run_check_existing` (verified by grep).
**Trace**: Writer: nothing in the PRD module assigns `step` on a PrdStepResult. Reader: `_handle_shutdown` accesses `last.step` and `last.step.name`. If `StepResult` declares `step` (likely as `Optional[Something] = None`), the `if last.step` branch goes false and returns `"unknown"` — masking a real bug. If `StepResult` lacks `step`, `last.step` raises `AttributeError`, crashing during SIGINT handling. Either way the field is never populated, so the recorded `halt_step` is meaningless.
**Reproduction sketch**: `kill -INT $(pgrep -f "superclaude prd run")` during a long pipeline. Either AttributeError aborts the shutdown handler (no resume state written), or `halt_step="unknown"` is recorded (resume info useless). Test under both StepResult schemas.
**Confidence (own)**: 0.85 — local code is unambiguous; severity depends on the upstream StepResult schema (deferred to Agent C).

---

### F-A-8: `result.outcome = "success"` set unconditionally after Stage B even if assembly STRICT halt was already recorded
**Severity (preliminary)**: MEDIUM
**Pattern tags**: P8
**File:line**: `src/superclaude/cli/prd/executor.py:396-409,676-689`
**Evidence**:
```python
# 676-689
assembly_result = self._execute_step("assembly", ...)
self._step_results.append(assembly_result)
result.step_results.append(assembly_result)
if assembly_result.status.is_failure:
    gate = GATE_CRITERIA.get("assembly")
    if gate and gate.enforcement_tier == "STRICT":
        result.outcome = "halt"
        result.halt_step = "assembly"
        return                       # returns from _execute_stage_b only
```
And back in `run()`:
```python
# 392-409
if result.outcome != "halt":
    self._execute_stage_b(result)

if result.outcome != "halt":
    ...
        completion_result = self._execute_step("present-complete", ...)

if result.outcome != "halt":
    result.outcome = "success"
```
This branch is actually correct — assembly's halt path sets `outcome = "halt"`, the subsequent `if result.outcome != "halt"` skips Step 15, and the final guard skips the "success" assignment. **However**, structural-qa (executor.py:692-697) and qualitative-qa (700-705) results are appended but their failure does NOT halt the pipeline (no `is_failure`/STRICT check around them), even though gates.py:475,488 marks both as STRICT. A STRICT failure in structural-qa or qualitative-qa is recorded as a step result but `outcome` stays `"success"`.
**Trace**: Writer: `_execute_step` returns a PrdStepResult with status HALT/VALIDATION_FAIL. Reader: Stage B's assembly branch checks it; structural-qa and qualitative-qa branches do NOT. The STRICT enforcement_tier defined in gates.py is honored inside `_run_subprocess_step:534` (which sets status=HALT on STRICT gate fail), but the higher-level outcome propagation only fires for assembly.
**Reproduction sketch**: Force a STRICT semantic-check failure in structural-qa output → step status=HALT but result.outcome="success", `superclaude prd run` exits 0 despite the documented STRICT gate.
**Confidence (own)**: 0.80 — verified by reading the Stage B control flow; semantics of "STRICT" deferred to Agent B.

---

### F-A-9: Brittle verdict literal matching in `_determine_status`
**Severity (preliminary)**: MEDIUM
**Pattern tags**: P4
**File:line**: `src/superclaude/cli/prd/executor.py:577-583`
**Evidence**:
```python
if "qa" in step_id or "review" in step_id:
    if '"verdict": "FAIL"' in output or "verdict: FAIL" in output:
        return PrdStepStatus.QA_FAIL
    if '"verdict": "PASS"' in output or "verdict: PASS" in output:
        return PrdStepStatus.PASS
```
**Trace**: The literal `'"verdict": "FAIL"'` requires exactly one space after the colon. JSON emitted with no space (`{"verdict":"FAIL"}`), different quoting (`'verdict': 'FAIL'`), or capitalised keys (`"Verdict"`) all miss. Reader chain: `_run_subprocess_step:527` → `_determine_status` decides QA_FAIL vs PASS_NO_SIGNAL. A miss demotes QA failures to PASS_NO_SIGNAL (which `is_success` returns True for, models.py:139-141), so the QA fix cycle in `_execute_qa_fix_cycle:854` exits at the first cycle and a failing QA step is silently treated as passing.
**Reproduction sketch**: QA subprocess emits `{"verdict":"FAIL","reasons":[...]}` (compact JSON, no spaces). Executor classifies as PASS_NO_SIGNAL; fix cycle terminates without spawning gap-fillers.
**Confidence (own)**: 0.90 — literal string match is verifiable in source; the cascade to PASS_NO_SIGNAL is direct from `_determine_status` falling through to line 585.

---

### F-A-10: `_extract_text_from_stream_json` silently falls back to raw NDJSON when parse yields no text blocks
**Severity (preliminary)**: MEDIUM
**Pattern tags**: P4, P6
**File:line**: `src/superclaude/cli/prd/executor.py:99-130`
**Evidence**:
```python
return "\n".join(texts) if texts else raw
```
**Trace**: When the subprocess emits NDJSON but the "assistant"/"message"/"content" path is empty (e.g., only tool_use blocks, system messages, or a different schema version), the function returns the entire raw NDJSON. Reader: `_run_subprocess_step:518` assigns this to `output_text`; the result is then used both for sentinel detection (which won't find `^EXIT_RECOMMENDATION:`) and as the fallback in `_resolve_step_content`. This compounds F-A-1: when there is no on-disk artifact AND the assistant emitted only tool_use blocks, gate evaluation runs against raw NDJSON, inflating line counts with `{"type":"tool_use",...}` JSON lines and possibly accidentally passing min_lines gates that should have failed.
**Reproduction sketch**: A subprocess that calls Write 10 times and emits one short text response → `texts` populated, but if it emits ZERO text and only tool_use blocks, the raw NDJSON (often 100+ lines for verbose tool_use chatter) bypasses the min_lines gate as a false positive.
**Confidence (own)**: 0.85 — fallback is direct; impact depends on output-format invariants enforced by process.py (Agent D).

---

### F-A-11: `_resolve_step_content` chooses largest file by raw byte length — no schema validation
**Severity (preliminary)**: MEDIUM
**Pattern tags**: P3, P6
**File:line**: `src/superclaude/cli/prd/executor.py:279-291`
**Evidence**:
```python
best_content = ""
for root in search_roots:
    for match in root.rglob(base_name):
        skip_parts = {"node_modules", ".git", "__pycache__"}
        if "-output.txt" in match.name or skip_parts & set(match.parts):
            continue
        try:
            content = match.read_text(encoding="utf-8", errors="replace")
            if len(content) > len(best_content):
                best_content = content
        except OSError:
            continue
```
**Trace**: Searches `task_dir` AND `task_dir.parent` (the project root). For `research-notes.md`, `rglob` from the project root walks the ENTIRE repository. If a prior PRD run or an unrelated documentation file happens to be named `research-notes.md` and is larger than the current run's file, it wins. There is no scoping to the current step_id's task_dir, no mtime check, no provenance check. Cross-PRD-run contamination is possible.
**Reproduction sketch**: Create `/config/workspace/IronClaude/docs/research-notes.md` with 1000 lines of unrelated content, then `superclaude prd run "auth" --product authy` — `_resolve_step_content("research-notes", ...)` will pick up the docs file because `task_dir.parent` rglob reaches it.
**Confidence (own)**: 0.85 — code path is direct; severity depends on layout in real `.dev/` directories.

---

### F-A-12: Persistence guard at line 545 short-circuits on STANDARD gate failure as well, fragmenting Stage A handoff
**Severity (preliminary)**: MEDIUM
**Pattern tags**: P6, P8
**File:line**: `src/superclaude/cli/prd/executor.py:542-546`
**Evidence**:
```python
# Persist artifact file for downstream steps whenever the
# subprocess completed (exit 0). STANDARD gate failures don't
# halt the pipeline, so downstream steps still need the data.
if exit_code == 0 and gate_content.strip():
    self._persist_step_artifact(step_id, gate_content)
```
The comment states the right intent. The guard is `exit_code == 0`, not `status.is_failure`. **But** `_persist_step_artifact` (executor.py:987-989) silently returns when `artifact_name` is missing. So for the 12+ step_ids that lack `_STEP_ARTIFACT_FILES` entries (everything past sufficiency-review plus all Stage B), no artifact is ever persisted to the canonical location. Downstream prompt builders that load by filename will fall back to whatever the subprocess happened to leave on disk (handled by `_resolve_step_content`'s search), which couples step N+1's prompt to step N's I/O side effects rather than to a deterministic artifact path.
**Trace**: Writer: only 4 step_ids ever trigger `artifact_path.write_text`. Reader: prompt builders in `prompts.py` (cross-reference to Agent E) load by canonical filename; if they look for `task-file.md` or `assembly-output.md` they find nothing.
**Reproduction sketch**: Inspect `task_dir/` after a complete run — only `parsed-request.json`, `scope-discovery-raw.md`, `research-notes.md`, `sufficiency-review.md` will be present at the canonical path. All other artifacts live wherever the subprocess wrote them (likely `task_dir/results/` or `.dev/`).
**Confidence (own)**: 0.90 — verified against the dict.

---

### F-A-13: `stall_timeout * 30` magic multiplier — wall timeout depends on a config knob named for stall cadence
**Severity (preliminary)**: LOW
**Pattern tags**: P7
**File:line**: `src/superclaude/cli/prd/executor.py:499`, `src/superclaude/cli/prd/models.py:190-191`
**Evidence**:
```python
# executor.py:499
timeout_seconds=self._config.stall_timeout * 30,
```
With defaults `stall_timeout=120` (models.py:190), this yields 3600s overall timeout per subprocess. The config field name suggests "kill on N seconds of no output", but here it sets total wall time via a hard-coded 30x multiplier. Users tuning `stall_timeout` to shorten stall detection will inadvertently and proportionally shrink overall wall timeout.
**Trace**: Reader: `PrdClaudeProcess.__init__` (process.py:140 — cross-reference Agent D) accepts `timeout_seconds` as the overall wait timeout. Writer: executor passes `stall_timeout * 30`. Coupling is undocumented.
**Reproduction sketch**: User sets `--max-turns 1000` and (hypothetically) `stall_timeout=30` to detect stalls fast → overall timeout becomes 900s, cutting off long subprocesses.
**Confidence (own)**: 0.80 — multiplier is explicit; semantic confusion is a judgment call.

---

### F-A-14: Stage B parallel step results appended TWICE to `self._step_results`
**Severity (preliminary)**: MEDIUM
**Pattern tags**: P8
**File:line**: `src/superclaude/cli/prd/executor.py:463-467, 792-802`
**Evidence**: `_execute_step` does NOT append to `self._step_results` itself, but it DOES return the result and the caller appends. However for parallel execution:
```python
# 794-802 inside _execute_parallel_steps
step_result = future.result()
...
self._step_results.append(step_result)
result.step_results.append(step_result)
```
And `_execute_step` runs on the worker thread. `_execute_step` calls `_diagnostics.record_step(step_result)` at line 462 and stores `_context_summaries[step_id]` at 465. Stage A's `run()` loop (executor.py:371-389) also appends — but only AFTER `_execute_step` returns. Reading carefully: Stage A appends exactly once (line 377). Stage B parallel appends exactly once (line 801-802). Stage B's `_execute_qa_fix_cycle` appends BOTH the qa_result (line 833, 846) AND the fix_result (890-891) explicitly — and `_execute_step` does NOT internally append, so the totals are consistent. **Retracting the duplicate-append claim**; however `_step_results` and `result.step_results` are maintained as two parallel lists with separate append sites at every callsite (run loop, _execute_stage_b, _execute_qa_fix_cycle, _execute_parallel_steps). Any future callsite that appends to only one drifts silently.
**Trace**: P8 risk: state machine maintains two parallel lists with no invariant enforcement. Future maintenance hazard, not an active bug.
**Reproduction sketch**: Add a new callsite that appends to only `result.step_results` — diagnostics and TUI based on `self._step_results` will silently undercount.
**Confidence (own)**: 0.70 — risk only, not an active defect; included for completeness because the duplicate-list pattern is a recognised P1/P8 anti-pattern.

---

### F-A-15: `_estimate_turns` substring matching collides — `verify-task-file` returns 10 instead of intended weight
**Severity (preliminary)**: LOW
**Pattern tags**: P3, P7
**File:line**: `src/superclaude/cli/prd/executor.py:1006-1019`
**Evidence**:
```python
@staticmethod
def _estimate_turns(step_id: str) -> int:
    if "qa" in step_id or "verify" in step_id or "review" in step_id:
        return 10
    if "assembly" in step_id or "build" in step_id:
        return 30
    if "investigation" in step_id or "synthesis" in step_id:
        return 20
    return 15
```
**Trace**:
- `verify-task-file` matches `"verify"` → 10. Likely intended to be a heavy step (verifying a 400+ line task file end-to-end), getting only 10 turns of budget.
- `qualitative-qa` and `structural-qa` match `"qa"` → 10. Reasonable for QA.
- `build-task-file` matches `"build"` → 30. OK.
- `sufficiency-review` matches `"review"` → 10. May be acceptable.
- `research-qa-fix-1` matches `"qa"` → 10, but gap-filling is heavier work than QA verification.
- Substring ordering: `"build" in step_id` would also match a hypothetical `"build-investigation"`, which would hit the 30 branch before the 20 branch. Brittle.
**Reproduction sketch**: Add a step_id like `"build-investigation-1"` → returns 30, even though investigation logic intends 20.
**Confidence (own)**: 0.75 — substring collision is verifiable; impact depends on turn-budget headroom per step.

---

### F-A-16: Step 15 (`present-complete`) has neither artifact entry nor TUI registration, and its gate is LIGHT but treated as terminal
**Severity (preliminary)**: LOW
**Pattern tags**: P1, P8
**File:line**: `src/superclaude/cli/prd/executor.py:396-404`, `src/superclaude/cli/prd/gates.py:501-504`
**Evidence**: `present-complete` is run by `_execute_step("present-complete", ...)` (line 398-402) but it is not in `_STAGE_A_STEPS`, not in `_STEP_ARTIFACT_FILES`, and not registered in the TUI. Its gate (gates.py:504) is LIGHT — meaning even a STRICT-tier failure wouldn't halt anyway. However if the subprocess errors out (`exit_code != 0`), `_run_subprocess_step:548-552` returns ERROR status; the loop in `run()` does NOT check this — line 405 just appends the result and then 407-408 sets `outcome = "success"` unconditionally because `result.outcome != "halt"`.
**Trace**: ERROR in present-complete → `outcome = "success"` and exit 0. The "completion" step is effectively cosmetic. Cross-reference Agent B for whether LIGHT semantics intend this.
**Reproduction sketch**: Cause present-complete to crash (e.g. budget exhaustion) → CLI reports success.
**Confidence (own)**: 0.75 — gate semantics dependent on Agent B's review.

---

### F-A-17: Sentinel detection runs on extracted text but gate evaluation runs on disk content — they can disagree
**Severity (preliminary)**: MEDIUM
**Pattern tags**: P6
**File:line**: `src/superclaude/cli/prd/executor.py:518-532`
**Evidence**:
```python
output_text = _extract_text_from_stream_json(raw_output) if raw_output else ""
gate_content = _resolve_step_content(step_id, self._config.task_dir, output_text)
status = self._determine_status(exit_code, output_text, step_id)  # ← uses NDJSON-extracted text
...
gate_passed = self._evaluate_gate(step_id, gate, gate_content)    # ← uses disk file (if found)
```
**Trace**: For step_ids with a `_STEP_ARTIFACT_FILES` entry where the on-disk file exists, `gate_content` is the disk file (e.g. 400+ line research-notes.md) but `status` derivation reads the NDJSON commentary. The subprocess may emit `^EXIT_RECOMMENDATION: HALT` in its narration even though the disk artifact passes the gate, or vice versa. The two read different sources and reach independent verdicts. Specifically, sentinel detection on NDJSON commentary that's 30 lines long, and gate evaluation on a 400-line disk file, can produce a "HALT sentinel + gate PASS" outcome — `_determine_status` returns HALT, gate code never runs (because `status.is_success` is False at line 531).
**Reproduction sketch**: Subprocess emits a hortative sentinel in narration that doesn't reflect artifact quality — pipeline halts despite a satisfactory artifact on disk.
**Confidence (own)**: 0.80 — the source-mismatch is direct; whether it surfaces in practice depends on subprocess prompts (Agent E).

---

## Considered and rejected

- **`_extract_text_from_stream_json` discarding fields other than "text"**: by design; tool_use / thinking blocks are not gate-relevant. Not a defect.
- **`TurnLedger.consume` having no callers in executor.py**: `consume` is called elsewhere? Verified `grep` shows zero callers in executor.py. Borderline P2 finding, but the field is consumed inside `TurnLedger.remaining` (no, it's not — `remaining = total_budget - allocated`). The `consumed` field is genuinely never read for any decision; reported only to log lines if any. Excluded because allocated-based budget guarding is the safer of the two semantics and `consume` is harmless dead code; mark for Agent F as a test-coverage gap rather than a runtime defect.
- **`_strip_json_fencing` returning whole text when no JSON fence found**: graceful fallback, not a defect. The downstream `json.loads()` will raise if the result isn't JSON; that's an upstream prompt issue, not an executor issue.
- **`_CODE_BLOCK_PATTERN` greediness**: regex uses `[\s\S]*?` (non-greedy) and operates per-document; cross-block matches would only fire if a code block is unclosed, which is an LLM output anomaly. Not pursued.
- **`_signal_handler.shutdown_requested` polled but not propagated to child subprocess**: PrdClaudeProcess.wait may not be interruptible by the flag. Defer to Agent D — this is process.py's domain.
- **Output-path semantics (`--output` flag)**: file-vs-directory ambiguity. The slug-derived task_dir lives at `output_path / f"prd-{slug}"`. Path resolution is config.py territory; left for Agent C.
- **Parallel execution worker pool size of 10**: matches NFR-PRD.7 comment; not a defect.
- **`PrdSignalHandler` restore order**: install/uninstall mirror correctly. Not a defect.
- **`_build_prompt` `TypeError` swallow**: deliberately falls back to calling without `context_summaries`; documented in docstring. Not a defect.
- **`_persist_step_artifact` not capturing OSError details**: logs ARTIFACT_WRITE_FAIL but doesn't change status. Borderline — logged only, no propagation. Excluded as low-severity P8; flagged here for awareness.
- **`_STAGE_A_STEPS` ordering**: matches the 9-step Stage A documented in the module docstring. Not a defect.
