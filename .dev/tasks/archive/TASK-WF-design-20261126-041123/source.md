# Design: release path from `integration` to `master` (issue 826)

Grounding: index_state: fresh, checked_at 2026-11-26T04:07:34Z (`codegraph_status`, `codegraph_node` with `symbolsOnly:true` on `tests/docs/test_branch_protection_rulesets.py`). The files that change are Markdown, JSON and new tests, so every other fact below comes from Read, Grep and read-only `gh` and `git` calls made on 2026-11-26.

Input: `.dev/brainstorms/826-release-path/merged-requirements.md` (convergence 1.00; 15 functional requirements FR-1 to FR-15, five open points). Type: component. Format: spec. This document turns the requirements into exact edits, resolves the open points and fixes the delivery order. It writes no implementation.

## 1. Scope

Documentation and skill text plus two new tests. No Python under `src/superclaude/cli/`, no ruleset or workflow edit, no release script, no new `/sc:post-release` flag, no edit to `src/superclaude/commands/post-release.md` (it has no branch text) and no plugin mirror (verified: `plugins/superclaude/` has no copy of `post-release`, `impact` or `auggie-review`).

## 2. Open points of the requirements, resolved

| # | Open point | Resolution (evidence) |
|---|---|---|
| 1 | Which of G1-G9 read files and which read GitHub state | See the table in 3.1. G3 to G7 read the checkout (`grep`, `uv run superclaude --version`, `make`, `uv build`, `./update.sh`: `release-procedure.md:73-77`; `update.sh` installs the checked-out tree). G2 and G9 read GitHub state. G1 reads `git remote -v`. G8 is the owner's choice and defaults to before the merge. The FR-3 tree check carries the pre-merge results to `<merge-sha>`. |
| 2 | Merge permission and merge setting | Read-only call on 2026-11-26: `gh api repos/IronbellyOrg/IronClaude --jq '{merge: .allow_merge_commit, squash: .allow_squash_merge, rebase: .allow_rebase_merge, auto: .allow_auto_merge}'` printed `merge true, squash true, rebase true, auto false`. Merge commits are allowed, and squash and rebase are allowed too, so the parent check of FR-3 is a real guard, not a formality. The procedure reads the same call before merging. `gh repo view` is not used: it names the repository positionally. The fork-safety test accepts `--repo IronbellyOrg/IronClaude` or a `gh api repos/IronbellyOrg/IronClaude...` path (the form `CLAUDE.md` allows). |
| 3 | Do the rulesets require CI, so the merge-back PR "can merge at once"? | `gh api repos/IronbellyOrg/IronClaude/rules/branches/master` and `.../integration` both print `deletion, non_fast_forward, pull_request`: no required status check today. The procedure does not depend on that: Step 5 says to wait for any check the merge-back PR shows (`gh pr checks <m> --repo IronbellyOrg/IronClaude --watch`) and the rehearsal records what `gh pr checks` prints and returns for a PR with no checks (not verified here). |
| 4 | Poll command and bound for G2 | The G2 command of 3.1 is repeated by hand. Once a run id shows, `gh run watch <databaseId> --repo IronbellyOrg/IronClaude --exit-status` waits for it (`--exit-status` verified in `gh run watch --help`). The bound is 30 minutes (the owner can change it in the procedure text). |
| 5 | `docs/user-guide/commands.md:1335` | Changed to `origin/integration`: `--base` of `superclaude reflect run` is "Explicit audit base ref" chosen by the user (`src/superclaude/cli/reflect/commands.py:307-315`), so the example value is documentation only. Lines 284 and `codegraph.md:92` are the `/sc:impact --diff origin/master --tests` examples. FR-13's acceptance check therefore has no exception. |

## 3. Components

### 3.1 `docs/developer-guide/release-procedure.md` (FR-1 to FR-8)

