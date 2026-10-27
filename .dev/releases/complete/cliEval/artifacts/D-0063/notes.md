# D-0063 — Implementation notes (T03.22)

## Design decisions

### 1. Stub vs. real binary for prompt-ready + inject

The AC says "asserts prompt readiness observed, input injected." The
production target is the real `claude` REPL, but the real binary
requires authentication that is not available in CI. We resolved this
with a two-track approach:

* **`test_real_claude_help_spawn_and_transcript`** drives the real
  binary in non-interactive mode (`claude --help`). This pins that
  `PtyDriver` + `EvalRunner` can actually spawn the production
  executable and capture its output to the runner-allocated
  transcript path. The test is skipped on hosts without `claude` in
  PATH — covered by `shutil.which("claude") is None`.
* **`test_lifecycle_prompt_ready_and_input_injection`** drives a
  deterministic Python subprocess stub that emits a banner, the
  `> ` prompt-ready marker, then echoes one line. The PTY wiring
  exercised is byte-for-byte identical to the real-binary path; only
  the child differs. This is the FR-G1 round-trip the test matrix
  needs to pass on every host, including auth-less CI.

The split mirrors the unit-test pattern in `test_pty_driver.py` (see
`_prompt_stub_source` plus `test_real_claude_help_smoketest`); the
shared shape was an explicit goal so future maintainers see the
parallel.

### 2. Banner capture in `PtyLifecycleExecutor.inject`

`pexpect.spawn.expect()` consumes everything up to AND INCLUDING the
matched pattern from its internal buffer and returns the pre-match
text in `child.before`. Our `PtyDriver.expect_prompt_ready` surfaces
this `before` text to the caller. A naive `LifecycleExecutor` that
calls `expect_prompt_ready` in `inject` and then drains via
`read_stdout` in `observe` will therefore lose the banner from the
transcript — `read_stdout` only sees what arrives **after** the
prompt-ready match.

We resolved this by capturing the `before` return value in the
executor's `_banner_capture` field during `inject`, then prepending it
to the `observe`-time drain. The placeholder `"> \r\n"` for the
prompt marker itself is appended so transcripts assert against both
the banner and the prompt — matching what the user would have seen
on screen.

### 3. Sub-second timeout via constructor knob, not `EvalSpec.timeout_sec`

`EvalSpec.timeout_sec` is declared as `int | None` in the dataclass.
The test wants a fast timeout (sub-second) so it doesn't slow the
suite by 1+ seconds per run. The runner's `_resolve_timeout` accepts
the constructor's `default_timeout_sec` (float) as a fallback, so
test #3 passes `default_timeout_sec=0.5` and leaves `spec.timeout_sec`
unset. This is the path documented in `runner.py:_resolve_timeout`.

### 4. Why TID251 + FR-G1 message both asserted

The TID251 rule code alone fires for any banned-api hit, including a
generic "don't import X" rule with no remediation message. Asserting
on the `FR-G1` substring in the test output pins not only that the
rule is enabled but that the operator-facing message documenting the
real-subprocess remediation survived. A TOML edit that converts the
table to a bare list of strings would still emit TID251 but drop the
message — and `test_ban_message_references_fr_g1` would catch it.

### 5. Probe directory placement under `src/superclaude/cli/eval/`

The synthetic `import anthropic` file MUST live under the path the
test asserts ruff scans. We chose `_probe_synth_ban_import_rule/` (a
leading-underscore subdirectory) so the file is obviously a probe and
not a candidate for collection by pytest or import by production code.
The cleanup fixture removes the directory at the start AND end of
every test so a partial run cannot leak files across the boundary.

## Files

| Path | Status | Reason |
|---|---|---|
| `tests/cli/eval/test_pty_lifecycle.py` | New | T03.22 deliverable (5 tests). |
| `tests/cli/eval/test_ban_import_rule.py` | New | T03.22 deliverable (3 tests). |
| `pyproject.toml` | Modified | Added `N818` to project-wide ignore list (justified by stable public-API exception names in `cli/eval/`); the `banned-api` table itself was wired in T02.19. |
| `src/superclaude/cli/eval/hook_adapter.py` | Modified | One relative import (`from ..install_hooks`) changed to absolute (`from superclaude.cli.install_hooks`) to clear a pre-existing TID252 finding so the clean-tree AC could be met. |
| `src/superclaude/cli/eval/pty_driver.py` | Modified | `ruff --fix` autocorrect of I001/F401 (import sort, unused imports). No semantic change. |

## Rejected alternatives

* **Inline the synthetic `import anthropic` in a test file.** Rejected
  because pytest collects everything under `tests/` and the import
  would fail at collection time — the test would never run.
* **Use ruff's Python API.** Rejected because ruff's `__main__`
  surface is not part of its public contract; a future ruff version
  could break this without breaking the CLI invocation, which is the
  one CI actually exercises.
* **Assert exit code 1 specifically (vs. any non-zero).** Ruff
  documents `1` for "lint findings found" but reserves higher codes
  for usage errors; we assert non-zero to keep the test robust to a
  future code reorganization while still failing if the rule does not
  fire at all.
