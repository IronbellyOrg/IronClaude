# RECONCILED_DESIGN — ClaudeProcess stdin-delivery: actionable plan for IronClaude

| Field | Value |
|-------|-------|
| Status | Supersedes DESIGN.md as the actionable plan; DESIGN.md retained as historical/adversarial record |
| Branch under analysis | `fix/claude-process-stdin-large-prompts` (HEAD `530955b`, off `feat/tdd-spec-merge`) |
| Source-of-truth for code edits | `src/superclaude/cli/pipeline/process.py`, `src/superclaude/cli/cli_portify/process.py` |
| Date | 2026-04-30 |
| Phase-1 inputs | `reconciliation/A-commit-history.md`, `B-code-state.md`, `C-design-claims.md`, `D-test-coverage.md` |
| Phase-2 input | `reconciliation/E-reconciliation-matrix.md` |

---

## §1. Document purpose & scope

This document **supersedes** `/config/workspace/IronClaude/.dev/architectural/claude-process-stdin-patch/DESIGN.md` as the actionable engineering plan for IronClaude. DESIGN.md remains the historical/adversarial record (it was authored against a snapshot of the pipx-installed `superclaude` that predates two load-bearing commits on `feat/tdd-spec-merge`); this RECONCILED_DESIGN.md is what we will land on master via the `feat/tdd-spec-merge` integration branch.

The reconciliation acknowledges that commit `4799719` (Apr 20, 2026, Alireza — "use stdin for the roadmap pipeline instead of passing the prompt as argument", per `A-commit-history.md` §2 row 9) **already implemented the core stdin migration** that DESIGN.md was authored to specify. Likewise, commit `39d5100` (Apr 18, 2026, Alireza — "added template and compression to the roadmap pipeline", per `A-commit-history.md` §2 row 8) added a `tool_write_mode: bool = False` constructor parameter and a `validate_tool_write_output()` method that DESIGN.md does not address. Together those two commits reshape the surface DESIGN.md targeted: the threshold-based dual path is now **always-stdin**, and any patch that re-declares `__init__` or rewrites `start()` per DESIGN.md verbatim would silently regress `tool_write_mode`. This delta lands the gaps that survived (`PromptTooLargeForArgv` cap, BrokenPipeError surfacing, chunked write with EINTR retry, the dead `cmd.index("-p")` Portify branch, missing tests) on top of `4799719` rather than re-deriving the mechanics from scratch.

---

## §2. Working baseline

- **Branch to base off**: `fix/claude-process-stdin-large-prompts` at HEAD `530955b` (off `feat/tdd-spec-merge`). Per `A-commit-history.md` §4, `master` tip equals merge-base `4e0c621` (Mar 24, 2026, "Merge PR #19 v3.7-TurnLedgerWiring") — `master` has not advanced since divergence. Both load-bearing commits (`4799719` stdin, `39d5100` tool_write_mode) live on `feat/tdd-spec-merge` and are absent from `master`. Continuing on this branch preserves them.
- **As-of SHA the delta is built against**: `530955b` (current `fix/claude-process-stdin-large-prompts` HEAD, identical to `feat/tdd-spec-merge` HEAD `5e1349c` plus the design-package import; per `A-commit-history.md` §4 last paragraph). All file-line citations below were captured at this SHA.
- **File inventory (LOC) at branch HEAD** (from `B-code-state.md` summary table):

  | File | LOC | Notes |
  |---|---|---|
  | `/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py` | 244 | Always-stdin delivery; `tool_write_mode` + `validate_tool_write_output()` present; `extra_args` present; hooks unchanged. |
  | `/config/workspace/IronClaude/src/superclaude/cli/cli_portify/process.py` | 245 | `cmd.index("-p")` lookup at line 210 falls into `except ValueError` for ALL invocations → `--add-dir` flags appended at end of `cmd`. |
  | `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py` | 385 | Subclass: hook-injection only, no `build_command` override. Inherits stdin delivery. |
  | `/config/workspace/IronClaude/src/superclaude/cli/cleanup_audit/process.py` | 72 | Subclass: prompt builder only. Inherits stdin delivery. (Pre-existing orthogonal bug: executor calls `is_running()`/`stop()` which do not exist on the class — out of scope.) |
  | `/config/workspace/IronClaude/tests/pipeline/test_process.py` | 234 | Canonical ClaudeProcess unit suite, includes a `TestClaudeProcessStdinDelivery` class with 200 KB and 1 MB cases. |
  | `/config/workspace/IronClaude/tests/pipeline/test_process_hooks.py` | 173 | Lifecycle hook tests. |
  | `/config/workspace/IronClaude/tests/cli_portify/test_process.py` | 517 | PortifyProcess subclass + `run()` + add-dir tests. |

