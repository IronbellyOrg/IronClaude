# F-12 Adjudication: Retry only fires on OSError -- post-launch transient failures bypass

**Mode**: B (single-finding, three-persona)
**Inputs**: `.dev/eval-workspaces/prd-cli-audit/findings/F-12-retry-only-on-oserror.md`
**Re-verified against**: `src/superclaude/cli/prd/process.py` (HEAD), `src/superclaude/cli/prd/executor.py` (HEAD)

---

## Re-verification (ground truth)

1. **Retry loop confirmed at `src/superclaude/cli/prd/process.py:208-219`.**
   `for attempt in range(self._max_retries + 1):` wraps `proc = self.start()` inside a `try/except OSError`. The exception type is `OSError` exclusively; no other class is caught.

2. **Retry fires only on `OSError` at launch, not on nonzero exit codes.**
   `executor.py:502-509` calls `proc.start_with_retry()` then immediately calls `proc.wait()` outside any retry harness. The exit code path goes to `_determine_status` (`executor.py:554-585`), which at line 567-568 maps any nonzero exit to `PrdStepStatus.ERROR` with no retry, no transient-vs-permanent classification, no consultation of `_TRANSIENT_EXIT_CODES`.

3. **`_TRANSIENT_PATTERNS` consumers (`grep`):**
   - Single hit: `process.py:216` (`if not _is_transient_failure(1, stderr_text):`).
   - `stderr_text` at line 214 is `str(exc)` where `exc` is the launch-time `OSError`.
   - No other module imports or invokes `_is_transient_failure`, `_TRANSIENT_PATTERNS`, `_NON_TRANSIENT_PATTERNS`, or `_TRANSIENT_EXIT_CODES`.

4. **Does `wait()`/`communicate()` raise `OSError` on transient failures?** No.
   `subprocess.Popen.wait()` returns an exit code. `OSError` from `Popen.__init__` is restricted to fork/exec failures: ENOENT (binary missing), EACCES (permission denied), EAGAIN (fork resource exhaustion), and platform-specific kernel-level conditions. None of these correspond to a Claude CLI rate-limit (HTTP 429), API 503, or transient network failure — those happen *after* the child process is running and emerge as nonzero exit codes with stderr text written to `error_file`.

**Finding's evidence stands.** All four trace claims (process.py:208-219 catches only OSError, `stderr_text` is OSError repr not child stderr, `_TRANSIENT_PATTERNS` is dead, `_retry_delays` unreachable for practical scenarios) are verified by direct read.

---

## Persona 1 — Analyzer (reproducibility)

**Scenario: Claude CLI hits a rate limit mid-pipeline.**

What actually happens on the wire:

- The `claude` binary launches successfully. `subprocess.Popen` returns a `Popen` object with `returncode=None`. No exception. `start_with_retry` returns the process object after `attempt=0`.
- The child issues an API call, receives HTTP 429, prints a message like `Error: rate_limit_exceeded` to stderr (which is captured in `error_file`), and exits with a nonzero code (commonly 1).
- `proc.wait()` (executor.py:504) returns 1.
- `_determine_status(1, output, step_id)` returns `PrdStepStatus.ERROR` (executor.py:567-568). The retry loop's transient pattern table is never consulted; `_retry_delays` is never reached; `time.sleep(5.0)` is never executed.

**Reproducibility verdict: TRIVIAL.** Replace the `claude` binary in PATH with:

```sh
#!/bin/sh
echo "rate_limit_exceeded: 429" >&2
exit 1
```

…and run any PRD step. Expected behavior per the docstring at process.py:195-197 ("Retry up to 2 times with exponential backoff (5s, 15s) on transient failures"): 3 attempts, 20s elapsed, retry warnings logged. Observed behavior: 1 attempt, ~0s elapsed (modulo CLI startup), immediate `PrdStepStatus.ERROR`. The gap between contract and behavior is observable in a single integration test.

**Confidence in reproducibility: 0.97.** The only thing that could make this *not* reproduce is if `Popen` itself somehow raises on rate-limit messages, which it provably doesn't — Popen never reads child stderr to decide whether to raise.

