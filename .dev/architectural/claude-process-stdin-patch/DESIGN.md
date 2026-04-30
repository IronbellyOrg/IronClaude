# Design — `ClaudeProcess` stdin-delivery patch for prompts exceeding `MAX_ARG_STRLEN`

| Field             | Value                                                                                          |
|-------------------|------------------------------------------------------------------------------------------------|
| Status            | Approved by /sc:adversarial (87% convergence); Risk #1 verified 2026-04-30 on `claude 2.1.123` |
| Type              | Component design (subprocess lifecycle)                                                        |
| Owner             | SuperClaude framework — pipeline subsystem                                                     |
| Source-of-truth   | `src/superclaude/cli/pipeline/process.py`                                                      |
| Active path       | `.claude/.../pipeline/process.py` (synced via `make sync-dev`)                                 |
| Date              | 2026-04-30                                                                                     |
| Adversarial input | `.dev/architectural/claude-process-stdin-patch/adversarial/merged-output.md`                   |

---

## 1. Problem Statement

`ClaudeProcess` (in `pipeline/process.py:24-203`) builds a `claude --print` subprocess invocation that passes the full prompt as a single argv element via `-p <PROMPT>`. Linux's per-argument size limit `MAX_ARG_STRLEN = PAGE_SIZE * 32 = 128 KiB` causes `execve(2)` to fail with `OSError: [Errno 7] Argument list too long` for any prompt that pushes that single argv element above 128 KiB.

The failure surfaces in roadmap pipelines that inline-embed source documents into the step prompt: a 181 KB PRD plus a 157 KB TDD composes a ≈338 KB prompt, ~2.7× the kernel limit, and the pipeline's `extract` step crashes before it can talk to the model.

**Goal:** deliver large prompts to `claude` reliably while preserving observable behavior for all current callers.

## 2. Architectural Context

```
┌─────────────────────────────────────────────────────────────────────────┐
│  superclaude.cli.pipeline                                                │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  process.py                                                         │ │
│  │   ClaudeProcess (base)                                              │ │
│  │     ├── start() / wait() / terminate()                              │ │
│  │     ├── build_command()                                             │ │
│  │     └── build_env()                                                 │ │
│  └──────────────┬───────────────────┬────────────────┬────────────────┘ │
│                 │                   │                │                  │
│  ┌──────────────▼───────┐  ┌────────▼───────┐  ┌─────▼────────────────┐│
│  │ sprint.process       │  │ cleanup_audit  │  │ cli_portify          ││
│  │ ClaudeProcess(sub)   │  │ Process(sub)   │  │ PortifyProcess(sub)  ││
│  │                      │  │                │  │   overrides          ││
│  │ no build_command     │  │ no build_command  │  build_command()    ││
│  │ override             │  │ override       │  │   (uses cmd.index)   ││
│  └──────────────────────┘  └────────────────┘  └──────────────────────┘│
│                                                                         │
│  Direct callers (instantiate base ClaudeProcess):                       │
│    roadmap/executor.py:749        ← THIS IS WHERE THE BUG SURFACES      │
│    roadmap/validate_executor.py:117                                     │
│    roadmap/remediate_executor.py:245                                    │
│    tasklist/executor.py:127                                             │
└─────────────────────────────────────────────────────────────────────────┘
```

**Scope of change:** `pipeline/process.py` (primary) + `cli_portify/process.py` (2-line tweak). All other callers and subclasses untouched.

## 3. Design Overview

A **threshold-based dual-path delivery** for the prompt:

- **Argv path (legacy)**: prompts < 96 KiB ride argv via `-p <PROMPT>` exactly as today. `stdin = DEVNULL`.
- **Stdin path (new)**: prompts ≥ 96 KiB are stripped from argv; a daemon thread streams the prompt into the child's stdin and closes the write end. `claude --print` reads from stdin when the positional prompt argument is absent.

