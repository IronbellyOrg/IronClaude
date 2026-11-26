---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-designR1-20261126-060136
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Release path from integration to master: procedure, skill text, tests, rehearsal (issue 826)

Source: ./source.md
Goal: A person can cut a release from `integration` to `master` by following only `docs/developer-guide/release-procedure.md`; `/sc:post-release` resolves the default branch live and never reports a false release-integrity finding for a merged-back release; two new tests pin the wording; the `origin/master` examples are gone; a local rehearsal log proves the git commands; and the GitHub-side rehearsal and the comment that posts the evidence on issue 826 are each either done with the owner's explicit approval or recorded as not exercised.

## Constraints

- Edit under `src/superclaude/` first, never under `.claude/`; run `make sync-dev` then `make verify-sync`; never stage anything under `.claude/` or `.dev/issues/`.
- Documentation, skill text and two new tests only: no Python under `src/superclaude/cli/`, no edit to `.github/rulesets/` or `.github/workflows/`, no release script, no new `/sc:post-release` flag, no edit to `src/superclaude/commands/post-release.md`.
- Every `gh` command written into `docs/developer-guide/release-procedure.md` is on one line and carries `--repo IronbellyOrg/IronClaude` (or is `gh api repos/IronbellyOrg/IronClaude ...`). Installed primitives (the skill) name no `src/superclaude/` path and no literal branch name in the edited paragraph.
- No task creates a repository, pushes, tags, merges or opens a pull request on GitHub, with two exceptions that each need the owner's explicit approval in this session: the scratch-repository run of Task 13 and the one `gh issue comment` of Task 13. Read-only `gh api` GET calls on `IronbellyOrg/IronClaude` and read-only git checks of this repository stay allowed. The approval for the scratch repository must name it as the owner's exception to the project rule that the fork is the only target (`CLAUDE.md:49`, `CLAUDE.md:52`, `CLAUDE.md:76`); without that approval Task 13 records "not exercised".
- The headings `Step 1` to `Step 4`, `What a release is here` and `Sources` of the release page keep their text; the old Step 5 becomes Step 6 and a new Step 5 is added.
- No task of this plan commits. The delivery order applies to the story's commit step after the plan finishes: three commit groups, (1) `docs/developer-guide/release-procedure.md`, `CLAUDE.md`, `CONTRIBUTING.md` and `tests/docs/test_release_procedure.py`, (2) the skill text and `tests/skills/test_post_release_base_branch.py`, (3) the example commands; commit types `docs(release)` for (1) and (3) and `fix(post-release)` for (2); each group is committed with only its own paths so each can be reverted alone; `make sync-dev` and `make verify-sync` run after (2) and (3) (Task 11 runs them once at the end of the plan); the pull request body says when the rehearsal acceptance is only partly met.
- `./artifacts/` is the `artifacts` folder next to this plan. A command that reads or writes it runs with the package folder (the folder that holds this plan and `source.md`) as the working directory, in the same shell call; it reaches repository files through `"$(git rev-parse --show-toplevel)"`.
- Where this plan overrides the design: the H2 order of `test_contents_links_resolve` (design section 3.3, `source.md:150`) and the path of the local rehearsal log (design section 3.6, `source.md:186`) follow the "Revision 1" section of `./source.md`.

## Phase 1: Release procedure page

## Task 1: Rewrite the top of release-procedure.md, its Contents list and Step 2

Edit `docs/developer-guide/release-procedure.md` (design section 3.1 in `./source.md`, "Top of page" and "Step 2").

- Line 22: replace "Every merge to `master` therefore reaches anyone who installs or upgrades." with "An unpinned `pipx install git+https://github.com/IronbellyOrg/IronClaude` follows the default branch (`integration`); a tagged install uses `@vX.Y.Z`." and keep the rest of that bullet (a release is a version number, a changelog section, a release-notes file, an annotated tag and a GitHub release on the fork, followed by `/sc:post-release`).
- Line 23: add the rule: ordinary PRs target `integration`; a person promotes a batch with a release PR from `integration` to `master`, merged as a merge commit; the annotated tag goes on that merge commit; `master` is then merged back into `integration` by pull request. Keep the protection sentences and the `--repo` bullet (line 24), but change the last sentence of that bullet, "Creating a new tag stays open, so Step 4 is unchanged.", to "Creating a new tag stays open: Step 4 creates it, on the merge commit of the release PR."
- Contents list: seven numbered links plus Sources, in this order: What a release is here, Step 1, Step 2 (Open the release PR), Step 3 (Run the go/no-go gate (G1-G9)), Step 4 (Tag and publish), Step 5 (Merge master back into integration), Step 6 (Post-release follow-through), Sources. The anchors of Steps 1 to 4 stay unchanged (`#step-2-open-the-release-pr`, `#step-3-run-the-gono-go-gate-g1-g9`, `#step-4-tag-and-publish`).
- Step 2 intro becomes: two PRs; a release-prep PR into `integration` carries the version bump, the changelog cut and the release notes; a release PR from `integration` to `master` carries nothing new.
- Step 2 gets a new precondition item before the version item, with this block, and the text that an exit code of 1 means the previous release was not merged back (do Step 5 first, with this check as its proof). Write no pull request number and no dated repository state on the page; today's state belongs in the Task 12 log.

