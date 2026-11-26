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

## Revision 1: findings to fix (regenerate after review)

The first plan generated from sections 1 to 6 above was reviewed by `/sc:reflect --mode pre` (report: `.dev/reflect/pre-TASK-WF-design-20261126-041123-20261126041625/REPORT.md`; that plan package is archived under `.dev/tasks/archive/`) and failed with six Blocking findings. The new plan must fix all six, must not repeat the eight Medium findings, and keeps the old plan's structure (13 tasks in 6 phases) unless a fix says otherwise. Where this section and sections 1 to 6 differ, this section wins, and the plan must say where it overrides the design (the H2 order of `test_contents_links_resolve` in section 3.3, and the log path of section 3.6). In the finding text below, `plan:N` means line N of the first plan (archived); the new plan has its own line numbers, so describe each fix by the text it changes.

### Blocking findings to fix

| id | grade | claim | citations | source findings |
|---|---|---|---|---|
| M-01 | Blocking (Missing) | **Affected action:** closing the rehearsal criterion of issue 826. This is G-1, regraded. **Missing step:** posting the rehearsal evidence with `gh issue comment 826 ...`. No task does it, and FR-15's acceptance criterion is "the comment exists". Task 13 only says which acceptance point is met, so the criterion has no owner task, even as "prepare the command, post only with approval". Constraint line 22 ("none runs a command against a repository other than a temporary local one") would also forbid it, so the fix has to change that constraint too (M-02). Repair: "M-01 and M-02" under Required repair content. | source.md:189; .dev/brainstorms/826-release-path/merged-requirements.md:162-163; plan:22; plan:283-315 (Tasks 12 and 13) | R1-F1, R2-F3, R3-F3, G-1 (debate C-001) |
| M-02 | Blocking (Decision) | **Affected action:** the owner-approved scratch-repository run of Task 13 and the issue comment of M-01. Constraint line 22 flatly forbids creating a repository, pushing, tagging or opening a PR on GitHub. Task 13 and the Goal allow exactly that once the owner approves, and the issue comment is a GitHub write too, so a literal executor refuses both and the approved outcome cannot be reached. Line 22 still allows read-only `gh api` GET calls on `IronbellyOrg/IronClaude`, so the conflict is with its write ban. Its second clause, read literally, also forbids the `git diff` and `git status` checks run against the real repo. Repair: "M-01 and M-02" under Required repair content. | plan:15, 22, 306, 310 | R2-F5, R3-F4 (debate C-008, X-003) |
| M-03 | Blocking (Safety) | **Affected action:** restoring the page after Task 6's mutation check. The plan never commits anything. So when Task 6 runs, the page still holds the uncommitted edits from Tasks 1 to 3, and "byte-identical to its committed state" with `git diff --stat` cannot be true. The obvious way to satisfy it is `git checkout` or `git restore` on the page, which deletes all Task 1 to 3 work. The check also cannot pass as written. Repair: "M-03" under Required repair content. | plan:197; plan:17-23 and a grep of the plan for "commit" find no commit step | R1-F2, R3-F1, G-4 (debate C-002, X-004) |
| M-04 | Blocking (Decision) | **Affected action:** Task 12's acceptance check. Its "`git status --short` shows only the files edited by Tasks 1 to 11" fails in this worktree. `.dev/issues/`, `.dev/brainstorms/`, `.dev/reflect/` and the plan's own folder are untracked but not ignored, so they show in `git status`. The new test files are created, not edited. Nothing in the check proves the rehearsal ran in the temporary clone either: `git status --short` shows an untracked folder as one line and shows no refs, so a wrong-folder `git tag` or `git merge --no-ff` passes, and a rehearsal run from the wrong folder produces answers that look like passes because the real repository already gives them (`refs/remotes/origin/HEAD` is `master`, `origin/master` is not an ancestor of `origin/integration`). The M-01 step would then post that log as evidence. Repair: "M-04" under Required repair content, which also carries the location guard of M-14. | plan:300; .gitignore:83-85,239-263 (no ignore rule for `.dev/issues` or `.dev/brainstorms`); .dev/issues/826/ exists; plan:287, 292 | R3-F2, R3-F7 (location guard); INV-001, INV-013, INV-023 (debate C-007 with C-017) |
| M-05 | Blocking (Decision) | **Affected action:** Task 6's H2-order assertion in `test_contents_links_resolve`. The stated order (What a release is here, Step 1 to Step 6, Sources) leaves out the existing `## Contents` heading, which is an H2 at line 9 of the page and stays. A literal equality assertion fails on the page Tasks 1 to 3 produce. The defect is inherited from the design (`source.md:150`), so the repaired line must say it overrides that line. Grade carried by 2 of 3 advocates; Variant 1 held Medium. Repair: "M-05" under Required repair content. | plan:196; docs/developer-guide/release-procedure.md:9; source.md:150 | R1-F4, R2-F1, R3-F8 (first part) (debate C-005, X-002) |
| M-06 | Blocking (Missing) | **Affected action:** the story's commit step after the plan finishes, which needs the design's delivery contract; UC-1 checks that no source requirement is dropped silently. **Missing:** `source.md:193` fixes three independently revertible commit groups, their order, their commit types (`docs(release)` and `fix(post-release)`) and synchronization after both the skill group and the example group. No task and no Constraint carries them; Task 11 supplies only the final synchronization. Grade carried by 2 of 3 advocates; Variant 1 and the base's G-2 re-check graded it Medium because commits happen outside the plan. Repair: "M-06" under Required repair content. | source.md:193; plan:17-23, 272-281 | R1-F7, R2-F4, G-2 (debate C-009, X-006) |

