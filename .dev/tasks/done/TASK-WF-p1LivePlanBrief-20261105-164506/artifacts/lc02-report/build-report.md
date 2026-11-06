# Build report: /sc:build --type dev --unattended

- Date: 2026-11-05
- Worktree: /home/coder/workspaces/worktrees/IronClaude/p1-live-build (branch ironbelly/p1-live-build, clean before the run)
- Result: SUCCEEDED

## Guard
- Both copies of the command file (project `.claude/commands/sc/build.md` and `~/.claude/commands/sc/build.md`) are byte-identical and have an `## Unattended mode` section.
- The brief line carries a standalone `--unattended`; `/sc:build` is not on the never-as-worker list. Guard passed.

## What was built
- Build system: hatchling (PEP 517), from `pyproject.toml`. Dev type: no clean, no optimize.
- Command: `uv build --wheel --out-dir .dev/p1-live/build/dist` (log: `.dev/p1-live/build/build.log`).
- Output: `.dev/p1-live/build/dist/superclaude-5.0.0-py3-none-any.whl`, 8,328,972 bytes.
- sha256: `acc8592136a8d9c2acd5010be5f806312c11b7563b327581b2c2dbb428b0d902`
- Exit code 0, about 1 second.

## Checks on the wheel
- Valid zip (testzip: no bad members), 1812 files, `superclaude-5.0.0.dist-info/METADATA` present.
- 124 files under `commands/` paths, including `superclaude/commands/build.md`.

## Not done (out of scope for this command)
- `make build-plugin` not run: it goes through `uv run`, which would sync a virtual environment (an install), and writes `dist/` in the repo root.
- No install, push, commit, stage or deployment.

## Notes for the coordinator
- `.dev/p1-live/build/` matches the repo's `.gitignore` rule `build/` (`.gitignore:7`). Nothing here shows in `git status`. If you want these files tracked, that needs `git add -f`, and the choice is yours.
- A `return-contract.yaml` already exists at the repo root from an older commit (81effef3). It was not touched.
