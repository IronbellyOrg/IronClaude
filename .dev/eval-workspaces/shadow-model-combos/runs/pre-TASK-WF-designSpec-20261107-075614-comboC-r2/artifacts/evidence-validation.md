# Wave 5: evidence-validator result

Validator: `evidence-validator` agent (read-only: Read, Grep, Glob; it could not write this file, so the orchestrator wrote it from the agent's reply). Scope: the 15 merged findings of `adversarial/adversarial/merged-output.yaml` (64 citations). The 84 inferred-requirement rows were checked by the deterministic script `artifacts/coverage_calc.py` (quote must be a substring of the cited spec lines): 84 kept; 2 more rows were already dropped at emission for a non-verbatim quote (`dropped_at_emission` in `coverage-matrix.json`).

Totals (agent part): citations_total 64, citations_revalidated 64, citations_dropped 2.

| Finding | Citation | Verdict | Reason |
|---|---|---|---|
| M-4 | source.md:311 | dropped | this line is the behavioural driver test, not the Wave 3 text test (the phrase-only test is at source.md:322) |
| M-6 | source.md:150 | dropped | release row 2 (`NOOP(not_held)`) says nothing about engage after a failed draft settle |

All other 62 citations were kept. Kept but PARTIAL support (context, not the weakness itself): M-2 plan:124, M-3 plan:37 and plan:127, M-6 plan:70, M-11 source.md:342, M-14 source.md:196-206, M-15 plan:76-77. Quotes checked: M-7, M-11, M-13 match verbatim.

Sub-claims the cited lines do not carry, therefore `[INFERRED]`: M-14 "git write verbs missing from classification steps" (plan lines 22 and 108 are not cited); M-8 "gh returns autoMergeRequest as an object or null" (outside knowledge; not verifiable offline). M-1 "the folded state holds neither" was checked against spec 190-191 only, not against code.

Surviving findings: M-1 to M-15 (all 15). Zero findings wholly unsupported.

Zero-drop flag: false (2 dropped).
