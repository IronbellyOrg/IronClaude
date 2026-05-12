# Phase 6: No State File Test (Item 6.5)
**Result:** CRASH — FileNotFoundError for roadmap.md

When run against a directory with no `.roadmap-state.json` AND no `roadmap.md`, the command crashes with `FileNotFoundError: roadmap.md`. This is NOT an auto-wire bug — it's the existing behavior when no roadmap is found. The auto-wire itself returns None gracefully (via `read_state`), but the downstream roadmap resolution doesn't handle missing files. Pre-existing issue.
