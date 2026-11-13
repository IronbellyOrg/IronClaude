# Reviewer 2 (qa, model_class: haiku, model: claude-haiku-5-5) card

persona: qa
model_class: haiku
model: claude-haiku-5-5

## Scope checked

- Read brief, source.md (as quoted), full plan (169 lines), progress.md ledger, and artifacts: t1-checks, t2.diff, t2-few-files, t3-consistency, t3-tests, t4-checks, t4-recommend-walk, t5.diff, t5-checks, t5-tests, t6.diff, t6-sweep, t7.diff, t7-regression, t7-tests. Not read: t7-manual-check.md, t1.diff, t3.diff (apart from grep), t4.diff, t3-sync, t4-sync, *-extras.log, return-contract.yaml.

## Matrix versus spec body

- source.md has six requirement-bearing spans; the six matrix rows (INF-001..INF-006) map one for one. No span absent from the matrix.
- Caveat 1: FR-ONB.1 spec not on disk; INF-002 ("every bullet and AC of FR-ONB.1") is an omnibus row mapped to Tasks 1-7; whether each FR-ONB.1 bullet has a task cannot be checked here.
- Caveat 2 (F4): INF-003 ("Part A rows of section 4.2") maps only to Task 1 (plan:19, plan:42); the plan never lists those rows; their targets (SKILL, prompts, docs) belong to Tasks 4-6.

## AC versus ledger

- Five AC/evidence defects, all minor (F1, F2, F3, F5, F6) plus the F4 coverage note. No unpassable check, no ordering defect.
- C-04 candidate confirmed as ledger-semantics note only (progress.md:36,38 test:fail beside compliant), not a defect.

## Findings block

```findings-v2
{"id":"F1","severity":"MINOR","blocking":false,"category":"contradiction","claim":"T5.AC2 ('closed key list and classifier examples are unchanged') is anchored to t5-checks.log:5-6, which says no key-list lines changed, yet t5.diff shows the task-file-generation key-list description lines were rewritten (the plan itself requires that rewrite), so the evidence is ambiguous or inaccurate.","citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/TASK-WF-implementFrOnb1O-20261023-180618.md","line_start":133,"line_end":138},{"role":"artifact","path":".dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/artifacts/t5-checks.log","line_start":5,"line_end":6},{"role":"diff","path":".dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/artifacts/t5.diff","line_start":9,"line_end":14}],"self_confidence":0.6}
{"id":"F2","severity":"MINOR","blocking":false,"category":"missing-requirement","claim":"Task 7 requires a CHANGELOG.md entry, but no T7 acceptance criterion covers it and the ledger records no evidence anchor for it, although CHANGELOG.md is listed in T7 files (t7.diff does contain the entry).","citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/TASK-WF-implementFrOnb1O-20261023-180618.md","line_start":160,"line_end":168},{"role":"artifact","path":".dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/progress.md","line_start":48,"line_end":48}],"self_confidence":0.7}
{"id":"F3","severity":"MINOR","blocking":false,"category":"missing-requirement","claim":"Plan bullets with no matching AC: T4 bullet 2 (make simple-plan the default in the level 3-or-4 offers), T5's key-description reword, and the post-T3 removal of the 'few files' routing-row hits that t2-few-files.log deferred to Task 3; T3's ACs contain no 'few files' re-check.","citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/TASK-WF-implementFrOnb1O-20261023-180618.md","line_start":113,"line_end":124},{"role":"plan","path":".dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/TASK-WF-implementFrOnb1O-20261023-180618.md","line_start":99,"line_end":105},{"role":"artifact","path":".dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/artifacts/t2-few-files.log","line_start":2,"line_end":3}],"self_confidence":0.6}
{"id":"F4","severity":"MINOR","blocking":false,"category":"missing-requirement","claim":"Matrix row INF-003 (Part A rows of section 4.2, wording approved incl. the level 5 re-point) maps only to Task 1, but the plan never enumerates those 4.2 rows and their targets (SKILL, prompts, docs) belong to Tasks 4-6, so coverage of this span is asserted rather than shown.","citations":[{"role":"spec","path":".dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/source.md","line_start":1,"line_end":1},{"role":"plan","path":".dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/TASK-WF-implementFrOnb1O-20261023-180618.md","line_start":19,"line_end":19}],"self_confidence":0.4}
{"id":"F5","severity":"MINOR","blocking":false,"category":"other","claim":"T6.AC1 and T6.AC2 anchors do not prove the ACs. AC1 cites only 5 of the 10 listed doc lines (commands.md 294, 506, 551, 806 and 927 are unanchored; the diff does show them edited). AC2 cites t6-sweep.log:1, a single hit line, though the log has no per-hit verdict.","citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/TASK-WF-implementFrOnb1O-20261023-180618.md","line_start":146,"line_end":153},{"role":"artifact","path":".dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/progress.md","line_start":46,"line_end":46},{"role":"artifact","path":".dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/artifacts/t6-sweep.log","line_start":1,"line_end":22}],"self_confidence":0.6}
{"id":"F6","severity":"MINOR","blocking":false,"category":"other","claim":"T2.AC4 (3.1 steps 2-11 byte-unchanged) is anchored to HOW-WE-WORK.md:53, the one edited line of 3.1, which cannot prove the rest is unchanged. AC3's 3.7 and 3.8 sub-items are not anchored (only lines 128 and 203). t2.diff supports both claims, but the ledger anchors do not.","citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/TASK-WF-implementFrOnb1O-20261023-180618.md","line_start":67,"line_end":73},{"role":"artifact","path":".dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/progress.md","line_start":38,"line_end":38}],"self_confidence":0.5}
```

calibration:
```yaml
per_finding: {}
```

reviewer_model_self_report: claude-gw-tier1b[1m] (Claude, via the claude-gw-tier1b gateway)
