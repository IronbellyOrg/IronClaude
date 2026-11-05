---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-revisedPlanRefac-20261102-213941
version: "1"
priority: Medium
created_date: "2026-11-02"
---

# Move IronClaude to Orca's default worktree paths, make eval_runner self-cleaning, and forbid all upstream interaction (revised)

Source: ./source.md
Goal: No tracked file outside `.dev/` tells anyone to create a project worktree under `.dev/worktrees/` or with raw `git worktree add`. Project worktrees are created by Orca at its default location, outside the main checkout. Every internal temporary checkout made by a CLI or a test, including `scripts/eval_runner.py`, creates and removes its own checkout and works without Orca, and its tests prove that by running with zero unexplained skips. The CLAUDE.md fork rule forbids any tool call, remote or link flag that reaches `SuperClaude-Org/SuperClaude_Framework`, with no exceptions, and none of its own checks contradict it.

## Constraints

- This plan supersedes `.dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/TASK-WF-refactorIronClau-20261102-162730.md` and resolves the 14 deviations D-001 to D-014 in `.dev/reflect/pre-refactorIronClau-20261102175540/REPORT.md`. Each task names the deviations it resolves. Do not execute the superseded plan.
- Two searches define the hit set. Search A is the spec's: `git grep -n -E '\.dev/worktrees|git worktree add' -- ':!.dev'` (108 lines in 17 files on 2026-11-02). Search B finds list-argument calls the spec's search cannot see: `git grep -n -E '"worktree",\s*"add"' -- ':!.dev'` (9 lines in 7 files on 2026-11-02). Each search keeps its own total. Do not edit anything under `.dev/` except this package's `./artifacts/`.
- `src/superclaude/` is the source of truth. `.claude/` is the generated mirror refreshed by `make sync-dev`. Never stage any `.claude/` path except `.claude/settings.json`, and never run `git add -f` on a `.claude/` path. This plan does not touch the tracked `.claude/cache/` files.
- `plugins/superclaude/commands/recommend.md`, `plugins/superclaude/skills/sc-recommend/SKILL.md` and `plugins/superclaude/skills/sc-recommend/refs/surface-enumeration.md` are byte copies of their `src/superclaude/` originals and must stay byte-identical (tests/commands/test_routing_plugin_parity.py). `sc-post-release-protocol` has no plugin copy.
- Installed primitives (`src/superclaude/{commands,skills}`) must not gain a host path such as `/home/coder/...` or a `src/superclaude/...` path. Describe Orca's location generically: Orca's default worktree location, outside the main checkout; the real path is shown by `orca worktree current --json` or `orca worktree list`.
- Confirmed Orca surface (from `--help` on 2026-11-02): `orca worktree create --name <name> [--repo <selector>] [--base-branch <ref>] [--parent-worktree <selector>|--no-parent] [--json]`, which also lists the link flags `--issue` and `--pr`; `orca worktree list [--repo <selector>] [--json]`; `orca worktree current [--json]`; `orca worktree rm --worktree <selector> [--force] [--json]`, where a selector is for example `path:<path>`, `name:<displayName>` or `branch:<branch>`. Do not name other Orca subcommands or flags without checking their `--help` first (resolves D-010).
- This repository has only an `origin` remote (`git remote -v`, 2026-11-02). No rule may depend on a remote named `upstream`, and no task adds one.
- `POST-REFLECT-TASK.md` is a historical record (owner decision) and stays byte-unchanged.
- The two existing checkouts under the retired location, `/home/coder/workspaces/IronClaude/.dev/worktrees/issue-body-templates` and `/home/coder/workspaces/IronClaude/.dev/worktrees/markdownlint-issue-body-files` (`git worktree list`, 2026-11-02), are recorded only. No task moves, removes or edits them.
- Make no GitHub, git-remote or Orca call that reaches `SuperClaude-Org/SuperClaude_Framework` while executing this plan.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), including this package and its `./artifacts/`. Staging is not committing: commit only when the user asks.

## Phase 1: Classify every hit

## Task 1: Write the two-search classification inventory