---

## Persona 2 — Refactorer (blast radius)

**What other defensive code is unreachable?**

- **`_TRANSIENT_EXIT_CODES` (process.py:37): 100% dead.** Frozen set defined and never imported, never referenced. The literal values `{1, 2, 137}` appear nowhere else in the codebase's retry path. `_is_transient_failure` accepts an `exit_code` parameter but the function body never compares against `_TRANSIENT_EXIT_CODES` — it only does pattern matching against stderr text. So even if a caller passed a real exit code, the constant would still be dead.

- **`_NON_TRANSIENT_PATTERNS` (process.py:53-60): effectively dead.** Consulted only via `_is_transient_failure`, which is only called with `str(OSError)`. The OSError repr format is `"[Errno N] <strerror>: '<filename>'"`. Strings like "permission denied", "not found", "no such file" *do* occasionally appear in OSError reprs (EACCES → "Permission denied"; ENOENT → "No such file or directory"). So this constant has a thin sliver of liveness — but only for launch-time errors, never for post-launch.

- **`_retry_delays = [5.0, 15.0]` (process.py:146): unreachable for any practical transient failure.** The only way to reach the `time.sleep(delay)` branch is for `Popen` to raise OSError *and* for `str(exc)` to match a `_TRANSIENT_PATTERNS` entry. None of the OSError repr strings produced by Linux kernel errno mapping match "rate limit", "429", "503", "ECONNRESET", etc. EAGAIN ("Resource temporarily unavailable") *could* match the "temporarily unavailable" pattern at process.py:49 — but this represents fork() exhaustion, not Claude API rate limiting, and is genuinely rare.

- **The `attempt` loop variable's exponential structure is honest dead code.** It allocates a list with two delays, indexes into it on each retry, and emits a log message — but in production this code path executes essentially never.

- **`max_retries=2` constructor parameter (process.py:141): a configuration knob with no observable effect** in the rate-limit case the docstring claims to handle (NFR-PRD.12/GAP-011).

**No `_TRANSIENT_PATTERNS` consumers exist outside the retry path.** This was verified by grep — `_is_transient_failure` is the sole consumer, and `_is_transient_failure` has one caller. The defensive vocabulary is concentrated entirely behind a gate that almost never opens.

**Blast radius: NARROW but DEEP.** Narrow because the dead code is confined to one module's retry function; deep because the dead code is the *entire reliability story* for the PRD pipeline. Removing it would not affect any other module. Fixing it (wrapping `wait()` + reading `error_file` into a retry loop) is a localized refactor of `executor.py:502-509` plus a sibling method on `PrdClaudeProcess`.

---

## Persona 3 — Architect (severity calibration)

**Preliminary: HIGH. Should it stay HIGH?**

Arguments for **CRITICAL**:
- The retry is the documented reliability story for the entire PRD subprocess layer (NFR-PRD.12, GAP-011). When the documented reliability mechanism is non-functional for the dominant production failure mode, that's reliability theater, not reliability.
- Rate-limit-related transient failures are not rare edge cases. The Claude CLI is invoked dozens of times per PRD pipeline run; the probability of hitting at least one transient API condition over a long pipeline is non-trivial.
- The user-visible consequence is silent pipeline aborts on transient failures that would self-heal in 5-15 seconds — the worst kind of operational failure mode because operators cannot tell whether the failure was permanent or transient without reading `error_file`.

Arguments for **HIGH** (not CRITICAL):
- The pipeline still *fails closed* — it does not silently produce wrong output. `PrdStepStatus.ERROR` is surfaced. No data corruption.
- Recoverable manually: a human operator can re-run the failed step. No state loss.
- No security impact, no correctness impact, no data integrity impact — purely an operational availability issue.

Arguments for **MEDIUM** (downgrade):
- Speculative. Rate-limit frequency in real PRD usage is uncertified; could be ~zero if usage is light.
- Workaround exists (operator re-run).

**Calibration verdict: HIGH stands.**

