# Solution 3: STDOUT/RESULT-CONTRACT CAPTURE

## Status
Design doc for future debate. Confirmed root cause: document-producing steps emit their real output via the Write tool at unpredictable paths; the pipeline captures subprocess NDJSON stdout, which `_resolve_step_content` (executor.py:266-365) says "only captures the assistant's commentary" (~24 lines). Gate then counts the thin commentary and fails.

---

## Summary

Stop depending on the agent writing its document to an unpredictable disk location. Make the document flow through a reliable channel: **(a)** strengthen the NDJSON/stream-json parser to extract the agent's full final assistant message (the `result`/final text), and **(b)** change prompts so document-producing steps emit the full document as their final message (no Write tool needed) OR write to a single canonical stdout-mirrored path. Add working-directory isolation to prevent agents from self-contaminating source directories (e.g. `/config/workspace/Octodive/.dev/specs/`).

This is Solution 3 of 3. It competes with:
- **Solution 1** (Write-to-canonical-path enforcement): force every agent to write to a deterministic path, then read that path.
- **Solution 2** (Tool-call interception): intercept the agent's Write tool call inside the subprocess and stream it back to the parent.

---

## Design

### (a) Capture Half — Strengthen NDJSON Parser

**Current state (executor.py:105-136)**
```python
def _extract_text_from_stream_json(raw: str) -> str:
    texts: list[str] = []
    for line in raw.splitlines():
        ...
        obj = json.loads(line)
        message = obj.get("message") or {}
        content = message.get("content")
        ...
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text = block.get("text", "")
                if text:
                    texts.append(text)
    return "\n".join(texts) if texts else raw
```

This only extracts `assistant` message text blocks. It misses the **final `result` event** that `claude --output-format stream-json` emits when the session ends. The `result` event contains the full final assistant response — the document the agent produced.

**Proposed change: executor.py:105-136**

Replace `_extract_text_from_stream_json` with a two-pass extractor:

1. **Pass 1: Look for `result` event** — this is the authoritative final output.
   The `stream-json` format emits a final line like:
   ```json
   {"type":"result","result":"<full assistant final message>"}
   ```
   If found, return `result` verbatim (it is the document).

2. **Pass 2: Fallback to assistant message accumulation** (current behavior) — if no `result` event is present (older CLI versions, truncated streams), fall back to accumulating text blocks from `assistant` messages.

Concrete implementation:
```python
def _extract_text_from_stream_json(raw: str) -> str:
    """Extract assistant text from stream-json (NDJSON) output.

    Priority:
    1. Final ``result`` event (authoritative full output).
    2. Accumulated ``assistant`` message text blocks (fallback).
    3. Raw string (last resort).
    """
    result_text: str | None = None
    texts: list[str] = []

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue

        # Pass 1: result event
        if obj.get("type") == "result":
            result_text = obj.get("result", "")
            continue

        # Pass 2: assistant message accumulation
        message = obj.get("message") or {}
        content = message.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text = block.get("text", "")
                if text:
                    texts.append(text)

    if result_text is not None:
        return result_text
    return "\n".join(texts) if texts else raw
```

**Why this works:**
- When the agent emits the full document as its final message, the CLI captures it in the `result` event.
- The `result` event is a single string, not fragmented across multiple assistant turns, so there is no interleaving with tool-use commentary.
- Token limits: the `result` event is subject to the model's output token limit (e.g. 128K for Opus 4). For an 800-line PRD (~15-20K tokens), this is well within bounds. For future 2000-line heavyweight PRDs, we may hit truncation; see Risks.

**Blast radius:**
- This changes the capture path shared by **ALL** steps. Every step's `output_text` now prefers `result` over accumulated assistant messages.
- **Risk:** If a step's final message is NOT the document (e.g. the agent says "Done!" after writing to disk), the `result` event will contain "Done!" and the gate will see empty/short content.
  - Mitigation: this is addressed by the Contract half (below) — we change prompts so the final message IS the document.
- **Risk:** QA steps (`research-qa`, `synthesis-qa`, `structural-qa`, `qualitative-qa`) currently write their reports to `qa/*.md` and the NDJSON stdout holds commentary + verdict. If we capture `result`, we may capture the report instead of the commentary, which is actually **desired** for gate evaluation (the report is what the gate should evaluate). However, `_determine_status` (executor.py:645-676) looks for `"verdict": "FAIL"` in `output_text` (the NDJSON-extracted text). If the `result` event contains the report, the verdict string is still inside it, so sentinel/verdict detection still works.
  - Verification needed: confirm that `result` events include the full text including `EXIT_RECOMMENDATION` and verdict strings. If the CLI strips these, sentinel detection breaks.

### (b) Contract Half — Prompt Changes

**Option B1 (preferred): Emit document as final message, no Write tool**

