# Flags decision

- Decided by: issue-worker-t1
- Depth: deep

| Field | Value | Reason |
|---|---|---|
| Mode | bug | The description reports a crash (unwanted behaviour) when the description is empty, not a new capability. Verification note: `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py` does not exist in this checkout (scripts/ holds only clickup_claim.py, origin_repo.py, orca_worktree.py), and SKILL.md line 156 already STOPs with usage on an empty description before Activation; the report is still a bug report and its claim should be treated as unverified. codegraph/auggie not used; Grep/Glob/Read only. |
| Type | skill | The file the description names lives under `src/superclaude/skills/sc-issue-protocol/`, and the behaviour belongs to the sc-issue-protocol skill. |
| Issue type | Bug | derived from the mode and the area by the rule in `refs/labels.md` (bug, any area: Bug) |
| Complexity | Complex | follows depth (quick = simple, standard = medium, deep = complex) |
