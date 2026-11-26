# Branch Protection

`master`, `integration` and the `v*` release tags of `IronbellyOrg/IronClaude` are protected by three GitHub repository rulesets. The rulesets are kept as JSON in `.github/rulesets/`; this page says what they do, how to apply and check them, and how to break glass.

## What is protected

| Ruleset | File | Target | Rules |
|---|---|---|---|
| `protect-master` | `.github/rulesets/protect-master.json` | `refs/heads/master` | `deletion`, `non_fast_forward`, `pull_request` (0 approvals) |
| `protect-integration` | `.github/rulesets/protect-integration.json` | `refs/heads/integration` | the same three rules |
| `protect-release-tags` | `.github/rulesets/protect-release-tags.json` | `refs/tags/v*` | `deletion`, `non_fast_forward`, `update` |

- Nobody can push straight to `master` or `integration`, force push over them or delete them. Every change arrives through a pull request, which a person or an automation may merge (zero approvals are required).
- Merging `master` into `integration` is a pull request too.
- Release tags can be created (`git push origin vX.Y.Z` still works) but never deleted, rewritten (`non_fast_forward`) or moved to another commit, forward or backward (`update`). There is deliberately no creation rule. The admin cannot bypass these rules either: the tag ruleset has no bypass actor.
- `protect-master` names `refs/heads/master` explicitly. Do not use `~DEFAULT_BRANCH`: the default branch is `integration`, so the token would protect the wrong branch.
- The two branch rulesets have one bypass actor: the Repository admin role (`actor_id` 5) in `pull_request` mode. It lets an admin merge a pull request that is blocked by a rule, and a direct push stays refused. Anything that runs under the admin login can use it, so a person uses it and records it (see Break glass). The tag ruleset has no bypass.

## Apply (repository admin only)

Before applying, confirm that no webhook, deploy key or GitHub App pushes to `master` or `integration`:

```bash
gh api repos/IronbellyOrg/IronClaude/hooks --jq 'length'
gh api repos/IronbellyOrg/IronClaude/keys --jq 'length'
gh api --paginate orgs/IronbellyOrg/installations --jq '.installations[] | [.app_slug, .permissions.contents] | @tsv'
```

Both counts should be `0`. The third command lists the GitHub Apps installed on the organization with their `contents` permission: an app with `write` can push, and once the rulesets are on it must use pull requests, because only the admin role can bypass them. Review each `write` app before applying. (The list shows installed apps, not which repositories they can reach.)

Apply in this order (tags first, then `integration`, then `master`):

```bash
gh api --method POST repos/IronbellyOrg/IronClaude/rulesets --input .github/rulesets/protect-release-tags.json
gh api --method POST repos/IronbellyOrg/IronClaude/rulesets --input .github/rulesets/protect-integration.json
gh api --method POST repos/IronbellyOrg/IronClaude/rulesets --input .github/rulesets/protect-master.json
```

Each call prints the new ruleset with its `id`. Comment the three ids and the date on the tracking issue (702).

## Check

```bash
gh api repos/IronbellyOrg/IronClaude/rulesets --jq '.[] | [.id, .name, .enforcement] | @tsv'
gh api repos/IronbellyOrg/IronClaude/rules/branches/master --jq '.[].type'
gh api repos/IronbellyOrg/IronClaude/rules/branches/integration --jq '.[].type'
```

The two branch checks must each print `deletion`, `non_fast_forward` and `pull_request`. Do not test a ruleset by pushing to, force pushing or deleting a real `master`, `integration` or release tag. To see a refusal, create a scratch ruleset on a throwaway branch name (for example `refs/heads/zz-ruleset-selftest`) with the same rules and push to that branch; delete the ruleset and the branch afterwards.

## Break glass

Use only when an emergency needs a direct push. The admin does all of it:

```bash
gh api --method PUT repos/IronbellyOrg/IronClaude/rulesets/<id> -f enforcement=disabled
# push the fix
gh api --method PUT repos/IronbellyOrg/IronClaude/rulesets/<id> -f enforcement=active
```

Then comment on the tracking issue (or an incident issue) with who, when and why. Do not rely on a ruleset audit log: whether the Free plan keeps one is not verified, so the comment is the record. The same comment is required each time the admin bypass is used to merge a pull request.

To roll a ruleset back completely: `gh api --method DELETE repos/IronbellyOrg/IronClaude/rulesets/<id>`. Re-apply it from the JSON file.

## Other IronbellyOrg repos

Six more public IronbellyOrg repositories get the same kind of protection for their `main` branch. The files are kept in `.github/rulesets/other-repos/`; the release-tag ruleset is the existing `.github/rulesets/protect-release-tags.json`. Nothing here is applied from this page without the audit and the gates below: each repo gets its rulesets only after its own 90-day check of direct pushes. The dated audit results are not kept here; they live in the audit records and the pull request that added this section.

