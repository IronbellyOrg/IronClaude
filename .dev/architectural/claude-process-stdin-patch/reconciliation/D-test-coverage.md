# Agent D — Test-Coverage Scout

**Workspace:** `/config/workspace/IronClaude`
**Branch:** `fix/claude-process-stdin-large-prompts`
**Reference:** `/config/workspace/IronClaude/.dev/architectural/claude-process-stdin-patch/DESIGN.md` §9.1
**Mode:** READ-ONLY (no tests run, no files modified outside this report)

---

## 1. Discovery summary

`find tests -name 'test_*.py'`: ~110 test files total.

Grep coverage:

| Pattern | Hits |
|---|---|
| `ClaudeProcess` | 24 files |
| `PortifyProcess` | 4 files |
| `subprocess.PIPE` | 0 (in tests) |
| `tool_write_mode` | 0 |
| `cmd.index` | 3 files (none reference `-p`) |
| `"-p"` | 2 files: `tests/sprint/test_tmux.py` (tmux flag, unrelated) and `tests/pipeline/test_process.py` (asserts `"-p" not in cmd`) |
| `stdin` (in test bodies) | 7 files |
| `large prompt`/`E2BIG` | 2 files |

The current code has **already moved to always-stdin**. `src/superclaude/cli/pipeline/process.py:73-95` builds a command without `-p`; `:140-146` writes the encoded prompt to `stdin` then closes it (no threshold, no daemon thread, no sidecar, no `PromptTooLargeForArgv`). `cli_portify/process.py:209-213` still contains `cmd.index("-p")` but its `try` raises `ValueError` and the `except` branch (`cmd.extend(add_dir_args)`) handles every call.

Most-relevant test files (in priority order):

1. `/config/workspace/IronClaude/tests/pipeline/test_process.py` — 234 LOC, the canonical ClaudeProcess unit suite, includes a `TestClaudeProcessStdinDelivery` class.
2. `/config/workspace/IronClaude/tests/pipeline/test_process_hooks.py` — 173 LOC, lifecycle hooks.
3. `/config/workspace/IronClaude/tests/cli_portify/test_process.py` — 517 LOC, PortifyProcess subclass + run() + add-dir.
4. `/config/workspace/IronClaude/tests/sprint/test_process.py` — 555 LOC, sprint subclass + signal/env.
5. `/config/workspace/IronClaude/tests/roadmap/test_file_passing.py` — 191 LOC, large-prompt scenarios via mocked ClaudeProcess.
6. `/config/workspace/IronClaude/tests/roadmap/test_inline_fallback.py` — embeds oversized inputs inline; verifies stdin transport.
7. `/config/workspace/IronClaude/tests/sprint/test_regression_gaps.py` — 815 LOC; only `cmd.index("--model")` (unrelated).
8. `/config/workspace/IronClaude/tests/sprint/test_tmux.py` — `"-p"` is **tmux split-window's percentage flag**, not claude's.

---

## 2. Per-test-file inventory

### 2.1 `/config/workspace/IronClaude/tests/pipeline/test_process.py` (234 LOC)

Tests in file (function names):
- `TestClaudeProcessCommand`
  - `test_default_output_format_stream_json` — pins `--output-format stream-json`
  - `test_text_output_format` — text format
  - `test_required_flags` — asserts `claude`, `--print`, `--verbose`, `--no-session-persistence`, `--tools default`, `--dangerously-skip-permissions` are present **and `assert "-p" not in cmd` (line 54)** plus `assert "hello" not in cmd` (line 55) — pins prompt-NOT-in-argv contract
  - `test_with_model`, `test_without_model`
  - `test_extra_args`, `test_max_turns_in_command`, `test_tools_default_in_command`
- `TestClaudeProcessEnv` — `test_removes_claudecode_env`
- `TestClaudeProcessStreamJsonCompat` — `test_stream_json_matches_sprint_flags`
- `TestClaudeProcessStdinDelivery` (lines 156-234)
  - `test_build_command_excludes_prompt` — `"-p" not in cmd`, `prompt not in cmd` (line 176-177)
  - `test_start_writes_prompt_to_stdin` — uses Python stand-in that echoes stdin → output_file; verifies byte-identical round-trip (line 181-198)
  - `test_stdin_handles_large_payload` — **200 KB prompt**, verifies no OSError + byte-identical round-trip (line 200-219)
  - `test_broken_pipe_tolerated` — 1 MB prompt, child exits before reading; parent must not raise (line 221-234)

