ROUND 2.5: INVARIANT PROBE — FAULT-FINDER AGENT. You are an independent fault-finder, not an advocate. Read-only: do not edit or write any file.

Inputs (Read): /home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule/.dev/reflect/pre-removeTheAnyIssu-20261101225845/adversarial/debate-transcript.md (Round 1, Round 2, and the "Convergence after Round 2" consensus at the end) and diff-analysis.md in the same folder. The debate is about defects in the plan /home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule/.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261101-225635/TASK-WF-removeTheAnyIssu-20261101-225635.md (spec: source.md in the same folder; site list .dev/review-severity-rule/inventory.md). You may Read any repo file (paths relative to /home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule).

The consensus claims that fixing the 7 blocking points (C-001 hash re-pin, C-002 lines 1349/2034 in Task 8 and Task 11 plus a wider cap regex, C-004 prd max_research_fix_cycles 3->2, C-005 prd/prompts.py:1173, C-007 S1-S3 in skill_template.md, C-008 R-008 grep header bug, X-002) makes every task's checks passable and the plan Goal true. Probe that consensus.

Probe each category and find specific assumptions that could be violated:
CATEGORY 1 STATE VARIABLES (e.g. .claude mirror state, sha pins, test fixtures shared across tasks).
CATEGORY 2 GUARD CONDITIONS (acceptance greps/tests that can never pass, or pass vacuously).
CATEGORY 3 COUNT DIVERGENCE (fix cycles vs reviews: "max N cycles" semantics, loops like `range(max_cycles + 1)`, off-by-one between 2 fix cycles and 3 reviews).
CATEGORY 4 COLLECTION BOUNDARIES (site lists that miss members: other "3 cycles" or old-rule wordings in src/superclaude not in any task; tests pinning lowered numbers, e.g. prd tests asserting max_research_fix_cycles == 3).
CATEGORY 5 INTERACTION EFFECTS (two tasks editing the same line; task ordering so a task's own acceptance fails).
CATEGORY 6 SUFFICIENCY CHALLENGE: name at least one downstream condition that would make "fixing the 7 points is sufficient" false, with source evidence (grep results, file:line). Do not assert "none" without evidence.

Output, one entry per finding (max 12 entries, under 60 lines):
ID: INV-NNN | CATEGORY | ASSUMPTION | STATUS: ADDRESSED or UNADDRESSED | SEVERITY: HIGH, MEDIUM or LOW | EVIDENCE: file:line you Read or grep you ran.
End with a 2-line summary: counts by status and severity.