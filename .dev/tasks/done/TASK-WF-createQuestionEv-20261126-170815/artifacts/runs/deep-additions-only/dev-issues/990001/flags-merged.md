<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (issue-worker-t1, flags-t1.md) -->
<!-- Merge date: 2026-11-26T18:37:54Z -->
# Flags decision

<!-- Source: Base (original, modified) — Change #3 -->
- Decided by: sc:adversarial merge (base: issue-worker-t1; incorporated: user flags)
- Depth: deep

<!-- Source: Base (original); Type row modified per Changes #1 and #2 -->
| Field | Value | Reason |
|---|---|---|
| Mode | feature | The description asks for new output (a skills count as the last line of `superclaude install`); nothing is described as broken. |
| Type | install | The change is in the `superclaude install` flow (`install` command in `src/superclaude/cli/main.py` and `install_all_skills` in `src/superclaude/cli/install_skills.py`), which copies skills to `~/.claude/skills/`. `superclaude update` also calls `install_all_skills` (`main.py:401-403`), and `cli` (the user's flag) is also defensible; the debate left this point unresolved. |
| Issue type | Feature | derived from the mode and the area by the rule in `refs/labels.md` (feature, area not tests, so Feature) |
| Complexity | Complex | follows depth (quick = simple, standard = medium, deep = complex) |
