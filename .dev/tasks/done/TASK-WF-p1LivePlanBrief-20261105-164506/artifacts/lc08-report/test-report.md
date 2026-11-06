# Test report: tests/skills/test_worker_contract.py

- Command: `/sc:test tests/skills/test_worker_contract.py --type unit --unattended --report-dir .dev/p1-live/test/`
- Runner: `uv run pytest tests/skills/test_worker_contract.py -v -p no:cacheprovider`
- Branch: ironbelly/p1-live-test (worktree created from ironbelly/OrcaCLICommandRefactor-P1)
- Verdict: PASS
- Result: 394 passed, 0 failed, 0 skipped, 0 errors, in 1.21 s
- Raw output: `.dev/p1-live/test/pytest-output.txt`

## Notes

- `--type unit` was not turned into a marker filter. The file lives in `tests/skills/`, not a `/unit/` folder, so it has no `unit` marker and `-m unit` would have deselected every test. The target file was run as a whole.
- Coverage was not requested (no `--coverage`), so no coverage figures exist.
- Brief guard passed before the run: `.claude/commands/sc/test.md` and `~/.claude/commands/sc/test.md` are byte-identical and both carry an `## Unattended mode` section.
- Nothing was pushed, committed or staged.
