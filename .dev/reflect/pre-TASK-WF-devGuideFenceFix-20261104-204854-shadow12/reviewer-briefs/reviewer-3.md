# Reviewer brief 3 — persona: refactorer (model class opus, model claude-opus-5-5, reviewer_id t1a-1)

## T1 card excerpt

```text
## Context
- Spec: 37-line source.md fixing six nested code-fence bugs in the developer guide; fix pattern mirrors Appendix B (four-backtick outer fences). Line-number table for all six pairs.
- Tasklist: 2 tasks, 2 phases, 5 constraints; progress.md PLAN sha256 matches the on-disk plan.
- The work unit was EXECUTED 2026-11-04 (progress.md: T1+T2 compliant, FINAL: pass) and archived. This shadow re-audit checks (a) plan-vs-spec coverage, (b) plan internal quality/fidelity, (c) recorded-evidence corroboration.

## Findings (candidates; reviewers pressure-test)
- C-04 [residue] Fix persists at HEAD: current guide has all six fixed pairs (136/177, 1303/1360, 1416/1482, 1486/1586, 1596/1655, 1809/1865) plus Appendix B (2063/2127). ACs frozen at execution time are not re-runnable against HEAD; anchor on package artifacts.
- C-05 [plan-quality, minor candidate] Task 2's AC references "### Example N:" headings generically; a future "Example 4" heading inside a four-backtick template would still pass the wording as written.
- C-06 [process, minor candidate] Task 2's git-status AC names a run-specific staged-file exception; in a clean checkout the exception is vacuous.
- C-07 [process, minor candidate] FINAL: issues round cites retries/T1/prompt-1-1.md and retries/T2/prompt-1-1.md, later moved unchanged to superseded-prompts/; the first FINAL's evidence paths now dangle.
```

Your lens: structural and process quality — the plan's operational design (baseline snapshot against uncommitted state, byte-exact script copy, diff-by-copy instead of HEAD, superseded-prompt archival) and its residue on the current tree. Judge C-04 (frozen ACs vs moved HEAD), C-06 (baked-in worktree state), C-07 (dangling evidence paths after the user-confirmed move).

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T02:20:11Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

Hunks are cited by repo-relative path; Read them yourself for full context (you are read-only; audit the hunks, the plan file, the package artifacts, and the current tree).

### .dev/tasks/done/TASK-WF-devGuideFenceFix-20261104-204854/source.md:1-37 (spec body, whole)

```text
See the file; 37 lines. Fix statement L7; six-fence table L11-18; confirm-pairs rule L20; checks L24-26 (script reuse, none-state, twelve-line diff, pytest); out of scope L30-31; constraints L35-37.
```

### .dev/tasks/done/TASK-WF-devGuideFenceFix-20261104-204854/TASK-WF-devGuideFenceFix-20261104-204854.md:17-50 (constraints + both tasks)

```text
Constraints L19-24: only the guide changes, twelve fence lines only, script copy (never edit archived), guide-before.md baseline because the earlier refactor is uncommitted, no dash, staging rule. Task 1 L28-35; Task 2 L39-50 with AC1-AC5 and the staged-memory-file exception on L50.
```

### .dev/tasks/done/TASK-WF-devGuideFenceFix-20261104-204854/progress.md:11-12 (the FINAL: issues + ARCHIVE ruling pair)

```text
FINAL: issues evidence=./artifacts/retries/T1/prompt-1-1.md:727-728,./artifacts/retries/T2/prompt-1-1.md:479-480,T1.AC1@./artifacts/t1-baseline-cmp.txt:2,T2.AC1@./artifacts/fence-after.txt:281,T2.AC2@./artifacts/guide-diff.txt:1-48 state=5a2072638970addffa2caa0d7845e8d6058d540e3401144e0e2b900eac82a97b
ARCHIVE: Ruling: T1,T2 superseded reviewer prompts retries/T1/prompt-1-1.md and retries/T2/prompt-1-1.md moved unchanged to ./artifacts/superseded-prompts/ on user confirmation "Move them and archive" in the current conversation — they miss one template blank line and both tasks were re-reviewed with template-exact prompt-1-2.md (all AC met, no findings) — cost-if-wrong: an archived package whose first-round review prompts sit outside retries/, so a later FINAL does not compare them
```

### docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:136,177,1303,1360,1416,1482,1486,1586,1596,1655,1809,1865,2063,2127 (current HEAD four-backtick fences)

```text
$ grep -n '^````' docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
136:````markdown
177:````
1303:````markdown
1360:````
1416:````markdown
1482:````
1486:````markdown
1586:````
1596:````markdown
1655:````
1809:````markdown
1865:````
2063:````markdown
2127:````
```
Seven pairs: the six fixed templates plus Appendix B. Line numbers shifted after the refactor was committed (spec's 1322/1379 etc. map to 1303/1360, 1416/1482, 1486/1586, 1596/1655, 1809/1865); the fix is present.

### .dev/tasks/done/TASK-WF-devGuideFenceFix-20261104-204854/artifacts/superseded-prompts/README.md (archival note)

Read it: it records why prompt-1-1 files were superseded.

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

All 9 inferred rows matched; coverage_pct_union 1.0; parsed=0 (parsed-sparse).

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.
