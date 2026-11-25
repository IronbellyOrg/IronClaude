## Owner decision 2026-11-17

Option A chosen: fix the two parser gaps in `block-bare-python.sh` (a `python3` call inside an unquoted shell heredoc, and one inside a `coproc` body). The simpler "block any python or pip word outside quotes" rule is not taken.

Next steps:
1. Patch the hook so both commands from this issue exit 2 (blocked), and a plain allowed command still exits 0.
2. Add both commands to `tests/hooks/test_block_bare_python.py`.
3. Reuse the same hook edit path as #359; keep the `plugins/superclaude/hooks/scripts/` mirror in step with `src/superclaude/hooks/scripts/`.

Related: #357 (original hook issue), #359 (PR that added it).

Posted by Claude Code on the owner's instruction.
