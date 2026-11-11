# Revise 1 (REVISE prompt, ids M1, M2, M3, M4, M5)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (edited in place)
input report: .dev/orca-command-refactor/review/round1.md (Reviser brief, lines naming M1-M5 as confirmed)

## Byte accounting
- Before: 57763 bytes. After: 59220 bytes. Net +1457 (wc -c).
- Added 1602, deleted 145 (byte-level diff of each replaced span; 1602 - 145 = 1457, matches wc -c).
- Per finding id (an edit that serves several ids is counted under each; the totals above count each edit once):

| id | bytes added | bytes deleted | edits (spec lines after revision) |
|---|---|---|---|
| M1 | 804 | 85 | 62, 73, 76, 79 (via shared row), 83, 92, 95, 182, 196-197 |
| M2 | 615 | 60 | 76, 79, 154, 159, 195 |
| M3 | 615 | 60 | same edits as M2 (same defect, AC-1.1 vs load) |
| M4 | 405 | 12 | 61, 73, 200, 208 |
| M5 | 423 | 35 | 62, 95, 148, 196-197, 200 |

M2 and M3 share every edit, so their figures are identical, not additive.

## Findings

| id | disposition | where applied and why |
|---|---|---|
| M1 | applied | WC-4 (spec:62) now has one location rule: `<report-dir>/return-contract.yaml`, `--report-dir` a directory-valued flag the brief always passes, so the path never depends on a run-time id. Adversarial row (spec:83) no longer says `<output>/adversarial/...`; it names the same rule. Workflow row (spec:92) writes the pre-creation-STOP contract to `<report-dir>`, giving it a location without an id. Brief (spec:73) names the directory; section 3 intros (spec:76, 79, 95) and AC step 3 (spec:182) use the one path. Added flag follows the finding's own recommendation (round1.md M1.a "a coordinator-supplied `--report-dir`") and the finding calls for it. |
| M2 | applied | Narrowed, nothing new. P1 flag/section sentence (spec:159) now covers only the P1 Commands cell, `load` excepted; the cell (spec:159) adds brainstorm and init-lite, which section 3.1 had left in no phase, and drops "fixes to"; section 3.1 intro (spec:79) lists which phase adds each ready command's contract; spec:154 states a command gains flags and section only in the phase its row names, so P1 does not touch implement, post-release or pr-submit (consistent with D3, spec:162 P4 row). AC-1.1 (spec:195) restricted to the P1 cell minus `load`. |
| M3 | applied | Same edits as M2: `load` exempted in spec:76 ("`load` gains neither"), spec:159 and AC-1.1 (spec:195), matching the load row (spec:112, "none (see note)") and its Decision, with `INV-B:65` ("writes no file") as support. init-lite note: it is now named in the P1 cell (spec:159) and spec:79, so its "Small fix: None" row (spec:87) is consistent with AC-1.1/1.2. |
| M4 | applied | WC-3 (spec:61) now permits `ask` only when the brief says `on a blocked gate: ask`; without that line the session sends no `ask` and follows WC-5, so the default is deterministic stop-and-report. Section 2.3 (spec:73) makes the line part of the brief. AC-2.2 (spec:200) and AC-4.1 (spec:208) require the brief line `on a blocked gate: stop and report`, so their `worker_done --outcome failed` pass condition is reachable. Evidence unchanged: `CAPS:58,129` (an `ask`-blocked worker shows `agentWait`) as cited in round1.md M4.a. |
| M5 | applied | Same single rule as M1: `--output` stays file-valued for tdd (spec:90), init-lite (spec:87), spec-panel (spec:120) per `INV-B:222,225`, `INV-B:182,185`; the contract goes to `--report-dir`. AC-2.2 tdd example (spec:200) now passes both `--output <file>` and `--report-dir <dir>`; AC-1.2/1.3 and SA-3 (spec:148, 196, 197) use `--report-dir`. The reviewer's `command.md:460-461` citation is outside the evidence set and is UNVERIFIED here; the fix does not depend on it. |

## Notes
- No rejected findings. No Medium or minor finding was touched.
- Checks not run: this sandbox has no repository, so no claim in the added text about `src/` files is newly verified; added text cites only spec and inventory lines.
- Residual item for the next re-review (not fixed, not a listed finding): `--report-dir` is a flag every changed command must accept, which Phase 1 delivers for P1 commands and later phases deliver for theirs; section 5/SA-3 keep standalone runs unchanged because the contract is written only when `--unattended` or `--report-dir` is passed.
- No verdict self-awarded.
