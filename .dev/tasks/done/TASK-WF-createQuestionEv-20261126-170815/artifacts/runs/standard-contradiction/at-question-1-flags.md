# Flags decision

- Decided by: issue-worker-t2
- Depth: standard

| Field | Value | Reason |
|---|---|---|
| Mode | bug | Agree with `--mode bug`: the description alleges a crash, not a new feature; `src/superclaude/commands/issue.md:56` requires an empty description to STOP with "--create needs a description". The alleged crash is not reproduced or verified by this quick check. |
| Type | skill | Disagree with `--type skill`; recommend `command` for the empty-description input gate explicitly owned by `src/superclaude/commands/issue.md:51-56`, before skill Activation (`src/superclaude/commands/issue.md:108-114`). Retain the supplied `skill` flag for filing, per the standard-depth rule. The skill directory and command file exist, but the user's named `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py` does not: an exact repository-wide Glob found no `create_issue.py`; `src/superclaude/skills/sc-issue-protocol/SKILL.md:33-35` lists the actual helper scripts, and `:98-103` describes the create workflow rather than such a script. A skill-internal crash location therefore cannot be accepted as verified evidence. |
| Issue type | Bug | derived from the mode and the area by the rule in `refs/labels.md` |
| Complexity | Medium | follows depth (quick = simple, standard = medium, deep = complex); `--depth standard` therefore means Medium, regardless of the unverified crash claim. |
