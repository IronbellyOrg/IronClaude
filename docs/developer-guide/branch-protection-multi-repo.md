# Branch Protection for Other Repos

How to put the rulesets of [Branch Protection](branch-protection.md) on another repo of an organization, one repo per run, with `scripts/apply_org_rulesets.py`. Without `--apply` it is a dry run that writes nothing; `--apply --confirm <digest>` creates the rulesets and reads each one back.

## What the script does, and what you do

The script checks one repo and prints a dry run that writes nothing. With `--apply --confirm <digest>` and `--out` it saves `<repo>-before.json` and creates the listed rulesets that are not already present, reading each back. A ruleset of the same name is skipped only when it equals the listed one; otherwise the run refuses. It never posts the comment, never edits or deletes a ruleset, never changes classic branch protection, refuses the upstream organization and has no default `--org`.

You choose the repo, read the dry run, check the release workflows, hooks, keys and installed apps, run the apply, comment on issue 838 and roll back if needed. A dry run changes nothing; an `--apply` run that does not refuse is a live write to the repo you name.

## Variables

Every command on this page uses these, so a command is never typed against a repo by accident:

```bash
OWNER=<org>      # the organization that owns the repo
REPO=<repo>      # one repo per run
OUT=<folder>     # outside any git checkout; receives <repo>-before.json
```

## Order for each repo

1. **Set `OWNER`, `REPO` and `OUT`.**
2. **Check webhooks, deploy keys and installed apps.** Anything that pushes to a protected branch must use pull requests once the rulesets are on.

   ```bash
   gh api "repos/$OWNER/$REPO/hooks" --jq 'length'; echo "exit status: $?"
   gh api "repos/$OWNER/$REPO/keys" --jq 'length'; echo "exit status: $?"
   gh api --paginate "orgs/$OWNER/installations" --jq '.installations[] | [.app_slug, .permissions.contents] | @tsv'; echo "exit status: $?"
   ```

   Read the exit status of each. A command that failed (for example HTTP 403 or 404) means **unknown**, never "0": a missing answer is not an empty list. Resolve it before going on. Read the results as in [Branch Protection](branch-protection.md).
3. **Dry run.** Writes nothing:

   ```bash
   uv run python scripts/apply_org_rulesets.py --org "$OWNER" --repo "$REPO"
   ```

   Read every line of it and resolve each `would refuse --apply:` line. A dry run that cannot plan the repo prints `no plan: the repo could not be planned`.
4. **Check the release workflows by hand.** The dry run prints `WARNING: the tag ruleset blocks moving and deleting v* tags; check the release workflows of this repo by hand before applying.` Open each workflow under `.github/workflows/` of the repo and look for a step that moves or deletes a `v*` tag (a force push of a tag, `git tag -f`, `git push --delete`). If there is one, change it first or do not apply to this repo yet.
5. **Apply**, with the digest the dry run printed:

   ```bash
   uv run python scripts/apply_org_rulesets.py --org "$OWNER" --repo "$REPO" --out "$OUT" --apply --confirm <digest>
   ```

   A digest that differs from the digest of the rulesets rendered at apply time gives `confirm digest does not match the rulesets rendered now`; rerun the dry run. The digest covers only the ruleset bodies, not the repo or the push-check result, so take it from the dry run of this same repo. The output has `before state saved:`, one `created:` line per ruleset it created, `skipped, already present:` for a ruleset it skipped, `comment for issue 838:` and, under `rollback by hand`, the rollback commands.
6. **Check** (read-only):

   ```bash
   gh api "repos/$OWNER/$REPO/rulesets" --jq '.[] | [.id, .name, .enforcement] | @tsv'
   gh api "repos/$OWNER/$REPO/rules/branches/<branch>" --jq '.[].type'
   ```

   Each branch must print `deletion`, `non_fast_forward` and `pull_request`. Do not test by pushing to, force pushing or deleting a real protected branch or tag.
7. **Comment** the `comment for issue 838:` line on issue 838. Keep the before-state file where you can find it.

## The canary rule

Start with one low-risk repo. The canary must show complete activity coverage before other repos rely on it: every branch line of its dry run reads `(source activity, ...)` and none reads `incomplete`. If any branch line reads `source commits` or `incomplete`, stop before a second repo.

## The 90-day push check

