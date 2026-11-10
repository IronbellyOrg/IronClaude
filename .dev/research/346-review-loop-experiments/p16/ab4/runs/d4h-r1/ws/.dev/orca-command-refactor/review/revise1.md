review: 1 of 3 (revision 1; no review reply written in this file)

# Revise 1 of the orca-worker-contract spec

Input: `.dev/orca-command-refactor/review/round1.md` (merged first review, verdict FAIL, Reviser brief lists M1, M2, M3, M4, M5, M6, M7, M8, M10, M11).
Candidate before revision: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (matches the `candidate:` line of round1.md:5).
Candidate after revision: same path, sha256 `84aa3fdce83498845e1a3cf58e05e4b1f83a15e38b34520e6f0393658bd74d26`.
Scope: only the ids in the brief. M9 (rejected by VF1, round1.md:11 and :102-109) is not in the id list and was not touched. No Medium or minor finding was changed. The spec-panel was not run. The candidate was not given a PASS.

## Byte accounting

Size before: 57763 bytes (`wc -c`). Size after: 60183 bytes. Net +2420.

Method: each Edit counted in bytes (UTF-8, `wc -c` of the old and new text). A pure insertion counts only as added. A replaced span counts its old text as deleted and its new text as added. Totals reconcile: added 3471, deleted 1051, net 2420.

| Edit (spec line before, section) | Ids | Added | Deleted | Note |
|---|---|---|---|---|
| WC-4 row, path sentence (line 62) | M1 | 370 | 0 | insertion |
| WC-4 row, load and workflow sentences (line 62) | M10 (88), M11 (325) | 413 | 0 | insertion; split 88 to M10 and 325 to M11 |
| Section 3 intro "Contract" meaning (line 76) | M1 | 71 | 67 | replaced span |
| Section 2.3 brief content (line 73) | M2 | 36 | 0 | insertion |
| WC-5 outcome mapping (line 63) | M3 | 322 | 211 | replaced span |
| WC-11 parallel-safe writes (line 69) | M4 | 142 | 74 | replaced span |
| Section 3.1 workflow row (line 92) | M11 | 31 | 0 | insertion |
| Section 3.2 load row (line 112) | M10 | 36 | 23 | replaced span |
| AC-0.4 (line 194), step 4 and P0 pass clause | M5 | 253 | 105 | shared edit with M2 and M7 |
| AC-0.4 (line 194), P0 brief clause | M2, M7 | 197 | 0 | shared edit with M5 (the 105 deleted bytes are counted once, under M5) |
| Section 7.2 step 5 (line 184) | M7 | 378 | 173 | replaced span |
| Section 7.2 step 6 (line 185) | M6 | 320 | 129 | replaced span |
| AC-1.1 (line 195) | M10 | 20 | 0 | insertion |
| AC-1.2 (line 196) | M10 | 20 | 0 | insertion |
| AC-2.2 (line 200) | M8 | 821 | 269 | replaced span |
| Decisions table, load row (line 265) | M10 | 41 | 0 | insertion |

Per finding id:

| Id | Added | Deleted |
|---|---|---|
| M1 | 441 | 67 |
| M2 | 36 + 197 (shared with M7) | 0 |
| M3 | 322 | 211 |
| M4 | 142 | 74 |
| M5 | 253 | 105 (shared) |
| M6 | 320 | 129 |
| M7 | 378 + 197 (shared with M2) | 173 |
| M8 | 821 | 269 |
| M10 | 88 + 36 + 20 + 20 + 41 = 205 | 23 |
| M11 | 325 + 31 = 356 | 0 |

Check: added 441+36+322+142+253+320+378+821+205+356 + 197 (the shared M2/M7 part counted once) = 3471. Deleted 67+211+74+129+173+269+23+105 = 1051. Net 2420 = 60183 - 57763.

## Findings

