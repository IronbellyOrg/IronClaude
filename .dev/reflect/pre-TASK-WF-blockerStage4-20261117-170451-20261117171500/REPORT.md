```yaml
contract_version: 1.8.0
status: partial          # see "Protocol gaps in this run": deterministic coverage extraction not run
mode: pre
tier_reached: 1
confidence_calibrated: 0.85      # blind calibrator mean, not the reviewer's own 0.85 self-report
citations_total: 36
citations_revalidated: 36
citations_dropped: 0
citations_misstated_corrected: 5
citations_inferred: 1
citation_budget_policy: full_reread
coverage_degraded: null
```

# Pre-execution review: stage 4 plan `TASK-WF-blockerStage4-20261117-170451`

Plan: `.dev/tasks/to-do/TASK-WF-blockerStage4-20261117-170451/TASK-WF-blockerStage4-20261117-170451.md` (134 lines, 5 tasks). Spec: the same folder's `source.md` (99 lines). Input snapshot: `artifacts/input-snapshot.yaml` (tree hash `e130c120...fb4f1`). Run folder: `.dev/reflect/pre-TASK-WF-blockerStage4-20261117-170451-20261117171500/`.

## Verdict
**PASS, zero Blocking findings, six Medium, two Note.** No named decision, acceptance check or quoted number in the plan changes if the Mediums are fixed; no required item is absent in substance; nothing loses data or acts outside scope. The Medium list is a warning list; it does not fail the plan.

## Coverage
The reviewer mapped 14 spec items to the plan (card: `reflection-card.md`, "Coverage map"): 7 covered by a task, 6 cut by Revision 4 or 5 and the plan agrees (digest, registry, plugin mirror, allow-list, strict switch, owner summary), 1 not carried by design. Unmapped: none. All of Tasks 1 to 3 acceptance numbers were checked true against the live tree today (cap counts 2/5/6 and 5/6/1/2, `follow-up candidates` 3 per spec-panel file, `once per loop` 1 per file, replace-target sentences present).

## Findings (after the evidence-validator corrections)

| id | grade | what | evidence | action |
|---|---|---|---|---|
| F1 | Medium | The L1 merge clause is added only at "Findings Consolidation" Step 5 of the MDTM templates. The generic template's Step PG.8 carries the same "severity ... and originating lens" wording and is left with the old merge. CORRECTED by the validator: the other sites the card listed (generic 737 and 967, complex 754, 1119, 1391) do NOT carry the same wording; only generic `:1220-1222` does. | `01_mdtm_template_generic_task.md:936` and `:1220-1222`; `02_mdtm_template_complex_task.md:1088` | Task 1 L1 bullet |
| F2 | Medium | Task 4's bullet asks for a grade prefix in the "What diverged" cell; the agent's example rows (`reflect-reviewer.md:86-87`) show none, so the template and the rule would disagree. consumer-unknown (nothing parses the column). | `src/superclaude/agents/reflect-reviewer.md:84-87`; plan 109, 112 | Task 4 |
| F3 | Medium | Task 4's "why" says the reviewers used the rule only because a person pasted it into the brief. The runs conflict: run B says the orchestrator pasted it (`B/RUN-RECORD.md:176`); run E says nothing was pasted and the origin is unverified (`E/RUN-RECORD.md:69`). Both agree the agent file holds no consequence rule. CORRECTED by the validator. | `.dev/throwaway-medium-runs-20261117/B/RUN-RECORD.md:175-176`, `E/RUN-RECORD.md:69`; plan 106 | Task 4 rationale |
| F4 | Medium | The gate's "statement refers to that trip" test cannot be run by a script; the plan names no pattern. | `stage-requests/README.md:21`; plan 20, 53 | Task 1 first check |
| F5 | Medium | The ledger's stage 4 row still names the old package and the old package is still in `to-do/`. | `stage-requests/README.md:21` | ledger bookkeeping |
| F6 | Medium | The L1 merge text (Constraints, plan 26) stops after the re-ask; the live rule in `rf-qa.md:83` also says the reviewer's label stands, the row is tagged `consumer-unknown` and listed first. | `src/superclaude/agents/rf-qa.md:83`; plan 26 | Tasks 1 and 2 |
| F7 | Note | "ten-file set" wording and line ranges `181-192` / `181-210` become stale with the 11th entry: they are in `docs/developer-guide/review-severity-rule.md:92,112` and the test comment at `test_review_severity_rule.py:179`; `docs/designs/spec-panel-review-loop.md:26` says "ten files". CORRECTED by the validator. | as listed | docs only |
| F8 | Note | After Task 3 the plugin spec-panel keeps its always-CRITICAL sentence while the source is narrowed; recorded on purpose (plan 88). | `plugins/superclaude/commands/spec-panel.md:370` | none |

## Evidence validation
36 citation units re-read: 31 verified, 0 dropped, 5 misstated (F1, F3, F7, coverage row "K8 moot" is source line 86 not 81, check 11 same as F3). The five were corrected in the table above, not dropped, because each fact the finding rests on still stands. A pass with zero drops was treated as suspect: the validator re-read the whole Findings table and found the five.

## Tier decision
Tier 1 stop. Blind calibrator C = 0.85 (citation 0.90, coverage 0.88, classification 0.85, risk 0.90, actionability 0.72), escalation: no. Scope is 5 tasks, domains docs and tests, no regression candidate (UC-1).

## Protocol gaps in this run (why status is partial)
- The deterministic Pass 1 / Pass 2 requirement extraction of Step 1B.0 was not run; the coverage map was written by the Tier 1 reviewer by hand. `coverage_pct` is therefore not reported. The spec is a request note with no requirement ids, so a regex pass would have returned few rows either way. [INFERRED] that this would not change the Tier 1 stop.
- The reviewer could not run pytest; the claim that the 11th tuple entry passes `test_c_*` rests on reading the test bodies. [INFERRED].
- No `metrics.json` and no `runs.jsonl` line were written.

## Recommendations
- R-1 (F2): in Task 4, also say to update the two example rows of the Deviations table so they carry the grade prefix. Verify: `grep -c "Blocking (Decision):\|Medium:\|Note:" src/superclaude/agents/reflect-reviewer.md` prints 3 or more after the edit.
- R-2 (F3): reword Task 4's reason to the part both runs support (the agent file holds no consequence rule: `B/RUN-RECORD.md:175-176`, `E/RUN-RECORD.md:69`).
- R-3 (F4): give Task 1's first check a pattern: the cell holds a date `2026-11-` and the string `RT1`.
- R-4 (F6): extend the L1 merge text with the end state after the re-ask ("if it still names none the reviewer's label stands, the row is tagged `consumer-unknown` and is listed first").
- R-5 (F1): add the L1 merge clause to Step PG.8 of the generic MDTM template and give it its own check.
- R-6 (F5): point the ledger's stage 4 row at the new package and mark the old one superseded.
- R-7 (F7): update the "ten-file set" wording in the developer guide and the test comment in the same change as the tuple append, or leave it as a note.

## Follow-up candidates (Medium list, for the once-per-run offer)
F1 to F6 above. No issue is opened without the owner's answer.