Run Search A and Search B (see Constraints), each with `-n` and with `-c`, and save the raw outputs to `./artifacts/t1-search-a.txt` and `./artifacts/t1-search-b.txt`. Also save `git worktree list` to `./artifacts/t1-worktree-list.txt`. Write `./artifacts/worktree-hit-classification.md` with these parts, in this order (resolves D-003, D-006, D-007, D-012, D-013, D-014):

- First line of the summary: "Historical record: POST-REFLECT-TASK.md, 79 of the Search A hits, left unchanged. The file's status is Blocked (POST-REFLECT-TASK.md:6) and its `.dev/worktrees` paths are intentionally stale; anyone resuming it must substitute an Orca-created worktree."
- A Search A table and a Search B table, each one row per file with its own hit count, class, action and one-line reason, with counts summing to that search's live total. A file found by both searches appears in both tables.
- Classes and assignments:
  - Project worktree, rewrite to Orca's default location: `CLAUDE.md` (subsection `### Parallel Development with Git Worktrees`, Task 3); `.gitignore` (action: "rewrite comment only; keep the `.dev/worktrees/` entry as a retired-path guard", Task 5); `src/superclaude/commands/recommend.md`, `src/superclaude/skills/sc-recommend/SKILL.md`, `src/superclaude/skills/sc-recommend/refs/surface-enumeration.md` and their three `plugins/superclaude/` copies (Tasks 6-7); `tests/docs/test_tavily_doc_alignment.py` (comment only, Task 8).
  - Internal temporary checkout, works without Orca: `scripts/eval_runner.py` (rewritten in Task 2 to create its master checkout in a temporary directory and remove it); `src/superclaude/cli/reflect/config.py` and `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (reflect `--isolate-reviewers` snapshot, removed with `git worktree remove --force`); `src/superclaude/skills/sc-post-release-protocol/SKILL.md` (optional read-only tag checkout, removed after the scan, wording made explicit in Task 6); `tests/cli/reflect/test_isolate_reviewers_cli.py`; `tests/skills/test_implement_retry_revert.py`, `tests/unit/test_ccsession_tag.py` (fixture repos in pytest `tmp_path`); `tests/troubleshoot/backtest/git_replay.py`, `tests/troubleshoot/backtest/test_git_replay_integration.py`, `tests/troubleshoot/backtest/test_git_replay_unit.py` (backtest replay, removed after use or mocked).
  - Historical record, unchanged: `POST-REFLECT-TASK.md`.
- A section "Outside both searches, recorded only": `docs/swarm/runbook.md:34` cites `/config/workspace/IronClaude/.claude/worktrees/BareReview/CLAUDE.md`, a documentation reference to another host's checkout, out of scope and left unchanged.
- A section "Existing checkouts at the retired location": every `git worktree list` line containing `/.dev/worktrees/`, with the note "left in place; not moved or removed by this plan".

If either live total differs from the 2026-11-02 baseline in the Constraints, classify every new hit with the same three classes and note the difference at the top.

Acceptance criteria:
- The Search A and Search B tables each have one row per file in that search's live `-c` output, and each table's counts sum to that search's live total.
- The summary's first line is the Historical record statement above, and the `.gitignore` row's action reads "rewrite comment only; keep the `.dev/worktrees/` entry as a retired-path guard".
- The "Outside both searches" and "Existing checkouts at the retired location" sections exist, and the second lists every `/.dev/worktrees/` line from `./artifacts/t1-worktree-list.txt`.

## Phase 2: Make eval_runner an internal temporary checkout

## Task 2: Rewrite scripts/eval_runner.py to create and remove its own master checkout, with a regression test

Depends on: Task 1

Resolves D-001 (owner decision 2026-11-02). Today `run_global` creates `REPO_ROOT.parent / "IronClaude-eval-master"` with a list-argument `git worktree add ... master`, ignores the exit code and never removes it, and `main` reuses that path for the global E2E scripts.

In `scripts/eval_runner.py`:
- Add a context manager `master_checkout()` that creates a directory with `tempfile.mkdtemp(prefix="ironclaude-eval-master-")` and runs `git worktree add --detach <that directory> master` with `cwd=REPO_ROOT`. `--detach` lets it work while `master` is checked out in the main checkout. On a non-zero exit it raises an error carrying git's stderr. In `finally` it runs `git worktree remove --force <that directory>` (never `rm -rf`), so the checkout is removed when the body succeeds and when it raises.
- Change `run_global(run_id)` to `run_global(run_id, checkout)` so it runs against the path it is given.
- In `main`, wrap the whole global block (`run_global("A")`, `run_global("B")` and the global E2E scripts) in one `with master_checkout() as checkout:`. If the checkout cannot be created, append a `RunResult` named `global-setup` with `errors=1` and git's stderr in `failures`; do not fail silently.
- Remove every use of `IronClaude-eval-master`, and update the module docstring's "(master worktree)" wording to "(temporary master checkout)".

Add `tests/unit/test_eval_runner_master_checkout.py`. It loads the script with `importlib.util.spec_from_file_location` (the pattern at tests/swarm/test_bare_review_golden_regen.py:153), builds a throwaway git repo in pytest `tmp_path` with a commit on `master`, and points the module's `REPO_ROOT` at it. Tests:
- inside `master_checkout()` the path exists and appears in `git worktree list`; after exit it is gone from disk and from `git worktree list`;
- the checkout is removed when the body raises;
- a repo with no `master` branch makes `master_checkout()` raise with git's stderr, not succeed silently;
- the script source contains no `IronClaude-eval-master`.

Acceptance criteria:
- `uv run pytest tests/unit/test_eval_runner_master_checkout.py -v` passes, and the same tests fail against the pre-change `scripts/eval_runner.py` (run once before the edit and save the output to `./artifacts/t2-fail-before.txt`; save the passing run to `./artifacts/t2-pass-after.txt`).
- `grep -n 'IronClaude-eval-master' scripts/eval_runner.py` prints nothing, and `grep -n 'worktree", "remove"' scripts/eval_runner.py` prints the teardown line.
- `uv run ruff check scripts/eval_runner.py tests/unit/test_eval_runner_master_checkout.py` and `uv run ruff format --check` on the same two files exit 0.

## Phase 3: Rewrite the repository rules

## Task 3: Replace the worktree rule in CLAUDE.md with the Orca rule

Depends on: Task 2

In `CLAUDE.md`, rewrite the subsection `### Parallel Development with Git Worktrees` (under `## 🌿 Git Workflow`). Today it holds an "ABSOLUTE RULE — worktree location is `./.dev/worktrees/`" paragraph, a bash block using `git worktree add .dev/worktrees/...`, a Usage list naming `<repo>/.dev/worktrees/...`, and a Cleanup block using `git worktree remove .dev/worktrees/integration`. The new subsection must (resolves D-012, D-013 and part of D-001):

