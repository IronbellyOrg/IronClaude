# Diff analysis: proposals A (minimal), B (safety), C (pipeline)

Run inline by the brainstorm session (the adversarial skill was not invoked as a skill; see LOG.md). Sources: proposals/proposal-a-minimal.md, proposal-b-safety.md, proposal-c-pipeline.md, each read in full.

| # | Decision point | A | B | C | Chosen | Agreement |
|---|---|---|---|---|---|---|
| 1 | Flags | `--unattended`, `--report-dir` | same + `--plan-sha256` | same + `--approve-plan`, `--plan-only` | `--unattended`, `--report-dir`, `--plan-sha256`; no `--plan-only` in v1 | 2 of 3 on a hash flag; name from B |
| 2 | Flag position | option prefix or after one file path | standalone token outside quotes | not stated | A's rule, flags first in the brief form | A, B compatible |
| 3 | Report dir | not in `.dev/tasks/` or ledger dir | under `.dev/`, no symlink, not in ledger dir or package | holds only the contract | B's rules; refuse a dir that already holds a contract (brainstorm precedent), not B's `.prev` rename | A, B, C compatible |
| 4 | Contract extras | none, plus `follow-ups.md` | flat NEW keys | `implement:` mapping | `implement:` mapping (C) with B's `plan_approval` and `unresolved`; no extra file | 2 of 3 |
| 5 | Status from | not stated | fresh ledger parse at exit | contract is a claim, ledger is proof | ledger parse at exit | B, C |
| 6 | Rows P, H | refuse, blocked | refuse, blocked | refuse, blocked | refuse before any write, blocked `E-HALT-QA` | unanimous |
| 7 | E-HALT-QA, E-NO-RULING | blocked | blocked | blocked | blocked | unanimous |
| 8 | E-RESUME-NEEDED | failed | failed | failed | failed | unanimous |
| 9 | E-ARCHIVE-BLOCKED | blocked if FINAL issues else failed | blocked | partial | A's split | A; C's partial rejected (D2 freeze text) |
| 10 | Legacy FINAL issues | partial | partial | partial | partial | unanimous |
| 11 | Plan hash mismatch | none | failed `E-PLAN-CHANGED` | blocked `E-PLAN-NOT-APPROVED` (NEW) | blocked `E-PLAN-NOT-APPROVED`, exempt from the D2 freeze | C; B's reuse rejected (E-PLAN-CHANGED means a pin mismatch after a start) |
| 12 | Parallel batches | unchanged | forced sequential | forced sequential | forced sequential | 2 of 3 |
| 13 | Extras | 4 min kill | background, waits at most 4 min, 20 min cap | not stated | B | B matches WC-10 |
| 14 | Nested | impact with `--unattended`; delegates unchanged | impact nested; optional delegates skipped | not stated | impact nested; optional delegates skipped and recorded | A, B |
| 15 | Ruling already in ledger | succeeded | partial | not stated | partial | B |
| 16 | `--skip-final-review` | not stated | partial | never passed | managed: refuse before any write; legacy: succeeded with `final: skipped` | new (neither proposal fully) |
| 17 | Launch levels, guard | not changed | not stated | detailed | C's text | C |
| 18 | WORKER-CONTRACT edits | none | pins only | section 5 row, D2 text | C, plus pins from B | C |

Convergence (inline estimate, not the adversarial skill's formula): the chosen option matches at least two proposals on 15 of 18 points and all three on 4, about 0.83. Not converged: see BRAINSTORM-NOTES.md.