Heading rules: the `#` title, "What a release is here", Step 1, Step 2 ("Open the release PR"), Step 3 ("Run the go/no-go gate (G1-G9)"), Step 4 ("Tag and publish") and "Sources" keep their text, so the existing anchors keep working (no other file links to a Step anchor: grep over `*.md`, `*.py`, `*.yaml`, `*.json` outside `.dev/` found only the page's own Contents). The old Step 5 becomes Step 6, "Post-release follow-through"; a new Step 5, "Merge master back into integration", goes between them. Contents list: seven numbered links plus Sources, updated. Every `gh` command stays on one line.

**Top of page (line 3, line 22, line 23).** Line 3 keeps its CI-trigger sentence. Line 22 becomes: "An unpinned `pipx install git+https://github.com/IronbellyOrg/IronClaude` follows the default branch (`integration`); a tagged install uses `@vX.Y.Z`. A release is a version number, ... followed by `/sc:post-release`." (the sentence "Every merge to `master` therefore reaches anyone who installs or upgrades." is removed). Line 23 gains the rule: "Ordinary PRs target `integration`. A person promotes a batch with a release PR from `integration` to `master`, merged as a merge commit; the annotated tag goes on that merge commit; `master` is then merged back into `integration` by pull request." The `--repo` sentence of line 24 stays.

**Step 2: Open the release PR.** Intro: "Two PRs. A release-prep PR into `integration` carries the version bump, the changelog cut and the release notes. A release PR from `integration` to `master` carries nothing new." Items:

0. Precondition (new, before item 1):

   ```bash
   git fetch origin master integration --tags
   git merge-base --is-ancestor origin/master origin/integration
   ```

   It must exit 0. If it exits 1, the previous release was not merged back: do Step 5 first with this check as its proof (today it exits 1: pull request 854 left `master` one merge commit ahead).
1. to 4. Version, Changelog cut, Release notes, Retire data: unchanged, except that "Set the version" and the other items are done on a branch cut from `origin/integration`.
5. Open the release-prep PR: `/sc:pr-submit --monitor 3 --head <branch> --base integration --title "chore(release): prepare X.Y.Z"`. Fallback: `gh pr create --repo IronbellyOrg/IronClaude --base integration --head <branch> --title "chore(release): prepare X.Y.Z" --body-file <body-file>`. Anything that merges before the release PR is opened rides along; anything later goes under the next `## [Unreleased]` (sentence kept).
6. Open the release PR after the release-prep PR has merged:

   ```bash
   git fetch origin master integration --tags
   gh pr create --repo IronbellyOrg/IronClaude --base master --head integration --title "chore(release): X.Y.Z" --body-file <body-file>
   gh pr view <n> --repo IronbellyOrg/IronClaude --json headRefOid --jq .headRefOid
   git rev-parse origin/master
   gh pr checks <n> --repo IronbellyOrg/IronClaude --watch
   ```

   The two recorded values are `<reviewed-head-sha>` and `<master-tip>`. If `integration` moves, record both again and repeat from the `gh pr checks` line. A freeze notice on `integration` helps; the pin in item 8 is the guard. Do not use `/sc:pr-submit --monitor 3` for this PR: its fix loop pushes "to the PR head branch only, never the default or a protected branch" (`src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:192-195`), and `integration` is both.
7. Run the Step 3 rows marked "before merge" on a detached checkout of the reviewed head, in a clean checkout (not a new worktree):

   ```bash
   git switch --detach <reviewed-head-sha>
   make sync-dev
   ```

   `make sync-dev` is required before G5: a fresh checkout has no `.claude/` copies, and `make verify-sync` reports them missing (`Makefile:166`; CI runs `sync-dev` first).
8. Read the merge setting, then merge:

   ```bash
   gh api repos/IronbellyOrg/IronClaude --jq '{merge: .allow_merge_commit, squash: .allow_squash_merge, rebase: .allow_rebase_merge, auto: .allow_auto_merge}'
   gh pr merge <n> --repo IronbellyOrg/IronClaude --merge --match-head-commit <reviewed-head-sha>
   ```

   `merge` must be `true`; otherwise stop. Never use `--squash`, `--rebase`, `--delete-branch`, `--admin` or `--auto`. A blocked merge is a stop, not a bypass.

**Step 3: Run the go/no-go gate (G1-G9).** Intro rewritten: "Every check must pass. Any failure is a no-go: stop and take the result back to the release owner. Do not tag, and do not work around a failed check (decisions 7.7 and T1). Rows marked 'before merge' ran in Step 2, item 7, on the reviewed head. The rest run on the merge commit after the merge." First, the capture block (new, before the table):

```bash
gh pr view <n> --repo IronbellyOrg/IronClaude --json state,baseRefName,headRefName,headRefOid,mergeCommit
git fetch origin master integration --tags
git rev-parse --verify -q <merge-sha>^2
git rev-parse --verify -q <merge-sha>^3
git rev-parse <merge-sha>^1 <merge-sha>^2
git rev-parse <merge-sha>^{tree} <reviewed-head-sha>^{tree}
```

Pass only if: `state` is `MERGED`, `baseRefName` is `master`, `headRefName` is `integration` and `mergeCommit.oid` is not null (that value is `<merge-sha>`); the `^2` line prints a hash and the `^3` line prints nothing and exits 1; `^1` equals `<master-tip>` and `^2` equals `<reviewed-head-sha>`; and the two trees are equal. Any failure: stop before tagging. A squash or rebase merge has no `^2`, and `master` moving after Step 2 breaks the `^1` and tree checks. The table gets a "When" column; G1 to G9 keep their numbers and rows:

| # | When | Command change |
|---|---|---|
| G1 | before merge | none |
| G2 | after merge | `gh run list --repo IronbellyOrg/IronClaude --workflow Tests --event push --branch master --commit <merge-sha> --json databaseId,status,conclusion` (replaces `--branch master --limit 3 --json headSha,conclusion,workflowName`). Pass condition: the push run for `<merge-sha>` completed with conclusion `success`. No run yet, or `status` not `completed`: wait (repeat by hand, or `gh run watch <databaseId> --repo IronbellyOrg/IronClaude --exit-status`) for at most 30 minutes, then stop without tagging. A completed run that is not `success`, or no run by the deadline, is no-go. Missing, other-SHA or `workflow_dispatch` evidence is never a pass. The newest attempt decides; two push runs for the same attempt: ask the owner. The `test-summary` sentence stays. |
| G3, G4, G5, G6, G7 | before merge | none. G5 and G7 note: run after `make sync-dev` on the detached checkout. |
| G8 | before merge unless the owner names a check that needs the merge commit or GitHub state | none |
| G9 | after merge | none: the release PR has merged and is no longer listed |

**Step 4: Tag and publish.** The first sentence stays ("never a later `master` commit"). The block becomes:

```bash
git tag --list vX.Y.Z
git ls-remote --tags origin vX.Y.Z
git tag -a vX.Y.Z <merge-sha> -m "Release vX.Y.Z - <short description>" && git push origin vX.Y.Z
git ls-remote origin 'refs/tags/vX.Y.Z^{}'
git rev-parse vX.Y.Z^{commit}
gh release create vX.Y.Z --verify-tag --repo IronbellyOrg/IronClaude --title "vX.Y.Z - <short description>" --notes-file docs/releases/vX.Y.Z.md
```

The first two commands must print nothing (the tag must not exist, locally or on `origin`). The last two before `gh release create` must print `<merge-sha>`; the `ls-remote` pattern must name `^{}` (verified: `git ls-remote origin 'refs/tags/v6.1.0^{}'` prints the peeled commit, `git ls-remote --tags origin v6.1.0` prints only the tag object). Run the lines one at a time and stop at the first failure. Why `--verify-tag`: without it, a failed push lets `gh release create` build a lightweight tag "from the latest state of the default branch" (`gh release create --help`), which is now `integration`, and the `v*` tag ruleset then makes it permanent. Never suggest a force push, a tag move or a tag deletion. The check block (`git cat-file -t`, `gh release view`) and "Never push the tag to the `upstream` remote" stay.

**Step 5: Merge master back into integration (new).**

```bash
git fetch origin master integration --tags
git merge-base --is-ancestor <merge-sha> origin/integration
gh pr create --repo IronbellyOrg/IronClaude --base integration --head master --title "chore(release): merge master into integration after X.Y.Z" --body-file <body-file>
gh pr merge <m> --repo IronbellyOrg/IronClaude --merge
```

If the first `is-ancestor` already exits 0, record "already merged back" and skip the last two lines. Otherwise run all four lines, then fetch again and check that the proof exits 0. The merge-back PR should change 0 files. If it changes any file or conflicts, stop and take it to the release owner: a content-carrying sync goes through a branch cut from `origin/integration` that merges `origin/master`, then an ordinary `/sc:pr-submit` PR, as pull request 846 did (this route is outside this procedure). Wait for any check the PR shows (`gh pr checks <m> --repo IronbellyOrg/IronClaude --watch`). The same ancestry fact, `git merge-base --is-ancestor origin/master origin/integration`, is the precondition of the next release (Step 2, item 0).

**Step 6: Post-release follow-through (old Step 5).**

```bash
git fetch origin
git switch -c post-release-vX.Y.Z origin/integration
```

then `/sc:post-release vX.Y.Z` from that branch, with no new flag. Why: a branch cut before the release-prep PR merged carries the old version metadata, and `SKILL.md:74` then raises a false release-integrity finding. The rest of the section stays; "Then start the next cycle" stays. "Sources" gets one row: "Branch rules, tag rules and merge method | `docs/developer-guide/branch-protection.md`, `.github/rulesets/`". It cites no file under `.dev/brainstorms/` or `.dev/issues/` (untracked folders).

### 3.2 `src/superclaude/skills/sc-post-release-protocol/SKILL.md` (FR-9)

Edits (lines checked on 2026-11-26):

- Line 91, the paragraph that starts `**Anchor the scan to the tagged commit.**`: keep everything up to and including "...removed with `git worktree remove` after the scan." and replace the rest of the paragraph (from "Confirm the tag actually belongs...") with:

  > Confirm the tag actually belongs to the release lineage. Resolve the default branch `<default-branch>` live with `git ls-remote --symref origin HEAD` (the `ref: refs/heads/<name>` line gives `<name>`); only when that call cannot reach the remote, fall back to `git symbolic-ref refs/remotes/origin/HEAD`, which can be stale. Record the value and which source gave it. Then run `git fetch origin <default-branch> --tags` and `git merge-base --is-ancestor <tag> refs/remotes/origin/<default-branch>`; never compare against a bare local branch name, which can be far behind its remote. If the fetch fails or the value came from the fallback, report the ancestry check as **unverified**, never as passed. If the tag is **not** an ancestor of the mainline, or the tree's version metadata disagrees with the tag, treat that as a release-integrity finding and report it before proceeding; with the finding, list the remote branches that contain the tag (`git branch -r --contains <tag>`, without the `origin/HEAD ->` alias line, at most 10, say when the list is cut off; when none: "no remote branch contains `<tag>`") and say that the release branch may not yet have been merged back into the default branch and should be merged back by pull request. Never hard-code a branch name.

  The paragraph then contains none of the words `main`, `master` or `integration` (the word "mainline" is allowed: the test uses whole-word matching).
- Line 74 (WARN, "then continue, anchored to the tag"): unchanged.
- Line 103 (`**Output:** resolved tag + auto-detected default branch + ...`): "auto-detected default branch" becomes "default branch (resolved live, with its source)".
- Line 105 (`**Exit criteria:** tag anchored, default branch auto-detected, ...`): "default branch auto-detected" becomes "default branch resolved and its source recorded".
- Guardrails, lines 347-348: "work on a feature branch off the repo's **auto-detected default branch**" becomes "off the default branch resolved in Wave 1"; "with `--base <default-branch>`" gets "(the Wave 1 value; a value that came from the offline fallback is never used as a PR base: ask the user)".
- No change to `argument-hint` (line 5) and none to the command file.

### 3.3 `tests/docs/test_release_procedure.py` (FR-10)

Pattern: `tests/docs/test_branch_protection_rulesets.py` (module constants, `Path.read_text(encoding="utf-8")`, `pytest.mark.parametrize`).

Interface:

- `_REPO`, `_PAGE = _REPO / "docs/developer-guide/release-procedure.md"`, `_TEXT` (read once).
- `_fenced_lines() -> list[str]`: the stripped lines inside ``` fences.
- `_REQUIRED_COMMANDS: tuple[str, ...]` with one entry per command of 3.1 (precondition `git merge-base --is-ancestor origin/master origin/integration`; `--base integration --head <branch>`; `/sc:pr-submit --monitor 3 --head <branch> --base integration`; `gh pr create --repo IronbellyOrg/IronClaude --base master --head integration`; `gh pr checks <n> --repo IronbellyOrg/IronClaude --watch`; `git switch --detach <reviewed-head-sha>`; `make sync-dev`; `gh pr merge <n> --repo IronbellyOrg/IronClaude --merge --match-head-commit <reviewed-head-sha>`; `--json state,baseRefName,headRefName,headRefOid,mergeCommit`; `git rev-parse --verify -q <merge-sha>^2`; `git rev-parse --verify -q <merge-sha>^3`; `git rev-parse <merge-sha>^{tree} <reviewed-head-sha>^{tree}`; the G2 command; `git ls-remote --tags origin vX.Y.Z`; `git ls-remote origin 'refs/tags/vX.Y.Z^{}'`; `git rev-parse vX.Y.Z^{commit}`; `--verify-tag`; `gh pr create --repo IronbellyOrg/IronClaude --base integration --head master`; `gh pr merge <m> --repo IronbellyOrg/IronClaude --merge`; `git merge-base --is-ancestor <merge-sha> origin/integration`; `git switch -c post-release-vX.Y.Z origin/integration`; `/sc:post-release vX.Y.Z`). One parametrized test asserts each is a substring of `_TEXT`; a future step adds a row.
- `test_every_gh_line_names_the_fork`: each fenced line that starts with `gh ` contains `--repo IronbellyOrg/IronClaude` or starts with `gh api repos/IronbellyOrg/IronClaude`.
- `test_banned_merge_options`: none of `--admin`, `--auto`, `--squash`, `--rebase`, `--delete-branch` appears in a fenced line; outside fences a line that contains one also contains `never` (case-insensitive).
- `test_removed_text_is_gone`: `--base master --head <branch>`, `--limit 3` and `Every merge to \`master\` therefore reaches` are absent.
- `test_contents_links_resolve`: every `](#anchor)` in the Contents list equals the GitHub slug of one H2 heading (slug: lowercase, drop characters other than word characters, spaces and hyphens, spaces to hyphens), and the H2 order is: What a release is here, Step 1 to Step 6, Sources.

Acceptance: `uv run pytest tests/docs/test_release_procedure.py -v` passes. Each assertion was seen failing once, by hand, with its edit removed (one mutation per row group; recorded in the plan's `progress.md`).

### 3.4 `tests/skills/test_post_release_base_branch.py` (FR-9, FR-10)

Reads `src/superclaude/skills/sc-post-release-protocol/SKILL.md` (pattern: `tests/skills/test_primitive_dual_surface_lookup.py`, constant `_SKILLS`).

- `_paragraph()`: the line that starts with `**Anchor the scan to the tagged commit.**`.
- Asserts the paragraph contains `git ls-remote --symref origin HEAD`, `git fetch origin <default-branch> --tags`, `git merge-base --is-ancestor <tag> refs/remotes/origin/<default-branch>`, `unverified` and `git branch -r --contains <tag>`.
- Asserts the whole file does not contain `git merge-base --is-ancestor <tag> <default-branch>`.
- Asserts `re.search(r"\b(main|master|integration)\b", paragraph)` is `None`.
- Asserts the line 74 WARN text still ends in "then continue, anchored to the tag", and that the Guardrails block names the offline fallback and "ask the user".
- Asserts `src/superclaude/commands/post-release.md` has no `--base` (the design adds no flag).

No temporary-history fixture: it would test git, not the skill text. Text tests guard wording; the rehearsal is the behaviour proof.

### 3.5 `CLAUDE.md`, `CONTRIBUTING.md`, examples (FR-11 to FR-13)

- `CLAUDE.md:297`: step 4 becomes "4. Merge to `integration` → validate. Release: a person opens a PR from `integration` to `master`, merges it as a merge commit, tags that commit, then merges `master` back into `integration` by PR (exact commands: `docs/developer-guide/release-procedure.md`)". Lines 290 and 292-296 stay.
- `CONTRIBUTING.md`: lines 9, 18, 22, 23, 24, 26, 81 and 83 say `integration` where they mean the branch ordinary work is cut from; line 66 becomes `--base integration`; line 73 stays. Line 26 ("run the same check locally on master in a separate worktree") becomes "...on `integration` in a second, clean checkout (not the one that holds your PR branch)". The fenced block at lines 28-35 is replaced by:

  ```bash
  git fetch origin integration
  git switch --detach origin/integration
  <run check>
  ```

  so the retired `.dev/worktrees/` location is gone. One new line after line 73: "Release PRs are the one exception: a maintainer promotes `integration` to `master` as described in [Release Procedure](docs/developer-guide/release-procedure.md)." The implementer re-checks the list with `grep -n master CONTRIBUTING.md` and edits every hit that is not line 73.
- Examples: `origin/master` becomes `origin/integration` in `src/superclaude/commands/impact.md:23`, `src/superclaude/commands/auggie-review.md:37,113`, `src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json:19-20`, `docs/user-guide/codegraph.md:92`, `docs/user-guide/commands.md:284` and `docs/user-guide/commands.md:1335`. `CHANGELOG.md` and `docs/testing/...` are historical and stay. Acceptance: `grep -rn "origin/master" src/superclaude docs/user-guide` prints nothing.
- Order of edits: `src/superclaude/` first, then `make sync-dev` and `make verify-sync`; never stage `.claude/`.

### 3.6 Rehearsal (FR-15)

Two parts, because only the first needs no outward action.

1. **Local git rehearsal (the agent runs it).** In a temporary directory: a bare repository as `origin` whose `HEAD` points to `refs/heads/integration`, branches `integration` and `master`, and a clone. Reproduce the release as written, with `git merge --no-ff` standing in for the GitHub merge (it produces the same two-parent shape; it does not prove `gh pr merge`): the Step 2 precondition (exit 1 before the merge-back, 0 after); the FR-3 captures (a fast-forward-free merge passes; a squash-shaped commit has no `^2`; `master` moving breaks `^1`); the Step 4 tag with a tag name that does not start with `v` (for example `rehearsal-0.0.0`), including `git ls-remote origin 'refs/tags/<tag>^{}'` and `git rev-parse <tag>^{commit}`; the Step 5 proof and the "already merged back" skip; the Wave 1 check of the skill (`git ls-remote --symref origin HEAD`, a stale local `integration` that gives exit 1 against the bare name and exit 0 against `refs/remotes/origin/integration`, and `refs/remotes/origin/HEAD` pointing at `master`, which must be reported "unverified"). The log (commands, outputs, exit codes, each check marked passed or not exercised) goes to `.dev/issues/826/rehearsal-local.md` (never staged).
2. **GitHub rehearsal (needs the owner's go).** A scratch repository on GitHub with `integration` as its default and a `master` branch, run with the written commands: the only substitutions are the repository name and a tag that does not start with `v`. Write the substituted commands to a file; `grep -n 'IronbellyOrg/IronClaude' <file>` must print nothing and `git remote -v` must name the scratch repository before any push (a `gh --repo` never reads the git remote). It shows `gh pr merge --match-head-commit`, `gh pr view` fields, `gh run list --commit`, `gh release create --verify-tag` rejecting a tag that is not on the remote, and what `gh pr checks --watch` does with no checks. G5-G8 are recorded as not exercised. Creating a repository on GitHub is an outward action: the implementer does not do it without the owner's explicit approval in that session. Without it the item is reported as not exercised, with the commands ready, and the issue's rehearsal criterion is reported as partly met.

Evidence of part 1 (and part 2 when it runs) is posted with `gh issue comment 826 --repo IronbellyOrg/IronClaude --body-file .dev/issues/826/rehearsal-local.md`.

## 4. Delivery

One pull request (the story's), with commits in this order so each can be reverted alone: (1) `release-procedure.md`, `CLAUDE.md`, `CONTRIBUTING.md` and `tests/docs/test_release_procedure.py`; (2) skill text and `tests/skills/test_post_release_base_branch.py`; (3) example commands. `make sync-dev` and `make verify-sync` run after (2) and (3). Commit type: `docs(release)` for (1) and (3), `fix(post-release)` for (2).

## 5. Validation of this design against the repository

- Paths and lines read on 2026-11-26: `release-procedure.md` lines 3, 9-17, 22-24, 38-63, 65-79, 87-118; `SKILL.md` lines 74, 91, 103, 105, 304, 347-348; `CLAUDE.md` lines 288-297; `CONTRIBUTING.md` lines 9, 18, 22-35, 66, 73, 81, 83; `tests/docs/test_branch_protection_rulesets.py` in full; `src/superclaude/cli/reflect/commands.py:307-315`.
- Commands checked with `--help` or a read-only call: `gh pr merge --match-head-commit`, `gh run list --commit --workflow --event --branch`, `gh pr checks --watch`, `gh run watch --exit-status`, `gh release create --verify-tag`, `git ls-remote --symref origin HEAD`, `git ls-remote origin 'refs/tags/v6.1.0^{}'`, `git rev-list --parents`.
- Consumers: no test reads `release-procedure.md` today; `tests/skills/test_worker_contract.py:2371-2384` lists the post-release `SKILL.md` path only in a conversion note and pins no text of Wave 1; `tests/unit/test_cli_install.py` pins the file list of the skill, which does not change.

## 6. Risks that stay

- The GitHub-side rehearsal may not run in this session (needs approval); then the issue's fifth acceptance point is partly met and the pull request says so (`Refs #826`).
- `gh pr checks --watch` with no checks, and the behaviour of `gh pr merge --match-head-commit` when the head has moved, are verified only by the GitHub rehearsal.
- Text tests guard wording, not behaviour. A reviewer reads the procedure once against the rehearsal log.
