---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-refactorIronClau-20261102-162730
version: "1"
priority: Medium
created_date: "2026-11-02"
---

# Move IronClaude to Orca's default worktree paths and forbid all SuperClaude upstream interaction

Source: ./source.md
Goal: No tracked file outside `.dev/` tells anyone to create a project worktree under `.dev/worktrees/` or with raw `git worktree add`. Project worktrees are created by Orca at its default location, outside the main checkout. Internal temporary checkouts made by a CLI or a test keep working without Orca. The CLAUDE.md fork rule forbids any push to, or other interaction with, `SuperClaude-Org/SuperClaude_Framework`, with no exceptions.

## Constraints

- The hit set is the output of `git grep -n -E '\.dev/worktrees|git worktree add' -- ':!.dev'`. On 2026-11-02 it was 108 matching lines in 17 files. Do not edit anything under `.dev/` except this package's `./artifacts/`.
- `src/superclaude/` is the source of truth. `.claude/` is the generated mirror refreshed by `make sync-dev`. Never stage any `.claude/` path except `.claude/settings.json`, and never run `git add -f` on a `.claude/` path.
- `plugins/superclaude/commands/recommend.md`, `plugins/superclaude/skills/sc-recommend/SKILL.md` and `plugins/superclaude/skills/sc-recommend/refs/surface-enumeration.md` were byte-identical to their `src/superclaude/` originals on 2026-11-02 (checked with `cmp`). `tests/commands/test_routing_plugin_parity.py` requires the plugin sc-recommend skill to be a byte copy of src. Keep all three byte-identical.
- Installed primitives (`src/superclaude/{commands,skills}`) must not gain a host path such as `/home/coder/...`, an Orca-specific absolute path, or a `src/superclaude/...` path. Describe Orca's location generically: Orca's default worktree location, outside the main checkout; the real path is shown by `orca worktree current --json` or `orca worktree list`.
- Orca commands this plan may name were confirmed in `orca worktree --help` and `orca worktree create --help` on 2026-11-02: `orca worktree create --name <name> [--repo <selector>] [--base-branch <ref>] [--parent-worktree <selector>|--no-parent]`, `orca worktree list`, `orca worktree current`, `orca worktree rm`. Do not name other Orca subcommands or flags without checking their `--help` first.
- Internal temporary checkouts, classified in Task 1, stay unchanged and must keep working without Orca.
- `POST-REFLECT-TASK.md` is a historical task record and stays byte-unchanged (see Task 1).
- Make no GitHub, git-remote or Orca call that reaches `SuperClaude-Org/SuperClaude_Framework` while executing this plan.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), including this package and its `./artifacts/`. Staging is not committing: commit only when the user asks.

## Phase 1: Classify every hit

## Task 1: Write the hit classification inventory

Run `git grep -n -E '\.dev/worktrees|git worktree add' -- ':!.dev'` and `git grep -c -E '\.dev/worktrees|git worktree add' -- ':!.dev'`. Write `./artifacts/worktree-hit-classification.md`, a table with one row per file giving the hit count, the class, the action, and a one-line reason. Use exactly these classes and assignments:

