# IronClaude 6.0.0, PR 8: remove /sc:improve

Clay (user clayphi) authorized this pull request on 2026-11-17 as part of the 6.0.0 release (IronClaude issue 571). Your orchestrator is the ic6-orchestrator session. Do the work below in this worktree only, open ONE pull request into `integration`, answer every review finding, make every check green, then STOP. Do NOT merge.

## Scope
Plan item PR 8. Remove `/sc:improve`: the command file `src/superclaude/commands/improve.md`, its mirrors, and every mention. The plan counted 3 files deleted and 19 edited outside (3 tests, 5 docs, 2 scripts, 12 other); known references: `core/CLAUDE.md` 1, `HOW-WE-WORK.md` 5 (both copies), `WORKER-CONTRACT.md` 1, the `adversarial` and `analyze` commands 1 each. Re-measure. Scripts `hooks/scripts/launch-level-guard.sh` and its test may name it (earlier PRs already removed their own lines; edit only the `/sc:improve` lines).
The improve half of issue 506 (usage line versus examples for `/sc:improve`) is held: it goes away with this removal, so do NOT fix it. Small-fix PR A fixes the cleanup half of 506 in another worktree. Say so in the PR body (`Refs #571`, `Refs #506`).
What stays: `/sc:cleanup`, `/sc:analyze`, `/sc:adversarial`; only the lines that point a reader to `/sc:improve` change. Where a sentence recommends `/sc:improve` as a next step, use the smallest edit that stays true (name the kept command that does the job, or drop the clause); if no kept command fits, STOP and tell the orchestrator.
Part of wave 3, with small-fix PR A (help-text fixes) and small-fix PR B (ic launcher fixes) running in parallel in other worktrees.

Read issue 571 (body and comments) for the rules: `gh issue view 571 --repo IronbellyOrg/IronClaude --comments`. Swarm and everything in "Kept for now" stays. Do not edit historical records (docs/releases/, docs/testing/v5.0.0/, docs/designs/, past CHANGELOG.md entries); do not add a CHANGELOG.md entry (the release PR does that).

## Steps (the plan's "One flow for every item")
1. Dependency map (read-only): with codegraph (callers, impact) and search, find every command, skill (including refs/), agent, hook, doc, test, install-code entry and mirror (`.claude`, `plugins/superclaude`) that names the item. Write `.dev/cleanup/improve/dependency-map.md`, each reference as path:line with the change it needs. Re-measure: the plan's counts were taken at d4d1662a8 and several shared files changed since.
2. Plan: `/sc:workflow "Remove <item> per .dev/cleanup/improve/dependency-map.md. Acceptance: /sc:improve is gone from commands, mirrors, docs, routing guide, hook scripts and routing tests; the routing table checks pass; no file outside the historical records names /sc:improve; 0 new test failures and the pass count drops only by the removed tests; lint, format, verify-sync and git diff --check stay green" --depth standard --handoff none`.
3. Implement: `/sc:implement <the plan path it printed>`. Source of truth is `src/superclaude/`; run `make sync-dev` for the mirrors; never stage `.claude/` (except `.claude/settings.json`). Update HOW-WE-WORK.md (both copies), WORKER-CONTRACT.md, core/CLAUDE.md, docs/user-guide/commands.md and the routing tests where they name the item.
4. Regression gate, recorded under `.dev/issues/v6-improve/` (do not commit that folder):
   - Before your first edit, run the full test suite as the `test` job of `.github/workflows/test.yml` runs it (without --maxfail), plus `make lint` and `uv run ruff format --check src/ tests/`. Save pass, fail and skip counts and failing test ids as the baseline.
   - After: the same commands. 0 new failures; the pass count drops only by the tests you removed; every lint, format, `make verify-sync` and `git diff --check` check that was green stays green.
   - A search finds no remaining file that names the removed item, outside the historical records.
   - `superclaude install` into a throwaway HOME succeeds and `superclaude doctor` passes there. Never touch the real ~/.claude.
5. Commit on your branch (conventional message, for example `refactor(commands): remove /sc:improve (6.0.0)`), push only your branch `clayphi/v6-improve`. Stage `.dev/tasks` too if the plan package was created there (the repo rule: `.dev/tasks/` is always staged).
6. Open the PR: `/sc:pr-submit --base integration --head clayphi/v6-improve --monitor 3 --repo IronbellyOrg/IronClaude`. Body in plain English: what was removed and what stays, the before and after test counts, the leftover-reference search result, `Refs #571` and `Refs #506`.
7. Answer every Augment and Codex finding (fix, or reply with evidence) and resolve threads. If the monitor keeps "polling" long after Augment posted a finished review, read it with `gh api` and carry on. If Codex shows its usage-limit notice, say so; it is not a clean review.
8. When every check is green, both reviewers have finished on the final head and no thread is open: STOP. Do not merge. Do not comment to anyone on the PR.

## Process notes for the orchestrator
Keep `.dev/issues/v6-improve/PROCESS-NOTES.md`: one line per step with roughly how long it took, what got in the way, and what would make the step easier next release.

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
