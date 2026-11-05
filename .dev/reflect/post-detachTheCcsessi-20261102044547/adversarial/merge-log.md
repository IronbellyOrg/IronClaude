# Merge Log

## Metadata

- Base variant: Variant 2 (reviewer 2, qa, haiku=glm-5.3) — variant-2-original.md
- Incorporated from: Variant 1 (reviewer 1, analyzer) — variant-1-original.md; debate-transcript.md; invariant-probe.md
- Plan: refactor-plan.md (8 planned changes; 2 rejected by the plan)
- Executor: merge-executor
- Output: merged-output.md
- Status: COMPLETE (8 of 8 applied, 0 skipped, 0 escalated)
- Timestamp: 2026-11-02T05:34Z

## Changes Applied (plan order)

### Change #1 — Reclassify R2-F1 (isatty guard) to necessary, LOW
- Status: applied
- What changed: Deviations row R2-F1 category drift -> necessary and severity MEDIUM -> LOW. The claim "no artifact documents a discovered constraint" was removed and replaced with the inline rationale at local-gateway-alias-proxy.py:859-862 plus the dead-pty stderr reason (proxy:126-127, :491). The untested tty branch (test:598, ccsession:808) and the unconditional CHANGELOG.md:11 wording are kept as notes; the recommendation is now to soften CHANGELOG.md:11 to "when not started on a terminal" (documentation note, LOW).
- Provenance tag: Variant 1 R1-F1 and debate C-001/X-002/X-003, merged per Change #1

### Change #2 — Reclassify R2-F2 (T1 extra assertions) to necessary, LOW
- Status: applied
- What changed: Row R2-F2 category drift -> necessary. Added the evidence from the plan: getsid follows pre-execution F15 (pre-detach.../adversarial/merge-log.md:23) with an inline comment at test:1538; the thread wrapper records exceptions (an applied pre-execution finding); timeout=30 matches `streaming.join(30)`.
- Provenance tag: Variant 1 R1-F2 and debate C-002, merged per Change #2

### Change #3 — Split R2-F3 (CHANGELOG)
- Status: applied
- What changed: R2-F3 split into R2-F3a (heading suffix, CHANGELOG.md:9; drift, LOW, cosmetic) and R2-F3b (last sentence, CHANGELOG.md:11; drift, LOW, accurate against ccsession:766 and :782-784; only rationale is the after-the-fact note at troubleshoot REPORT.md:135; pre-execution F3 asked only for "shims stay up until stopped", pre-detach REPORT.md:45, :76-77). R2-F3b is marked as the unresolved debate point C-004.
- Merge note: the base's single gold-standard cell "plan:78, :81" is kept as written on R2-F3b; R2-F3a cites only plan:78 (the line Variant 1 says holds `#### Fixed`). The new IDs R2-F3a/R2-F3b are the executor's labels for the split; the plan names the two parts but not their IDs.
- Provenance tag: Base (original, modified); both variants and debate C-003/C-004/C-010

### Change #4 — Keep R2-F4 (`make sync-dev`) as necessary, LOW
- Status: applied (no change, as planned)
- What changed: nothing; row copied from base.
- Provenance tag: Base (original)

### Change #5 — Add a Risks section (non-gating)
- Status: applied
- What changed: new section "Risks (non-gating)" with the seven plan bullets: INV-002 residual, INV-001, macOS getsid (R1-F6), subreaper (U-003; INV-004), `sys.stderr` None (INV-005), stale shims accumulating (INV-006), and the grouped list (INV-007, INV-003, INV-009, U-004). Added only the `(ccsession:1)` pointer from the probe's INV-001 orchestrator note.
- Provenance tag: Variant 1 / invariant probe, merged per Change #5

