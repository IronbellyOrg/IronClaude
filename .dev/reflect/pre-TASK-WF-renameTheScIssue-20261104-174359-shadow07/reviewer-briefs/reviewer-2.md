# Reviewer brief 2 — persona: qa, model class: haiku (pin claude-haiku-5-5, reviewer_id t4-1)

codegraph run state: index_state=fresh checked_at=2026-11-13T00:05:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

## T1 card excerpt

Verbatim from t1-card.md (qa-relevant slice: coverage + acceptance surface):

Coverage: Pass 1 = 0 requirement IDs (prose spec, Task headings only). Pass 2 = 5 inferred quote-pinned rows INF-001..005 (rename everywhere; analysis naming rule; fix-2 paragraph mechanism correction; deterministic regression test; dated design note + file lists), all containment-matched to tasks (0.80-0.90). coverage_pct_union 1.0, parsed 0, coverage_degraded parsed-sparse.

- **H2 (minor candidate)**: T1.AC3 demands `grep -rn 'summary\.md' src/superclaude/skills/sc-issue-protocol` print ONLY issue-summary.md occurrences. `issue-summary.md` itself matches the pattern `summary\.md` (substring), so the AC is self-consistent only if read as "grep -v issue-summary". Slight AC ambiguity, non-blocking.
- **H3 (minor candidate)**: T3's red-check runs the two file checks against the 10 pre-fix copies in `./artifacts/pre/`; plan copies only the renamed-surface files, not tests or design doc pre-state; adequate since checks are name-based.
- **H5**: resolved non-finding (Outputs-section scan covers create-mode files too: the test scans the whole `## Outputs` section, so flags.md, flags-t1.md, issue-body.md, draft-notes.md, create-review-comment.md, description.md, scout.md are pinned).
- **H6**: resolved non-finding (user/developer guides carry no /sc:issue summary-file reference; spec directive conditional; Task 4 records the check in t4-guides.log).

End your card with a ## Findings block fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec) and a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

### spec source.md:1 (whole spec, 1 line)
```text
Rename the /sc:issue claim summary file written by issue-worker-t1/t2 from summary.md to issue-summary.md (the template may be renamed to templates/issue-summary.md) everywhere it is referenced (SKILL.md, refs/claim.md, refs/chains.md where <S> = .dev/issues/<N>/summary.md, templates claim-comment.md and next-steps.md, the three worker agent files including the fix-2 'tool inputs' paragraph, commands/issue.md Outputs table, the design doc, and the developer and user guide rows), and require that files written under <D>/analysis/ use names that do not start with analysis, report, summary or findings (for example analysis/analyze-<scope>.md). Correct the fix-2 paragraph so it states the real mechanism: Claude Code refuses subagent writes of .md files whose names start with REPORT, SUMMARY, FINDINGS or ANALYSIS, which is why the names avoid them. Add a deterministic regression test that collects every file name a worker is told to write (agent files, SKILL.md, refs, the Outputs table) and asserts that none matches the harness regex ^(REPORT|SUMMARY|FINDINGS|ANALYSIS).*\.md$ case-insensitively, and that no reference to the old <D>/summary.md path remains. In docs/designs/sc-issue-command.md, add a dated note (2026-11-04) explaining the rename and its cause, and update the file lists. Files: as listed in scope.
```

