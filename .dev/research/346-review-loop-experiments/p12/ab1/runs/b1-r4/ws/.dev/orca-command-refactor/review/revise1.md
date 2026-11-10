# Revise 1 (blocking ids M1, M2, M3, M4, M5)

Candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md, edited in place. Inputs read: review/round1.md (Reviser brief, lines 156-161), review/verify-1.md, the spec, README.md. No inventory line was re-checked beyond the ones already cited in the spec; citations I did not re-read are UNVERIFIED here.

## Byte accounting
- Before: 57763 bytes. After: 58352 bytes. Net +589.
- Five span replacements (replaced span bytes -> new span bytes). Edits E1-E3 serve several ids at once, so the bytes are listed per edit and the ids it serves; no byte is counted for two edits.

| Edit | Location (after) | Deleted (bytes) | Added (bytes) | Ids |
|---|---|---|---|---|
| E1 | spec:76 | 94 | 154 | M1, M4, M5 |
| E2 | spec:159 (P1 row, Scope) | 112 | 188 | M1, M4, M5 |
| E3 | spec:195 (AC-1.1) | 194 | 263 | M1, M4, M5 |
| E4 | spec:194 (AC-0.4) | 105 | 283 | M2 |
| E5 | spec:62 (WC-4) | 91 | 297 | M3 |

Per finding id (shared edits split by the ids they carry; M1/M4/M5 share E1-E3 because one scoping change repairs all three): M1+M4+M5 together: deleted 400, added 605. M2: deleted 105, added 283. M3: deleted 91, added 297. Deleted/added are the replaced span and its replacement, not a minimal diff, so both are overstated by the unchanged words inside the spans. No section or table was added.

## Findings
| id | Result | Where applied | Reason |
|---|---|---|---|
| M1 | Applied | spec:76 ("except `/sc:load`"), spec:159 ("`/sc:load` gets neither"), spec:195 (test asserts `/sc:load` has no section) | Removes the contradiction with the load row (spec:112, "none (see note)", "usage line only") and the Decision (spec:265, "a report file would be an unrequested addition"). Narrowing, per round1.md:36-39 recommendation. |
| M2 | Applied | spec:194 (AC-0.4) | Steps 3 and 4 both use the command's existing report file in P0; step 3 compares `--outcome` with that report under WC-5; step 4 is `test -s` only (the YAML parse of 7.2 step 4 cannot apply to `REPORT.md`, spec:91). Step 7.2 text itself is unchanged, so P1-P4 still use the contract. |
| M3 | Applied | spec:62 (WC-4) | One rule: file-valued `--output` puts the contract in the file's parent directory (covers tdd, init-lite, spec:87, 90, 200); fixed-location commands (cleanup-audit, index-repo, spec:85-86) write it there; adversarial's `<output>/adversarial/` (spec:83) named as the stated exception. No new flag. Not decided: whether spec-panel's added `--output` is file or directory (spec:120); the parent-directory rule gives a defined path either way. The `CMD:460` citation in the finding is UNVERIFIED (not in the sandbox). |
| M4 | Applied | spec:76, spec:159, spec:195 | `--unattended` and the section arrive in the phase of each command's own row (P1 row commands plus brainstorm and init-lite; P2-P4 rows otherwise), so auggie-review, task, post-release, pr-submit, implement no longer accept the flag before their gates are converted. Scope removed from P1, no rule added. |
| M5 | Applied | spec:159, spec:195 | AC-1.1 now tests only the P1 scope and requires P2-P4 commands to have no section, which removes the conflict with spec:154/225 ("Phases 1-3 need no user decision") and with D3(a) (no pr-submit change, spec:240). |

## Left alone
Medium and minor follow-ups from round1.md (follow-up candidates) were not touched. No verdict is awarded.
