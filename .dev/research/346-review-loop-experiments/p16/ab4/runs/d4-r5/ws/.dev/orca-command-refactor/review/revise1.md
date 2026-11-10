# Revise 1 (REVISE prompt, IDS = M1, M2, M3, M4, M5)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
inputs: review/round1.md (Reviser brief, lines 123-128), the spec, inventory/ (not needed for these edits; no new inventory claim made)
M6 and M7 untouched (verifier-rejected, noted, unactioned: round1.md:11,96-117). No minor or Medium finding touched. No PASS awarded.

## Byte accounting
Size before: 57763 bytes. Size after: 59005 bytes. Net +1242.
Only line-local edits in the spec; no new section, rule id or flag name added other than the path rule in WC-4.

| id | bytes added | bytes deleted | net | lines touched |
|---|---|---|---|---|
| M1 | 95 | 0 | +95 | 195 |
| M2 | ~300 | ~24 | +276 | 62 |
| M3 | ~410 | ~50 | +394 (incl. +86 on line 73) | 62, 73, 182, 194 |
| M4 | 56 | 0 | +56 | 196 |
| M5 | 421 | 0 | +421 | 200 |

Net per id is exact (measured by wc -c after each sequential edit: 57858, 58134, 58442, 58498, 58919, then +86 for line 73 = 59005). Added/deleted split on M2/M3 is a character-diff estimate; line 62 is shared by M2 and M3.

## Findings
| id | disposition | where applied | what changed |
|---|---|---|---|
| M1 | applied (narrowed the test, not the rows, per round1.md:30) | spec line 195 (AC-1.1) | The assertion now covers commands in 3.1-3.2 whose row adds a section: `load` and every 3.1 row whose small-fix column is `None` (brainstorm line 84, init-lite line 87) are excluded. Rows at lines 84, 87, 112 and Decisions (line 265, `/sc:load`) are unchanged, so no text now requires a section on them. Section-4 clause kept. |
| M2 | applied | spec line 62 (WC-4) | One rule for the location: `--output-dir`, or `--output` when it names a directory; when `--output` names a file (tdd line 90, init-lite line 87, spec-panel line 120) `<output-dir>` is its parent directory; for workflow (line 92) the package dir `.dev/tasks/to-do/<id>/`, or `.dev/tasks/to-do/` when a STOP precedes any `<id>`. AC-2.2 (line 200) and 7.2 step 3 (line 182) now resolve to a defined path because they cite the WC-4 path. |
| M3 | applied | lines 62, 73, 182, 194 | WC-4 title no longer promises "known before dispatch"; it adds that where the command picks the directory (troubleshoot line 91, workflow line 92, adversarial's `<output>/adversarial/` line 83) the coordinator reads the path from `worker_done --report-path` (also resolves the adversarial-vs-`<output-dir>` mismatch in B2). Section 2.3 (line 73) says the same. Live-check step 3 (line 182) now requires the command's named report (the WC-4 contract from P1 on). AC-0.4 (line 194) states the report path comes from `--report-path`, so steps 3 and 4 agree. |
| M4 | applied | spec line 196 (AC-1.2) | `load` excluded from the P1 live check by name, with the reason (it writes no contract, row at line 112). Together with M1's edit to line 195 neither criterion requires a section or contract on `load`. |
| M5 | applied (restricted the criterion, per round1.md:93) | spec line 200 (AC-2.2) | The blocked-outcome check now covers only the nine P2 commands whose rows resolve a gate as blocked: cli-eval (104), cli-portify (105), recommend (115), review-translation (117), spec-panel (120), task (121), tdd (90), troubleshoot (91), release-split (89). The six with no blocked outcome (auggie-review 100, cleanup 103, improve 110, research 116, tasklist 122, reflect 88) get a one-clause check: same run ends `--outcome succeeded` with the default applied, no `agentWait`, no `AskUserQuestion`. |

## Notes
- All line numbers are spec lines before the edit except where stated; line numbers did not shift (no line added or removed).
- Citations to inventory lines were not added; every new claim cites a spec row. Spec line 87/90/91/92/104-105/115/117/120-122 are inside the spec and checked by reading it.
- Not run: the spec-panel (per brief).
