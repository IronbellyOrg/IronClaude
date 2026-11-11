# Revise 1 (REVISE prompt; ids M1, M2, M3, M4, M5, M6)

Candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (edited in place). No PASS is claimed.
Evidence limits: only files in the workspace were checked. The review's `CMD:460`/`CMD:23` (real spec-panel `--report-dir`) cannot be checked in this workspace: UNVERIFIED, and the spec says so.
Process note: the edit script was written to the session scratchpad outside the sandbox (/tmp/claude-0/.../scratchpad/ed.py), a rule slip; no other outside path was touched.

## Byte accounting
Before 57763, after 58684 (net +921). Bytes added / deleted per edit (bytes of replaced text vs new text):
| Id | Edit | added | deleted |
|---|---|---|---|
| M1+M4+M5 | AC-1.1 (spec line 195) scoped to the P1 row, `load` excepted | 133 | 68 |
| M1+M4 | AC-1.2 (line 196) `load` excepted | 100 | 72 |
| M1 | section 3 intro (line 76): `load` gets no section | counted in M5 row | |
| M2 | AC-0.4 (line 194) steps 1-2, 5-7; step 3 uses existing report file | 185 | 105 |
| M3 | cli-portify row (line 105) states unattended run ends blocked | 191 | 104 |
| M3 | AC-2.3 (line 201) cli-portify expected result `blocked` | 287 | 109 |
| M5 | section 3 intro (line 76), phase-scoped section; includes M1 clause | 148 | 80 |
| M5 | P1 row (line 159) flag limited to P1 commands | 158 | 111 |
| M6 | WC-4 (line 62) `--report-dir` | 411 | 91 |
| M6 | section 2.3 (line 73) | 80 | 72 |
| M6 | section 3 intro "Contract" definition (line 76) | 88 | 67 |
| M6 | AC-2.2 example (line 200) | 64 | 45 |

## Findings
| Id | Disposition | Where and how |
|---|---|---|
| M1 (a) | applied | AC-1.1 narrowed so `load` is excluded (follows the review's preferred narrowing); line 76 says `load` gets no section, consistent with the load row (spec line 112) and Decisions (line 265). |
| M2 (a, b) | applied | AC-0.4 now runs steps 1-2 and 5-7, and step 3 passes on one `worker_done` with the command's existing report file (spec lines 91, 92, 158, 182). |
| M3 (a) | applied | Took the review's preferred AC-2.3 narrowing: cli-portify expected `failed`/`blocked`; row now says no flag carries an approval (gates always on, `inventory/commands-a.md:45`). No new flag added. |
| M4 (a, b) | applied | Same edits as M1: AC-1.1 and AC-1.2 name `load` as the exception. |
| M5 (a) | applied | AC-1.1 scoped to the P1 row; P1 flag text limited to P1 commands; line 76 adds sections in each command's own phase. Later phases are not given new checks beyond AC-2.1/AC-3.x already present. |
| M6 (a) | applied, with one added mechanism | The finding calls for one coordinator-supplied directory argument separate from file-valued `--output`: WC-4 defines `--report-dir <dir>`, workflow writes the pre-creation STOP contract there; section 2.3, the "Contract" definition and AC-1.2/AC-2.2 use it. Not changed: AC-3.2 and AC-4.2 still show `--output <dir>` (not named by M6), and the `analyze`/`design`/etc. "add `--output`" cells in section 3.2, which are unreconciled with `--report-dir` (leave as follow-up for the next review). |

Left alone: all Medium and minor findings (follow-up candidates, W1-W4, FC-x).
