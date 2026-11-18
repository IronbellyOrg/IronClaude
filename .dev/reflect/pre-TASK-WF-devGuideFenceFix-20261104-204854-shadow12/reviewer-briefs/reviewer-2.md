# Reviewer brief 2 — persona: qa (model class haiku, model claude-haiku-5-5, reviewer_id t4-1)

## T1 card excerpt

```text
## Context
- Spec: 37-line source.md fixing six nested code-fence bugs in the developer guide; fix pattern mirrors Appendix B (four-backtick outer fences). Line-number table for all six pairs.
- Tasklist: 2 tasks, 2 phases, 5 constraints; progress.md PLAN sha256 matches the on-disk plan.
- The work unit was EXECUTED 2026-11-04 (progress.md: T1+T2 compliant, FINAL: pass) and archived. This shadow re-audit checks (a) plan-vs-spec coverage, (b) plan internal quality/fidelity, (c) recorded-evidence corroboration.

## Coverage
parsed=0, inferred=9, all matched; coverage_pct_union=1.0; parsed-sparse.
```

Your lens: coverage and acceptance — audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Verify each AC is mechanically checkable from recorded evidence (fence-before/fence-after, t1-baseline-cmp, guide-diff, dash-check, pytest-docs, changed-files).

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T02:20:11Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

Hunks are cited by repo-relative path; Read them yourself for full context (you are read-only; audit the hunks, the plan file, the package artifacts, and the current tree).

### .dev/tasks/done/TASK-WF-devGuideFenceFix-20261104-204854/source.md:1-37 (SPEC BODY, whole file)

```markdown
# Request: fix the nested code-fence rendering bugs in the developer guide

## What to change and why

In `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, six example file templates are wrapped in a three-backtick outer fence that holds three-backtick inner blocks. The first inner block's bare closing fence closes the outer fence instead, so the rest of the template renders as live Markdown, and the template's own closing fence then opens a new fence that swallows the text after it (for example the `### 2.2 Create a Minimal Agent` heading). The earlier guide refactor reported ten such spots without fixing them: `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-stale-fences.txt`.

The fix is the same one already applied to Appendix B: make each affected outer fence four backticks, opening and closing, so the inner three-backtick blocks nest correctly.

## The six outer fences (guide line numbers as of 2026-11-04, after the refactor)

| Template | Opening line (today) | Closing line (today) |
|---|---|---|
| 2.1 Quick Start command template (`src/superclaude/commands/hello.md` example) | 136 (```markdown) | 177 (```) |
| Section 10, Example 1 command file | 1322 (```markdown) | 1379 (```) |
| Section 10, Example 2 command file | 1435 (```markdown) | 1501 (```) |
| Section 10, Example 2 skill file (`sc-pr-review/SKILL.md`) | 1505 (```markdown) | 1605 (```) |
| Section 10, Example 3 command file (`adversarial.md`) | 1615 (```markdown) | 1674 (```) |
| Section 10, Example 3 `refs/agent-specs.md` | 1828 (```markdown) | 1884 (```) |

Each opening line becomes four backticks plus `markdown`; each closing line becomes four backticks. Confirm each pair by reading the guide before editing; if a line number has moved, find the pair by its template and say so in the task notes.

## Checks

