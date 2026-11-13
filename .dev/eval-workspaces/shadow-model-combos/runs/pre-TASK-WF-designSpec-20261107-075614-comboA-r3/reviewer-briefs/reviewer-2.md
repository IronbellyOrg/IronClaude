# Reviewer 2 brief — persona: qa — model pin: claude-haiku-5-5 (slot t4) — comboA-r3 shadow panel

## Grounding hunks
Codegraph run state: index_state=fresh, worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel (projectPath for every codegraph call). You are read-only; no Bash/Edit/Write.
ATTRIBUTION RULE (decisive): the plan was authored 2026-11-07 against base e8db2fe6. HEAD c2e3347d (2026-11-13) already contains the implemented feature. Audit the PLAN TEXT vs the SPEC only; never cite HEAD content as evidence of a plan defect. Verified: F12 WRITE_VERB_CLASSIFICATION at tests/skills/test_worker_contract.py:2087; F6 core-purity test rejects gh/git words in core files.

## Inputs (read them)
- Spec: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md (379 lines)
- Plan: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md (201 lines)

## Coverage slice
FR-12..FR-23: foreign toggle detection, ready-then-draft roundtrip disable, unreadable/short timeline never readies, engage failure blocks edits, release retry once, held-exit reporting + clear command + docs, L2 mergeable line, ci cycle ids, resume reconcile reasons, the twelve tests, the pre-build gate record.

## Lens
QA: are the acceptance criteria mechanically checkable — would a WRONG implementation fail them? Find escape hatches, unfailable checks, missing baselines, self-verifying assertions.

## Findings block (MANDATORY output format)
End your reply with a heading exactly `## Findings block` followed by one fenced block with info string `findings-v2` (NOT json), containing ONE JSON OBJECT PER LINE (JSON-lines). Each line has this shape:
{"id":"F1","severity":"MAJOR","blocking":true,"category":"missing-requirement","claim":"<=300 chars","anchor":"12-200 chars","citations":[{"role":"spec","path":"input/TASK-WF-designSpec-20261107-075614/source.md","line_start":6,"line_end":6,"quote":"<=200 chars"}],"coverage_rows":["FR-1"],"lens":"reflect-pre"}
Rules: severity CRITICAL|MAJOR|MINOR uppercase; blocking boolean, MINOR cannot be blocking; category one of contradiction|unpassable-check|data-loss|safety|missing-requirement|other; claim <=300 chars; quote <=200 chars; path repo-relative (input dir = input/TASK-WF-designSpec-20261107-075614/); coverage_rows lists the assigned row ids you verified. Zero findings: emit heading + empty fence, and list verified rows in your prose.