Mocking: uses `unittest.mock.patch.object(ClaudeProcess, "build_command", return_value=...)` to swap in a Python stand-in for `claude` (`sys.executable -c '...'`). Real subprocesses are spawned; no `subprocess.Popen` mocking in stdin-delivery class.

**Would DESIGN.md verbatim patch break any test here?** YES. DESIGN.md proposes a **threshold-based** dual path: argv for <96 KiB. The patch reintroduces `-p` for small prompts. Under DESIGN.md:
- `test_required_flags` line 54 (`assert "-p" not in cmd`) — **WOULD FAIL** for the small-prompt argv path.
- `test_required_flags` line 55 (`assert "hello" not in cmd`) — **WOULD FAIL** because DESIGN.md keeps `-p hello` on argv.
- `TestClaudeProcessStdinDelivery::test_build_command_excludes_prompt` lines 176-177 — **WOULD FAIL** for the small ("multi-line body") prompt because that's < 96 KiB and goes argv path under DESIGN.md.
- `test_start_writes_prompt_to_stdin` (line 198 expects output equals prompt) — under DESIGN.md the small prompt rides argv, the Python stand-in's `sys.stdin.read()` returns "" → assertion fails.

DESIGN.md §9.1 coverage signals from this file:
- Already covered: huge-prompt-via-stdin round trip (200 KB); broken-pipe; argv excludes prompt under always-stdin.
- The class is structured around the **always-stdin** contract. DESIGN.md would invert ~half of it.

### 2.2 `/config/workspace/IronClaude/tests/pipeline/test_process_hooks.py` (173 LOC)

Tests: `test_on_spawn_called_with_pid`, `test_on_spawn_none_no_error`, `test_on_signal_called_before_sigterm`, `test_on_signal_none_no_error`, `test_on_exit_called_on_normal_wait`, `test_on_exit_called_with_nonzero_returncode`, `test_on_exit_called_in_terminate`, `test_defaults_are_none`.

Mocks `subprocess.Popen` and patches `_close_handles`. Uses `MagicMock(spec=subprocess.Popen)`; `fake_popen.stdin = MagicMock()` lines 47, 60 — confirms callers expect stdin handle to exist on Popen.

**Break under DESIGN.md verbatim?** No assertions on `-p`/`cmd.index`/argv shape — these would survive the patch. The MagicMock `stdin` works for both modes.

DESIGN.md §9.1 coverage: indirect — **does not exercise** SIGTERM mid-stdin-write directly (the writer-thread is fully mocked). Doesn't satisfy `test_terminate_during_stdin_write_no_hang`.

### 2.3 `/config/workspace/IronClaude/tests/cli_portify/test_process.py` (517 LOC)

Tests: 30+ tests across `TestPortifyProcessInheritance`, `TestDualAddDir`, `TestPromptConstruction`, `TestProcessResult`, `TestPortifyProcessRun`, `TestAdditionalDirs`, `TestConsolidateDirs`, `TestBackwardCompatibilitySC11`, `TestClaudeBinaryDetection`.

Key tests for DESIGN.md collision:
- `TestDualAddDir::test_both_dirs_in_command` (line 49-65) — counts `--add-dir` occurrences and asserts their positions; does **not** assert anything about `-p` placement — neutral.
- `TestBackwardCompatibilitySC11::test_additional_dirs_none_matches_v224_baseline` (line 392-418) — compares `cmd_v224 == cmd_new`. Both built under current code (no `-p`); test compares pre/post and is symmetric — survives.

Mocking: `@patch.object(ClaudeProcess, "start")`, `@patch.object(ClaudeProcess, "wait", return_value=...)` for `run()` tests (lines 167-234). `@patch("...shutil.which")` for binary detection.

