# HO-3 notes

Plan sha256 81cf9cc6... equals the plan hash in the report's input-snapshot.yaml and the ledger; the report's `plan:N` cites (:34, :49, :64, :101, :105-107, :119, :124, :128, :130-133, :153, :162) were checked against the copied plan and match. The plan stays as written (reflect is advisory).

## Included (12)
B-1..B-6 (blocking, GT1-GT6) and M-1..M-6 (GT7-GT12, `blocking_in_implement: false`).
- B-2, B-3, B-4, B-5, M-2, M-5 are marked "design first" in the report: the same defect sits in source.md and the plan copies it. They are kept because an implementer who follows the plan as written builds the wrong thing, and the plan quote anchors it.
- The implementation-time review records (artifacts/retries/T5, T6, T7 review-1.md, blocking) concern code the implementation wrote (ac-selector name, remedy text, hand_command output). They are not plan defects and map to no item.

## Dropped
- m-1..m-7 and A-1..A-3: LOW findings (Orca dependency in Constraints, Task 2 size, lint timing, Task 8 placement, pending store growth, tests/docs, ASCII routing row, directory modes, `launched_at` name, -k filter). Kept out to hold the set strict.
- m-8: the report itself says "nothing diverged" (addressed).
- Rejected-or-withdrawn table rows in the report (Regression label, ARG-1/LA-7 overstated, Wave 6 overlap, lint gate, INV-001 premise, green-between-tasks).

## Base
`start sha=63bc2f2d...` is a tree object. Base = HEAD in artifacts/retries/T1/q0-head: e8db2fe660d9104cbe8cdbcdc6f2c967f4994f4b (commit; ancestor of implementing commit f8305000b). The plan folder is not tracked at that commit (present only in the tree snapshot). masked_paths: [] (no file added by the implementation exists at base).
