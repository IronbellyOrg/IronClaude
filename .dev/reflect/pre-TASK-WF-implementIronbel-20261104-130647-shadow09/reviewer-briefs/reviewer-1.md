# Reviewer brief — reviewer-1 (persona: analyzer, model class: sonnet)

Run: /sc:reflect --mode pre --tier 2 --t2-engine shadow (run id 2026-11-13T01:13-shadow09)
You are reviewer-1 of 3 in a Tier-2 heterogeneous UC-1 pre-execution audit.

## Mission
Audit the PLAN (a workflow tasklist) against its driving SPEC for coverage and internal fidelity, BEFORE re-execution. The package is archived (work already executed once); audit the plan-as-written, using the on-disk repo state and the package's artifacts/amendments.md ONLY as evidence of what the plan's text actually required and where it fell short. A defect that the implement-time amendments later fixed is STILL a plan finding (the plan text is the object under audit); record it and cite both the plan line and the amendment row.

## Inputs (Read these yourself; cite with repo-relative paths)
- SPEC (1 line, incorporates issue #357 by reference): .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/source.md
- Issue #357 Done-when (the acceptance criteria): run `gh issue view 357 --repo IronbellyOrg/IronClaude` if available; otherwise the tasklist Constraints section quotes it verbatim at .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md:19
- PLAN (the object under audit): .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md
- Implement-time amendments: .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/artifacts/amendments.md
- Progress ledger: .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/progress.md

## Codegraph run state (pass as projectPath on every codegraph call; index is fresh)
- index_state: fresh, checked_at: 2026-11-13T01:11:33Z, worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

## Grounding hunks (verified by the orchestrator; re-Read before citing)
- src/superclaude/hooks/hooks.json:95-103 — shipped PreToolUse Bash registration of block-bare-python.sh (timeout 3), exactly one entry
- src/superclaude/cli/install_hooks.py:85 — "block-bare-python.sh" in _FRESHNESS_SCRIPTS
- src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md:8 — now uv run --no-project python -c
- src/superclaude/hooks/scripts/block-bare-python.sh:1-30 — header documents decision contract, awk scanner, fail-open
- tests/hooks/test_block_bare_python.py — 268 lines, 6 test functions, 3 parametrized tables (BLOCKED/ALLOWED/FAIL_OPEN)
- CHANGELOG.md:137-146 — shipped #357 section under [Unreleased]
- .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/artifacts/t7-summary.md — fresh-session + subagent proof, live ~/.claude untouched
- .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/artifacts/amendments.md — AMD-01..AMD-08 + M-CONSTRAINTS/R1-F7/R1-F10/M-CEILINGS from the advisory pre-reflect

## Coverage slice (your assigned requirement rows; report observed subset in coverage_rows)
- INF-001: PreToolUse Bash hook blocks bare python/python3/pip/pip3 command words, message names `uv run python` and `jq` (spec:1; plan:32-43)
- INF-002: allows uv run python / uv pip / uvx; never blocks text-only mentions in args, paths, patterns, quoted text (spec:1; plan:37-39, Task 2 allowed list plan:58)
- INF-007: deliverable file surface: hook script src+plugins byte-identical, hooks.json registration both copies, installer _FRESHNESS_SCRIPTS entry (spec:1; plan:32,46,73-77)
Probe hypotheses (verify independently, keep only what the evidence supports; add your own):
- H-A1: plan:37 rule "text inside double quotes is never a command word" contradicts executable substitution inside double quotes (x="$(python3 -c 1)"); AMD-04 had to reverse it. Category contradiction.
- H-A2: plan:41 requires jq-or-awk tokenising; shipped header says one stateful awk scanner — consistency check only.

## Findings output contract (MANDATORY — a nonconforming block is discarded)
End your reply with ONE fenced block whose info string is exactly `findings-v2`, containing one JSON object per line (JSON-lines, no pipes, no prose inside the fence). Each line:
{"id":"R1-F1","severity":"MAJOR|MINOR|CRITICAL","blocking":true|false,"category":"contradiction|unpassable-check|data-loss|safety|missing-requirement|other","claim":"<=300 chars","citations":[{"role":"plan|spec|source|test|diff|artifact","path":"repo-relative","line_start":N,"line_end":N,"quote":"<=200 chars"}],"lens":"reflect-pre","coverage_rows":["INF-001"],"self_confidence":0.0-1.0}
Rules: id matches ^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$; MINOR cannot be blocking; 1-8 citations each; paths repo-relative (the plan is `.dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md`); line ranges must be integers with start<=end; quote text verbatim from those lines (<=200 chars). Before finishing, re-Read every file:line you cite and make the quote match. Also state in one line above the fence: which assigned coverage rows you verified as covered (or flag missing-requirement findings for uncovered ones).
Read-only audit: you have no Bash/Write; return findings in your final message only.
