# Research: ClaudeProcess and Output Mechanism

**Investigation type:** Code Tracer + Architecture Analyst
**Scope:** pipeline/process.py (ClaudeProcess), pipeline/executor.py (_execute_single_step)
**Status:** Complete
**Date:** 2026-04-04

---

## 1. ClaudeProcess Architecture

**File:** `src/superclaude/cli/pipeline/process.py` (lines 24-203)

ClaudeProcess is a thin subprocess wrapper. It has exactly four lifecycle methods:

| Method | Purpose |
|--------|---------|
| `build_command()` | Constructs the `claude` CLI argv |
| `build_env()` | Cleans env (removes CLAUDECODE, CLAUDE_CODE_ENTRYPOINT) to prevent nested-session detection |
| `start()` | Opens file handles, calls `subprocess.Popen` with stdout/stderr redirected to files |
| `wait()` | Blocks with `timeout_seconds`, returns exit code (124 on timeout) |
| `terminate()` | SIGTERM -> 10s grace -> SIGKILL, uses process groups (`os.setpgrp`) |

Three optional lifecycle hooks are injected via constructor kwargs:
- `on_spawn(pid)` -- called after Popen
- `on_signal(pid, signal_name)` -- called before signal send
- `on_exit(pid, returncode)` -- called before file handle close

## 2. CLI Flags Used by build_command()

**File:** `src/superclaude/cli/pipeline/process.py`, lines 71-91

The constructed command is always:

```
claude --print --verbose <permission_flag> --no-session-persistence \
       --tools default --max-turns <N> --output-format <format> -p <prompt> \
       [--model <model>] [extra_args...]
```

### Flag inventory:

| Flag | Value | Purpose |
|------|-------|---------|
| `--print` | (boolean) | **Non-interactive mode.** Sends prompt, captures all output to stdout. No interactive conversation. |
| `--verbose` | (boolean) | Includes additional diagnostic output (goes to stderr) |
| `<permission_flag>` | Default: `--dangerously-skip-permissions` | Allows tool use without approval prompts |
| `--no-session-persistence` | (boolean) | Prevents session state from persisting between invocations |
| `--tools default` | `default` | **Enables all default tools** including Read, Write, Edit, Bash, etc. |
| `--max-turns` | Integer, default 100 | Maximum agentic turns the subprocess can take |
| `--output-format` | `text` or `stream-json` | Controls stdout format (see Section 3) |
| `-p` | The prompt string | Inline prompt (not from file) |
| `--model` | Optional model name | Overrides default model |

### Critical observation: `--tools default` is always present

This means the child Claude process **has full tool access** -- it can call Read, Write, Edit, Bash, Glob, Grep, etc. The subprocess is a fully agentic Claude Code session. It is not a bare completion call. However, the **output capture mechanism** ignores this capability entirely.

## 3. Output Capture Mechanism: The One-Shot Architecture

### 3.1 How stdout is captured

**File:** `src/superclaude/cli/pipeline/process.py`, lines 110-137

```python
self._stdout_fh = open(self.output_file, "w")
self._stderr_fh = open(self.error_file, "w")
self._process = subprocess.Popen(self.build_command(), stdout=self._stdout_fh, stderr=self._stderr_fh, ...)
```

The file handles are opened **before** the process starts and closed **after** it finishes (in `wait()` -> `_close_handles()`). All stdout from the child process is written directly to `self.output_file` by the OS kernel's pipe buffer mechanism. There is no streaming read, no line-by-line processing, no intermediate buffering in Python.

### 3.2 The `--output-format` split

Two consumers use different output formats:

| Consumer | Format | Purpose |
|----------|--------|---------|
| **Roadmap pipeline** | `text` | Plain text output. The LLM's final response text goes to stdout. Tool calls and intermediate reasoning are suppressed from stdout. |
| **Sprint pipeline** | `stream-json` | NDJSON (newline-delimited JSON). Each event (tool call, text chunk, etc.) is a separate JSON line on stdout. |

