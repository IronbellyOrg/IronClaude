# Walk-through: /sc:recommend match rules on the spec's manual-check request

Request: "Add CSV export to the invoices list; touches 6 files; spec at docs/specs/x.md"
Rules: src/superclaude/skills/sc-recommend/SKILL.md:58 (match by intent phrase; prefer the more specific phrase that names an artifact; then the level tie rule) and :60 (hard limit for level 1-2 rows).
Table: src/superclaude/core/HOW-WE-WORK.md routing table after Tasks 1-3 (lines 318-326).

| Row (line) | Level | Intent phrases | Matches the request? |
|---|---|---|---|
| small-change (319) | 2 | one source file plus its test; five edits or fewer; exact change known | No: 6 files |
| simple-plan (320) | 3 | planned change; clear requirements; many files; more than one session | Yes: "planned change", "many files" (6 files) |
| task-file (321) | 4 | whole project built from scratch; major component built from scratch; nearly needs a PRD and TDD | No: adds a feature to an existing list; nothing is built from scratch and no PRD/TDD is implied |
| feature-existing (322) | 3 | add a feature to an existing system; requirements clear; spec file exists; no PRD | Yes: "add a feature to an existing system", "spec file exists" (docs/specs/x.md) |
| research-first (323) | 5 | how does our system work; is it feasible; what would need to change | No |

Step 1 (more specific phrase wins): feature-existing's "spec file exists" names an artifact (the spec), so feature-existing is preferred over simple-plan.
Step 2 (level tie rule): not reached. Had the two still tied, both are level 3; and the edited tie rule (SKILL.md:58) means a level-4 row never wins a tie against a level-3 row.
Step 3 (hard limit, SKILL.md:60): applies only to level 1-2 matches; not applicable.

Result: row feature-existing, level 3: `/sc:workflow <spec file>` then `/sc:implement .dev/tasks/to-do/<id>/<id>.md`. The request does NOT land on task-file (/task-builder). Before Tasks 1-4, the old task-file intent ("many files; more than one session; must not drift") matched "touches 6 files" and the old tie rule chose the higher level, which is the behaviour the spec's manual check (spec.md:183) guards against.
