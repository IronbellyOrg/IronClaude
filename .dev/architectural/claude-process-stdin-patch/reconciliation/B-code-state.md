# B-code-state.md — Current ClaudeProcess subsystem (branch `fix/claude-process-stdin-large-prompts`)

Read-only inspection. All citations are `<absolute_path>:<line>`. Source-of-truth is `src/superclaude/`.

## Summary table

| File | LOC | Key observation |
|---|---|---|
| `/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py` | 244 | Always-stdin delivery (no `-p`, no positional prompt). Adds `tool_write_mode` + `validate_tool_write_output()`. `extra_args` already present. Hooks unchanged. |
| `/config/workspace/IronClaude/src/superclaude/cli/cli_portify/process.py` | 245 | `cmd.index("-p")` lookup at line 210 falls into `except ValueError` for ALL invocations → `--add-dir` flags appended at end of `cmd` rather than spliced before `-p`. Argv layout differs from DESIGN.md anchor. |
| `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py` | 385 | Subclass: hook-injection only, no `build_command` override. Inherits stdin delivery. |
| `/config/workspace/IronClaude/src/superclaude/cli/cleanup_audit/process.py` | 72 | Subclass: prompt builder only. Inherits stdin delivery. Executor calls `is_running()`/`stop()` which DO NOT EXIST on the class. |

---

### `/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py` (244 lines)

#### Constructor signature — lines 37-71

Keyword-only constructor:
```python
def __init__(
    self,
    *,
    prompt: str,                                              # 40
    output_file: Path,                                        # 41
    error_file: Path,                                         # 42
    max_turns: int = 100,                                     # 43
    model: str = "",                                          # 44
    permission_flag: str = "--dangerously-skip-permissions",  # 45
    timeout_seconds: int = 6300,                              # 46
    output_format: str = "stream-json",                       # 47
    extra_args: list[str] | None = None,                      # 48
    on_spawn: Callable[[int], None] | None = None,            # 49
    on_signal: Callable[[int, str], None] | None = None,      # 50
    on_exit: Callable[[int, int | None], None] | None = None, # 51
    env_vars: dict[str, str] | None = None,                   # 52
    tool_write_mode: bool = False,                            # 53
):
```
Stored on self at lines 55-71. No `prompt_sidecar`, no `PROMPT_STDIN_THRESHOLD`, no `PromptTooLargeForArgv`.

#### stdin/argv handling — lines 73-95, 114-146

`build_command()` lines 73-95:
```python
cmd = [
    "claude",
    "--print",
    "--verbose",
    self.permission_flag,
    "--no-session-persistence",
    "--tools",
    "default",
    "--max-turns",
    str(self.max_turns),
    "--output-format",
    self.output_format,
]
if self.model:
    cmd.extend(["--model", self.model])
cmd.extend(self.extra_args)
return cmd
```
`-p` is **NOT** in the argv at all. The prompt is never passed via argv.

Docstring at lines 76-78 states explicitly: *"Prompt is delivered via stdin in start(), not as a -p argv value, to bypass the Linux MAX_ARG_STRLEN = 128 KB per-argument ceiling."*

`start()` lines 114-157 sets `stdin=subprocess.PIPE` (line 126) for ALL prompt sizes, then writes synchronously at line 142:
```python
self._process.stdin.write(self.prompt.encode("utf-8"))
self._process.stdin.close()
```
guarded by a top-level `try/except BrokenPipeError` (lines 140-146).

#### Prompt sizing — none

No size guard, no chunking, no `PROMPT_STDIN_THRESHOLD`, no `PROMPT_MAX_BYTES`, no `PromptTooLargeForArgv`. The entire prompt is encoded once on line 142 (`self.prompt.encode("utf-8")`) and passed to a single `write()` call.

#### Signal handling — lines 173-214 (`terminate`)

- Process group used when `os.getpgid` and `os.killpg` exist (line 179).
- `SIGTERM` first (lines 183-189), 10s wait (line 195), then `SIGKILL` (lines 197-203) with 5s wait (line 203).
- `ProcessLookupError` swallowed at lines 190-192, 204.
- `_close_handles()` invoked on every exit branch (lines 176, 191, 214).

#### Lifecycle hooks — lines 49-51, 64-66, 148-149, 168-169, 183-184, 212-213

