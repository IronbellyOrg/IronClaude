# Re-review 4 (changed lines plus prior findings), reflect-reviewer opus: verdict ready, 0 blocking, confidence 0.8

All 15 prior findings (R1 to R4, N1, N3 to N12) resolved, none regressed.

New findings, all Medium or Note (not repaired):
- M1 Medium: `restore` removes only added lines, so it cannot undo `archive` rewriting `unresolved: []` or `mark` replacing a `superseded_by` line; the byte-identical restore criterion cannot be met for those contracts. Fix: store the original contract bytes in `archive-undo.txt`.
- M2 Medium: the "already superseded" check reads the whole file; it matches after `superseded_by` is written, and matches a contract that only mentions another package as superseded (blockerStage4-20261117-170451). Fix: match only `unresolved` items that start with "superseded", check before writing `superseded_by`, test the known-id case.
- M3 Medium: routes none, escalate and forced have no writer for `remediation_route` and `finding_counts`; Task 8 promises "recorded as forced".
- M4 Medium: `archive` moves, then edits the contract; a failure after the move strands the package in `archive/`. Fix: edit first, or call `restore` on failure.
- Na Note: constraint says archived contracts are edited "by appending lines"; Task 4 replaces, inserts and removes lines. Nb Note: a failed `prepare` is not a `release` trigger in Task 4. Nc Note: Task 13's grep check can fail if this package's own contract text says "superseded".

Not run: blind calibration, adversarial merge, evidence validator.