Change document-producing prompts so the agent's final assistant message IS the document, rather than writing it to disk via Write/Edit.

Affected prompts (prompts.py):
- `build_scope_discovery_prompt` (line 110-191)
- `build_research_notes_prompt` (line 194-266)
- `build_task_file_prompt` (line 359-454)
- `_render_investigation_prompt` (line 736-808)
- `_render_web_research_prompt` (line 823-866)
- `_render_synthesis_prompt` (line 999-1044)
- `build_assembly_prompt` (line 1149-1246)

For each, replace instructions like:
```
Write a markdown document with these sections:
...
Write the task file to: {path}
```

With:
```
Produce the full markdown document below. Do NOT use the Write tool.
Your final assistant message must contain the complete document.
```

**Token/truncation analysis:**
- Scope discovery: ~50-200 lines (~2-8K tokens) — safe.
- Research notes: ~100-300 lines (~4-12K tokens) — safe.
- Task file: ~400-800 lines (~15-30K tokens) — safe for 128K context models, but approaching limits for older models.
- Assembly PRD: ~800-2500 lines (~30-80K tokens) — **risky**. An 800-line PRD is ~15-20K tokens; a 2500-line heavyweight PRD is ~50-60K tokens. This is within Opus 4's 128K output limit but leaves little headroom. If the model truncates, the gate fails on `min_lines`.
  - Mitigation: for assembly, keep the Write-tool path as a fallback. The prompt can say: "Emit the full PRD as your final message. If the document exceeds 1500 lines, write it to {output_path} instead and emit 'WRITTEN_TO_DISK' as your final message." The capture logic then checks for `WRITTEN_TO_DISK` and falls back to `_resolve_step_content` disk recovery.

**Option B2 (fallback): Write to canonical stdout-mirrored path**

If Option B1 is too risky for large documents, keep the Write tool but constrain the path to a canonical location inside `task_dir`, and mirror it to stdout.

For each prompt, change:
```
Write the file to: {path}
```
to:
```
Write the file to: {canonical_path}
After writing, read the file back and echo its full contents as your final message.
```

This is less clean than B1 but preserves the Write tool for incremental writing while still ensuring the `result` event contains the document.

**Recommended hybrid:**
- Steps with small outputs (`parse-request`, `scope-discovery`, `research-notes`, `sufficiency-review`, `verify-task-file`, `preparation`, `investigation`, `web-research`, `synthesis`, `qa-*`): use **B1** (final message is the document).
- Steps with large outputs (`build-task-file`, `assembly`): use **B2** (write to disk, then echo back as final message). The echo ensures the `result` event is populated, but the Write tool provides a backup on disk.

### Working-Directory Isolation

**Problem:** Agents write into source directories like `/config/workspace/Octodive/.dev/specs/` because their working context includes the full repo and they are instructed to write documents to paths like `/config/workspace/Octodive/.dev/specs/scope-discovery.md`.

**Solution: executor.py:560-640 (`_run_subprocess_step`)**

Launch the subprocess with `cwd=task_dir` and inject a `CLAUDE_WORK_DIR` env var pointing to `task_dir`.

Changes:
1. In `process.py:114-156` (`ClaudeProcess.start`), add `cwd` support:
   ```python
   popen_kwargs = {
       "stdin": subprocess.PIPE,
       "stdout": self._stdout_fh,
       "stderr": self._stderr_fh,
       "env": self.build_env(env_vars=self._extra_env_vars),
       "cwd": str(self.output_file.parent),  # or explicit cwd param
   }
   ```

2. In `PrdClaudeProcess.__init__` (process.py:132-161), pass `cwd`:
   ```python
   super().__init__(
       ...,
       env_vars={"CLAUDE_WORK_DIR": str(config.task_dir)},
   )
   ```

3. In prompts, replace references to `/config/workspace/Octodive/.dev/specs/` or repo-root paths with `{task_dir}` or `CLAUDE_WORK_DIR`.

**Blast radius:**
- Changing `cwd` affects all file paths the agent resolves. If the prompt says "Read `src/foo.py`", the agent must resolve it relative to the repo root, not `task_dir`.
  - Mitigation: pass the repo root as an explicit `--file` arg or env var, and instruct the agent to use absolute paths.
- Agents that use `Glob` to discover the project structure need the repo root as their search root.
  - Mitigation: include the repo root in the prompt explicitly: "The project root is {work_dir}. Use absolute paths when reading files."

### Gate Criteria Adjustments

With the capture+contract fix, gate content comes from `result` events, not disk files. Some gates currently rely on disk-file side effects:

- `assembly` gate (gates.py:459-481): `min_lines=800`, checks for PRD template sections. With B1/B2, the gate content is the `result` event text, which is the full PRD — correct.
- `research-qa` gate (gates.py:421-432): `min_lines=20`, checks for verdict. The QA agent's final message should be the report (including verdict) — correct.
- `build-task-file` gate (gates.py:367-394): `min_lines=400`, checks frontmatter + phases. The task file content is in the `result` event — correct.

No gate changes are strictly required, but we should add a semantic check to detect truncation:
```python
def _check_no_truncation_marker(content: str) -> bool | str:
    if "[TRUNCATED" in content or content.rstrip().endswith("..."):
        return "Content appears truncated — model output limit may have been reached"
    return True
```

---

## Why This Approach

| Criterion | Solution 3 (this) | Solution 1 (canonical Write) | Solution 2 (tool interception) |
|---|---|---|---|
| **Reliability** | High — uses CLI's native `result` event | Medium — agents often ignore path instructions | High — but requires hooking tool calls |
| **Implementation complexity** | Low-Medium — parser + prompt changes | Low — just change prompts | High — requires subprocess instrumentation |
| **Blast radius** | High — all steps' capture path | Low — only document-producing steps | Medium — all tool-using steps |
| **Backward compat** | Good — fallback to current behavior | Good — no code changes | Poor — new infrastructure |
| **Token limit risk** | Real for 1500+ line docs | None | None |
| **Working-dir isolation** | Addressed | Not addressed | Not addressed |

Solution 3 is the best balance of reliability and implementation cost. It fixes the root cause (unreliable capture channel) without requiring complex subprocess instrumentation (Solution 2) or trusting agents to follow path instructions (Solution 1).

---

## Risks & Footguns (Ranked)

### 1. Blast radius across ALL steps (CRITICAL)
Changing `_extract_text_from_stream_json` affects every step in the pipeline. If the `result` event contains something unexpected (e.g. a tool-use summary instead of the document), gates for unrelated steps may fail.
- **Mitigation:** Extensive testing on all 15 step types. Add a feature flag `use_result_event` defaulting to False, enabling gradual rollout.

### 2. Token truncation for large documents (HIGH)
An 800-line PRD is ~20K tokens; a 2500-line heavyweight PRD is ~60K tokens. Opus 4's output limit is 128K, but other models (Sonnet, Haiku) have lower limits. If the model truncates, the gate fails on `min_lines` and the PRD is incomplete.
- **Mitigation:** Hybrid B1/B2 approach — use Write tool for large documents, echo back for capture. Add truncation detection semantic check.

### 3. Sentiment/verdict detection breakage (HIGH)
`_determine_status` (executor.py:645-676) searches `output_text` for `EXIT_RECOMMENDATION` and verdict strings. If the `result` event strips these markers (e.g. the CLI only returns the final assistant text without the sentinel), status detection breaks.
- **Mitigation:** Verify with real CLI runs that `result` events include the full assistant text including sentinels. If not, accumulate assistant messages separately for sentinel detection while using `result` for gate content.

### 4. Working-directory isolation breaks file discovery (MEDIUM)
Changing `cwd` to `task_dir` may break agents that use relative paths to discover the codebase.
- **Mitigation:** Pass `work_dir` explicitly in prompts and env vars. Test scope-discovery and investigation steps thoroughly.

### 5. Prompt drift — agents still Write to arbitrary paths (MEDIUM)
Even with prompt changes, agents may still use Write tool out of habit or because the prompt includes file paths.
- **Mitigation:** Add a system prompt instruction: "You do not have access to the Write tool." (This requires CLI support for disabling specific tools, which may not exist.)
- **Alternative:** Post-process: after subprocess exit, scan for new files under `task_dir` and treat them as artifacts. This is a weaker mitigation.

### 6. Resume state inconsistency (MEDIUM)
Resume logic checks for existing artifacts on disk. If we stop writing artifacts to disk (B1), resume cannot find them.
- **Mitigation:** Always write artifacts to disk in `_persist_step_artifact` (executor.py:1145-1173), even if gate content comes from `result`. The disk copy is for resume; the `result` event is for gate evaluation.

### 7. Parallel step interference (LOW)
Parallel steps (investigation, web-research, synthesis) share the same `task_dir` parent. Working-directory isolation must not collide.
- **Mitigation:** Each parallel step already has its own output path derived from `step_id`. Ensure `cwd` is still `task_dir`, not a per-step subdirectory.

---

## Backward Compatibility

- **NDJSON parser:** The new `_extract_text_from_stream_json` is backward-compatible: if no `result` event is present, it falls back to the current assistant-message accumulation.
- **Prompts:** Prompt changes are additive — old prompts still work, they just don't populate the `result` event optimally.
- **Gate criteria:** No changes required, but adding truncation detection is recommended.
- **Resume:** No changes required if we continue persisting artifacts to disk.
- **Feature flag:** Recommend adding `config.capture_mode = "result" | "legacy"` to allow rollback.