- `on_spawn(pid)` after Popen (line 148-149).
- `on_signal(pid, "SIGTERM")` before signal send (line 183-184). Note: **only** SIGTERM is reported; SIGKILL escalation does NOT call `on_signal` again (lines 197-203 omit the hook).
- `on_exit(pid, returncode)` from `wait()` (line 168-169) and from `terminate()` (line 212-213).

#### New constructor params/methods after pipx baseline — `tool_write_mode` + `validate_tool_write_output()`

- `tool_write_mode: bool = False` kwarg at line 53; stored at line 68.
- In `start()` lines 118-120, when true, stdout file handle is redirected to `output_file.with_suffix(".log")` rather than `output_file` itself (so the LLM is expected to write `output_file` directly via its tools).
- `validate_tool_write_output()` lines 216-236 returns True for non-tool-write mode (line 222-223), else verifies `output_file` exists (224-229) and is non-empty (230-235).

---

### `/config/workspace/IronClaude/src/superclaude/cli/cli_portify/process.py` (245 lines)

#### Constructor signature — lines 131-145

```python
def __init__(
    self,
    *,
    prompt: str,
    output_file: Path,
    error_file: Path,
    work_dir: Path,
    workflow_path: Path,
    max_turns: int = 100,
    model: str = "",
    timeout_seconds: int = 300,
    extra_args: Optional[list[str]] = None,
    artifact_refs: Optional[list[Path]] = None,
    additional_dirs: Optional[list[Path]] = None,
) -> None:
```
Calls `super().__init__(...)` lines 154-163 with `output_format="text"`. Does **not** forward `tool_write_mode`, `permission_flag`, hooks, or `env_vars`.

#### stdin/argv handling — inherited; `build_command` override at lines 185-215

```python
185  def build_command(self) -> list[str]:
186      """Build claude CLI command with dual --add-dir flags."""
187      cmd = super().build_command()
...
208      # Insert before -p
209      try:
210          p_idx = cmd.index("-p")
211          cmd[p_idx:p_idx] = add_dir_args
212      except ValueError:
213          cmd.extend(add_dir_args)
214
215      return cmd
```
Because the base `build_command()` (pipeline/process.py:79-95) **never emits `-p`**, line 210's `cmd.index("-p")` always raises `ValueError`, and `--add-dir` is always appended at the end (line 213). The "insert before -p" intent is dead code. The flags still reach claude (positionally meaningless for `--add-dir`), but argv layout no longer matches the DESIGN.md anchor strategy and any tests that asserted "before -p" splice would now fail or be irrelevant.

#### Prompt sizing — inherited (none); plus `_build_prompt` prepends `@path` refs

Lines 178-183:
```python
@staticmethod
def _build_prompt(base_prompt: str, artifact_refs: list[Path]) -> str:
    if not artifact_refs:
        return base_prompt
    ref_lines = "\n".join(f"@{ref.resolve()}" for ref in artifact_refs)
    return f"{ref_lines}\n{base_prompt}"
```
This concatenates references onto the prompt before delegating to base; the resulting prompt is delivered via the same single `stdin.write()` at pipeline/process.py:142.

#### Signal handling — fully inherited from base.

#### Lifecycle hooks — `run()` wrapper at lines 217-245

```python
217  def run(self) -> ProcessResult:
218      """Start the subprocess, wait for completion, return ProcessResult."""
219      start = time.monotonic()
220      self.start()
221      exit_code = self.wait()
...
237      return ProcessResult(...)
```
No cancel polling; `wait()`'s timeout (line 162 in base) is the only escape.

#### New params/methods after pipx baseline

- `additional_dirs` + `MAX_ADDITIONAL_DIRS = 10` (line 25) + `consolidate_dirs()` helper (lines 71-113) + `resolution_log` attribute (lines 173, 176).
- `ProcessResult` dataclass (lines 49-63) with `succeeded` property.
- `detect_claude_binary()` module helper (lines 28-41).
- The `run()` synchronous return-result method (lines 217-245).

---

### `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py` (385 lines)

#### Constructor signature — lines 97-121

