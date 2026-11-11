# Revise report: gate review, B-01

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Blocking ids from the gate Reviser brief (`review/gate.md:166-168`): B-01. No PASS is claimed.

## Byte accounting

Candidate size before: 57939 bytes. After: 58817 bytes. Net +878 (matches the per-line sum below). Line count unchanged (286). Per-line figures are line-level before to after bytes; the edits are in-place replacements, so net per line is shown (gross added and deleted are not separable without a character diff, which was not run).

| Finding | Line (after) | Before | After | Net |
|---|---|---|---|---|
| B-01 | 62 (WC-4) | 1210 | 1364 | +154 |
| B-01 | 73 (2.3) | 511 | 635 | +124 |
| B-01 | 76 (section 3 intro, "Contract" definition) | 431 | 479 | +48 |
| B-01 | 83 (adversarial) | 316 | 333 | +17 |
| B-01 | 85 (cleanup-audit) | 313 | 393 | +80 |
| B-01 | 87 (init-lite) | 209 | 256 | +47 |
| B-01 | 90 (tdd) | 336 | 383 | +47 |
| B-01 | 92 (workflow) | 307 | 508 | +201 |
| B-01 | 182 (7.2 step 3) | 274 | 307 | +33 |
| B-01 | 198 (AC-1.4) | 242 | 314 | +72 |
| B-01 | 200 (AC-2.2) | 355 | 410 | +55 |
| total | | | | +878 |

Line 76 is outside the line list in the Reviser brief but carries the same `<output-dir>/return-contract.yaml` generalisation (a third statement of it), so it was changed to keep WC-4 and section 3 from contradicting. Step 4 of 7.2 (`SPEC:183`) needed no edit: it uses `<contract>`, which step 3 now defines.

## Findings

| Id | Disposition | Where applied |
|---|---|---|
| B-01 | Applied | See below |

B-01 had three sub-defects (`gate.md:89-93`):

1. File-valued `--output` (tdd, init-lite): the contract path rule is now "parent directory of that file" in WC-4 (`SPEC:62`) and in both rows (`SPEC:87`, `:90`); AC-2.2 states the expected location (`SPEC:200`).
2. adversarial: the Report column now names `<output>/adversarial/return-contract.yaml` (`SPEC:83`); AC-1.4 (`SPEC:198`) checks that exact path. The `<output-dir>/return-contract.yaml` generalisation is deleted from WC-4 and the section 3 intro (`SPEC:62`, `:76`).
3. workflow and cleanup-audit: cleanup-audit gets the fixed `.claude-audit/return-contract.yaml` (`SPEC:85`; fixed directory per `INV-A:42`). workflow keeps `.dev/tasks/to-do/<id>/return-contract.yaml`, whose real path the worker returns in `worker_done --report-path` (the existing WC-4 last sentence, `SPEC:62`); pre-creation stops (`INV-B:272`) write `.dev/tasks/to-do/return-contract.yaml` (`SPEC:92`). Decision for the author: that fallback path is a choice of this revision, not taken from any inventory line (`INV-B:272` only says the file is not written for pre-creation stops); it collides if two workflow workers stop before creating a package, and this was not mitigated, to avoid adding a mechanism.

Coordinator side: 2.3 (`SPEC:73`) and 7.2 step 3 (`SPEC:182`) now read the path from the section 3 Report column (the gate's recommendation, `gate.md:94`), with workflow's path taken from `worker_done`.

Left untouched: M-01 to M-13 and minor notes, per the brief. The gate-report line citations (`gate.md:*`) and spec/inventory lines above were checked in the workspace; the `command.md:460` corroboration in the gate report is UNVERIFIED (outside the workspace).
