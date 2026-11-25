# Branch Protection

`master`, `integration` and the `v*` release tags of `IronbellyOrg/IronClaude` are protected by three GitHub repository rulesets. The rulesets are kept as JSON in `.github/rulesets/`; this page says what they do, how to apply and check them, and how to break glass.

## What is protected

| Ruleset | File | Target | Rules |
|---|---|---|---|
| `protect-master` | `.github/rulesets/protect-master.json` | `refs/heads/master` | `deletion`, `non_fast_forward`, `pull_request` (0 approvals) |
| `protect-integration` | `.github/rulesets/protect-integration.json` | `refs/heads/integration` | the same three rules |
| `protect-release-tags` | `.github/rulesets/protect-release-tags.json` | `refs/tags/v*` | `deletion`, `non_fast_forward` |

- Nobody can push straight to `master` or `integration`, force push over them or delete them. Every change arrives through a pull request, which a person or an automation may merge (zero approvals are required).
- Merging `master` into `integration` is a pull request too.
- Release tags can be created (`git push origin vX.Y.Z` still works) but never moved or deleted.
- `protect-master` names `refs/heads/master` explicitly. Do not use `~DEFAULT_BRANCH`: the default branch is `integration`, so the token would protect the wrong branch.
- The two branch rulesets have one bypass actor: the Repository admin role (`actor_id` 5) in `pull_request` mode. It lets an admin merge a pull request that is blocked by a rule, and a direct push stays refused. Anything that runs under the admin login can use it, so a person uses it and records it (see Break glass). The tag ruleset has no bypass.

## Apply (repository admin only)

Before applying, confirm that no webhook, deploy key or GitHub App pushes to `master` or `integration`:

```bash
gh api repos/IronbellyOrg/IronClaude/hooks --jq 'length'
gh api repos/IronbellyOrg/IronClaude/keys --jq 'length'
gh api orgs/IronbellyOrg/installations --jq '.installations[] | [.app_slug, .permissions.contents] | @tsv'
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

## Tests

`tests/docs/test_branch_protection_rulesets.py` pins the three JSON files (targets, rule types, zero approvals, bypass actor) and the commands on this page. Changing a ruleset means changing its JSON, this page and that test together, then applying the new JSON with `gh api --method PUT repos/IronbellyOrg/IronClaude/rulesets/<id> --input <file>`.