### Change #6 — Correct the evidence notes
- Status: applied
- What changed: new "Evidence notes" subsection under Deviations stating "262 passed" (129 tiers + 133 tag) at verify-logs/pytest-ccsession.stdout.txt:17 and "457 passed" (7 files) at t5-checks.log:11, and that the progress.md ledger pointer drift (t1-before.log:13/:19 vs outcome :15-20, :22-23) is harmless. The base's "No regression" paragraph keeps both figures unchanged. Variant 1's R1-F7 is not carried over (rejected by the plan).
- Provenance tag: Base (original, modified)

### Change #7 — Update the adherence summary
- Status: applied
- What changed: new "Adherence summary" section: 13 AC audited, 13 adherent; Authorized 0; Necessary 3 (R2-F1, R2-F2, R2-F4); Drift 2 (R2-F3a, R2-F3b; both LOW); Regression 0. The "Total deviations" header line was changed from "4 (0/1/3/0)" to "5 rows (0/3/2/0)" to match. The AC audit table is untouched.
- Provenance tag: Base (original, modified)

### Change #8 — Add provenance and a "Not verified" list
- Status: applied
- What changed: three provenance header lines; a `<!-- Source: ... -->` comment on all 9 sections plus a row-level source comment under Deviations; new "Not verified" section (Orca itself on other hosts; macOS; bash 3.2 runtime; `bash -n`, lint and live check are implement-leg artifacts cross-corroborated by the 262-pass run).
- Provenance tag: Variant 1 / invariant probe, merged per Change #8

## Not Applied (per plan)

- R1-F7 (no "262 passed" figure): rejected by the plan (false premise, verify-logs:17).
- R1-F4 (CHANGELOG sentence "authorized by reflection"): rejected by the plan (taxonomy:28-36; F3 did not ask for the sentence).

## Post-Merge Validation

| Check | Result |
|---|---|
| Heading hierarchy | PASS: H1 (line 5) -> H2 x8 -> one H3 ("Evidence notes") under Deviations; no skipped level |
| Provenance header | PASS: the three required lines are lines 1-3 |
| Source comment on every section | PASS: 9 `<!-- Source: -->` comments for 9 sections (title block, AC audit, Deviations, Evidence notes, Judgments, Risks, Adherence summary, Grounding gaps, Not verified) |
| AC audit table intact | PASS: the 13 AC rows are byte-identical to variant-2-original.md (diff reported IDENTICAL) |
| Adherence counts vs deviation rows | PASS: 5 rows = necessary 3 (R2-F1, R2-F2, R2-F4) + drift 2 (R2-F3a, R2-F3b) + authorized 0 + regression 0; header line and summary section agree |
| Finding IDs resolve | PASS: R2-F1/F2/F3a/F3b/F4 are defined in the table; INV-001 to INV-007 and INV-009 exist in invariant-probe.md; R1-F1, R1-F2, R1-F6, R1-F7 in variant-1-original.md; C-001, C-002, C-004, C-008, X-001, X-002, X-003 in debate-transcript.md. U-003 appears in debate-transcript.md and U-004 only in refactor-plan.md; both are Variant 1 diff-point IDs cited as the plan cites them |
| file:line citations | PASS after one fix: every citation was checked as a literal string against the five sources. One `plan:81` I had introduced was not a literal source citation; restored to the base's "plan:78, :81". Remaining hits are all present in the sources |
| New contradictions | None found: R2-F1 is necessary/LOW in the table, the Risks section and the summary; CHANGELOG.md:11 wording note appears once as a LOW documentation note; "No regression" and Judgment 1 are unchanged; no AC verdict changed |

Residual notes (not contradictions): the base's R2-F1 recommendation "record the guard's justification (or drop it)" was replaced because the justification is already recorded at local-gateway-alias-proxy.py:859-862. Variant 2's self-reported confidence 0.86 was kept unadjusted since the plan does not change it.

## Summary

- Planned changes: 8
- Applied: 8
- Skipped: 0
- Escalated to the orchestrator: 0
- Rollback: use variant-2-original.md
