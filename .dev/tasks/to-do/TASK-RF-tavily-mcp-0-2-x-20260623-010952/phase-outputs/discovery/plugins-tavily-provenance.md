# H2 Discovery — `plugins/superclaude/mcp/configs/tavily.json` Provenance

**Date:** 2026-06-23
**Step:** 1.3 (Phase 1 discovery)
**Finding folded in:** H2 (reflect-fixes 03, lines 32-34)

## VERDICT

`TRACKED-HAND-MAINTAINED`

The `plugins/superclaude/mcp/configs/tavily.json` copy is an independent git-tracked
file with **no regeneration link** from `src/superclaude/`. It MUST be deleted in
Phase 2 Step 2.2 alongside the `src/` copy.

## Evidence

### (a) Git tracking — both files tracked
```
$ git ls-files src/superclaude/mcp/configs/tavily.json
src/superclaude/mcp/configs/tavily.json
$ git ls-files plugins/superclaude/mcp/configs/tavily.json
plugins/superclaude/mcp/configs/tavily.json
```
Both are git-tracked. The `plugins/` copy is therefore a real tracked file, not a
build artifact ignored by git.

### (b) Build script treats `plugins/superclaude/` as SOURCE, not output
`scripts/build_superclaude_plugin.py`:
- L16: `PLUGIN_SRC = ROOT / "plugins" / "superclaude"`  ← this tree is the **source**
- L17: `DIST_ROOT = ROOT / "dist" / "plugins" / "superclaude"`  ← the **output** (matches `Makefile:65` `PLUGIN_DIST := dist/plugins/superclaude`)
- L51-52: `if not PLUGIN_SRC.exists(): raise SystemExit(...)` — the script READS `plugins/superclaude/`; it never writes to it.

The build flows `plugins/superclaude/` → `dist/plugins/superclaude/`. The documented
build output (`dist/plugins/`) is downstream of, not the same as, the tracked
`plugins/superclaude/` tree. There is **no** code path in the repo that regenerates
`plugins/superclaude/` from `src/superclaude/` (the `src/ → .claude/` sync via
`make sync-dev` targets `.claude/`, not `plugins/`).

### (c) Build script does NOT copy `mcp/configs` at all
`scripts/build_superclaude_plugin.py:75-76`:
```python
for folder in ["agents", "commands", "hooks", "scripts", "skills"]:
    copy_tree(PLUGIN_SRC / folder, DIST_ROOT / folder)
```
Only `agents, commands, hooks, scripts, skills` are copied into `dist/`. `mcp/configs`
is neither read from `src/` nor written into `dist/` by the build. The
`plugins/superclaude/mcp/configs/tavily.json` file is thus a standalone tracked
artifact maintained by hand, with no generation source and no consumer in the build.

## Instruction for Phase 2 Step 2.2

Because the VERDICT is `TRACKED-HAND-MAINTAINED`:
- DELETE `src/superclaude/mcp/configs/tavily.json` (`git rm`, since tracked).
- ALSO DELETE `plugins/superclaude/mcp/configs/tavily.json` (`git rm`, since tracked) —
  it has no regeneration link, so it will NOT disappear on rebuild and must be removed explicitly.
- Delete no other config file.