```bash
git fetch origin master integration --tags
git merge-base --is-ancestor origin/master origin/integration
```

- The version, changelog, release-notes and retire-data items stay, and say they are done on a branch cut from `origin/integration`.
- The "Open the PR" item becomes the release-prep PR: `/sc:pr-submit --monitor 3 --head <branch> --base integration --title "chore(release): prepare X.Y.Z"`, with the fallback `gh pr create --repo IronbellyOrg/IronClaude --base integration --head <branch> --title "chore(release): prepare X.Y.Z" --body-file <body-file>`. Keep the sentence that anything merging before the release PR is opened rides along and anything later goes under the next `## [Unreleased]`. The string `--base master --head <branch>` must not remain on the page.
- New item "Open the release PR" (after the release-prep PR has merged):

```bash
git fetch origin master integration --tags
gh pr create --repo IronbellyOrg/IronClaude --base master --head integration --title "chore(release): X.Y.Z" --body-file <body-file>
gh pr view <n> --repo IronbellyOrg/IronClaude --json headRefOid --jq .headRefOid
git rev-parse origin/master
gh pr checks <n> --repo IronbellyOrg/IronClaude --watch
```

  The two recorded values are `<reviewed-head-sha>` and `<master-tip>`; if `integration` moves, record both again and repeat from the `gh pr checks` line; a freeze notice on `integration` helps but the head pin of the merge command is the guard. Say not to use `/sc:pr-submit --monitor 3` for this PR because its fix loop pushes "to the PR head branch only, never the default or a protected branch" (`src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:192-195`) and `integration` is both.
- New item "Run the Step 3 rows marked before merge on a detached checkout of the reviewed head, in a clean checkout (not a new worktree)":

```bash
git switch --detach <reviewed-head-sha>
make sync-dev
```

  Say `make sync-dev` is required before G5 because a fresh checkout has no `.claude/` copies and `make verify-sync` reports them missing.
- New item "Read the merge setting, then merge":

```bash
gh api repos/IronbellyOrg/IronClaude --jq '{merge: .allow_merge_commit, squash: .allow_squash_merge, rebase: .allow_rebase_merge, auto: .allow_auto_merge}'
gh pr merge <n> --repo IronbellyOrg/IronClaude --merge --match-head-commit <reviewed-head-sha>
```

  Say `merge` must be `true` or the run stops, and add the sentence "Never use `--squash`, `--rebase`, `--delete-branch`, `--admin` or `--auto`. A blocked merge is a stop, not a bypass." (the word "Never" must be on the same line as the banned options, because a test checks this).

Acceptance criteria:
- `grep -n 'Every merge to .master. therefore reaches' docs/developer-guide/release-procedure.md` prints nothing, and `grep -n '@vX.Y.Z' docs/developer-guide/release-procedure.md` finds a hit.
- `grep -n 'so Step 4 is unchanged' docs/developer-guide/release-procedure.md` prints nothing, and `grep -n 'pull request 854' docs/developer-guide/release-procedure.md` prints nothing.
- `grep -n -e '--base master --head <branch>' docs/developer-guide/release-procedure.md` prints nothing, and the page contains each command block above verbatim.
- Every `gh` line inside a fenced block of the page contains `--repo IronbellyOrg/IronClaude` or starts with `gh api repos/IronbellyOrg/IronClaude`.
- The Contents list has eight entries in the stated order and its Step 2, 3 and 4 anchors still resolve to existing H2 headings.

## Task 2: Rewrite the Step 3 gate with the capture block and the When column

Depends on: Task 1

Edit `docs/developer-guide/release-procedure.md`, section "Step 3: Run the go/no-go gate (G1-G9)" (design section 3.1 in `./source.md`, "Step 3"). The heading text and the G1 to G9 numbers stay.

- Rewrite the intro paragraph (today "Run every check on the merge commit of the release PR. ...") to: every check must pass; any failure is a no-go, stop and take the result back to the release owner; do not tag and do not work around a failed check (decisions 7.7 and T1); rows marked "before merge" ran in Step 2 on the reviewed head; the rest run on the merge commit after the merge.
- Add this capture block before the table, with the pass rule below it:

```bash
gh pr view <n> --repo IronbellyOrg/IronClaude --json state,baseRefName,headRefName,headRefOid,mergeCommit
git fetch origin master integration --tags
git rev-parse --verify -q <merge-sha>^2
git rev-parse --verify -q <merge-sha>^3
git rev-parse <merge-sha>^1 <merge-sha>^2
git rev-parse <merge-sha>^{tree} <reviewed-head-sha>^{tree}
```

  Pass only if `state` is `MERGED`, `baseRefName` is `master`, `headRefName` is `integration` and `mergeCommit.oid` is not null (that value is `<merge-sha>`); the `^2` line prints a hash and the `^3` line prints nothing and exits 1; `^1` equals `<master-tip>` and `^2` equals `<reviewed-head-sha>`; the two trees are equal. Any failure: stop before tagging. A squash or rebase merge has no `^2`; `master` moving after Step 2 breaks the `^1` and tree checks.
