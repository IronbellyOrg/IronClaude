# Flags decision

- Decided by: issue-worker-t2
- Depth: standard

| Field | Value | Reason |
|---|---|---|
| Mode | bug | agree: a reported crash on an empty description is defective existing behavior, not a request for a new feature; the crash itself is not verified. |
| Type | skill | agree: `sc-issue-protocol/SKILL.md` owns the create workflow and delegates it to `refs/create.md`, so skill fits the affected area. |
| Issue type | Bug | derived from the mode and the area by the rule in `refs/labels.md` |
| Complexity | Medium | follows depth (quick = simple, standard = medium, deep = complex) |

## Validation

No disagreement.

Both named scripts, `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py` and `src/superclaude/skills/sc-issue-protocol/scripts/issue_logger.py`, are absent from this checkout. The skill's file inventory instead describes a Markdown-driven create workflow. The alleged crash and logging behavior are not verified; these evidence gaps do not justify changing the user's mode or type.
