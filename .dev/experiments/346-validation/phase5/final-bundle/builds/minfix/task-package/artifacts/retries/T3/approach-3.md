Implementer claims (not verified by review):
- Followed brief 3 (advice-3-a): span edits on the revised text, no whole-file safety net except the raw-size case, depends closure over entries with no kept hunk.
- Deviation from brief 3 step 4: instead of per-run line rules, each diff region holding a reverted part is composed again (kept parts give revised units, reverted parts baseline units) and replaces exactly that region's span; separators at junctions split at the first line break (end of the previous line from the emitted neighbour, break and prefix from the unit's own file); regions without reverted parts stay byte for byte.
- A kept finding whose part must go back with a moved unit is reverted whole and listed.
- Property test rewritten: table between paragraphs, edits on rows and cells and line starts, asserts every kept hunk's revised slice survives; 18,000 extra cases on four document shapes passed (artifacts/t3-extra-seeds.txt).
- Believed T3.AC1-AC4 met; the reviewer found that a whitespace-only change of a unit's kind (fence join, row prefix cut) sits in an equal region and is never restored, so --enforce exits 1.
