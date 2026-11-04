# Fix 3 report: rename the claim summary file to issue-summary.md

Task: task_73d57dc866d4 (dispatch ctx_739732197929). Branch: ironbelly/feat-sc-issue-command.

## 1. Plan and check result

- Plan (archived by the `/sc:implement` helper): `.dev/tasks/done/TASK-WF-renameTheScIssue-20261104-174359/TASK-WF-renameTheScIssue-20261104-174359.md`. It has 4 tasks: the skill package rename, the agents and the command Outputs table, the regression test, and the design doc. The workflow contract is `status: success`, `reflect_status: success`.
- Check result (`/sc:reflect --mode pre`, advisory): `.dev/reflect/pre-renameTheScIssue-20261104174640/REPORT.md`.
  - Tier 2 was forced by `coverage_degraded: parsed-sparse`: the spec has no labelled IDs and 9 inferred requirements, all of them mapped to a task.
  - It used 3 reviewers (sonnet, glm-5.3, opus), and the adversarial merge reached convergence 0.95.
  - Merged verdict: PASS (with notes), 0 blocking, 13 minor (`adversarial/merged-verdict.yaml`). 18 citations, 0 dropped.
- Minor findings applied during execution, within the plan's wording:
  - `<scope>` is defined only for the analysis file name, and `refs/chains.md:7` is unchanged (M-04).
  - The exact literal `<D>/analysis/analyze-<scope>.md` is in `refs/claim.md:58` (M-05).
  - The design-doc grep for `analyze-<scope>` is in `t4-grep.log` (M-10).
  - A shared helper, `old_summary_refs`, is used by both tests and by the red check (M-01).
  - The test asserts that the set of collected names is not empty (M-02).
  - A `<REPORT.md` probe case is added (M-07).
  - The stale-mirror removal is covered in section 5 (M-08).

## 2. Files changed

All changes are uncommitted, as before.

| File | Change |
|---|---|
| `src/superclaude/skills/sc-issue-protocol/templates/summary.md` -> `templates/issue-summary.md` | Renamed (`mv`; the file was untracked). Line 20 now says the analysis links are "named like `analyze-<scope>.md`". |
| `src/superclaude/skills/sc-issue-protocol/SKILL.md` | Line 37: the template table row. Line 86: Wave 4 writes `<D>/issue-summary.md` and `<D>/analysis/analyze-<scope>.md`, and no file under `<D>/analysis/` starts with analysis, report, summary or findings. |
| `src/superclaude/skills/sc-issue-protocol/refs/claim.md` | Lines 58-59: the analysis name rule, and `issue-summary.md` from `templates/issue-summary.md`. Also lines 79 and 88. |
| `src/superclaude/skills/sc-issue-protocol/refs/chains.md` | Line 7 (`<S>` = `.dev/issues/<N>/issue-summary.md`), line 28 and line 33. |
| `src/superclaude/skills/sc-issue-protocol/templates/claim-comment.md` | Line 17. |
| `src/superclaude/skills/sc-issue-protocol/templates/next-steps.md` | Line 8. |
| `src/superclaude/agents/issue-worker-t1.md`, `issue-worker-t2.md`, `issue-worker-t3.md` | Line 15: the fix-2 "tool inputs" paragraph is replaced (detail below the table). Line 21 (t1/t2 only, claim job 1): `<D>/analysis/analyze-<scope>.md`, and `<D>/issue-summary.md` from the `issue-summary.md` template. |
| `src/superclaude/commands/issue.md` | Line 68, the claim row of the Outputs table: `issue-summary.md` and `analysis/analyze-<scope>.md`. |
| `tests/skills/test_issue_worker_agents.py` | Updated `_TOOL_INPUT_PARAGRAPH`, `_WORKER_FILES` and the cause comment. Added the helpers `_HARNESS_REPORT_NAME`, `written_md_names`, `blocked_names`, `old_summary_refs` and `worker_instruction_texts`. Added the tests `test_harness_regex_matches_probe` (17 cases), `test_written_md_names_takes_basenames`, `test_worker_written_names_avoid_harness_block`, `test_old_summary_path_is_gone` and `test_checks_flag_pre_fix_text`. |
| `docs/designs/sc-issue-command.md` | Lines 168-169, 173-174, 179, 223, 249-250, 361 (template list), 439 (D22) and 469 (section 20 item 1). New dated note at line 261, under section 10, "Note (2026-11-04)": it records the rename, its cause, the regex, the #365 refusal and the pinning test. |
| Developer and user guides | Not changed. The developer guide has no `/sc:issue` row; its `summary.md` hits at lines 1178 and 1239 are an unrelated `/sc:summary` example. In the user guide, neither the `/sc:issue` row (line 115) nor its section (lines 347-380) names a summary file. Evidence: `t4-guides.log` in the package. |