- State the absolute rule: every project worktree is created through Orca with `orca worktree create --name <name>` (with `--repo <selector>`, `--base-branch <ref>`, and `--parent-worktree <selector>` or `--no-parent` as needed) and lives at Orca's default worktree location, outside the main checkout; `orca worktree current --json` and `orca worktree list` show the real path.
- Forbid creating project worktrees with raw `git worktree add`, under the retired `.dev/worktrees/` location, or under `.claude/worktrees/`. Keep the ban on the `EnterWorktree` tool and its reason: it hardcodes `.claude/worktrees/`, which is gitignored sync-dev territory.
- Forbid Orca link flags (`--issue`, `--pr`) for this repo, pointing to the fork rule edited in Task 4.
- State the exception: internal temporary checkouts that a CLI, script or test creates and removes itself keep using `git worktree add` directly and must work without Orca. Name the five cases: the reflect `--isolate-reviewers` snapshot; the troubleshoot backtest replay; test fixtures in a pytest temporary directory; `scripts/eval_runner.py`'s temporary master checkout; and the optional read-only release-tag checkout in `/sc:post-release`, removed after the scan.
- Say what happens to existing checkouts under the retired `.dev/worktrees/` location: they may stay until their branch is merged, then are removed with `git worktree remove`; no new checkout may be created there.
- Rewrite Usage so session A opens the main checkout and sessions B and C open Orca-created worktrees. Rewrite Cleanup to use `orca worktree rm --worktree <selector>`, for example `orca worktree rm --worktree name:<name>`.
- Remove the instruction to add `.dev/worktrees/` to `.gitignore`, and contain no host absolute path such as `/home/coder/...`.