**Break under DESIGN.md verbatim?** No — none of the assertions hard-pin `-p` presence in PortifyProcess. The `cmd.index("--add-dir")` checks (lines 61-65) survive both delivery modes. Add-dir injection is robust against re-introduction of `-p` because DESIGN.md's §6.3 patch uses `--output-format` as the new anchor.

DESIGN.md §9.1 coverage:
- `test_portify_add_dir_insertion_unchanged_for_small_prompt` — partially covered by `test_additional_dirs_none_matches_v224_baseline` and `TestDualAddDir::test_both_dirs_in_command`. The byte-identical-to-v2.24 contract is checked, but for the **current** baseline (no `-p`); not a true small-prompt-with-`-p` test.
- `test_portify_add_dir_insertion_works_for_large_prompt` — **NOT COVERED**.

### 2.4 `/config/workspace/IronClaude/tests/sprint/test_process.py` (555 LOC)

Sprint-specific `ClaudeProcess` (subclass in `superclaude.cli.sprint.process`). Tests `build_command` / `build_env` / signal handler / context injection / git diff / progressive summary.

Key:
- `test_build_command_required_flags` (line 40-52) — does **not** assert presence of `-p`; only `claude`, `--print`, `--no-session-persistence`, `--output-format`, `stream-json`, `--max-turns`, `50`. Survives DESIGN.md.
- `TestClaudeProcessPlatformFallback::test_start_without_setpgrp_fallback` (line 186-212) — patches `subprocess.Popen`; asserts `"preexec_fn" not in kwargs`. Neutral re: prompt delivery.
- No `-p`/`cmd.index`/stdin-write assertions.

DESIGN.md §9.1 coverage: Tangential — sprint subclass passes through to base; not a target for §9.1.

### 2.5 `/config/workspace/IronClaude/tests/roadmap/test_file_passing.py` (191 LOC, top file for large-prompt scenarios)

Tests:
- `TestPromptContainsEmbeddedContent::test_prompt_contains_embedded_content` (line 46-77)
- `TestPathsWithSpaces::test_paths_with_spaces` (line 82-108)
- `TestLargePromptSoftWarning::test_over_threshold_logs_warning_and_embeds_inline` (line 118-149) — **embeds `_LARGE_PROMPT_WARN_BYTES + 1024` bytes**, asserts content is in `prompt` kwarg passed to `ClaudeProcess`, asserts `extra_args == []`, asserts a warning log.
- `TestLargePromptSoftWarning::test_under_threshold_no_warning` (line 151-183) — **150 KB** input (above old 128 KB ceiling), asserts no warning + content present.

Mocks `superclaude.cli.roadmap.executor.ClaudeProcess` (entire class). Captures kwargs in helper `_capture_and_return` (line 186-190). Does NOT exercise `start()` / `Popen` / stdin write — these are full mocks.

**Break under DESIGN.md verbatim?** No — assertions are on the `prompt` kwarg passed to ClaudeProcess, not on argv shape. DESIGN.md guarantees `self.prompt` always equals constructor input (Compatibility Contract row 2). Survives.

DESIGN.md §9.1 coverage:
- `test_huge_prompt_delivered_via_stdin` — **PARTIAL**: confirms the prompt is forwarded to ClaudeProcess for large content, but does not verify *the actual stdin transport*. That coverage lives in `test_process.py::test_stdin_handles_large_payload`.

### 2.6 `/config/workspace/IronClaude/tests/roadmap/test_inline_fallback.py` (~210 LOC)

Tests:
- `TestInlineEmbedFallbackWhenFileBroken::test_inline_embed_fallback_when_file_broken` (parametrized over validate_executor / tasklist_executor / remediate_executor)
- `test_no_file_flag_in_any_execution_path` (parametrized)

Module-level docstring (line 4): "stdin (ClaudeProcess.start). --file flags must never appear in extra_args."

Mocks each executor's `ClaudeProcess`. Captures kwargs. Asserts `"--file" not in captured["extra_args"]` and oversized content present in `prompt`.

**Break under DESIGN.md?** No — same shape as test_file_passing.py. Survives.

DESIGN.md §9.1 coverage: indirect — verifies callers send full prompt to ClaudeProcess; does not test ClaudeProcess transport itself.

