# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential) plus Round 2.5 invariant probe; Round 3 skipped (depth=standard)
- Convergence achieved: 91% (10 of 11 diff points)
- Convergence threshold: 80%
- Convergence status: BLOCKED_BY_INVARIANTS (INV-001, INV-002 HIGH and UNADDRESSED after Round 2.5; resolved by incorporation into M-01 and M-02 fixes, not by a further round)
- Focus areas: All
- Advocate count: 2
  - Variant 1 advocate: haiku, persona analyzer
  - Variant 2 advocate: sonnet, persona qa
- Fault-finder: sonnet (independent)
- Judge / orchestrator: a different model class from every debater

## Round 1: Advocate Statements

Full statements are persisted verbatim (not edited) in:
- `round1-variant1-haiku-analyzer.md`
- `round1-variant2-sonnet-qa.md`

### Variant 1 Advocate (haiku:analyzer) — summary
- Position: V1 is the better design review (contradictions between plan, source and snapshot contract); V2 is the better test-coverage audit.
- Steelman of V2: QA-01 (four-kind contract gate, SPEC:215) and QA-05's direct T5 citation (SPEC:369).
- Concessions: R1-06 raised to blocking (X-001); X-002 rule — a missing criterion is not automatically blocking.
- Shared assumptions: A-001 QUALIFY, A-002 QUALIFY, A-003 QUALIFY, A-004 REJECT.
- Missed items: export completeness under A-003 only.

### Variant 2 Advocate (sonnet:qa) — summary
- Position: V2 is the better coverage audit; V1's R1-02 and R1-03 are real defects V2 missed.
- Steelman of V1: `_find_orca` probe (`install_user_setup.py:209`) falsifies plan:23; plan:173 never publishes SNAP:88 STALE/ERROR.
- Concessions: QA-03, QA-04 to minor; QA-08, QA-11, QA-12 narrowed.
- Shared assumptions: A-001 QUALIFY, A-002 QUALIFY, A-003 REJECT, A-004 QUALIFY.
- Missed items: T16 scenario matrix, T22 view texts, export vs hidden rows.

## Round 2: Rebuttals

