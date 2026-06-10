# Research: ClaudeProcess Primitive
**Topic type:** File Inventory + Integration Points
**Scope:** src/superclaude/cli/pipeline/process.py
**Status:** Complete
**Date:** 2026-06-08
---

## Import path (confirmed)

`ClaudeProcess` is importable two ways; both resolve to the same class:

- Direct module: `from superclaude.cli.pipeline.process import ClaudeProcess`
  — class defined at `src/superclaude/cli/pipeline/process.py:24`.
- Package re-export: `from superclaude.cli.pipeline import ClaudeProcess`
  — re-exported at `src/superclaude/cli/pipeline/__init__.py:74` and listed in `__all__` at `__init__.py:93`.

**Recommendation for the wrapper:** use the direct module import
`from superclaude.cli.pipeline.process import ClaudeProcess` — this is the
form every other reusing subpackage uses (roadmap/executor.py:33,
tasklist/executor.py:25, prd/process.py:24, cli_portify/process.py:19,
eval/claude_process.py:84). The spec §"How it slots in" (line 125) names
exactly this import. Confirmed.

NFR-007 (process.py:9): the module has **no imports from
`superclaude.cli.sprint` or `superclaude.cli.roadmap`** — it is a clean
generic primitive safe for a new `cli/reflect/` package to depend on.

---

## `__init__` signature — EVERY parameter, type, default

Defined `process.py:37-54`. All parameters are **keyword-only** (note the
bare `*` at line 39 — positional calls are rejected).

| Param | Type | Default | Source line | Notes |
|---|---|---|---|---|
| `prompt` | `str` | **required** | 37/55 | Delivered via stdin, not argv (see start()). |
| `output_file` | `Path` | **required** | 56 | stdout target (or `.log` sibling in tool_write_mode). |
| `error_file` | `Path` | **required** | 57 | stderr target. |
| `max_turns` | `int` | `100` | 43/58 | → `--max-turns`. |
| `model` | `str` | `""` | 44/59 | empty string ⇒ `--model` flag omitted (see build_command). |
| `permission_flag` | `str` | `"--dangerously-skip-permissions"` | 45/60 | Injected verbatim as a single argv token. |
| `timeout_seconds` | `int` | `6300` | 46/61 | Passed to `wait()`'s `Popen.wait(timeout=…)`. NOTE default is **6300 s**, NOT the spec's 3600 — wrapper must pass `timeout_seconds=3600` (NFR-5, spec line 40/125). |
| `output_format` | `str` | `"stream-json"` | 47/62 | → `--output-format`. Sprint default; roadmap callers pass `"text"`. Spec wants `"stream-json"` (line 123/125). |
| `extra_args` | `list[str] \| None` | `None` → `[]` | 48/63 | Appended AFTER all built flags incl. `--model` (build_command:94). |
| `on_spawn` | `Callable[[int], None] \| None` | `None` | 49/64 | Called post-Popen with `pid` (start():148-149). |
| `on_signal` | `Callable[[int, str], None] \| None` | `None` | 50/65 | Called before signal send in terminate() (183-184). |
| `on_exit` | `Callable[[int, int\|None], None] \| None` | `None` | 51/66 | Called before `_close_handles()` in wait()/terminate() (168-169, 212-213). |
| `env_vars` | `dict[str, str] \| None` | `None` | 52/67 | Stored as `self._extra_env_vars`; passed to `build_env(env_vars=…)` inside start() (129). |
| `tool_write_mode` | `bool` | `False` | 53/68 | If True, LLM writes `output_file` via Write tool; stdout redirected to `output_file.with_suffix(".log")` (118-122). |

There is **no** `cwd` parameter — the child inherits the parent's cwd
(Popen call at 134 passes no `cwd=`). This satisfies spec FR-10's "cwd
stays the project root" (line 30) automatically, as long as the wrapper
process itself runs from the repo root. Unverified whether the wrapper
needs to chdir; flag for the runner-design track.

Instance attributes initialized in `__init__`: all params stored as
`self.<name>`, plus `self._process = None` (69), `self._stdout_fh = None`
(70), `self._stderr_fh = None` (71). `_extra_env_vars` holds the
constructor's `env_vars` (67).

---

## `build_command()` — exact claude argv (process.py:73-95)

Built in this fixed order (73-91):