- Add a "When" column to the gate table: G1 before merge; G2 after merge; G3, G4, G5, G6 and G7 before merge; G8 before merge unless the owner names a check that needs the merge commit or GitHub state; G9 after merge. Do not add a row and do not renumber.
- Replace the G2 command (`gh run list --repo IronbellyOrg/IronClaude --branch master --limit 3 --json headSha,conclusion,workflowName`) with `gh run list --repo IronbellyOrg/IronClaude --workflow Tests --event push --branch master --commit <merge-sha> --json databaseId,status,conclusion`. New pass condition: the push run for `<merge-sha>` completed with conclusion `success`; no run yet, or `status` not `completed`, means wait (repeat the command by hand, or `gh run watch <databaseId> --repo IronbellyOrg/IronClaude --exit-status`) for at most 30 minutes, then stop without tagging; a completed run that is not `success`, or no run by the deadline, is no-go; missing, other-SHA or `workflow_dispatch` evidence is never a pass; the newest attempt decides; two push runs for the same attempt: ask the owner. Keep the `test-summary` sentence.
- Rewrite the G7 row: its command cell "In a checkout of the release commit: `./update.sh`; ..." becomes "On the detached reviewed-head checkout of Step 2, after `make sync-dev`: `./update.sh`; ..." with the rest of the cell unchanged. In the G5 row or the notes under the table, say G5 runs on that checkout after `make sync-dev` too.
- Rewrite the G1 pass text so it reads: `origin` is `IronbellyOrg/IronClaude`; every `gh` command in this procedure passes `--repo IronbellyOrg/IronClaude` or is a `gh api repos/IronbellyOrg/IronClaude ...` call, so gh's default repository cannot send it to the upstream parent.
- The G7 notes about `./update.sh` stay.

Acceptance criteria:
- `grep -n -e '--limit 3' docs/developer-guide/release-procedure.md` prints nothing, and the page contains the G2 command above verbatim.
- `grep -n '30 minutes' docs/developer-guide/release-procedure.md` finds the G2 limit, `grep -n 'no-go' docs/developer-guide/release-procedure.md` finds the rule that a completed run that is not `success` is no-go, and `grep -n 'ask the owner' docs/developer-guide/release-procedure.md` finds the two-push-runs rule.
- The page contains the six capture-block lines verbatim and the table has a "When" column with the stated value for each of G1 to G9, still nine rows numbered G1 to G9, and the heading `## Step 3: Run the go/no-go gate (G1-G9)` is unchanged.
- `grep -n 'checkout of the release commit' docs/developer-guide/release-procedure.md` prints nothing, and the G1 row names the `gh api repos/IronbellyOrg/IronClaude` form.
- No fenced line on the page starts with `gh ` without `--repo IronbellyOrg/IronClaude` or the `gh api repos/IronbellyOrg/IronClaude` form.

## Task 3: Rewrite Step 4, add Step 5 (merge-back), renumber the post-release step to Step 6, add the Sources row

Depends on: Task 2

Edit `docs/developer-guide/release-procedure.md`, sections Step 4, the old Step 5, and Sources (design section 3.1 in `./source.md`, "Step 4", "Step 5", "Step 6").

- Step 4 keeps its first sentence ("never a later `master` commit"). Replace the command block with the lines below, and add the text: the first two commands must print nothing (the tag must not exist locally or on `origin`); the `ls-remote` line and the `rev-parse` line must both print `<merge-sha>` before `gh release create` runs; the `ls-remote` pattern must name `^{}`; run the lines one at a time and stop at the first failure.

```bash
git tag --list vX.Y.Z
git ls-remote --tags origin vX.Y.Z
git tag -a vX.Y.Z <merge-sha> -m "Release vX.Y.Z - <short description>" && git push origin vX.Y.Z
git ls-remote origin 'refs/tags/vX.Y.Z^{}'
git rev-parse vX.Y.Z^{commit}
gh release create vX.Y.Z --verify-tag --repo IronbellyOrg/IronClaude --title "vX.Y.Z - <short description>" --notes-file docs/releases/vX.Y.Z.md
```

- Add why `--verify-tag` is there: without it a failed push lets `gh release create` build a lightweight tag "from the latest state of the default branch", which is now `integration`, and the `v*` tag ruleset then makes it permanent. Add: never suggest a force push, a tag move or a tag deletion. Keep the `git cat-file -t` and `gh release view` check block and the sentence "Never push the tag to the `upstream` remote".
- Insert a new section `## Step 5: Merge master back into integration` after Step 4, with this block and text: if the first `is-ancestor` already exits 0, record "already merged back" and skip the last two lines; otherwise run all four lines, fetch again and check that the proof exits 0; the merge-back PR should change 0 files; if it changes any file or conflicts, stop and take it to the release owner (a content-carrying sync goes through a branch cut from `origin/integration` that merges `origin/master`, then an ordinary `/sc:pr-submit` PR, as pull request 846 did, outside this procedure); wait for any check the PR shows with `gh pr checks <m> --repo IronbellyOrg/IronClaude --watch`; the same ancestry fact `git merge-base --is-ancestor origin/master origin/integration` is the precondition of the next release (Step 2 precondition).