| File | Role | Rules |
|---|---|---|
| `.github/rulesets/other-repos/protect-main.json` | full | `deletion`, `non_fast_forward`, `pull_request` (0 approvals) on `refs/heads/main` |
| `.github/rulesets/other-repos/protect-main-mirror.json` | mirror | `deletion`, `non_fast_forward` on `refs/heads/main`; no pull request is required, so a fork can still fast-forward from its parent |
| `.github/rulesets/other-repos/protect-aidev02.json` | full, one branch | the full role on `refs/heads/aidev02`; this file exists only on Clay's written yes for `aidev02` |

Both `main` files keep the one bypass actor of the IronClaude rulesets (the Repository admin role in `pull_request` mode). Whether the API accepts that bypass actor on the mirror, which has no `pull_request` rule, is UNVERIFIED; the self-test below answers it before anything real is created.

### Targets

| Repo | Applier | Branch role | Tag ruleset | Excluded branches | Owner |
|---|---|---|---|---|---|
| CPA-Manager-Plus | Clay | a fork: `protect-main-mirror.json` when the fork test gives 0 and Clay's written acceptance is quoted, `protect-main.json` when it gives more | applied only if the producer search clears it | `dev`, `release/v*` | Clay; standing rule: switch to `protect-main.json` when `ahead_by` is above 0 |
| IronOrca | Clay | a fork: the same role rule as above; `aidev02` is protected only on Clay's written yes (`.github/rulesets/other-repos/protect-aidev02.json`) | applied only if the producer search clears it | `dev`, `release/v*` | Clay; standing rule: switch to `protect-main.json` when `ahead_by` is above 0 |
| coder_orca | Clay | `protect-main.json` | skipped | none | Clay |
| IronHands-CLI | Ryan | a fork: the same role rule as the other forks | in Ryan's handoff, conditional | none | Ryan; standing rule: switch to `protect-main.json` when `ahead_by` is above 0 |
| irondots | Ryan | `protect-main.json` | in Ryan's handoff, conditional | `dot/*` | Ryan |
| ironops-marketplace | Ryan | `protect-main.json` | in Ryan's handoff, conditional | none | Ryan |

The applier writes to a repo only when the repo's audit record is `CLEAR` and every gate in the gate ledger passes. Repos where Clay has only read access (IronHands-CLI, irondots, ironops-marketplace) are never written to by Clay: the applier there is Ryan.

### Variables

Every command below uses these variables and never a repo name:

```bash
REPO=<repo name, for example CPA-Manager-Plus>
BRANCH=main
PARENT_OWNER=<owner of the parent repo, forks only>
ID=<ruleset id printed by the create call>
END=$(date -u +%Y-%m-%dT%H:%M:%SZ)
START=$(date -u -d "$END - 90 days" +%Y-%m-%dT%H:%M:%SZ)
```

### Role of a fork's main

A fork's `main` receives fast-forwards from its parent, which a `pull_request` rule would block. Print how far the fork is ahead of the parent:

```bash
gh api repos/IronbellyOrg/$REPO --jq .parent.full_name
gh api "repos/IronbellyOrg/$REPO/compare/$PARENT_OWNER:main...main" --jq '[.ahead_by, .behind_by] | @tsv'
```

If `ahead_by` is 0 the fork carries no work of its own and the mirror role fits, but only with Clay's written acceptance of the mirror's direct-push exposure. If `ahead_by` is above 0 the fork holds its own commits and gets the full role. Whether the Sync fork button is refused under a `pull_request` rule is UNVERIFIED.

### Before applying

```bash
gh api user --jq .login
gh api repos/IronbellyOrg/$REPO --jq '[.permissions.admin, .default_branch, .archived, .private] | @tsv'
gh api repos/IronbellyOrg/$REPO/hooks --jq length
gh api repos/IronbellyOrg/$REPO/keys --jq length
gh api repos/IronbellyOrg/$REPO/branches/main/protection
gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id, .name, .enforcement] | @tsv'
gh api --paginate orgs/IronbellyOrg/installations --jq '.installations[] | [.app_slug, .permissions.contents] | @tsv'
```

Expect the admin value `true`, default branch `main`, not archived and public; both counts `0`; the `branches/main/protection` call answering 404; and an empty ruleset list (an existing ruleset stops the repo, nothing pre-existing is updated or deleted). The installations command needs the `admin:org` scope: without it the command fails, and that failure is written down as "could not run" and blocks the repo until an organisation owner runs it or Clay accepts the gap in writing.

