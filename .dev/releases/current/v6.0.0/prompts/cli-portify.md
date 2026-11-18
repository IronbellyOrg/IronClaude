# IronClaude 6.0.0, PR 4: remove cli-portify (command-line pipeline, command and skill)

Clay (user clayphi) authorized this pull request on 2026-11-17 as part of the 6.0.0 release (IronClaude issue 571). Your orchestrator is the ic6-orchestrator session. Do the work below in this worktree only, open ONE pull request into `integration`, answer every review finding, make every check green, then STOP. Do NOT merge.

## Scope
Plan item PR 4. Remove cli-portify: `src/superclaude/cli/cli_portify` (about 288 KB), the `/sc:cli-portify` command, and the `sc-cli-portify-protocol` skill (about 83 KB, including its `refs/`), with their mirrors (`.claude`, `plugins/superclaude`, the root `commands/` folder), tests (about 386 KB), the registration in `cli/main.py`, and every mention in docs, hooks, scripts and install code. The plan counted 71 files deleted and 42 edited outside (17 tests, 12 docs, 4 code, 2 scripts, 7 other); known references: the skill mentioned `/sc:build` once (that command is already removed, and the skill goes with this PR). Re-measure; several shared files changed since (PRs 1, 2, 5, 6, 7, 8, 10 and the small fixes are merged into `integration`).
Notes: (1) Do not remove anything the plan keeps: `cli/pipeline` (the shared runner used by the opt-in `reflect` wrapper), `reflect`, swarm, `cli/audit`, the eval harness, `/sc:implement`. If a kept module imports something from `cli/cli_portify`, STOP and tell the orchestrator. (2) If this PR deletes or edits a file named `gates.py`, `structural_checkers.py` or `*_validator.py`, put a `## Generator-Constraint Considered` section in the PR body when you open it. (3) PR 11 (roadmap, tasklist, sprint) comes after this PR because it edits files this PR deletes.
This is wave 4 and runs alone, so no other removal PR is open while you work.

Read issue 571 (body and comments) for the rules: `gh issue view 571 --repo IronbellyOrg/IronClaude --comments`. Swarm and everything in "Kept for now" stays. Do not edit historical records (docs/releases/, docs/testing/v5.0.0/, docs/designs/, past CHANGELOG.md entries); do not add a CHANGELOG.md entry (the release PR does that).

## Steps (the plan's "One flow for every item")
1. Dependency map (read-only): with codegraph (callers, impact) and search, find every command, skill (including refs/), agent, hook, doc, test, install-code entry and mirror (`.claude`, `plugins/superclaude`) that names the item. Write `.dev/cleanup/cli-portify/dependency-map.md`, each reference as path:line with the change it needs. Re-measure: the plan's counts were taken at d4d1662a8 and several shared files changed since.
2. Plan: `/sc:workflow "Remove <item> per .dev/cleanup/cli-portify/dependency-map.md. Acceptance: cli-portify is gone: `superclaude cli-portify` is not listed in `superclaude --help`, /sc:cli-portify and the sc-cli-portify-protocol skill are not installed; every kept module still imports and its tests pass; no file outside the historical records names cli-portify or cli_portify; 0 new test failures and the pass count drops only by the removed tests; lint, format, verify-sync and git diff --check stay green" --depth standard --handoff none`.
3. Implement: `/sc:implement <the plan path it printed>`. Source of truth is `src/superclaude/`; run `make sync-dev` for the mirrors; never stage `.claude/` (except `.claude/settings.json`). Update HOW-WE-WORK.md (both copies), WORKER-CONTRACT.md, core/CLAUDE.md, docs/user-guide/commands.md and the routing tests where they name the item.
4. Regression gate, recorded under `.dev/issues/v6-cli-portify/` (do not commit that folder):
   - Before your first edit, run the full test suite as the `test` job of `.github/workflows/test.yml` runs it (without --maxfail), plus `make lint` and `uv run ruff format --check src/ tests/`. Save pass, fail and skip counts and failing test ids as the baseline.
   - After: the same commands. 0 new failures; the pass count drops only by the tests you removed; every lint, format, `make verify-sync` and `git diff --check` check that was green stays green.
   - A search finds no remaining file that names the removed item, outside the historical records.
   - `superclaude install` into a throwaway HOME succeeds and `superclaude doctor` passes there. Never touch the real ~/.claude.
5. Commit on your branch (conventional message, for example `refactor(cli): remove cli-portify (6.0.0)`), push only your branch `clayphi/v6-cli-portify`. Stage `.dev/tasks` too if the plan package was created there (the repo rule: `.dev/tasks/` is always staged).
6. Open the PR: `/sc:pr-submit --base integration --head clayphi/v6-cli-portify --monitor 3 --repo IronbellyOrg/IronClaude`. Body in plain English: what was removed and what stays, the before and after test counts, the leftover-reference search result, `Refs #571`.
7. Answer every Augment and Codex finding (fix, or reply with evidence) and resolve threads. If the monitor keeps "polling" long after Augment posted a finished review, read it with `gh api` and carry on. If Codex shows its usage-limit notice, say so; it is not a clean review.
8. When every check is green, both reviewers have finished on the final head and no thread is open: STOP. Do not merge. Do not comment to anyone on the PR.

## Process notes for the orchestrator
Keep `.dev/issues/v6-cli-portify/PROCESS-NOTES.md`: one line per step with roughly how long it took, what got in the way, and what would make the step easier next release.

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