```bash
git fetch origin master integration --tags
git merge-base --is-ancestor <merge-sha> origin/integration
gh pr create --repo IronbellyOrg/IronClaude --base integration --head master --title "chore(release): merge master into integration after X.Y.Z" --body-file <body-file>
gh pr merge <m> --repo IronbellyOrg/IronClaude --merge
```

- Rename the old `## Step 5: Post-release follow-through` to `## Step 6: Post-release follow-through`. Before the `/sc:post-release vX.Y.Z` block add this block and the reason (a branch cut before the release-prep PR merged carries the old version metadata and `SKILL.md` line 74 then raises a false release-integrity finding); keep the rest of the section and "start the next cycle" text; `/sc:post-release` takes no new flag.

```bash
git fetch origin
git switch -c post-release-vX.Y.Z origin/integration
```

- Add one row to the Sources table: "Branch rules, tag rules and merge method" with the sources `docs/developer-guide/branch-protection.md` and `.github/rulesets/`. Cite no file under `.dev/brainstorms/` or `.dev/issues/`.

Acceptance criteria:
- The page contains each block above verbatim, includes `--verify-tag`, and contains the headings `## Step 5: Merge master back into integration` and `## Step 6: Post-release follow-through` in that order after `## Step 4: Tag and publish`.
- `grep -n '## Step 5: Post-release' docs/developer-guide/release-procedure.md` prints nothing.
- No fenced line on the page starts with `gh ` without the fork form, and none of `--admin`, `--auto`, `--squash`, `--rebase`, `--delete-branch` appears in a fenced line.
- `grep -n '.dev/brainstorms\|.dev/issues' docs/developer-guide/release-procedure.md` prints nothing.

## Phase 2: Project and contributor docs

## Task 4: State the release rule in the CLAUDE.md Git Workflow

Edit `CLAUDE.md`, section "Git Workflow", step 4 at line 297 (design section 3.5 in `./source.md`). Lines 290 and 292 to 296 stay.

- Replace the line "4. Merge to `integration` → validate → merge to `master`" with one line that keeps "Merge to `integration` → validate." and adds: Release: a person opens a PR from `integration` to `master`, merges it as a merge commit, tags that commit, then merges `master` back into `integration` by PR (exact commands: `docs/developer-guide/release-procedure.md`).

Acceptance criteria:
- `grep -n 'release-procedure.md' CLAUDE.md` finds a hit in the Git Workflow section, and the line "Merge to `integration` → validate → merge to `master`" no longer exists.
- `git diff -U0 -- CLAUDE.md` shows one hunk, and no other section of `CLAUDE.md` changed.

## Task 5: Move CONTRIBUTING.md from master to integration and drop the retired worktree example

Edit `CONTRIBUTING.md` (design section 3.5 in `./source.md`). First run `grep -n master CONTRIBUTING.md` to list every hit; edit every hit except line 73.

- Lines 9, 18, 22, 23, 24, 81 and 83 say `integration` where they mean the branch ordinary work is cut from or compared against (the rot-budget baseline is the most recent CI run on `integration`).
- Line 26 ("run the same check locally on master in a separate worktree") becomes "...on `integration` in a second, clean checkout (not the one that holds your PR branch)".
- Replace the fenced block at lines 28 to 35 (the `git worktree add --detach .dev/worktrees/master-check master` example) with this block, so the retired `.dev/worktrees/` location is gone:

```bash
git fetch origin integration
git switch --detach origin/integration
<run check>
```

- Line 66: `--base master` becomes `--base integration` in the `gh pr create --repo IronbellyOrg/IronClaude ...` fallback.
- Line 73 ("`master` and `integration` take pull requests only ...") stays. After it add one line: "Release PRs are the one exception: a maintainer promotes `integration` to `master` as described in [Release Procedure](docs/developer-guide/release-procedure.md)."

Acceptance criteria:
- `grep -n -e '--base master' CONTRIBUTING.md` and `grep -n '.dev/worktrees' CONTRIBUTING.md` print nothing.
- `grep -n master CONTRIBUTING.md` prints only the line 73 sentence and the new release-exception line.
- `grep -n 'release-procedure.md' CONTRIBUTING.md` finds the new link, and the target file exists.

## Phase 3: Procedure test

## Task 6: Add tests/docs/test_release_procedure.py

Depends on: Task 3

Create `tests/docs/test_release_procedure.py` (design section 3.3 in `./source.md`), following the pattern of `tests/docs/test_branch_protection_rulesets.py` (module constants `_REPO = Path(__file__).resolve().parents[2]`, `Path.read_text(encoding="utf-8")`, `pytest.mark.parametrize`). It reads `docs/developer-guide/release-procedure.md`.

