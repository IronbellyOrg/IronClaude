# Flags decision

- Decided by: mode given by the user, type chosen by issue-worker-t2
- Depth: quick (nothing was given)

| Field | Value | Reason |
|---|---|---|
| Mode | feature | Given by the user; retained unchanged. |
| Type | command | The feature adds unattended behaviour to /sc:implement; its protocol skill, helper script, worker-contract text and tests support that command. |
| Issue type | Feature | Derived from mode feature and area command by the rule in `refs/labels.md`: a feature outside tests is Feature. |
| Complexity | Complex | The depth rule gives Simple, but the coordinator overrides it to Complex because the issue is a 37-requirement change to a protocol other work depends on. |
