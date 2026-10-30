**Phase 2 (install codegraph) progress: G3 indexing hook**

- Commit: 997b8cc5 `feat(hooks): index each checkout with codegraph on its first session` on `ironbelly/feat-codememory-codegraph-init`
- Done: Task 9. A POSIX `sh` SessionStart hook (matcher `startup`, timeout 5) starts one detached `codegraph init --yes <git top-level>` when `<top>/.codegraph/codegraph.db` is absent. It uses the binary the installer recorded in `~/.codegraph/.superclaude-bin`, else `codegraph` on PATH; it skips `$HOME`, `/` and non-git directories; it always exits 0 and prints nothing; `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` turns it off. Registered in `src` and `plugins` `hooks.json`, mirrored to `plugins/superclaude/hooks/scripts/`, listed in `_FRESHNESS_SCRIPTS`.
- Tests: `uv run pytest tests/cli/test_codegraph_session_start_hook.py tests/cli/test_install_hooks.py tests/unit/test_cli_install.py -q -p no:cacheprovider` -> 133 passed (12 hook tests, including: returns in under 1 s while the stub sleeps 10 s, stdout always empty). `sh -n`, `cmp` of the two copies, `make sync-dev`, `make verify-sync` all pass. `tests/cli/test_verify_sync_hooks.py` -> 7 passed, no failing id outside the baseline.
- Decisions taken: all "self", logged in `.dev/codegraph-migration/decisions/P2X-log.md`
- Not verified: whether Claude Code kills the hook's background process when the hook or the session ends. That is only observable inside a real session; Task 13 records it if one can be started, otherwise it stays marked UNVERIFIED.
- Next: G4 guidance, docs, CI and the isolated-HOME proof (Tasks 10-13)
