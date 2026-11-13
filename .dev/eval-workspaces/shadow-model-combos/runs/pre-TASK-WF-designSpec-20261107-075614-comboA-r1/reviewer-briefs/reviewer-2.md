# Reviewer 2 brief — persona: qa (coverage / acceptance lens)

Audit target: UC-1 pre-execution. Spec = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (design spec v3, issue #375, pr-submit merge guard). Plan = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (13 tasks, 5 phases).

ATTRIBUTION NOTE (binding): this is a PRE-execution audit of the frozen spec↔plan pair. The spec's facts F1-F13 are pinned at base commit e8db2fe6 (2026-11-07). HEAD has since evolved (the feature landed as commit 0b8a5801d); do NOT file findings that rest on HEAD source text — audit the plan's coverage against the frozen spec only.

Your lens: requirement coverage, missing deliverables, unpassable or escape-hatch acceptance criteria, test-design completeness. The spec's traceability table (source.md:346-356) maps FR-1..FR-23 to sections; the files-to-change table (source.md:283-301) enumerates deliverables; section 7 enumerates the 12 minimum tests; section 10 constrains plan authoring.

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

## T1 card excerpt

Verbatim excerpt from t1-card.md (coverage-relevant slice):

> ## Coverage summary (Step 1B.0)
>
> - Pass 1 (ID_REGEX R-|REQ-|SPEC-|T-\d+): 0 IDs in spec, 0 in tasklist. parsed_total = 0.
> - Pass 2 (inference, quote-pinned): 15 INF rows (INF-001..INF-015), anchored on the spec's own traceability table (source.md:346-356), the files-to-change table (source.md:283-301), section 4.7 and section 10.
> - parsed-sparse guard (Step 1B.2b): inferred_count (15) > parsed_count (0) → coverage_degraded: parsed-sparse; T1 stop forbidden; route to T2 (tier already pinned 2).
> - Union matching: all 15 rows match at least one task via containment → coverage_pct_union = 1.0000; unmapped (union) = [].
> - coverage_pct (parsed-only): null.
>
> ## Findings (hypotheses — for Tier 2 review)
>
> - **H2 (superset dependency, MINOR candidate).** Task 13 (docs/user-guide) declares "Depends on: Task 2" (tasklist:190); nothing in Task 13 consumes the enum change. Harmless over-sequencing, not a coverage gap. [INFERRED]
> - **H3 (verified conformance).** Dependency completeness per source.md:363: every consumer declares its producers (T5←T3,T4; T8←T1,T4,T7; T9←T6,T8; T10←T9; T11←T3,T4,T5,T7; T12←T6,T8; T13←T2,T10,T11,T12). Every file in the spec's files-to-change table (source.md:283-301) has an owning task. The 12 minimum tests of source.md:307-322 all appear by name in Task 11 (tasklist:169). The classification-last discipline (source.md:255, 373) appears in Tasks 7, 8, 9, 10, 12.
> - **H4 (constraint without explicit AC, MINOR candidate).** source.md:208 "A corrupt line still raises, as it does today" — no task AC names corrupt-line fold behavior explicitly (implicitly held by existing RunLog tests; Task 5's legacy-log AC is adjacent but not the same). Family: constraint without matching AC (shadow06/10 recurrence).

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

Cite with repo-relative paths: spec = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md`, plan = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md`. Quote ≤200 chars.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T03:03:29Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### Spec body part 1 — source.md:1-140 (header, facts, overview, behaviour table, sections 4.1 start)

```text
# Design Spec: pr-submit merge guard (issue #375)
- Owner decisions (accepted 2026-11-07, relayed by the coordinator): draft not label; engage at the first verified Medium-or-higher finding routed to a fix; default on at `--monitor 3` via `--merge-guard {draft,off}`; release when the fix push is confirmed on the PR head, before replies and the re-trigger; an unreadable timeline or an exit with unpublished fixes keeps the PR draft and reports.
[Pass-1 regex (R-|REQ-|SPEC-|T-\d+) extracts 0 IDs; the spec labels requirements FR-1..FR-23 in .dev/brainstorms/20261107-062111-pr-submit-draft-guard/merged-requirements.md — NOT in this document except via the traceability table's FR references]
## 3. Behaviour in one table [13 rows: ordinal<3/off/conflict-cycle → nothing; --resume; off at L3 print; fresh monitor-2 run L2 line; engage end of W3; already-draft skip; no-edit release; pre-push head guard; push confirmed release; foreign toggle; timeline unreadable hold; engage fail halt; any exit unpublished → held]
## 4.1 [GuardMode/Direction/Phase/GuardAction/GuardRead/GuardDecision + 9 function contracts + 3 decision tables 11/9/9 rows + guard_status mapping + classify_toggles rule]
```

### Spec body part 2 — source.md:141-379 (sections 4.1 release/resume tables through section 10)

```text
[4.2 events and folded key: 2 new EventType members (43→45), event field tables, fold effect table 10 rows; 4.3 fsm.py flag; 4.4 set-draft-state.sh; 4.5 protocol and docs table; 4.6 cycle identity; 4.7 pinned write-verb classification; 5 sequences (happy path + acceptance trace + 8 case rows); 6 files-to-change table (14 rows); 7 test design (12 minimum tests + unit tables + v3 additions); 8 pre-build gate G1-G6 + open items O1-O4; 9 traceability FR-1..FR-23 → sections; 10 plan authoring notes (v2 + v3 bullets)]
```

### TASK-WF-designSpec-20261107-075614.md:29-50 (Phases + Tasks 1-2)

```text
## Phase 1: Contracts and pure core
## Task 1: Write the pre-build record ./artifacts/pre-build-gate.md [records base-commit lint/format/full-suite; release-gate decision; closes O1-O4 by reading code]
Acceptance criteria: [base-commit record + G1-G6 rows: G1-G3 CONFIRMED locally, G1/G2 live + G4-G6 OPEN release gate; O1-O4 findings with file+symbol; pins and line-content rules listed; no GitHub call]
## Task 2: Add the two guard events to the closed event enum and the enumeration texts [models.py 43→45, run_log.py docstring, loop-guard.md, test_run_log.py rename+45, test_codex_reviews.py 45]
```

### TASK-WF-designSpec-20261107-075614.md:166-200 (Task 11 scenario tests + Tasks 12-13)

```text
## Task 11: Write the scenario tests over the run log [12 named tests, acceptance trace, crash cases via real detect_crash_window/resolve_crash_window, forbidden-call assertions]
Acceptance criteria: [all 12 test names defined; acceptance-trace event order; crash tests use real recovery; no pr ready at ordinal 2/off; full tests/pr_submit passes]
## Task 12: Document the flag in the command file [pr-submit.md argument-hint, Options row, Merge guard section; classification entries last]
## Task 13: Document the flag in the user guides, sync, and run the final checks [commands.md paragraph, flags.md row, full suite + final-checks.md]
Acceptance criteria: [usage/paragraph/row present; verify-sync 0; full suite failures ⊆ base-commit record; git status only src/+tests/+docs/+dev/; .dev/tasks staged]
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-006 FR-12..14 classify_toggles release rows 5-6 | Task 4, 11 | covered | source.md:353 |
| INF-007 FR-15..19 clear command, L2 line, halt reasons | Task 8, 9 | covered | source.md:354 |
| INF-008 FR-21 resume_decision + pending_requests | Task 3, 4 | covered | source.md:355 |
| INF-009 FR-22/23 test design + pre-build gate | Task 1, 11 | covered | source.md:356 |
| INF-010 write-verb classification every new hit line, added last | Tasks 7-10, 12 | covered | source.md:255 |
| INF-011 symbol-name citations, complete Depends-on | Constraints | covered | source.md:362-363 |
| INF-012 files-to-change table complete ownership | Tasks 2,3,5,6,7,8,9,10,11,12,13 | covered | source.md:283-301 |
| INF-013 G1-G6 + O1-O4 pre-build record | Task 1 | covered | source.md:326-341 |
| INF-014 12 minimum tests by name | Task 11 | covered | source.md:305-322 |
| INF-015 script exit codes, --repo every call, legacy fold | Task 7, 11 | covered | source.md:320 |
| INF-015a — audit the spec body for any requirement-bearing span absent above | YOU | open | full spec |
