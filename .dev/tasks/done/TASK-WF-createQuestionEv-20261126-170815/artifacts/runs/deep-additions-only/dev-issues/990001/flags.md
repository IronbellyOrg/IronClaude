# Flags decision

- Decided by: user (taken as given); deep check by issue-worker-t1 and `sc:adversarial --compare flags-user.md,flags-t1.md --depth quick` (merged view: `flags-merged.md`)
- Depth: deep

| Field | Value | Reason |
|---|---|---|
| Mode | feature | passed as `--mode feature`; issue-worker-t1 chose the same (new output, nothing described as broken) |
| Type | cli | passed as `--type cli`; filed as given. issue-worker-t1 chose `install`; the debate left the point unresolved (X-001), so the difference goes to the pushback comment |
| Issue type | Feature | derived from the mode and the area by the rule in `refs/labels.md` (same for `cli` and `install`) |
| Complexity | Complex | follows depth (quick = simple, standard = medium, deep = complex) |
