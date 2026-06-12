# R3 Test & Verification — recursion-breaker test catalogue + regression-test design

Status: Complete

## 1. Recursion-breaker marker catalogue (`test_marker_suppression.py`)

Source under review: `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_marker_suppression.py`.

The module defines `_MARKER = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"` and `_SUPPRESS_MSG = "recursion breaker"` at lines 15-16. The production guard being asserted is the Click group callback in `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/cli/reflect/commands.py`: it checks exact marker value `"1"` at lines 62-69, prints `reflect-wrapper recursion breaker: nested gate suppressed` at lines 70-72, and exits 0 at line 73.

### 1.1 `test_marker_one_suppresses_before_launch`

Lines 19-28 assert the happy suppression case. The test sets `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` with `monkeypatch.setenv`, invokes the reflect Click group via `cli_runner.invoke(reflect_group, ["run", str(temp_tasklist)])`, and asserts: exit code 0; patched `superclaude.cli.reflect.runner.ClaudeProcess` was never constructed; output contains `"recursion breaker"`.

```python
19 def test_marker_one_suppresses_before_launch(
20     cli_runner, temp_tasklist, monkeypatch
21 ) -> None:
22     """marker == "1" -> exit 0 and ClaudeProcess is NEVER constructed (AC-1)."""
23     monkeypatch.setenv(_MARKER, "1")
24     with patch("superclaude.cli.reflect.runner.ClaudeProcess") as mock_cls:
25         result = cli_runner.invoke(reflect_group, ["run", str(temp_tasklist)])
26     assert result.exit_code == 0
27     mock_cls.assert_not_called()
28     assert _SUPPRESS_MSG in result.output
```

### 1.2 `test_marker_one_suppresses_since_moved_file`

Lines 31-40 assert the group-callback guard pre-empts Click path validation. The test sets `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1`, invokes `reflect run /no/such/since-moved-tasklist.md`, and still expects exit code 0, no `ClaudeProcess` construction, and the suppression message. This is load-bearing because the production guard is intentionally placed before `click.Path(exists=True)` validation, per `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/cli/reflect/commands.py` lines 62-68 and the `exists=True` argument declaration at lines 76-80.

```python
31 def test_marker_one_suppresses_since_moved_file(cli_runner, monkeypatch) -> None:
32     """marker == "1" pre-empts Click exists=True: a since-moved path still exits 0."""
33     monkeypatch.setenv(_MARKER, "1")
34     with patch("superclaude.cli.reflect.runner.ClaudeProcess") as mock_cls:
35         result = cli_runner.invoke(
36             reflect_group, ["run", "/no/such/since-moved-tasklist.md"]
37         )
38     assert result.exit_code == 0
39     mock_cls.assert_not_called()
40     assert _SUPPRESS_MSG in result.output
```

### 1.3 Shared negative-control helper `_assert_not_suppressed`

Lines 43-53 are the shared negative-control assertion. It stubs `ClaudeProcess` with the fixture-backed `make_stub("pass.yaml", rc=0)`, invokes `reflect run <temp_tasklist>`, then asserts the suppression message is absent and at least one `ClaudeProcess` launch occurred.

```python
43 def _assert_not_suppressed(cli_runner, temp_tasklist, make_stub):
44     """Helper: a non-suppressing marker proceeds to a real (stubbed) launch."""
45     factory = make_stub("pass.yaml", rc=0)
46     with patch(
47         "superclaude.cli.reflect.runner.ClaudeProcess", side_effect=factory
48     ) as mock_cls:
49         result = cli_runner.invoke(reflect_group, ["run", str(temp_tasklist)])
50     # NOT suppressed: the guard message is absent and a launch occurred.
51     assert _SUPPRESS_MSG not in result.output
52     assert mock_cls.call_count >= 1
53     return result
```

### 1.4 `test_marker_zero_does_not_suppress`

Lines 56-66 set `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=0` and delegate to `_assert_not_suppressed`, proving the guard is exact-string, not truthiness based.

```python
56 def test_marker_zero_does_not_suppress(
57     cli_runner,
58     temp_tasklist,
59     patch_git,
60     patch_runner_env,
61     make_claude_process_stub,
62     monkeypatch,
63 ) -> None:
64     """marker == "0" must NOT suppress (only the string "1" does)."""
65     monkeypatch.setenv(_MARKER, "0")
66     _assert_not_suppressed(cli_runner, temp_tasklist, make_claude_process_stub)
```

