## Inferred requirements (Pass 2)

Pass 1 (parsed) rows: 9. Pass 2 rows from the requirements-analyst agent: 84; dropped by the parsed-span dedup rule: 35; kept: 49.

### Parsed rows (Pass 1)

| id | lines in source.md | exact-match tasks | note |
|---|---|---|---|
| R-001 | 26,28,42,44 | none | a recommendation label of the first two reviews (R-nnn), not a requirement: false positive of the ID regex |
| R-002 | 29,47 | none | a recommendation label of the first two reviews (R-nnn), not a requirement: false positive of the ID regex |
| R-003 | 30,45 | none | a recommendation label of the first two reviews (R-nnn), not a requirement: false positive of the ID regex |
| R-004 | 31,46 | none | a recommendation label of the first two reviews (R-nnn), not a requirement: false positive of the ID regex |
| R-005 | 32,48 | none | a recommendation label of the first two reviews (R-nnn), not a requirement: false positive of the ID regex |
| R-006 | 33,49 | none | a recommendation label of the first two reviews (R-nnn), not a requirement: false positive of the ID regex |
| R-007 | 26,34,50 | none | a recommendation label of the first two reviews (R-nnn), not a requirement: false positive of the ID regex |
| R-008 | 42 | none | a recommendation label of the first two reviews (R-nnn), not a requirement: false positive of the ID regex |
| REQ-09 | 46 | [7] | REQ-09 is a real spec requirement (cross-run match); Task 7 names it |

### Inferred rows kept (Pass 2)

