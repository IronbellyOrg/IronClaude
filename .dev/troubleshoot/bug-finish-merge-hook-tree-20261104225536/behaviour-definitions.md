| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | git commit with a pre-commit hook | commits the index as the hook left it, including files the hook staged | observed in this run (probe-c4.out:3-5) | n/a (observed) | observed:probe-c4.out:3-5 |
| 2 | git write-tree | writes the current index as a tree object and prints its id, without changing the index, HEAD or any ref | git documentation (git-write-tree); used by the proposed fix, verified by its regression test | n/a | unobserved:verified by the fix test |