- Each branch ends `pass`, `blocked` or `incomplete`, and the dry run prints the overall result with the same three words.
- `incomplete` is never turned into `pass`.
- Each branch line names its source: `source activity` or `source commits`.
- Only `source activity` can give `pass`. The commit list is the fallback when the activity source gives no full answer: it gives `blocked` when a commit in the window has no merged pull request, and otherwise `incomplete`, because it filters by commit date, not by push date, and so cannot see a push of an older commit. An `incomplete` check refuses `--apply`.
- A direct push by a named person is not excused: the check reports `blocked` for it.

## Refusals and failures

An `--apply` that refuses prints `refused:` and the texts below, joined by `; `, on stderr.

| Text | What you do |
|---|---|
| `repo is archived` | Do not apply to this repo |
| `no admin permission on the repo` | Get admin permission on the repo, then rerun the dry run |
| `repo has no default branch` | Do not apply to this repo |
| `repo cannot be read (HTTP <n>)` | Check the name and your access with `gh api "repos/$OWNER/$REPO"`, then rerun the dry run |
| `a branch lookup failed` | Rerun the dry run; if it repeats, check your access |
| `branch not supported: <reason>` | Do this repo by hand |
| `push check is <result>` | Do not apply; read the push check lines of the dry run |
| `classic branch protection on <branch>` | Do not apply; decide by hand with the repo owner |
| `branch protection state unknown on <branch>` | Rerun the dry run; if it repeats, decide by hand |
| `ruleset list cannot be read (HTTP <n>)` | Check your access, then rerun the dry run |
| `repo lists a ruleset id this script never touches` | Stop: the ids 28081842, 28081844 and 28081845 are never touched, so this is probably not the repo you meant |
| `same-name ruleset <name> (id <n>) differs: <differences>` | A ruleset of that name is already on the repo and is not the listed one. The script never edits one: fix it by hand (for example set the enforcement back to active), or remove it on purpose, then rerun the dry run |
| `same-name ruleset <name> (id <n>) cannot be read` | Check your access, then rerun the dry run |
| `no --out folder given` | Add `--out "$OUT"` |
| `confirm digest does not match the rulesets rendered now` | Rerun the dry run and use the digest it prints |
| `before-state file already exists: <path>` | Use another `OUT` folder, or move the old file away on purpose |
| `before-state read failed for ruleset <id>` | Check your access, then rerun the dry run |

A usage mistake prints `usage error:` and a reason and exits 64: fix the command line. The reasons include these and the ones the argument parser gives (for example `the following arguments are required: --org` or `unrecognized arguments: ...`):

- `--repo takes exactly one repo name`
- `--org: <reason>`
- `--confirm needs --apply`
- `--apply needs --confirm DIGEST`

Any other `refused: <text>` or `failed: <text>`: stop and report it.

After the before-state file is saved, a failed step prints `failed:` and one of these on stderr:

- `POST of <name> failed (HTTP <n>)`
- `POST of <name> timed out and no ruleset of that name found`
- `read-back of <name> (id <n>) failed`
- `read-back of <name> (id <n>) differs: <differences>`

The read-back and the same-name check accept the default parameters GitHub adds to a `pull_request` rule (the allowed merge methods, the required reviewers, the dismissal restriction and the extra approval for unattributed changes), each only with its default value. Every parameter the listed file names must be there with the same value, and any other difference, including one of those parameters set to another value, is reported.

After any `failed:` line, or any non-zero exit of an `--apply` run, first list the repo's rulesets by hand with the check command in step 6. Compare that list with the printed `created:` lines and the `rollback by hand` commands: a ruleset can exist that no printed line names. Only then decide on a rollback. A rerun into the same `OUT` refuses with `before-state file already exists: <path>`.

## Roll back by hand

The script has no rollback. Run the commands it printed under `rollback by hand`, or, for an id you found by listing the rulesets that is not in `<repo>-before.json`:

```bash
gh api --method DELETE "repos/$OWNER/$REPO/rulesets/<id>"
```

`<repo>-before.json` in `OUT` holds the keys `org`, `repo`, `saved_at`, `digest`, `rulesets` and `protection`. It is the record to restore from by hand; the script never reads it back.

## Not in this version (follow-ups)

Dropped from the first plan to keep this small, to be decided and built later if they are wanted: a persistent file of target repos with a status per repo and one writer; owner statements and evidence (pushes accepted by the owner, tag statements and exceptions); a scan of workflows for tag mutation and handling of deleted tags; an automatic review of hooks, keys and installed apps (step 2 above is by hand); a rollback command; a check over all the repos that the rulesets are on; an allowlist file; a branch-only interim state; and seven owner decisions from the review of the larger plan.
