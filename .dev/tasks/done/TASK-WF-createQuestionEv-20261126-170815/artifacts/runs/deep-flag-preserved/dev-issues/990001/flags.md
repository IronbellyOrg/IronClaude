# Flags decision

- Decided by: user (taken as given)
- Depth: deep

| Field | Value | Reason |
|---|---|---|
| Mode | bug | passed as `--mode bug`; the deep compare (adversarial/merged-flags.md, convergence 100%) found the evidence favours `feature`, recorded as the pushback comment, not applied |
| Type | cli | passed as `--type cli`; issue-worker-t1 chose `cli` independently (src/superclaude/cli/main.py:46, src/superclaude/cli/install_skills.py:62) |
| Issue type | Bug | derived from the mode and the area by the rule in `refs/labels.md` |
| Complexity | Complex | follows depth (quick = simple, standard = medium, deep = complex) |

Disagreement for the Wave 5 pushback comment: Mode (user `bug`, issue-worker-t1 and the debate `feature`), and therefore Issue type (Bug vs Feature) and label (`bug` vs `enhancement`).
