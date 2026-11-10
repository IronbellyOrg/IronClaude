# Revise 1: orca-worker-contract-spec.md

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Blocking ids repaired: F-1, F-2, F-3 (Reviser brief, `review/round1.md`, last section). Medium and minor findings (M-1 to M-7, m-1 to m-4) left alone. No PASS is awarded.

## Byte accounting

- Before: 57763 bytes (285 lines). After: 58227 bytes (285 lines). Net +464.
- All additions are ASCII, so bytes equal characters.

| Finding | Bytes added | Bytes deleted |
|---|---|---|
| F-1 | 171 | 0 |
| F-2 | 53 + 95 + 6 = 154 (P1 sentence at spec:159, AC-1.1 at spec:195 as an in-line clause, and the F-2 tag) | 0 |
| F-3 | 139 | 0 |
| Total | 464 | 0 |

Each finding was met by a narrowing clause in an existing cell. No rule, section, mechanism or table was added.

## Per-finding rows

| Id | Result | Where | How |
|---|---|---|---|
| F-1 | Applied | WC-4, spec:62 | Added "or the parent directory of a file-valued `--output`", and "a command whose section 3 row names another contract location uses that location, and the brief names it". This covers tdd and init-lite (rows spec:87, 90, `--output <file>`) and spec-panel (spec:120). It also covers adversarial (spec:83), workflow (spec:92) and cleanup-audit (spec:85), whose rows already name a different location. The live check (spec:182-183) and AC-2.3 (spec:201) now have an existing path to test. The brief rule at spec:73 is unchanged; the new WC-4 clause says the brief names the location. |
| F-2 | Applied | Phase 1 row, spec:159; AC-1.1, spec:195 | The P1 flag sentence now excludes the P4 commands (implement, post-release, pr-submit; list from the P4 row, spec:163). AC-1.1 now excludes `load` and those three. `load` is excluded because its row (spec:112) and the Decisions row (spec:265) say it gets no contract. The P4 commands' gates depend on D2-D4, which Phase 4 waits for (spec:225). The section-4 exclusion in AC-1.1 is kept. The section 2.1 definition (spec:51) and SA-4 (spec:149) were not edited. SA-4 still says Phase 1-3 edits add a section, and the AC and P1 text now carve out load and the P4 commands. |
| F-3 | Applied | cli-portify row, spec:105 | Appended to the `--resume <contract>` cell: "it counts as approval of the gate the contract names as blocked, so the resumed run passes that gate and stops only at the next one". A run to `succeeded` is now reachable after three resumes, so AC-2.3 (spec:201) can pass. This took the reviewer's first recommended option, so AC-2.3 was not changed. |

## Notes

- The inventory citations (`INV-A:45,68`) already in the F-3 row were not re-edited. All source citations beyond the spec and `README.md` are UNVERIFIED in this sandbox.
- AC-1.1 still names one test file whose behavior is described in prose. It was not reworded beyond the exclusions.
