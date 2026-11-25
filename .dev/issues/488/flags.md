# Flags decision

- Decided by: issue-worker-t2
- Depth: quick

| Field | Value | Reason |
|---|---|---|
| Mode | feature | Requests a new Tier 3 preference order (GLM-5.3 first, GPT-6.1 Terra fallback), not a reported failure of existing behavior. |
| Type | skill | Tier 3 routing belongs to the ccsession-tag skill: ccsession-models.json references ordered T3Model environment slots, and MODEL-TIERS.md currently documents Terra first. |
| Complexity | simple | follows depth (quick = simple, standard = medium, deep = complex) |