- Constants and helpers: `_PAGE`, `_TEXT` (page text), `_fenced_lines()` returning the stripped lines inside triple-backtick fences, and `_section(title_start)` returning the page text from the H2 heading that starts with `title_start` up to the next H2 heading.
- `_REQUIRED_COMMANDS`: a module-level tuple of exact strings, one per command written in Tasks 1 to 3, except the two that the page also states in other sections (they are checked by the Step 2 test below): `/sc:pr-submit --monitor 3 --head <branch> --base integration`; `--base integration --head <branch>`; `gh pr create --repo IronbellyOrg/IronClaude --base master --head integration`; `gh pr checks <n> --repo IronbellyOrg/IronClaude --watch`; `git switch --detach <reviewed-head-sha>`; `gh pr merge <n> --repo IronbellyOrg/IronClaude --merge --match-head-commit <reviewed-head-sha>`; `--json state,baseRefName,headRefName,headRefOid,mergeCommit`; `git rev-parse --verify -q <merge-sha>^2`; `git rev-parse --verify -q <merge-sha>^3`; `git rev-parse <merge-sha>^{tree} <reviewed-head-sha>^{tree}`; the G2 command `gh run list --repo IronbellyOrg/IronClaude --workflow Tests --event push --branch master --commit <merge-sha> --json databaseId,status,conclusion`; `git ls-remote --tags origin vX.Y.Z`; `git ls-remote origin 'refs/tags/vX.Y.Z^{}'`; `git rev-parse vX.Y.Z^{commit}`; `--verify-tag`; `gh pr create --repo IronbellyOrg/IronClaude --base integration --head master`; `gh pr merge <m> --repo IronbellyOrg/IronClaude --merge`; `git merge-base --is-ancestor <merge-sha> origin/integration`; `git switch -c post-release-vX.Y.Z origin/integration`; `/sc:post-release vX.Y.Z`. One parametrized test asserts each is a substring of `_TEXT`.
- `test_step2_has_its_own_commands`: `make sync-dev` and `git merge-base --is-ancestor origin/master origin/integration` are each a substring of `_section("Step 2")`, so removing the Step 2 precondition or the Step 2 `make sync-dev` item fails this test even though the page states both elsewhere.
- `test_every_gh_line_names_the_fork`: each fenced line starting with `gh ` contains `--repo IronbellyOrg/IronClaude` or starts with `gh api repos/IronbellyOrg/IronClaude`.
- `test_banned_merge_options`: none of `--admin`, `--auto`, `--squash`, `--rebase`, `--delete-branch` appears in a fenced line, and any non-fenced line containing one also contains `never` (case-insensitive).
- `test_removed_text_is_gone`: the page lacks `--base master --head <branch>`, `--limit 3`, and "Every merge to `master` therefore reaches".
- `test_contents_links_resolve`: every `](#anchor)` in the Contents list equals the GitHub slug of one H2 heading (slug: lowercase, drop characters that are not word characters, spaces or hyphens, spaces to hyphens), and the H2 order is: Contents, What a release is here, Step 1 to Step 6, Sources. The `## Contents` heading stays on the page and the Contents list keeps its eight entries. This line overrides design section 3.3 (`source.md:150`), which left Contents out of the order.
- Mutation check, done once by hand and recorded in `./artifacts/t6-mutation-check.md` (commands that touch `./artifacts/` run with the package folder as the working directory and reach the page through `"$(git rev-parse --show-toplevel)"`): before the first mutation record the `sha256sum` of the page in `./artifacts/t6-page.sha256` and save a copy as `./artifacts/t6-page.pre-mutation`; both are written once and never overwritten on a rerun. For each group of required commands, remove or alter one line of the page in place, confirm the matching test fails and that `cmp` of the page against the saved copy exits 1 (which proves the mutation changed the page), then restore the page by copying the saved file back and confirm `cmp` exits 0. At the end `sha256sum -c` against the recorded file passes and the Task 6 tests pass on the restored page. Never use a command that discards uncommitted changes on the page (`git checkout`, `git restore`, `git reset --hard`, `git stash`): the edits of Tasks 1 to 3 are not committed.

Acceptance criteria:
- `uv run pytest tests/docs/test_release_procedure.py -v` passes with every parametrized case present.
- `./artifacts/t6-mutation-check.md` lists at least one failing mutation per test function, the checksum before and after, and states that the page was restored by copy.
- `uv run pytest tests/docs/test_branch_protection_rulesets.py -v` still passes.

## Phase 4: Skill text and its test

## Task 7: Rewrite the ancestry check in sc-post-release-protocol/SKILL.md

Edit `src/superclaude/skills/sc-post-release-protocol/SKILL.md` (design section 3.2 in `./source.md`). Read the file first; the line numbers below were checked on 2026-11-26.

- Line 91, the paragraph that starts `**Anchor the scan to the tagged commit.**`: keep everything up to and including "...removed with `git worktree remove` after the scan." and replace the rest of the paragraph (from "Confirm the tag actually belongs...") with: "Confirm the tag actually belongs to the release lineage. Resolve the default branch `<default-branch>` live with `git ls-remote --symref origin HEAD` (the `ref: refs/heads/<name>` line gives `<name>`); only when that call cannot reach the remote, fall back to `git symbolic-ref refs/remotes/origin/HEAD`, which can be stale. Record the value and which source gave it. Then run `git fetch origin <default-branch> --tags` and `git merge-base --is-ancestor <tag> refs/remotes/origin/<default-branch>`; never compare against a bare local branch name, which can be far behind its remote. If the fetch fails or the value came from the fallback, report the ancestry check as **unverified**, never as passed. If the tag is **not** an ancestor of the mainline, or the tree's version metadata disagrees with the tag, treat that as a release-integrity finding and report it before proceeding; with the finding, list the remote branches that contain the tag (`git branch -r --contains <tag>`, without the `origin/HEAD ->` alias line, at most 10, say when the list is cut off; when none: \"no remote branch contains `<tag>`\") and say that the release branch may not yet have been merged back into the default branch and should be merged back by pull request. Never hard-code a branch name." The paragraph must then contain none of the whole words `main`, `master` or `integration` (the word "mainline" is allowed).
- Line 74 (the WARN line ending "then continue, anchored to the tag."): unchanged.
- Line 103 (`**Output:** resolved tag + auto-detected default branch + ...`): "auto-detected default branch" becomes "default branch (resolved live, with its source)".
- Line 105 (`**Exit criteria:** tag anchored, default branch auto-detected, ...`): "default branch auto-detected" becomes "default branch resolved and its source recorded".
- Guardrails, lines 347 and 348: "work on a feature branch off the repo's **auto-detected default branch**" becomes "work on a feature branch off the default branch resolved in Wave 1"; the "PR target" bullet's "with `--base <default-branch>`" gets the addition "(the Wave 1 value; a value that came from the offline fallback is never used as a PR base: ask the user)".
- No change to `argument-hint` (line 5) and none to `src/superclaude/commands/post-release.md`.