The threshold (`PROMPT_STDIN_THRESHOLD = 96 KiB`) leaves a 32 KiB margin under `MAX_ARG_STRLEN`, accommodating other argv elements, environment-variable budget pressure on `ARG_MAX`, and kernel-version drift.

## 4. Component Interface

### 4.1 Public surface (additive — no breaking changes)

```python
class ClaudeProcess:
    def __init__(
        self,
        *,
        prompt: str,                                # unchanged
        output_file: Path,
        error_file: Path,
        max_turns: int = 100,
        model: str = "",
        permission_flag: str = "--dangerously-skip-permissions",
        timeout_seconds: int = 6300,
        output_format: str = "stream-json",
        extra_args: list[str] | None = None,
        on_spawn: Callable[[int], None] | None = None,
        on_signal: Callable[[int, str], None] | None = None,
        on_exit: Callable[[int, int | None], None] | None = None,
        env_vars: dict[str, str] | None = None,
        prompt_sidecar: bool = False,               # NEW (default off)
    ) -> None: ...

    def build_command(self) -> list[str]: ...      # signature unchanged
    def start(self) -> subprocess.Popen: ...        # signature unchanged
    def wait(self) -> int: ...                      # signature unchanged
    def terminate(self) -> None: ...                # signature unchanged
    def build_env(self, *, env_vars=None) -> dict[str, str]: ...  # unchanged
```

### 4.2 New helpers (private)

```python
def _use_stdin_for_prompt(self) -> bool:
    """True iff encoded prompt size >= PROMPT_STDIN_THRESHOLD.
    Empty prompts (size 0) explicitly stay on argv path."""

def _prompt_anchor_flag(self) -> str:
    """Stable insertion anchor for subclasses that splice flags before the
    prompt. Returns '--output-format' — present in both delivery modes,
    immediately preceding the prompt-delivery flags."""

def _iter_prompt_chunks(self, chunk_size: int = 64 * 1024) -> Iterator[bytes]:
    """Stream-encode the prompt in chunks. Slices the source string by
    character index, encodes each slice. O(chunk_size) memory."""

def _join_stdin_writer(self, timeout: float = 5.0) -> None:
    """Best-effort join on the prompt-writer thread; called from wait()
    and terminate() before _close_handles()."""
```

### 4.3 New module-level constants & exception

```python
PROMPT_STDIN_THRESHOLD: int = 96 * 1024            # 98,304 bytes
PROMPT_MAX_BYTES: int = int(os.environ.get(
    "SUPERCLAUDE_PROMPT_MAX_BYTES", 16 * 1024 * 1024
))

class PromptTooLargeForArgv(ValueError):
    """Raised when the prompt is too large for argv delivery and the
    sanity cap is exceeded. Subclass of ValueError for backward-compat
    with callers catching ValueError."""
```

## 5. Sequence Diagrams

### 5.1 Small-prompt path (argv, unchanged)

```
caller                ClaudeProcess.start()       Popen / kernel       claude
  │                          │                          │                │
  │── start() ──────────────▶│                          │                │
  │                          │── build_command()        │                │
  │                          │   = [..., -p, prompt]    │                │
  │                          │── open stdout/stderr fhs │                │
  │                          │── Popen(stdin=DEVNULL)──▶│                │
  │                          │                          │── execve ─────▶│ argv parses, prompt visible
  │                          │── on_spawn(pid) ─────────│                │ claude reads no stdin (DEVNULL)
  │                          │── _log.debug(...) ───────│                │ runs, writes stdout/stderr to files
  │◀── return Popen ─────────│                          │                │
  │                          │                          │                │
  │── wait() ───────────────▶│                          │                │
  │                          │── proc.wait(timeout) ────│◀── exit ───────│
  │                          │── _join_stdin_writer()   │ (no thread, no-op)
  │                          │── _close_handles()       │
  │◀── exit code ────────────│                          │                │
```

### 5.2 Large-prompt path (stdin, new)

