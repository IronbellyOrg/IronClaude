3a9a7af2406ab1610b54764488bbf572416840d6
Review one task for spec compliance.

Task brief: ## Task 1: Rewrite the top of release-procedure.md, its Contents list and Step 2

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


AC ids (source order):
T1.AC1 = `grep -n 'Every merge to .master. therefore reaches' docs/developer-guide/release-procedure.md` prints nothing, and `grep -n '@vX.Y.Z' docs/developer-guide/release-procedure.md` finds a hit.
T1.AC2 = `grep -n 'so Step 4 is unchanged' docs/developer-guide/release-procedure.md` prints nothing, and `grep -n 'pull request 854' docs/developer-guide/release-procedure.md` prints nothing.
T1.AC3 = `grep -n -e '--base master --head <branch>' docs/developer-guide/release-procedure.md` prints nothing, and the page contains each command block above verbatim.
T1.AC4 = Every `gh` line inside a fenced block of the page contains `--repo IronbellyOrg/IronClaude` or starts with `gh api repos/IronbellyOrg/IronClaude`.
T1.AC5 = The Contents list has eight entries in the stated order and its Step 2, 3 and 4 anchors still resolve to existing H2 headings.
Global constraints: ## Constraints

- Edit under `src/superclaude/` first, never under `.claude/`; run `make sync-dev` then `make verify-sync`; never stage anything under `.claude/` or `.dev/issues/`.
- Documentation, skill text and two new tests only: no Python under `src/superclaude/cli/`, no edit to `.github/rulesets/` or `.github/workflows/`, no release script, no new `/sc:post-release` flag, no edit to `src/superclaude/commands/post-release.md`.
- Every `gh` command written into `docs/developer-guide/release-procedure.md` is on one line and carries `--repo IronbellyOrg/IronClaude` (or is `gh api repos/IronbellyOrg/IronClaude ...`). Installed primitives (the skill) name no `src/superclaude/` path and no literal branch name in the edited paragraph.
- No task creates a repository, pushes, tags, merges or opens a pull request on GitHub, with two exceptions that each need the owner's explicit approval in this session: the scratch-repository run of Task 13 and the one `gh issue comment` of Task 13. Read-only `gh api` GET calls on `IronbellyOrg/IronClaude` and read-only git checks of this repository stay allowed. The approval for the scratch repository must name it as the owner's exception to the project rule that the fork is the only target (`CLAUDE.md:49`, `CLAUDE.md:52`, `CLAUDE.md:76`); without that approval Task 13 records "not exercised".
- The headings `Step 1` to `Step 4`, `What a release is here` and `Sources` of the release page keep their text; the old Step 5 becomes Step 6 and a new Step 5 is added.
- No task of this plan commits. The delivery order applies to the story's commit step after the plan finishes: three commit groups, (1) `docs/developer-guide/release-procedure.md`, `CLAUDE.md`, `CONTRIBUTING.md` and `tests/docs/test_release_procedure.py`, (2) the skill text and `tests/skills/test_post_release_base_branch.py`, (3) the example commands; commit types `docs(release)` for (1) and (3) and `fix(post-release)` for (2); a last group (4) carries `.dev/tasks` (this package with its `./artifacts/` and the archived earlier plans) and `docs/memory/reflect/deviation-patterns-IronClaude.md`, has commit type `docs(dev)` and is committed last and alone; `.dev/reflect/`, `.dev/brainstorms/` and `.dev/issues/` are not committed; each group is committed with only its own paths so each can be reverted alone; `make sync-dev` and `make verify-sync` run after (2) and (3) (Task 11 runs them once at the end of the plan); the pull request body says when the rehearsal acceptance is only partly met.
- `./artifacts/` is the `artifacts` folder next to this plan. A command that reads or writes it runs with the package folder (the folder that holds this plan and `source.md`) as the working directory, in the same shell call; it reaches repository files through `"$(git rev-parse --show-toplevel)"`.
- Where this plan overrides the design: the H2 order of `test_contents_links_resolve` (design section 3.3, `source.md:150`) and the path of the local rehearsal log (design section 3.6, `source.md:186`) follow the "Revision 1" section of `./source.md`.