Acceptance criteria:
- `git grep -n -E '\.dev/worktrees|git worktree add' -- CLAUDE.md` prints only lines that forbid the retired location, describe existing checkouts there, or state the internal-checkout exception. The output is saved to `./artifacts/t3-claude-md-grep.txt`.
- The subsection names `orca worktree create`, `orca worktree list` or `orca worktree current`, and `orca worktree rm --worktree`, names all five exception cases, states the rule for existing retired-location checkouts, and still forbids `EnterWorktree`.
- `grep -n '/home/coder' CLAUDE.md` prints nothing.

## Task 4: Tighten the fork rule so SuperClaude upstream is never touched

Depends on: Task 3

In `CLAUDE.md`, edit the section `## ABSOLUTE RULE: PR Target = Fork (`IronbellyOrg/IronClaude`), NEVER Upstream`. Keep the heading text unchanged. Resolves D-002, D-004, D-005 and D-009.

- Open with an unconditional rule: SuperClaude upstream (`SuperClaude-Org/SuperClaude_Framework`) is never pushed to or interacted with. No push, fetch or pull from it; no PR, issue, comment, review or reaction there; no remote pointing at it; and no tool call (gh, git or Orca) and no gh or Orca link flag that resolves to it. The fetch/pull ban is the literal reading of "interacted with" (D-009).
- Replace the remotes sentence that says `upstream` = `SuperClaude-Org/SuperClaude_Framework` with: this clone has only `origin` (`IronbellyOrg/IronClaude`); the public parent is `SuperClaude-Org/SuperClaude_Framework`; no remote for it may be added. Rewrite the bullet "Push to `upstream` (the `upstream` remote name above)" so it does not depend on a remote named `upstream` (D-004).
- Make the bullet "Open PRs against `SuperClaude-Org/SuperClaude_Framework` without explicit user authorization in the same session" an unconditional prohibition.
- Rewrite pre-PR check 1 (today: a bare `gh repo view --json nameWithOwner -q .nameWithOwner` that may print the upstream parent) to: `git remote get-url origin` must print the `IronbellyOrg/IronClaude` URL, and `gh repo view IronbellyOrg/IronClaude --json nameWithOwner -q .nameWithOwner` must print `IronbellyOrg/IronClaude`; if gh's default repo is wrong, run `gh repo set-default IronbellyOrg/IronClaude` (D-002).
- Rewrite pre-PR check 3 (today: "If it shows the wrong owner, close it immediately and reopen") to: if a PR URL points at `SuperClaude-Org`, stop, report the URL to the user, and take no action on that PR; the user closes it. This matches `/sc:pr-submit`, which already halts on a misrouted URL (D-002).
- List the allowed gh forms: a command that accepts `--repo` passes `--repo IronbellyOrg/IronClaude`; a command that takes the repo as a positional argument (`gh repo view`) names `IronbellyOrg/IronClaude` explicitly; a `gh api` path spells `repos/IronbellyOrg/IronClaude/...`, never the `{owner}/{repo}` placeholder (D-002).
- Add a bullet recording that Orca identified this project as `github:superclaude-org/superclaude_framework` in `orca worktree current --json` on 2026-11-02, that the source of that id is unverified (possibly the upstream URLs in `pyproject.toml` or `package.json`), and that until `orca worktree current --json` shows the fork's project id, `--issue`, `--pr` and other Orca link flags are never passed for this repo. This bullet is an authorized addition backed by the owner's standing instruction (D-004, D-009).
- State that static references to the upstream repository in documentation and test fixtures (for example the negative fixtures in `tests/pr_submit/test_pre_pr_checks.py`) are not "interaction" and are out of scope. Decide the `#419` issue link in `CLAUDE.md`'s Slash Commands note explicitly: keep it unchanged as a static documentation reference (D-005).
- Replace the `**Exceptions:**` paragraph that allows contributing back to upstream with "There are no exceptions." Keep the `/sc:pr-submit --monitor 3` instruction, the fallback `gh pr create --repo IronbellyOrg/IronClaude ...` block, pre-PR check 2 and the Rationale paragraph, editing them only where they contradict the rules above.