```python
def __init__(
    self,
    config: SprintConfig,
    phase: Phase,
    *,
    env_vars: dict[str, str] | None = None,
):
```
Positional `(config, phase)`, keyword `env_vars`. Calls `super().__init__(...)` lines 108-121 forwarding hook factories `_make_spawn_hook(phase, config)` (line 117) etc., and `output_format="stream-json"` (line 116).

#### stdin/argv handling — fully inherited from base.

The factory `_make_spawn_hook` at lines 30-55 logs `cmd="['claude', '--print', '--verbose']"` as a hard-coded string (line 45), not from `self.build_command()`. So even if `build_command()` later changed, the debug log line is frozen.

#### Prompt sizing — `build_prompt()` lines 123-216

Composes a multi-section markdown prompt from phase metadata. The `Sprint Context` block (lines 147-167) references prior artifact dirs and phase dirs. Plausible size: a few KB to ~10 KB depending on number of phases.

`build_task_context()` (lines 257-319) and `compress_context_summary()` (lines 347-385) are **standalone helpers**, not used by `build_prompt()` itself. They are invoked from `sprint/executor.py` for prior-task injection — see caller analysis below.

#### Signal handling — `SignalHandler` class lines 219-249

Sprint-specific. Sets `shutdown_requested = True` on SIGINT/SIGTERM (line 249); the executor poll loop terminates the active claude subprocess. Saves and restores original handlers (lines 234-246).

#### Lifecycle hooks

Hook factories at lines 30-85 build closures that capture `phase` and `config`. The hooks themselves only call `debug_log(...)`. No subclass override of `start`/`wait`/`terminate`.

#### New constructor params/methods after pipx baseline

- `env_vars` kwarg at line 102 (forwarded to base via line 120).
- `_make_spawn_hook`, `_make_signal_hook`, `_make_exit_hook` factories (lines 30-85). These move what may have been method overrides into hook closures.
- `build_task_context`, `get_git_diff_context`, `compress_context_summary` module-level context builders (lines 257-385) — used by executor, not by this class.

---

### `/config/workspace/IronClaude/src/superclaude/cli/cleanup_audit/process.py` (72 lines)

#### Constructor signature — lines 29-42

```python
def __init__(self, config: CleanupAuditConfig, step: CleanupAuditStep):
    self.config = config
    self.step = step
    prompt = self.build_prompt()
    super().__init__(
        prompt=prompt,
        output_file=config.work_dir / f"{step.id}-output.jsonl",
        error_file=config.work_dir / f"{step.id}-error.log",
        max_turns=config.max_turns,
        model=config.model,
        permission_flag=config.permission_flag,
        timeout_seconds=step.timeout_seconds,
        output_format="stream-json",
    )
```
No keyword-only marker, no hook wiring, no `env_vars`, no `tool_write_mode`.

#### stdin/argv handling — fully inherited.

#### Prompt sizing — `build_prompt()` lines 44-46

```python
def build_prompt(self) -> str:
    """Build the prompt for this audit step."""
    return self.step.prompt
```
Pass-through. Size depends entirely on `step.prompt` content.

#### Signal handling — `SignalHandler` class lines 49-72

Identical pattern to sprint. Note this class exposes `restore()` (line 64), not `uninstall()` like the sprint variant — minor API drift between the two.

#### Lifecycle hooks — none wired.

#### New params/methods after pipx baseline — none on this subclass.

#### Surprise: `is_running()` and `stop()` are called by the executor but DO NOT EXIST.

`cleanup_audit/executor.py:91` does `while process.is_running():`, `:93` does `process.stop()`, `:97` does `process.stop()`. Neither method is defined on `CleanupAuditProcess` (this file) nor on the base `ClaudeProcess` (`pipeline/process.py`). Confirmed by:
```
grep -n 'def is_running\|def stop\b' .../cleanup_audit/process.py .../pipeline/process.py  ->  (no matches)
```
This audit executor would `AttributeError` on its first iteration. Not introduced by stdin work, but pre-existing.

---

## Specific questions answered

### 1. Is `cli_portify/process.py`'s `cmd.index("-p")` lookup currently broken?

