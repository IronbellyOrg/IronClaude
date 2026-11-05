# Reviewer 2 brief (persona: qa)

Plan under review: `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/TASK-WF-phase3CodegraphA-20261029-204913.md` (224 lines). Spec: `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/source.md` (405 lines). Mode UC-1 (pre-execution): judge whether the plan fully and correctly implements the spec, whether each task is independently executable by a reviewer who sees only that task plus the Constraints, and whether each acceptance criterion can pass as written. Classify each divergence as Authorized expansion / Necessary deviation / Drift / Regression with a `file:line` citation you Read yourself. Read-only: do not run commands or edit files. Return findings as YAML: `findings: [{id, class, severity, plan_ref, spec_ref, claim, fix}]` plus `self_audit` if you find nothing. Focus: coverage. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred), or present in the matrix but not actually carried by the plan task named, as a finding. Also check that every phase ends with a test command, a commit point and an issue-#323 comment, and that the decision rules and a final full verification task are present.

## T1 card excerpt

(Coverage section, verbatim from `.dev/reflect/pre-phase3CodegraphA-20261029205359/t1-card.md`)

## Coverage

- Pass 1 (ID_REGEX) found 0 labeled ids; Pass 2 extracted 119 quote-pinned rows (`artifacts/inferred-requirements.yaml`). `coverage_degraded: parsed-sparse` (inferred 119 > parsed 0).
- Containment matching: 72/119 matched, `coverage_pct_union = 0.605` (`artifacts/coverage-matrix.yaml`).
- Triage of the 47 unmatched rows (`artifacts/unmapped-triage.yaml`): all 47 are covered by reference (the plan cites the spec section or row range, for example Task 6 "Apply source §1.2 rows 13-18", Task 3 "the seven sections of source §4"). Real gaps: 0.
- Spec task to plan task: §0 gate + baselines → Task 1; T0 → 2; T1 → 3; T2 → 4; T3 → 5; T4 → 6; T5 → 7; T6 → 8; T7 → 9; T8 → 10; T9 → 11; T10 → 12; T11 → 13; T12 → 14.
- Brief requirements: test command in every task's acceptance; commit point every task and an issue-#323 group comment at the last task of each of the 8 phases (groups 0, A-G); decision rules in Constraints (plan:28); final full verification (Task 13).

## Grounding hunks

### .dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/TASK-WF-phase3CodegraphA-20261029-204913.md:1-224

Read the whole plan file; cite by line.

### .dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/source.md:1-79

Spec header, inputs, §0 gate, §1.1 standing rules.

### .dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/source.md:80-134

Spec §1.2 per-primitive table (42 rows) and mirror rule.

### .dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/source.md:135-192

Spec §2 brainstorm (history; §2.2 ideas kept are carried by tasks T10 etc.).

### .dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/source.md:193-263

Spec §3 new commands and §4 shared guide.

### .dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/source.md:264-350

Spec §5 tasks, §6 reporting, §7 autonomy rules.

### .dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/source.md:351-405

Decisions and Review resolution (rationale; requirements they impose are in the sections above).

### .dev/reflect/pre-phase3CodegraphA-20261029205359/artifacts/coverage-matrix.yaml

Containment matrix (72/119 matched).

### .dev/reflect/pre-phase3CodegraphA-20261029205359/artifacts/unmapped-triage.yaml

By-reference triage of the 47 unmatched rows.

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| 119 inferred rows | matrix | 72 containment + 47 by-reference | artifacts/coverage-matrix.yaml, artifacts/unmapped-triage.yaml |
| Group comments 0, A-G at each phase end | brief | covered | plan Tasks 2, 4, 5, 7, 9, 11, 12, 14 |
| Final full verification | brief | covered | plan Task 13 |
