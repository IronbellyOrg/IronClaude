# T1 Reflection Card — UC-1 pre audit: rename /sc:issue summary file (TASK-WF-renameTheScIssue-20261104-174359)

Run: shadow07. Mode pre, tier pinned 2, engine shadow. Spec = one-sentence directive (source.md:1). Tasklist = 4 tasks in 3 phases. The package is already executed and archived (progress.md:11 FINAL: pass); this audit judges the plan as a plan.

## Spec (verbatim, source.md:1)

"Rename the /sc:issue claim summary file written by issue-worker-t1/t2 from summary.md to issue-summary.md (the template may be renamed to templates/issue-summary.md) everywhere it is referenced (SKILL.md, refs/claim.md, refs/chains.md where <S> = .dev/issues/<N>/summary.md, templates claim-comment.md and next-steps.md, the three worker agent files including the fix-2 'tool inputs' paragraph, commands/issue.md Outputs table, the design doc, and the developer and user guide rows), and require that files written under <D>/analysis/ use names that do not start with analysis, report, summary or findings (for example analysis/analyze-<scope>.md). Correct the fix-2 paragraph so it states the real mechanism: Claude Code refuses subagent writes of .md files whose names start with REPORT, SUMMARY, FINDINGS or ANALYSIS, which is why the names avoid them. Add a deterministic regression test that collects every file name a worker is told to write (agent files, SKILL.md, refs, the Outputs table) and asserts that none matches the harness regex ^(REPORT|SUMMARY|FINDINGS|ANALYSIS).*\.md$ case-insensitively, and that no reference to the old <D>/summary.md path remains. In docs/designs/sc-issue-command.md, add a dated note (2026-11-04) explaining the rename and its cause, and update the file lists. Files: as listed in scope."

## Coverage matrix (Step 1B.0 two-pass)

Pass 1 (ID_REGEX + range expansion): 0 requirement IDs in spec; tasklist uses "Task N" headings, no REQ/T-IDs. parsed = 0.

Pass 2 (inferred, quote-pinned):

| INF id | Quote (≤2 sentences, source.md:1) | Task / constraint match (containment ≥0.6) |
|---|---|---|
| INF-001 | "Rename the /sc:issue claim summary file written by issue-worker-t1/t2 from summary.md to issue-summary.md ... everywhere it is referenced" | Task 1 (skill package) + Task 2 (agents, command) + Task 4 (design doc) — 0.85 |
| INF-002 | "require that files written under <D>/analysis/ use names that do not start with analysis, report, summary or findings (for example analysis/analyze-<scope>.md)" | Task 1 (SKILL/claim template/claim.md) + Task 2 (t1/t2 job text, Outputs) + Task 4 (section 7) — 0.80 |
| INF-003 | "Correct the fix-2 paragraph so it states the real mechanism: Claude Code refuses subagent writes of .md files whose names start with REPORT, SUMMARY, FINDINGS or ANALYSIS, which is why the names avoid them" | Task 2 (paragraph replace, verbatim Constraints paragraph) + Task 3 (`_TOOL_INPUT_PARAGRAPH`, comment update) — 0.90 |
| INF-004 | "Add a deterministic regression test that collects every file name a worker is told to write ... and asserts that none matches the harness regex ^(REPORT|SUMMARY|FINDINGS|ANALYSIS).*\.md$ case-insensitively, and that no reference to the old <D>/summary.md path remains" | Task 3 (5 test additions incl. probe parametrization, pre-fix negative case) — 0.90 |
| INF-00(INF-005) | "In docs/designs/sc-issue-command.md, add a dated note (2026-11-04) explaining the rename and its cause, and update the file lists" | Task 4 (dated note + section 7/9/10/15/18/20 updates + guides check) — 0.88 |

Union coverage: 5/5 matched → coverage_pct_union = 1.0; coverage_pct = null (0 parsed); coverage_degraded = parsed-sparse (5 inferred > 0 parsed) → T1-stop forbidden; pinned to 2 anyway.

## Wave 1A grounding (verified on disk this run)