- Project worktree, rewrite to Orca's default location: `CLAUDE.md` (8 hits, subsection `### Parallel Development with Git Worktrees`); `.gitignore` (2 hits, the worktree comment and the `.dev/worktrees/` entry); `src/superclaude/commands/recommend.md` (1 hit, `## Output Constraints`); `plugins/superclaude/commands/recommend.md` (1, mirror); `src/superclaude/skills/sc-recommend/SKILL.md` (2 hits, the paragraph beginning "The checkout paths (row 7)" and the "worktree-aware paths" bullet); `plugins/superclaude/skills/sc-recommend/SKILL.md` (2, mirror); `src/superclaude/skills/sc-recommend/refs/surface-enumeration.md` (1 hit, the sentence beginning "The current worktree is the repository root"); `plugins/superclaude/skills/sc-recommend/refs/surface-enumeration.md` (1, mirror); `tests/docs/test_tavily_doc_alignment.py` (1 hit, the comment in `_iter_text_files` that says the worktree lives under `.dev/worktrees/`).
- Internal temporary checkout, keep unchanged and working without Orca: `src/superclaude/cli/reflect/config.py` (1, docstring of the reflect `--isolate-reviewers` snapshot at `<output>/_review-snapshot`, removed with `git worktree remove --force`); `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (2, Step 0.5e describing that same snapshot); `src/superclaude/skills/sc-post-release-protocol/SKILL.md` (1, a read-only checkout of a release tag in "Anchor the scan to the tagged commit"); `tests/cli/reflect/test_isolate_reviewers_cli.py` (2, docstrings about that snapshot); `tests/skills/test_implement_retry_revert.py` (2, `test_revert_targets_ledger_worktree_only` and `test_restored_parent_symlink_contained_in_linked_worktree` build a fixture repo inside pytest `tmp_path`); `tests/troubleshoot/backtest/git_replay.py` (1, replay checkout docstring); `tests/troubleshoot/backtest/test_git_replay_integration.py` (1, docstring of `test_backtest_replay_leaves_no_leaked_worktree`).
- Historical record, keep unchanged: `POST-REFLECT-TASK.md` (79 hits). It is an MDTM task file dated 2026-06-22 whose paths `/config/workspace/IronClaude/.dev/worktrees/reflect-reviewer-guard` record where that past run executed. The `reflect-reviewer` agent it built exists at `src/superclaude/agents/reflect-reviewer.md`, and the file was last changed by commit 08b1a5f8 "feat(reflect): harden reviewer isolation (#203)". Rewriting its paths would falsify the record.

If the live output differs from 108 lines in 17 files, add a row for each new hit, classify it with the same three classes and a reason, and note the difference at the top of the inventory.

Acceptance criteria:
- `./artifacts/worktree-hit-classification.md` exists, has one row for every file in the live `git grep -c` output, and its per-file counts sum to the live total.
- Every row has exactly one of the three classes and a non-empty action and reason.
- The raw `git grep -n` output is saved to `./artifacts/t1-hits-before.txt`.

## Phase 2: Rewrite the repository rules

## Task 2: Replace the worktree rule in CLAUDE.md with the Orca rule

Depends on: Task 1

In `CLAUDE.md`, rewrite the subsection `### Parallel Development with Git Worktrees` (under `## 🌿 Git Workflow`). Its current text has an "ABSOLUTE RULE — worktree location is `./.dev/worktrees/`" paragraph, a bash block using `git worktree add .dev/worktrees/...`, a Usage list naming `<repo>/.dev/worktrees/...`, and a Cleanup block using `git worktree remove .dev/worktrees/integration`. The new subsection must:

- State the absolute rule that every project worktree is created through Orca with `orca worktree create --name <name>` (with `--repo <selector>`, `--base-branch <ref>`, and `--parent-worktree <selector>` or `--no-parent` as needed) and lives at Orca's default worktree location, outside the main checkout. Name `orca worktree current --json` and `orca worktree list` as the way to see the real path.
- Forbid creating project worktrees with raw `git worktree add`, under the retired `.dev/worktrees/` location, or under `.claude/worktrees/`. Keep the existing ban on the `EnterWorktree` tool and its reason: it hardcodes `.claude/worktrees/`, which is gitignored sync-dev territory.
- Forbid Orca GitHub link flags (`--issue`, `--pr`) for this repo and point to the fork rule edited in Task 3.
- State the exception: internal temporary checkouts that a CLI or test creates and removes itself keep using `git worktree add` directly and must work without Orca. Name the four cases from Task 1: the reflect `--isolate-reviewers` snapshot, the troubleshoot backtest replay, test fixtures in a pytest temp directory, and the read-only release-tag checkout in `/sc:post-release`.
- Rewrite Usage so session A opens the main checkout and sessions B and C open Orca-created worktrees. Rewrite Cleanup to use `orca worktree rm` (check `orca worktree rm --help` for its selector syntax before writing the example).
- Remove the instruction to add `.dev/worktrees/` to `.gitignore`.
- Contain no host absolute path such as `/home/coder/...`.

