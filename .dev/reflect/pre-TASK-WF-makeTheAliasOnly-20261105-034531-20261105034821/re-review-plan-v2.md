# Re-review of the regenerated plan (fix cycle 1 of 2)

- Plan reviewed: `.dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-051649/TASK-WF-makeTheAliasOnly-20261105-051649.md`
- Reviewer: fresh `reflect-reviewer` agent on claude-opus-5-5, read-only, no knowledge of the first review other than the merged card and the old plan it was handed
- Persisted by the orchestrator from the reviewer's returned report (condensed; all findings, citations and statuses kept)

## Verdict

PASS_WITH_NOTES. `/sc:implement` can run this plan. M-1 to M-4 are closed. No blocking findings.

## M-1..M-4 status

| ID | Status | New plan line |
|---|---|---|
| M-1 | Closed | plan:56 (no literal tier id in the comment), plan:60 (tier-text test passes after Task 2), plan:125 (whole policy file, `final-policy.log`) |
| M-2 | Closed, with N-1 | plan:129 (lines to add to the fake claude's `json.dump`, the three variables removed from the environment, scratch run), plan:133 (log must show an AssertionError, not a KeyError) |
| M-3 | Closed | plan:66 (the note may not contain `--models`), plan:69 (`grep -n -- "--models"`) |
| M-4 | Closed | plan:56 (`D12-reflect.md:235`), plan:39 (test), plan:59 (grep) |

## What the reviewer checked

Task 3 grep versus the mandated bullet (only `chains.md:11-13,21` contain `--models` and all four lines are rewritten); Task 4 Haiku sites (only `SKILL.md:68,74,95,99,114`, `templates/final-report.md:77`, `cleanup-audit.md:43,53`; no `refs/` folder, no mirrors); Task 2 (`D12-reflect.md:235` is the only line with `claude-opus-4-8`; line 243 cites only `commands.py:31,359`); Task 5 grep (`retry.md:162,164,168,169,172` in src and mirror, `ledger.md:200`, `test_workflow_archive.py:774-777,786`, `test_task_workspace_lifecycle.py:597`; the literal `T[0-4]_Model` in the new test cannot match `T[0-4]_Model0`); that exactly seven policy tests fail on the unchanged tree (frontmatter, tier-text and markdown model-flag tests pass today; Python constants finds only `commands.py:31`); task ordering interactions; no edit to `ccsession-tag/` or the launcher; the line numbers the plan cites.

## Minor notes (not fixed in the plan; passed to the implementer)

- N-1 (Task 9, plan:129, 133): `tests/unit/test_ccsession_tiers.py:30-33` sets `REPO_ROOT = Path(__file__).resolve().parents[2]` and imports `models` from `SKILL_DIR`; `_launch` runs `SKILL_DIR / "ccsession"` (line 307). A copy in `./artifacts/t9-scratch/` resolves `parents[2]` to the package folder and fails collection with ModuleNotFoundError. Fix at implementation time: set `REPO_ROOT` to the absolute worktree path (or `parents[6]`) and name the file `test_*.py`.
- plan:37: the regex contains a backtick inside an inline code span; put it in a fenced block.
- plan:102: "spelled exactly as in the mapping table" is unclear; the page must contain the literal lines `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a` and the other two.
- plan:46: "fails exactly seven" assumes one test per bullet; bullets 8 and 10 combine a passing and a failing check.
- `docs/designs/sc-issue-command.md:227-229,452` keep `--models opus,sonnet` on purpose (historical record).

## Self-confidence

0.86. The reviewer ran no pytest or ruff and did not confirm mirror byte-identity.