```
caller          ClaudeProcess.start()    Popen / kernel    Writer Thread        claude
  │                    │                       │                 │                │
  │── start() ────────▶│                       │                 │                │
  │                    │ encode prompt size    │                 │                │
  │                    │ if > PROMPT_MAX:      │                 │                │
  │                    │   raise PromptTooLargeForArgv           │                │
  │                    │ build_command() = [...] (no -p, no prompt)               │
  │                    │ open stdout/stderr fhs│                 │                │
  │                    │ open .prompt sidecar  │                 │                │
  │                    │   (if opted in)       │                 │                │
  │                    │ Popen(stdin=PIPE) ───▶│                 │                │
  │                    │                       │── execve ───────────────────────▶│ argv parses, no prompt, blocks reading stdin
  │                    │ spawn daemon thread ──────────────────▶ │                │
  │                    │ on_spawn(pid)         │                 │                │
  │                    │ _log.debug(prompt_via=stdin, ...)       │                │
  │◀── return Popen ───│                       │                 │                │
  │                    │                       │                 │ for chunk in iter_prompt_chunks(): ◀─────┐
  │                    │                       │                 │   os.write(fd, chunk)  ──────────────────│
  │                    │                       │                 │   (handles EINTR / BrokenPipe)           │
  │                    │                       │                 │   tee chunk → sidecar (if enabled)       │
  │                    │                       │                 │ stdin_fh.close()  ──── EOF ─────────────▶│ claude begins processing
  │                    │                       │                 │                │ writes output → file
  │── wait() ─────────▶│                       │                 │                │
  │                    │ proc.wait(timeout) ──│◀── exit ────────│ ──────────────│
  │                    │ _join_stdin_writer(5)──────────────────▶│ (already exited, immediate join)
  │                    │ _close_handles()      │                 │                │
  │◀── exit code ──────│                       │                 │                │
```

### 5.3 Cancellation mid-stream

```
caller (poll loop)              Writer Thread                   claude
       │                              │                            │
       │ poll() loop running          │ os.write(fd, chunk_N)      │ (alive, reading stdin)
       │ cancel_check() == True       │                            │
       │── terminate() ──┐            │                            │
       │                 ├─ killpg(SIGTERM) ────────────────────────▶ exits
       │                 │            │ next os.write → BrokenPipe │
       │                 │            │ caught; close stdin in finally
       │                 ├─ wait(10s) │ thread exits               │
       │                 ├─ _join_stdin_writer(5) → immediate      │
       │                 ├─ _close_handles()                       │
       │◀── return ──────┘            │                            │
```

## 6. Detailed Behavior

### 6.1 `_use_stdin_for_prompt()` decision table

| Prompt encoded size           | `_use_stdin_for_prompt()` | Argv contains `-p <prompt>` | stdin disposition |
|-------------------------------|---------------------------|------------------------------|-------------------|
| 0 bytes (empty string)        | False                     | yes (`-p ""`)                | DEVNULL           |
| 1 byte … 98,303 bytes         | False                     | yes                          | DEVNULL           |
| 98,304 bytes (96 KiB)         | True                      | no                           | PIPE              |
| 98,304 … 16,777,215 bytes     | True                      | no                           | PIPE              |
| > 16,777,216 bytes (16 MiB)   | True (raises in start())  | n/a                          | n/a (raises)      |
| Encoding failure              | True                      | no                           | PIPE              |

### 6.2 Stdin write protocol

1. `subprocess.Popen(..., stdin=subprocess.PIPE, stdout=fh, stderr=fh)`.
2. Spawn `threading.Thread(daemon=True)` named `claude-stdin-writer-<pid>`.
3. Thread iterates `_iter_prompt_chunks(64 * 1024)`:
   - Encode each character slice as UTF-8 with `errors="strict"`.
   - For each chunk, `os.write(fd, view)` in a loop until fully written; retry on `InterruptedError` (EINTR); terminate on `BrokenPipeError`.
   - If `prompt_sidecar=True`, also append the chunk to `output_file.with_suffix(".prompt")`.
4. **`finally`**: close child stdin (delivers EOF; required by `claude --print`), close sidecar handle.
5. Errors stored in `self._stdin_error`; surfaced in `_join_stdin_writer()` log line.

