# Flags decision

- Decided by: <user (taken as given) | issue-worker-t2 | issue-worker-t1>
- Depth: <quick | standard | deep>

| Field | Value | Reason |
|---|---|---|
| Mode | <feature | bug> | <one line> |
| Type | <cicd | command | skill | agent | hook | cli | core | docs | tests | install | other> | <one line> |
| Issue type | <Feature | Bug | Test> | derived from the mode and the area by the rule in `refs/labels.md` |
| Complexity | <Simple | Medium | Complex> | follows depth (quick = simple, standard = medium, deep = complex) |