The new line 15 paragraph in the three agent files:
- It names `issue-summary.md` and `analysis/analyze-<scope>.md`.
- It states the real mechanism: "Claude Code refuses a subagent's Write of any `.md` file whose name starts with REPORT, SUMMARY, FINDINGS or ANALYSIS (in any letter case), which is why none of these names starts with those words."
- The old "does not apply to them" clause is gone.

## 3. Proof the test fails on the old text

There are two proofs. The real files were never reverted.

- **Red run on the pre-fix copies.**
  - Task 1 saved byte-exact copies of the ten edited files, before any edit, to `.dev/tasks/done/TASK-WF-renameTheScIssue-20261104-174359/artifacts/pre/`. The FINAL reviewer confirmed they match the T1 start snapshot.
  - `artifacts/t3_red.py` loads the test module and runs `blocked_names` and `old_summary_refs` on each copy. It flags 9 of the 10. The tenth, `template-summary.md`, names no file.
  - On the pre-fix `SKILL.md` it reports `blocked_names=['summary.md']` and `old_summary_refs=['<D>/summary.md', 'templates/summary.md', '`summary.md`']`. Every pre-fix agent file reports `blocked_names=['summary.md']`.
  - It also confirms the test's old literals are byte-present in the pre-fix files.
  - It exits `rc=1` (`artifacts/t3-red.log`, lines 2-15).
- **`tmp_path` negative test in the suite.** `test_checks_flag_pre_fix_text` writes the pre-fix paragraph and the pre-fix Wave 4 line to a `tmp_path` file. It asserts that `blocked_names` returns `['summary.md']` and that `old_summary_refs` returns `['<D>/summary.md', '`summary.md`']`. It passes.

## 4. /sc:implement ledger

Ledger: `.dev/tasks/done/TASK-WF-renameTheScIssue-20261104-174359/progress.md`. Every task passed. Each review was a fresh subagent working from the closed template.

| Task | Verdict | Reviews |
|---|---|---|
| T1 skill package | complete, compliant | 1 review, no findings |
| T2 agents and command | complete, compliant | 1 review, no findings. Extras show `test:fail`: the 6 transient failures expected from the old test constant, which T3 fixed. |
| T3 regression test | complete, compliant | Review 1 found one blocking gap: the probe parametrization was missing the `analyze-report.md` and `notes.md` cases the plan names (`retries/T3/review-1.md`). One fix pass followed (`retries/T3/probe-1-1.md`). Review 2 marked it resolved, with no findings. |
| T4 design doc | complete, compliant | 1 review, no findings |

Managed FINAL: `FINAL: pass state=e984a1df…`, from a fresh subagent; every saved prompt matches the template. The helper then archived the package (`ARCHIVE: start … token=3ee351364418babf`), so it now lives in `.dev/tasks/done/`.

Two errors of mine:
- The T1 ledger line cites `./artifacts/t1-tests.log:4` for the pytest outcome, but the outcome is on line 14. The ledger is append-only, so the wrong pointer stays. The FINAL reviewer read line 14.
- I once ran a bare `python3` heredoc, outside UV. It did nothing.

## 5. Verification (suite counts, lint, sync, path grep)

| Check | Result | Exit code | Log |
|---|---|---|---|
| `make sync-dev` | synced | 0 | `01-sync-dev.log` |
| `make verify-sync`, first run | `DIFFERS: sc-issue-protocol`, "Only in .claude/skills/sc-issue-protocol/templates: summary.md" | 2 | `02a-verify-sync-before-stale-removal.log` |
| `make verify-sync`, after removing the stale mirror | "All components in sync." | 0 | `02-verify-sync.log` |
| Targeted tests: `tests/skills/test_issue_worker_agents.py tests/skills/test_issue_protocol.py tests/commands/test_issue_command.py tests/cli/test_issue_body_templates.py` | 151 passed | 0 | `03-targeted-tests.log` |
| Full `uv run pytest` | 14873 passed, 136 skipped, 2 xpassed, 0 failed | 0 | `04-full-suite.log` |
| `make lint` (`ruff check .`) | All checks passed | 0 | `05-lint.log` |
| CLAUDE.md `src/superclaude` path grep over the changed primitives | no hit | 1 (no match) | `06-path-and-name-grep.log` |
| `summary\.md` grep over the skill, the three agents and `commands/issue.md` | every hit is `issue-summary.md`: 20 tokens, 0 bare `summary.md` | 0 | `06-path-and-name-grep.log` |
| Anything under `.claude/` staged? | none staged | 1 (no match) | `06-path-and-name-grep.log` |