### 2.7 Other files referencing ClaudeProcess (informational, do not pin DESIGN.md-relevant assertions)

- `tests/sprint/test_regression_gaps.py` (815 LOC) — `cmd.index("--model")` only. No `-p`.
- `tests/sprint/test_preflight.py` — references `_TrackingClaudeProcess` for python-mode assertion; unrelated.
- `tests/sprint/test_phase8_halt_fix.py` — `ClaudeProcess.__new__(ClaudeProcess)` for in-place attribute setup; no argv assertions.
- `tests/sprint/test_integration_lifecycle.py` — full mock; no argv pinning.
- `tests/sprint/test_execute_sprint_integration.py` — full mock at executor level.
- `tests/v3.3/test_turnledger_lifecycle.py` — turn ledger tests; ClaudeProcess simulated as a debit/reconcile op.
- `tests/v3.3/test_wiring_points_e2e.py` — `_FakeClaudeProcess` swap; no argv pinning.
- `tests/roadmap/test_pipeline_integration.py` — uses a controlled mock runner, not ClaudeProcess directly.
- `tests/roadmap/test_remediate_executor.py` — patches `ClaudeProcess` symbol; doesn't introspect argv.
- `tests/roadmap/test_anti_instinct_integration.py` — doc-string mention only.
- `tests/roadmap/test_compression_integration.py` — `fake` ClaudeProcess swap, writes output_text to file; no argv pinning.
- `tests/roadmap/test_semantic_layer.py` — `FakeClaudeProcess` test double; no argv pinning.
- `tests/cli_portify/test_cli.py` — `TestProcessIntegration` builds two PortifyProcess instances and compares `build_command()` symmetrically (line 313-360). Survives.
- `tests/cli_portify/test_mock_harness.py` — fixture inventory, not ClaudeProcess transport.
- `tests/cli_portify/fixtures/mock_harness.py` — `patch.object(PortifyProcess, "run", ...)` for run-level mocks.
- `tests/cli/prd/test_executor.py`, `tests/cli/prd/test_e2e.py`, `tests/cli/prd/test_integration.py` — patches `PrdClaudeProcess`; no argv pinning.
- `tests/sprint/test_summarizer.py` — separate haiku invocation tests; line 297-298 asserts `call.kwargs["stdin"] == subprocess.DEVNULL` for the **summarizer** subprocess (not ClaudeProcess) — unrelated.

### 2.8 Files that mention `"-p"` but are NOT about ClaudeProcess

- `/config/workspace/IronClaude/tests/sprint/test_tmux.py` lines 112, 117 — these are tmux's `split-window -p 50` (percentage) assertions. **Not affected by ClaudeProcess transport changes.**

---

## 3. DESIGN.md §9.1 ↔ existing tests cross-reference

(§9.1 lists 16 test cases — table has 16 rows.)