Acceptance criteria:
- `git grep -n -E '\.dev/worktrees|git worktree add' -- CLAUDE.md` prints only lines that forbid the retired location or describe the internal-checkout exception. No line tells the reader to create a project worktree under `.dev/worktrees/` or with raw `git worktree add`. The output is saved to `./artifacts/t2-claude-md-grep.txt`.
- The subsection names `orca worktree create`, `orca worktree list` or `orca worktree current`, and `orca worktree rm`, and still forbids `EnterWorktree`.
- `grep -n '/home/coder' CLAUDE.md` prints nothing.

## Task 3: Tighten the fork rule so SuperClaude upstream is never touched

Depends on: Task 2

In `CLAUDE.md`, edit the section `## ABSOLUTE RULE: PR Target = Fork (`IronbellyOrg/IronClaude`), NEVER Upstream`. Keep the heading text unchanged so existing references keep working. Change the body so that:

- It opens with an unconditional rule: SuperClaude upstream (`SuperClaude-Org/SuperClaude_Framework`, the `upstream` remote) is never pushed to or interacted with. That means no push, fetch or pull from the `upstream` remote; no PR, issue, comment, review or reaction there; and no tool call or link (gh, git or Orca) that resolves to it.
- The bullet "Open PRs against `SuperClaude-Org/SuperClaude_Framework` without explicit user authorization in the same session" becomes an unconditional prohibition with no authorization clause.
- Every `gh` call that accepts `--repo` passes `--repo IronbellyOrg/IronClaude`, not only `gh pr create`.
- A new bullet records that Orca currently identifies this project as `github:superclaude-org/superclaude_framework` (seen in `orca worktree current --json` on 2026-11-02). Until `orca worktree current --json` shows the fork's project id, never pass `--issue`, `--pr` or other GitHub link flags to Orca commands for this repo.
- The `**Exceptions:**` paragraph that allows contributing back to upstream with authorization is replaced by a statement that there are no exceptions.
- The mandatory `/sc:pr-submit --monitor 3` instruction, the fallback `gh pr create --repo IronbellyOrg/IronClaude ...` block, the pre-PR checks and the Rationale paragraph stay. Edit them only where they contradict the rules above.

Acceptance criteria:
- `grep -n -i 'contributing back' CLAUDE.md` prints nothing, and the section contains no clause that permits upstream interaction with user authorization.
- The section explicitly forbids push, fetch or pull from `upstream`, PRs, issues, comments, and Orca `--issue`/`--pr` linking to the upstream repository, and requires `--repo IronbellyOrg/IronClaude` on every `gh` call that accepts it.
- The heading line `## ABSOLUTE RULE: PR Target = Fork (`IronbellyOrg/IronClaude`), NEVER Upstream` is unchanged (`git diff CLAUDE.md` shows no change to it).

## Task 4: Mark .dev/worktrees as retired in .gitignore

Depends on: Task 1

In `.gitignore`, replace the two comment lines above the `.dev/worktrees/` entry. Today they say the canonical location is `.dev/worktrees/<name>/`. The new comment says this location is retired, that Orca creates project worktrees at its default location outside the repository, and that the entry stays so a leftover checkout here is never staged. Keep the `.dev/worktrees/` entry itself.

Acceptance criteria:
- No `.gitignore` line calls `.dev/worktrees/` canonical. The comment says it is retired and that Orca creates project worktrees outside the repository.
- `git check-ignore -q .dev/worktrees/example` exits 0.

## Phase 3: Update the installed primitives and their mirrors

## Task 5: Make the sc-recommend surfaces location-neutral

Depends on: Task 1

Edit these three source-of-truth files so they no longer assume worktrees live under `.dev/worktrees/<name>/`. Keep each sentence's meaning: paths resolve against the worktree that `git rev-parse --show-toplevel` returns.

