observation-kind: string
producer-count: 0 (repo)

The observed strings ("API Error: Connection lost mid-response", "Connection refused ... (ECONNREFUSED)") are emitted by Claude Code's HTTP client, not by this repository (`grep -rn` over src/: 0 hits, tier1-observation.md O11). Grep hit count 0 = row count 0. The observation is not a categorical enum produced in-repo, so no producer menu applies; the repo-side condition (shim process exits) is covered by the execution-locus card and tier1-observation.md O2/O7/O8/O10.

## Producers

| id | line | statement | exit statement | before/after started marker | wall-time compatible | cheap observable | surviving |
|---|---|---|---|---|---|---|---|
