# make verify-sync Summary

- **Command:** `cd <worktree> && make verify-sync 2>&1; echo "EXIT=$?"`
- **Exit code:** 0
- **Grep for MISSING|DIFFERS:** 0 matches (no drift detected)
- **`confidence-calibrator.md` entry:** ✅ confirmed in the Agents section
- **All sections:** Skills, Agents, Commands, Hooks, Templates, Installer Registration, Hooks Cross-Consistency — all ✅
- **Banner:** `✅ All components in sync.`
- **Verdict:** **PASS** — `src/superclaude/` and `.claude/` are byte-identical for all components.
