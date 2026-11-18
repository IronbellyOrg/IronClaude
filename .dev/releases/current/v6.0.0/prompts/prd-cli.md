# IronClaude 6.0.0, PR 1: remove the prd command-line pipeline

Clay (user clayphi) authorized this pull request on 2026-11-17 as part of the 6.0.0 release (IronClaude issue 571). Your orchestrator is the ic6-orchestrator session. Do the work below in this worktree only, open ONE pull request into `integration`, answer every review finding, make every check green, then STOP. Do NOT merge.

## Scope
Plan item PR 1. Remove the `prd` command-line pipeline: `src/superclaude/cli/prd` (about 217 KB) and its registration in `cli/main.py`, plus the tests, the one hook script and the `cli/eval/orchestrator.py` mention that name it (re-measure; the plan counted 32 files deleted, 13 edited outside). The plan found no reference to it in any command or skill, and nothing else in the source imports it except the registration in `cli/main.py`.
What stays: the interactive `prd` skill (a different thing from the command-line pipeline).
Part of wave 1 (approved by Ryan, 2026-11-17 07:27), with PR 2 (cleanup-audit runner) and PR 5 (`/sc:spawn`) running in parallel in other worktrees.

Read issue 571 (body and comments) for the rules: `gh issue view 571 --repo IronbellyOrg/IronClaude --comments`. Swarm and everything in "Kept for now" stays. Do not edit historical records (docs/releases/, docs/testing/v5.0.0/, docs/designs/, past CHANGELOG.md entries); do not add a CHANGELOG.md entry (the release PR does that).

## Steps (the plan's "One flow for every item")
1. Dependency map (read-only): with codegraph (callers, impact) and search, find every command, skill (including refs/), agent, hook, doc, test, install-code entry and mirror (`.claude`, `plugins/superclaude`) that names the item. Write `.dev/cleanup/prd-cli/dependency-map.md`, each reference as path:line with the change it needs. Re-measure: the plan's counts were taken at d4d1662a8 and several shared files changed since.
2. Plan: `/sc:workflow "Remove <item> per .dev/cleanup/prd-cli/dependency-map.md. Acceptance: `superclaude prd` is gone and `superclaude --help` does not list it; the interactive prd skill still installs; no file outside the historical records names the removed pipeline; 0 new test failures and the pass count drops only by the removed tests; lint, format, verify-sync and git diff --check stay green" --depth standard --handoff none`.
3. Implement: `/sc:implement <the plan path it printed>`. Source of truth is `src/superclaude/`; run `make sync-dev` for the mirrors; never stage `.claude/` (except `.claude/settings.json`). Update HOW-WE-WORK.md (both copies), WORKER-CONTRACT.md, core/CLAUDE.md, docs/user-guide/commands.md and the routing tests where they name the item.
4. Regression gate, recorded under `.dev/issues/v6-prd-cli/` (do not commit that folder):
   - Before your first edit, run the full test suite as the `test` job of `.github/workflows/test.yml` runs it (without --maxfail), plus `make lint` and `uv run ruff format --check src/ tests/`. Save pass, fail and skip counts and failing test ids as the baseline.
   - After: the same commands. 0 new failures; the pass count drops only by the tests you removed; every lint, format, `make verify-sync` and `git diff --check` check that was green stays green.
   - A search finds no remaining file that names the removed item, outside the historical records.
   - `superclaude install` into a throwaway HOME succeeds and `superclaude doctor` passes there. Never touch the real ~/.claude.
5. Commit on your branch (conventional message, for example `refactor(cli): remove the prd command-line pipeline (6.0.0)`), push only your branch `clayphi/v6-prd-cli`. Stage `.dev/tasks` too if the plan package was created there (the repo rule: `.dev/tasks/` is always staged).
6. Open the PR: `/sc:pr-submit --base integration --head clayphi/v6-prd-cli --monitor 3 --repo IronbellyOrg/IronClaude`. Body in plain English: what was removed and what stays, the before and after test counts, the leftover-reference search result, `Refs #571`.
7. Answer every Augment and Codex finding (fix, or reply with evidence) and resolve threads. If the monitor keeps "polling" long after Augment posted a finished review, read it with `gh api` and carry on. If Codex shows its usage-limit notice, say so; it is not a clean review.
8. When every check is green, both reviewers have finished on the final head and no thread is open: STOP. Do not merge. Do not comment to anyone on the PR.

## Process notes for the orchestrator
Keep `.dev/issues/v6-prd-cli/PROCESS-NOTES.md`: one line per step with roughly how long it took, what got in the way, and what would make the step easier next release.

## Finish
End with a plain-English report: the DONE / NEXT table, then What I did, How, Where it stands, What's next, My recommendation. Include the PR link, the before and after test counts, and the state of every check and reviewer on the final head.
Never log or commit credentials. No paid model calls beyond your own session. Update the Orca comment at checkpoints: `orca worktree set --worktree active --comment "<short status>"`.