| Id | Status | Where applied (revised file) | What changed |
|---|---|---|---|
| M1 | applied | WC-4 row, line 62; section 3 intro, line 76 | WC-4 names the default path and lists the rows that name another path: adversarial `<output>/adversarial/return-contract.yaml` (row line 83), cleanup-audit fixed `.claude-audit/`, init-lite and tdd `--output` file, cli-portify named before its live check. Line 76 now says "the path WC-4 or the row names". |
| M2 | applied | Section 2.3, line 73; AC-0.4, line 194 | Brief carries `--unattended` from P1 on; P0 briefs omit it. AC-0.4 states the P0 test is limited to launch and top-level run, with WC-2 first tested in AC-1.2 (line 196). |
| M3 | applied | WC-5, line 63 | `succeeded` only for a parsed contract with status `succeeded` or `partial`. Every other case (failed, blocked, no report, empty or unparseable contract, unknown status) is `failed`. The audit-FAIL-is-succeeded rule is kept. |
| M4 | applied | WC-11, line 69 | The timestamp or slug rule is limited to `--unattended`; standalone defaults are unchanged (SA-1, line 146). |
| M5 | applied | AC-0.4, line 194 | P0 step 4 is `test -s` on the command's existing report file (for troubleshoot `REPORT.md`, `INV-B:49`). The YAML field check is not run in P0. The workflow contract has no `command` key (`INV-B:272`, which lists `status`, `plan_path`, `reflect_report_path` only). |
| M6 | applied | Section 7.2 step 6, line 185 | Compare `git status --short` before dispatch with the one after the worker settles. Pass only for new entries under the output directory or the command's documented artifacts. The phase's own pre-dispatch edits are not counted. |
| M7 | applied | Section 7.2 step 5, line 184; AC-0.4, line 194 | Step 5 also searches for Agent or Task tool-use events whose prompt is the `/sc:` command line (WC-7). The field that holds the tool name is UNVERIFIED: a search of `orca-capabilities.md` for "transcript" found no tool-name field (`orca-capabilities.md:131` and `:140` give only the `--source` options). |
| M8 | applied | AC-2.2, line 200 | Scope narrowed to the nine P2 commands with a blocked path in their section 3.2 rows (cli-eval, tdd, troubleshoot, task, recommend, review-translation, release-split, spec-panel, cli-portify), each with its trigger input. The six with a documented default (auggie-review, cleanup, improve, research, reflect, tasklist) run AC-2.3 and record the default in the contract. Trigger inputs are taken from the section 3.2 rows (`cmd/` and `sk/` citations as given there); they were not re-read in the inventories. |
| M10 | applied | WC-4, line 62 (load exempt); section 3.2 load row, line 112; AC-1.1, line 195; AC-1.2, line 196; Decisions table load row, line 265 | `load` is exempt from WC-4 and writes no contract; the decision row now says WC-4 exempts it. AC-1.1 and AC-1.2 exclude `load`. |
| M11 | applied | WC-4, line 62; section 3.1 workflow row, line 92 | Workflow gets `--output <dir>` in P1. A pre-creation STOP writes `<output-dir>/return-contract.yaml`. After package creation the same contract is also written to `.dev/tasks/to-do/<id>/return-contract.yaml`; the inventory says it is not written for pre-creation STOPs, `INV-B:272`), and the `<output-dir>` file lists it under `artifacts`. The coordinator always reads the `<output-dir>` file. |

## Notes

- The brief asks for `review/revise1.md`; `review/README.md` shared context names `review/disposition.md` for the Revise step. The file was written under the brief's name.
- Citations added in this revision that were checked against the inventories: `INV-B:49` (troubleshoot writes `REPORT.md`, `report_path`), `INV-B:272` (workflow contract fields, package path, no pre-creation contract) and `INV-A:35` (adversarial real runs wrote `<output>/adversarial/return-contract.yaml`). Other citations added (`cmd/` and `sk/` paths in the section 3.2 rows) are carried from the existing rows and were not re-read here, marked UNVERIFIED where they are the only support.
- UNVERIFIED: the transcript field that holds the tool name (M7); whether the workflow contract has a `command` key (M5, already marked UNVERIFIED in the inventory at `INV-B:272`); the cli-portify contract location, which the spec now leaves to P2 (M1).
- No review reply was written; the VERIFY step and the next re-review are the coordinator's.
