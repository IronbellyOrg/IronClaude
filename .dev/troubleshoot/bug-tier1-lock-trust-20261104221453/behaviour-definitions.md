| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | `uv lock` with `[build-system] backend-path` and `[project].dynamic` | imports the in-tree build backend to get metadata | observed in this run (probe-lock-trust.out:5, "in-tree backend executed: yes") | n/a (observed) | observed:probe-lock-trust.out:6 |
| 2 | `uv lock` with a `[tool.uv.sources]` path or editable source | builds the local package's metadata (runs its backend) | uv resolver behaviour; not probed here | n/a | unobserved:owner trigger list |
| 3 | Python `tomllib` | stdlib TOML parser on Python >= 3.11 only | Python docs (3.11 "What's New"); runtime here 3.11.15, floor 3.10 | n/a | unobserved:guarded import, missing parser halts |