### 1.5 `test_marker_absent_does_not_suppress`

Lines 69-79 delete `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` and delegate to `_assert_not_suppressed`, proving normal CLI behavior when the marker is absent.

```python
69 def test_marker_absent_does_not_suppress(
70     cli_runner,
71     temp_tasklist,
72     patch_git,
73     patch_runner_env,
74     make_claude_process_stub,
75     monkeypatch,
76 ) -> None:
77     """marker absent (unset) must NOT suppress."""
78     monkeypatch.delenv(_MARKER, raising=False)
79     _assert_not_suppressed(cli_runner, temp_tasklist, make_claude_process_stub)
```

### 1.6 `test_marker_two_does_not_suppress`

Lines 82-92 set `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=2` and delegate to `_assert_not_suppressed`, explicitly guarding against a too-loose truthiness check.

```python
82 def test_marker_two_does_not_suppress(
83     cli_runner,
84     temp_tasklist,
85     patch_git,
86     patch_runner_env,
87     make_claude_process_stub,
88     monkeypatch,
89 ) -> None:
90     """marker == "2" must NOT suppress (guards against a too-loose truthiness check)."""
91     monkeypatch.setenv(_MARKER, "2")
92     _assert_not_suppressed(cli_runner, temp_tasklist, make_claude_process_stub)
```

## 2. Marker-set vs marker-unset proof for reflect CLI tests

### 2.1 These tests invoke the reflect CLI

`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_cli_smoke.py` imports `reflect_group` at line 13. It invokes the Click group directly in all CLI smoke cases: group help at lines 34-37; run help at lines 40-44; dry-run at lines 47-54; print-command at lines 57-68; nonexistent tasklist at lines 71-74; argv preview at lines 77-102; config-stop sidecar at lines 105-129.

`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_promote_plumbing.py` imports `reflect_group` at line 11. Two tests build prompt/config directly at lines 22-35, but the CLI regression guard invokes `reflect_group` with `cli_runner.invoke(reflect_group, ["run", str(temp_tasklist), "--print-command"])` at lines 38-52.

Because the production marker guard runs in the group callback before subcommand parsing, any `cli_runner.invoke(reflect_group, ...)` executed with `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` can short-circuit to exit 0 with only the recursion-breaker message; see `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/cli/reflect/commands.py` lines 62-73.

### 2.2 Marker-set proof run

Command run from repo root `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring`:

```bash
SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1 uv run pytest tests/cli/reflect/test_cli_smoke.py tests/cli/reflect/test_promote_plumbing.py -q
```

Observed result: exit code 1; 6 failed, 4 passed. Load-bearing output:

```text
collected 10 items

tests/cli/reflect/test_cli_smoke.py .F.FFFF                              [ 70%]
tests/cli/reflect/test_promote_plumbing.py ..F                           [100%]

=================================== FAILURES ===================================
_____________________ test_run_help_shows_all_spec9_flags ______________________
tests/cli/reflect/test_cli_smoke.py:44: in test_run_help_shows_all_spec9_flags
    assert flag in result.output, f"missing option in help: {flag}"
E   AssertionError: missing option in help: --tmux
E   assert '--tmux' in 'reflect-wrapper recursion breaker: nested gate suppressed\n'
E    +  where 'reflect-wrapper recursion breaker: nested gate suppressed\n' = <Result okay>.output
_________________ test_print_command_prints_and_never_launches _________________
tests/cli/reflect/test_cli_smoke.py:66: in test_print_command_prints_and_never_launches
    assert "/sc:reflect --mode post" in result.output
E   AssertionError: assert '/sc:reflect --mode post' in 'reflect-wrapper recursion breaker: nested gate suppressed\n'
E    +  where 'reflect-wrapper recursion breaker: nested gate suppressed\n' = <Result okay>.output
_____________________ test_nonexistent_tasklist_is_nonzero _____________________
tests/cli/reflect/test_cli_smoke.py:74: in test_nonexistent_tasklist_is_nonzero
    assert result.exit_code != 0
E   assert 0 != 0
E    +  where 0 = <Result okay>.exit_code
____________ test_print_command_argv_preview_matches_build_command _____________
tests/cli/reflect/test_cli_smoke.py:95: in test_print_command_argv_preview_matches_build_command
    assert "--no-session-persistence" in out
E   AssertionError: assert '--no-session-persistence' in 'reflect-wrapper recursion breaker: nested gate suppressed\n'
___________________ test_config_stop_writes_blocked_sidecar ____________________
tests/cli/reflect/test_cli_smoke.py:125: in test_config_stop_writes_blocked_sidecar
    assert result.exit_code == 2
E   assert 0 == 2
E    +  where 0 = <Result okay>.exit_code
_________________ test_default_promote_is_on_regression_guard __________________
tests/cli/reflect/test_promote_plumbing.py:51: in test_default_promote_is_on_regression_guard
    assert "/sc:reflect --mode post" in result.output
E   AssertionError: assert '/sc:reflect --mode post' in 'reflect-wrapper recursion breaker: nested gate suppressed\n'
E    +  where 'reflect-wrapper recursion breaker: nested gate suppressed\n' = <Result okay>.output
========================= 6 failed, 4 passed in 0.16s ==========================
```

