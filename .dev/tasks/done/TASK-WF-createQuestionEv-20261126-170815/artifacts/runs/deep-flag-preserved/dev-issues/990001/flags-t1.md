# Flags decision

- Decided by: issue-worker-t1
- Depth: deep

| Field | Value | Reason |
|---|---|---|
| Mode | feature | The description asks for new output (a skills count as the last line), not a fix of broken behaviour; today `install` ends with the Step 10 retire step and the exit-code check, with no count line (src/superclaude/cli/main.py:271-296), and `install_all_skills` already reports per-category counts but no total (src/superclaude/cli/install_skills.py:119-147). |
| Type | cli | The change lives in the `superclaude install` click command (src/superclaude/cli/main.py:46, steps at 202-296) and its skills installer module (src/superclaude/cli/install_skills.py:62); this is Python CLI code, not an installed command, skill, hook or agent primitive. |
| Issue type | Feature | derived by the rule in `refs/labels.md`: feature in any area other than tests -> Feature (bug -> Bug; feature in tests -> Test). |
| Complexity | Complex | follows depth (deep = Complex). |
