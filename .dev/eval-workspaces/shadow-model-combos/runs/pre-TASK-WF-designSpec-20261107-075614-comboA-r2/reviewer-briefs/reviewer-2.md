# Reviewer 2 brief - persona: qa

Audit target: UC-1 pre-execution. Spec = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (design spec v3, issue #375, pr-submit merge guard). Plan = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (13 tasks, 5 phases).

ATTRIBUTION NOTE (binding): this is a PRE-execution audit of the frozen spec+plan pair. The spec's facts F1-F13 are pinned at base commit e8db2fe6 (2026-11-07); verify anything pre-landing with `git show e8db2fe6:<path>` if needed. HEAD has since evolved (the feature landed); do NOT file findings that rest on HEAD source text - audit the plan's coverage against the frozen spec only. NEVER read anything under .dev/tasks/done/TASK-WF-designSpec-20261107-075614/ (it is the implement-history answer key).

Your lens: requirement coverage, missing deliverables, unpassable or escape-hatch acceptance criteria, test-design completeness. The spec's traceability table (source.md:346-356) maps FR-1..FR-23 to sections; the files-to-change table (source.md:283-301) enumerates deliverables; section 7 enumerates the 12 minimum tests; section 8 the gates; sections 4.5-4.6 protocol/docs deliverables.
## T1 card excerpt
Verbatim excerpt from t1-card.md (coverage-relevant slice):

> ## Coverage (Wave 1B, Step 1B.0 two-pass)
>
> - Pass 1 (deterministic): 0 parsed IDs in BOTH docs - the spec labels requirements `FR-1..FR-23`, outside `ID_REGEX` (`R-|REQ-|SPEC-|T-`). `coverage_pct` (parsed-only) = null.
> - Pass 2 (requirements-analyst, quote-pinned): 45 rows INF-001..INF-045, every row quote+citation verified.
> - Deterministic containment floor: 26/45 matched (0.5778), 19 unmapped, S_dev_density 0.4222.
> - Step 1B.2b: inferred 45 > parsed 0 -> `coverage_degraded: parsed-sparse`.
>
> ### Semantic resolution of the 19 floor-unmapped rows (T1 judgment, all resolved COVERED)
>
> The containment rule under-matches cross-cutting constraints restated at PLAN level (Constraints section) rather than inside one task. Resolutions: INF-001 -> plan Goal + Constraints owner-decisions line; INF-003 -> Constraints purity + Task 10 overlay; INF-004 -> Task 4 AC + Task 11; INF-009 -> Constraints + Task 3; INF-011 -> Task 3/4; INF-012 -> Task 3 AC; INF-015 -> Task 2; INF-016 -> Task 8; INF-019 -> Task 3 fold AC; INF-030 -> Constraints + Tasks 7/8/9/12; INF-033 -> Task 11 AC; INF-034 -> Constraints; INF-035 -> Task 11 AC (12 test names); INF-039 -> Task 1 O4 + Task 10; INF-040 -> Constraints; INF-041 -> dependency graph verified complete; INF-042 -> Tasks 3/4 ACs; INF-043 -> Constraints; INF-044 -> Task 11 AC.
>
> Coverage after semantic resolution: 45/45 = 1.0 (deterministic floor 0.5778; resolution is T1 judgment, to be pressure-tested by the T2 panel).
>
> ## Hypotheses
>
> - **H2 [MINOR - method transparency]** The deterministic containment floor reports 0.5778 with 19 unmapped rows that all resolve semantically; a consumer reading `coverage_pct_union` without the resolution table would misread plan quality.
> - **H4 [MINOR - scope note]** `test_allowed_tools_cover_every_program` scans only the two conflict refs; refs/merge-guard.md fenced commands are covered instead by Task 8's own protocol test. Residual exposure: nothing checks the new ref's fenced programs against the SKILL front-matter grants; Task 1 O2 is the plan's own resolution path.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.
Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T04:05:44Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### Spec body part 1 - source.md:1-189 (header/owner decisions, facts F1-F13, component overview, behaviour table, section 4.1 decision tables, 4.2 start)

The FULL spec text source.md:1-378 is on disk at the path above; Read it in full yourself (it is 378 lines). Key anchors for your slice: owner decisions L6; repo-scoping F7 L23; behaviour table L55-69; purity/imports L75; decision contracts L101-171; events/fold L173-208; flag L212-217; script L219-234; protocol/docs table L236-247; cycle identity L249-251; classification L253-255; sequences L257-281; files-to-change L283-301; test design L303-322; gates L324-342; traceability L344-356; plan-authoring L358-378.

## Coverage slice

Your assigned rows (INF ids from the union matrix; all 45 rows resolved COVERED at T1 - your job is to pressure-test that resolution for YOUR rows):

INF-022..INF-038 (17 rows: merge-guard.md ref, SKILL.md bullets+tables, command file, user guides, output field, cycle identity, WRITE_VERB discipline + add-last, acceptance trace, published path, sync cadence, 12 minimum tests, crash-boundary ACs, release gate, unverified-until statement)

The full matrix with per-row quotes is at artifacts/coverage-matrix.yaml and artifacts/pass2-inferred.yaml (Read them if you need the row quotes).

Report each finding as one JSON line per the instruction above. A zero-finding result is valid; if you verify your rows are covered, return an empty findings block and list the row ids you verified under `coverage_rows` in EACH finding only when you have a finding; for a zero-finding card write exactly `[]` inside the fence plus your `coverage_rows_observed` line AFTER the fence as a plain line listing the INF ids you checked.