Acceptance criteria:
- The paragraph at line 91 contains `git ls-remote --symref origin HEAD`, `git fetch origin <default-branch> --tags`, `git merge-base --is-ancestor <tag> refs/remotes/origin/<default-branch>`, `unverified` and `git branch -r --contains <tag>`, and the file no longer contains `git merge-base --is-ancestor <tag> <default-branch>`.
- `grep -n '[[:space:]]src/superclaude' src/superclaude/skills/sc-post-release-protocol/SKILL.md` shows no new hit compared with `git show HEAD:src/superclaude/skills/sc-post-release-protocol/SKILL.md`.
- `git diff --stat -- src/superclaude/commands/post-release.md` prints nothing.

## Task 8: Add tests/skills/test_post_release_base_branch.py

Depends on: Task 7

Create `tests/skills/test_post_release_base_branch.py` (design section 3.4 in `./source.md`), following the pattern of `tests/skills/test_primitive_dual_surface_lookup.py` (a `_SKILLS = Path(__file__).resolve().parents[2] / "src" / "superclaude" / "skills"` constant and a helper that reads `sc-post-release-protocol/SKILL.md` as lines).

- `_paragraph()`: the line that starts with `**Anchor the scan to the tagged commit.**`.
- Assert the paragraph contains `git ls-remote --symref origin HEAD`, `git fetch origin <default-branch> --tags`, `git merge-base --is-ancestor <tag> refs/remotes/origin/<default-branch>`, `unverified` and `git branch -r --contains <tag>`.
- Assert the whole file does not contain `git merge-base --is-ancestor <tag> <default-branch>`.
- Assert `re.search(r"\b(main|master|integration)\b", paragraph)` is `None`.
- Assert the line that starts with `**Output:** resolved tag` contains `default branch (resolved live, with its source)` and the line that starts with `**Exit criteria:** tag anchored` contains `default branch resolved and its source recorded`.
- Assert the WARN line (the line that contains `then continue, anchored to the tag`) still ends with that phrase, allowing the full stop that ends the line: `line.rstrip().rstrip(".").endswith("then continue, anchored to the tag")`. Assert the Guardrails section names the offline fallback and "ask the user".
- Assert `src/superclaude/commands/post-release.md` does not contain `--base`.
- Mutation check, done once by hand and recorded in `./artifacts/t8-mutation-check.md` (commands that touch `./artifacts/` run with the package folder as the working directory and reach the skill file through `"$(git rev-parse --show-toplevel)"`): before the first mutation record the `sha256sum` of the skill file in `./artifacts/t8-skill.sha256` and save a copy as `./artifacts/t8-skill.pre-mutation`; both are written once and never overwritten on a rerun. For each assertion group (the paragraph, the old command, the regular expression, the Output and Exit criteria lines, the WARN line and Guardrails text, the `--base` check), revert the matching Task 7 edit in place, confirm the matching assertion fails and that `cmp` against the saved copy exits 1, then restore the skill file by copying the saved file back and confirm `cmp` exits 0. At the end `sha256sum -c` passes and the Task 8 tests pass on the restored file. Never use a command that discards uncommitted changes on the skill file (`git checkout`, `git restore`, `git reset --hard`, `git stash`): the Task 7 edits are not committed.
- No temporary-history fixture: it would test git, not the skill text.

Acceptance criteria:
- `uv run pytest tests/skills/test_post_release_base_branch.py -v` passes.
- `./artifacts/t8-mutation-check.md` lists a failing mutation for each assertion group, the checksum before and after, and states that the skill file was restored by copy.
- `uv run pytest tests/skills/test_worker_contract.py tests/unit/test_cli_install.py -q` still passes (they reference the skill path and file list).

## Phase 5: Example commands

## Task 9: Replace origin/master in the two command files and the eval data

Edit three files (design section 3.5 in `./source.md`): `src/superclaude/commands/impact.md` line 23, `src/superclaude/commands/auggie-review.md` lines 37 and 113, and `src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json` lines 19 and 20.

