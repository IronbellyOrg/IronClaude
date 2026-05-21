# Adjudication — F-25: Subprocess lifecycle gaps

**Source finding**: `.dev/eval-workspaces/prd-cli-audit/findings/F-25-subprocess-lifecycle-gaps.md`
**Stage 2 preliminary**: MEDIUM
**Mode**: B (analyzer / refactorer / architect → converge)
**Date**: 2026-05-20

---

## Re-verification (read-only)

### Exit-code collapse — confirmed
`src/superclaude/cli/prd/executor.py:562-568`:

```python
# Timeout
if exit_code == 124:
    return PrdStepStatus.TIMEOUT
# Crash
if exit_code != 0:
    return PrdStepStatus.ERROR
```

Only `124` is distinguished. `130` (SIGINT/Ctrl-C), `137` (SIGKILL/OOM), `143` (SIGTERM), negative `-N` (signal-killed on POSIX `Popen.returncode`), `1`, `2` all fold into the single `ERROR` bucket. `execution-log.jsonl` therefore cannot tell "user interrupted" from "OOM killer" from "claude CLI bug" — all three look identical to retry logic and to the operator.

**Contradiction with retry logic**: `src/superclaude/cli/prd/process.py:37` declares `_TRANSIENT_EXIT_CODES = frozenset({1, 2, 137})` (calling SIGKILL "retryable"), but the code path that consults it is `start_with_retry()` at launch only — once `proc.wait()` returns `137`, `_determine_status` short-circuits to `ERROR` at executor.py:567 and the "transient" classification never runs. Dead policy.

### PrdSignalHandler does not relay — confirmed
`src/superclaude/cli/prd/executor.py:188-203`:

```python
def install(self) -> None:
    self._original_sigint = signal.getsignal(signal.SIGINT)
    self._original_sigterm = signal.getsignal(signal.SIGTERM)
    signal.signal(signal.SIGINT, self._handle)
    signal.signal(signal.SIGTERM, self._handle)
...
def _handle(self, signum, frame) -> None:
    self.shutdown_requested = True
```

`_handle` only flips a flag. No call to `proc.terminate()`, no `os.killpg`, no relay. The flag is polled **only between steps** (`executor.py:372, 397, 632, 643, 653, 660, 667, 677, 692, 700, 787, 824`) — never during the blocking `exit_code = proc.wait()` at `executor.py:504`.

### What happens at Ctrl-C mid-step — derived
`src/superclaude/cli/pipeline/process.py:131-132`:

```python
if hasattr(os, "setpgrp"):
    popen_kwargs["preexec_fn"] = os.setpgrp
```