The CRITICAL threshold typically requires correctness, security, or data-integrity impact, or an unrecoverable failure mode. F-12 is recoverable manually and fails loudly. But MEDIUM would understate the gap between the contract (the docstring at process.py:195-197 explicitly promises retry on transient failures) and reality (no retry on the dominant transient failure mode). The defect is a documented-feature regression that consumes the operational time of whoever runs the pipeline.

The severity is correctly HIGH because: **(a)** the documented contract is materially false, **(b)** the failure mode is one the system *advertises* it handles, and **(c)** the fix is localized and cheap. A HIGH that is also cheap to fix is the most actionable severity tier.

---

## Convergence

**Verdict: CONFIRMED.**

All three personas independently agree: the retry harness only catches launch-time `OSError`, post-launch transient failures (rate-limit, 429, 503, network reset) flow through `wait()` → nonzero exit → `_determine_status` → `PrdStepStatus.ERROR` with no retry, and the `_TRANSIENT_*` constants plus `_retry_delays` are effectively dead code for the failure modes they claim to handle.

**Convergence score: 0.96.**

The only minor divergence is in severity framing — Architect briefly considered CRITICAL but rejected it on availability-vs-correctness grounds. Reproducibility (0.97), blast-radius mapping (1.0 — clean single-module dead-code identification), and severity calibration (HIGH) all align.

**Final severity: HIGH** (unchanged from preliminary).

**Fix difficulty: LOW-MEDIUM (~1-2 hour fix).**

Required changes:
1. Add a method `PrdClaudeProcess.wait_with_retry()` (or refactor `start_with_retry` into `run_with_retry`) that, after `wait()` returns nonzero, reads `error_file`, applies `_is_transient_failure(exit_code, stderr_text)` with the *real* child stderr and exit code, and re-invokes the launch.
2. Update `executor.py:502-509` to call the wrapping method instead of the separate `start_with_retry()` + `wait()` pair.
3. Honor `_TRANSIENT_EXIT_CODES` in `_is_transient_failure` (currently the `exit_code` parameter is largely unused — only `124` is checked).
4. Add integration tests with stubbed `claude` binary printing rate-limit messages and exiting nonzero; assert retry-and-recover and retry-exhaustion paths.

Risk surface for the fix:
- Re-launching the subprocess invalidates the previous `output_file` / `error_file`. Must decide whether to truncate, rotate (suffix with `.attemptN`), or accumulate. Truncation is simplest and matches existing single-attempt semantics.
- Watchdog/timeout interaction: the parent timeout window (`stall_timeout * 30`, executor.py:499) must accommodate `1 + N` attempts plus backoff delays, or the timeout must reset per attempt. The current code does not multiply by attempt count.
- The `_TRANSIENT_EXIT_CODES = {1, 2, 137}` set is dangerously broad — exit 1 is the generic "something went wrong" code emitted by almost every CLI failure mode (invalid args, prompt-rejected, internal error, etc.). Retrying on exit 1 unconditionally would cause pipeline runs to take 3x as long on permanent failures. The fix must keep the *stderr pattern* match as the primary discriminator and only use exit codes as a secondary signal.

---

## Synthesis

F-12 documents a contract-vs-implementation gap of the cleanest kind: a defensive subsystem (transient-failure retry with exponential backoff) was implemented to handle a stated failure mode (rate-limit, 429/503, network transients per NFR-PRD.12/GAP-011), but the dispatch logic only fires on the wrong exception class (`OSError` at launch) and against the wrong input string (the OSError repr, not the child's stderr). The fix is localized to one module, requires no architectural change, and would replace dead code with working code. The severity is HIGH because the system *advertises* a reliability behavior it does not actually provide; the fix is cheap; and the failure mode is operationally annoying but not corrupting. This is a textbook "high-value, low-cost" defect: high impact relative to fix difficulty.

**Recommended Stage 3 action**: schedule for the next reliability sprint. Bundle with any other retry-harness work in `executor.py` to share the watchdog/timeout reconciliation cost. Do *not* widen `_TRANSIENT_EXIT_CODES` to retry on bare exit 1 without a corroborating stderr pattern.
