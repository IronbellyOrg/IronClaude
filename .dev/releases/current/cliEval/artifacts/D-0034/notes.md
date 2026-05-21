# D-0034 — Notes (Task T02.14)

## Design decisions

### Why a verbatim copy on top of `install_hooks`?

`install_hooks` merges hook registrations into `settings.json` but
does not copy `hooks.json` itself to the destination. The T02.14 AC
requires `<home_path>/.claude/hooks.json` to be byte-identical
(SHA256-equal) to `src/superclaude/hooks/hooks.json` for two reasons:

1. The per-eval HOME becomes self-describing: a post-mortem operator
   can diff the file against the source to confirm the deployed
   registrations match the source-of-truth.
2. FR-G* gate tests can read the deployed file directly without
   un-merging it from `settings.json`.

A separate step `shutil.copy2` (via the dedicated
`_copy_hooks_json_verbatim` helper) preserves the source mtime and
metadata, which gives idempotency: re-running the adapter produces
the same destination bytes AND the same mtime, so consumers that
mtime-watch the file see no change.

### Why a private `_copy_hooks_json_verbatim` helper?

`install_hooks` uses `shutil.copy2` internally to copy hook scripts.
The adapter's verbatim-copy step also uses `shutil.copy2`. If the
test for `hooks-json-copy-failed` patched the shared `shutil.copy2`
global, it would also break `install_hooks`'s script-copy pipeline
and the patched OSError would surface from the installer first,
making the test verify the wrong failure mode.

The helper is the smallest possible seam: a one-line wrapper whose
only purpose is to be monkeypatch-friendly. The test patches
`superclaude.cli.eval.hook_adapter._copy_hooks_json_verbatim`
directly, leaving `shutil.copy2` untouched for the installer to use.

### Why resolve `home_path / .claude` in the refusal guard?

The naive guard "refuse if `home_path` resolves to real `~/.claude/`"
misses the case where the caller passes their own `$HOME` as
`home_path`. The adapter writes `<home_path>/.claude/settings.json`,
which would land directly on `~/.claude/settings.json` if
`home_path == $HOME`. The fix is to additionally resolve
`home_path / .claude` and check it against the real Claude dir.

Both checks are necessary:
- `home_path` direct check catches `home_path == ~/.claude/` and
  symlinks pointing there.
- `home_path / .claude` check catches `home_path == $HOME` and any
  path whose `.claude` subdir would land under real `~/.claude/`.

### Source resolution

The adapter resolves
`src/superclaude/hooks/hooks.json` independently of
`install_hooks._get_hooks_source` to avoid coupling on a private
helper. The package layout convention is stable:
`hook_adapter.py` lives at `src/superclaude/cli/eval/hook_adapter.py`,
so `__file__.resolve().parent.parent.parent` is the package root.

## Failure-mode taxonomy

The `error_tag` taxonomy is deliberately small (4 tags) and stable so
the EvalRunner's routing table can hard-code them. All tags are
lowercase kebab-case with alphanumeric tokens. Adding new tags is
allowed; renaming existing tags is not (the orchestrator's bucket
mapping treats them as a public API surface).

| Tag                          | Where raised                              |
|------------------------------|-------------------------------------------|
| `refused-real-home`          | `_refuse_real_home`                       |
| `source-hooks-json-missing`  | Early existence check in `deploy_hooks_to` |
| `install-hooks-failed`       | After `install_hooks` returns `(False, …)` |
| `hooks-json-copy-failed`     | After `_copy_hooks_json_verbatim` raises   |

## Pre-existing test failures (out of scope)

`tests/cli/test_install_hooks.py` has 8 pre-existing failures on the
branch tip caused by the test's fake source-tree fixture missing
`reject-workspace-writes.sh`. These failures predate T02.14 and are
not caused by the adapter — verified by `git stash && pytest && git
stash pop` showing the same 8 failures on a clean checkout. Cleanup
tracked separately; out of scope for this task.
