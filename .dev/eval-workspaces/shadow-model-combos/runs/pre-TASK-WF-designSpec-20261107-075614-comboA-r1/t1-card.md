# Tier 1 reflection card — pre-TASK-WF-designSpec-20261107-075614-comboA-r1

Mode: pre (UC-1). Executor class: unknown (no flag/env/log hint; fail-open per §7.1).
Inputs: source.md (379 lines, design spec v3, issue #375 pr-submit merge guard), tasklist TASK-WF-designSpec-20261107-075614.md (13 tasks, 5 phases, workflow-plan/1.2).

## Coverage summary (Step 1B.0)

- Pass 1 (ID_REGEX R-|REQ-|SPEC-|T-\d+): 0 IDs in spec, 0 in tasklist. parsed_total = 0.
- Pass 2 (inference, quote-pinned): 15 INF rows (INF-001..INF-015), anchored on the spec's own traceability table (source.md:346-356), the files-to-change table (source.md:283-301), section 4.7 and section 10.
- parsed-sparse guard (Step 1B.2b): inferred_count (15) > parsed_count (0) → coverage_degraded: parsed-sparse; T1 stop forbidden; route to T2 (tier already pinned 2).
- Union matching: all 15 rows match at least one task via containment → coverage_pct_union = 1.0000; unmapped (union) = [].
- coverage_pct (parsed-only): null.

## Findings (hypotheses — for Tier 2 review)

- **H1 (wording tension, MINOR candidate).** The Wave 0 SKILL.md bullet must itself carry the L3/`--merge-guard off` print clause ("at L3 with `--merge-guard off` the line 'Remediation is unprotected...' is printed once", source.md:241) while Task 9's AC says the bullet "contains no `L3 only` or `draft` gate wording" (tasklist:137,140). The AC's "gate wording" qualifier makes it implementable (the load-clause carries no gate; the print-clause names L3), but a test author reading only the AC could ban the token `L3` outright and write an unpassable test. Family: pass-gate wording (shadow06/08/10 recurrence class).
- **H2 (superset dependency, MINOR candidate).** Task 13 (docs/user-guide) declares "Depends on: Task 2" (tasklist:190); nothing in Task 13 consumes the enum change. Harmless over-sequencing, not a coverage gap. [INFERRED]
- **H3 (verified conformance).** Dependency completeness per source.md:363: every consumer declares its producers (T5←T3,T4; T8←T1,T4,T7; T9←T6,T8; T10←T9; T11←T3,T4,T5,T7; T12←T6,T8; T13←T2,T10,T11,T12). Every file in the spec's files-to-change table (source.md:283-301) has an owning task. The 12 minimum tests of source.md:307-322 all appear by name in Task 11 (tasklist:169). The classification-last discipline (source.md:255, 373) appears in Tasks 7, 8, 9, 10, 12.
- **H4 (constraint without explicit AC, MINOR candidate).** source.md:208 "A corrupt line still raises, as it does today" — no task AC names corrupt-line fold behavior explicitly (implicitly held by existing RunLog tests; Task 5's legacy-log AC is adjacent but not the same). Family: constraint without matching AC (shadow06/10 recurrence).
- **H5 (verified conformance).** The owner decisions (source.md:6: draft not label; engage end of Wave 3; default on at monitor 3; release on confirmed push before replies; unreadable/unpublished keeps draft) are each carried into Constraints (tasklist:26) and the corresponding tasks (6, 8, 9, 10, 11).

## Best-practice grade

4/5 — phased plan, per-task ACs runnable as tests, dependency-complete, sync cadence and classification discipline explicit; minus one for the two wording-level tensions above.
