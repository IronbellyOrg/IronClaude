# Flags decision

- Decided by: issue-worker-t1
- Depth: deep

| Field | Value | Reason |
|---|---|---|
| Mode | feature | The description asks for new output (a skills count as the last line of `superclaude install`); nothing is described as broken. |
| Type | install | The change is in the `superclaude install` flow (`install` command in `src/superclaude/cli/main.py` and `install_all_skills` in `src/superclaude/cli/install_skills.py`), which copies skills to `~/.claude/skills/`. |
| Issue type | Feature | derived from the mode and the area by the rule in `refs/labels.md` (feature, area not tests, so Feature) |
| Complexity | Complex | follows depth (quick = simple, standard = medium, deep = complex) |
