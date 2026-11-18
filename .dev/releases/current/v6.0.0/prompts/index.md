# IronClaude 6.0.0, PR 9: remove /sc:index and /sc:index-repo

Clay (user clayphi) authorized this pull request on 2026-11-17 as part of the 6.0.0 release (IronClaude issue 571). Your orchestrator is the ic6-orchestrator session. Do the work below in this worktree only, open ONE pull request into `integration`, answer every review finding, make every check green, then STOP. Do NOT merge.

## Scope
Plan item PR 9. Remove `/sc:index` and `/sc:index-repo`: the two command files and their mirrors (`.claude`, `plugins/superclaude`, the root `commands/` folder), and every mention. The plan counted 6 files deleted and 9 edited outside (3 tests, 2 docs, 4 other); known references: `HOW-WE-WORK.md` 3 and 1 (both copies), `WORKER-CONTRACT.md` 2. Re-measure; several shared files changed since.
What stays: the `repo-index` agent and every other agent (agents are a separate evaluation, issue 572), codegraph and the `/sc:graph` command. Only the lines that tell a reader to run `/sc:index` or `/sc:index-repo` change; use the smallest edit that keeps the sentence true (name `/sc:graph` or codegraph only where it really does the job, otherwise drop the clause). If a kept skill or command cannot work without the removed commands, STOP and tell the orchestrator.
Part of wave 5, with PR 11 (roadmap, tasklist and sprint, a much larger PR) running in parallel in another worktree. This PR is small and should merge first; PR 11 will then rebase.

Read issue 571 (body and comments) for the rules: `gh issue view 571 --repo IronbellyOrg/IronClaude --comments`. Swarm and everything in "Kept for now" stays. Do not edit historical records (docs/releases/, docs/testing/v5.0.0/, docs/designs/, past CHANGELOG.md entries); do not add a CHANGELOG.md entry (the release PR does that).

## Steps (the plan's "One flow for every item")
1. Dependency map (read-only): with codegraph (callers, impact) and search, find every command, skill (including refs/), agent, hook, doc, test, install-code entry and mirror (`.claude`, `plugins/superclaude`) that names the item. Write `.dev/cleanup/index/dependency-map.md`, each reference as path:line with the change it needs. Re-measure: the plan's counts were taken at d4d1662a8 and several shared files changed since.
2. Plan: `/sc:workflow "Remove <item> per .dev/cleanup/index/dependency-map.md. Acceptance: /sc:index and /sc:index-repo are gone from commands, mirrors, docs, routing guide, worker contract and routing tests; the routing table checks pass; no file outside the historical records names them; 0 new test failures and the pass count drops only by the removed tests; lint, format, verify-sync and git diff --check stay green" --depth standard --handoff none`.
3. Implement: `/sc:implement <the plan path it printed>`. Source of truth is `src/superclaude/`; run `make sync-dev` for the mirrors; never stage `.claude/` (except `.claude/settings.json`). Update HOW-WE-WORK.md (both copies), WORKER-CONTRACT.md, core/CLAUDE.md, docs/user-guide/commands.md and the routing tests where they name the item.
4. Regression gate, recorded under `.dev/issues/v6-index/` (do not commit that folder):
   - Before your first edit, run the full test suite as the `test` job of `.github/workflows/test.yml` runs it (without --maxfail), plus `make lint` and `uv run ruff format --check src/ tests/`. Save pass, fail and skip counts and failing test ids as the baseline.
   - After: the same commands. 0 new failures; the pass count drops only by the tests you removed; every lint, format, `make verify-sync` and `git diff --check` check that was green stays green.
   - A search finds no remaining file that names the removed item, outside the historical records.
   - `superclaude install` into a throwaway HOME succeeds and `superclaude doctor` passes there. Never touch the real ~/.claude.
5. Commit on your branch (conventional message, for example `refactor(commands): remove /sc:index and /sc:index-repo (6.0.0)`), push only your branch `clayphi/v6-index`. Stage `.dev/tasks` too if the plan package was created there (the repo rule: `.dev/tasks/` is always staged).
6. Open the PR: `/sc:pr-submit --base integration --head clayphi/v6-index --monitor 3 --repo IronbellyOrg/IronClaude`. Body in plain English: what was removed and what stays, the before and after test counts, the leftover-reference search result, `Refs #571`.
7. Answer every Augment and Codex finding (fix, or reply with evidence) and resolve threads. If the monitor keeps "polling" long after Augment posted a finished review, read it with `gh api` and carry on. If Codex shows its usage-limit notice, say so; it is not a clean review.
8. When every check is green, both reviewers have finished on the final head and no thread is open: STOP. Do not merge. Do not comment to anyone on the PR.

## Process notes for the orchestrator
Keep `.dev/issues/v6-index/PROCESS-NOTES.md`: one line per step with roughly how long it took, what got in the way, and what would make the step easier next release.

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