The child is placed in its **own process group**. On a TTY, Ctrl-C sends SIGINT only to the foreground process group (the parent's group). The child does **not** receive the SIGINT from the terminal driver. The parent's handler sets `shutdown_requested=True`, then immediately returns into the next instruction of `proc.wait()` (line 504), which is blocked on `_process.wait(timeout=self.timeout_seconds)` with `timeout_seconds = stall_timeout * 30`. Default `stall_timeout` is 5 minutes → child can run **up to 2.5 hours** after the user hits Ctrl-C before parent notices the flag, and only then between steps. The child genuinely continues writing artifacts during that window.

`SIGTERM` from a supervisor (e.g. systemd, container runtime, `kill <pid>`) has the same outcome: parent flips flag, parent stays blocked in wait, child runs on in its own pgrp.

### Why `terminate()` does not save us
`pipeline/process.py:173-205` is well-written — it uses `os.killpg(pgid, SIGTERM)` then `SIGKILL` after 10 s. It correctly kills the process group. **But it is only called from the timeout path** (`process.py:163-164`). The signal handler at `executor.py:202` does not call it. Operator interrupts never reach this code.

---

## Persona 1 — Analyzer (reproducibility)

**Question**: User hits Ctrl-C mid-pipeline. Observed behavior?

**Trace**:
1. `t=0` user presses Ctrl-C.
2. TTY driver sends `SIGINT` to foreground process group = parent's pgrp. Child (in its own pgrp via `setpgrp`) does not receive it.
3. Parent's `PrdSignalHandler._handle` runs (executor.py:202): sets `shutdown_requested=True`, returns.
4. Parent thread resumes inside `subprocess.Popen.wait(timeout=stall_timeout*30)` at `pipeline/process.py:162`. Waiting on the child PID. No syscall checks the flag.
5. Child continues normally. Streams NDJSON to `output_file` (`pipeline/process.py:122`), invokes tools, writes artifacts, etc. No knowledge that the user wants out.
6. **Case A**: child finishes naturally in time `T`. Parent reads exit code, sees `shutdown_requested` between steps, calls `_handle_shutdown`. **Latency: T (anywhere from seconds to 2.5h)**.
7. **Case B**: user gets impatient, presses Ctrl-C again. Python's default SIGINT behaviour after a custom handler is installed: handler runs again, flag re-set. Still no propagation. After enough presses some users will `kill -9` the parent — orphaning the child entirely (it survives until its own timeout or completion).
8. **Case C**: user `kill -TERM <parent_pid>` from another shell. Same as 3-6.

**Observed**:
- Pipeline does **not** halt promptly.
- Subprocess **continues** writing artifacts post-Ctrl-C (the artifacts may even be committed to `task_dir` as the basis for a downstream step if Case A resolves before the flag check).
- Final status reported in `execution-log.jsonl` is `ERROR` (because exit code from a non-zero finish is mapped to ERROR at executor.py:567), **not** "user-interrupted". If Case A resolved with success, status is `PASS` and the cancellation is silently discarded.
- If the user force-kills the parent: orphaned child writes artifacts that no one is tracking.

**Reproducibility**: 100%. The control flow is deterministic on POSIX systems with `os.setpgrp`. The only variability is *when* the parent eventually notices.

**Severity contribution**: HIGH for operational predictability. The product fails the basic "Ctrl-C halts the work" contract that every CLI user assumes. Worse, it fails *silently*: no log entry says "received SIGINT, awaiting current step", so the operator believes the program is frozen.

---

## Persona 2 — Refactorer (blast radius)

**Question**: Is this an isolated PRD-executor bug, or a codebase-wide pattern?

**Same flag-only pattern, no relay**:
| File:line | Class | Relay? |
|---|---|---|
| `src/superclaude/cli/prd/executor.py:188-203` | `PrdSignalHandler` | NO |
| `src/superclaude/cli/sprint/process.py:220-249` | `SprintSignalHandler` (`_handle` at 248-249) | NO |
| `src/superclaude/cli/cleanup_audit/process.py:49-72` | `SignalHandler` (`_handle` at 71-72) | NO |
| `src/superclaude/cli/cli_portify/executor.py:507-524` | inline `_handle` | NO (just sets `_interrupted`) |

Four independent pipelines, four copies of the same defect. Each one spawns long-running `claude -p` subprocesses with `preexec_fn=os.setpgrp` (all route through `ClaudeProcess` in `pipeline/process.py:114-157`), so all four exhibit the same "child outlives Ctrl-C" behavior.

**Same exit-code collapse**:
- `prd/executor.py:563-568`: only `124` recognised.
- `sprint` and `cleanup_audit` executors follow the same shape (they use `proc.wait()` from `pipeline/process.py:159-171` and map non-zero → failure).
- `cli_portify/executor.py` is slightly better (it preserves the raw exit code in `_execution_log.signal_received` at line 517 when *its own* process is signalled) but still inherits the no-relay defect for children.

**One bright spot**: `src/superclaude/cli/eval/signal_handler.py:56-127` (`CancellationToken` + `SignalHandlerInstaller`) is the only correctly-designed signal subsystem in the repo — thread-safe, records `signum`, supports cooperative cancellation, defines an explicit `EXIT_INTERRUPTED=3` constant. Nothing in `prd/`, `sprint/`, `cleanup_audit/`, or `cli_portify/` uses it. **This is a refactoring target**: the eval module already has the abstraction; the other four pipelines reinvented an inferior version.

**Other lifecycle defects observed**:
- `pipeline/process.py:144-146`: silent swallow of `BrokenPipeError` on stdin write. Comment says "Child exited before reading stdin; wait() will surface the exit code." True, but the exit code path collapses to ERROR — so a child that died before reading its prompt is indistinguishable from a child that ran the prompt and crashed.
- `pipeline/process.py:167`: `rc = self._process.returncode if self._process.returncode is not None else -1`. The `-1` fallback fires when the process is still running (impossible after wait) or — more relevantly — when `returncode` is a negative number representing a signal (`-SIGTERM = -15`). Actually `returncode` for a signal-killed child is `-N` (negative signal number), which is not None, so this branch is fine; **but** that `-N` then flows into `_determine_status` which sees `exit_code != 0` and returns ERROR, losing the signal identity.
- `prd/process.py:37` `_TRANSIENT_EXIT_CODES` is dead policy at the wait-path level (described above).

**Blast radius**: codebase-wide. Four pipelines × two defects (no relay + collapse) = 8 instances of the same operational gap. Fix is shared (extract / adopt `eval/signal_handler.py` pattern, add code → status mapping for `130/137/143/-N`).

---

## Persona 3 — Architect (severity calibration)

**Stage 2 preliminary**: MEDIUM.

**Arguments to keep at MEDIUM**:
- No data corruption. Artifacts written post-Ctrl-C are syntactically valid; they're just unwanted work.
- No security impact. Process groups are isolated; orphaned children cannot escalate.
- No correctness regression on the happy path. Pipelines that complete normally are unaffected.
- Workaround exists (`pkill -9 -f claude`), so a determined operator can recover.

**Arguments to escalate to HIGH**:
- **Violates a universal CLI contract**: every UNIX operator expects Ctrl-C to stop work within seconds. This pipeline can take up to 2.5h to honour it on default settings, and may *silently succeed* in the meantime, producing artifacts the user thought they cancelled. That's a trust-breaking surprise.
- **Compounds across the codebase**: four pipelines, all with the same defect, all spawning multi-hour `claude -p` subprocesses. This is not "an edge case in one tool" — it is the framework's standard subprocess hygiene.
- **Diagnostic invisibility blocks operations**: when a step fails, the engineer reading `execution-log.jsonl` sees `status: ERROR, exit_code: 137` (if exit_code is even logged — `PrdStepResult` does carry it per executor.py:548-552, good) but has no semantic label. OOM, SIGKILL by container, and "claude CLI exited 1 because of an internal error" all look the same. Time-to-diagnosis on production failures goes up.
- **Dead retry policy**: `_TRANSIENT_EXIT_CODES` at `prd/process.py:37` is the kind of false-positive control that *looks* like it's protecting the pipeline but is structurally bypassed. That is worse than not having it — auditors and contributors will believe SIGKILL is being retried when it is not.
- **Resume state is built on a lie**: the executor writes resume state assuming the cancellation was honoured. If the child actually completed work between flag-set and flag-check, the resume state is for a step that already ran (and possibly produced gate-passing output), wasting reruns and confusing downstream comparison.

**Counterweight**: severity is bounded by *who notices*. PRD pipeline is operator-driven (someone is at the terminal). The "Ctrl-C didn't work" failure mode is loud and immediate to that operator. They will hit Ctrl-C harder and eventually `kill -9`. So the failure is recoverable, just embarrassing and operationally wasteful.

**Calibration**: MEDIUM is defensible but understated. Recommend **MEDIUM-HIGH**: the bug is reproducible 100% of the time, affects four independent pipelines, breaks a basic CLI contract, has a dead policy that masks the issue, and the fix is well-scoped (the eval module already shows how). It is not HIGH because there is no data loss or security impact and a determined operator can recover with `kill -9`.

---

## Convergence

**Verdict**: VALID — both sub-claims (exit-code collapse, no-relay) reproduce deterministically by reading the code, and they compound exactly as the finding describes. The finding additionally understates the scope: the same defect is present in four pipelines, and there is a dead retry-policy contradiction (`_TRANSIENT_EXIT_CODES`) that the original finding flagged but did not fully connect to the wait-path bypass.

**Convergence score**: 0.92.
- Analyzer, refactorer, architect all independently arrive at the same control-flow trace.
- Mild disagreement on final severity (analyzer leans HIGH on operational predictability; architect lands MEDIUM-HIGH on calibrated impact; refactorer is severity-neutral but emphasises blast radius). All three accept the same fix shape.
- No persona disputes the evidence.

**Final severity**: **MEDIUM-HIGH** (Stage 2 preliminary MEDIUM raised one notch on the strength of the codebase-wide blast radius and the dead `_TRANSIENT_EXIT_CODES` policy).

**Fix difficulty**: **MEDIUM (~1-2 day spike)**.
1. Map `_determine_status` to recognise `130 → INTERRUPTED`, `137 → KILLED` (OOM/external), `143 → TERMINATED`, negative `-N → SIGNAL_KILLED(name)`. Add `PrdStepStatus.INTERRUPTED` / `.KILLED` enum members. Pure addition, no behaviour change for existing callers. ~2-4 h.
2. In `PrdSignalHandler._handle`, relay to the live subprocess: stash a weak ref or callback to the currently-executing `ClaudeProcess`, and call `proc.terminate()` from the handler. `terminate()` already does the right thing (killpg SIGTERM → wait 10s → killpg SIGKILL). ~4-6 h plus tests.
3. Use one shared signal subsystem. The cleanest path is to adopt `src/superclaude/cli/eval/signal_handler.py:SignalHandlerInstaller` + `CancellationToken` in `prd`, `sprint`, `cleanup_audit`, `cli_portify`. Avoids the four-way reinvention. ~1 day refactor.
4. Remove or fix `_TRANSIENT_EXIT_CODES` — either wire it into the wait-path retry decision or delete it as dead code. ~1 h.

Test coverage requires a pty harness that signals the parent and asserts the child receives SIGTERM within (say) 2 s; the `eval/` module presumably already has a similar fixture.

**Synthesis**:
F-25 is **valid and slightly under-scoped**. The original finding correctly identifies the two defects (exit-code collapse, no signal relay) but treats them as a single PRD-executor concern with confidence 0.80. Re-verification shows:

1. The defects are **architectural**, not localised — four pipelines (`prd`, `sprint`, `cleanup_audit`, `cli_portify`) ship the same flag-only signal handler and route their subprocesses through the same `ClaudeProcess` that uses `setpgrp` to isolate the child from terminal SIGINT. The "child outlives Ctrl-C" behaviour is the framework default.
2. There is a **bright-spot abstraction** already in the codebase (`eval/signal_handler.py`) that solves this correctly with `CancellationToken` and a proper `SignalHandlerInstaller`. The fix is "adopt that", not "design something new".
3. The **dead `_TRANSIENT_EXIT_CODES` policy** at `prd/process.py:37` deserves explicit mention in the finding — it is not just confusion-causing, it actively misleads code review into thinking SIGKILL is being handled.
4. Observed behaviour at Ctrl-C is concretely: parent flag flips, parent stays blocked in `proc.wait()` for up to `stall_timeout * 30` seconds (2.5h default), child writes artifacts the user thought they cancelled. The pipeline may **silently succeed** during this window, discarding the cancellation and writing log status `PASS`.
5. Final-status visibility loss is operational (not data-integrity), but the four-way duplication and the contract violation push calibrated severity to **MEDIUM-HIGH**.

Confidence in adjudication: **0.92** (one Read pass across all four pipelines + the eval module; behaviour derived from Python `subprocess` + POSIX TTY semantics, not from a runtime repro).