Acceptance criteria:
- `grep -n -i -E 'close it immediately|contributing back' CLAUDE.md` prints nothing.
- Every line in the section that runs a `gh` command names `IronbellyOrg/IronClaude` (by `--repo`, positionally, or in an `api` path) or states a prohibition; the check is saved as `./artifacts/t4-gh-lines.txt` from `grep -n 'gh ' CLAUDE.md`.
- No line in the section makes a rule depend on a remote named `upstream`; the section states the clone has only `origin`, contains the Orca project-id bullet, states the static-reference scope, and contains "There are no exceptions."
- `git diff CLAUDE.md` shows no change to the section heading line, and the `#419` line in the Slash Commands note is unchanged.

## Task 5: Mark .dev/worktrees as retired in .gitignore

Depends on: Task 1

In `.gitignore`, replace the two comment lines above the `.dev/worktrees/` entry (today: "canonical location is .dev/worktrees/<name>/") with a comment saying this location is retired, that Orca creates project worktrees at its default location outside the repository, and that the entry stays so existing or leftover checkouts here are never staged. Keep the `.dev/worktrees/` entry (resolves D-007).

Acceptance criteria:
- No `.gitignore` line calls `.dev/worktrees/` canonical; the comment says it is retired and that Orca creates project worktrees outside the repository.
- `git check-ignore -q .dev/worktrees/example` exits 0.

## Phase 4: Update the installed primitives and their mirrors

## Task 6: Make the sc-recommend surfaces location-neutral and state the post-release checkout removal

Depends on: Task 1

Edit these source-of-truth files. Keep each sentence's meaning: paths resolve against the worktree that `git rev-parse --show-toplevel` returns.

- `src/superclaude/commands/recommend.md`, `## Output Constraints`, the bullet that says "When cwd is `.dev/worktrees/<name>/`": change it to "When cwd is inside a linked git worktree (for example one Orca created at its default location outside the main checkout), paths resolve against that worktree, not the main checkout."
- `src/superclaude/skills/sc-recommend/SKILL.md`, the paragraph beginning "The checkout paths (row 7) resolve under the repository root": replace "If the user's cwd is a worktree under `.dev/worktrees/<name>/`" with wording about a linked worktree, such as an Orca-created worktree outside the main checkout.
- `src/superclaude/skills/sc-recommend/SKILL.md`, the bullet "worktree-aware paths (resolved under `git rev-parse --show-toplevel`, which is the worktree's root when cwd is inside `.dev/worktrees/<name>/`)": end it with "when cwd is inside a linked worktree".
- `src/superclaude/skills/sc-recommend/refs/surface-enumeration.md`, the sentence "The current worktree is the repository root returned by `git rev-parse --show-toplevel`, including when cwd is under `.dev/worktrees/<name>/`.": end it with "including when cwd is inside a linked worktree (such as an Orca-created one)". Keep "Never redirect lookups to another checkout by assumption."
- `src/superclaude/skills/sc-post-release-protocol/SKILL.md`, the paragraph "Anchor the scan to the tagged commit": where it offers "a `git worktree add` / `git archive` checkout of the tag", add that such a checkout is made in a temporary directory and removed with `git worktree remove` after the scan (resolves D-012).