### Required repair content (wording the new plan must carry)


Repair only the Blocking ids M-01 to M-06, and respect the format rules at the end of this section.

#### M-01 and M-02

- Inside Task 13, after `./artifacts/rehearsal-github.md` exists, add this step and no new task number: write `./artifacts/issue-comment-body.md` holding `./artifacts/rehearsal-local.md` followed by `./artifacts/rehearsal-github.md`. Only with the owner's explicit approval in this session for this posting (approval of a scratch repository is not approval to post), post it once with `gh issue comment 826 --repo IronbellyOrg/IronClaude --body-file ./artifacts/issue-comment-body.md` and record the comment URL in `./artifacts/issue-comment.md`.
- Without that approval `./artifacts/issue-comment.md` starts with `Status: not posted (needs the owner's approval)`, holds the ready command, and the plan states that issue 826's rehearsal criterion stays partly met. Acceptance: that file holds the comment URL or that status line.
- Post nothing until the location proof of M-04 is in the local log.
- Constraint line 22 keeps the ban on creating a repository, pushing, tagging, merging or opening a pull request on GitHub, with two exceptions: the scratch-repository run of Task 13 and the one issue comment, each only with the owner's explicit approval in this session. Read-only `gh api` GET calls and read-only git checks of this repository stay allowed. The scratch approval must name the scratch repository as the owner's exception to the project rule that the fork is the only target (`CLAUDE.md:49`, `CLAUDE.md:52`, `CLAUDE.md:76`); without it Task 13 records "not exercised".

Check: `grep -n 'gh issue comment 826 --repo IronbellyOrg/IronClaude'` finds the step; line 22 no longer contradicts Task 13.

#### M-03

- In Task 6 (and in Task 8 with `t8-` names and the skill file): before the first mutation record the file's `sha256sum` in `./artifacts/t6-page.sha256` and save a copy as `./artifacts/t6-page.pre-mutation`; both are written once and never overwritten on a rerun.
- Mutate the file in place; after each mutation restore it by copying the saved file back.
- At the end: `cmp` of the file against the saved copy exits 0 (and exited 1 after each mutation, which also proves the mutation changed the file), `sha256sum -c` passes, and the tests pass on the restored file.
- Remove the words "committed state" and the environment-variable option. Never use a command that discards uncommitted changes on an edited file (`git checkout`, `git restore`, `git reset --hard`, `git stash`).

Scope: the repair edits the sentence at plan:197 and, for Task 8, only the restore sentence of plan:234 (this also covers M-07); the "each edit" wording of M-08 stays untouched because Medium findings are not repaired.

Check: `grep -n 'committed state'` on the plan prints nothing; the mutation log records the checksum before and after.

#### M-04