**Stale mirror.** `make sync-dev` only copies and never deletes (Makefile:117-123). The rename therefore left a stale, gitignored copy: `.claude/skills/sc-issue-protocol/templates/summary.md`.
- The copy was byte-equal to the pre-rename template.
- `git check-ignore` confirms it is ignored (`.gitignore:127`).
- I removed that one file so `verify-sync` exits 0. It was never staged.
- CI is not affected, because it syncs into a fresh runner.

**Suite side effect.** As in fix 2, the full suite rewrote the tracked file `.dev/releases/current/cliEval/evidence/T02.15/perf.json` (written by `tests/cli/eval/test_perf_home_setup.py`). I restored it with `git restore` right after the run.

## 6. Open findings and follow-ups

All of these are minor or outside this task's scope, and none changes a verdict.

- **Refresh installed copies before the next live claim (M-13).** `superclaude install` skips an existing skill, agent or command unless `--force` is given (`src/superclaude/cli/install_skills.py:102-104`, `install_agents.py:51`, `install_commands.py:55`). Skills also resolve `~/.claude/skills/` before the project `.claude/skills/` (CLAUDE.md:96).
  - Run `superclaude install --force` before the next live `/sc:issue --claim`.
  - Nothing is installed for sc-issue on this machine today.
- **Create-mode `/sc:analyze` runs name no output file (M-12, invariant probe INV-001).** This covers t1 jobs 2 and 4, t2 job 4, t3 job 3, and `refs/create.md:51-53`.
  - A worker could invent `ANALYSIS.md` or `report.md`, and the static test cannot see a name that only exists at run time.
  - This is outside the claim-mode scope of this fix and is a candidate follow-up.
- **Small notes.**
  - The name scan reads backtick code spans only. Names in fenced blocks or prose are caught only by the old-path substring check (M-03).
  - The spawn-rule line at `SKILL.md:66` still says "not report files" without naming the mechanism. It is pinned by `_SPAWN_PROMPT_LINE` and was deliberately left unchanged (M-11).
  - The test comment says "Live acceptance of #365", while the design note says #302 with issue #365. Both refer to the same event.

Not touched, as instructed: minor notes m1 to m7 and N1 to N3, and `.dev/issues/`. No `/sc:issue` run, no issue-worker spawn, and no gh writes, commits or pushes. Nothing under `.claude/` is staged; `.dev/tasks` is staged.

## 7. Log paths

**Verification logs**, in `.dev/tasks/issue-302-handoff/fix-3/` (each records its command and `rc=`):
- `01-sync-dev.log`
- `02a-verify-sync-before-stale-removal.log`
- `02-verify-sync.log`
- `03-targeted-tests.log`
- `04-full-suite.log`
- `05-lint.log`
- `06-path-and-name-grep.log`

**Task evidence**, in the archived package `.dev/tasks/done/TASK-WF-renameTheScIssue-20261104-174359/artifacts/`:
- T1: `t1-grep.log`, `t1-tests.log`, `t1-diff.patch`
- T2: `t2-grep.log`, `t2-extras.log`, `t2-diff.patch`
- T3: `t3-green.log`, `t3-red.log`, `t3_red.py`, `t3-diff.patch`, `t3-delta-1.patch`
- T4: `t4-grep.log`, `t4-guides.log`, `t4-diff.patch`
- `pre/`: the ten pre-fix copies
- `retries/T1..T4/`: `q0-head`, the saved review prompts, and T3's `review-1.md` and `probe-1-1.md`

**Plan check (reflect) artifacts**, in `.dev/reflect/pre-renameTheScIssue-20261104174640/`: `REPORT.md`, `return-contract.yaml`, and in `adversarial/`: `merged-verdict.yaml`, `debate-transcript.md` and `invariant-probe.md`.
