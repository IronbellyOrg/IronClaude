# Flags decision

- Decided by: issue-worker-t2
- Depth: quick

| Field | Value | Reason |
|---|---|---|
| Mode | bug | The description reports excessive launch time and CPU use with a large session list in existing functionality, not a new feature request. |
| Type | cli | The affected component is the executable session-manager launcher at `/home/coder/workspaces/IronClaude/src/superclaude/skills/ccsession-tag/ccsession`; although bundled with a skill, it is a shell CLI rather than a skill instruction or slash command. |
| Issue type | Bug | Derived from the mode and area by the rule in `refs/labels.md`: bug in any area maps to Bug. |
| Complexity | Simple | Follows the requested depth: quick = Simple; this is not an implementation-effort assessment. |