- **Branch recommendation** (from `E-reconciliation-matrix.md` §7): **continue on `fix/claude-process-stdin-large-prompts`**. Rationale: rebasing to master would lose `tool_write_mode` and the `4799719` stdin migration plus its existing `tests/pipeline/test_process.py:156-234` coverage, and would waste the verified P0 probe (DESIGN.md §11 Risk #1, closed 2026-04-30 on `claude 2.1.123`). Eventual PR target is `feat/tdd-spec-merge` (the live integration branch); the upstream PR (D-084) ultimately targets master via the existing integration flow.

---

## §3. Scope of this delta

### §3.1 In-scope (from matrix)

Grouped by subsystem. Each bullet: D-NNN — short description — adversarial provenance — DESIGN.md AC/Risk it traces to.

**`src/superclaude/cli/pipeline/process.py` (primary)**

- D-007 — pre-spawn cap raises `PromptTooLargeForArgv` when prompt > `PROMPT_MAX_BYTES` — provenance U-003 (B), U-001 (A) — AC-7
- D-014 — prompt-size explosion mitigation via 16 MiB env-overridable cap — U-001 (A), U-003 (B) — Risk #4
- D-020 — `PROMPT_MAX_BYTES = int(os.environ.get('SUPERCLAUDE_PROMPT_MAX_BYTES', 16*1024*1024))` constant — U-001 (A only, 95%) — Risk #4
- D-021 — `class PromptTooLargeForArgv(ValueError)` exception — U-003 (B only, 90%, Change #1) — AC-7
- D-025 / D-107 — chunked stdin writer (`_iter_prompt_chunks(64 KiB)`) replacing single-shot encode — C-007 (B 75%, Change #3) — Risk #3 (reframed, sync stall)
- D-026 / D-013 — coordinated stdin-write lifecycle with `terminate()` and `wait()` (writer-thread or chunked-os.write loop with cancellation hook) — INV-002 — Risk #3, AC-5
- D-032 — replace Python `stdin.write(...)` with `os.write` loop, retry on `InterruptedError` (EINTR), terminate cleanly on `BrokenPipeError` with error capture — C-004 (A 85%) — Risk #3
- D-034 — surface stdin write errors via `self._stdin_error` and a `_log.warning(...)` line in `wait()` / `terminate()` — A§3.3 — Risk #5 mitigation
- D-036 — sanity guard: prompts > `PROMPT_MAX_BYTES` raise pre-`Popen` (no orphan child) — U-001/U-003 — Risk #4
- D-040 — cancellation polling preserved; ensure `start()` itself cannot stall indefinitely (chunk loop honors a cancellation flag or daemon writer joins on terminate) — merged-output §5 — Risk #3 (reframed)
- D-052 — invariant: no argv element > `MAX_ARG_STRLEN`; new test pins it — X-001 (A) — AC-3
- D-071 — debug log adds `prompt_bytes=N` field — DESIGN-NEW — operational
- D-099 — open Q: `prompt_bytes=N` accepted as compliance-neutral telemetry; documented in operational notes — DESIGN-NEW
- D-108 — move `stdin.close()` from `try` body to `finally` so EOF is guaranteed even on unexpected `OSError` — INV-002 — Risk #3
- D-001 — 400 KB end-to-end stdin round-trip test (extends current 200 KB) — C-007 (B), C-001 (A) — AC-1
- D-003 — argv byte-size invariant for huge prompts now structural; pin with test — X-001 (A) — AC-3
- D-005 — SIGTERM during stdin write does not hang or leak — INV-002 — AC-5
- D-006 — 200 KB UTF-8 multibyte (emoji) round-trip — Change #4 (B§8.2) — AC-6
- D-027 — empty-prompt behavior documented and tested (currently empty stdin write + EOF; explicit assertion of "no `-p ""`" contract under always-stdin) — X-003 (B 75%, Change #5) — operational

**`src/superclaude/cli/cli_portify/process.py`**

- D-012 — fix dead `cmd.index("-p")` ValueError branch — C-003 (A), X-002 (A) — Risk #2
- D-046 — anchor on `--output-format` (always present) instead of `-p` — C-003, X-002, U-002 — Risk #2
- D-047 — anchor strategy yields stable argv layout for all current and future Portify prompts — C-003, X-002 — Risk #2
- D-048 — 2-line tweak in `build_command()` — C-003 (A 65%) — Risk #2

**Tests** (live in `tests/pipeline/test_process.py` per current layout — see §3.2 for path adaptation)

- D-049 — pin `--output-format <value>` adjacency contract — DESIGN-NEW
- D-052 — `test_argv_total_byte_size_bounded_for_huge_prompt` — X-001 (A) — AC-3
- D-058 — `test_huge_utf8_emoji_prompt_round_trip` — Change #4 — AC-6
- D-059 — `test_prompt_max_bytes_guard` — U-001/U-003 — AC-7
- D-060 — `test_terminate_during_stdin_write_no_hang` (reframed for synchronous-write stall) — INV-002 — AC-5
- D-061 — `test_portify_add_dir_insertion_with_anchor` (replaces "unchanged for small prompt") — C-003 — AC-4 (adapted)
- D-062 — `test_portify_add_dir_insertion_works_for_large_prompt` — C-003, X-002
- D-068 — fixtures (small, empty, boundary-removed-as-N/A, huge 400 KB, emoji 200 KB, oversize-cap-exceed) — C-001, X-003, Change #4
- D-066 / D-089 — test path adapted from DESIGN's `tests/cli/pipeline/test_claude_process_delivery.py` to repo-native `tests/pipeline/test_process_stdin.py` (or extend existing `tests/pipeline/test_process.py`) — DESIGN-NEW

**Observability**

- D-071 — debug log `prompt_via=stdin prompt_bytes=N` in `start()` — DESIGN-NEW

**Rollout / deployment**

- D-009 / D-083 — `make sync-dev && make verify-sync` — project policy — AC-9
- D-010 / D-082 — full `make test` green — project policy — AC-10
- D-067 — CI integration via existing .github actions pipeline (no one-off scripts) — DESIGN-NEW
- D-078 — single PR with this RECONCILED_DESIGN.md attached — DESIGN-NEW + S-005 (B 65%)
- D-080 — apply scoped patch on top of `4799719` rather than re-implementing — partial (DESIGN-NEW)
- D-081 — apply Portify anchor tweak — C-003, U-002 — Risk #2
- D-084 — open upstream PR — DESIGN-NEW
- D-086 — re-run failing roadmap pipeline end-to-end (338 KB prompt) — original bug repro
- D-088 — file-modification scope (now smaller than DESIGN.md projected; `pipeline/process.py` adds ~+40-60 LOC instead of ~+95) — DESIGN-NEW

### §3.2 Out-of-scope (drop or defer)

**DROP — current code is already functionally equivalent or invariant:**

- D-008, D-011, D-101, D-102, D-079 — Risk #1 verified resolved 2026-04-30 (P0 probe, `claude 2.1.123`).
- D-029 — `Popen(stdin=PIPE, stdout=fh, stderr=fh)` already in place at `pipeline/process.py:125-130`.
- D-033 — `stdin.close()` already present at `pipeline/process.py:143` (will be moved to `finally` per D-108).
- D-037 — `self.prompt` invariant already holds at `pipeline/process.py:55`.
- D-038 — `cmd[:3]` debug log shape preserved.
- D-039 — `setpgrp` hasattr-gating already in place at `pipeline/process.py:131-132`.
- D-041 — `build_env()` unchanged; CLAUDECODE strip preserved at `pipeline/process.py:108-109`.
- D-044 — `Popen` + manual stdin manage already chosen over `communicate()`.
- D-051 — `"-p" not in cmd` for all sizes already pinned by `tests/pipeline/test_process.py:54, :176-177`.
- D-056 — 200 KB stdin round-trip already pinned by `tests/pipeline/test_process.py:200-219`.
- D-063 — `--output-format` + value adjacency already pinned by `tests/pipeline/test_process.py:17-37`.

**SUPERSEDED — threshold-based proposals replaced by always-stdin contract:**

- D-002, D-004 (AC-2/AC-4 byte-identical-argv contract — pre-patch shape obsolete since `4799719`).
- D-017, D-018, D-019, D-023, D-024, D-028, D-042, D-109 — threshold + `_use_stdin_for_prompt` + `_prompt_anchor_flag(--output-format)` no longer applicable (always-stdin chosen).
- D-050, D-053, D-054, D-055, D-057 — threshold-boundary tests N/A; "empty → argv with `-p ''`" inverted by always-stdin.
- D-075 — threshold-tweak rollback mechanism N/A; rollback is now `git revert 4799719`.

**DEFER-TO-BEAT-2 (15 items):**

- D-016, D-022, D-035, D-064, D-065, D-072, D-073 — sidecar feature (`prompt_sidecar` kwarg, `.prompt` file, caller policy, opt-in tests, off-by-default test, disk-bloat note). Sidecar is observability-only and adds disk-bloat surface; `4799719` already gives us the security improvement of hiding prompts from `ps` for free. Land sidecar in beat 2 once the cap-and-error-surfacing baseline is stable.
- D-077, D-085, D-087 — vendored monkey-patch in consumer repo (`/config/workspace/Coder` deployment) is a separate operational deliverable downstream of the IronClaude release.
- D-093, D-095, D-096, D-097 — beat-2 architectural items (`pre_prompt_args`, `--input-format=stream-json`, sidecar rotation, `PromptSource` Protocol).
- D-098 — `force_prompt_via` per-caller override; superseded under always-stdin.

---

## §4. Concrete patches

All patches apply to `src/superclaude/`. Run `make sync-dev` after editing. Line numbers cite `B-code-state.md` against branch HEAD `530955b`.

### Patch P-001: Remove dead `cmd.index("-p")` branch in PortifyProcess; anchor on `--output-format`

- **D-NNN refs**: D-012, D-046, D-047, D-048
- **AC refs**: AC-4 (adapted — Portify anchor regression coverage)
- **Provenance**: C-003 (A), X-002 (A), U-002 (A only, 70%) — Portify anchor strategy
- **File**: `/config/workspace/IronClaude/src/superclaude/cli/cli_portify/process.py`
- **Anchor lines (current)**: 185-215 (per `B-code-state.md` §2 cli_portify subsection)

**Before** (cli_portify/process.py:203-215):
```python
        # Inject --add-dir args after the fixed base flags
        add_dir_args: list[str] = []
        for d in add_dirs:
            add_dir_args.extend(["--add-dir", str(d)])

        # Insert before -p
        try:
            p_idx = cmd.index("-p")
            cmd[p_idx:p_idx] = add_dir_args
        except ValueError:
            cmd.extend(add_dir_args)

        return cmd
```

**After**:
```python
        # Inject --add-dir args after the fixed base flags
        add_dir_args: list[str] = []
        for d in add_dirs:
            add_dir_args.extend(["--add-dir", str(d)])

        # Anchor: insert add-dir flags after `--output-format <value>` (always
        # present in the base build_command). The prompt is delivered via
        # stdin (no `-p` in argv since 4799719), so the legacy `cmd.index("-p")`
        # lookup is dead. `--output-format` is the stable anchor: it is emitted
        # by ClaudeProcess.build_command() unconditionally and its value is the
        # next element, so insert at index+2.
        try:
            anchor_idx = cmd.index("--output-format")
            insert_at = anchor_idx + 2  # skip flag + value
            cmd[insert_at:insert_at] = add_dir_args
        except ValueError:  # pragma: no cover — defensive: base contract violated
            cmd.extend(add_dir_args)

        return cmd
```

**Why**: The current `cmd.index("-p")` raises `ValueError` for every invocation because the base `build_command()` (`pipeline/process.py:79-95`) no longer emits `-p` (per `B-code-state.md` Q1, Surprise #5). The flags still reach claude, but argv layout drifts toward the tail and the comment is misleading. `--output-format` is present unconditionally in the base argv, making it a stable anchor for both small and large prompts. Resolves DESIGN.md Risk #2.

**Acceptance**:
- `cmd.index("--output-format")` succeeds for every Portify invocation.
- `--add-dir <path>` flags land immediately after `--output-format <value>`, before `--max-turns`/extra_args.
- No code path raises uncaught `ValueError` from `build_command()`.

---

### Patch P-002: Add `PROMPT_MAX_BYTES` and `PromptTooLargeForArgv` exception

- **D-NNN refs**: D-007, D-014, D-020, D-021, D-036
- **AC refs**: AC-7
- **Provenance**: U-001 (A only, 95%) — `PROMPT_MAX_BYTES`; U-003 (B only, 90%, Change #1) — typed exception
- **File**: `/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py`
- **Anchor lines (current)**: top of module after imports (line 21 area, before `class ClaudeProcess`)

**Before** (pipeline/process.py:14-23):
```python
from __future__ import annotations

import logging
import os
import signal
import subprocess
from pathlib import Path
from typing import Callable, Optional

_log = logging.getLogger("superclaude.pipeline.process")
```

**After**:
```python
from __future__ import annotations

import logging
import os
import signal
import subprocess
from pathlib import Path
from typing import Callable, Optional

_log = logging.getLogger("superclaude.pipeline.process")


# Default 16 MiB; env-overridable for operators with exotic workflows.
# This is a sanity guard, not a kernel limit — Linux MAX_ARG_STRLEN no
# longer applies because the prompt is delivered via stdin (since 4799719).
PROMPT_MAX_BYTES: int = int(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", 16 * 1024 * 1024))


class PromptTooLargeForArgv(ValueError):
    """Raised pre-spawn when the encoded prompt exceeds PROMPT_MAX_BYTES.

    Subclass of ValueError for backward-compat with callers catching
    ValueError. Name kept from the original DESIGN for traceability,
    though under always-stdin the failure mode is "child memory" not
    "argv overflow".
    """
```

**Why**: Without an upper bound, a pathological caller (e.g., a roadmap step that embeds a multi-GB artifact) can OOM the child claude process before the parent has any feedback. A typed exception lets callers distinguish "user supplied too-large input" from arbitrary `OSError`/`subprocess` failures. Default 16 MiB comfortably accommodates the 338 KB observed bug case while bounding worst-case memory. Resolves DESIGN.md Risk #4.

**Acceptance**:
- Importing `PromptTooLargeForArgv` from `superclaude.cli.pipeline.process` succeeds.
- `PROMPT_MAX_BYTES` reads `SUPERCLAUDE_PROMPT_MAX_BYTES` env var on import (test by patching env before import).
- `PromptTooLargeForArgv` is a subclass of `ValueError` (callers using `except ValueError` keep working).

---

### Patch P-003: Pre-spawn size guard in `start()`

- **D-NNN refs**: D-007, D-036
- **AC refs**: AC-7
- **Provenance**: U-001 (A) + U-003 (B) — pre-spawn cap
- **File**: `/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py`
- **Anchor lines (current)**: 114-134 (start() prelude through Popen)

**Before** (pipeline/process.py:114-117):
```python
    def start(self) -> subprocess.Popen:
        """Launch the claude process."""
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        if self.tool_write_mode:
```

**After**:
```python
    def start(self) -> subprocess.Popen:
        """Launch the claude process."""
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        # Sanity guard before any handle/process is created.
        # Encode once here so the result is reused below for stdin write.
        prompt_bytes = self.prompt.encode("utf-8") if self.prompt else b""
        if len(prompt_bytes) > PROMPT_MAX_BYTES:
            raise PromptTooLargeForArgv(
                f"prompt is {len(prompt_bytes)} bytes; PROMPT_MAX_BYTES={PROMPT_MAX_BYTES}"
            )
        self._prompt_bytes = prompt_bytes  # consumed in stdin write below

        if self.tool_write_mode:
```

**Why**: The guard runs before `output_file` is opened and before `Popen` forks the child, so over-cap inputs cannot leak file handles or orphan a child. The encoded buffer is captured for reuse so we don't re-encode in the chunked write loop (P-004). Resolves DESIGN.md Risk #4.

**Acceptance**:
- A 17 MiB prompt raises `PromptTooLargeForArgv` before any file is opened.
- The child process is never spawned on over-cap inputs.
- A 400 KB prompt passes the guard without modification.

---

### Patch P-004: Replace single-shot stdin write with chunked, EINTR-safe loop; capture errors; close in `finally`

- **D-NNN refs**: D-013, D-025, D-026, D-032, D-034, D-040, D-107, D-108
- **AC refs**: AC-1, AC-5, AC-6
- **Provenance**: C-007 (B 75%, Change #3) — chunked encode; C-004 (A 85%) — `os.write` over `BufferedWriter`; INV-002 — finally + lifecycle
- **File**: `/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py`
- **Anchor lines (current)**: 136-146 (the synchronous `stdin.write(...)` block) plus add helper

**Before** (pipeline/process.py:136-146):
```python
        # Deliver the prompt via stdin to bypass the Linux MAX_ARG_STRLEN
        # (128 KB per-argv-entry) kernel ceiling. Deadlock-safe: stdout/stderr
        # are real file handles, not pipes, so the parent never reads from the
        # child and a blocked stdin write cannot deadlock.
        try:
            if self._process.stdin is not None:
                self._process.stdin.write(self.prompt.encode("utf-8"))
                self._process.stdin.close()
        except BrokenPipeError:
            # Child exited before reading stdin; wait() will surface the exit code.
            pass
```

**After**:
```python
        # Deliver the prompt via stdin to bypass the Linux MAX_ARG_STRLEN
        # (128 KB per-argv-entry) kernel ceiling. Deadlock-safe: stdout/stderr
        # are real file handles, not pipes, so the parent never reads from the
        # child and a blocked stdin write cannot deadlock.
        #
        # Chunked write protects against (a) full kernel pipe buffer (typically
        # 64 KiB on Linux) by yielding control between chunks, (b) EINTR from
        # signal delivery, (c) silent BrokenPipe masking. Errors are captured
        # in self._stdin_error and surfaced in wait()/terminate() via _log.
        self._stdin_error: Optional[BaseException] = None
        self._write_prompt_to_stdin(self._prompt_bytes)

        if self._on_spawn is not None:
            self._on_spawn(self._process.pid)

        _log.debug(
            "spawn pid=%d cmd=%s prompt_via=stdin prompt_bytes=%d",
            self._process.pid,
            str(self.build_command()[:3]),
            len(self._prompt_bytes),
        )

        return self._process

    _STDIN_CHUNK_SIZE = 64 * 1024  # match typical Linux pipe-buffer size

    def _write_prompt_to_stdin(self, payload: bytes) -> None:
        """Write payload to child stdin in chunks; close stdin in finally.

        Uses os.write on the underlying FD so EINTR can be retried (Python's
        BufferedWriter does not surface InterruptedError reliably on partial
        writes). Closes stdin in finally so claude --print receives EOF even
        on unexpected exception (BrokenPipe, OSError, KeyboardInterrupt).
        """
        if self._process is None or self._process.stdin is None:
            return
        fd = self._process.stdin.fileno()
        try:
            view = memoryview(payload)
            offset = 0
            while offset < len(view):
                chunk = view[offset:offset + self._STDIN_CHUNK_SIZE]
                while True:
                    try:
                        n = os.write(fd, chunk)
                        break
                    except InterruptedError:
                        # EINTR from signal delivery — retry the same chunk.
                        continue
                if n <= 0:
                    # Defensive — os.write should not return 0 on a pipe.
                    break
                offset += n
        except BrokenPipeError as exc:
            # Child exited before reading stdin; surface in wait()/terminate().
            self._stdin_error = exc
        except OSError as exc:
            self._stdin_error = exc
        finally:
            try:
                self._process.stdin.close()
            except Exception:  # pragma: no cover — defensive
                pass
```

And in `wait()` (lines 159-171) and `terminate()` (lines 173-214), after the existing logic, add a one-line surfacing of `_stdin_error`:

```python
        # in wait(), after computing rc and BEFORE returning:
        if self._stdin_error is not None:
            _log.warning("stdin_error pid=%s err=%r", self._process.pid, self._stdin_error)

        # in terminate(), after the SIGKILL block, BEFORE _close_handles():
        if getattr(self, "_stdin_error", None) is not None:
            _log.warning("stdin_error pid=%s err=%r", self._process.pid, self._stdin_error)
```

**Why**: The current single-shot `self._process.stdin.write(...)` (B Q3, B §1 lines 140-146) blocks the parent thread until claude drains the pipe — for a 338 KB prompt with a slow-starting child, the parent's `start()` itself stalls before the executor's cancel-poll loop runs (B Q3, B §1 lines 137-139 docstring is incomplete on this point). Chunking via `os.write` against the FD (a) keeps each syscall to the kernel pipe-buffer size so we yield to other threads/signals between writes, (b) handles EINTR explicitly (Python's `BufferedWriter` swallows partial-write/EINTR cases inconsistently), (c) puts the close in `finally` so EOF is guaranteed even on unexpected exceptions, and (d) captures errors instead of `pass` so post-mortem diagnostics work. Resolves DESIGN.md Risk #3 (reframed for synchronous-write stall) and addresses the "BrokenPipeError swallowed silently" gap from `E-reconciliation-matrix.md` §5.4.

Note on architectural choice: The original DESIGN.md §6.2 specified a daemon writer thread (D-030). With always-stdin and `tool_write_mode` already in tree, the simpler chunked-os.write loop on the parent thread achieves the same anti-stall properties (each `os.write` is bounded to ~64 KiB) without adding thread-lifecycle complexity (`_join_stdin_writer`, daemon threads, error sync). For prompts of practical size (≤ a few MB), the chunked loop completes in milliseconds; for pathological sizes the cap from P-002/P-003 prevents arrival at this code path. If future production telemetry shows stalls, the writer-thread upgrade (DESIGN.md D-030) is a localized follow-up.

**Acceptance**:
- A 400 KB ASCII prompt round-trips byte-identical via stdin (extends current 200 KB test).
- A 200 KB UTF-8 emoji prompt round-trips byte-identical.
- `BrokenPipeError` (child exits early) populates `self._stdin_error` and emits a `WARNING` log line, but does not raise from `start()`.
- A SIGTERM delivered to the parent during the write loop does not hang `start()` indefinitely (the chunk loop exits after the current chunk because the child closes its end).
- `stdin.close()` runs in the `finally`, even if `os.write` raises an unexpected `OSError`.

---

### Patch P-005: Pin `tool_write_mode` behavior with regression test (orthogonal but necessary)

- **D-NNN refs**: orthogonal to DESIGN.md (Surprise #1 in `B-code-state.md` and `E-reconciliation-matrix.md` §4.1). DESIGN.md does not address `tool_write_mode`; D-test-coverage.md §4 Q7 reports zero tests.
- **AC refs**: AC-10 (full test suite green) — adding test, not patching code, but documenting the contract here ensures the delta does not silently regress `tool_write_mode` and gives reviewers a clear baseline.
- **Provenance**: DESIGN-NEW (gap surfaced in reconciliation)
- **File**: tests only — see §5 (T-007). No source patch.
- **Why**: `tool_write_mode` was added in commit `39d5100` and is wired by the roadmap executor (`cli/roadmap/executor.py:1117, :1927, :1945, :2008`). Any reshape of `start()` (as P-004 does) must preserve the dual stdout-handle path at `pipeline/process.py:118-122`. A regression test pins the contract.

**Acceptance**: see T-007 in §5.

---

## §5. Test additions

Test-file path: **`/config/workspace/IronClaude/tests/pipeline/test_process_stdin.py`** (new file, sibling of existing `tests/pipeline/test_process.py`). Rationale: DESIGN.md proposed `tests/cli/pipeline/test_claude_process_delivery.py`, but the live test layout is `tests/pipeline/` (per `D-test-coverage.md` §1 and `B-code-state.md` confirmation that 110 test files in `tests/...` follow a flat-by-subsystem pattern). A new sibling file keeps the existing `TestClaudeProcessStdinDelivery` class intact while collecting reconciliation-specific cases in one place. Mocking strategy follows the existing pattern (`tests/pipeline/test_process.py:181-219`): patch `ClaudeProcess.build_command` to return a Python stand-in (`sys.executable -c "..."`) that echoes stdin to stdout, exercising the full real subprocess transport.

Run via: `uv run pytest tests/pipeline/test_process_stdin.py -v`.

| Test ID | §9.1 source | File | Function name | Asserts | Mocking strategy | Pass/fail criteria |
|---------|-------------|------|---------------|---------|-------------------|---------------------|
| **T-001** | DESIGN.md §9.1 #3 (D-052) | `tests/pipeline/test_process_stdin.py` | `test_argv_total_byte_size_bounded_for_huge_prompt` | For a 400 KB prompt, `max(len(arg.encode('utf-8')) for arg in proc.build_command()) < 128 * 1024` | No subprocess; just instantiate `ClaudeProcess(prompt=...)` and call `build_command()`. | Pass: max argv element size ≤ 4 KB (only fixed flags + model + extra_args). Fail: any element > 128 KB. |
| **T-002** | DESIGN.md §9.1 #7 (D-001) — extend 200 KB to 400 KB | same | `test_huge_prompt_400kb_round_trip_via_stdin` | A 400 KB ASCII prompt arrives byte-identical at the Python stand-in's stdout (which echoes stdin). | Real subprocess via `sys.executable -c "import sys; sys.stdout.buffer.write(sys.stdin.buffer.read())"`. Patch `build_command()` to return that argv. | Pass: `output_file.read_bytes() == prompt.encode('utf-8')`. Fail: truncation, EOF before completion, or `OSError`. |
| **T-003** | DESIGN.md §9.1 #9 (D-058) | same | `test_huge_utf8_emoji_prompt_round_trip` | A 200 KB prompt of `"🦀"` (4 bytes/codepoint) round-trips byte-identical. Tests UTF-8 multibyte path through the chunked encoder (chunk boundaries can't split codepoints because we encode once at start). | Same Python stand-in pattern as T-002. | Pass: byte-identical round-trip. Fail: mojibake, truncation, or `UnicodeError`. |
| **T-004** | DESIGN.md §9.1 #10 (D-059) | same | `test_prompt_max_bytes_guard` | Calling `start()` with a prompt ≥ `PROMPT_MAX_BYTES + 1` raises `PromptTooLargeForArgv`. The child process is never spawned (`self._process is None`). `self.output_file` is never created. | No subprocess; `pytest.raises(PromptTooLargeForArgv)`. Set `PROMPT_MAX_BYTES` to a small value via `monkeypatch.setattr` for test isolation. | Pass: raises pre-spawn; no file/process side effects. Fail: silent acceptance, raises wrong exception type, or fork happens before raise. |
| **T-005** | DESIGN.md §9.1 #11 (D-005, D-060) — reframed | same | `test_terminate_during_stdin_write_no_hang` | Spawning a Python stand-in that sleeps for 30 seconds before reading stdin, then calling `terminate()` from the test thread, completes within `terminate()`'s 10s SIGTERM + 5s SIGKILL window without hanging. `self._stdin_error` is populated (BrokenPipe from killed child). | Real subprocess; stand-in is `python -c "import time; time.sleep(30); sys.stdin.read()"`. `threading.Timer` to call `terminate()` 0.5s after `start()` returns. Use 100 KB prompt to fill pipe buffer. | Pass: total wall time < 16s; no orphan child (verify via `proc.poll() is not None`); `_stdin_error is not None`. Fail: hangs > 16s, leaves orphan, or raises uncaught from `start()`. |
| **T-006** | DESIGN.md §9.1 #6 (D-027) — reframed for always-stdin | same | `test_empty_prompt_uses_stdin_with_zero_bytes` | An empty `prompt=""` invocation: `build_command()` does NOT contain `-p`; `start()` writes 0 bytes and closes stdin (claude receives immediate EOF). No exception. | Real subprocess with stand-in that echoes stdin; output_file is empty. | Pass: `output_file.read_bytes() == b""`; no exception; no `-p` in cmd. Fail: any exception, presence of `-p`, or non-empty output. |
| **T-007** | orthogonal coverage gap (Surprise #4.1) | same | `test_tool_write_mode_redirects_stdout_to_log_sidecar` | When `tool_write_mode=True`, `start()` opens `output_file.with_suffix(".log")` for stdout (not `output_file`). The base output_file is NOT created by stdout. `validate_tool_write_output()` returns False if `output_file` is empty/missing post-exit, True if non-empty. | Real subprocess; stand-in writes to stdout but NOT to `output_file`. | Pass: `.log` file exists with stdout content; `output_file` does not exist; `validate_tool_write_output()` returns False. Then create `output_file` with content and verify True. Fail: stdout lands in `output_file`. |
| **T-008** | DESIGN.md §9.1 #14 (D-049) | same | `test_output_format_flag_and_value_are_adjacent_for_portify_anchor` | For `PortifyProcess`, `cmd.index("--output-format") + 1` equals the index of the format value (`"text"`), and `cmd[index+2]` is the first `--add-dir` flag. | No subprocess; instantiate `PortifyProcess(...)` and call `build_command()`. Use `tmp_path` for work_dir/workflow_path. | Pass: anchor lookup succeeds; `--add-dir` lands directly after `--output-format <value>`. Fail: any anchor drift, `ValueError`, or wrong adjacency. |
| **T-009** | DESIGN.md §9.1 #13 (D-062) | same | `test_portify_add_dir_works_for_large_prompt` | A `PortifyProcess` invocation with a 200 KB prompt: `cmd` contains `--add-dir` for both `work_dir` and `workflow_path` at the anchor position; argv has no `-p`; stdin transport delivers full prompt. | Real subprocess via stand-in; build_command introspection. | Pass: both `--add-dir` flags present at anchor; round-trip byte-identical; no argv element > 128 KB. Fail: missing `--add-dir`, anchor drift, or transport corruption. |
| **T-010** | new from P-001 (Risk #2 regression) | same | `test_portify_anchor_resilient_to_repeated_calls` | Calling `build_command()` on the same `PortifyProcess` instance twice produces equal results (no mutation of base `cmd` between calls). | No subprocess. | Pass: `proc.build_command() == proc.build_command()`. Fail: argv accretes flags or anchor drifts. |
| **T-011** | new from P-004 (BrokenPipe surfacing) | same | `test_broken_pipe_surfaces_via_stdin_error_log` | When the child exits before reading stdin (1 MB prompt + stand-in that immediately exits 0), `start()` returns without raising; `_stdin_error` is populated; `wait()` emits a `WARNING` log line containing "stdin_error". | Real subprocess via `sys.executable -c "import sys; sys.exit(0)"` stand-in. Use `caplog` fixture. | Pass: `start()` does not raise; `caplog.records` contains a WARNING with "stdin_error"; `wait()` returns child's actual exit code (0). Fail: raises from `start()`, no log, or wrong log level. |

**Total new tests: 11.** Together with the 4 existing tests in `tests/pipeline/test_process.py` already covering DESIGN §9.1 (per `D-test-coverage.md` §5: #2, #7, #14, #12-partial), the §9.1 matrix is fully addressed under the always-stdin contract. The 5 SUPERSEDED §9.1 cases (#1, #4, #5, #6-as-argv, #8) are not reintroduced; the existing `tests/pipeline/test_process.py:54, 176-177` assertions that pin the `"-p" not in cmd` contract are preserved (no regression).

---

## §6. Risks resolved by current state

(From `E-reconciliation-matrix.md` §6, expanded.)

- **DESIGN.md Risk #1** — *"pinned `claude` does not read stdin in `--print` when positional arg is omitted"*. Verified resolved. Cited evidence: `DESIGN.md §11 row 1` records P0 probe success on 2026-04-30 against `claude 2.1.123 (Claude Code)` with three probes (baseline-positional, stdin-only, ~200 KB stdin). Code state: `pipeline/process.py:125-130` (`stdin=subprocess.PIPE`) and `:140-146` (write+close) implements the path; `tests/pipeline/test_process.py:200-219` exercises a 200 KB round-trip through a real subprocess. Commit `4799719` shipped on this verified assumption.

- **Original `argv too long` (E2BIG) failure mode at 128 KiB** — pre-`4799719` code passed prompts via `-p <prompt>` argv pair (commit `6548f17`'s argv shape; `A-commit-history.md` §3 row 1). Linux `MAX_ARG_STRLEN = 128 KiB` per-argument ceiling caused `Popen` to fail with `OSError: [Errno 7] Argument list too long`. `4799719` removed `-p` from argv entirely (`pipeline/process.py:79-95` — no `-p` element); the failure mode is mechanically eliminated. Verified by `tests/pipeline/test_process.py:200-219` (200 KB round-trip, `D-test-coverage.md` §2.1).

- **`ps` / `/proc/<pid>/cmdline` prompt visibility** — `4799719` makes prompts invisible to `ps`. DESIGN.md D-074 / merged-output §6 case #11 calls this an intentional security improvement. Resolved as a side-effect at `pipeline/process.py:79-95`.

---

## §7. Risks newly introduced or unmitigated

(From `E-reconciliation-matrix.md` §5, expanded with severity and patch routing.)

| # | Risk | File:line | Severity | Mitigation |
|---|------|-----------|----------|------------|
| R-1 | **`cli_portify` `cmd.index("-p")` dead branch** — `cmd.index("-p")` raises `ValueError` for every Portify invocation; `--add-dir` flags accrete at end of argv instead of at the documented splice point. The flags reach claude (which accepts them positionally), but the argv layout no longer matches the design contract; future flag insertion could shift their relative position unpredictably. | `cli_portify/process.py:208-213` | medium | **P-001** — anchor on `--output-format` (always present); add T-008, T-009, T-010 to pin the new contract. Maps to DESIGN.md Risk #2. |
| R-2 | **Synchronous stdin write blocking on full pipe buffer** — `pipeline/process.py:142` performs a single synchronous `stdin.write()` of the entire encoded prompt on the parent thread. Linux pipe buffer is ~64 KiB; for a 338 KB prompt with slow-starting claude, parent's `start()` itself stalls before the executor's cancel-poll loop runs. The deadlock-safety docstring at `pipeline/process.py:137-139` addresses 4-way pipe deadlock (genuinely impossible) but does not address parent-thread stall. | `pipeline/process.py:140-146` | high | **P-004** — chunked `os.write` loop bounded to `_STDIN_CHUNK_SIZE = 64 KiB`; each chunk yields control between syscalls; `terminate()` running on another thread can complete because the child's eventual close releases the loop. Add T-005 to pin SIGTERM-no-hang. Maps to DESIGN.md Risk #3 (reframed). |
| R-3 | **`BrokenPipeError` swallowed silently** — `pipeline/process.py:144-146` catches `BrokenPipeError` with bare `pass` (no logging, no error capture). When claude exits early (parse error, OOM, signal), the parent only sees the eventual exit code and must reconstruct cause from the error log. | `pipeline/process.py:140-146` | medium | **P-004** — capture in `self._stdin_error`; surface via `_log.warning(...)` from `wait()` and `terminate()`. Add T-011 to pin the surfacing. |
| R-4 | **Empty-prompt behavior** — current `prompt=""` becomes `stdin.write(b"")` + close; claude receives EOF with zero bytes. Behavior depends on claude's own handling. No defensive guard. DESIGN.md row 1 of §6.1 expected `-p ""` + DEVNULL stdin — that path is gone. | `pipeline/process.py:140-143` | low | **DEFER-TO-BEAT-2 — accepted risk**: the 2026-04-30 probe (`claude 2.1.123`) tolerates empty stdin in practice; a defensive raise would surprise existing callers (none of which depend on empty prompts). T-006 documents the current contract; if claude's behavior changes, we'll add a guard then. |
| R-5 | **Full-buffer encode without chunking** — `pipeline/process.py:142` encodes the entire prompt in one shot. For multi-MB prompts (audit-pipeline composition, future workflows), peak heap doubles (Python str + bytes coexist). | `pipeline/process.py:142` | medium | **P-004 + P-002/P-003** — encoding still happens once per `start()` (P-003 captures `prompt_bytes` for reuse, so the chunked write loop slices a pre-existing buffer rather than re-encoding). Heap-doubling is bounded by `PROMPT_MAX_BYTES = 16 MiB`. True streaming-encode (DESIGN.md D-025) is deferred to beat 2 if telemetry shows it matters. |
| R-6 | **Missing `PromptTooLargeForArgv`** — DESIGN.md AC-7 is an explicit acceptance criterion. Under always-stdin the failure mode shifts from "argv overflow" to "child memory exhaustion", but the typed exception still gives callers a clean signal vs an arbitrary `OSError`/MemoryError. | `pipeline/process.py` (module-level) | medium | **P-002 + P-003 + T-004** — define exception, define `PROMPT_MAX_BYTES` (16 MiB env-overridable), guard pre-`Popen`, pin with test. Class name preserved for traceability even though the underlying mechanism changed. Maps to DESIGN.md Risk #4. |

---

## §8. Recommended commit sequence

All commits are mergeable independently after their predecessor in this list lands; no branch fan-out is needed. Apply in order on `fix/claude-process-stdin-large-prompts`. After landing, target PR is `feat/tdd-spec-merge`.

1. **`fix(cli_portify): anchor --add-dir on --output-format instead of dead -p lookup`** — P-001 — T-008, T-009, T-010 — yes (independent). Smallest, lowest-risk change; gives us a regression baseline before touching the base class.

2. **`feat(pipeline): add PROMPT_MAX_BYTES and PromptTooLargeForArgv exception`** — P-002 — (no tests in this commit; T-004 lands with P-003 since the guard is what's testable) — yes (independent; pure additive at module scope).

3. **`feat(pipeline): pre-spawn size guard + capture encoded prompt for reuse`** — P-003 — T-004 — yes (depends on commit #2 for the symbol; standalone otherwise). Adds the guard + persists `_prompt_bytes` on `self` for the chunked-write commit to consume.

4. **`fix(pipeline): chunked stdin write with EINTR retry, error capture, finally-close`** — P-004 — T-002, T-003, T-005, T-006, T-011 — yes (depends on #3 for `self._prompt_bytes`).

5. **`test(pipeline): pin tool_write_mode contract`** — P-005 (test-only) — T-007 — yes (independent; can land any time after #4 to prevent regression of `tool_write_mode` from any future `start()` reshape).

6. **`test(pipeline): argv byte-size invariant for huge prompts`** — — T-001 — yes (independent of all above; pure invariant test against `build_command()`).

7. **`docs: replace DESIGN.md with RECONCILED_DESIGN.md as actionable plan`** — no patches — no tests — yes (independent; updates `.dev/architectural/claude-process-stdin-patch/` with the reconciliation outputs and links DESIGN.md as historical).

After commit #6, run `make sync-dev && make verify-sync && make test` (per project policy CLAUDE.md).

---

## §9. Deployment plan

### §9.1 Landing in IronClaude

**Branch flow**: `fix/claude-process-stdin-large-prompts` → PR into `feat/tdd-spec-merge` (the live integration branch) → eventual merge into `master` via the existing integration flow. Per `A-commit-history.md` §4, `master` tip equals merge-base `4e0c621` (Mar 24, 2026) and has not advanced; `feat/tdd-spec-merge` is where the load-bearing `4799719` and `39d5100` commits live, so the patch must land there first.

**Sync step** (after each source edit): run `make sync-dev` to copy `src/superclaude/` to `.claude/`, then `make verify-sync` before commit. Both are documented in `/config/workspace/IronClaude/CLAUDE.md` ("Component sync").

**Tests to run pre-merge**:
- `uv run pytest tests/pipeline/ -v` — full pipeline subsystem (existing 234-line suite + 11 new tests).
- `uv run pytest tests/cli_portify/test_process.py -v` — Portify regression (existing 517-line suite must remain green; T-008/T-009/T-010 extend it).
- `uv run pytest tests/roadmap/test_file_passing.py tests/roadmap/test_inline_fallback.py -v` — caller-level large-prompt assertions (per `D-test-coverage.md` §2.5–2.6, these mock `ClaudeProcess` at executor level and should remain green).
- `make test` — full suite (gates AC-10).

**Adversarial sign-off requirements (STRICT mode)**: not invoked for this delta since DESIGN.md was already approved at 87% convergence by `/sc:adversarial` (per DESIGN.md frontmatter). RECONCILED_DESIGN.md is a reconciliation, not a re-design. If reviewers request adversarial re-validation, run `/sc:adversarial` against `RECONCILED_DESIGN.md` vs `DESIGN.md` → expect a near-100% convergence on the patches because they are a strict subset of DESIGN.md intent.

### §9.2 Rebuilding pipx env so /config/workspace/Coder works

After landing on `feat/tdd-spec-merge` (and eventually `master`):

1. **Build wheel**: `uv build` in `/config/workspace/IronClaude` (verify exact command from `pyproject.toml` build system before running; CLAUDE.md notes `hatchling` PEP-517 build, so `uv build` produces a wheel at `dist/superclaude-<version>-py3-none-any.whl`).
2. **Reinstall locally**: `pipx install --force /config/workspace/IronClaude` (from local checkout) OR `pipx reinstall superclaude` if the local repo is what pipx picked up. For a published-package release, `pipx upgrade superclaude` after a PyPI publish (separate step — out of scope for this delta).
3. **Verify in `/config/workspace/Coder`**: re-run the originally failing `superclaude roadmap run …` command with the 338 KB composed prompt (181 KB PRD + 157 KB TDD per `DESIGN.md §1`). Acceptance: process exits 0; no `OSError: [Errno 7] Argument list too long`; output artifact present; `.log` sidecar contains stdout when `tool_write_mode=True`.

If a PyPI release is needed (vs editable pipx), that is a separate downstream step (cut a tag → CI publishes → operators run `pipx upgrade superclaude`). The vendored monkey-patch alternative (DESIGN.md D-077, D-085, D-087) is intentionally **deferred to beat 2** here — once the IronClaude release is available, the monkey-patch is redundant.

---

## §10. Acceptance for this delta

A reviewer marks this delta done when **all** of the following are checked:

- [ ] All P-NNN patches landed on `fix/claude-process-stdin-large-prompts` (P-001 through P-005).
- [ ] All T-NNN tests pass: `uv run pytest tests/pipeline/test_process_stdin.py -v` shows T-001 through T-011 green.
- [ ] Existing tests still pass: per `D-test-coverage.md`, the existing assertions at `tests/pipeline/test_process.py:54, 176-177, 198` (always-stdin contract) and `tests/cli_portify/test_process.py:392-418` (PortifyProcess backward-compat) remain green.
- [ ] DESIGN.md AC-1..AC-10 each map to a verdict in `E-reconciliation-matrix.md` §3:
  - AC-1 → ADAPT (D-001) — addressed by P-004 + T-002.
  - AC-2 → SUPERSEDED (D-002) — pre-patch shape obsolete since `4799719`.
  - AC-3 → ADAPT (D-003) — addressed by T-001.
  - AC-4 → SUPERSEDED (D-004) — Portify anchor reshape addressed by P-001 + T-008/T-009.
  - AC-5 → ADAPT (D-005) — addressed by P-004 + T-005.
  - AC-6 → IMPLEMENT-FRESH (D-006) — addressed by T-003.
  - AC-7 → IMPLEMENT-FRESH (D-007) — addressed by P-002 + P-003 + T-004.
  - AC-8 → DROP (D-008) — closed; P0 probe verified 2026-04-30.
  - AC-9 → IMPLEMENT-FRESH (D-009) — addressed by §9.1 (`make sync-dev && make verify-sync`).
  - AC-10 → IMPLEMENT-FRESH (D-010) — addressed by §9.1 (`make test`).
- [ ] DESIGN.md §11 risks 1-6 each map to a verdict in `E-reconciliation-matrix.md` §3:
  - Risk #1 → DROP — P0 probe verified.
  - Risk #2 → ADAPT — P-001 + T-008/T-009/T-010.
  - Risk #3 → ADAPT (reframed) — P-004 + T-005 + T-011.
  - Risk #4 → IMPLEMENT-FRESH — P-002 + P-003 + T-004.
  - Risk #5 → IMPLEMENT-FRESH — P-004 (`_stdin_error` surfacing) + version-pin documented in §9.1; sidecar deferred.
  - Risk #6 → DEFER-TO-BEAT-2 — accepted; sidecar feature absent, so disk-bloat risk is moot.
- [ ] `make sync-dev` and `make verify-sync` run clean.
- [ ] `/config/workspace/Coder` roadmap-run with the 338 KB original-bug prompt succeeds end-to-end after pipx rebuild (D-086).

---

## §11. Appendix: provenance map

Compact table — one row per patch, mapping back to D-NNN, adversarial provenance, and AC/Risk.

| Patch | D-NNN | Adversarial provenance | AC / Risk reference |
|-------|-------|-------------------------|-----------------------|
| P-001 | D-012, D-046, D-047, D-048 | C-003 (A 65%), X-002 (A 60%), U-002 (A only, 70%) | DESIGN.md AC-4 (adapted), Risk #2 |
| P-002 | D-014, D-020, D-021 | U-001 (A only, 95%), U-003 (B only, 90%, Change #1) | DESIGN.md AC-7, Risk #4 |
| P-003 | D-007, D-036 | U-001 (A) + U-003 (B) — pre-spawn cap | DESIGN.md AC-7, Risk #4 |
| P-004 | D-013, D-025, D-026, D-032, D-034, D-040, D-107, D-108 | C-007 (B 75%, Change #3), C-004 (A 85%), INV-002 (HIGH ADDRESSED) | DESIGN.md AC-1, AC-5, AC-6, Risk #3 (reframed), Risk #5 (partial — error surfacing) |
| P-005 | (orthogonal — `tool_write_mode` regression net) | DESIGN-NEW (Surprise from `B-code-state.md` Surprise #4 / `E-reconciliation-matrix.md` §4.1) | DESIGN.md AC-10 (full suite green) |

| Test | D-NNN | Adversarial provenance | AC / Risk reference |
|------|-------|-------------------------|-----------------------|
| T-001 | D-052 | X-001 (A) | DESIGN.md AC-3 |
| T-002 | D-001, D-056 (extended) | C-007 (B), C-001 (A) | DESIGN.md AC-1 |
| T-003 | D-006, D-058 | Change #4 (B§8.2) | DESIGN.md AC-6 |
| T-004 | D-007, D-059 | U-001 (A) + U-003 (B) | DESIGN.md AC-7 |
| T-005 | D-005, D-060 (reframed) | INV-002 | DESIGN.md AC-5, Risk #3 |
| T-006 | D-027 (reframed for always-stdin) | X-003 (B 75%, Change #5) | operational documentation |
| T-007 | (orthogonal — `tool_write_mode` regression net) | DESIGN-NEW | DESIGN.md AC-10 |
| T-008 | D-049, D-063 | DESIGN-NEW (test contract for U-002) | DESIGN.md AC-4 (adapted) |
| T-009 | D-062 | C-003, X-002 | DESIGN.md AC-4, Risk #2 |
| T-010 | new from P-001 | DESIGN-NEW (regression net) | DESIGN.md Risk #2 |
| T-011 | D-034 | A§3.3 — error surfacing | DESIGN.md Risk #5 (partial) |

**End of RECONCILED_DESIGN.md.**
