# T1 reflection card (UC-1, pre-execution)

Spec: `.dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/source.md` (55 lines: a revision request listing changes to a first plan, grouped under seven headings)
Plan: `.dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md` (5 phases, 46 tasks, schema workflow-plan/1.2, 552 lines)
Author of this card: the orchestrator that also authored the plan (self-review; the T2 reviewers exist to break that bias).

## Coverage and acceptance

The source has no labelled requirement ids (parsed_count 0). Step 1B.0 Pass 2 emitted 28 quote-pinned inferred rows (`artifacts/coverage-matrix.yaml`, each quote is a verbatim substring of its cited `source.md` line). The deterministic containment rule (60 percent of a quote's content words inside ONE task) matched 20 of 28, so the mechanical `coverage_pct_union` is 0.714. The mechanical rule is noisy on prose requirements: it matched INF-008 (the classifier-inputs supplier), INF-027 (the cap wording pin) and INF-028 (the not-to-be-done list) to the Constraints block rather than to a task, and missed five rows that a manual read maps as follows.

- INF-001 (three owner gates) and INF-002 (remove "run in one pass"): the Constraints bullet "Owner gates" states three gates and does not contain "run in one pass". Covered.
- INF-006 (fresh-findings set): Task 6. INF-018 (escalation-halt offer at the cap sites): Tasks 27, 28, 34 and 37. INF-022 (pins by content): Constraints bullet "Pins are by content" plus the acceptance checks of Tasks 27, 28 and 33. Covered.
- INF-008 (supplier module): Task 20, with Tasks 21 and 22 holding the "only when supplied" tests. INF-027 (cap check uses the task skill's wording): Task 37 acceptance. INF-028: the Constraints "Not built here" bullet. Covered.

## Deviation and risk observations

- Self-trip risk, found while writing this card: Task 13 puts the three merge-rule phrases `highest severity`, `more severe rating` and `higher severity` into `refs/scale-map.md` (its "Merge-rule allow-list" section names them), and Task 40's scan covers every Markdown file under `src/superclaude/skills` and `plugins/superclaude`, with an allow-list that does not list `scale-map.md` (Task 40 lists the auggie file, `refs/rule.md` and its mirror, and the six stage 4 files). The first run of Task 40's test would fail on `scale-map.md` and on its Task 46 plugin mirror unless that file avoids the literal phrases or is allow-listed.
- Ordering risk: Task 46 copies the skill folder into the plugin and then adds a `canonical` registry row to the registry file that the folder copy already contains, while the T15 parity test requires the mirror to equal the source.
- Gate risk: the three owner gates are prose in `## Constraints`; no task checks that a recorded owner go exists before Phase 3, 4 or 5 starts. Task 11 depends on Task 10 but Tasks 26, 31 and 41 carry no dependency on the earlier phase's last task.
- Evidence risk: line numbers named in Tasks 33 to 45 (pragmatic.md 225, 226 and 229; rf-qa 402 and 549; rule-prompt lines near 11, 27, 28) were re-read from disk for the files verified in the pre-check, and are marked "near" for the template and rule-prompt files that were not re-read.
- Dependency risk: the plan cites the spec by section and requirement id (REQ-01 to REQ-30, GR1 to GR12, T1 to T17) without restating them; a reviewer must open the 1,224-line spec to confirm each citation.

## Recommendations

- Rewrite the Task 13 allow-list section so `scale-map.md` does not contain the three phrases literally, or add `scale-map.md` and its plugin mirror to Task 40's allow-list.
- Make Task 46 add the plugin `canonical` row before the copy, or say the copy is repeated after the row is added.
- Add an explicit "owner go recorded in chat" acceptance line to the first task of each gated phase.

## Self-reported confidence

0.80 (self-review by the plan's own author; the mechanical coverage number is a containment-rule artifact, and the template and rule-prompt line numbers were not re-read).
