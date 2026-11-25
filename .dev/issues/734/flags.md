# Flags decision

- Decided by: mode given, type chosen by issue-worker-t2
- Depth: quick

| Field | Value | Reason |
|---|---|---|
| Mode | feature | Given by the coordinator on the owner's behalf; adds unattended operation rather than fixing an existing supported mode. |
| Type | command | Adds unattended operation to /sc:spec-panel-stoprule, with its skill, script, worker contract and tests supporting that command. |
| Issue type | Feature | Derived from feature mode and an area other than tests by the rule in `refs/labels.md`; Feature is listed in the repo's issue types. |
| Complexity | Medium | The depth rule gives Simple for quick; the coordinator overrides it to Medium because it changes a verdict-computing review loop that other work gates on. |
