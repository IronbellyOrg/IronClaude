Implementer claims (not verified by review):
- Followed brief 5 (refactor of advice-4-b): ported attempt 4; an unclaimed inserted fence or code unit is never charged to a neighbouring entry; the structure loop reverts only findings whose own hunks change the fence count.
- Added beyond brief 5: when the composed text still fails the in-memory check and no fence-changing finding is left, revert the kept findings the re-check names (reported as recheck=); a regression test from a fuzz case covers it.
- Property test asserts every revert has a stated reason, structure reverts only hit fence changers, and kept slices survive; 26,000 extra fuzz cases passed (artifacts/t3-extra-seeds.txt).
- The reviewer found an undeclared mid-text fence can still duplicate sentences or leave exit 1 (pairwise probe, 6 of 2,142), and that the diff_hunks docstring overstates which whitespace changes are detected (row and paragraph joins are not).