---

## Test Plan

### Unit tests (`/config/workspace/IronClaude/tests/cli/prd/test_executor.py`)

1. **`test_extract_text_prefers_result_event`**
   - Input: NDJSON with both `assistant` messages and a final `result` event.
   - Assert: returns `result` text, not accumulated assistant messages.

2. **`test_extract_text_fallback_to_assistant_messages`**
   - Input: NDJSON without `result` event.
   - Assert: returns accumulated assistant text (current behavior).

3. **`test_extract_text_result_event_empty_fallback`**
   - Input: NDJSON with `result: ""`.
   - Assert: returns empty string (not fallback), because `result` was present.

4. **`test_resolve_step_content_uses_result_text`**
   - Mock `_extract_text_from_stream_json` returning a long document.
   - Assert: `_resolve_step_content` returns that text without disk search.

5. **`test_run_subprocess_step_cwd_isolation`**
   - Mock `subprocess.Popen` and inspect `cwd` kwarg.
   - Assert: `cwd=str(config.task_dir)`.

6. **`test_determine_status_finds_verdict_in_result_text`**
   - Input: `result` event text containing `"verdict": "FAIL"`.
   - Assert: status is `QA_FAIL`.

### Prompt tests (`/config/workspace/IronClaude/tests/cli/prd/test_prompts.py`)

7. **`test_scope_discovery_prompt_requires_final_message`**
   - Assert: prompt contains instruction to emit document as final message.

8. **`test_assembly_prompt_has_echo_fallback`**
   - Assert: prompt contains "echo its full contents" or similar for large documents.

9. **`test_investigation_prompt_no_write_tool`**
   - Assert: prompt does not reference Write tool for output file.

### Integration tests (`/config/workspace/IronClaude/tests/cli/prd/test_integration.py`)

10. **`test_stage_a_document_steps_pass_gate`**
    - Run steps 2-5 with mock subprocess returning `result` events.
    - Assert: gates pass with `min_lines` satisfied.

11. **`test_assembly_step_large_document_not_truncated`**
    - Run assembly with 1500-line mock document in `result` event.
    - Assert: gate passes, no truncation marker detected.

12. **`test_qa_step_verdict_detected_in_result`**
    - Run `research-qa` with mock `result` containing report + verdict.
    - Assert: status is `PASS` or `QA_FAIL` correctly.

### E2E tests (`/config/workspace/IronClaude/tests/cli/prd/test_e2e.py`)

13. **`test_e2e_prd_pipeline_with_result_capture`**
    - Full pipeline run with `capture_mode="result"`.
    - Assert: all gates pass, output PRD exists at `config.output_path`.

14. **`test_e2e_resume_after_stage_a`**
    - Run Stage A, interrupt, resume from Stage B.
    - Assert: resume finds artifacts on disk, continues successfully.

15. **`test_e2e_cwd_isolation_no_source_contamination`**
    - Run pipeline on repo with `/config/workspace/Octodive/.dev/specs/` directory.
    - Assert: no new files appear in `/config/workspace/Octodive/.dev/specs/` after pipeline completes.

---

## Effort Estimate

| Task | Effort | Owner |
|---|---|---|
| Strengthen NDJSON parser (`_extract_text_from_stream_json`) | 2h | Backend |
| Add `cwd` + env var isolation to `ClaudeProcess` / `PrdClaudeProcess` | 2h | Backend |
| Update document-producing prompts (B1/B2 hybrid) | 4h | Prompt engineer |
| Add truncation detection semantic check | 1h | Backend |
| Add `capture_mode` feature flag | 1h | Backend |
| Unit tests (test_executor.py) | 3h | QA |
| Prompt tests (test_prompts.py) | 2h | QA |
| Integration tests (test_integration.py) | 4h | QA |
| E2E tests (test_e2e.py) | 4h | QA |
| Manual validation on real PRD run | 4h | QA |
| **Total** | **~27h** | |

---

## Open Questions for Debate

1. Does `claude --output-format stream-json` reliably emit a `result` event with the full final assistant text on all platforms and versions? Need to verify with CLI team.
2. Should we disable the Write tool in the subprocess via `--tools` flag (e.g. `--tools Read,Glob,Bash` instead of `--tools default`)? This would force compliance with B1 but may break steps that legitimately need Write (e.g. QA steps that fix issues in-place).
3. For the assembly step, is the hybrid B1/B2 approach acceptable, or should we invest in chunked assembly (multiple messages) to stay within token limits?
4. How do we handle the `build-task-file` step, which currently writes a dynamic filename (`TASK-PRD-{slug}.md`)? Should the prompt echo the file content back, or should we change the capture logic to key on `result` first and fall back to disk?
