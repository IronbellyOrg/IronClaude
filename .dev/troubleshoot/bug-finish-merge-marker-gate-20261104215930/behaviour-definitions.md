| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | git merge (conflict-marker-size attribute) | writes conflict markers at the attribute's width | observed in this run (tier1-observation.md ## Probe, probe-finish.out:2) | n/a (observed) | observed:probe-finish.out:2 |
| 2 | git blob id | excludes the file mode | observed in this run (mode-only change passed the blob-id comparison and was committed) | n/a (observed) | observed:probe-finish.out:6-9 |
| 3 | git diff --cached --name-only <tree> | lists mode-only differences | observed in this run | n/a (observed) | observed:probe-finish.out:6 |
