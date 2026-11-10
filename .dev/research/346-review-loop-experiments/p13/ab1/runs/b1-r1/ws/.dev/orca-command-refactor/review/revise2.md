# Revise 2: blocking findings L1, L2, L9

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place. Source of the ids: `.dev/orca-command-refactor/review/round2.md:96-100` (Reviser brief: "Blocking finding ids: L1, L2, L9"). The sub-claims per id come from `round2.md:30-60` (ledger anchors) and `round2-t1b-1.md:69-127`. Line numbers below are of the revised spec. No self-awarded PASS; the spec-panel was not run; only the spec and this file were written.

## Byte accounting

Spec size: before 60365 bytes (`wc -c`), after 60803 bytes (`wc -c`), net +438. Added and deleted are bytes of changed text per id (character-level diff per edited line).

| Finding id | Bytes added | Bytes deleted | Net |
|---|---|---|---|
| L1 | 271 | 5 | +266 |
| L2 | 106 | 0 | +106 |
| L9 | 66 | 0 | +66 |
| Total | 443 | 5 | +438 |

The net equals the file-size change, so no byte is unattributed.

Note on scope: `round2-t1b-1.md:115-127` grades M2-M10 Medium (non-blocking), but the merged ledger (`round2.md:30-60`) attaches M2, M3, M5, M8 to L1, M4 to L2 and M10 to L9 as anchored sub-claims. I treated the ledger as authoritative for what each blocking id names, and repaired each with the smallest narrowing; no other Medium or minor finding (L3-L8, L11-L20, M1, M6, M7, M9) was touched.

## Finding rows

| Id | Sub-claim | Disposition | Where | Reason |
|---|---|---|---|---|
| L1 | N1 (P1 scope and AC-1.2 require `--unattended` for `load`) | applied | Spec 159 (P1 row), 196 (AC-1.2) | Both now say "other than `load`", matching the load row (spec 112), section 6 intro (154) and AC-1.1 (195). +36 bytes. |
| L1 | M3 (post-release missing `--output`: blocked vs failed) | applied | Spec 113 | Row now says a missing `--output` follows WC-4 (worker ends `failed`) and a missing pre-tag choice is blocked with the contract in `--output`; the two texts no longer give different outcomes for one input (WC-4 at spec 62). +71 bytes. |
| L1 | M8 (WC-3 names an answer flag most blocked rows lack) | applied | Spec 61 (WC-3) | Where the section 3 row names no flag, the answer travels as text in the new Task's brief. Narrowing, no new mechanism. +49 bytes. |
| L1 | M5 (existing status values unchecked; brainstorm "None") | applied | Spec 62 (WC-4), 84 (brainstorm row) | The value sets stay UNVERIFIED (not in the sandbox inventories: `INV-A:97` only says brainstorm writes a named contract, not its status values), so the brainstorm row now carries the mapping in P1 instead of "None". +111 bytes. |
| L1 | M2 (spec-panel has a file-valued `--output` and own `--report-dir` contract) | rejected | none | The only checkable evidence contradicts the claim: `INV-B:43` and the spec-panel entry in `INV-B` (d) say "no path or `--output` flag exists" (`cmd/spec-panel.md:22,222`), so the spec-panel row "add `--output`" is consistent with the inventory. The reviewer's citation (`command.md:22-24,460-461`) is not a file in the workspace: UNVERIFIED. |
| L2 | M4 (troubleshoot has no brief-named output path for fresh-dir re-runs) | applied | Spec 64 (WC-6) | WC-6 now says a command with no output flag (troubleshoot) re-runs into its timestamped default directory, which is new per attempt (`INV-B:237-240` area: default `.dev/troubleshoot/<slug>-<timestamp>/`, `cmd/troubleshoot.md:56`). +106 bytes. |
| L9 | M10 (AC-C1 exempts whole files, SA-2 allows only an Orca section) | applied | Spec 147 (SA-2) | SA-2 now states that AC-C1 excludes `HOW-WE-WORK.md` whole and that AC-0.3 guards its existing rows, so the text and the check agree; no new check added. +66 bytes. |

## Fix map

```fixmap-v1
{"id": "L1", "action": "applied", "reason": "N1 (load excluded from the P1 flag scope and AC-1.2), M3, M5 and M8 narrowed at spec 159, 196, 113, 61, 62, 84; M2 rejected because INV-B shows spec-panel has no --output flag and the reviewer's citation is UNVERIFIED."}
{"id": "L2", "action": "applied", "reason": "M4: WC-6 now names troubleshoot's timestamped default directory as its fresh path (spec 64)."}
{"id": "L9", "action": "applied", "reason": "M10: SA-2 now states the file-level AC-C1 exclusion and the AC-0.3 guard (spec 147)."}
```