### 6.3 PortifyProcess subclass change (2 lines)

In `cli_portify/process.py:209-213`, replace direct `cmd.index("-p")` lookup with the stable anchor:

```python
# Before
try:
    p_idx = cmd.index("-p")
    cmd[p_idx:p_idx] = add_dir_args
except ValueError:
    cmd.extend(add_dir_args)

# After
try:
    anchor = cmd.index(self._prompt_anchor_flag())
    insert_at = anchor + 2          # skip flag and its value
except ValueError:
    insert_at = len(cmd)
cmd[insert_at:insert_at] = add_dir_args
```

For all current Portify invocations (small prompts), this produces byte-identical argv. For future large Portify prompts, `--add-dir` flags land in the same relative position even when `-p` is absent.

## 7. Compatibility Contract

| Concern                        | Guarantee                                                                                                  |
|--------------------------------|------------------------------------------------------------------------------------------------------------|
| Constructor signature          | One added kwarg (`prompt_sidecar=False`). All existing call sites work unmodified                           |
| `self.prompt` attribute        | Always equals the constructor's `prompt` argument (no value-erasure for large prompts)                      |
| `build_command()` argv shape   | Identical for prompts < 96 KiB. For ≥ 96 KiB, drops `-p` and the prompt; all other elements unchanged       |
| `cmd[:3]` debug log            | Unchanged: `['claude', '--print', '--verbose']` in both modes (sprint/audit log scrapers continue to work) |
| Sprint subclass                | No code change. Inherits new behavior; sprint prompts (~few KB) always take argv path                       |
| Audit subclass                 | No code change. Same as sprint                                                                              |
| Portify subclass               | 2-line tweak in `build_command()` to use `_prompt_anchor_flag()`; produces byte-identical argv for small prompts |
| Existing tests                 | Pass unchanged. New tests added (§9) for stdin path and boundary cases                                      |
| Environment handling           | `build_env()` unchanged; same `CLAUDECODE` / `CLAUDE_CODE_ENTRYPOINT` stripping                             |
| Process group / signals        | Unchanged. `preexec_fn=os.setpgrp` still gates child into its own pgroup                                    |
| Cancellation polling           | Unchanged. Daemon writer thread isolates parent's poll loop from stdin write progress                       |

## 8. Module Layout

### 8.1 Files modified

| File                                        | Change       | Net LOC delta |
|---------------------------------------------|--------------|---------------|
| `src/superclaude/cli/pipeline/process.py`   | Primary      | ~+95 lines    |
| `src/superclaude/cli/cli_portify/process.py`| 2-line tweak | +5 / −4       |

### 8.2 Files added

| File                                                                | Purpose                                  |
|---------------------------------------------------------------------|------------------------------------------|
| `tests/cli/pipeline/conftest.py` (extend)                           | Fixtures for mock claude, prompt sizes   |
| `tests/cli/pipeline/test_claude_process_delivery.py` (new)          | Unit + e2e tests (§9)                    |

### 8.3 Files NOT modified

- `roadmap/executor.py` — `_EMBED_SIZE_LIMIT` warning at lines 735-742 stays as advisory; remove in beat 2 once stdin path is proven.
- All other callers (`validate_executor.py`, `remediate_executor.py`, `tasklist/executor.py`, `sprint/executor.py`).
- Sprint and audit subclasses.

## 9. Test Strategy

### 9.1 Coverage matrix