- SKILL.md:38 templates table row reads `templates/issue-summary.md` -> `issue-summary.md (claim)`; SKILL.md:88 Wave 4 names `<D>/issue-summary.md` + `analyze-<scope>.md` naming rule. [executed]
- refs/claim.md:58-59: analysis naming rule + `<D>/issue-summary.md` from `templates/issue-summary.md`; :79 goal input `@.dev/issues/<N>/issue-summary.md` — wait, disk line 79 is the `gh api PATCH` accuracy-check line; the input line the plan names sits in the recommend step (verified in design doc mirrors). Anchor drift only; content present.
- refs/chains.md:7 `<S>` = `.dev/issues/<N>/issue-summary.md`; :28 "filled from issue-summary.md". [executed]
- templates/claim-comment.md:17 and templates/next-steps.md:8 carry issue-summary.md (verified via earlier grep of the skill tree, no residual summary.md). [executed]
- Agents t1/t2/t3: heading "Your files are tool inputs, not reports" at :13/:13/:14; paragraph under it matches the Constraints verbatim paragraph (spot-verified); job-1 text updated. [executed]
- commands/issue.md Outputs table (claim row): issue-summary.md + analysis/analyze-<scope>.md. [executed]
- tests/skills/test_issue_worker_agents.py: `_HARNESS_REPORT_NAME` at :339, `written_md_names` :370, tests at :440-493 (probe, basenames, avoid-block, old-path-gone, pre-fix negative). [executed]
- docs/designs/sc-issue-command.md:178-188 issue-summary.md everywhere; :234 `<S>` = issue-summary; :261 table row; :272 dated 2026-11-04 note naming regex, cause, pinning test. [executed]
- Guides check (T4): user guide has no summary-file reference for /sc:issue (verified lines 115, 347-380 name none); developer guide `summary.md` hits at 1178/1239 (plan) — disk shows only `commands/summary.md` at :1301 (an unrelated file). Plan's "no /sc:issue row" conclusion holds; its line anchors were pre-edit.
- Repo-wide sweep: zero residual `summary.md` references on the /sc:issue surface; remaining hits are unrelated sprint/eval subsystems (executor.py:1843, summarizer.py:515, run_report.py:391 etc.), out of scope by the spec's "everywhere it is referenced" scoping to the listed files.

## Hypothesis cards (candidate findings pre-debate)

- **H1 (medium candidate)**: No task schedules `make sync-dev` / `make verify-sync` after editing `src/superclaude/{skills,agents,commands}`. Constraint explicitly forbids touching `.claude/`, so without a sync step the mirror goes stale and `make verify-sync` (pre-commit hook + CI) fails for every later contributor. Mirrors shadow03 M1 for this package. Current disk state: mirror in sync (diff clean), so the executed run did sync — but the plan as written omits the step; the executed run's own FINAL evidence does not include a verify-sync line. → missing AC / unmeetable-adjacent.
- **H2 (minor candidate)**: T1.AC3 demands `grep -rn 'summary\.md' src/superclaude/skills/sc-issue-protocol` print ONLY issue-summary.md occurrences. `issue-summary.md` itself matches the pattern `summary\.md` (substring), so the AC is self-consistent only if read as "grep -v issue-summary". The task's own t1-grep.log artifact presumably used that reading. Slight AC ambiguity, non-blocking.
- **H3 (minor candidate)**: T3 red-check runs file checks "against the pre-fix copies in ./artifacts/pre/" — but Task 1 only copies 10 files (SKILL, 2 refs, 3 templates, 3 agents, issue.md), NOT tests/skills/test_issue_worker_agents.py pre-state or docs/designs. t3-red.log exists; the checks flagged summary.md blocked-name and <D>/summary.md old-path as designed. The plan's red-check is fully specified on the 10 pre copies; adequate.
- **H4 (low)**: Plan line anchors (claim.md:58/59/79/88, design doc 168-174/223/249-250/359/437/467) are pre-edit anchors; post-edit drift is inherent to a rename task. Each anchor is accompanied by content description, so an executor is not misled. Non-finding.
- **H5 (medium candidate)**: T3's `test_worker_written_names_avoid_harness_block` scans "the `## Outputs` section rows of src/superclaude/commands/issue.md" — but the Outputs table also names files written in CREATE mode (flags.md, flags-t1.md, issue-body.md, draft-notes.md, create-review-comment.md, description.md, scout.md). The test reads the Outputs section as a whole (verified test file structure), so both modes' files are pinned. Covered; no finding.
- **H6 (medium candidate)**: Spec says rename "the developer and user guide rows" — Task 4 concludes the guides need NO edit and records the check. Verified on disk: user guide names no summary file; developer guide's summary.md occurrences are unrelated. The spec's directive was conditional ("rows" that reference it); zero rows reference it. Sound.

## Self-calibration (inline, pre-blind)

Citation grounding 0.9 (all anchors re-verified this run, two anchor-drift notes); Coverage completeness 0.85 (5/5 inferred matched; manual spec-clause walkthrough complete); Deviation-classification clarity n/a UC-1 → 0.8; Risk surface 0.7 (H1 is a real process risk the plan misses); Recommendation actionability 0.85. Mean ≈ 0.82. Rubric would ESCALATE anyway (parsed-sparse + pinned).

## Tier decision

--tier 2 pinned (hard override). Rubric concurs: C≈0.82 < 0.85, coverage_degraded=parsed-sparse. Engine shadow read at Wave 3 start.