**Yes, effectively dead.** The base `build_command()` no longer emits `-p` (cli/pipeline/process.py:79-91 quoted above shows the cmd list ending at `--output-format`/`output_format` with no `-p`). The override at cli_portify/process.py:208-213:
```python
208      # Insert before -p
209      try:
210          p_idx = cmd.index("-p")
211          cmd[p_idx:p_idx] = add_dir_args
212      except ValueError:
213          cmd.extend(add_dir_args)
```
always hits `except ValueError` and appends to the end. The `--add-dir` flags still reach claude (claude accepts them positionally), but the comment "Insert before -p" is misleading and the splice-point semantics from DESIGN.md §6.3 are not preserved.

### 2. What does `tool_write_mode` do?

It is a flag that **redirects stdout to a `.log` sidecar** so the LLM is expected to author the real output file via its own Write/Edit tools. It does **NOT** pass any flag to claude — there is no claude-side argv contribution from this mode.

- Defined on `Step`: `cli/pipeline/models.py:98` — `tool_write_mode: bool = False`.
- Set at construction sites: `cli/roadmap/executor.py:1927`, `:1945`, `:2008` — set to `_roadmap_template is not None` for the `generate-A`, `generate-B`, and `merge` steps.
- Forwarded to `ClaudeProcess` constructor: `cli/roadmap/executor.py:1117` — `tool_write_mode=step.tool_write_mode`.
- Stored: `cli/pipeline/process.py:53,68`.
- Consumed in `start()` at `cli/pipeline/process.py:118-122`:
  ```python
  if self.tool_write_mode:
      # LLM writes output_file via Write tool; stdout goes to .log
      self._stdout_fh = open(self.output_file.with_suffix(".log"), "w")
  else:
      self._stdout_fh = open(self.output_file, "w")
  ```
- Validated post-exit: `cli/pipeline/process.py:216-236` (`validate_tool_write_output()`) — returns False if `output_file` missing or empty. Called from `cli/roadmap/executor.py:1161`.
- Prompt is also wrapped with template/incremental-write framing at `cli/roadmap/executor.py:1089-1105` via `wrap_for_incremental_write(...)`.

No claude CLI flag is passed; the contract is purely behavioral (the prompt instructs the LLM to write the file; the wrapper checks it did).

### 3. Synchronous stdin write that could block on full pipe buffer?

**Yes.** `cli/pipeline/process.py:140-146`:
```python
try:
    if self._process.stdin is not None:
        self._process.stdin.write(self.prompt.encode("utf-8"))
        self._process.stdin.close()
except BrokenPipeError:
    pass
```
This is a single synchronous `write()` of the **entire encoded prompt** on the parent thread. The Linux pipe buffer is typically 64 KiB; if `claude` is slow to start consuming stdin, a 338 KB prompt will fill the pipe and `write()` blocks. Stdout/stderr are real file FDs (`self._stdout_fh`, `self._stderr_fh` opened at lines 120-123), so there is no parent-side reader to deadlock — but the parent's `start()` itself stalls until claude drains stdin. The DESIGN.md daemon-thread strategy is **not** implemented; the `BrokenPipeError` handler exists but `os.write` chunking, EINTR retry, and writer-thread isolation do not.

### 4. Empty-prompt behavior?

