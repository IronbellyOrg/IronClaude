# Flags decision

- Decided by: user (taken as given); deep adversarial check against issue-worker-t1's independent variant found no disagreement (`adversarial/diff-analysis.md`)
- Depth: deep

| Field | Value | Reason |
|---|---|---|
| Mode | bug | passed as `--mode bug`; the independent T1 variant also picks bug |
| Type | skill | passed as `--type skill`; the independent T1 variant also picks skill (sc-issue-protocol) |
| Issue type | Bug | derived from the mode and the area by the rule in `refs/labels.md` |
| Complexity | Complex | follows depth (quick = simple, standard = medium, deep = complex) |
