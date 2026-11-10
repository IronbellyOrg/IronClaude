# Revise 1

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place. Blocking ids repaired: M2, M3, M4, M5, M6, M7 (the ids in `review/round1.md:105`). M1 and M8 were rejected by the verifier (`review/round1.md:11`) and are untouched. Medium and minor findings are untouched. No PASS is awarded. No line was added or removed, so the line numbers cited in `review/round1.md` still hold.

## Byte accounting

Before: 57763 bytes. After: 59200 bytes (sha256 e08236b563e957f919d430bee09f668cc4d154a475a77554660dd7026ed73de4). Net +1437. Total over the 17 edits: 1511 bytes of old text deleted, 2948 bytes of new text added, which nets to +1437.

Method: each edit replaces one exact string (asserted to occur once), and the table counts the full length of the replaced string and of its replacement, not a character diff. A shared edit is listed once and not split between ids.

| Edit | Spec location (line numbers unchanged) | Ids | Deleted | Added |
|---|---|---|---|---|
| 1 | WC-4 path sentence, line 62 | M2, M5, M6 | 166 | 429 |
| 2 | Section 2.3, line 73 | M5 | 72 | 85 |
| 3 | Section 3 intro "Contract means", line 76 | M2, M4 | 100 | 124 |
| 4 | adversarial row, line 83 | M6 | 77 | 116 |
| 5 | cleanup-audit row, line 85 | M5 | 105 | 179 |
| 6 | index-repo row, line 86 | M5 | 30 | 117 |
| 7 | workflow row, "Brief must pass", line 92 | M5 | 78 | 107 |
| 8 | workflow row, small fix, line 92 | M5 | 73 | 247 |
| 9 | spec-panel row, line 120 | M5 | 66 | 77 |
| 10 | load row, other change, line 112 | M4 | 52 | 106 |
| 11 | P1 scope, line 159 | M4 | 111 | 130 |
| 12 | 7.2 step 4, line 183 | M2, M5 | 27 | 43 |
| 13 | AC-0.4, line 194 | M3 | 105 | 292 |
| 14 | AC-1.1, line 195 | M4 | 172 | 202 |
| 15 | AC-1.2, line 196 | M4, M2, M5 | 70 | 169 |
| 16 | AC-2.2 check cell, line 200 | M7 | 79 | 126 |
| 17 | AC-2.2 pass cell, line 200 | M7 | 128 | 399 |

Per finding id, counting only the edits that serve that id alone:

| Id | Edits (own only) | Deleted | Added | Shared edits that also serve it |
|---|---|---|---|---|
| M2 | none | 0 | 0 | 1, 3, 12, 15 |
| M3 | 13 | 105 | 292 | none |
| M4 | 10, 11, 14 | 335 | 438 | 3, 15 |
| M5 | 2, 5, 6, 7, 8, 9 | 424 | 812 | 1, 12, 15 |
| M6 | 4 | 77 | 116 | 1 |
| M7 | 16, 17 | 207 | 525 | none |
| shared edits (1, 3, 12, 15) | | 363 | 765 | |

The own-only rows plus the shared row add up to the totals: 1511 deleted, 2948 added.

## One row per finding id

| id | disposition | where applied | reason, with citation |
|---|---|---|---|
| M2 | applied | Edit 1 (WC-4, line 62); edits 3, 12, 15 (lines 76, 183, 196) | The text `<output-dir>/return-contract.yaml` could not be built where `--output` names a file (tdd line 90, init-lite line 87; `review/round1.md:25`). WC-4 now gives three cases: directory gives `<dir>/return-contract.yaml`, file gives `<file>.return-contract.yaml`, and a fixed path named in the section 3 row overrides both. The section 3 intro, the 7.2 step 4 `<contract>` and AC-1.2 now point to that path. AC-2.2's `/sc:tdd ... --output <file>` run (line 200) now has a defined contract path, so it is unchanged. |
| M3 | applied | Edit 13 (AC-0.4, line 194) | `review/round1.md:34` says only step 4 was carved out. The cell now carves out step 3 as well: report path and `status` come from the command's existing report file, `REPORT.md` for troubleshoot (line 91) and the `<id>` path for workflow (line 92), with `<id>` read from the `worker_done` report path. The WC-4 check starts in P1. The "reopens section 1" sentence is kept, because the gate no longer fails by construction. |
| M4 | applied | Edit 14 (AC-1.1, line 195), edit 15 (AC-1.2, line 196), edit 11 (P1 scope, line 159), edit 10 (load row, line 112), edit 3 (line 76) | Line 112 and Decisions line 265 say load gets no report and is not its own Task (`review/round1.md:40`). Following the narrowing option in the revise prompt, `load` is now excepted from the `## Unattended mode` section, the contract and the AC-1.2 live check. It keeps its P1 usage-line fix. AC-1.1 also asserts that load has no such section. The Decisions text at line 265 was not edited, since it already says the same. |
| M5 | applied | Edit 1 (WC-4), edit 2 (line 73), edits 5, 6, 7, 8 (cleanup-audit, index-repo, workflow rows), edit 9 (spec-panel, line 120), edits 12, 15 | Each command named in `review/round1.md:48-54` now has a stated contract path known before dispatch. cleanup-audit: `.claude-audit/return-contract.yaml`. The fixed `.claude-audit` directory is shown by `pass1-summary.md` at `INV-A:107`. index-repo: `PROJECT_INDEX.md.return-contract.yaml` beside the index. Its location is only implied, UNVERIFIED (`INV-A:53`, `INV-A:117`). workflow: a new `--output <file>` with the contract at `<file>.return-contract.yaml` on every outcome, so the unknown package `<id>` (`INV-B:272`, `INV-B:274`) no longer matters. The existing package contract is unchanged. tdd and init-lite: covered by the file case in WC-4. spec-panel: `--output <dir>`, a directory. The new flag for workflow is the only flag added beyond what P1 scope already allows ("output flags for commands that lack one", line 159). |
| M6 | applied | Edit 4 (adversarial row, line 83); edit 1 | WC-4's override clause now states that a fixed path in the section 3 row, such as `<output>/adversarial/return-contract.yaml`, is the WC-4 path for that command (`review/round1.md:62`). The adversarial row keeps its filename and says so. 7.2 step 3 therefore compares against the same file the worker reports. AC-1.4 (line 198) still holds. |
| M7 | applied | Edits 16 and 17 (AC-2.2, line 200) | `review/round1.md:75` shows that research, auggie-review, cleanup, improve, tasklist and reflect have no blocked path. AC-2.2 now applies the blocked run only to P2 commands whose row resolves a gate as blocked. For the six commands that resolve by default or deferral, the pass condition is that the stated default or deferral applies, step 2 never shows `agentWait`, and `--outcome` matches the contract's `status`. |

## Notes for the next review

- Check each added bracket tag `[M2]` through `[M7]` in the spec. They exist to cite the finding id on every addition, and the coordinator may strip them after the loop ends.
- Citations I could not check inside this workspace: the command and skill files cited as `cmd/` and `sk/` are not in the sandbox, so the facts I reused come only from the inventories (`INV-A:42,53,107,117`; `INV-B:272,274`). The `index-repo` location and the `workflow` flag surface are therefore UNVERIFIED against the source files.
- The edits kept line numbers stable. `review/round1.md` and `review/verify-1.md` still cite the right lines.
- I left Decisions line 265 (load) and section 4 unchanged.