- `src/superclaude/commands/recommend.md`, `## Output Constraints`, the bullet "Paths are absolute or repo-relative and worktree-aware. When cwd is `.dev/worktrees/<name>/` ...": say "When cwd is inside a linked git worktree (for example one Orca created at its default location outside the main checkout), paths resolve against that worktree, not the main checkout."
- `src/superclaude/skills/sc-recommend/SKILL.md`, the paragraph beginning "The checkout paths (row 7) resolve under the repository root": replace "If the user's cwd is a worktree under `.dev/worktrees/<name>/`" with wording about a linked worktree, such as an Orca-created worktree outside the main checkout.
- `src/superclaude/skills/sc-recommend/SKILL.md`, the bullet "worktree-aware paths (resolved under `git rev-parse --show-toplevel`, which is the worktree's root when cwd is inside `.dev/worktrees/<name>/`)": end it with "when cwd is inside a linked worktree".
- `src/superclaude/skills/sc-recommend/refs/surface-enumeration.md`, the sentence "The current worktree is the repository root returned by `git rev-parse --show-toplevel`, including when cwd is under `.dev/worktrees/<name>/`.": end it with "including when cwd is inside a linked worktree (such as an Orca-created one)". Keep "Never redirect lookups to another checkout by assumption."

Acceptance criteria:
- `git grep -n '\.dev/worktrees' -- src/superclaude/commands/recommend.md src/superclaude/skills/sc-recommend` prints nothing.
- No line added in `git diff -- src/superclaude/commands/recommend.md src/superclaude/skills/sc-recommend` contains `/home/` or `src/superclaude/`. The diff is saved to `./artifacts/t5-recommend.diff`.

## Task 6: Mirror the sc-recommend edits to the plugin copy and the dev mirror

Depends on: Task 5

Copy the three files edited in Task 5 byte-for-byte to `plugins/superclaude/commands/recommend.md`, `plugins/superclaude/skills/sc-recommend/SKILL.md` and `plugins/superclaude/skills/sc-recommend/refs/surface-enumeration.md`. Then run `make sync-dev` and `make verify-sync`, and run `uv run pytest tests/commands/test_routing_plugin_parity.py tests/recommend/ -v`.

Acceptance criteria:
- `cmp` reports each `plugins/superclaude/...` file identical to its `src/superclaude/...` original.
- `make verify-sync` exits 0. Its output is saved to `./artifacts/t6-verify-sync.txt`.
- The pytest run passes. Its output is saved to `./artifacts/t6-pytest.txt`.
- `git diff --cached --name-only` lists no `.claude/` path other than `.claude/settings.json`.

## Phase 4: Fix the test comment and confirm the residual hits

## Task 7: Make the tavily test comment location-neutral and record the residual hits

Depends on: Task 2, Task 3, Task 4, Task 6

In `tests/docs/test_tavily_doc_alignment.py`, function `_iter_text_files`, rewrite the comment that says "the worktree itself lives under `.dev/worktrees/…`". It should say that the checkout itself may sit under a directory whose name is in `_EXCLUDE_DIRS` (for example an older checkout under `.dev/`), so testing `p.parts` would exclude every file and make the guard vacuous. Change only the comment, not the code. Then rerun the full hit search and save the residual hits.

Acceptance criteria:
- `uv run pytest tests/docs/test_tavily_doc_alignment.py -v` passes, and `uv run ruff check tests/docs/test_tavily_doc_alignment.py` and `uv run ruff format --check tests/docs/test_tavily_doc_alignment.py` both exit 0.
- `git grep -n -E '\.dev/worktrees|git worktree add' -- ':!.dev'` output is saved to `./artifacts/t7-residual-hits.txt`. Every remaining line is in a file classified "internal temporary checkout" or "historical record" in `./artifacts/worktree-hit-classification.md`, or is a retired-location or internal-exception line in `CLAUDE.md` or `.gitignore`. No project-worktree file other than those two has a remaining hit.
- `git diff --stat` shows no change to `POST-REFLECT-TASK.md` or to any file classified "internal temporary checkout".
- `.dev/tasks/` is staged (`git add .dev/tasks`), and `git diff --cached --name-only` lists no `.claude/` path other than `.claude/settings.json`.
