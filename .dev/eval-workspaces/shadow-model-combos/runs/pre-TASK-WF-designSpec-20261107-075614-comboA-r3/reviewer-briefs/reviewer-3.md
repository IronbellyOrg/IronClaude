# Reviewer 3 brief — persona: refactorer — model pin: claude-opus-5-5 (slot t1a) — comboA-r3 shadow panel

## Grounding hunks
Codegraph run state: index_state=fresh, worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel (projectPath for every codegraph call). You are read-only; no Bash/Edit/Write.
ATTRIBUTION RULE (decisive): the plan was authored 2026-11-07 against base e8db2fe6. HEAD c2e3347d (2026-11-13) already contains the implemented feature. Audit the PLAN TEXT vs the SPEC only; never cite HEAD content as evidence of a plan defect.

## Inputs (read them)
- Spec: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md (379 lines, sections 6, 8, 10 carry the plan-authoring requirements)
- Plan: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md (201 lines)

## Coverage slice
INF-1..INF-7: owner decisions fixed (header line 6), sync-dev + verify-sync + full-suite-vs-baseline discipline (spec:301,363-365), symbol-name citations + one Depends-on per dependency (spec:362-363), classification entries added last (spec:255), build with no GitHub calls + release gate (spec:326), SKILL.md pin discipline (spec:241), test-hygiene notes (spec:377: no imported test_*, RunLog.read_events assertions, string-constant byte-identical checks).

## Lens
Refactorer: cross-cutting integrity. Are the process constraints carried into enforceable task steps? Are task dependencies complete and correctly ordered? Does any task consume output another task has not produced?

## Findings block (MANDATORY output format)
End your reply with a heading exactly `## Findings block` followed by one fenced block with info string `findings-v2` (NOT json), containing ONE JSON OBJECT PER LINE (JSON-lines). Each line has this shape:
{"id":"F1","severity":"MAJOR","blocking":true,"category":"missing-requirement","claim":"<=300 chars","anchor":"12-200 chars","citations":[{"role":"spec","path":"input/TASK-WF-designSpec-20261107-075614/source.md","line_start":6,"line_end":6,"quote":"<=200 chars"}],"coverage_rows":["FR-1"],"lens":"reflect-pre"}
Rules: severity CRITICAL|MAJOR|MINOR uppercase; blocking boolean, MINOR cannot be blocking; category one of contradiction|unpassable-check|data-loss|safety|missing-requirement|other; claim <=300 chars; quote <=200 chars; path repo-relative (input dir = input/TASK-WF-designSpec-20261107-075614/); coverage_rows lists the assigned row ids you verified. Zero findings: emit heading + empty fence, and list verified rows in your prose.