| Behavior                                                  | Test                                                          |
|-----------------------------------------------------------|---------------------------------------------------------------|
| Small prompt → argv path                                  | `test_build_command_keeps_p_flag_for_small_prompt`            |
| Huge prompt → stdin path, `-p` absent                     | `test_build_command_omits_p_flag_for_large_prompt`            |
| No argv element exceeds MAX_ARG_STRLEN                    | `test_argv_total_byte_size_bounded_for_huge_prompt`            |
| Threshold boundary (95 KiB → argv)                        | `test_threshold_boundary_under`                               |
| Threshold boundary (97 KiB → stdin)                       | `test_threshold_boundary_over`                                |
| Empty prompt preserved on argv (`-p ""`)                  | `test_empty_prompt_uses_argv_with_empty_p_value`              |
| End-to-end huge prompt round-trip via stdin               | `test_huge_prompt_delivered_via_stdin`                        |
| End-to-end small prompt still uses argv                   | `test_small_prompt_still_uses_argv`                           |
| UTF-8 multibyte (200 KB emoji) round-trip                 | `test_huge_utf8_emoji_prompt_round_trip`                      |
| `PROMPT_MAX_BYTES` cap raises typed exception             | `test_prompt_max_bytes_guard`                                 |
| SIGTERM mid-write does not hang or leak the writer thread | `test_terminate_during_stdin_write_no_hang`                   |
| Portify regression — small prompt argv layout unchanged   | `test_portify_add_dir_insertion_unchanged_for_small_prompt`   |
| Portify regression — large prompt still gets `--add-dir`  | `test_portify_add_dir_insertion_works_for_large_prompt`       |
| `--output-format` and value are adjacent argv elements    | `test_output_format_flag_and_value_are_adjacent`              |
| Sidecar is written when opted in                          | `test_prompt_sidecar_written_when_opted_in`                   |
| No sidecar by default                                     | `test_no_sidecar_by_default`                                  |

### 9.2 Test execution

Per CLAUDE.md UV-only rule:
```
uv run pytest tests/cli/pipeline/test_claude_process_delivery.py -v
```

CI integration: per project policy ("Validation should be done via the .github actions"), add the suite to the existing pipeline workflow. No one-off scripts.

## 10. Operational Considerations

### 10.1 Observability

- Existing `_log.debug("spawn pid=%d cmd=%s", ..., self.build_command()[:3])` is preserved unchanged.
- New fields appended to the same debug line: `prompt_via=stdin|argv`, `prompt_bytes=N`, `sidecar=bool`.
- Optional `.prompt` sidecar file (opt-in via `prompt_sidecar=True`) provides an operator-readable "what did claude actually see?" record when stdin mode hides the prompt from `ps`.
- Recommended caller policy: roadmap-family executors opt **in** to the sidecar (large prompts, debugging value); sprint/audit opt **out** (high-frequency phases, disk-bloat avoidance).

### 10.2 Rollback

- The threshold-based design is naturally rollback-friendly: setting `PROMPT_STDIN_THRESHOLD = 2**31` reverts to argv-only behavior without code change.
- For emergency rollback at runtime: revert the patched `process.py` from git; no caller code or data migration is required.

### 10.3 Deployment

**Immediate (operator unblock today):** vendored monkey-patch in the consumer repo at `.dev/claude_process_stdin_patch.py`, imported via the project's superclaude wrapper. Survives `pipx upgrade`.

**Durable:**
1. Branch: `fix/claude-process-stdin-large-prompts`
2. Apply diffs to `src/superclaude/cli/pipeline/process.py` and `src/superclaude/cli/cli_portify/process.py`.
3. Add `tests/cli/pipeline/test_claude_process_delivery.py`.
4. `make sync-dev && make verify-sync && make test`.
5. PR with this DESIGN.md as the design doc.
6. After merge & release: `pipx upgrade superclaude` ships the fix.

## 11. Risk Register

