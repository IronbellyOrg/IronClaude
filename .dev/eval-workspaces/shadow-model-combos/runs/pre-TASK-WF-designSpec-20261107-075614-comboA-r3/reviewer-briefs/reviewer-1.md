# Reviewer 1 brief — persona: analyzer — model pin: claude-sonnet-5-5 (slot t1b) — comboA-r3 shadow panel

## Grounding hunks
Codegraph run state: index_state=fresh, worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel (projectPath for every codegraph call). You are read-only; no Bash/Edit/Write.
ATTRIBUTION RULE (decisive): the plan was authored 2026-11-07 against base e8db2fe6. HEAD c2e3347d (2026-11-13) already contains the implemented feature (merge_guard.py exists, len(EventType)==45). Audit the PLAN TEXT vs the SPEC only; never cite HEAD content as evidence of a plan defect. Spec facts verified: F4 CONFLICT_CYCLE_PREFIXES=("sync-","conflict-") conflicts.py:46; F13 BRANCH_A_LANDED="landed" recovery.py:40; F5 --conflict-max-tier fsm.py:108.

## Inputs (read them)
- Spec: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md (379 lines)
- Plan: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md (201 lines)

## Coverage slice
FR-1..FR-11: ordinals 0-2/off no-op, engage at end of Wave 3 per routed finding, preexisting draft preserved, crash/resume authority, release only on confirmed push or zero-edit proof, release before reply/re-trigger, pr_not_open halt, moved head.

## Lens
Analyzer: does every spec requirement in your slice reach a task plus an acceptance criterion? Find unmapped or contradicted requirements.

## Findings block (MANDATORY output format)
End your reply with a heading exactly `## Findings block` followed by one fenced block with info string `findings-v2` (NOT json), containing ONE JSON OBJECT PER LINE (JSON-lines). Each line has this shape:
{"id":"F1","severity":"MAJOR","blocking":true,"category":"missing-requirement","claim":"<=300 chars","anchor":"12-200 chars","citations":[{"role":"spec","path":"input/TASK-WF-designSpec-20261107-075614/source.md","line_start":6,"line_end":6,"quote":"<=200 chars"}],"coverage_rows":["FR-1"],"lens":"reflect-pre"}
Rules: severity CRITICAL|MAJOR|MINOR uppercase; blocking boolean, MINOR cannot be blocking; category one of contradiction|unpassable-check|data-loss|safety|missing-requirement|other; claim <=300 chars; quote <=200 chars; path repo-relative (input dir = input/TASK-WF-designSpec-20261107-075614/); coverage_rows lists the assigned row ids you verified. Zero findings: emit heading + empty fence, and list verified rows in your prose.
