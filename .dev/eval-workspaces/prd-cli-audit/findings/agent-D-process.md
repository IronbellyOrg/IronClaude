# Agent D — Subprocess & process plumbing

**Scope**: `src/superclaude/cli/prd/process.py`, `src/superclaude/cli/prd/monitor.py`, `src/superclaude/cli/prd/logging_.py` (with mandatory cross-reads of `src/superclaude/cli/pipeline/process.py` and `src/superclaude/cli/prd/executor.py` because the plumbing crosses module boundaries).

The originating failure ("Min lines: 30/400" on `build-task-file`) is **architecturally a P4/P6 defect of this layer**, not just Bug 1 in `_STEP_ARTIFACT_FILES`. Bug 1 is the proximate trigger; everything below describes the standing weaknesses in the subprocess layer that make every non-mapped step a latent repeat of the same failure. Findings are ordered by severity.

---

### F-D-1: Subprocess hard-codes `output_format="stream-json"`; gate consumer downstream reads NDJSON commentary as if it were artifact text — sibling instance of Bug 1's pattern for every unmapped step

**Severity (preliminary)**: CRITICAL
**Pattern tags**: P4, P6, P7
**File:line**: `src/superclaude/cli/prd/process.py:159` (output_format set), `src/superclaude/cli/prd/executor.py:514-524` (downstream consumer)
**Evidence**:
```python
# process.py:151-161
super().__init__(
    prompt=prompt,
    output_file=output_file,
    ...
    output_format="stream-json",   # always stream-json, no override
    extra_args=file_args,
)

# executor.py:514-523
raw_output = output_file.read_text(encoding="utf-8", errors="replace")
output_text = _extract_text_from_stream_json(raw_output) if raw_output else ""

# Resolve best content: prefer files written to disk by the
# subprocess over extracted NDJSON commentary
gate_content = _resolve_step_content(
    step_id, self._config.task_dir, output_text
)
```
**Trace**: `process.py` always launches the child in `stream-json` mode and pipes stdout into `{step_id}-output.txt`. The base `ClaudeProcess.start()` (line 122) opens the file for write and the child's stdout is whatever NDJSON the model emits — at minimum the assistant's commentary, never the Write-tool output. The executor reads that file at `executor.py:514`, extracts assistant text via `_extract_text_from_stream_json`, then calls `_resolve_step_content` which uses the static `_STEP_ARTIFACT_FILES` dispatch table (Bug 1's domain). For any step whose ID is absent from that table — `build-task-file`, `verify-task-file`, `preparation`, `template-triage`, every `investigation-N`, every `synthesis-*`, every `*-fix-N`, `assembly`, `present-complete` — `_resolve_step_content` falls through to `return ndjson_text` (executor.py:269), and the gate evaluates 30 lines of LLM commentary against a 400-line threshold. This is the failure that halted step 7. The plumbing **never differentiates "subprocess wrote a real artifact via the Write tool" from "subprocess produced freeform NDJSON"** — the base class has a `tool_write_mode` parameter expressly designed for this (pipeline/process.py:53, 118-122, 216-236) and the PRD `PrdClaudeProcess.__init__` does not pass it through. So every step that produces its real output via Write is silently mis-plumbed.
**Reproduction sketch**: Add a new pipeline step `foo-step` that writes its real output to `task_dir/foo-step-result.md` via the Write tool. Without touching `_STEP_ARTIFACT_FILES`, run the pipeline. Gate evaluates the NDJSON commentary, not the real artifact, and any nontrivial `min_lines` fails. This is the recurring shape Agent A found at `build-task-file`.
**Confidence (own)**: 0.95. Direct read of both files. The omission of `tool_write_mode` is intentional design but never exercised by the PRD entry point.

---

### F-D-2: `PrdMonitor` is instantiated but its public API (`parse_line`, `check_stall`, `reset`, `get_state`) is **never called** anywhere in the executor — entire monitor.py is dead code

**Severity (preliminary)**: HIGH
**Pattern tags**: P2, P4, P8
**File:line**: `src/superclaude/cli/prd/monitor.py:1-202` (entire file); `src/superclaude/cli/prd/executor.py:334` (only reference)
**Evidence**:
```python
# executor.py:334 — only place PrdMonitor is touched
self._monitor = PrdMonitor()
```
`grep -rn "self\._monitor\." src/superclaude/cli/prd/` returns zero hits beyond the assignment. `grep -n "parse_line\|check_stall\|monitor\." executor.py` confirms no call sites for `_monitor.parse_line`, `_monitor.check_stall`, `_monitor.reset`, or `_monitor.get_state`.
**Trace**: The subprocess's stdout flows directly into the on-disk `{step_id}-output.txt` file via Popen's `stdout=` redirection (pipeline/process.py:127). Nothing streams those bytes line-by-line. `executor._run_subprocess_step` calls `proc.start_with_retry(); proc.wait()` and only **after** the child exits reads the whole file with `read_text`. Consequently:
- `PrdMonitor.parse_line` is unreachable.
- `PrdMonitor.check_stall` is unreachable, so `PrdConfig.stall_timeout` and `stall_action` (models.py:190-191) have no detection path.
- TUI is updated only on step completion (executor.py:455), never mid-stream from monitor signals.
- All the QA verdict / fix-cycle / research-file-count signal extraction in `monitor.py:153-201` produces nothing usable.

This is a textbook P2 (knob defined in `monitor.py` and `models.py`, consumed in zero places) compounded with P4 (stream is collected as a whole file, never sampled). A subprocess that hangs forever printing nothing will sit until `proc.wait(timeout=self.timeout_seconds)` fires — i.e. `stall_timeout * 30 = 3600s` for the default config — with no intermediate stall signal at the configured 120s.
**Reproduction sketch**: Run any step whose child stalls for 2-3 minutes without writing output. Expected per `stall_timeout=120`: a stall warning/abort. Actual: silence until the 3600s wall-clock timeout. Equivalently, write a unit test asserting `monitor.parse_line` is called by the executor — it will fail by inspection.
**Confidence (own)**: 0.98. Trivially verifiable with grep.

---

### F-D-3: `stall_timeout` is repurposed as `timeout_seconds = stall_timeout * 30` — a load-bearing semantic shift hidden behind a default; classic P7

**Severity (preliminary)**: HIGH
**Pattern tags**: P4, P7, P8
**File:line**: `src/superclaude/cli/prd/executor.py:499`
**Evidence**:
```python
proc = PrdClaudeProcess(
    config=self._config,
    step_id=step_id,
    prompt=prompt,
    output_file=output_file,
    error_file=error_file,
    timeout_seconds=self._config.stall_timeout * 30,
)
```
`PrdConfig.stall_timeout: int = 120` (models.py:190). The PRD docstring & field name say "stall" (i.e. quiet period); the value is silently multiplied by 30 and used as the wall-clock subprocess timeout (process.py:140, pipeline/process.py:162). There is **no separate field** for wall-clock timeout vs. stall threshold — they have been collapsed into a single field whose meaning depends on the consumer.
**Trace**: A user reducing `stall_timeout` to 60 (thinking they tighten stall detection) actually halves the wall-clock budget to 30 minutes per step. A user raising it to 600 to allow long quiet periods extends every step's wall-clock cap to 5 hours. There is no stall detection at all (F-D-2), so the field's name is actively misleading. Also: `stall_action` is never read anywhere in PRD code (`grep` returns only the field definition), so the "warn"/halt/etc. distinction does not exist.
**Reproduction sketch**: `superclaude prd run ... --stall-timeout 30` and observe wall-clock timeout becomes 900s, with no quiet-period detection.
**Confidence (own)**: 0.95.

---

### F-D-4: NDJSON parsing silently swallows every malformed line and never differentiates "model error embedded in stream" from "transport corruption" — gate sees the survivor text and proceeds

**Severity (preliminary)**: HIGH
**Pattern tags**: P4, P8
**File:line**: `src/superclaude/cli/prd/executor.py:99-130` (`_extract_text_from_stream_json`); mirrored in `src/superclaude/cli/prd/monitor.py:86-91` (`parse_line`)
**Evidence**:
```python
# executor.py:111-130
for line in raw.splitlines():
    line = line.strip()
    if not line:
        continue
    try:
        obj = json.loads(line)
    except (json.JSONDecodeError, ValueError):
        continue                          # <— silent

    message = obj.get("message") or {}
    content = message.get("content")
    if not isinstance(content, list):
        continue
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            text = block.get("text", "")
            if text:
                texts.append(text)

return "\n".join(texts) if texts else raw   # <— silent fallback to raw on full failure
```
**Trace**: Three independent silent-swallow conditions, each capable of feeding the gate something semantically wrong:
1. Malformed JSON line → skipped, no log, no diagnostic. A child that emits partial-buffer truncated lines under load loses content with zero visibility.
2. `content` not a list / no `type: "text"` blocks → skipped silently. The new Claude CLI message variants (tool_use, tool_result, thinking) are dropped entirely, so a child whose output is mostly tool_use events presents as near-empty.
3. **The final fallback at line 130** is the most dangerous: if zero text blocks were extracted, the function returns `raw` — i.e. the whole NDJSON blob — and the caller treats it as plain text. The gate's `splitlines()` then counts NDJSON envelope lines (one per event) as "content lines", which is precisely the failure mode that produced "30 lines" on the build-task-file output: short JSON metadata events being counted as content. A subprocess that fails early may produce a small number of NDJSON envelopes that look like a valid (but tiny) content body.

`monitor.py:88-91` has the same swallow pattern with the same lack of distinction between "parser couldn't decode" and "this was deliberately plain text".
**Reproduction sketch**: Have the child emit 30 valid NDJSON envelopes with `type: "tool_use"` and zero `type: "text"` blocks. `_extract_text_from_stream_json` returns the entire raw NDJSON; `splitlines()` counts 30. Gate min_lines=400 fails with the exact "30/400" message observed in production.
**Confidence (own)**: 0.9. The "fallback to raw" branch is unambiguous; the failure-mode mapping is high-confidence by inspection.

---

### F-D-5: `_is_transient_failure` only ever sees launch-time `OSError`; retry never engages for stderr-based transient signals from a started-and-died process

**Severity (preliminary)**: HIGH
**Pattern tags**: P4, P8
**File:line**: `src/superclaude/cli/prd/process.py:63-86` (definition), `src/superclaude/cli/prd/process.py:208-219` (call site), `src/superclaude/cli/prd/executor.py:502-509` (caller)
**Evidence**:
```python
# process.py:208-219
for attempt in range(self._max_retries + 1):
    try:
        proc = self.start()
        return proc                       # <— returns immediately on Popen success
    except OSError as exc:
        last_error = exc
        stderr_text = str(exc)            # <— stderr_text is the OSError repr, NOT child stderr

        if not _is_transient_failure(1, stderr_text):
            raise RuntimeError(...) from exc
```
**Trace**: `subprocess.Popen` raises `OSError` only for kernel-level launch failures (executable not found, permission denied on exec, fork failure). It does **not** raise for any case where the binary started and then died — including 429s, 503s, rate-limit messages from the `claude` CLI, network errors, or any other transient pattern listed in `_TRANSIENT_PATTERNS`. Those all manifest as `start()` returning normally and then `proc.wait()` later yielding a nonzero exit code with the real error in the error_file.

Result:
- The retry harness is wired only to OSError on launch, so 99% of real transient failures bypass it.
- `_TRANSIENT_PATTERNS` and `_NON_TRANSIENT_PATTERNS` (process.py:38-60) are effectively dead — they're only matched against `str(OSError)`, never against actual child stderr.
- `executor._run_subprocess_step` catches `RuntimeError` (executor.py:505) and converts to `PrdStepResult(status=ERROR)` with no retry, so a 429 from the API just becomes an immediate halt.
- The 5s/15s exponential backoff (`_retry_delays`) is unreachable for any practical scenario.

This is a P4 (subprocess output mishandling) and P8 (halt control flow on a failure that should retry).
**Reproduction sketch**: Stub `claude` with a script that prints "rate limit exceeded" to stderr and exits 1. Run the pipeline. Observe: zero retries, immediate ERROR. The patterns at lines 38-50 are inert.
**Confidence (own)**: 0.92. Read of Python subprocess semantics + direct read of retry loop.

---

### F-D-6: Exit-code semantics are inconsistent across the layer; multiple meaningful codes collapse to ERROR; SIGINT/SIGKILL never distinguishable

**Severity (preliminary)**: MEDIUM
**Pattern tags**: P4, P7, P8
**File:line**: `src/superclaude/cli/prd/executor.py:562-585` (`_determine_status`), `src/superclaude/cli/pipeline/process.py:160-171` (`wait()`)
**Evidence**:
```python
# executor.py:563-568
if exit_code == 124:
    return PrdStepStatus.TIMEOUT

# Crash
if exit_code != 0:
    return PrdStepStatus.ERROR
```
**Trace**: The exit-code branches recognise only `124` (mapped to TIMEOUT by `pipeline/process.py:165` after `subprocess.TimeoutExpired`) and `0` (success). Every other code — including:
- `130` = SIGINT (user Ctrl-C; the operator's deliberate interrupt presents identical to a crash)
- `137` = SIGKILL (OOM kill or our own `terminate()` after grace)
- `143` = SIGTERM
- `-N` = signal-killed without WIFEXITED on POSIX
- `1` = generic CLI error
- `2` = CLI usage error

...all fold into `PrdStepStatus.ERROR`. `_is_transient_failure` (process.py:37) has `137` in `_TRANSIENT_EXIT_CODES` — so the layer **claims** SIGKILL is transient and retryable in one place but immediately surfaces it as ERROR in another. The logger (logging_.py:21-35) has a status emoji map that includes "timeout", "error", "halt", but no entry distinguishing operator-cancel from crash, and the executor never feeds it that distinction anyway. The `start_with_retry` retry table refers to `137` (process.py:37) but per F-D-5 it's never consulted post-launch, so the apparent intent ("retry on OOM kill") is unimplemented.

Cross-ref: `pipeline/process.py:165` returns 124 on `TimeoutExpired`. But it does not record whether `terminate()` succeeded — if SIGKILL fired, the child's actual recorded `returncode` (137 or -9) is overwritten. That's lossy.
**Reproduction sketch**: Ctrl-C during a step. The pipeline reports ERROR, not "user-interrupted". OOM-kill the child. Same ERROR. Real cause is invisible in `execution-log.jsonl`.
**Confidence (own)**: 0.85.

---

### F-D-7: `terminate()` overrides base class to use 5s grace but the base `wait()` calls the base `terminate()` (10s) on timeout, so the override is dead code for timeout-path

**Severity (preliminary)**: MEDIUM
**Pattern tags**: P3 (dynamic-vs-static dispatch), P4
**File:line**: `src/superclaude/cli/prd/process.py:238-278` (override), `src/superclaude/cli/pipeline/process.py:159-171` (`wait()`)
**Evidence**:
```python
# pipeline/process.py:159-165
def wait(self) -> int:
    try:
        self._process.wait(timeout=self.timeout_seconds)
    except subprocess.TimeoutExpired:
        self.terminate()                 # <— polymorphic, OK in principle
        return 124
```
**Trace**: `self.terminate()` in the base does dispatch polymorphically, so this is actually wired right — but the docstring on `PrdClaudeProcess.terminate` ("F-004: Override base terminate to use 5s grace period instead of default 10s") implies the override is the *only* termination path. In practice:
- The base `wait()` (which is what `executor._run_subprocess_step` calls at line 504) does call the subclass `terminate()`. OK.
- BUT: there is no place in `PrdExecutor` where `terminate()` is called for any reason **other** than the wait-timeout path — no SIGINT handler, no shutdown handler, nothing calls `proc.terminate()`. `PrdSignalHandler` (executor.py:176-203) just sets a `shutdown_requested` flag; it never propagates the signal to the running child. So the 5s grace period applies only to the wall-clock-timeout path. Operator Ctrl-C during a running step leaves the child running until it finishes or signals propagate via the process group.

The override is "real" but its surface area is much smaller than the docstring suggests. Combined with F-D-6 (Ctrl-C invisible) this creates a real lifecycle gap: the user hits Ctrl-C, Python's default SIGINT handler is replaced, `shutdown_requested=True`, the parent waits for `proc.wait()` to finish, the child has no idea the parent wants out. (Process group SIGINT from the TTY will hit the child too, but a programmatic SIGTERM to the parent process — what `kill -TERM <pid>` does — will not.)
**Reproduction sketch**: Send SIGTERM to the parent during a long step. Parent sets `shutdown_requested=True` but doesn't relay; child runs to completion.
**Confidence (own)**: 0.75. The exact relay behaviour depends on whether the process is foregrounded under a TTY; the signal-handler-not-relaying claim is conservative but defensible.

---

### F-D-8: Logger appends to JSONL/Markdown with no flush/fsync; no rotation; no size cap; resume reads may race with in-flight writes

**Severity (preliminary)**: LOW
**Pattern tags**: P4
**File:line**: `src/superclaude/cli/prd/logging_.py:166-174`
**Evidence**:
```python
def _write_jsonl(self, data: dict) -> None:
    with open(self._jsonl_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, default=str) + "\n")

def _write_md(self, line: str) -> None:
    with open(self._md_path, "a", encoding="utf-8") as f:
        f.write(line)
```
**Trace**: Each call opens the file in append mode and lets the context manager close it (which flushes to libc buffers but not `fsync` to disk). For a single-process writer this is fine on local FS; on NFS or a crash mid-write the last entry can be torn. No rotation/size cap means `execution-log.jsonl` grows unbounded across very long runs. Resume logic that reads `execution-log.jsonl` to reconstruct state has no concurrency lock — though by inspection only `PrdLogger` writes it, so practically safe. Open-close-per-write is also a per-event syscall cost that becomes visible at thousands of monitor events (which currently don't fire — see F-D-2 — but would if monitor were ever wired).
**Reproduction sketch**: Kill `-9` the parent mid-write; tail `execution-log.jsonl`; observe partial last line. Recovery code that does naive `json.loads(line)` will hit JSONDecodeError on the tail.
**Confidence (own)**: 0.7. Low severity because PRD pipeline cardinality of writes is small.

---

### F-D-9: `start()` writes prompt to stdin without checking child liveness; BrokenPipeError swallowed without logging — early child death goes undiagnosed

**Severity (preliminary)**: LOW
**Pattern tags**: P4, P8
**File:line**: `src/superclaude/cli/pipeline/process.py:140-146`
**Evidence**:
```python
try:
    if self._process.stdin is not None:
        self._process.stdin.write(self.prompt.encode("utf-8"))
        self._process.stdin.close()
except BrokenPipeError:
    # Child exited before reading stdin; wait() will surface the exit code.
    pass
```
**Trace**: Comment is correct that `wait()` will catch the exit code — but no log of "prompt delivery failed because child was already dead" is emitted, so when this happens the user sees a generic ERROR with whatever the early-death exit code was (likely 1 or 2). For an LLM CLI this is a meaningful diagnostic: it tells you the binary didn't even get to read the prompt. Pair this with F-D-5 (no retry on post-launch failure) and the failure mode is: child dies immediately, prompt never reaches it, parent sees BrokenPipe-then-ERROR-exit, no retry, halt.
**Reproduction sketch**: Replace `claude` with `/bin/false`; observe pipeline produces ERROR with no diagnostic that prompt delivery failed.
**Confidence (own)**: 0.75. Defer to Agent E if "stream lifecycle / observability" is in scope there.

---

### F-D-10: `_extract_text_from_stream_json` is duplicated in spirit between `executor.py:99-130` and `monitor.py:69-98` with divergent behaviour — single source of truth missing

**Severity (preliminary)**: LOW
**Pattern tags**: P1
**File:line**: `src/superclaude/cli/prd/executor.py:99-130` and `src/superclaude/cli/prd/monitor.py:69-98`
**Evidence**: Both files parse NDJSON line-by-line, both call `json.loads`, both silently swallow `JSONDecodeError`. The executor variant extracts `message.content[].text` to feed gates; the monitor variant extracts `step_id`/`agent_type`/`artifact`/`verdict`/`fix_cycle` for state. Two parsers, two failure modes, two places to update when the stream-json schema evolves.
**Trace**: A schema change in the claude CLI (e.g. moving `text` from `message.content[].text` to `delta.text`, as some streaming APIs have done) requires touching both. Bug-fix asymmetry is likely. Given F-D-2 (monitor unused), this is currently low-impact, but if monitor is ever wired up, the two parsers will drift.
**Reproduction sketch**: Schema change to claude's stream-json output. Executor breaks first; monitor breaks differently (or silently degrades).
**Confidence (own)**: 0.65. Defer to Agent A/E for the monitor-revival decision.

---

### F-D-11: Phase-allowed-refs table (`_PHASE_ALLOWED_REFS`) is static and step-ID-keyed; new step IDs added downstream silently get empty allow-list — sibling of Bug 1 pattern

**Severity (preliminary)**: LOW
**Pattern tags**: P1, P3
**File:line**: `src/superclaude/cli/prd/process.py:95-113`
**Evidence**:
```python
_PHASE_ALLOWED_REFS: dict[str, list[str]] = {
    "parse-request": [],
    "scope-discovery": [],
    ...
}
# at line 175:
allowed = _PHASE_ALLOWED_REFS.get(base_step, [])
```
**Trace**: Step IDs that aren't in the table get `[]` with no error. Step normalization at line 173 strips a trailing numeric suffix (`investigation-3` → `investigation`), which is OK for the listed parallel families, but `qa-research-fix-2`, `present-complete`, or any future step typo will silently receive zero --file args, producing a subprocess that can't see its refs and therefore writes a degraded output. This is the same dispatch-table-misses-new-key shape as Bug 1, just in a different table.
**Reproduction sketch**: Add a new step ID `precommit-check` that needs `validation-checklists.md`. Forget to add to `_PHASE_ALLOWED_REFS`. Subprocess silently runs without the --file arg; gate later fails for unrelated-looking content reasons.
**Confidence (own)**: 0.6. Lower severity because only inlining-vs-flag is affected (refs may still be loaded by the prompt builder), but the silent-empty-on-miss pattern is real.

---

### F-D-12: No fsync after Write-tool artifacts; gate evaluates artifact file immediately after child exit — local-FS-safe in practice, but no flush primitive exists if move to networked FS

**Severity (preliminary)**: LOW
**Pattern tags**: P4
**File:line**: `src/superclaude/cli/prd/executor.py:502-524`
**Trace**: The subprocess is the `claude` CLI which writes via its Write tool. Once `proc.wait()` returns, the OS guarantees that all the child's writes are at least in the page cache (POSIX semantics for sibling processes reading the same FS). For local ext4/tmpfs this means the gate `read_text` will see all of the child's writes. **But** the chain `_resolve_step_content → rglob → read_text` searches both `task_dir` and `task_dir.parent` (executor.py:275-277), which on NFS or on a filesystem with delayed metadata visibility could in principle miss freshly-Write'd files that haven't yet appeared in the parent's directory cache. Defer to Agent E/F if production deployment ever moves to NFS.
**Confidence (own)**: 0.5.

---

## Considered and rejected

- **"Output file is opened in `w` mode and may truncate across retries"** — looked at `start_with_retry` (process.py:192) carefully. Retries happen only on `OSError` at launch (which is itself rare, see F-D-5). Even if a retry did fire, each call to `start()` re-opens the file in `w` (pipeline/process.py:122), which is intentional clobber. Not a bug — but the rarity of the retry path is itself a bug (F-D-5), which already captures the underlying concern.

- **"`tool_write_mode` validation runs after `_close_handles` so file may not be visible"** — `validate_tool_write_output` (pipeline/process.py:216) reads `output_file.exists()`/`stat()`. By the time we're past `wait()` the child is dead and POSIX guarantees visibility. Not a defect. (Separately: PRD layer never sets `tool_write_mode=True` — see F-D-1.)

- **"Logger could race if multiple steps run in parallel"** — `_execute_parallel_steps` (executor.py:768) does spawn parallel children via ThreadPoolExecutor, and `_execute_step` calls `_logger.log_step_start`/`log_step_complete` from worker threads. Each `_write_jsonl` call uses open-write-close, which on POSIX `O_APPEND` is atomic for writes shorter than `PIPE_BUF`. JSONL entries are short. The Markdown table-row writes are also short. Practically safe. Not flagged.

- **"`_PHASE_ALLOWED_REFS` strips numeric suffix incorrectly"** — line 173 only strips when `step_id[-1:].isdigit()`. A step ID like `qa-fix-cycle-2` becomes `qa-fix-cycle` which is sensible. `web-research-1` becomes `web-research` which is in the table. Edge case `step-10` → `step-1` (still digit, strips again? — no, only one rsplit). For double-digit suffixes (e.g. `investigation-10`), `step_id[-1:]` is `"0"`, digit; `rsplit("-", 1)` correctly yields `investigation`. No bug.

- **"`output_file.read_text` could race with child still writing because `_close_handles` doesn't flush"** — `_close_handles` calls `fh.close()` which calls `fflush()` then `close(2)`; the kernel guarantees data is in the page cache after `close()`. Parent's subsequent `read_text` sees all of it. Not a bug on local FS. F-D-12 captures the NFS-deployment-only concern.

- **"Bug 1 sibling: `_PHASE_ALLOWED_REFS` consumer reads NDJSON stream when it should read file"** — no, this table feeds `--file` args at child-launch time, not gate evaluation. Different pattern. F-D-11 captures the dispatch-miss aspect instead.