| # | DESIGN.md test idea | Existing test (file:test_name) or "NEW NEEDED" | Notes |
|---|---|---|---|
| 1 | `test_build_command_keeps_p_flag_for_small_prompt` | NEW NEEDED | **Current code has no `-p` for any size**. Existing `test_required_flags` (`tests/pipeline/test_process.py:39-55`) asserts the **opposite** (`"-p" not in cmd`). |
| 2 | `test_build_command_omits_p_flag_for_large_prompt` | `tests/pipeline/test_process.py::TestClaudeProcessCommand::test_required_flags` (line 39-55) and `TestClaudeProcessStdinDelivery::test_build_command_excludes_prompt` (line 167-179) | Already covered for *all* sizes; DESIGN.md narrows it to large only. |
| 3 | `test_argv_total_byte_size_bounded_for_huge_prompt` | NEW NEEDED | No existing test asserts a numeric byte ceiling per argv element. `test_stdin_handles_large_payload` (200 KB) passes implicitly because prompt isn't on argv at all. |
| 4 | `test_threshold_boundary_under` (95 KiB → argv) | NEW NEEDED | Threshold concept does not exist in current code. |
| 5 | `test_threshold_boundary_over` (97 KiB → stdin) | NEW NEEDED | Same. |
| 6 | `test_empty_prompt_uses_argv_with_empty_p_value` | NEW NEEDED — and would CONFLICT with `tests/pipeline/test_process.py::test_required_flags:54` (`"-p" not in cmd`) when prompt="hello"; that small-prompt assertion would need to become "empty → argv with `-p`, non-empty <96 KiB → argv with `-p`". |
| 7 | `test_huge_prompt_delivered_via_stdin` | `tests/pipeline/test_process.py::TestClaudeProcessStdinDelivery::test_stdin_handles_large_payload` (line 200-219, 200 KB round-trip) | Covered. Also indirectly by `tests/roadmap/test_file_passing.py::test_under_threshold_no_warning` (150 KB) at the executor mock level. |
| 8 | `test_small_prompt_still_uses_argv` | NEW NEEDED | Inverse of current always-stdin behavior; no existing test pins this. |
| 9 | `test_huge_utf8_emoji_prompt_round_trip` (200 KB multibyte) | NEW NEEDED | `test_stdin_handles_large_payload` uses ASCII `"x"`. UTF-8 multibyte path not exercised. |
| 10 | `test_prompt_max_bytes_guard` (raise PromptTooLargeForArgv) | NEW NEEDED | `PromptTooLargeForArgv` does not exist in current code. |
| 11 | `test_terminate_during_stdin_write_no_hang` | NEW NEEDED | `tests/pipeline/test_process.py::test_broken_pipe_tolerated` covers child-exits-first; SIGTERM mid-write w/ daemon-thread join is not exercised. |
| 12 | `test_portify_add_dir_insertion_unchanged_for_small_prompt` | `tests/cli_portify/test_process.py::TestBackwardCompatibilitySC11::test_additional_dirs_none_matches_v224_baseline` (line 392-418) and `TestDualAddDir::test_both_dirs_in_command` (line 49-65) | Partial — both compare layouts symmetrically against current baseline (no `-p`). DESIGN.md needs an *anchor*-vs-`-p` byte-equivalence test; not present. |
| 13 | `test_portify_add_dir_insertion_works_for_large_prompt` | NEW NEEDED | No large-prompt PortifyProcess test in the suite. |
| 14 | `test_output_format_flag_and_value_are_adjacent` | `tests/pipeline/test_process.py::test_default_output_format_stream_json` (line 17-26), `test_text_output_format` (line 28-37) | Covered (`cmd[idx + 1] == "stream-json"` / `"text"`). |
| 15 | `test_prompt_sidecar_written_when_opted_in` | NEW NEEDED | Sidecar feature not present in current code. |
| 16 | `test_no_sidecar_by_default` | NEW NEEDED | Same. |

**Tally: 4 covered, 1 partial-pair (12), 11 NEW NEEDED.**

Additionally, two existing assertions in `tests/pipeline/test_process.py` would **regress** under DESIGN.md verbatim:
- `test_required_flags` lines 54-55 (`"-p" not in cmd` and `"hello" not in cmd`) — would fail because DESIGN.md restores `-p hello` for sub-96 KiB prompts.
- `TestClaudeProcessStdinDelivery::test_build_command_excludes_prompt` lines 176-177 — same root cause; the small "multi-line body" prompt would be argv-routed.
- `test_start_writes_prompt_to_stdin` (line 181-198) — uses small prompt, would no longer go via stdin under DESIGN.md.

---

## 4. Specific-questions answers

**Q1. Is the bug originally reported (large-prompt argv overflow / E2BIG) covered by any current test?**

YES — at two layers:
- Unit/transport: `tests/pipeline/test_process.py::TestClaudeProcessStdinDelivery::test_stdin_handles_large_payload` (line 200-219) sends a 200 KB prompt through real subprocess via stdin and asserts byte-identical round-trip. The historical 128 KB ceiling is annotated in the docstring (line 201).
- Integration/caller: `tests/roadmap/test_file_passing.py::TestLargePromptSoftWarning::test_under_threshold_no_warning` (line 151-183) embeds 150 KB content (above old 128 KB ceiling) and asserts the `prompt` kwarg arrives intact at ClaudeProcess.

**Q2. Does any existing test pin `cmd.index("-p")` or `"-p" in cmd` — i.e., would break if `-p` is removed?**

