# IronClaude 6.0.0, Small-fix PR B: ic launcher fixes (#542, #543, #544)

Clay (user clayphi) authorized this pull request on 2026-11-17 as part of the 6.0.0 release (IronClaude issue 571). Your orchestrator is the ic6-orchestrator session. Do the work below in this worktree only, open ONE pull request into `integration`, answer every review finding, make every check green, then STOP. Do NOT merge.

## Scope
Small-fix PR B (decision 6.7, Option A: approved small fixes ship in 6.0.0 on `integration`). Fix three problems in the `ic` launcher script `src/superclaude/scripts/ic` (and its installed mirrors via `make sync-dev`). For each, do ONLY what the issue and Clay's comment approve (Clay's decision on all three: fix this); read each issue in full first (`gh issue view <n> --repo IronbellyOrg/IronClaude --comments`).
- #542: `ic` expands unrelated environment variables as model aliases (for example `ic -H HOME` puts the home path in the model setting); restrict the resolution to the intended model aliases.
- #543: `ic -p` with no preset name stops with Bash's internal `$2: unbound variable`; print a clear missing-argument message instead (the script's line 74 reads `$2` under `set -u`).
- #544: `ic --help` fails when the environment file named by `AIENV` contains a failing command, because the file is sourced (lines 25-28, under `set -e`) before the help handler (lines 80-82); make help work without depending on that file.
Add tests under the project's existing test conventions for `ic` (find them with search), each failing before the fix and passing after. All three fixes are in one script, so do them in one branch, one commit per issue. The PR body must say `Closes #542`, `Closes #543`, `Closes #544` and `Refs #571`.
Part of wave 3, with PR 8 (remove `/sc:improve`) and small-fix PR A (help-text fixes) running in parallel in other worktrees.

Read issue 571 (body and comments) for the rules: `gh issue view 571 --repo IronbellyOrg/IronClaude --comments`. Swarm and everything in "Kept for now" stays. Do not edit historical records (docs/releases/, docs/testing/v5.0.0/, docs/designs/, past CHANGELOG.md entries); do not add a CHANGELOG.md entry (the release PR does that).

## Steps (the plan's "One flow for every item")
1. Dependency map (read-only, short): with codegraph (callers, impact) and search, find every file and mirror (`.claude`, `plugins/superclaude`) each fix touches, and check whether any other wave 3 PR (PR 8 removing `/sc:improve`) or an earlier merged PR touches the same lines. Write `.dev/cleanup/ic-launcher-fixes/dependency-map.md`, each reference as path:line with the change it needs. Re-measure: the plan's counts were taken at d4d1662a8 and several shared files changed since.
2. Plan: `/sc:workflow "Fix issues 542, 543 and 544 per .dev/cleanup/ic-launcher-fixes/dependency-map.md. Acceptance: each of the three issues is fixed as the issue describes and nothing more; each fix has a test that fails before the change and passes after; 0 new test failures; lint, format, verify-sync and git diff --check stay green" --depth standard --handoff none`.
3. Implement: `/sc:implement <the plan path it printed>`. Source of truth is `src/superclaude/`; run `make sync-dev` for the mirrors; never stage `.claude/` (except `.claude/settings.json`). Update docs and tests only where a fix needs it.
4. Regression gate, recorded under `.dev/issues/v6-ic-launcher-fixes/` (do not commit that folder):
   - Before your first edit, run the full test suite as the `test` job of `.github/workflows/test.yml` runs it (without --maxfail), plus `make lint` and `uv run ruff format --check src/ tests/`. Save pass, fail and skip counts and failing test ids as the baseline.
   - After: the same commands. 0 new failures; the pass count drops only by the tests you removed; every lint, format, `make verify-sync` and `git diff --check` check that was green stays green.
   - Each new test fails on the old code and passes on the new code (show both runs in the evidence folder).
   - `superclaude install` into a throwaway HOME succeeds and `superclaude doctor` passes there. Never touch the real ~/.claude.
5. Commit on your branch (conventional message, for example `fix(ic): launcher alias, preset and help fixes (6.0.0)`), push only your branch `clayphi/v6-ic-launcher-fixes`. Stage `.dev/tasks` too if the plan package was created there (the repo rule: `.dev/tasks/` is always staged).
6. Open the PR: `/sc:pr-submit --base integration --head clayphi/v6-ic-launcher-fixes --monitor 3 --repo IronbellyOrg/IronClaude`. Body in plain English: what was removed and what stays, the before and after test counts, the leftover-reference search result, `Closes #542`, `Closes #543`, `Closes #544` and `Refs #571`.
7. Answer every Augment and Codex finding (fix, or reply with evidence) and resolve threads. If the monitor keeps "polling" long after Augment posted a finished review, read it with `gh api` and carry on. If Codex shows its usage-limit notice, say so; it is not a clean review.
8. When every check is green, both reviewers have finished on the final head and no thread is open: STOP. Do not merge. Do not comment to anyone on the PR.

## Process notes for the orchestrator
Keep `.dev/issues/v6-ic-launcher-fixes/PROCESS-NOTES.md`: one line per step with roughly how long it took, what got in the way, and what would make the step easier next release.

## Finish
End with a plain-English report: the DONE / NEXT table, then What I did, How, Where it stands, What's next, My recommendation. Include the PR link, the before and after test counts, and the state of every check and reviewer on the final head.
Never log or commit credentials. No paid model calls beyond your own session. Update the Orca comment at checkpoints: `orca worktree set --worktree active --comment "<short status>"`.

## Notes from wave 1 (orchestrator, 2026-11-17)
- A new worktree has no virtualenv. Run first: `uv venv --python 3.10 && uv pip install -e '.[dev]' 'pytest-xdist>=3.5,<4' && make sync-dev`.
- Known failing tests on `integration` before any edit (they are not yours): `tests/cli/test_install_keep.py::test_same_content_is_true_only_for_identical_readable_files`; and under load, timing or shared-folder tests such as `tests/cli/test_claude_process_adapter*`, `tests/sprint/test_nfr_benchmarks.py` (credit and debit constant-time) and `tests/cli/eval/test_schema_id_rejection.py` (shared `/tmp/eval-runs`). Still take your own baseline, and re-run a failing test alone before calling it new.
- If your PR deletes or edits a file named `gates.py`, `structural_checkers.py` or `*_validator.py`, put a `## Generator-Constraint Considered` section in the PR body when you open it (a CI check fails without it).
- The other PRs of this wave merge first or after yours and touch the same shared files (`PROJECT_INDEX.*`, `docs/developer-guide/technical-architecture.md`, the routing guide). If yours conflicts after another merges, the orchestrator will tell you to rebase on `origin/integration`; keep every removal that is already there.
- Delete your throwaway HOME with a literal path (for example `rm -rf /tmp/throwaway-home.XXXX`), never `rm -rf "$(cat file)"`: that form stops at a permission prompt that nobody answers.
- Do not launch subagents (standing user rule); do the skill steps inline and say so in the PR body and notes.