| INF id | Verbatim quote (prefix, 120 characters at most) | Citation | Match result |
|---|---|---|---|
| INF-001 | This stage creates new files only (the skill folder, new CLI modules, new tests, one doctor check); it edits no review-l | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:3 | mechanical: none (task 7, 0.562); manual: PLAN:20 (Constraints, 'One package, one stage': creates new files only) |
| INF-002 | Generate it only after the owner has read the stage 0 package's `./artifacts/stage0-summary-for-owner.md` and said go in | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:3 | mechanical: containment (task 1, 0.818) |
| INF-003 | and after the stage ledger row for stage 0 has the package id | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:3 | mechanical: containment (task 1, 1.0) |
| INF-004 | Reuse Tasks 11 to 25 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 2, stage 1; found by  | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:7 | mechanical: none (task 9, 0.368); manual: provenance of the base text; no plan line states it; the plan holds Tasks 1 to 15 plus the exit task 16 (PLAN:34-248) |
| INF-005 | Read its `## Constraints` and carry over what applies to stage 1: spec and PF naming, owner-decision defaults, the not-b | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:7 | mechanical: none (task 1, 0.357); manual: Constraints PLAN:17-30 |
| INF-006 | the classifier facts (M, C and E run only with code-supplied inputs; the "M or C is Y gives BLOCKING" row is never enabl | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:7 | mechanical: containment (task 12, 0.632) |
| INF-007 | pins by content, `src/superclaude/` as source of truth with `make sync-dev`, UV only | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:7 | mechanical: none (task 9, 0.5); manual: PLAN:27 (pins by content), PLAN:28 (source of truth, make sync-dev), PLAN:29 (UV only) |
| INF-008 | The stage 0 package's evidence (inventory freeze, availability counts, spec reconciliation) is read by package id. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:7 | mechanical: none (task 1, 0.5); manual: PLAN:19 (earlier-stage evidence read by package id) |
| INF-009 | State this package is stage 1: new files only, no carrier edited, every registry `digest` row stays `legacy`. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:11 | mechanical: containment (task 6, 0.769) |
| INF-010 | The next package (stage 2) starts only after the owner's go in chat. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:11 | mechanical: containment (task 16, 0.667) |
| INF-011 | Drop the base plan's Phase 3 to 5 gate prose. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:11 | mechanical: none (task 2, 0.333); manual: plan has 4 phases (PLAN:32, 118, 145, 216) and no gate prose after Phase 4 |
| INF-012 | The "Merge-rule allow-list" section lists files by path and never writes the three merge-rule phrases or the old definit | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:12 | mechanical: containment (task 3, 0.929) |
| INF-013 | At stage 1 it lists the auggie file, `refs/rule.md` and the six stage 4 files. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:12 | mechanical: containment (task 3, 0.9) |
| INF-014 | Say in the task that the plugin mirror is added in stage 4, not here. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:12 | mechanical: containment (task 3, 0.625) |
| INF-015 | `refs/rule.md` holds the GR5 sentence with the phrase `highest severity` (allow-listed) | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:13 | mechanical: containment (task 2, 0.875) |
| INF-016 | never quotes the old definition sentence "Grade every review finding as blocking or minor" outside the digest's own fenc | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:13 | mechanical: containment (task 2, 0.8) |
| INF-017 | state this as an acceptance line (`grep` of the old sentence over the skill folder prints nothing) | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:13 | mechanical: containment (task 2, 0.8) |
| INF-018 | No file under `src/superclaude/skills/sc-review-severity/` cites a `.dev/` or `./artifacts/` path (acceptance: `grep -rn | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:14 | mechanical: containment (task 5, 0.857) |
| INF-019 | State the M, C and E input rule in words. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:14 | mechanical: containment (task 5, 0.714) |
| INF-020 | Keep exactly 11 `digest` rows, 1 `canonical`, 2 `pointer-only`, 5 `installed-only` (19 rows). | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:15 | mechanical: containment (task 6, 0.923) |
| INF-021 | Say the analysis template is not a carrier row (merge-rule text only in stage 4). | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:15 | mechanical: containment (task 6, 0.667) |
| INF-022 | T3's `src/superclaude` check applies to `digest` and `canonical` rows only | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:16 | mechanical: containment (task 15, 1.0) |
| INF-023 | `pointer-only` and `installed-only` rows are checked for pointer order only, and a `pointer-only` row only once its poin | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:16 | mechanical: containment (task 15, 1.0) |
| INF-024 | the test never reads `~/.claude` | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:16 | mechanical: containment (task 15, 1.0) |
| INF-025 | T2 is non-strict (strict only in stage 4). | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:16 | mechanical: containment (task 15, 0.8) |
| INF-026 | Acceptance includes a temporary-tree test of each exemption. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:16 | mechanical: containment (task 11, 0.6) |
| INF-027 | that a later task of the same package makes false get an end point ("until Task N"). | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:17 | mechanical: none (task 7, 0.5); manual: PLAN:27 (end-point rule); applied at PLAN:129 ('Until Task 10', 'From Task 10 until') |
| INF-028 | New final task: stage 1 exit summary for the owner. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:18 | mechanical: containment (task 16, 0.625) |
| INF-029 | Write `./artifacts/stage1-summary-for-owner.md`: for each task its artifact or file and its observed test result (the co | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:18 | mechanical: containment (task 16, 0.667) |
| INF-030 | the list of files created | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:18 | mechanical: containment (task 16, 1.0) |
| INF-031 | a statement that no carrier was edited (`git diff --stat` over carriers is empty) | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:18 | mechanical: containment (task 16, 0.75) |
| INF-032 | the open items, and the sentence that the owner's go for stage 2 is given in chat and not by this file | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:18 | mechanical: containment (task 16, 1.0) |
| INF-033 | No edit of any carrier (`pragmatic.md`, agents, templates, rule prompts, task skill, tech-research, WORKER-CONTRACT) and | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:22 | mechanical: none (task 4, 0.4); manual: Constraints PLAN:20 and PLAN:22 |
| INF-034 | Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 fix cycles or the 35 percent ta | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:22 | mechanical: none (task 2, 0.364); manual: Constraints PLAN:22 |
| INF-035 | No Jev call, key or account. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:22 | mechanical: none (task 9, 0.5); manual: Constraints PLAN:22 (no Jev call, key or account) |
| INF-060 | Task 3 lists `skills/task/SKILL.md`, `skills/task-builder/` and `agents/rf-task-builder.md` as `exempt-by-retirement` (p | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:35 | mechanical: containment (task 3, 1.0) |
| INF-061 | the exemption ends when the retirement removes the file | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:35 | mechanical: containment (task 3, 1.0) |
| INF-062 | Task 16's carrier diff adds the task-builder folder. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:35 | mechanical: containment (task 16, 0.625) |
| INF-063 | `/sc:implement`'s final review step records and prints only, the offer stays with the top-level session and the consent- | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:36 | mechanical: containment (task 4, 0.938) |
| INF-064 | `tech-research` writes the ledger and neither sweeps nor offers | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:36 | mechanical: containment (task 4, 1.0) |
| INF-065 | `sc-implement-protocol` joins the not-edited list and the Task 16 diff. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:36 | mechanical: none (task 7, 0.429); manual: Constraints PLAN:20, PLAN:25; Task 16 diff PLAN:248 |
| INF-066 | Task 3 no longer says a plugin mirror comes in stage 4 | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:37 | mechanical: containment (task 3, 0.667) |
| INF-067 | Task 6's canonical row has no plugin surface | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:37 | mechanical: containment (task 15, 0.857) |
| INF-068 | Task 16 diff adds `plugins`. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:37 | mechanical: containment (task 16, 0.8) |
| INF-069 | Registry counts unchanged: 11 `digest`, 1 `canonical`, 2 `pointer-only`, 5 `installed-only` (19 rows). | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:37 | mechanical: containment (task 6, 0.846) |
| INF-081 | Task 7's importer list has the end point "until the stage 2 package adds its own importer" | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:53 | mechanical: containment (task 7, 0.917) |
| INF-082 | Tasks 9, 10, 12 and 13 gain a `make lint` acceptance line. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:53 | mechanical: containment (task 7, 0.6) |
| INF-083 | a later `write` or `update_field` never clears a ledger's capture state or a row's tags (the stage 2 package tests it) | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:54 | mechanical: containment (task 7, 0.875) |
| INF-084 | Task 15 names the strict switch of T2 as the constant `STRICT_T2` (default `False`); the stage 4 package sets it `True`. | .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:55 | mechanical: containment (task 15, 0.867) |

### Inferred rows dropped by the parsed-span rule (parsed wins)

Rows whose cited line lies inside the span of a parsed ID (the Revision 2 and Revision 3 bullets that carry R-nnn or REQ-09): INF-036 (line 26), INF-037 (line 26), INF-038 (line 28), INF-039 (line 28), INF-040 (line 29), INF-041 (line 29), INF-042 (line 29), INF-043 (line 30), INF-044 (line 31), INF-045 (line 31), INF-046 (line 31), INF-047 (line 31), INF-048 (line 31), INF-049 (line 32), INF-050 (line 32), INF-051 (line 32), INF-052 (line 33), INF-053 (line 33), INF-054 (line 33), INF-055 (line 33), INF-056 (line 34), INF-057 (line 34), INF-058 (line 34), INF-059 (line 34), INF-070 (line 44), INF-071 (line 45), INF-072 (line 45), INF-073 (line 46), INF-074 (line 46), INF-075 (line 47), INF-076 (line 47), INF-077 (line 48), INF-078 (line 48), INF-079 (line 50), INF-080 (line 50). Their content was checked by hand against the plan (the revision check table in the report).