```
claude
--print
--verbose
<permission_flag>                 # default "--dangerously-skip-permissions"
--no-session-persistence
--tools default                   # two tokens: "--tools", "default"
--max-turns <max_turns>
--output-format <output_format>
```

Then conditionally (92-93): `if self.model:` → append `--model <model>`.
An **empty `model=""` omits the `--model` flag entirely** — so to force a
specific model the wrapper MUST pass a non-empty `model=`.

Finally (94): `cmd.extend(self.extra_args)` — extra_args land LAST, after
`--model`. Use this slot for reflect-specific passthrough flags
(`--mode post`, `--depth`, etc.) that become the slash-command prompt's
trailing tokens — though note these are CLI argv tokens to `claude`, not
to the slash command; the `/sc:reflect --mode post` invocation itself
lives in `prompt` (stdin), NOT extra_args. (Cross-check with R08 for the
reflect invocation surface.)

**Spec parity check (line 123):**
`claude --print --verbose --output-format stream-json --model <resolved> --dangerously-skip-permissions --max-turns <N>`
— all six elements are present in build_command. Argument ORDER differs
from the spec's illustrative string (actual order: `--print --verbose
<perm> --no-session-persistence --tools default --max-turns --output-format
[--model]`), but order is immaterial to `claude`. Two flags the spec
string omits but build_command always adds: `--no-session-persistence`
(84) and `--tools default` (85-86). These are harmless/desirable for the
headless reflect run. **Unverified:** whether `--no-session-persistence`
interferes with reflect's serena session corroboration — flag for R08, but
note spec FR-11 already treats `serena_summary_corroboration: unavailable`
as expected/non-halting (line 31), so this is likely fine.

Prompt is NOT in the argv (74-77 docstring): delivered via stdin to bypass
the Linux `MAX_ARG_STRLEN` 128 KB per-arg ceiling.

---

## `build_env(*, env_vars=None)` — LOAD-BEARING for FR-10 (process.py:97-112)

Exact behavior, line by line:

1. `env = os.environ.copy()` (107) — full snapshot copy of the parent
   environment. **Preserves HOME, PATH, all MCP registration vars, and
   `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` aliases** — nothing is
   stripped except the two vars below.
2. `env.pop("CLAUDECODE", None)` (108) — removes nested-session marker.
3. `env.pop("CLAUDE_CODE_ENTRYPOINT", None)` (109) — removes nested-session
   marker.
4. `if env_vars: env.update(env_vars)` (110-111) — caller-supplied dict is
   merged **with override semantics, applied AFTER the os.environ copy**,
   so injected keys win over inherited ones.
5. `return env` (112).

### Direct answer to the FR-10 question (spec line 30)

**`build_env` ALREADY pops the nested-session vars.** The wrapper does
**NOT** need to pop `CLAUDECODE` / `CLAUDE_CODE_ENTRYPOINT` itself — calling
`ClaudeProcess` (constructed normally) routes through `start()` →
`build_env(env_vars=self._extra_env_vars)` (process.py:129) automatically.

**`build_env` does NOT strip** `ANTHROPIC_DEFAULT_*` model aliases, `HOME`,
or MCP registration vars — it only pops the two `CLAUDECODE*` markers. So
the FR-10 requirement ("preserve HOME/MCP/ANTHROPIC_DEFAULT_* aliases but
pop nested-session vars") is satisfied **purely by the default
`ClaudeProcess` construction path** — no custom env overlay is required for
the preservation half, and the popping half is built in.

**Implication for the wrapper:**
- If the wrapper passes `env_vars=None` (or omits it), the child inherits
  the operator's real env minus the two nested markers — exactly FR-10's
  "bare real-env overlay."
- The wrapper does NOT need `HomeIsolation`/`ClaudeProcessAdapter` from
  `cli/eval/claude_process.py` — that path builds a hermetic mkdtemp HOME
  (see eval/claude_process.py:84+ usage), which would strip the MCP+alias
  vars FR-10 depends on. The plain `ClaudeProcess` is the correct primitive.
  (Spec lines 30, 67, 110 reach the same conclusion; source confirms the
  mechanism.)
- FR-11's "count `ANTHROPIC_DEFAULT_*` aliases in the exact child env"
  (line 31): the wrapper can reconstruct the exact child env by calling
  `build_env()` on a throwaway/constructed instance (it's a public method,
  no side effects, returns a plain dict) and counting matching keys.
  `build_env` is safe to call standalone for preflight — it neither spawns
  nor mutates `os.environ` (it copies). **Verified:** pure function of
  `os.environ` + `env_vars` arg.

---

## `start()` — subprocess spawn (process.py:114-157)

- Ensures `output_file.parent` exists (116, `mkdir(parents=True, exist_ok=True)`).
- Opens output handle (118-122): tool_write_mode=False → `open(output_file,"w")`;
  tool_write_mode=True → `open(output_file.with_suffix(".log"),"w")` (LLM
  writes the real output_file itself via Write tool).
- Opens `error_file` for stderr (123, `open(error_file,"w")`).
- `popen_kwargs` (125-130): `stdin=subprocess.PIPE`, `stdout=<file handle>`,
  `stderr=<file handle>`, `env=self.build_env(env_vars=self._extra_env_vars)`.
  **stdout/stderr are real FILE handles, not pipes** → the parent never
  reads from the child, so a blocked stdin write cannot deadlock (per the
  136-139 comment).
- Process-group isolation (131-132): `if hasattr(os,"setpgrp"):
  popen_kwargs["preexec_fn"] = os.setpgrp` — child starts in its own
  process group so the whole tree can be killed together.
- Spawn (134): `subprocess.Popen(self.build_command(), **popen_kwargs)`.
- **Prompt delivery (140-146):** if `self._process.stdin is not None`,
  `stdin.write(self.prompt.encode("utf-8"))` then `stdin.close()`.
  Encoding is **UTF-8**, and stdin is **closed immediately after the
  write** (EOF signaled). `BrokenPipeError` is swallowed (child exited
  early; wait() surfaces the code).
- `on_spawn(pid)` fired if set (148-149); debug log (151-155).
- **Returns** the `subprocess.Popen` object (157).

The wrapper's `self._process` is reachable as `proc._process` after start()
— the roadmap executor polls `proc._process.poll()` for cancellation
(roadmap/executor.py ~1196). For the wrapper's blocking-foreground default
(spec line 71: `proc.start(); rc = proc.wait()`), no polling is needed.

---

## `wait()` — exit code + timeout (process.py:159-171)

- `self._process.wait(timeout=self.timeout_seconds)` (162).
- **On `subprocess.TimeoutExpired`** (163-165): calls `self.terminate()`
  (SIGTERM→SIGKILL escalation) then **returns `124`** — explicitly chosen
  to match the bash `timeout` exit code (comment line 165). This is the
  signal the wrapper maps to the `blocked`/timeout verdict per spec NFR-5
  (line 40). On the timeout path, `on_exit` is NOT called by wait() itself,
  but terminate() fires `on_exit` with the post-kill returncode (212-213).
- On normal exit (167): `rc = returncode if not None else -1`, then
  `on_exit(pid, rc)` if set (168-169), `_close_handles()` (170),
  `return rc` (171).

**Exit-code contract for the wrapper verdict mapping:**
- `124` → timeout (terminate() was invoked). Maps to `blocked`/timeout.
- `-1` → returncode was None unexpectedly (defensive fallback).
- any other int → the child `claude` process's real exit code.

---

## `terminate()` — SIGTERM→SIGKILL escalation (process.py:173-214)

- No-op + close handles if process is None or already exited (175-177).
- Process-group capable iff `os.getpgid` AND `os.killpg` exist (179);
  `pgid = os.getpgid(pid)` (180).
- `on_signal(pid,"SIGTERM")` if set (183-184), then **SIGTERM to the whole
  process group** via `os.killpg(pgid, SIGTERM)` (186), else fallback
  `self._process.terminate()` (188). `ProcessLookupError` → close + return
  (190-192).
- Grace wait **10 s** (195, `wait(timeout=10)`).
- On `TimeoutExpired` (196): **SIGKILL the process group** `os.killpg(pgid,
  SIGKILL)` (199) else `self._process.kill()` (201), then `wait(timeout=5)`
  (203). `ProcessLookupError`/`TimeoutExpired` swallowed (204-205).
- `on_exit(pid, returncode)` if set (212-213); `_close_handles()` (214).

This is exactly the "SIGTERM→SIGKILL via process group" the spec promises
(NFR-5, line 40). The wrapper inherits it for free; no signal code needed.

---

## Other public methods/attributes the wrapper may touch

- `build_command() -> list[str]` (73) — public; the wrapper can call it for
  `--print-command`/`--dry-run` to print the exact argv WITHOUT launching
  (spec FR-12, line 32). Pure (no side effects). NOTE: it does NOT include
  the prompt (stdin); for a faithful dry-run print the wrapper should also
  surface `self.prompt` separately.
- `build_env(*, env_vars=None) -> dict[str,str]` (97) — public; usable for
  FR-11 preflight alias counting (see above).
- `validate_tool_write_output() -> bool` (216-236) — only meaningful when
  `tool_write_mode=True`; returns True if `output_file` exists and is
  non-empty. The reflect wrapper consumes a separate `return-contract.yaml`
  (R02), so this is likely irrelevant unless the wrapper uses
  tool_write_mode for the contract file. Flag for runner-design track.
- `start() -> Popen` (114), `wait() -> int` (159), `terminate() -> None`
  (173) — the core lifecycle trio the wrapper drives.
- `_process`, `_stdout_fh`, `_stderr_fh`, `_close_handles()` — "private"
  but `_process` is read by existing callers (roadmap poll loop). The
  wrapper's blocking default does not need `_process`.

---

## Summary (for the wrapper / FR-1, FR-10, NFR-2, NFR-5)

1. **Import:** `from superclaude.cli.pipeline.process import ClaudeProcess`
   (process.py:24; also re-exported at pipeline/__init__.py:74). Clean of
   sprint/roadmap deps (NFR-007).

2. **Construction (all kwargs-only, `*` at line 39):** the spec's intended
   call —
   `ClaudeProcess(prompt=…, output_file=…, error_file=…, model=<resolved>,
   timeout_seconds=3600, output_format="stream-json", env_vars=None)` — is
   directly supported. **Two defaults the wrapper MUST override:**
   `timeout_seconds` defaults to **6300** not 3600 (pass 3600 for NFR-5),
   and `model=""` omits `--model` so a non-empty model must be passed for
   parity with spec line 123. `output_file`/`error_file` are required Paths.

3. **FR-10 env (the load-bearing question):** `build_env` (97-112) does
   `os.environ.copy()`, then pops ONLY `CLAUDECODE` and
   `CLAUDE_CODE_ENTRYPOINT`. It **already pops the nested-session vars** —
   the wrapper does NOT need to. It does **NOT** strip HOME / MCP vars /
   `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` — those are preserved
   automatically. So the "bare real-env overlay that preserves aliases +
   pops nested-session vars" is the DEFAULT `ClaudeProcess` behavior with
   `env_vars=None`. No `HomeIsolation`/`ClaudeProcessAdapter` needed (and
   it would be wrong — it hermetically isolates HOME). `build_env()` is a
   safe standalone pure-ish call (copies os.environ; no spawn, no mutation)
   for FR-11 preflight alias counting.

4. **NFR-2 reuse:** subprocess spawn (Popen, start():134), stdin UTF-8
   prompt delivery + immediate close (142-143), stdout/stderr→file
   separation (120-123), env scrub (build_env), process-group isolation
   (preexec_fn=os.setpgrp, 131-132), timeout→124 (wait():162-165), and
   SIGTERM(10s)→SIGKILL process-group escalation (terminate():173-214) are
   ALL inherited. The wrapper writes none of this.

5. **NFR-5 timeout:** `wait()` returns **124** on `TimeoutExpired` after
   invoking terminate() (165). Wrapper maps 124 → blocked/timeout verdict.

6. **FR-12 dry-run:** `build_command()` (73) and `build_env()` (97) are
   public and side-effect-free — callable for `--print-command`/`--dry-run`
   without launching. Remember to also surface `self.prompt` (stdin, not in
   argv) for a complete dry-run preview.

7. **argv (build_command 73-95):** always emits
   `claude --print --verbose <permission_flag> --no-session-persistence
   --tools default --max-turns <N> --output-format <fmt> [--model <m>]
   <extra_args…>`. Two extra always-on flags vs. the spec's illustrative
   string: `--no-session-persistence` and `--tools default` (benign for
   headless reflect; cross-check serena-session impact with R08, but FR-11
   already treats serena corroboration loss as non-halting).

**Unverified / flagged for other tracks:**
- Whether `--no-session-persistence` affects reflect's serena
  corroboration (→ R08).
- The `/sc:reflect --mode post …` slash invocation goes in `prompt`
  (stdin), not in build_command's argv; reflect's flag surface (→ R08).
- Whether the wrapper needs to chdir to repo root (no `cwd=` param;
  inherits parent cwd — FR-10 line 30 wants project root).
