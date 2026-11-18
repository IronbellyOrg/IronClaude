# IronClaude: fix the flaky install-keep test (a follow-up of the 6.0.0 release)

Clay accepted this failing test as a known, test-only failure for the 6.0.0 release gate (2026-11-18, relayed by GeneralIronFlow) on the condition that it is fixed afterwards in a small pull request. This is that pull request. Your orchestrator is the ic6-orchestrator session. Do the work below in this worktree only, open ONE pull request into `integration`, answer every review finding, make every check green, then STOP. Do NOT merge.

## The problem

`tests/cli/test_install_keep.py::test_same_content_is_true_only_for_identical_readable_files` fails on fast machines (it fails alone on the orchestrator's machine every time; GitHub's runners pass it). The test writes file `a` and `b` with the same content, asserts `same_content(a, b)`, rewrites `b` with different content of the same size and asserts `not same_content(a, b)`. `same_content` in `src/superclaude/cli/install_keep.py` is `filecmp.cmp(a, b, shallow=False)`, and `filecmp.cmp` keeps a process-wide cache keyed on the two paths and their `(type, size, modification time)` signatures: when the rewrite lands in the same filesystem timestamp tick as the first write, the signature is unchanged and the cache returns the stale "identical" answer.

## What to do

1. Setup: `uv venv --python 3.10 && uv pip install -e '.[dev]' 'pytest-xdist>=3.5,<4' 'ruff==0.15.20' && make sync-dev`. Reproduce: `uv run pytest tests/cli/test_install_keep.py -q -p no:cacheprovider` (it must fail before your change; save the output under `.dev/issues/v6-install-keep-test/`, not committed).
2. Decide, with evidence from the installer's flow (`install_keep.py` and its callers `install_commands.py`, `install_skills.py`, `install_agents.py`, `install_core.py`, `install_hooks` and so on: find them with search), where the defect is. If any caller can compare the same pair of paths twice in one process with a write in between (for example compare, back up, overwrite, then compare again to report), the stale cache is a real defect in `same_content`, and the fix belongs there (`filecmp.clear_cache()` before the comparison, or a direct byte comparison that does not use the cache). If no caller can, the defect is only in the test and the fix is in the test. State your finding with file and line references in the pull request body.
3. Fix it with the smallest change. Add or adjust a test so that it fails on the old code and passes on the new code in the same-timestamp situation without depending on timing (force it: write both files, set the same `os.utime` on the second after rewriting it, so the signature is identical on any machine).
4. Run the regression gate: before your first edit, the baseline (`pytest -n auto --ignore=tests/cli/test_verify_sync_hooks.py`, no `--maxfail`, plus `make lint`, `uv run ruff format --check src/ tests/` with the pinned ruff, `make verify-sync`); after, the same. The pass count rises by the tests you add; 0 new failures; this one test passes.
5. Commit (`fix(install): ...`), push only your branch `clayphi/v6-fix-install-keep-test`, and open the PR with `/sc:pr-submit --base integration --head clayphi/v6-fix-install-keep-test --monitor 3 --repo IronbellyOrg/IronClaude`. Body in plain English: the cause, where the fix is and why, before and after test counts, `Refs #571`. Do not add a CHANGELOG entry unless the fix changes installer behavior (then one entry under `## [Unreleased]`).
6. Answer every Augment and Codex finding (fix, or reply with evidence) and resolve threads. When every check is green, both reviewers have finished on the final head and no thread is open: STOP. Do not merge. Do not comment to anyone else on the PR.

Rules: never stage `.claude/` (except `.claude/settings.json`); do not edit historical records; do not launch subagents (do skill steps inline); never log or commit credentials; update the Orca comment at checkpoints (`orca worktree set --worktree active --comment "<short status>"`). Another agent works on documentation in a separate worktree at the same time; do not touch documentation files.

## Process notes for the orchestrator

Keep `.dev/issues/v6-install-keep-test/PROCESS-NOTES.md`: one line per step with roughly how long it took, what got in the way, and what would make the step easier next release.

## Finish

End with a plain-English report: the DONE / NEXT table, then What I did, How, Where it stands, What's next, My recommendation. Include the PR link, the before and after test counts, and the state of every check and reviewer on the final head.