### plan TASK-WF-renameTheScIssue-20261104-174359.md:62-76 (Task 3, regression test)
```text
In `tests/skills/test_issue_worker_agents.py`:
- Update `_TOOL_INPUT_PARAGRAPH` to the exact Constraints paragraph and `_WORKER_FILES` to replace `summary.md` with `issue-summary.md` and `analysis/` with `analysis/analyze-<scope>.md`; update the comment above them (lines 199-203) to say the cause is Claude Code's Write-tool refusal of subagent `.md` files whose names start with REPORT, SUMMARY, FINDINGS or ANALYSIS.
- Add `_HARNESS_REPORT_NAME = re.compile(r"^(REPORT|SUMMARY|FINDINGS|ANALYSIS).*\.md$", re.IGNORECASE)` and a helper `written_md_names(text)` that returns the basenames (text after the last `/`, after stripping a leading `@`) of every whitespace-separated token ending in `.md` inside backtick code spans.
- Add `test_harness_regex_matches_probe` parametrized with the probe results: `summary.md`, `findings.md`, `report.md` match; `scout.md`, `accuracy-check.md`, `flags.md`, `flags-t1.md`, `issue-body.md`, `draft-notes.md`, `issue-summary.md`, `cheatsheet.md`, and the basenames of `analysis/analyze-report.md` and `analysis/notes.md` do not.
- Add `test_worker_written_names_avoid_harness_block`: apply `written_md_names` to the three agent files, `src/superclaude/skills/sc-issue-protocol/SKILL.md`, every `refs/*.md` of that skill, and the `## Outputs` section rows of `src/superclaude/commands/issue.md`; assert no name matches `_HARNESS_REPORT_NAME`, and assert the analysis naming example `analysis/analyze-<scope>.md` appears in SKILL.md, `refs/claim.md` and the t1 and t2 agent files.
- Add `test_old_summary_path_is_gone`: over the same files plus every `templates/*.md` of the skill, assert none contains `<D>/summary.md`, `.dev/issues/<N>/summary.md`, `templates/summary.md` or the code span `` `summary.md` ``.
- Add a negative case that proves the checks fail on pre-fix text without touching the real files: `test_checks_flag_pre_fix_text(tmp_path)` writes the pre-fix tool-input paragraph (the old string, kept as a test literal) and the old Wave 4 line to a `tmp_path` file and asserts `written_md_names` yields a name matching `_HARNESS_REPORT_NAME` and that the old-path check finds `<D>/summary.md`.
```

### plan TASK-WF-renameTheScIssue-20261104-174359.md:29-45 (Task 1)
```text
Before editing, copy each file this task and Task 2 change (`src/superclaude/skills/sc-issue-protocol/SKILL.md`, `refs/claim.md`, `refs/chains.md`, `templates/summary.md`, `templates/claim-comment.md`, `templates/next-steps.md`, `src/superclaude/agents/issue-worker-t1.md`, `issue-worker-t2.md`, `issue-worker-t3.md`, `src/superclaude/commands/issue.md`) unchanged into `./artifacts/pre/` (keep the basename; prefix the template copies with `template-` and the refs copies with `ref-` so no two collide) as the pre-fix evidence used by Task 3.

Then, all under `src/superclaude/skills/sc-issue-protocol/`:
- Move `templates/summary.md` to `templates/issue-summary.md` (plain `mv`; the file is untracked) and in its `## Analysis` placeholder say the links point at reports under `.dev/issues/<N>/analysis/` named like `analyze-<scope>.md`.
- `SKILL.md`: the templates table row `templates/summary.md` -> `summary.md (claim)` becomes `templates/issue-summary.md` -> `issue-summary.md (claim)`; Wave 4 (step 5 of Claim mode) names `<D>/issue-summary.md` and states that files under `<D>/analysis/` are named like `<D>/analysis/analyze-<scope>.md`, never starting with analysis, report, summary or findings.
- `refs/claim.md`: line 58 (`/sc:analyze` report saved under `<D>/analysis/`) adds the same naming rule; line 59 writes `<D>/issue-summary.md` from `templates/issue-summary.md`; line 79 input becomes `@.dev/issues/<N>/issue-summary.md`; line 88 links to `<D>/issue-summary.md`.
- `refs/chains.md`: line 7 `<S>` = `.dev/issues/<N>/issue-summary.md`; line 28 "filled from `issue-summary.md`"; line 33 `Summary: .dev/issues/<N>/issue-summary.md`.
- `templates/claim-comment.md` line 17: `- Summary: .dev/issues/<N>/issue-summary.md` (keep the code-span style).
- `templates/next-steps.md` line 8: `- Input: @.dev/issues/<N>/issue-summary.md` (keep the code-span style).

Acceptance criteria:
- `./artifacts/pre/` holds the ten unchanged pre-fix copies listed above.
- `src/superclaude/skills/sc-issue-protocol/templates/issue-summary.md` exists, `templates/summary.md` does not, and the template content is otherwise unchanged apart from the analysis-name wording.
- `grep -rn 'summary\.md' src/superclaude/skills/sc-issue-protocol` prints only `issue-summary.md` occurrences; output saved to `./artifacts/t1-grep.log`.
- `uv run pytest tests/skills/test_issue_protocol.py -q` passes (the two-way refs/templates inventory sees `templates/issue-summary.md` in SKILL.md); output saved to `./artifacts/t1-tests.log`.
```

### tests/skills/test_issue_worker_agents.py:330-500 (post-edit tests)
Read the file directly in the repo (paths above) to verify the five tests exist as specified: `test_harness_regex_matches_probe` (:440), `written_md_names` (:370), `test_worker_written_names_avoid_harness_block` (:459), `test_old_summary_path_is_gone` (:482), `test_checks_flag_pre_fix_text` (:493).

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-001 rename everywhere | — | covered | Task 1 + Task 2 + Task 4 |
| INF-002 analysis naming rule | — | covered | Task 1 + Task 2 + Task 4 sec 7 |
| INF-003 fix-2 paragraph mechanism | H2-adjacent | covered | Task 2 + Task 3 comment |
| INF-004 deterministic regression test | H3 | covered | Task 3 |
| INF-005 dated design note + file lists | — | covered | Task 4 |
