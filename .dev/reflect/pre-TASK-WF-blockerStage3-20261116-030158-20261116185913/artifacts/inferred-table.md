# Inferred requirements (Pass 2), UC-1

Source: .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/source.md. Match items for the containment rule: the Constraints block and Tasks 1 to 14 of the plan. Quote check at Wave 5: each verbatim quote re-read against its cited line by script.

| INF id | Verbatim quote | Citation | Match result | Quote re-read |
|---|---|---|---|---|
| INF-001 | at least 5 shadow runs have been observed with zero safety misses (by the stage 0 definition) and no capture failure | source.md:3 | CONSTRAINTS (containment 1.00) | verified |
| INF-002 | stage 0b's escape result is written and stage 0c's re-grade is written | source.md:3 | none by the mechanical rule (best CONSTRAINTS 0.50); covered by hand in Task 1 | verified |
| INF-003 | the owner's go in chat is recorded in the stage ledger | source.md:3 | CONSTRAINTS (containment 1.00) | verified |
| INF-004 | The seeded-recall result is produced INSIDE this package (first task) and gates the rule switch by an acceptance line, not by a dependency line. | source.md:3 | CONSTRAINTS (containment 0.79) | verified |
| INF-005 | the stage 2 package's `./artifacts/stage2-summary-for-owner.md` exists and the owner has read it | source.md:3 | CONSTRAINTS (containment 0.88) | verified |
| INF-006 | Stage 4 starts only after one audit window with no revert trigger tripped (the spec's section 13.2 triggers RT1 and RT2) and the owner's go in chat. | source.md:11 | CONSTRAINTS (containment 0.95) | verified |
| INF-007 | State that `/sc:implement` runs the whole package in order, so the rule switch cannot start unless the first tasks pass. | source.md:11 | CONSTRAINTS (containment 0.80) | verified |
| INF-008 | Each pass (old rule text, new rule text) is run with freshly spawned agents, never agents continued from an earlier pass | source.md:12 | T-03 (containment 1.00) | verified |
| INF-009 | the pass order is alternated across the three reviewers | source.md:12 | T-03 (containment 1.00) | verified |
| INF-010 | Write `./artifacts/seeded-recall-result.md` with per-class recall under both texts and the intervals, the cosmetic block share under both | source.md:12 | T-03 (containment 1.00) | verified |
| INF-011 | when a line shows fail, the task's check fails and the run halts for the owner's Ruling | source.md:13 | T-06 (containment 1.00) | verified |
| INF-012 | Do not rely on `Depends on:` for this gate. | source.md:13 | T-03 (containment 0.67) | verified |
| INF-013 | (three bullets replaced, cap and own-scale bullets pinned by content, hook check through `src/superclaude/hooks/hooks.json`) | source.md:13 | T-06 (containment 0.64) | verified |
| INF-014 | reads the allow-list from `refs/scale-map.md` and allow-lists only files that exist in this stage | source.md:14 | CONSTRAINTS (containment 0.86) | verified |
| INF-015 | No plugin mirror is listed (no package makes one). | source.md:14 | CONSTRAINTS (containment 1.00) | verified |
| INF-016 | The existence check applies to every file named in the allow-list and passes in this stage. | source.md:14 | T-05 (containment 0.67) | verified |
| INF-017 | that a later task of the same package makes false get an end point | source.md:15 | CONSTRAINTS (containment 0.88) | verified |
| INF-018 | Write `./artifacts/stage3-summary-for-owner.md` | source.md:16 | T-14 (containment 1.00) | verified |
| INF-019 | and end with the sentence that the owner's go for stage 4 is given in chat and not by this file | source.md:16 | CONSTRAINTS (containment 1.00) | verified |
| INF-020 | the revert triggers RT1 and RT2 with their current state, read from the spec's text and not restated from memory | source.md:16 | T-14 (containment 0.75) | verified |
| INF-021 | No template, rule-prompt, builder, researcher or spec-panel edit (stage 4). | source.md:20 | CONSTRAINTS (containment 1.00) | verified |
| INF-022 | No change to `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the severity code under `src/superclaude/cli/**/*.py`, the cap of 2 fix cycles | source.md:20 | CONSTRAINTS (containment 0.92) | verified |
| INF-023 | No Jev call, key or account. | source.md:20 | CONSTRAINTS (containment 0.75) | verified |
| INF-024 | New Task 1 runs every entry check before any agent is spawned or file is edited. | source.md:28 | CONSTRAINTS (containment 0.85) | verified |
| INF-025 | the stage ledger row for stage 3 carries the owner go, the list of shadow-run folders the owner counted and the owner's safety-confirmation file | source.md:28 | CONSTRAINTS (containment 0.93) | verified |
| INF-026 | the RT5 threshold (75 percent of the M1 mean) | source.md:29 | T-02 (containment 1.00) | verified |
| INF-027 | keeps model class and brief identical across arms | source.md:30 | T-03 (containment 0.86) | verified |
| INF-028 | gains a command, `superclaude review fixcheck` | source.md:31 | T-05 (containment 0.80) | verified |
| INF-029 | adds `--promote` to the one sweep call in `src/superclaude/skills/sc-implement-protocol/SKILL.md` and `refs/managed-workspace.md` | source.md:35 | CONSTRAINTS (containment 0.86) | verified |
| INF-030 | No new plugin surface. | source.md:36 | CONSTRAINTS (containment 0.67) | verified |
| INF-031 | no mapping of `follow-ups.md` to `review-ledger/1` | source.md:39 | CONSTRAINTS (containment 1.00) | verified |
| INF-032 | The seeded-recall gate is now Task 4, a read-only task that edits nothing under `src/`, `tests/` or `plugins/` and runs before every task that edits a rule file | source.md:49 | CONSTRAINTS (containment 0.94) | verified |
| INF-033 | Only a ruling recorded on the stage ledger row (line id, date, SHA-256) counts | source.md:49 | T-03 (containment 1.00) | verified |
| INF-034 | Task 3 now freezes the old-arm and new-arm blocks as copies | source.md:49 | T-03 (containment 0.75) | verified |
| INF-035 | the found threshold fixed before dispatch (more than half of the arm's valid reviewers: 2 of 3 or 2 of 2) | source.md:50 | T-03 (containment 1.00) | verified |
| INF-036 | Tasks 7 and 8 now rewrite principle 8 "NO LENIENCY" and rule 9 "Report honestly" | source.md:51 | T-07 (containment 0.82) | verified |
| INF-037 | Task 12 re-pins that block hash against the new Rule 6, Rule 9 and L3 text | source.md:51 | T-08 (containment 0.92) | verified |
| INF-038 | Task 6 keeps "never to meet a quota" and runs | source.md:57 | T-06 (containment 1.00) | verified |
| INF-039 | Task 6 keeps the sentence "Medium and Note findings are not rechecked in later rounds." after the pointer line. | source.md:59 | T-06 (containment 0.92) | verified |
| INF-040 | Task 14 gives the baseline source of each of M4, M5, M6, M9, M11. | source.md:60 | T-14 (containment 0.82) | verified |
| INF-041 | the L2 text has a missing-command clause (one line in the fix log, carry on) | source.md:66 | T-07 (containment 0.89) | verified |
| INF-042 | Tasks 7 and 8 record kept gates in a section `Kept mechanical gates` at the end of `refs/scale-map.md` | source.md:65 | T-14 (containment 1.00) | verified |
| INF-043 | Task 13 reads only the `Merge-rule allow-list` section. | source.md:65 | CONSTRAINTS (containment 0.83) | verified |
| INF-044 | Tasks 7 to 10 begin by reading that the `pragmatic.md` registry row reads `v2` | source.md:49 | CONSTRAINTS (containment 0.90) | verified |
| INF-045 | a confirmation given to a `/sc:implement` Ruling prompt does not | source.md:49 | CONSTRAINTS (containment 1.00) | verified |