| # | Risk                                                                                                            | L | I | Score | Mitigation                                                                                                                                                                |
|---|-----------------------------------------------------------------------------------------------------------------|---|---|-------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | ~~A-001 / INV-005 — pinned `claude` does not read stdin in `--print` when positional arg is omitted~~ **VERIFIED RESOLVED** | — | — | **0** | Verified 2026-04-30 against `claude 2.1.123 (Claude Code)`. Three probes passed: (a) baseline with positional prompt; (b) stdin-only, no positional arg — claude returned expected output, exit 0; (c) ~200 KB stdin prompt — claude returned expected output, exit 0. Risk closed |
| 2 | PortifyProcess `cmd.index("-p")` raises ValueError for theoretical large Portify prompts                        | L | M | 2     | §6.3 anchor change makes Portify stdin-safe; CI test covers both small and large Portify prompts                                                                          |
| 3 | Writer thread leak if stdin close path is missed                                                                | L | H | 3     | `try/finally close()`; `_join_stdin_writer(timeout=5)` in both `wait()` and `terminate()`; daemon=True bounds leak                                                       |
| 4 | Prompt-size explosion now that stdin "just works"                                                               | M | M | 4     | `PROMPT_MAX_BYTES` cap (16 MiB default, env-overridable) raises `PromptTooLargeForArgv` before fork; debug log records `prompt_bytes=N` for monitoring                    |
| 5 | claude CLI behavior change in a future Anthropic release                                                        | L | H | 3     | Pin `claude` CLI version range in installation docs; sidecar (when enabled) gives prompt replay capability                                                                 |
| 6 | Sidecar file disk-bloat                                                                                          | L | L | 1     | Off by default; opt-in only; cleanup follows existing `output_file` lifecycle; automated rotation deferred to beat 2                                                      |

## 12. Open Questions

1. ~~Does pinned `claude --print` accept a missing positional prompt argument and read stdin?~~ **YES** — verified 2026-04-30 on `claude 2.1.123`.
2. ~~Trailing newline / framing requirements?~~ **None** — `echo` adds a trailing newline and probe 2 passed; the 200 KB probe also worked. No defensive `\n` needed.
3. **Per-caller threshold override?** Out of scope for this design. Add `force_prompt_via` kwarg in beat 2 if needed.
4. **`prompt_bytes=N` in production debug logs — acceptable?** Sizes are not content but may be a compliance signal in some contexts. Decide before merging.
5. **Downgrade `_EMBED_SIZE_LIMIT` warnings at call sites to debug?** Defer until stdin path proves stable.

## 13. Beat-2 Follow-ups (NOT part of this design)

These are recorded so they don't get lost; they are explicitly out of scope:

- Introduce `pre_prompt_args: list[str]` mechanism on base; migrate `PortifyProcess` to set it in `__init__` and delete its `build_command` override entirely.
- Promote stdin to default delivery for all prompt sizes once the sidecar observability story is mature.
- `--input-format=stream-json` delivery for tool-use orchestration.
- Automated rotation/cleanup of `.prompt` sidecars (TTL or pipeline-bound).
- Optional `PromptSource` Protocol if a second concrete source (file, stream-json) actually ships.

## 14. Acceptance Criteria

The design is implemented correctly when **all** of the following hold:

- [ ] **AC-1**: A 400 KB prompt produces a successful `claude --print` invocation; output round-trips byte-identical (verified by `test_huge_prompt_delivered_via_stdin`).
- [ ] **AC-2**: A small prompt's argv is byte-identical to pre-patch behavior (verified by `test_small_prompt_still_uses_argv`).
- [ ] **AC-3**: No argv element ever exceeds `MAX_ARG_STRLEN = 128 KiB`, regardless of prompt size (verified by `test_argv_total_byte_size_bounded_for_huge_prompt`).
- [ ] **AC-4**: PortifyProcess produces byte-identical argv layout for small prompts (verified by `test_portify_add_dir_insertion_unchanged_for_small_prompt`).
- [ ] **AC-5**: SIGTERM during stdin write does not leak the writer thread (verified by `test_terminate_during_stdin_write_no_hang`).
- [ ] **AC-6**: 200 KB UTF-8 multibyte prompt round-trips correctly (verified by `test_huge_utf8_emoji_prompt_round_trip`).
- [ ] **AC-7**: A prompt above `PROMPT_MAX_BYTES` raises `PromptTooLargeForArgv` before `fork()` (verified by `test_prompt_max_bytes_guard`).
- [x] **AC-8**: P0 release-gate probe passes — verified 2026-04-30 on `claude 2.1.123` with stdin-only and ~200 KB stdin payload, exit 0 in both cases.
- [ ] **AC-9**: `make verify-sync` passes after `src/superclaude/` edits → `make sync-dev`.
- [ ] **AC-10**: Full `make test` suite passes.

