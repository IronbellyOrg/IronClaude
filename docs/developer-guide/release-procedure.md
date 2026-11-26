# Release Procedure

This is how a maintainer cuts an IronClaude release: the version bump, the release notes, the go/no-go gate (checks G1-G9), the tag, the GitHub release and the post-release follow-through. A human runs every step. No workflow, script or Makefile target cuts a release: the CI workflows run on pushes and pull requests to `master` and `integration`, never on tags (`.github/workflows/test.yml:3-6`).

The procedure generalizes the one used for v5.0.0: the gate is section 6.3 of `.dev/releases/current/v5.0.0/RELEASE-READINESS.md`, adopted as the release gate by decision 7.7 in `.dev/releases/current/v5.0.0/DECISIONS.md`. The changelog rules it relies on are in `src/superclaude/rules/core/changelog_maintenance.md` (installed as a rule file).

In the commands below, replace `X.Y.Z` with the version you are releasing, for example `5.1.0`.

## Contents

1. [What a release is here](#what-a-release-is-here)
2. [Step 1: Choose the version](#step-1-choose-the-version)
3. [Step 2: Open the release PR](#step-2-open-the-release-pr)
4. [Step 3: Run the go/no-go gate (G1-G9)](#step-3-run-the-gono-go-gate-g1-g9)
5. [Step 4: Tag and publish](#step-4-tag-and-publish)
6. [Step 5: Merge master back into integration](#step-5-merge-master-back-into-integration)
7. [Step 6: Post-release follow-through](#step-6-post-release-follow-through)
8. [Sources](#sources)

## What a release is here

- IronClaude is not published to PyPI. Users install from git with `pipx install git+https://github.com/IronbellyOrg/IronClaude`, then `superclaude install` (`scripts/README.md:3-9`). `uv build` builds the package locally without uploading it (`scripts/README.md:11`).
- An unpinned `pipx install git+https://github.com/IronbellyOrg/IronClaude` follows the default branch (`integration`); a tagged install uses `@vX.Y.Z`. A release is a version number, a changelog section, a release-notes file, an annotated tag and a GitHub release on the fork, followed by `/sc:post-release`.
- `master` and `integration` take pull requests only: the server refuses direct pushes, force pushes and deletion, and release tags (`v*`) cannot be deleted, rewritten or moved (see [Branch Protection](branch-protection.md)). Ordinary PRs target `integration`. A person promotes a batch with a release PR from `integration` to `master`, merged as a merge commit, and the annotated tag goes on that merge commit. `master` is then merged back into `integration` by pull request. Creating a new tag stays open: Step 4 creates it, on the merge commit of the release PR.
- Every `gh` command carries `--repo IronbellyOrg/IronClaude`. This repository is a fork, and without `--repo` the GitHub CLI targets the upstream parent.

## Step 1: Choose the version

Apply the semantic-versioning rule in `changelog_maintenance.md`:

| Part | When |
|---|---|
| MAJOR (`X.0.0`) | Breaking changes, incompatible API changes |
| MINOR (`X.Y.0`) | New features, backward-compatible |
| PATCH (`X.Y.Z`) | Bug fixes, documentation, backward-compatible |

A removed command, flag, core file or MCP server is a breaking change. That is why the release after 4.3.5 became 5.0.0 (decision 7.1).

## Step 2: Open the release PR

A release takes two PRs. The release-prep PR goes into `integration` and carries the version bump, the changelog cut and the release notes. The release PR goes from `integration` to `master` and carries nothing new: it only promotes what `integration` already holds. Items 2 to 5 are done on a branch cut from `origin/integration`.

1. **Precondition: the previous release is merged back.** `master` must already be an ancestor of `integration`:

   ```bash
   git fetch origin master integration --tags
   git merge-base --is-ancestor origin/master origin/integration
   ```

   Exit code 0 means go on. Exit code 1 means the previous release was not merged back into `integration`: do Step 5 first, with this check as its proof.
2. **Version.** Set the same version in three places that must agree (gate check G3):
   - `version = "X.Y.Z"` in `pyproject.toml`
   - `__version__ = "X.Y.Z"` in `src/superclaude/__init__.py`
   - `uv run superclaude --version` then prints `SuperClaude, version X.Y.Z`
3. **Changelog cut.** In `CHANGELOG.md`, move every entry under `## [Unreleased]` into a new `## [X.Y.Z] - YYYY-MM-DD` section directly below it, and leave `## [Unreleased]` empty above it (gate check G4). Add a link to the release notes in the new section, as the 5.0.0 section does.
4. **Release notes.** Write `docs/releases/vX.Y.Z.md`, starting from the template `~/.claude/templates/workflow/changelog_template.md` (in a dev checkout also `.claude/templates/workflow/changelog_template.md` after `make sync-dev`). The file is tracked and is the body of the GitHub release (decision 7.3). Do not save release notes under `.claude/`: that folder is git-ignored. A detailed notes file is required for every major or minor version, for breaking changes and for 10 or more changed files (`changelog_maintenance.md:88-96`).
5. **Retire data.** `superclaude install` and `superclaude update` remove the commands, skills and agents an earlier release shipped and this one does not, but only files whose SHA-256 matches the shipped file. The list is generated, not edited by hand. Regenerate it from the previous release's tag and commit the result:

   ```bash
   git fetch --tags
   uv run python scripts/gen_retired_install_data.py --tag vPREVIOUS   # add --tag for every older release still worth retiring from
   uv run python scripts/gen_retired_install_data.py --tag vPREVIOUS --check
   ```

   The script writes `src/superclaude/cli/install_retired_data.py` (`scripts/gen_retired_install_data.py:1-23`). It reads names and file hashes with `git ls-tree` and `git cat-file` against each tag and compares them with the working tree. A workspace that skips a release only keeps retiring older names if every older tag is passed too.
6. **Open the release-prep PR** with `/sc:pr-submit --monitor 3 --head <branch> --base integration --title "chore(release): prepare X.Y.Z"` in Claude Code. Fallback when that command cannot run:

   ```bash
   gh pr create --repo IronbellyOrg/IronClaude --base integration --head <branch> --title "chore(release): prepare X.Y.Z" --body-file <body-file>
   ```

7. **Open the release PR** once the release-prep PR has merged:

   ```bash
   git fetch origin master integration --tags
   gh pr create --repo IronbellyOrg/IronClaude --base master --head integration --title "chore(release): X.Y.Z" --body-file <body-file>
   gh pr view <n> --repo IronbellyOrg/IronClaude --json headRefOid --jq .headRefOid
   git rev-parse origin/master
   gh pr checks <n> --repo IronbellyOrg/IronClaude --watch
   ```

   The two recorded values are `<reviewed-head-sha>` (the PR's `headRefOid`) and `<master-tip>` (`origin/master`). If `integration` moves, record both again and repeat from the `gh pr checks` line. A freeze notice on `integration` helps, but the head pin of the merge command is the guard. Do not use `/sc:pr-submit --monitor 3` for this PR: its fix loop pushes "to the PR head branch only, never the default or a protected branch" (`src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:192-195`), and `integration` is both.
8. **Run the Step 3 rows marked before merge on a detached checkout of the reviewed head, in a clean checkout (not a new worktree).**

   ```bash
   git switch --detach <reviewed-head-sha>
   make sync-dev
   ```

   `make sync-dev` is required before G5, because a fresh checkout has no `.claude/` copies and `make verify-sync` reports them missing.
9. **Read the merge setting, then merge.**

   ```bash
   gh api repos/IronbellyOrg/IronClaude --jq '{merge: .allow_merge_commit, squash: .allow_squash_merge, rebase: .allow_rebase_merge, auto: .allow_auto_merge}'
   gh pr merge <n> --repo IronbellyOrg/IronClaude --merge --match-head-commit <reviewed-head-sha>
   ```

   `merge` must be `true`, or the run stops. Never use `--squash`, `--rebase`, `--delete-branch`, `--admin` or `--auto`. A blocked merge is a stop, not a bypass.

Anything that merges before the release PR is opened rides along in the release. Anything that merges later goes under the next `## [Unreleased]`.

## Step 3: Run the go/no-go gate (G1-G9)

Every check must pass. **Any failure is a no-go: stop and take the result back to the release owner.** Do not tag, and do not work around a failed check (decisions 7.7 and T1). The rows marked "before merge" ran in Step 2 on the reviewed head; the rest run on the merge commit after the merge.

After the merge, capture what was merged:

```bash
gh pr view <n> --repo IronbellyOrg/IronClaude --json state,baseRefName,headRefName,headRefOid,mergeCommit
git fetch origin master integration --tags
git rev-parse --verify -q <merge-sha>^2
git rev-parse --verify -q <merge-sha>^3
git rev-parse <merge-sha>^1 <merge-sha>^2
git rev-parse <merge-sha>^{tree} <reviewed-head-sha>^{tree}
```

Pass only if `state` is `MERGED`, `baseRefName` is `master`, `headRefName` is `integration` and `mergeCommit.oid` is not null (that value is `<merge-sha>`); the `^2` line prints a hash and the `^3` line prints nothing and exits 1; `^1` equals `<master-tip>` and `^2` equals `<reviewed-head-sha>`; the two trees are equal. Any failure: stop before tagging. A squash or rebase merge has no `^2`; `master` moving after Step 2 breaks the `^1` and tree checks.

| # | Check | When | Command | Pass condition |
|---|---|---|---|---|
| G1 | Fork target | before merge | `git remote -v` | `origin` is `IronbellyOrg/IronClaude`; every `gh` command in this procedure passes `--repo IronbellyOrg/IronClaude` or is a `gh api repos/IronbellyOrg/IronClaude ...` call, so gh's default repository cannot send it to the upstream parent. |
| G2 | CI on the exact commit | after merge | `gh run list --repo IronbellyOrg/IronClaude --workflow Tests --event push --branch master --commit <merge-sha> --json databaseId,status,conclusion` | The push run of the `Tests` workflow for `<merge-sha>` completed with conclusion `success`. No run yet, or a `status` that is not `completed`, means wait: repeat the command by hand, or run `gh run watch <databaseId> --repo IronbellyOrg/IronClaude --exit-status`, for at most 30 minutes, then stop without tagging. A completed run that is not `success`, or no run by the deadline, is no-go. Evidence that is missing, for another SHA or from a `workflow_dispatch` run is never a pass. The newest attempt decides; two push runs for the same attempt: ask the owner. Its `test-summary` job fails if the `test`, `swarm-marker-matrix`, `lint` or `doctor-check` job failed (`.github/workflows/test.yml:177-186`). |
| G3 | Version consistency | before merge | `grep -n '^version' pyproject.toml`; `grep -n '__version__ =' src/superclaude/__init__.py`; `uv run superclaude --version` | All three show `X.Y.Z`. |
| G4 | Changelog cut | before merge | `grep -n '^## ' CHANGELOG.md` | `## [Unreleased]` is empty and is followed by `## [X.Y.Z] - YYYY-MM-DD`; breaking entries sit in the `X.Y.Z` section. |
| G5 | Full local suite and gates | before merge | `make test`; `make lint`; `make verify-sync`; `make verify-deps`; `make lint-architecture` | All exit 0. Run on the detached reviewed-head checkout of Step 2, after `make sync-dev`. |
| G6 | Package builds | before merge | `uv build` | Wheel and sdist are built. Nothing is uploaded. |
| G7 | Upgrade path on an existing workspace | before merge | On the detached reviewed-head checkout of Step 2, after `make sync-dev`: `./update.sh`; start a new Claude session; `superclaude doctor`; `superclaude install --list`; `/sc:graph status` | `doctor` passes; `install --list` shows the codegraph block; `/sc:graph status` reports an index state. |
| G8 | Release-specific checks | before merge, unless the owner names a check that needs the merge commit or GitHub state | Whatever checks the owner names for this release | Each one passes and its result is recorded where the owner asked. For v5.0.0 these were the post-merge codegraph check and the QA-loop findings (`RELEASE-READINESS.md` section 6.2). |
| G9 | No open PR meant for this release | after merge | `gh pr list --repo IronbellyOrg/IronClaude --state open` | Only PRs that were deferred to a later release are open. |

Notes on G7:

- `./update.sh` installs the checked-out tree, not the release from GitHub: it runs `pipx install --force ./`, `superclaude install --force`, `make sync-dev` and `superclaude doctor` (`update.sh:7-10`). It needs `pipx` and `make` on the PATH.
- A plain `superclaude install` keeps existing framework files, so it does not test the upgrade. Use `./update.sh` or `superclaude install --force`.
- A running Claude session keeps the tools it started with. Start a new session before `/sc:graph status`.

## Step 4: Tag and publish

After G1-G9 all pass, tag the release PR's merge commit (never a later `master` commit) with an annotated tag, push the tag to `origin`, and create the GitHub release from the release notes:

```bash
git tag --list vX.Y.Z
git ls-remote --tags origin vX.Y.Z
git tag -a vX.Y.Z <merge-sha> -m "Release vX.Y.Z - <short description>" && git push origin vX.Y.Z
git ls-remote origin 'refs/tags/vX.Y.Z^{}'
git rev-parse vX.Y.Z^{commit}
gh release create vX.Y.Z --verify-tag --repo IronbellyOrg/IronClaude --title "vX.Y.Z - <short description>" --notes-file docs/releases/vX.Y.Z.md
```

Run the lines one at a time and stop at the first failure. The first two commands must print nothing: the tag must not exist locally or on `origin`. The `ls-remote` line, whose pattern names `^{}` so that it shows the commit the annotated tag points to, and the `rev-parse` line must both print `<merge-sha>` before `gh release create` runs.

`--verify-tag` is there because without it a failed push lets `gh release create` build a lightweight tag "from the latest state of the default branch", which is now `integration`, and the `v*` tag ruleset then makes that tag permanent. Never suggest a force push, a tag move or a tag deletion.

Check the result:

```bash
git cat-file -t vX.Y.Z
gh release view vX.Y.Z --repo IronbellyOrg/IronClaude
```

`git cat-file -t` prints `tag` for an annotated tag. The release URL must start with `https://github.com/IronbellyOrg/IronClaude/`.

Never push the tag to the `upstream` remote.

## Step 5: Merge master back into integration

The release PR put the merge commit on `master`. `integration` must contain it, or the next release starts from a diverged history:

```bash
git fetch origin master integration --tags
git merge-base --is-ancestor <merge-sha> origin/integration
gh pr create --repo IronbellyOrg/IronClaude --base integration --head master --title "chore(release): merge master into integration after X.Y.Z" --body-file <body-file>
gh pr merge <m> --repo IronbellyOrg/IronClaude --merge
```

If the first `is-ancestor` already exits 0, record "already merged back" and skip the last two lines. Otherwise run all four lines, fetch again, and check that the proof exits 0. The merge-back PR should change 0 files. If it changes any file or conflicts, stop and take it to the release owner: a content-carrying sync goes through a branch cut from `origin/integration` that merges `origin/master`, then an ordinary `/sc:pr-submit` PR, outside this procedure. Wait for any check the PR shows with `gh pr checks <m> --repo IronbellyOrg/IronClaude --watch`. The same ancestry fact, `git merge-base --is-ancestor origin/master origin/integration`, is the precondition of the next release (the Step 2 precondition).

## Step 6: Post-release follow-through

Once the tag exists and `master` is merged back, cut a branch from `origin/integration`:

```bash
git fetch origin
git switch -c post-release-vX.Y.Z origin/integration
```

A branch cut before the release-prep PR merged carries the old version metadata, and `SKILL.md` line 74 of `sc-post-release-protocol` then raises a false release-integrity finding. Then run in Claude Code:

```text
/sc:post-release vX.Y.Z
```

The command takes an existing release tag (for example `v5.0.0`) and brings the release's external surface up to date: user docs, technical docs, install and deploy scripts checked by real end-to-end runs, and human-run test guides. By default it writes its report, manifest and guides to `docs/testing/vX.Y.Z/` (`src/superclaude/commands/post-release.md:15,35-36`). It runs only after the tag exists.

Then start the next cycle: keep adding changes under `## [Unreleased]` in `CHANGELOG.md`.

## Sources

| Claim | Source |
|---|---|
| Gate G1-G9 and its commands | `.dev/releases/current/v5.0.0/RELEASE-READINESS.md`, section 6.3 |
| Gate adopted as the release gate; any failure goes back to the owner; tag on green, then `/sc:post-release` | `.dev/releases/current/v5.0.0/DECISIONS.md`, decisions 7.7 and T1 |
| Release notes at `docs/releases/vX.Y.Z.md`, used as `--notes-file` | `DECISIONS.md` decision 7.3; `src/superclaude/rules/core/changelog_maintenance.md:104-109` |
| Semantic-versioning rule | `changelog_maintenance.md:161-167` |
| Annotated tag; the GitHub release command always names the fork | `changelog_maintenance.md:126-144`; the `v5.0.0` tag is annotated (`git cat-file -t v5.0.0` prints `tag`) |
| No PyPI publishing; local `uv build` | `scripts/README.md:3-11` |
| CI triggers and `test-summary` job | `.github/workflows/test.yml:3-6,177-186` |
| Makefile targets used by G5 | `Makefile`: `test`, `lint` (depends on `lint-architecture`), `verify-sync`, `verify-deps`, `lint-architecture` |
| What `./update.sh` runs | `update.sh:7-10` |
| `/sc:post-release` input and output | `src/superclaude/commands/post-release.md:15,18,35-36` |
| `/sc:graph status` | `src/superclaude/commands/graph.md:8,21,31` |
| Branch rules, tag rules and merge method | `docs/developer-guide/branch-protection.md` and `.github/rulesets/` |