- `impact.md:23`: `/sc:impact --diff origin/master --tests` becomes `/sc:impact --diff origin/integration --tests`.
- `auggie-review.md:37` and `:113`: `--diff origin/master...HEAD` becomes `--diff origin/integration...HEAD`.
- `evals.json:19`: the prompt text `--diff origin/master...HEAD ...` becomes `origin/integration...HEAD`, and its prose "against master" becomes "against integration". `evals.json:20`: the expected-output text "against master" becomes "against integration" and `git diff --stat origin/master...HEAD` becomes `git diff --stat origin/integration...HEAD`. The JSON stays valid and no other eval entry changes.
- Edit only text that names the example branch; keep every flag and sentence otherwise.

Acceptance criteria:
- `grep -rn 'origin/master' src/superclaude` prints nothing, and `grep -n 'against master' src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json` prints nothing.
- `uv run python -c "import json; json.load(open('src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json'))"` exits 0.
- `uv run pytest tests/commands/test_impact_command.py tests/commands/test_auggie_review_revagent.py tests/commands/test_auggie_review_remediation_chain.py -q` passes.

## Task 10: Replace origin/master in the user guide examples

Edit `docs/user-guide/codegraph.md` line 92 and `docs/user-guide/commands.md` lines 284 and 1335 (design sections 2 (open point 5) and 3.5 in `./source.md`).

- `codegraph.md:92` and `commands.md:284`: `/sc:impact --diff origin/master --tests` becomes `/sc:impact --diff origin/integration --tests`.
- `commands.md:1335`: `superclaude reflect run path/to/TASK.md --base origin/master --no-promote` becomes `--base origin/integration` (the `--base` option of `superclaude reflect run` takes any explicit audit base ref: `src/superclaude/cli/reflect/commands.py:307-315`).
- Do not edit `CHANGELOG.md` or anything under `docs/testing/`: they are historical records.

Acceptance criteria:
- `grep -rn 'origin/master' src/superclaude docs/user-guide` prints nothing.
- `git diff --stat -- CHANGELOG.md docs/testing` prints nothing.

## Phase 6: Sync and rehearsal

## Task 11: Sync the dev copies of the edited primitives

Depends on: Task 10

Run `make sync-dev` then `make verify-sync` from the repository root so the gitignored dev copies of the edited `src/superclaude/` primitives are current (design section 3.5 in `./source.md`, "Order of edits"). Record the command outputs and exit codes in `./artifacts/t11-sync.log`. Stage nothing under `.claude/`.

Acceptance criteria:
- `make verify-sync` exits 0.
- `git status --short -- .claude` prints nothing (the dev copies are ignored) and `git diff --cached --name-only` lists no path under `.claude/`.
- `./artifacts/t11-sync.log` shows both commands and exit code 0.

## Task 12: Run the local git rehearsal and write its log

Depends on: Task 11

Reproduce the written release steps and the skill's Wave 1 check in a temporary local repository and write the log to `./artifacts/rehearsal-local.md` (design section 3.6, part 1, in `./source.md`). The design's log path `.dev/issues/826/rehearsal-local.md` is overridden: the package is always staged, and the issue comment of Task 13 reads the file from `./artifacts/`. No GitHub call, no push to any real remote, no tag in the real repository. Use `mktemp -d` for the working directory and remove it at the end (nothing from it is committed). Commands that touch `./artifacts/` run with the package folder as the working directory.

- State before the run: before the run, and again before any fix sent back to Task 1, 2, 3 or 7, record into `./artifacts/t12-state-before.txt` the output of `git status --short --untracked-files=all`, `git rev-parse HEAD`, `git symbolic-ref -q refs/remotes/origin/HEAD` and `git tag --list 'rehearsal-*'` for the real repository (run each as `git -C "$(git rev-parse --show-toplevel)" ...` so the answer does not depend on the working directory).
- Location guard: every rehearsal git command runs as `git -C <absolute temporary clone>` or inside one shell call that starts with `cd` into the temporary folder; never rely on a previous call's folder or variables. Log `git rev-parse --show-toplevel` with each check and confirm it equals the temporary clone; before any push confirm `git remote get-url origin` prints the temporary bare repository. A missing or mismatched location invalidates the check, and the log must not be posted as evidence.
- Set up a bare repository as `origin` whose `HEAD` points to `refs/heads/integration`, with branches `integration` and `master`, and a clone of it. Use a tag name that does not start with `v`, for example `rehearsal-0.0.0`.
- Step 2 precondition: after a merge of `integration` into `master` made with `git merge --no-ff` (the stand-in for a GitHub merge commit; it has the same two-parent shape and does not prove `gh pr merge`), `git merge-base --is-ancestor origin/master origin/integration` exits 1; after the merge-back it exits 0.
- Step 3 capture: for the no-ff merge the `^2` line prints a hash, `^3` prints nothing and exits 1, `^1` equals the recorded master tip and `^2` equals the recorded head, and the two trees are equal; for a squash-shaped commit there is no `^2`; when `master` gets an extra commit between the recorded tip and the merge, the `^1` check fails.
- Step 4: the tag does not exist locally or on `origin` before tagging; after `git tag -a <tag> <merge-sha> && git push origin <tag>`, `git ls-remote origin 'refs/tags/<tag>^{}'` and `git rev-parse <tag>^{commit}` both print the merge SHA; `git ls-remote --tags origin <tag>` without `^{}` prints the tag object instead.
- Step 5: the proof `git merge-base --is-ancestor <merge-sha> origin/integration` exits 1 before the merge-back and 0 after, still 0 after a newer commit lands on `integration`, and a second run records "already merged back".
- Skill Wave 1 check: `git ls-remote --symref origin HEAD` prints `ref: refs/heads/integration`; with a stale local `integration` branch (behind `origin/integration`), `git merge-base --is-ancestor <tag> integration` exits 1 while `git merge-base --is-ancestor <tag> refs/remotes/origin/integration` exits 0 after a fetch; with `refs/remotes/origin/HEAD` set to `master` the offline fallback resolves `master`, which must be reported as unverified.
- The log lists each command, its output, its exit code, and passed, failed or not exercised; the GitHub-only items (`gh pr merge --match-head-commit`, `gh pr view` fields, `gh run list --commit`, `gh release create --verify-tag`, `gh pr checks --watch` with no checks) are listed as not exercised here.
- State after the run: record the same four outputs into `./artifacts/t12-state-after.txt`.
- A mismatch between a written step and the log is a document defect: fix it in Task 1, 2, 3 or 7, then run again the pytest commands of Tasks 6 and 8 and `make sync-dev && make verify-sync` (Task 11) and record the state files again.

