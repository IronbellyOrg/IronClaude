# D-0034 — Evidence (Task T02.14)

## Test execution

```text
$ uv run pytest tests/cli/eval/test_hook_adapter.py -v
============================== test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
collected 12 items

tests/cli/eval/test_hook_adapter.py::test_deploy_hooks_to_writes_settings_json_under_home_path PASSED
tests/cli/eval/test_hook_adapter.py::test_deploy_hooks_to_copies_hook_scripts                  PASSED
tests/cli/eval/test_hook_adapter.py::test_hooks_json_is_byte_identical_to_source               PASSED
tests/cli/eval/test_hook_adapter.py::test_re_invocation_is_idempotent                          PASSED
tests/cli/eval/test_hook_adapter.py::test_real_user_claude_dir_is_untouched                    PASSED
tests/cli/eval/test_hook_adapter.py::test_refuses_when_home_path_is_real_user_claude_dir        PASSED
tests/cli/eval/test_hook_adapter.py::test_refuses_when_home_path_is_descendant_of_real_user_claude_dir PASSED
tests/cli/eval/test_hook_adapter.py::test_install_hooks_failure_propagates_as_hook_deploy_failed PASSED
tests/cli/eval/test_hook_adapter.py::test_missing_source_hooks_json_raises_hook_deploy_failed   PASSED
tests/cli/eval/test_hook_adapter.py::test_hooks_json_copy_failure_raises_hook_deploy_failed     PASSED
tests/cli/eval/test_hook_adapter.py::test_error_tags_are_kebab_case_strings                    PASSED
tests/cli/eval/test_hook_adapter.py::test_settings_json_merge_uses_per_eval_target_path        PASSED

============================== 12 passed in 0.15s ==============================
```

Full log: `TASKLIST_ROOT/evidence/T02.14/pytest-T02.14.log`.

## Source hooks.json SHA256 (verbatim-copy reference)

```
cd630cac2a8b9e683adb3d676dd58f132f8ebed0c426081b04ebbd139364daad  src/superclaude/hooks/hooks.json
```

The `test_hooks_json_is_byte_identical_to_source` test asserts that
the deployed `<home>/.claude/hooks.json` SHA256-equals the source.

## Acceptance criteria checklist

- [x] **Function exists.** `deploy_hooks_to(home_path: Path) -> None` defined in
      `src/superclaude/cli/eval/hook_adapter.py` and re-exported from
      `superclaude.cli.eval`.
- [x] **Calls `install_hooks` with target under home_path.**
      Verified by `test_settings_json_merge_uses_per_eval_target_path` —
      the spy captures `target_path=<home>/.claude/settings.json`.
- [x] **Raises `HookDeployFailed` with `error_tag` on failure.**
      Verified by `test_install_hooks_failure_propagates_as_hook_deploy_failed`,
      `test_missing_source_hooks_json_raises_hook_deploy_failed`,
      `test_hooks_json_copy_failure_raises_hook_deploy_failed`,
      `test_refuses_when_home_path_is_real_user_claude_dir`.
- [x] **Idempotent.** Verified by `test_re_invocation_is_idempotent` —
      re-invocation produces byte-identical `settings.json`,
      `hooks.json`, and an identical set of hook scripts.
- [x] **`<home>/.claude/hooks.json` byte-identical to source.**
      Verified by `test_hooks_json_is_byte_identical_to_source` (SHA256
      equality assertion).
- [x] **Never writes to real `~/.claude/`.** Verified by
      `test_real_user_claude_dir_is_untouched` (mtime fixture) plus the
      two refusal tests
      (`test_refuses_when_home_path_is_real_user_claude_dir`,
      `test_refuses_when_home_path_is_descendant_of_real_user_claude_dir`).
- [x] **Adapter contract documented.** See `D-0034/spec.md`.

## Files added / modified

| Path                                                          | Action   |
|---------------------------------------------------------------|----------|
| `src/superclaude/cli/eval/hook_adapter.py`                    | added    |
| `src/superclaude/cli/eval/__init__.py`                        | edited   |
| `tests/cli/eval/test_hook_adapter.py`                         | added    |
| `.dev/releases/current/cliEval/artifacts/D-0034/spec.md`      | added    |
| `.dev/releases/current/cliEval/artifacts/D-0034/notes.md`     | added    |
| `.dev/releases/current/cliEval/artifacts/D-0034/evidence.md`  | added    |
| `.dev/releases/current/cliEval/evidence/T02.14/pytest-T02.14.log` | added    |

## Pre-existing failures (NOT introduced by this task)

`tests/cli/test_install_hooks.py` shows 8 failures on the branch tip
both before and after this commit (verified via `git stash`). The
failures stem from the test's fake source-tree fixture not staging
`reject-workspace-writes.sh`. The adapter does not interact with that
fixture and does not regress those tests; they require a separate
cleanup task.