For the roadmap pipeline (`output_format="text"`), only the **final text response** appears in the output file. This is the fundamental constraint: the subprocess runs a multi-turn agentic session, may use tools internally, but only the final text blob is captured.

### 3.3 The roadmap StepRunner (`roadmap_run_step`)

**File:** `src/superclaude/cli/roadmap/executor.py`, lines 649-830

The roadmap step runner:
1. Creates a `ClaudeProcess` with `output_format="text"` (line 758)
2. Embeds input file content directly into the prompt via `_embed_inputs()` (line 732-734)
3. Starts the process and polls for cancellation every 1 second (lines 764-775)
4. Waits for completion, checks exit code (lines 777-798)
5. **Post-processes the output file** via `_sanitize_output()` (line 801) -- strips conversational preamble before YAML frontmatter
6. For specific steps (extract, test-strategy), injects additional frontmatter fields (lines 804-819)
7. Returns `StepResult.PASS` -- actual gate checking is deferred to `execute_pipeline` in the generic executor

### 3.4 Post-capture sanitization

**File:** `src/superclaude/cli/roadmap/executor.py`, lines 355-399

`_sanitize_output()` strips leading whitespace and conversational preamble (anything before the first `---` frontmatter delimiter). This is necessary because with `--output-format text`, Claude sometimes emits conversational text ("Here's the extraction:") before the structured output. Uses atomic write (`.tmp` + `os.replace`) to prevent partial file states.

## 4. Input Embedding Mechanism

**File:** `src/superclaude/cli/roadmap/executor.py`, lines 319-352

Inputs are embedded inline into the prompt, not passed via `--file`:

```python
_MAX_ARG_STRLEN = 128 * 1024          # Linux kernel limit
_PROMPT_TEMPLATE_OVERHEAD = 8 * 1024   # Safety margin for template
_EMBED_SIZE_LIMIT = 120 * 1024         # 120 KB effective limit
```

The comment at line 721 states: `--file is broken (cloud download mechanism, not local file injector)`. This means all spec/TDD/PRD content is concatenated into the `-p` argument. This creates a hard Linux kernel limit of ~120 KB for the entire composed prompt (spec content + prompt template + embedded prior outputs).

Semantic role labels are applied so the LLM knows which embedded file is the primary spec vs supplementary context (line 724-731).

## 5. Token Limit and max-turns Behavior

### 5.1 max-turns

Default is 100 turns (from `PipelineConfig`, line 175 of models.py). This is the number of agentic turns (tool calls + responses) the subprocess can make.

For **sprint**, the timeout is derived from max_turns: `timeout_seconds = max_turns * 120 + 300` (sprint/process.py line 115). This gives 100 turns * 2 min/turn + 5 min grace = 205 minutes.

For **roadmap**, timeout is set per-step via `step.timeout_seconds` (defined in the step list, not derived from max_turns).

### 5.2 What happens when output exceeds limits

There are **two distinct limit scenarios**:

1. **Output token limit (Claude's response):** When the LLM generates a response that hits the context window output limit, `--output-format text` will capture whatever was generated up to that point. The process exits normally (exit code 0) but the output may be truncated. There is no detection or recovery for truncated output -- the gate criteria (min_lines, frontmatter checks) may catch some cases but not all.

2. **Max turns exhausted:** When `--max-turns` is reached, the Claude CLI exits cleanly. The last text response is captured. There is no specific handling for "ran out of turns."

3. **Timeout:** Exit code 124 is returned, `StepStatus.TIMEOUT` is set.

### 5.3 No continuation or resume logic

The `--no-session-persistence` flag is always set. There is no `--continue`, `--session`, or `--resume` flag used anywhere. Each step is a completely isolated one-shot invocation. The executor comment at line 8 explicitly confirms: "No --continue, --session, --resume, or --file flags are passed (FR-003, FR-023)."

## 6. Gate Validation After Capture

**File:** `src/superclaude/cli/pipeline/gates.py` (lines 1-117)

Gates run **after** the subprocess completes and the output file is written. They are pure Python, no LLM:

| Tier | Checks |
|------|--------|
| EXEMPT | Always passes |
| LIGHT | File exists + non-empty |
| STANDARD | + min line count + YAML frontmatter field presence |
| STRICT | + custom semantic check functions |

Gate validation reads the file from disk (`output_file.read_text()`). The retry loop in `_execute_single_step` (pipeline/executor.py, lines 199-283) will re-run the entire subprocess if a gate fails, up to `retry_limit + 1` attempts.

## 7. Incremental Writing Feasibility Assessment

### 7.1 Current architecture summary

```
[Prompt with embedded inputs] --> claude --print --output-format text --> stdout --> file
                                  ^                                         |
                                  |                                         v
                              Subprocess runs            File written ONLY when process exits
                              with full tool access       (OS-level pipe buffer flush)
                              (Write, Edit, Bash, etc.)
                              but output is stdout-only
```

### 7.2 Can the subprocess use Write/Edit to produce output files?

**Yes, technically.** The subprocess has `--tools default` and `--dangerously-skip-permissions`. Nothing prevents the child Claude from calling Write or Edit to create/modify files. The sprint pipeline already exploits this: the subprocess prompt says "write the result file to `<path>`" (sprint/process.py, line 199), and the subprocess uses Write tool to create that file.

### 7.3 What would need to change for incremental writing

To switch from stdout-capture to tool-use-based file writing:

1. **Prompt changes:** Each step's prompt would need to instruct Claude to write its output to a specific file path using Write/Edit tools, rather than outputting to stdout. The prompt would need to specify the exact file path and format expectations.

2. **Output format change:** Could switch from `--output-format text` to `--output-format stream-json` for roadmap steps. This would allow the parent process to monitor tool calls in real time, but adds complexity.

3. **Output capture change:** The parent process would no longer rely on stdout redirection. Instead, it would check for the existence/content of the target file after the subprocess completes (similar to how sprint checks for result files).

4. **Gate validation:** No change needed -- gates already read from `step.output_file` on disk.

5. **Sanitization removal:** `_sanitize_output()` would no longer be needed if the subprocess writes structured content directly via Write tool (no conversational preamble in tool-written files).

### 7.4 Key technical constraints

| Constraint | Impact | Severity |
|-----------|--------|----------|
| **Linux MAX_ARG_STRLEN (128 KB)** | Prompt size limit for `-p` flag. Large specs + embedded prior outputs could exceed this. Incremental writing doesn't help here -- the prompt still needs to fit. | HIGH |
| **--output-format text suppresses tool call visibility** | Parent process cannot see what tools the child used. If the child writes to the wrong path or fails to write, parent only knows via gate failure. | MEDIUM |
| **No streaming feedback with `text` format** | Parent process polls `_process.poll()` every 1 second but has zero visibility into progress. With `stream-json`, parent could parse NDJSON for progress events. | LOW (for correctness), HIGH (for UX) |
| **Process group isolation** | `os.setpgrp` means the child and its descendants are isolated. If the child spawns sub-agents (via /sc:task-unified), they inherit the process group. This is correct behavior. | NONE |
| **Atomic write risk** | If the child uses Write tool to produce output, and the process is killed mid-write, the file could be partial. The current stdout-redirect approach also has this risk (OS flushes pipe buffer on process exit, but SIGKILL can lose buffered data). | LOW |

### 7.5 Hybrid approach: stdout + tool-use

A more pragmatic approach than full tool-use migration:

1. Keep `--output-format text` for capturing the "final answer" to stdout (backward compatible)
2. **Additionally** instruct the subprocess to write intermediate artifacts via tools (e.g., "As you work, write progress markers to `<output>.progress`")
3. Parent process monitors both stdout file growth and progress file for liveness detection

This avoids changing the core output capture mechanism while enabling incremental visibility.

### 7.6 Assessment verdict

**Incremental writing via tool-use IS feasible** but requires coordinated changes across:
- Prompt templates (to instruct file writing)
- Output validation (to check tool-written files instead of stdout)
- Sanitization logic (can be simplified/removed)

The most impactful change would be switching roadmap steps to `stream-json` output format, which would give the parent process real-time visibility into the subprocess's tool calls and text generation. This is a larger change but would unlock progress monitoring, partial output recovery, and early failure detection.

## 8. Retry and Continuation Logic

### 8.1 Retry mechanism

**File:** `src/superclaude/cli/pipeline/executor.py`, lines 199-283

The retry loop in `_execute_single_step`:
- Runs `run_step()` up to `retry_limit + 1` times
- Only retries if the gate check fails (not on process crash or timeout)
- Each retry is a completely fresh subprocess invocation (no state carried over)
- No prompt modification between retries (the same prompt is re-sent)

### 8.2 No continuation logic

There is zero continuation logic. If a step produces 80% of the expected output before hitting a token limit, the entire step is re-run from scratch on retry. The 80% partial output is overwritten because `open(self.output_file, "w")` truncates on open.

### 8.3 Parallel step execution

**File:** `src/superclaude/cli/pipeline/executor.py`, lines 297-347

Parallel steps use `threading.Thread` with a shared `threading.Event` for cross-cancellation. If any step in a parallel group fails, the event is set and remaining steps' `cancel_check()` returns True.

## 9. Sprint vs Roadmap: Key Differences

| Aspect | Sprint | Roadmap |
|--------|--------|---------|
| Output format | `stream-json` | `text` |
| File writing | Subprocess writes result files via Write tool | Subprocess outputs everything to stdout |
| Timeout calculation | Derived: `max_turns * 120 + 300` | Per-step, defined in step config |
| Process class | Sprint-specific subclass with debug hooks | Direct `ClaudeProcess` instantiation |
| Context injection | `build_task_context()` with progressive summarization | `_embed_inputs()` with inline file embedding |
| Prompt source | `/sc:task-unified` command with phase file | Custom prompt builders per step type |

---

## Gaps and Questions

1. **No truncation detection:** If Claude's response is cut off at the output token limit, there is no mechanism to detect this. A step could produce a syntactically incomplete markdown file that passes LIGHT gate but is useless.

2. **Retry without learning:** Retries re-send the identical prompt. If the LLM failed because the prompt was ambiguous or the task too large for one shot, retry will likely fail the same way.

3. **Prompt size ceiling:** With large specs (>80 KB) plus embedded prior outputs, the 120 KB `_EMBED_SIZE_LIMIT` could be hit. The code logs a warning but proceeds anyway (line 737-742), which could cause kernel `E2BIG` errors on Linux.

4. **stream-json for roadmap:** Why was `text` chosen over `stream-json` for roadmap? Sprint uses `stream-json` successfully. The roadmap pipeline could benefit from the richer output format for progress monitoring and tool-call visibility.

5. **No partial output preservation:** `open(self.output_file, "w")` truncates the file. If a retry happens, the partial (potentially useful) output from the first attempt is destroyed. No backup/versioning of failed attempts.

## Stale Documentation Found

- **Line 8 of executor.py** states: "`--file is a cloud download mechanism and does not inject local file content.`" This may or may not still be accurate for current Claude CLI versions. Should be verified against current `claude --help` output.

- **sprint/process.py line 116**: `output_format="stream-json"` is hardcoded for sprint. The comment at pipeline/process.py line 6 documents this split but doesn't explain the rationale for the divergence.

## Summary

ClaudeProcess is a straightforward subprocess wrapper that redirects stdout/stderr to files. The roadmap pipeline uses `--output-format text` which captures only the final text response, discarding all intermediate tool calls and reasoning. The subprocess has full tool access (`--tools default`) but this is unused for output -- everything must fit in a single stdout blob.

**Incremental writing is technically feasible** because the subprocess already has Write/Edit tool access. The main barriers are:
1. Prompt templates must be rewritten to instruct file-based output
2. Output validation must shift from stdout-file to tool-written-file checking
3. The `_sanitize_output()` preamble stripping can be eliminated
4. Switching to `stream-json` would unlock real-time progress monitoring

The one-shot stdout-capture architecture is the root cause of the "output exceeds limits" failure mode. There is no truncation detection, no continuation, and no partial output preservation. Retries restart from zero with no learning from the failed attempt.
