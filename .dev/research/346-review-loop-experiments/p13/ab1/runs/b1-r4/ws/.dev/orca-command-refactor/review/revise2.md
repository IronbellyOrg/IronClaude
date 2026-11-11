# Revise 2 (blocking ids L1, L2, L5, L17)

Source of findings: `.dev/orca-command-refactor/review/round2.md` (Reviser brief) and `review/round2-t1b-1.md` (R2-1, R2-2, R2-3, R2-4, R2-6 and L1 of AC-0.4). Evidence checked: `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md` (INV-A / INV-B cited below); no citation here is outside the workspace.

## Byte accounting (file `specs/orca-worker-contract-spec.md`)
- Before: 60019 bytes. After: 60761 bytes. Net +742.
- Counted per whole changed line (a table row is one line, so deleted and added include the unchanged part of the row). Net is exact; per-id split of lines 198-199 is shared between L2 (AC-0.3) and L17 (AC-0.4).

| id | spec lines (after) | deleted | added | net |
|---|---|---|---|---|
| L1 | 62 (WC-4), 87 (init-lite row), 92 (workflow row), 208 (AC-1.4) | 1691+220+308+243 = 2462 | 2078+241+332+142 = 2793 | +331 |
| L2 | 176 (AC-C5), 181 new fenced block (in the 176-181 span), AC-0.3 row (in 203-204) | 280 (plus AC-0.3 part of 643) | 431 (plus AC-0.3 part of 677) | about +185 |
| L5 | 52 (2.1), 76 (section 3 intro) | 550+432 = 982 | 568+454 = 1022 | +40 |
| L17 | 192-193 (7.2 steps 3 and 4), AC-0.4 row (in 203-204) | 601 (plus AC-0.4 part of 643) | 787 (plus AC-0.4 part of 677) | about +186 |

## Finding table
| id | disposition | where and why |
|---|---|---|
| L1 / R2-1 | applied | WC-4 (spec line 62) now says each worker gets its own output directory and two workers never share one, citing WC-11 (line 69 "Two workers in one worktree must never write the same file", unchanged). The init-lite row (line 87) now says `--output` file "in a fresh directory per attempt" so a retry does not overwrite the first contract (WC-6). |
| L1 / R2-2 | applied | WC-4 now names the three commands with no output flag (cleanup-audit, index-repo, troubleshoot; `INV-A:42`, `INV-A:53`, `INV-B:242`) and has them write the contract into the directory of the report their 3.1 row names, the coordinator learning the path from `worker_done --report-path`. Any other command given no output stops and writes no contract; the worker ends `failed` under WC-5. The "stops before any other output exists" wording is narrowed to "as long as its directory exists". D1's `--output` example for troubleshoot is round-1 L7, a non-blocking id, and was left alone. |
| L1 / R2-6 | applied by narrowing | WC-4's "existing contract's own status values are mapped to these" (no mapping given) is replaced by "keeps its own status field and adds `status` with these values beside it", which needs no mapping. The workflow row's "Write the contract for pre-creation STOPs too" (line 92) is deleted: a STOP before the package id exists has no directory (`INV-B:267-275` puts the contract under `.dev/tasks/to-do/<id>/`), so no contract is written and WC-5 gives `failed`. AC-1.4 (line 208) no longer asserts the workflow clause. |
| L2 / R2-4 | applied | AC-C5 and AC-0.3 no longer hold `\|` inside table cells. Both now point to a fenced `bash` block (AC-C5 command, placed after the 7.1 table beside the AC-C1 block) written with plain `|`; AC-0.3 reuses it with the HOW-WE-WORK path. AC-C4 (line 175) has the same escaped-pipe form but is not named by L2 and was left alone. |
| L5 / R2-3 | applied | Section 2.1 (line 52) and the section 3 intro (line 76) now read "Each/Every changed command except `/sc:load`", agreeing with the P1 row "load (usage line only, no section)" (line 159, unchanged), AC-1.1 (line 200, unchanged) and the Decisions row for `/sc:load`. |
| L17 / L1 of AC-0.4 | applied | 7.2 step 4 now runs the YAML assertion from P1 only; in P0 it is `test -s` on the command's existing report file, since troubleshoot's `REPORT.md` is markdown (`INV-B:237-245` lists it as `REPORT.md`). Step 3's pass text states that in P0 there is no contract, so the outcome is `succeeded` and the path is the existing report file. The AC-0.4 pass cell now says step 4 is `test -s` only, with the YAML assertion arriving in P1, which removes the false reopening of section 1. |

## Not touched
Medium and minor findings (L3, L6-L16, R2-5, R2-7) and AC-C4's escaped pipes were left alone per the brief.

## Fix map
```fixmap-v1
{"id": "L1", "action": "applied", "reason": "WC-4 now requires a per-worker output directory, defines the contract location for commands with no output flag, drops the unspecified status mapping, and the workflow pre-creation clause is deleted."}
{"id": "L2", "action": "applied", "reason": "AC-C5 and AC-0.3 moved out of table cells into a fenced block with plain pipes so a raw copy runs the intended check."}
{"id": "L5", "action": "applied", "reason": "The general 'every changed command' sentences in 2.1 and section 3 now exclude /sc:load, matching the P1 row and AC-1.1."}
{"id": "L17", "action": "applied", "reason": "In P0 the 7.2 step 4 and step 3 checks use the command's existing report file with test -s; the YAML status assertion starts in P1."}
```