Full rebuttals are persisted verbatim in:
- `round2-variant1-haiku-analyzer.md` (delivered first)
- `round2-variant2-sonnet-qa.md` (delivered second, after reading V1's rebuttal)

### Variant 1 Rebuttal — summary
- Accepts SPEC:369 as the stronger basis for R1-01; accepts that reusing `_find_orca` is SPEC-prescribed (SPEC:312), narrowing R1-02 to the false "only" claim plus the missing seam.
- Withdraws whole-field suppression for R1-04 but holds blocking on the credential prohibition (SNAP:77).
- Holds QA-09 blocking (inspector half missing, SPEC:352).
- Missed items: T16 holds blocking; T22 view texts hold blocking; export vs hidden rows holds minor.

### Variant 2 Rebuttal — summary
- Confirms narrowed QA-04, QA-08, QA-11, QA-12.
- Holds R1-04 minor: SNAP:77 and SNAP:103 together make "no credentials" a field-level rule; the SPEC sanitizer is control-only (SPEC:337).
- Concedes QA-09 to blocking, narrowed to the inspector half.
- Missed items: T16 blocking (sessions x widths; the orchestrators axis has no R1 source); T22 view texts blocking; export vs hidden rows minor.

## Round 2.5: Invariant Probe

See `invariant-probe.md`. 12 findings, all UNADDRESSED: 2 HIGH (INV-001 discovery cost and subprocess count inside the cycle; INV-002 undefined outcome of a budget-truncated cycle), 8 MEDIUM, 2 LOW. The HIGH items block convergence; both are amendments to the blocking cycle-budget/discovery fixes and are incorporated there.

## Taxonomy coverage gate

| Level | Points | Addressed in debate |
|-------|--------|---------------------|
| L1 surface | S-001, S-002 | yes (both advocates compared granularity and evidence style in their steelmen) |
| L2 structural | C-003, X-001, X-002, A-001, A-002, A-004 | yes |
| L3 state mechanics | C-001, C-002, A-003 | yes |

All three levels covered; no forced round needed.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 | Variant 2 | 75% | Both advocates agree V2's 12 findings cover more of the SPEC test list; V1's 7 go deeper on design. |
| S-002 | Variant 1 | 80% | V2 conceded "R1 found the defects that need reading source code" (R1-02 cites `install_user_setup.py:209`). |
| C-001 | Variant 2 | 90% | Same blocking claim; V1 accepted V2's SPEC:369 (T5) citation as the stronger basis. |
| C-002 | Variant 2 | 95% | V1 conceded T33 is blocking (SPEC:172 "must render"; T33 unmapped at plan:126). |
| C-003 | Tie | 90% | Both rate the PARTIAL disclosure minor; merged. |
| X-001 | Variant 2 | 95% | Resolved as blocking by concession. |
| X-002 | Variant 1 | 85% | Both adopted V1's stricter rule: instructed-but-unasserted = minor; absent deliverable or unmet gate = blocking. |
| A-001 | — (agreed QUALIFY) | 85% | Tests for excluded B/R2+ features are out; R0/R1 tests not excluded (T16, T31, T33) are in. |
| A-002 | — (agreed QUALIFY) | 80% | plan:22 cites the owner message; owner-decisions:9 leaves full gate satisfaction to the owner; not a finding. |
| A-003 | — (agreed: holds, minor) | 80% | plan:126 hides/filters rows; plan:157 "every ledger row"; SPEC:189; no instruction to delete, but unpinned. |
| A-004 | Unresolved | 50% | V1 REJECT, V2 QUALIFY on the label; both keep R1-05 minor. Fault-finder INV-004 found a second gap (Task 10). |

## Convergence Assessment
- Points resolved: 10 of 11
- Alignment: 91%
- Threshold: 80%
- Taxonomy: all levels covered
- Invariant gate: BLOCKED (INV-001, INV-002)
- Status: BLOCKED_BY_INVARIANTS at end of debate; the two HIGH items are carried into the M-01 and M-02 fixes in `refactor-plan.md`
- Unresolved points: A-004 (label only)

## Per-finding outcome after debate (input to Step 4)

| Finding | V1 final | V2 final | Agreement |
|---|---|---|---|
| R1-01 / QA-05 | confirmed, blocking | confirmed, blocking | yes |
| R1-02 | narrowed, blocking | confirmed (seam + false claim), blocking | yes |
| R1-03 | confirmed, blocking | confirmed, blocking | yes |
| R1-04 | narrowed, blocking | narrowed, minor | NO — decided by the judge in `refactor-plan.md` |
| R1-05 | confirmed, minor | confirmed, minor | yes |
| R1-06 / QA-02 | confirmed, blocking | confirmed, blocking | yes |
| R1-07 / QA-06 | confirmed, minor | confirmed, minor | yes |
| QA-01 | confirmed, blocking | confirmed, blocking | yes |
| QA-03 | narrowed, minor | narrowed, minor | yes |
| QA-04 | narrowed, minor | narrowed, minor | yes |
| QA-07 | confirmed, minor | confirmed, minor | yes |
| QA-08 | narrowed, minor | narrowed, minor | yes |
| QA-09 | confirmed, blocking | narrowed (inspector half), blocking | yes |
| QA-10 | narrowed, minor | confirmed, minor | yes (severity) |
| QA-11 | narrowed, minor | narrowed, minor (nit) | yes |
| QA-12 | narrowed, minor | narrowed, minor | yes |
| T16 (new) | holds, blocking | holds, blocking (sessions x widths) | yes |
| T22 view texts (new) | holds, blocking | holds, blocking | yes |
| Export vs hidden rows (new) | holds, minor | holds, minor | yes |