The existing tests pin the **opposite** invariant: that `-p` is **absent**.
- `tests/pipeline/test_process.py:54` — `assert "-p" not in cmd`
- `tests/pipeline/test_process.py:176-177` — `assert "-p" not in cmd` and `assert prompt not in cmd`

These would break under DESIGN.md verbatim (which restores `-p` for small prompts). The only `cmd.index("-p")` calls in tests are absent. The only `"-p" in cmd` is in `tests/sprint/test_tmux.py` (tmux flag, unrelated).

**Q3. Does any existing test mock stdin write to verify the prompt is sent there?**

YES, two distinct strategies:
- `tests/pipeline/test_process.py::TestClaudeProcessStdinDelivery` uses a **real subprocess** with a Python stand-in (`sys.executable -c "import sys; sys.stdout.write(sys.stdin.read())"`) that echoes stdin to stdout so the test can read it back from `output_file` — verifying byte-identical delivery (line 181-219).
- `tests/pipeline/test_process_hooks.py` mocks `subprocess.Popen` and provides `fake_popen.stdin = MagicMock()` (lines 47, 60) so the parent's `.write()` / `.close()` calls succeed in unit tests, but does NOT introspect what was written.

No test isolates the writer thread (because there is no thread — the current code writes inline in `start()`).

**Q4. Are there integration tests vs unit tests for ClaudeProcess? Inventory split.**

- **Unit (build_command, env, hook plumbing)**: `tests/pipeline/test_process.py` (TestClaudeProcessCommand, TestClaudeProcessEnv, TestClaudeProcessStreamJsonCompat); `tests/pipeline/test_process_hooks.py`; sprint subclass equivalents in `tests/sprint/test_process.py`.
- **Real-subprocess (transport)**: `tests/pipeline/test_process.py::TestClaudeProcessStdinDelivery` — these spawn an actual Python interpreter as the stand-in for `claude` and exercise the full stdin write path.
- **Caller-level integration (fully mocked ClaudeProcess)**: `tests/roadmap/test_file_passing.py`, `test_inline_fallback.py`, `test_compression_integration.py`, `test_remediate_executor.py`, `test_semantic_layer.py`; `tests/cli/prd/*` for PrdClaudeProcess; `tests/v3.3/test_wiring_points_e2e.py` for sprint executor.
- **No-mock, full-stack against real `claude`**: none in the test tree (those would be in `.github` workflows or manual smoke tests).

**Q5. Are any tests parametrized over prompt size?**

Not parametrized via `@pytest.mark.parametrize`. Discrete prompt sizes are exercised:
- ~30 bytes (multi-line body) — `test_build_command_excludes_prompt`
- ~25 bytes — `test_start_writes_prompt_to_stdin`
- 200 KB — `test_stdin_handles_large_payload`
- 1 MB — `test_broken_pipe_tolerated`
- 150 KB and `_LARGE_PROMPT_WARN_BYTES + 1024` — at the executor level in `test_file_passing.py`.

DESIGN.md's threshold-boundary tests (95 KiB / 97 KiB) and the 16 MiB cap test have no analog.

**Q6. Any tests that simulate subprocess hang / signal handling?**

Yes, but none exercise mid-stdin-write SIGTERM:
- `tests/sprint/test_process.py::TestSignalHandler` (line 241-281) — sets shutdown flag.
- `tests/sprint/test_process.py::TestClaudeProcessPlatformFallback::test_terminate_non_unix_fallback_calls_process_methods` (line 214-238) — terminate fallback when `getpgid`/`killpg` absent.
- `tests/pipeline/test_process_hooks.py::TestOnSignalHook` (line 69-105) — `terminate()` triggers `on_signal` hook before SIGTERM.
- `tests/pipeline/test_process.py::test_broken_pipe_tolerated` (line 221-234) — child exits before reading 1 MB stdin.
- `tests/sprint/test_integration_signal.py` exists (84 KB-ish file in the inventory) — signal-flow integration; not specifically mid-stdin.

DESIGN.md's `test_terminate_during_stdin_write_no_hang` requires an active writer thread, which doesn't exist in current code — **NEW NEEDED**.