## 15. Implementation Plan

| Phase | Task                                                                                  | Deliverable                                                  |
|-------|---------------------------------------------------------------------------------------|--------------------------------------------------------------|
| ~~P0~~ | ~~Risk-gate verification — run the live `claude` stdin probe~~ **DONE 2026-04-30**  | ✅ Verified on `claude 2.1.123`; all 3 probes passed         |
| P1    | Apply patch to `src/superclaude/cli/pipeline/process.py` per §4-§6                    | Modified base class                                           |
| P2    | Apply 2-line PortifyProcess tweak per §6.3                                            | Modified subclass                                             |
| P3    | Add tests per §9 to `tests/cli/pipeline/test_claude_process_delivery.py`              | Test suite green locally via `uv run pytest`                  |
| P4    | `make sync-dev && make verify-sync && make test`                                      | `.claude/` synced; CI-equivalent green                        |
| P5    | Open upstream PR with this DESIGN.md attached                                         | PR URL                                                        |
| P6    | Vendored monkey-patch in consumer repo for immediate unblock                          | `.dev/claude_process_stdin_patch.py` + wrapper wiring         |
| P7    | Re-run failing roadmap pipeline command end-to-end                                    | Successful `superclaude roadmap run …` with 338 KB composed prompt |

The vendored monkey-patch (P6) and upstream PR (P5) proceed in parallel. When the upstream release ships, `pipx upgrade superclaude` makes the monkey-patch redundant and it can be removed.

---

## Appendix A — Cited Line Ranges (verified 2026-04-30)

- `pipeline/process.py:71-91` — current `build_command` with `-p` argv.
- `pipeline/process.py:110-137` — `start()` with `stdin=DEVNULL`, `cmd[:3]` debug log.
- `pipeline/process.py:139-194` — `wait`/`terminate`/`_close_handles` lifecycle.
- `pipeline/process.py:114-115` — stdout/stderr file FD invariant.
- `cli_portify/process.py:185-215` — `PortifyProcess.cmd.index("-p")` insertion point.
- `sprint/process.py:88-121` — sprint subclass.
- `cleanup_audit/process.py:22-47` — audit subclass.
- `roadmap/executor.py:719-759` — primary caller; embed-size warning at 735-742.
- `roadmap/executor.py:319-328` — `_MAX_ARG_STRLEN = 128 * 1024`, `_EMBED_SIZE_LIMIT = 120 KB`.
- `roadmap/executor.py:763-775` — cancellation polling loop.
- `roadmap/validate_executor.py:117-140` — sibling caller.
- `roadmap/remediate_executor.py:245` — sibling caller.
- `tasklist/executor.py:127-141` — sibling caller.
- `sprint/executor.py:1248-1271` — TUI tail-pane updater + signal handler.

## Appendix B — Source Adversarial Pipeline Outputs

All artifacts under `.dev/architectural/claude-process-stdin-patch/adversarial/`:

- `variant-1-original.md` — Proposal A (selected base; minimal-blast-radius)
- `variant-2-original.md` — Proposal B (strategy-pattern; partially incorporated)
- `diff-analysis.md` — 23 diff points across structure, content, contradictions, unique contributions, shared assumptions
- `debate-transcript.md` — Round 1 + Round 2 + scoring matrix; 87% convergence
- `invariant-probe.md` — 15 invariant findings, 1 HIGH UNADDRESSED (INV-005)
- `base-selection.md` — quantitative + qualitative scoring; A wins by L1 tiebreaker (debate performance)
- `refactor-plan.md` — 7 incorporations from B, 6 rejections with rationale
- `merged-output.md` — unified design feeding this DESIGN.md
- `merge-log.md` — provenance + post-merge validation

---

**End of DESIGN.md.**
