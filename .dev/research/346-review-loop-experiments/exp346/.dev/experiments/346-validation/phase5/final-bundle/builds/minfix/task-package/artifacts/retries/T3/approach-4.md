Implementer claims (not verified by review):
- Followed brief 4 (advice-4-a): ported attempt 3 and changed diff_hunks and the moved-unit pool to match units on (kind, norm); added the fence-join, row-cut and heading-join tests and a plain-check row-cut test; the property base gained a fence and join/cut edits.
- Deviation beyond brief 4: added a structure loop in enforce (when the composed text still fails the in-memory check, revert one kept finding whole, fence-count changers first, then by position, and compose again), reported as structure=<ids>; a probe showed a kept fix opening an unmatched fence made --enforce exit 1.
- 76 tests passed; 16,000 extra fuzz cases (artifacts/t3-extra-seeds.txt) exited 0 with kept slices surviving.
- The reviewer found the structure loop can revert an in-budget fix when an undeclared fence unit is charged to that fix by the neighbour rule.