There is **no guard**. If `prompt == ""`, then at `cli/pipeline/process.py:142` we call `self._process.stdin.write(b"")` (no-op write), then `close()` at 143 — claude receives EOF on stdin with zero bytes. The base `build_command()` does not include `-p ""` (it doesn't include `-p` at all — lines 79-95). Behavior: claude is launched and immediately gets EOF on stdin with no positional arg → behavior depends on claude's own handling, but the framework offers no defensive handling. Compare DESIGN.md row "0 bytes (empty string) → argv yes (-p '') → DEVNULL" — the current code does not match this; it sends empty stdin instead.

### 5. Does the constructor accept a list of CLI flags?

**Yes — `extra_args`** at `cli/pipeline/process.py:48`:
```python
extra_args: list[str] | None = None,
```
Stored at line 63 (`self.extra_args = extra_args or []`), appended verbatim to the cmd at line 94 (`cmd.extend(self.extra_args)`). Subclasses use it: `cli/prd/process.py:160` passes `extra_args=file_args` (the `--file` args built at `cli/prd/process.py:163-...`). PortifyProcess also forwards an `extra_args` kwarg through `super().__init__` at `cli/cli_portify/process.py:161`.

### 6. Stdin re-encoding or chunking?

**No chunking.** The only encoding step is `self.prompt.encode("utf-8")` at `cli/pipeline/process.py:142` — single shot. No `_iter_prompt_chunks`, no thread, no `os.write` loop, no EINTR handling. The DESIGN.md §6.2 protocol is absent.

### 7. Does `subprocess.PIPE` show up for stdin?

**Yes, unconditionally.** `cli/pipeline/process.py:125-130`:
```python
popen_kwargs = {
    "stdin": subprocess.PIPE,
    "stdout": self._stdout_fh,
    "stderr": self._stderr_fh,
    "env": self.build_env(env_vars=self._extra_env_vars),
}
```
Stdin is `subprocess.PIPE` for every invocation (no threshold branch).

### 8. Stdout/stderr piped, concurrent reader, deadlock risk?

**No.** `self._stdout_fh` and `self._stderr_fh` are real file handles opened at `cli/pipeline/process.py:120-123` (and `:122` for non-tool-write mode). They are **not** `subprocess.PIPE`, so the parent never reads from them. No concurrent reader thread. The deadlock surface is purely on the stdin side (Q3): a slow claude with full pipe buffer stalls the parent's synchronous `stdin.write()` call.

The docstring at lines 137-139 explicitly states: *"Deadlock-safe: stdout/stderr are real file handles, not pipes, so the parent never reads from the child and a blocked stdin write cannot deadlock."* — this is true with respect to a 4-way pipe deadlock, but **does not address parent-thread stall** from the stdin write blocking on a full kernel pipe buffer. A `terminate()` from another thread could still rescue, but the executor's cancel-poll loop sleeps 1s per iteration, so a stalled `start()` may never reach the poll loop.

---

## Caller analysis

### `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:1107-1118` (primary caller)

- Prompt construction: `cli/roadmap/executor.py:1072-1105`. `_embed_inputs(step.inputs, labels=labels)` (line 1072) reads each input file fully and embeds it as `## File: <path>\n```\n<content>\n``` ` blocks. Composed prompt = `step.prompt + "\n\n" + embedded` (line 1074). When `tool_write_mode` is on (line 1089), prompt is further wrapped via `wrap_for_incremental_write(...)` at lines 1101-1105.
- Plausible size: very large. Lines 1075-1081 emit a warning when composed > `_LARGE_PROMPT_WARN_BYTES`. The DESIGN.md problem statement names a real 338 KB case (181 KB PRD + 157 KB TDD).
- `-p`: never passed; `extra_args` at line 1116 is always `[]` (set at line 1083 or line 1086).
- Use of result: starts (line 1120), polls cancellation in 1s loop (lines 1123-1134), `wait()` at 1136, branches on exit codes (1139-1157), then `validate_tool_write_output()` at 1161 when tool_write_mode is on.

### `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py:1271-1287` (`_ClaudeRunner` adapter)

- Prompt construction: passes through whatever caller of `_ClaudeRunner.run(prompt)` provides. Used by the semantic/convergence layer.
- Plausible size: depends on caller — likely ≤ 100 KB but unbounded.
- `-p`: never passed.
- Use: `start()`, `wait()` with `KeyboardInterrupt → terminate()` (lines 1281-1286), reads `out_file.read_text()`. No cancel polling.

### `/config/workspace/IronClaude/src/superclaude/cli/roadmap/validate_executor.py:122-132`

- Prompt construction: `cli/roadmap/validate_executor.py:106-120`. Same `_embed_inputs` pattern (line 106). Composed prompt + `extra_args=[]` (line 117).
- Plausible size: large — embeds spec/tdd/prd/roadmap.
- `-p`: never passed.
- Use: `start()` (line 134), 1s cancel poll loop (lines 136-148), `wait()` (line 149).

### `/config/workspace/IronClaude/src/superclaude/cli/roadmap/remediate_executor.py:246-255`

- Prompt construction: `cli/roadmap/remediate_executor.py:222-241`. Reads `target_file` text (line 223), wraps in `## Current File Content\n\n```\n...\n```` (line 224), concatenates with `base_prompt`. Warns over `_LARGE_PROMPT_WARN_BYTES` (lines 226-233).
- Plausible size: file-content-bound. Could be 100+ KB if target file is large.
- `-p`: never passed.
- Use: `start()` (line 257), `wait()` with KeyboardInterrupt→terminate (258-262). No cancel polling.

### `/config/workspace/IronClaude/src/superclaude/cli/tasklist/executor.py:130-140`

- Prompt construction: `cli/tasklist/executor.py:114-128`. Same `_embed_inputs` pattern; warns over threshold; `extra_args=[]`.
- Plausible size: large — roadmap text plus inputs.
- `-p`: never passed.
- Use: `start()` (142), 1s cancel poll loop (144-155), `wait()` (157).

### `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1287-1290`

- Prompt construction: built inside the sprint subclass via `build_prompt()` (`cli/sprint/process.py:123-216`). Composes phase markdown — typically a few KB.
- Plausible size: small (few KB).
- `-p`: never passed.
- Use: `start()` (line 1288), uses `_process.poll()` directly in TUI loop (line 1303), terminates on shutdown signal (line 1305) or deadline (line 1307).

### `/config/workspace/IronClaude/src/superclaude/cli/cleanup_audit/executor.py:85-88`

- Prompt construction: `step.prompt` pass-through (`cli/cleanup_audit/process.py:44-46`). Size = whatever `CleanupAuditStep.prompt` was preset to.
- Plausible size: medium (audit step prompts are typically a few KB).
- `-p`: never passed.
- Use: `start()` (line 88), then `process.is_running()` (line 91) and `process.stop()` (lines 93, 97). **As noted, neither method exists** on the class hierarchy — this is broken regardless of stdin work.

### `/config/workspace/IronClaude/src/superclaude/cli/cli_portify/steps/*.py:71/73/109/159/324` (5 sites)

All instantiate `PortifyProcess(...)` and call `.run()` (the synchronous wrapper at `cli/cli_portify/process.py:217-245`). Prompts are built via local `_build_prompt(...)` helpers in each step. Sizes vary but typically embed analysis files. None pass `-p`.

---

## Surprises vs DESIGN.md baseline

1. **Always-stdin (no threshold).** DESIGN.md §3 prescribes a 96 KiB threshold with argv path for small prompts; current code is unconditional stdin and has no `-p` in the base argv at all (`cli/pipeline/process.py:79-95`). DESIGN.md AC-2/AC-4 ("byte-identical argv for small prompts") cannot hold under the current code.
2. **No daemon writer thread, no chunking, no EINTR handling.** DESIGN.md §6.2 specifies `_iter_prompt_chunks(64 KiB)` + `os.write` loop in a daemon thread + `_join_stdin_writer()`. Current code is one synchronous `stdin.write(...)` on the parent thread (`cli/pipeline/process.py:140-146`). Parent can stall on full-pipe-buffer.
3. **No `PROMPT_MAX_BYTES` cap, no `PromptTooLargeForArgv` exception, no `prompt_sidecar` kwarg.** DESIGN.md §4.1 / §4.3 features are entirely absent.
4. **`tool_write_mode` is wholly new and undescribed in DESIGN.md.** It rewrites `start()` to switch the stdout target to a `.log` sidecar (`cli/pipeline/process.py:118-122`) and adds a post-run `validate_tool_write_output()` (`cli/pipeline/process.py:216-236`). The `Step` dataclass adds matching `tool_write_mode` and `template_path` fields (`cli/pipeline/models.py:98-99`). Roadmap executor wires it for `generate-A`, `generate-B`, and `merge` steps (executor.py:1927, 1945, 2008).
5. **`PortifyProcess.build_command` `-p` lookup is silently dead.** Lines 208-213 always fall into the `except ValueError` branch because the base no longer emits `-p`. `--add-dir` flags get appended at the end rather than spliced. DESIGN.md §6.3 anchor strategy not implemented.
6. **Empty-prompt path differs from DESIGN.md.** DESIGN.md §6.1 row 1 expects `-p ""` + DEVNULL stdin; current code sends an empty stdin write + EOF (no `-p` ever).
7. **`CleanupAuditProcess`'s executor calls `is_running()`/`stop()` which are not defined** on either subclass or base. Pre-existing bug, but worth flagging as part of the surface area.
8. **`SignalHandler` API drift.** `sprint/process.py:241` exposes `uninstall()`; `cleanup_audit/process.py:64` exposes `restore()`. Same role, different method name. DESIGN.md does not address either.