Start sha: 3a9a7af2406ab1610b54764488bbf572416840d6
Diff against the start snapshot: diff --git a/docs/developer-guide/release-procedure.md b/docs/developer-guide/release-procedure.md
index ca5cd2488..705b352f6 100644
--- a/docs/developer-guide/release-procedure.md
+++ b/docs/developer-guide/release-procedure.md
@@ -13,14 +13,15 @@ In the commands below, replace `X.Y.Z` with the version you are releasing, for e
 3. [Step 2: Open the release PR](#step-2-open-the-release-pr)
 4. [Step 3: Run the go/no-go gate (G1-G9)](#step-3-run-the-gono-go-gate-g1-g9)
 5. [Step 4: Tag and publish](#step-4-tag-and-publish)
-6. [Step 5: Post-release follow-through](#step-5-post-release-follow-through)
-7. [Sources](#sources)
+6. [Step 5: Merge master back into integration](#step-5-merge-master-back-into-integration)
+7. [Step 6: Post-release follow-through](#step-6-post-release-follow-through)
+8. [Sources](#sources)
 
 ## What a release is here
 
 - IronClaude is not published to PyPI. Users install from git with `pipx install git+https://github.com/IronbellyOrg/IronClaude`, then `superclaude install` (`scripts/README.md:3-9`). `uv build` builds the package locally without uploading it (`scripts/README.md:11`).
-- Every merge to `master` therefore reaches anyone who installs or upgrades. A release is a version number, a changelog section, a release-notes file, an annotated tag and a GitHub release on the fork, followed by `/sc:post-release`.
-- `master` and `integration` take pull requests only: the server refuses direct pushes, force pushes and deletion, and release tags (`v*`) cannot be deleted, rewritten or moved (see [Branch Protection](branch-protection.md)). Merging `master` into `integration` after a release is a pull request too. Creating a new tag stays open, so Step 4 is unchanged.
+- An unpinned `pipx install git+https://github.com/IronbellyOrg/IronClaude` follows the default branch (`integration`); a tagged install uses `@vX.Y.Z`. A release is a version number, a changelog section, a release-notes file, an annotated tag and a GitHub release on the fork, followed by `/sc:post-release`.
+- `master` and `integration` take pull requests only: the server refuses direct pushes, force pushes and deletion, and release tags (`v*`) cannot be deleted, rewritten or moved (see [Branch Protection](branch-protection.md)). Ordinary PRs target `integration`. A person promotes a batch with a release PR from `integration` to `master`, merged as a merge commit, and the annotated tag goes on that merge commit. `master` is then merged back into `integration` by pull request. Creating a new tag stays open: Step 4 creates it, on the merge commit of the release PR.
 - Every `gh` command carries `--repo IronbellyOrg/IronClaude`. This repository is a fork, and without `--repo` the GitHub CLI targets the upstream parent.
 
 ## Step 1: Choose the version
@@ -37,15 +38,23 @@ A removed command, flag, core file or MCP server is a breaking change. That is w
 
 ## Step 2: Open the release PR
 
-One PR on the fork carries the version bump, the changelog cut and the release notes.
+A release takes two PRs. The release-prep PR goes into `integration` and carries the version bump, the changelog cut and the release notes. The release PR goes from `integration` to `master` and carries nothing new: it only promotes what `integration` already holds. Items 2 to 5 are done on a branch cut from `origin/integration`.
 
-1. **Version.** Set the same version in three places that must agree (gate check G3):
+1. **Precondition: the previous release is merged back.** `master` must already be an ancestor of `integration`:
+
+   ```bash
+   git fetch origin master integration --tags
+   git merge-base --is-ancestor origin/master origin/integration
+   ```
+
+   Exit code 0 means go on. Exit code 1 means the previous release was not merged back into `integration`: do Step 5 first, with this check as its proof.
+2. **Version.** Set the same version in three places that must agree (gate check G3):
    - `version = "X.Y.Z"` in `pyproject.toml`
    - `__version__ = "X.Y.Z"` in `src/superclaude/__init__.py`
    - `uv run superclaude --version` then prints `SuperClaude, version X.Y.Z`
-2. **Changelog cut.** In `CHANGELOG.md`, move every entry under `## [Unreleased]` into a new `## [X.Y.Z] - YYYY-MM-DD` section directly below it, and leave `## [Unreleased]` empty above it (gate check G4). Add a link to the release notes in the new section, as the 5.0.0 section does.
-3. **Release notes.** Write `docs/releases/vX.Y.Z.md`, starting from the template `~/.claude/templates/workflow/changelog_template.md` (in a dev checkout also `.claude/templates/workflow/changelog_template.md` after `make sync-dev`). The file is tracked and is the body of the GitHub release (decision 7.3). Do not save release notes under `.claude/`: that folder is git-ignored. A detailed notes file is required for every major or minor version, for breaking changes and for 10 or more changed files (`changelog_maintenance.md:88-96`).
-4. **Retire data.** `superclaude install` and `superclaude update` remove the commands, skills and agents an earlier release shipped and this one does not, but only files whose SHA-256 matches the shipped file. The list is generated, not edited by hand. Regenerate it from the previous release's tag and commit the result:
+3. **Changelog cut.** In `CHANGELOG.md`, move every entry under `## [Unreleased]` into a new `## [X.Y.Z] - YYYY-MM-DD` section directly below it, and leave `## [Unreleased]` empty above it (gate check G4). Add a link to the release notes in the new section, as the 5.0.0 section does.
+4. **Release notes.** Write `docs/releases/vX.Y.Z.md`, starting from the template `~/.claude/templates/workflow/changelog_template.md` (in a dev checkout also `.claude/templates/workflow/changelog_template.md` after `make sync-dev`). The file is tracked and is the body of the GitHub release (decision 7.3). Do not save release notes under `.claude/`: that folder is git-ignored. A detailed notes file is required for every major or minor version, for breaking changes and for 10 or more changed files (`changelog_maintenance.md:88-96`).
+5. **Retire data.** `superclaude install` and `superclaude update` remove the commands, skills and agents an earlier release shipped and this one does not, but only files whose SHA-256 matches the shipped file. The list is generated, not edited by hand. Regenerate it from the previous release's tag and commit the result:
 
    ```bash
    git fetch --tags
@@ -54,12 +63,40 @@ One PR on the fork carries the version bump, the changelog cut and the release n
    ```
 
    The script writes `src/superclaude/cli/install_retired_data.py` (`scripts/gen_retired_install_data.py:1-23`). It reads names and file hashes with `git ls-tree` and `git cat-file` against each tag and compares them with the working tree. A workspace that skips a release only keeps retiring older names if every older tag is passed too.
-5. **Open the PR** with `/sc:pr-submit --monitor 3` in Claude Code. Fallback when that command cannot run:
+6. **Open the release-prep PR** with `/sc:pr-submit --monitor 3 --head <branch> --base integration --title "chore(release): prepare X.Y.Z"` in Claude Code. Fallback when that command cannot run:
 
    ```bash
-   gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title "chore(release): X.Y.Z" --body-file <body-file>
+   gh pr create --repo IronbellyOrg/IronClaude --base integration --head <branch> --title "chore(release): prepare X.Y.Z" --body-file <body-file>
    ```
 
+7. **Open the release PR** once the release-prep PR has merged:
+
+   ```bash
+   git fetch origin master integration --tags
+   gh pr create --repo IronbellyOrg/IronClaude --base master --head integration --title "chore(release): X.Y.Z" --body-file <body-file>
+   gh pr view <n> --repo IronbellyOrg/IronClaude --json headRefOid --jq .headRefOid
+   git rev-parse origin/master
+   gh pr checks <n> --repo IronbellyOrg/IronClaude --watch
+   ```
+
+   The two recorded values are `<reviewed-head-sha>` (the PR's `headRefOid`) and `<master-tip>` (`origin/master`). If `integration` moves, record both again and repeat from the `gh pr checks` line. A freeze notice on `integration` helps, but the head pin of the merge command is the guard. Do not use `/sc:pr-submit --monitor 3` for this PR: its fix loop pushes "to the PR head branch only, never the default or a protected branch" (`src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:192-195`), and `integration` is both.
+8. **Run the Step 3 rows marked before merge on a detached checkout of the reviewed head, in a clean checkout (not a new worktree).**
+
+   ```bash
+   git switch --detach <reviewed-head-sha>
+   make sync-dev
+   ```
+
+   `make sync-dev` is required before G5, because a fresh checkout has no `.claude/` copies and `make verify-sync` reports them missing.
+9. **Read the merge setting, then merge.**
+
+   ```bash
+   gh api repos/IronbellyOrg/IronClaude --jq '{merge: .allow_merge_commit, squash: .allow_squash_merge, rebase: .allow_rebase_merge, auto: .allow_auto_merge}'
+   gh pr merge <n> --repo IronbellyOrg/IronClaude --merge --match-head-commit <reviewed-head-sha>
+   ```
+
+   `merge` must be `true`, or the run stops. Never use `--squash`, `--rebase`, `--delete-branch`, `--admin` or `--auto`. A blocked merge is a stop, not a bypass.
+
 Anything that merges before the release PR is opened rides along in the release. Anything that merges later goes under the next `## [Unreleased]`.
 
 ## Step 3: Run the go/no-go gate (G1-G9)

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