- Replace the sentence at plan:300. Before the run, and again before any fix sent back to Task 1, 2, 3 or 7, record into `./artifacts/t12-state-before.txt` the output of `git status --short --untracked-files=all`, `git rev-parse HEAD`, `git symbolic-ref -q refs/remotes/origin/HEAD` and `git tag --list 'rehearsal-*'` for the real repository; after the run record the same into `./artifacts/t12-state-after.txt`.
- Pass only when HEAD, the symbolic ref and the tag list are identical, and the status lines differ only for paths inside this package's folder (its ledger, staging, `./artifacts/`). Do not compare `integration` or `master` ids (other worktrees move them). On an unexplained mismatch stop and report failure or concurrent interference; do not restore shared refs or erase files.
- Every rehearsal git command runs as `git -C <absolute temporary clone>` or inside one shell call that starts with `cd` into the temporary folder; never rely on a previous call's folder or variables. Log `git rev-parse --show-toplevel` with each check and confirm it equals the temporary clone; before any push confirm `git remote get-url origin` prints the temporary bare repository. A missing or mismatched location invalidates the check, and the log must not be posted as evidence.

Scope: the third bullet is also the guard of M-14; M-14 gets no separate repair.

Check: a grep of the plan for `shows only the files edited by Tasks 1 to 11` prints nothing, and Task 12 names `./artifacts/t12-state-before.txt`, `./artifacts/t12-state-after.txt`, `git rev-parse --show-toplevel` and `git remote get-url origin`.

#### M-05

- In Task 6's H2-order assertion say the order is Contents, What a release is here, Step 1 to Step 6, Sources; the `## Contents` heading stays and the Contents list keeps its eight entries. Say the line overrides `source.md:150`.

Check: Task 6's H2-order line starts the order with Contents and names `source.md:150` as overridden; Task 1's "eight entries" acceptance line is unchanged.

#### M-06

- Add one Constraints bullet that says: no task of this plan commits; the delivery order applies to the story's commit step after the plan finishes: three commit groups, (1) `docs/developer-guide/release-procedure.md`, `CLAUDE.md`, `CONTRIBUTING.md` and `tests/docs/test_release_procedure.py`, (2) the skill text and `tests/skills/test_post_release_base_branch.py`, (3) the example commands; commit types `docs(release)` for (1) and (3) and `fix(post-release)` for (2); each group is committed with only its own paths so each can be reverted alone; `make sync-dev` and `make verify-sync` run after (2) and (3) (Task 11 runs them once at the end of the plan); the pull request body says when the rehearsal acceptance is only partly met.

Check: the Constraints section has one bullet that says no task of this plan commits and names `docs(release)` and `fix(post-release)`, and no line of the plan starts with a number followed by a dot or bracket.



### Medium findings the new plan must not repeat

Each of these is a defect of the first plan. Write the new plan so that it does not contain it; the change that avoids each one is in the last clause.

| id | grade | claim | citations | source findings |
|---|---|---|---|---|
| M-07 | Medium | Task 8 "confirms" the skill file was restored with `git diff --stat`. That output already shows Task 7's diff, so it proves nothing unless compared with a snapshot taken before the mutation. It also invites the same `git checkout` data loss as M-03. Its one restore sentence is covered by the M-03 repair wording; nothing else in Task 8 is repaired for it. | plan:234 | R3-F6 (debate C-003) |
| M-08 | Medium | Task 8 requires reverting **each** Task 7 edit to fail an assertion. Reverting the Output or Exit criteria edits (SKILL.md lines 103 and 105) cannot fail any listed assertion: those lines are never inspected. Task 8's acceptance says "each assertion group" and can pass, so nothing named rests on it. Not repaired: the "each edit" wording stays. | plan:212-214, 228-234, 239 | R2-F2 (debate C-004, X-001) |
| M-09 | Medium | Task 8 asserts the WARN line still ends with "then continue, anchored to the tag". The line ends with "tag." (with a full stop), so a literal ends-with assertion on "the tag" fails. | plan:232; src/superclaude/skills/sc-post-release-protocol/SKILL.md:74 | R3-F8 (second part) (debate C-006) |
| M-10 | Medium | Task 12 sends document defects back to Tasks 1, 2, 3 or 7, but never says to re-run the Task 6 and Task 8 tests or Task 11's `make sync-dev` and `make verify-sync`. A late fix to the skill file leaves a stale `.claude/` copy. | plan:299, 274-281 | R1-F6, R3-F5 (debate C-010) |
| M-11 | Medium | Task 2's acceptance criteria and Task 6's assertions can pass after G2's 30-minute limit, failed-run rejection and ambiguous-run escalation are deleted, and Task 12 does not exercise GitHub checks, so the required release-stop behaviour can be absent while its named checks pass. Medium, not Blocking: the design accepts text-only tests (`source.md:205`) and the task body already requires the text. | source.md:85; plan:98, 102-105, 192-196, 295 | R2-F7 (debate C-011) |
| M-12 | Medium | `_REQUIRED_COMMANDS` entries `make sync-dev` and `git merge-base --is-ancestor origin/master origin/integration` are already satisfied by other text. `make sync-dev` is on the page today (page lines 47 and 83), and the ancestry line is reused in Step 5. Removing Step 2 item 7 or the Step 2 precondition cannot make that entry fail. Task 6's "one failing mutation per group" would hit this with no guidance. The test also checks `_TEXT`, not fenced lines. | plan:192; docs/developer-guide/release-procedure.md:47, 83 | R1-F3 (debate C-013) |
| M-13 | Medium | The G7 row says "In a checkout of the release commit" (page line 77). Task 2 only adds a note that G7 runs on the detached reviewed-head checkout before merge. The row text stays and contradicts the "When" column. The G1 pass text "Every `gh` command ... passes `--repo`" (page line 71) now also conflicts with the `gh api repos/...` form. Line 23's "so Step 4 is unchanged" becomes false once Step 4 is rewritten, and Task 1 says to keep that sentence. | plan:99, 32; docs/developer-guide/release-procedure.md:23, 71, 77 | R1-F5 (debate C-014) |
| M-14 | Medium | Task 12 runs `git tag -a` and `git push origin <tag>` but has no guard that they target the temporary clone, such as `git -C <tmp>` or a `remote get-url` check before the push. If the working directory resets between calls [INFERRED] (depends on the executor), this pushes to the real fork. Its guard is carried inside the M-04 repair content, so it has no separate repair. | plan:287, 292 | R3-F7 (debate C-017) |

