# T1 reflection card (UC-1, pre-execution)

- Spec: .dev/tasks/to-do/TASK-WF-renameTheScIssue-20261104-174359/source.md (one paragraph, line 1)
- Tasklist: .dev/tasks/to-do/TASK-WF-renameTheScIssue-20261104-174359/TASK-WF-renameTheScIssue-20261104-174359.md (4 tasks, 3 phases)
- Card source: inline orchestrator (hypothesis_source: inline)
- Self-reported confidence (NOT used by the rubric): 0.86

## Coverage / acceptance

Pass 1 parsed 0 requirement IDs (the spec has no R-/REQ-/SPEC-/T- tokens). Pass 2 inferred 9 quote-pinned rows (artifacts/inferred-requirements.json), all citing source.md:1. The deterministic containment matcher (artifacts/coverage-matrix.json) matched all 9: INF-001 and INF-002 -> Task 1; INF-003 and INF-006 -> Task 2; INF-005, INF-007, INF-008 -> Task 3; INF-004 and INF-009 -> Task 4. coverage_pct (parsed) = null; coverage_pct_union = 1.0; coverage_degraded = parsed-sparse (9 inferred > 0 parsed).

INF-004 ("the developer and user guide rows"): the plan edits neither guide. Evidence: `grep -n -i issue` on docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md finds no /sc:issue row (its `summary.md` hits at lines 1178 and 1239 are unrelated `/sc:summary` examples); docs/user-guide/commands.md line 115 and lines 347-380 name no summary file. Task 4 records this check as ./artifacts/t4-guides.log. Classified as a documented necessary deviation, not a coverage gap.

## Root cause / deviation candidates

- D-1 (candidate, blocking for the executor's own acceptance): renaming `templates/summary.md` to `templates/issue-summary.md` leaves a stale `.claude/skills/sc-issue-protocol/templates/summary.md`. `make sync-dev` only copies (Makefile:117-123, `cp "$$src" "$$target_dir/"`), never deletes, and `make verify-sync` runs `diff -rq` over each skill dir (Makefile:178), so it reports the orphan and exits non-zero. The coordinator requires verify-sync exit 0. No task removes the stale mirror (deleting a gitignored `.claude/` copy is not staging, so it is allowed).
- D-2 (minor): Task 2 defines `<scope>` as "the main path's last segment", while refs/chains.md:7 already defines `<scope>` as "the main path from the summary". Two meanings of one placeholder in one skill.

## Structural / tech-debt

- Task 3's `written_md_names` scans every `.md` code span in agent files, SKILL.md and refs, a superset of "files a worker is told to write" (it also picks up `SKILL.md`, `CLAUDE.md`, `ISSUE-HANDOFF.md`). None of those match the harness regex today, so the superset is safe and deterministic; a future reference like `REPORT.md` in a ref would fail the test even if no worker writes it (false positive risk, acceptable).
- The negative test keeps the old paragraph as a literal; the red log runs the checker against ./artifacts/pre/ copies. Real files are never reverted (meets the coordinator constraint).
- The tool-input paragraph text is pinned once in Constraints and reused verbatim by Task 2 and Task 3, so the agent files and `_TOOL_INPUT_PARAGRAPH` cannot drift.

## Risk surface

- verify-sync failure from the stale mirror (D-1).
- tests/skills/test_issue_protocol.py two-way inventory (`templates/*.md` vs SKILL.md mentions, line 134) breaks unless SKILL.md names `templates/issue-summary.md`; Task 1 covers it and runs that test.
- Design doc section 16 (Tests) may list test files; the plan updates sections 7, 9, 10, 15, 18, 20 only.