- Re-use the existing fence-state script `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-fence-check.py` (copy it into this plan's package `./artifacts/`, do not edit the archived copy) and run it with `uv run python -I` on the guide before and after the edits. After the edits its "Inner fence closes outer fence" section prints `none`, the headings `### 2.2 Create a Minimal Agent`, `### Example 2: ...` and `### Example 3: ...` are outside any fence, and Appendix B and Appendix C keep the state they have today (Appendix B inside its four-backtick fence, Appendix C heading outside).
- The guide's diff against its state before this plan (the earlier refactor is still uncommitted, so compare with a copy saved before the first edit, not with `HEAD`) changes exactly the twelve fence lines above and nothing else; save that diff under `./artifacts/`.
- `uv run pytest tests/docs -q` passes.

## Out of scope

- Any other line of the guide, including prose and the inner code blocks.
- Any other file.

## Constraints

- Only `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` changes; scripts and evidence go under the plan package's `./artifacts/`.
- No em dash and no en dash in changed lines.
- `.dev/tasks/` is always staged (`git add .dev/tasks`); staging is not committing; commit only when the user asks.
```

### .dev/tasks/done/TASK-WF-devGuideFenceFix-20261104-204854/artifacts/coverage-matrix rows (the matrix under audit)

```text
INF-001 four-backtick outer fences (source.md:7) -> Task 1, Task 2
INF-002 the six fence pairs table (source.md:9-18) -> Task 1, Task 2
INF-003 confirm pairs / moved line numbers in notes (source.md:20) -> Task 1, Task 2
INF-004 reuse archived fence script, copy never edit, run before+after (source.md:24) -> Task 1, Task 2
INF-005 fence-after none + named headings outside + Appendix B/C state (source.md:24) -> Task 1, Task 2
INF-006 diff vs saved baseline = exactly twelve fence lines (source.md:25) -> Task 1, Task 2
INF-007 pytest tests/docs -q passes (source.md:26) -> Task 2
INF-008 no other line of the guide, no other file (source.md:30-31) -> Task 2
INF-009 no em/en dash; staging rule (source.md:36-37) -> Task 2, Constraints
parsed=0, inferred=9, coverage_pct_union=1.0, S_dev_density=0.0
```

### .dev/tasks/done/TASK-WF-devGuideFenceFix-20261104-204854/TASK-WF-devGuideFenceFix-20261104-204854.md:28-50 (both tasks with acceptance criteria)

```text
Task 1 (L28-35): baseline copy + script copy + fence-before; fix 136/177; AC1 byte-identical baseline + fence-before lists the 2.1 spot; AC2 2.1 template opens ````markdown and closes ```` , 2.2 heading outside, no spot opened at 136/177; AC3 t1-diff exactly two lines.
Task 2 (L39-50): five section-10 pairs (1322/1379, 1435/1501, 1505/1605, 1615/1674, 1828/1884), located by **File**: line on drift, recorded in t2-notes; AC1 fence-after none + headings outside + Appendix B inside four-backtick fence + Appendix C outside; AC2 guide-diff exactly twelve lone-fence lines; AC3 dash grep no output; AC4 pytest tests/docs passes; AC5 git-status shows no change outside the guide other than the already-staged memory file.
```

### .dev/tasks/done/TASK-WF-devGuideFenceFix-20261104-204854/artifacts/fence-after.txt:280-281 (the none-state check)

```text
## Inner fence closes outer fence
none
```

### .dev/tasks/done/TASK-WF-devGuideFenceFix-20261104-204854/artifacts/fence-after.txt (heading states, excerpt)

```text
L20: L179: ### 2.2 Create a Minimal Agent  [outside]
L142: L1316: ### Example 1: Simple Command + Agent (Beginner)  [outside]
L157: L1429: ### Example 2: Medium Command + Skill with Compliance (Intermediate)  [outside]
L181: L1609: ### Example 3: Complex Command + Skill + Agents with Refs (Advanced)  [outside]
L215: L1837: ### Examples  [inside fence opened at line 1828 (````markdown)]
L258: L2080: ## Appendix B: Command Template  [outside]
L267-268: L2092 headings inside ````markdown fence from 2082; L2148: ## Appendix C: Agent Template  [outside]
```

## Coverage slice

| Requirement | Matched | Grounding |
|---|---|---|
| INF-001 four-backtick outer fences, opening and closing | Task 1, Task 2 | plan:30,43 |
| INF-002 the six fence pairs with line numbers | Task 1, Task 2 | plan:30,43 |
| INF-003 confirm pairs by reading; moved line numbers recorded in notes | Task 1, Task 2 | plan:30,43 |
| INF-004 reuse archived fence script (copy, never edit), run before and after | Task 1, Task 2 | plan:21,30,43 |
| INF-005 fence-after none-state + headings outside + Appendix B/C unchanged | Task 1, Task 2 | plan:34,46 |
| INF-006 diff vs saved baseline changes exactly twelve fence lines | Task 1, Task 2 | plan:35,47 |
| INF-007 pytest tests/docs passes | Task 2 | plan:49 |
| INF-008 no other line/file changes | Task 2 | plan:47,50 |
| INF-009 no em/en dash in changed lines; staging rule | Task 2, Constraints | plan:48,24 |

All 9 inferred rows matched; coverage_pct_union 1.0; parsed=0 (parsed-sparse). If a requirement-bearing spec span is missing from this matrix, that is your primary finding.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.