The 90-day audit of direct pushes (`time_period=quarter` is not used because its length is UNVERIFIED):

```bash
gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/$BRANCH&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp, .ref, .activity_type, .actor.login] | @tsv'
```

Classify every kept row as direct push by human, direct push by automation, sync (a parent fast-forward on a fork), pr_merge or branch_creation. The activity endpoint shows no tag events, so tag writes are invisible to it.

Producer search for the tag ruleset: read every workflow of the repo (`gh api repos/IronbellyOrg/$REPO/contents/.github/workflows`, then each file and the scripts it calls) and search them for `git push`, `git tag -d`, `push --delete`, `git/refs`, `gh release delete` and `--force`; look for other IronbellyOrg repos that hold a release token for the repo; check how tags arrive from a parent. Resolve every hit by reading it: no grep output proves nothing, because names built at run time defeat grep. The tag ruleset is applied only when the search is `CLEAR`.

### Apply

Create only if the ruleset name is absent, in this order: the tag ruleset, then non-default branches (`aidev02`), then `main`. Run each create from a checkout at the pushed commit that holds the files:

```bash
gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/protect-release-tags.json
gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/other-repos/protect-main.json
```

For a fork in the mirror role use `.github/rulesets/other-repos/protect-main-mirror.json` in the last command. After a timeout list the rulesets again before any retry. On the first 403 stop that repo and record the partial state.

### Check

```bash
gh api repos/IronbellyOrg/$REPO/rules/branches/$BRANCH --jq '.[].type'
gh api repos/IronbellyOrg/$REPO/rulesets/$ID
```

The first command prints `deletion`, `non_fast_forward` and `pull_request` for the full role, and `deletion` and `non_fast_forward` for the mirror. Compare the second with the file on `name`, `target`, `enforcement`, `conditions.ref_name`, the bypass actors, the rule types and the `pull_request` parameters; for the tag ruleset compare the rule types. A ruleset that fails the read-back is deleted by id (only a ruleset this rollout created) and the repo is reported as skipped.

### Self-test

Before the first real create, test the role on a throwaway branch of the target repo, from a scratch clone (never from IronClaude): create the branch `zz-ruleset-selftest` with two commits, create a scratch ruleset from the role file, check that a push is refused, then delete the ruleset and the branch.

```bash
# the scratch clone is on a local branch with two commits; create the throwaway branch first
# RULESET_FILE is the role file in a separate checkout of IronClaude (it is only read), for example
# RULESET_FILE=/path/to/IronClaude/.github/rulesets/other-repos/protect-main.json
# ID below is the id of the scratch ruleset that the create call prints, not a real ruleset
git push https://github.com/IronbellyOrg/$REPO.git HEAD:refs/heads/zz-ruleset-selftest
jq '.name="zz-selftest-<role>" | .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' "$RULESET_FILE" | gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input -
# full role: an empty commit on top must be refused (error GH013)
git commit --allow-empty -m "selftest: this push must be refused"
git push https://github.com/IronbellyOrg/$REPO.git HEAD:zz-ruleset-selftest
# mirror: rewinding the branch by one commit (a force push) must be refused
git push --force https://github.com/IronbellyOrg/$REPO.git HEAD~1:zz-ruleset-selftest
gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
git push https://github.com/IronbellyOrg/$REPO.git --delete zz-ruleset-selftest
gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
```

Run the empty-commit push for the full role and the force push for the mirror (the mirror skips the empty commit, so the force push rewinds a branch that holds both commits). The full role must refuse the empty commit pushed to the branch (error GH013); the mirror must refuse the force push of the earlier commit. The last command must show no name that starts with `zz-selftest-`. The answer of the scratch create also settles whether the mirror's bypass actor is accepted. If the API refuses it, drop the bypass actor from `protect-main-mirror.json` and change the file, the test and this page together before anything is applied.

### Roll back and break glass

The commands are the same as for IronClaude, with `$REPO` and `$ID`. Break glass, for an emergency that needs a direct push (the ruleset stays in place):

```bash
gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
# push the fix
gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
```

Roll back, which removes the protection for good: run it on its own, never as part of a break-glass sequence, and only for a ruleset that this rollout created:

```bash
gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
```

Comment on the tracking issue with who, when and why each time.

## Tests

`tests/docs/test_branch_protection_rulesets.py` pins the three JSON files and the files in `.github/rulesets/other-repos/` (targets, rule types, zero approvals, bypass actor) and the commands on this page. Changing a ruleset means changing its JSON, this page and that test together, then applying the new JSON with `gh api --method PUT repos/IronbellyOrg/IronClaude/rulesets/<id> --input <file>`.