Acceptance criteria:
- `git grep -n '\.dev/worktrees' -- src/superclaude/commands/recommend.md src/superclaude/skills/sc-recommend` prints nothing.
- The post-release paragraph names a temporary directory and `git worktree remove` for the optional tag checkout.
- No line added in `git diff -- src/superclaude/commands/recommend.md src/superclaude/skills/sc-recommend src/superclaude/skills/sc-post-release-protocol` contains `/home/` or `src/superclaude/`. The diff is saved to `./artifacts/t6-primitives.diff`.

## Task 7: Mirror the edits to the plugin copy and the dev mirror, and run the contract tests

Depends on: Task 6

Copy the three sc-recommend files edited in Task 6 byte-for-byte to `plugins/superclaude/commands/recommend.md`, `plugins/superclaude/skills/sc-recommend/SKILL.md` and `plugins/superclaude/skills/sc-recommend/refs/surface-enumeration.md`. Then run `make sync-dev`, `make verify-sync`, and `uv run pytest tests/commands/test_routing_plugin_parity.py tests/recommend/ tests/skills/test_sc_recommend_routing_contract.py tests/unit/test_cli_install.py -v` (resolves D-011; `tests/unit/test_cli_install.py` covers the installed post-release skill).

Acceptance criteria:
- `cmp` reports each `plugins/superclaude/...` file identical to its `src/superclaude/...` original.
- `make verify-sync` exits 0; output saved to `./artifacts/t7-verify-sync.txt`.
- The pytest run passes; output saved to `./artifacts/t7-pytest.txt`.
- `git diff --cached --name-only` lists no `.claude/` path other than `.claude/settings.json`.

## Phase 5: Prove internal checkouts work and confirm the residual hits

## Task 8: Fix the tavily comment, run the internal-checkout tests with no silent skips, and record the residual hits

Depends on: Task 2, Task 3, Task 4, Task 5, Task 7

In `tests/docs/test_tavily_doc_alignment.py`, function `_iter_text_files`, rewrite the comment that says "the worktree itself lives under `.dev/worktrees/…`" to say the checkout itself may sit under a directory whose name is in `_EXCLUDE_DIRS` (for example an older checkout under `.dev/`), so testing `p.parts` would exclude every file and make the guard vacuous. Change only the comment.

Then prove the internal temporary checkouts work without Orca (resolves D-008) by running `uv run pytest tests/cli/reflect/test_isolate_reviewers_cli.py tests/skills/test_implement_retry_revert.py tests/troubleshoot/backtest/test_git_replay_integration.py tests/troubleshoot/backtest/test_git_replay_unit.py tests/unit/test_ccsession_tag.py tests/unit/test_eval_runner_master_checkout.py -v -rs` and saving the output to `./artifacts/t8-internal-checkouts.txt`. Record `git rev-parse --is-shallow-repository` and `id -u` beside it.

Finally re-run Search A and Search B and save them to `./artifacts/t8-residual-a.txt` and `./artifacts/t8-residual-b.txt`.

Acceptance criteria:
- `uv run pytest tests/docs/test_tavily_doc_alignment.py -v` passes, and `uv run ruff check` and `uv run ruff format --check` on that file exit 0.
- The internal-checkout run passes with no SKIPPED line, or every skip reason is recorded in `./artifacts/t8-internal-checkouts.txt` and the run is repeated in a full-depth (`git rev-parse --is-shallow-repository` prints `false`), non-root (`id -u` is not 0) checkout with no SKIPPED line.
- Every remaining Search A line is in a file classified "internal temporary checkout" or "historical record" in `./artifacts/worktree-hit-classification.md`, or is a retired-location, existing-checkout or internal-exception line in `CLAUDE.md` or `.gitignore`. Every remaining Search B line is in a file classified "internal temporary checkout", and `scripts/eval_runner.py` no longer creates a checkout outside a temporary directory.
- `git diff --stat` shows no change to `POST-REFLECT-TASK.md`, `docs/swarm/runbook.md`, or any internal-checkout file other than `scripts/eval_runner.py` and `src/superclaude/skills/sc-post-release-protocol/SKILL.md`.
- `.dev/tasks/` is staged (`git add .dev/tasks`), and `git diff --cached --name-only` lists no `.claude/` path other than `.claude/settings.json`.