Interpretation: this proves marker leakage breaks reflect CLI tests that expect normal CLI parsing/preview/validation. The marker makes the group callback suppress the run and return `<Result okay>` with only `reflect-wrapper recursion breaker: nested gate suppressed`.

### 2.3 Marker-unset proof run

Command run from repo root `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring`:

```bash
env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE uv run pytest tests/cli/reflect/test_cli_smoke.py tests/cli/reflect/test_promote_plumbing.py -q
```

Observed result: exit code 0; 10 passed. Output:

```text
collected 10 items

tests/cli/reflect/test_cli_smoke.py .......                              [ 70%]
tests/cli/reflect/test_promote_plumbing.py ...                           [100%]

============================== 10 passed in 0.14s ==============================
```

## 3. Regression-test design for the fix

### 3.1 What can be tested without live `claude --print`

The leak manifests inside a live reflect subprocess, but the regression does not need an LLM subprocess. The testable invariant is: the §6.1.1 verification-envelope command/path that runs UC-2 step 5.5 verification must strip `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` before invoking verification commands. This prevents reflect CLI tests from inheriting the wrapper marker while preserving the recursion-breaker for actual nested reflect gates.

Current §6.1.1 has the safety-envelope controls for `execute_shell_command` at `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/sc-reflect-protocol/SKILL.md` lines 489-502. The current eight controls cover template construction, verb allowlist, metacharacter rejection, timeout, output cap, cwd scoping, audit artifact, and `--no-verify` at lines 493-500. No current line in that section mentions `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` or `env -u`, so a content-contract test would currently fail and would pass after the skill-body fix is added.

### 3.2 Recommended lowest-friction regression test: content/contract test

Recommended file: `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py`.

Rationale: this file already contains Layer-A content/contract tests that read source skill text, not `.claude/` mirrors. It defines `_REPO_ROOT` at lines 18-20 and reads `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/task-builder/SKILL.md` for a wrapper-shell-out contract test at lines 80-92. A sibling content test for `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/sc-reflect-protocol/SKILL.md` is idiomatic and avoids any `claude --print` subprocess.

Proposed test name: `test_execute_shell_command_envelope_strips_reflect_wrapper_marker`.

Proposed implementation shape:

```python
_REFLECT_SKILL_SRC = _REPO_ROOT / "src/superclaude/skills/sc-reflect-protocol/SKILL.md"


def _extract_execute_shell_command_envelope(text: str) -> str:
    start = text.index("### 6.1.1 `execute_shell_command` safety envelope")
    end = text.index("### 6.2", start)
    return text[start:end]


def test_execute_shell_command_envelope_strips_reflect_wrapper_marker() -> None:
    """Regression guard: verification subprocesses must not inherit the reflect wrapper marker."""
    text = _REFLECT_SKILL_SRC.read_text(encoding="utf-8")
    envelope = _extract_execute_shell_command_envelope(text)
    assert "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE" in envelope
    assert "env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE" in envelope
```

Exact assertions:

1. `assert "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE" in envelope` — proves §6.1.1 explicitly accounts for the recursion-breaker marker.
2. `assert "env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE" in envelope` — proves the control is a concrete env-strip command prefix rather than vague prose. This is intentionally specific because the required fix is to strip the marker for verification commands only.

Verification command for the builder after adding the test and skill fix:

```bash
uv run pytest tests/cli/reflect/test_no_nesting_guard.py tests/cli/reflect/test_cli_smoke.py tests/cli/reflect/test_promote_plumbing.py -q
```

Optional red/green command that demonstrates the original failure mode remains real while the contract test is independent:

```bash
SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1 uv run pytest tests/cli/reflect/test_cli_smoke.py tests/cli/reflect/test_promote_plumbing.py -q
```

Expected behavior of that optional command remains failure outside the verification envelope, because these tests intentionally invoke the reflect CLI under the marker; the actual fix is that the §6.1.1 verification subprocess must run them with the marker stripped.

### 3.3 If R2 implements the fix in Python code instead of skill text

If R2 identifies or adds a Python helper that prepares verification command env, prefer a direct unit test on that helper over the content test. The invariant should be the same: input environment contains `{"SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE": "1", ...}`; output env/command for verification omits the marker or wraps the command with `env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`. I did not find such a Python verification helper in the scoped test files; current verification-envelope source of truth appears to be skill text at `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/sc-reflect-protocol/SKILL.md` lines 489-502.

## 4. Test framework and idioms in `tests/cli/reflect/`

### 4.1 Fixtures

`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/conftest.py` provides shared test utilities:

- `cli_runner()` returns a fresh `click.testing.CliRunner` at lines 40-43.
- `temp_tasklist(tmp_path)` writes a minimal MDTM tasklist with `start_commit` and `reflect_post` frontmatter and returns its `Path` at lines 46-55.
- `patch_git(monkeypatch)` stubs `superclaude.cli.reflect.config._git` so config resolution works without a real repo; it returns fake HEAD/base SHAs at lines 58-80.
- `patch_runner_env(monkeypatch)` stubs `runner._child_env` to `{}` and `runner.shutil.which` to `/usr/bin/claude` so launch-path tests can run under isolation at lines 83-95.
- `make_claude_process_stub()` returns the Idiom-B `ClaudeProcess` factory that writes a fixture `return-contract.yaml` during `.wait()` at lines 98-138.
- `make_claude_process_sequence()` supports multi-step bounded fix-loop tests by returning successive fake `ClaudeProcess` objects at lines 141-188.

### 4.2 Env mutation pattern

Marker tests use pytest's `monkeypatch` fixture: `monkeypatch.setenv(_MARKER, "1")` at `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_marker_suppression.py` line 23 for suppression, `setenv(..., "0")` at line 65 and `setenv(..., "2")` at line 91 for negative controls, and `monkeypatch.delenv(_MARKER, raising=False)` at line 78 for absent-marker behavior.

### 4.3 Click invocation pattern

Reflect CLI tests import `reflect_group` directly and use `cli_runner.invoke(...)`, not shell subprocesses. Examples: `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_cli_smoke.py` lines 34-44 for help commands, lines 47-68 for `--dry-run`/`--print-command`, and `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_promote_plumbing.py` lines 46-52 for the promote default CLI guard.

### 4.4 Patching launch boundaries

Tests that assert no live launch occurs patch `superclaude.cli.reflect.runner.ClaudeProcess` and assert `mock_cls.assert_not_called()`, e.g. `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_cli_smoke.py` lines 47-54, 57-68, and 77-102. Marker suppression tests use the same patch to prove the guard exits before construction at `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_marker_suppression.py` lines 23-28 and 33-40.

### 4.5 Source-text contract test pattern

`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py` is the best home for the regression because it already treats source text as the contract. It defines source paths at lines 18-24, extracts the task-builder wrapper branch with string anchors at lines 49-65, and asserts positive/negative contract tokens at lines 80-92. The proposed §6.1.1 marker-strip test should follow this pattern: read `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, extract the bounded section with stable headings, then assert concrete control tokens.

## Summary

- The marker suppression unit tests are already strong: they prove exact-string suppression for `"1"`, Click-validation pre-emption for since-moved files, and negative controls for `"0"`, absent, and `"2"`.
- The marker-set pytest run proves the live failure mode for CLI tests: 6 failures caused by `reflect-wrapper recursion breaker: nested gate suppressed` replacing expected help/preview/validation output.
- The marker-unset pytest run proves the same tests pass cleanly: 10 passed.
- Recommended regression test: add a source-text contract test in `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py` asserting §6.1.1 in `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/sc-reflect-protocol/SKILL.md` includes `env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`.