How the new plan avoids them: M-07 and M-14 are covered by the M-03 and M-04 wording above. M-08: Task 8 asserts the Output line and the Exit criteria line of SKILL.md (the replaced wording of lines 103 and 105), so that reverting each Task 7 edit fails one assertion, and the mutation check says "each assertion group". M-09: the WARN-line assertion allows the full stop at the end of the line. M-10: Task 12 says that after any fix sent back to Task 1, 2, 3 or 7 the pytest commands of Tasks 6 and 8 and `make sync-dev && make verify-sync` run again. M-11: Task 2's acceptance criteria also grep for the 30-minute limit, the no-go rule for a completed run that is not `success`, and the owner question for two push runs of one attempt. M-12: Task 6 matches `make sync-dev` and the Step 2 ancestry line inside the Step 2 section only (a helper that returns the text between one H2 and the next). M-13: Task 1 rewrites the sentence "so Step 4 is unchanged" (it becomes "Step 4 creates the tag, on the merge commit of the release PR"), and Task 2 rewrites the G7 row ("In a checkout of the release commit" becomes the detached reviewed-head checkout of Step 2) and the G1 pass text (it allows the `gh api repos/IronbellyOrg/IronClaude` form too).

### Notes the new plan should also avoid

- The page names no pull request number and no dated repository state ("today it exits 1 because pull request 854 left master ahead" is not written on the page); the state goes in the Task 12 log.
- `evals.json` line 19 also says "against master" in prose: Task 9 changes it with the `origin/master...HEAD` text.
- Task 4's acceptance uses `git diff -U0 -- CLAUDE.md` and expects one hunk, not "one changed block" from `git diff --stat`.
- Task 12's body and acceptance both say "passed, failed or not exercised".
- Task 12 says the log goes to `./artifacts/rehearsal-local.md` and not to `.dev/issues/826/` (the package is always staged), so the issue comment's `--body-file` paths are under `./artifacts/`.
- The environment-variable option of the Task 6 mutation check is removed (the `_PAGE` constant has no such interface).

### Format rules for the new plan

- No line may start with a number followed by a dot or a bracket, and none may be a checkbox, even inside a fenced block. Write orders inline as "(1) ... (3)".
- Task numbers run 1 to 13 without a gap; add the new steps inside Task 12 and Task 13, not as new tasks; each task has at most one `Depends on: Task K` line, naming a lower task.
- `./artifacts/` is the package folder: say in the tasks that use it that those commands run with the package folder as the working directory. No absolute path and no `.dev/tasks/to-do/` prefix in an operational link.
