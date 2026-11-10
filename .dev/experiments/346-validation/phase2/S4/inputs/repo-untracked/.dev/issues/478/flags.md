# Flags decision

- Decided by: issue-worker-t2
- Depth: quick

| Field | Value | Reason |
|---|---|---|
| Mode | bug | The description reports existing bundled tools missing their expected default availability across projects, rather than requesting a new tool. |
| Type | install | The request concerns image/catalogue installation scope and first-use project initialization; BMAD's existing installer initializes only the seed repo, while Ponytail's source is not established yet. |
| Complexity | simple | Follows the requested quick depth (quick = simple), not an independently verified implementation estimate. |