**Q7. Any tests for `tool_write_mode`?**

ZERO. Grep `tool_write_mode tests/` returns no hits. `tool_write_mode` is a **new** kwarg on `ClaudeProcess.__init__` (line 53 of `src/superclaude/cli/pipeline/process.py`) added in commit 4799719 alongside the always-stdin migration. `start()` branches on it (line 118-122) to redirect stdout to `<output_file>.log` when set. **No tests pin this behavior.** This is a coverage gap orthogonal to DESIGN.md but worth flagging — DESIGN.md does not address `tool_write_mode` at all.

---

## 5. Final summary

### §9.1 cases already covered (4 of 16)

- #2 `test_build_command_omits_p_flag_for_large_prompt` — covered for ALL sizes by `test_required_flags` and `test_build_command_excludes_prompt` in `tests/pipeline/test_process.py`.
- #7 `test_huge_prompt_delivered_via_stdin` — covered by `test_stdin_handles_large_payload` (real-subprocess, 200 KB) and indirectly by `test_under_threshold_no_warning` (150 KB caller-level mock).
- #14 `test_output_format_flag_and_value_are_adjacent` — covered by `test_default_output_format_stream_json` and `test_text_output_format`.
- #12 `test_portify_add_dir_insertion_unchanged_for_small_prompt` — partial; `TestDualAddDir` and `TestBackwardCompatibilitySC11` exercise add-dir layout symmetrically against the current baseline.

### §9.1 cases that need NEW test files (11 of 16)

- #1 small-prompt argv path with `-p`
- #3 numeric argv-byte-size bound for huge prompts
- #4 95 KiB threshold-under
- #5 97 KiB threshold-over
- #6 empty prompt argv with `-p ""`
- #8 small prompt argv path (round-trip)
- #9 200 KB UTF-8 multibyte
- #10 PROMPT_MAX_BYTES → PromptTooLargeForArgv
- #11 SIGTERM mid-stdin-write writer-thread join
- #13 large-prompt PortifyProcess --add-dir layout
- #15 sidecar opt-in
- #16 no sidecar by default

DESIGN.md §8.2 specifies the new file: `tests/cli/pipeline/test_claude_process_delivery.py`. That directory is empty today (`tests/cli/pipeline/` does not exist). The natural home in the current tree is `tests/pipeline/test_process.py` (extend existing classes) or a new sibling file.

### §9.1 cases that are obsolete given current code

NONE strictly obsolete in §9.1, but ~half are obsolete *as written* because they assume the threshold-based dual path. If the project decides to **stay always-stdin** instead of importing DESIGN.md's threshold model, these become moot:
- #1 (`test_build_command_keeps_p_flag_for_small_prompt`) — never makes sense if `-p` is permanently gone.
- #4, #5 (threshold boundaries) — no threshold to test.
- #6 (`test_empty_prompt_uses_argv_with_empty_p_value`) — under always-stdin, empty prompt is just an empty stdin write; no `-p ""`.
- #8 (`test_small_prompt_still_uses_argv`) — there is no argv path.

### Conflict surface — tests that DESIGN.md verbatim would BREAK

In `tests/pipeline/test_process.py`:
- Line 54 `assert "-p" not in cmd` — would fail (small prompt restores `-p`).
- Line 55 `assert "hello" not in cmd` — would fail.
- Lines 176-177 in `test_build_command_excludes_prompt` — would fail.
- Line 198 in `test_start_writes_prompt_to_stdin` — small prompt no longer routed via stdin; the Python stand-in's stdin-echo returns "" and the assertion against `prompt` fails.

These are the four assertions that hard-pin the always-stdin contract and would have to be reworked (made size-conditional) for DESIGN.md verbatim.

### Coverage gap orthogonal to DESIGN.md

`tool_write_mode` (added in 4799719, present in `src/superclaude/cli/pipeline/process.py:53,68,118-122`) has **zero test coverage**. DESIGN.md does not mention it. Worth flagging for the reconciliation deciders — any unification of DESIGN.md with current code must decide whether `tool_write_mode` survives, and if so, gain tests.

---

**End of D-test-coverage.md**