Acceptance criteria:
- `./artifacts/rehearsal-local.md` exists and contains a command, output and exit code for each bullet above, each check marked passed, failed or not exercised, and the `git rev-parse --show-toplevel` output of each check, equal to the temporary clone.
- Every check that the written procedure or skill text claims (exit codes, printed values) matches what the log shows; a mismatch is fixed as the last bullet says before this task is accepted.
- `./artifacts/t12-state-before.txt` and `./artifacts/t12-state-after.txt` exist; the HEAD id, the `origin/HEAD` symbolic ref and the rehearsal tag list are identical in both, and the status lines differ only for paths inside this package's folder (its ledger, staging, `./artifacts/`). `integration` and `master` ids are not compared (other worktrees move them). On an unexplained mismatch the task stops and reports failure or concurrent interference; it does not restore shared refs or erase files.

## Task 13: Record the GitHub rehearsal status, prepare its command file and post the evidence

Depends on: Task 12

Create `./artifacts/rehearsal-github.md` (design section 3.6, part 2, in `./source.md`). A scratch repository on GitHub is an outward action: do not create a repository, push, tag, merge or open a pull request unless the owner has approved it explicitly in this session. Commands that touch `./artifacts/` run with the package folder as the working directory.

- Write the commands of Steps 2 to 6 of `docs/developer-guide/release-procedure.md` with the substitutions made for a scratch repository: the only allowed substitutions are the repository name `<scratch-owner>/<scratch-repo>` and a tag that does not start with `v`. Save them as `./artifacts/rehearsal-github-commands.sh.txt` (a text file, not an executable).
- Check that `grep -n 'IronbellyOrg/IronClaude' ./artifacts/rehearsal-github-commands.sh.txt` prints nothing, and list the checks the run must show: a missed substitution is rejected before it runs; `git remote -v` names the scratch repository before any push; `gh pr merge --match-head-commit` behaviour; `gh pr view` fields; `gh run list --commit`; `gh release create --verify-tag` rejecting a tag that is not on the remote; what `gh pr checks --watch` prints and returns for a PR with no checks; an idempotent merge-back; `master` moving between Step 2 and the merge stopping the tag; a content-carrying merge-back stopping; G5 to G8 recorded as not exercised.
- If the owner approved the run in this session, run it and record the evidence (PR ids, SHAs, parent checks, CI evidence, unperformed checks). If not, write at the top of the file: "Status: not exercised (needs the owner's approval to create a scratch repository)". Either way the file lists which acceptance point of issue 826 is met and which is partly met.
- After `./artifacts/rehearsal-github.md` exists, post the evidence on the issue: write `./artifacts/issue-comment-body.md` holding the text of `./artifacts/rehearsal-local.md` followed by the text of `./artifacts/rehearsal-github.md`. Only with the owner's explicit approval in this session for this posting (approval of a scratch repository is not approval to post), post it once with `gh issue comment 826 --repo IronbellyOrg/IronClaude --body-file ./artifacts/issue-comment-body.md` and record the comment URL in `./artifacts/issue-comment.md`. Without that approval, `./artifacts/issue-comment.md` starts with `Status: not posted (needs the owner's approval)`, holds the ready command, and the plan states that issue 826's rehearsal criterion stays partly met. Post nothing until the location proof of Task 12 is in the local log.

Acceptance criteria:
- `./artifacts/rehearsal-github.md` and `./artifacts/rehearsal-github-commands.sh.txt` exist; the commands file contains no `IronbellyOrg/IronClaude` text.
- `./artifacts/rehearsal-github.md` starts with a `Status:` line that says either `exercised` with evidence or `not exercised (needs the owner's approval to create a scratch repository)`.
- `./artifacts/issue-comment.md` exists and holds either the comment URL or the line `Status: not posted (needs the owner's approval)` with the ready command; no issue comment was posted unless that file records the owner's approval.
- No GitHub repository, pull request, tag or release was created by this task unless the file records the owner's approval.
