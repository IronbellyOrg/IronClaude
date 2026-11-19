# Orca automation for the merged pull request log

Definition only. Nothing in this file has been created in Orca, switched on or triggered. A person sets the automation up in Orca once, and Clay switches it on.

This repository holds no other automation definitions, so the exact file format Orca expects is not confirmed here. The fields below are what a person enters when creating the automation.

Name: merged-pr-log-refresh
Trigger (UTC): 5 0,6,12,18 * * *
Status: written, not switched on

## Why the name and the trigger are what they are

- The name must not start with `coordinator-`. Orca run history under that prefix is copied into the daily work report, and this log must stay out of it. The cost is that a failed run does not show in that report; see "When a run fails" below.
- Orca triggers are UTC, so the cron string is in UTC: five minutes past 0, 6, 12 and 18, every day of the week (the day-of-week field is `*`, so weekends run too). The script buckets days in the zone named by `DIGEST_TZ` (default `America/Chicago`), not in the zone of the trigger.
- The refresh interval and the lookback are `DIGEST_LOOKBACK_DAYS` (default 21) and the trigger above. Changing the lookback does not change the trigger.

## Command to run (precheck shape)

This is the shape the workspace's existing scheduled jobs use (not re-verified here): load the workspace environment, start the script detached, and exit non-zero so Orca starts no agent session and leaves no terminal. `<checkout>` is a checkout of this repository and `<out dir>` is a folder outside version control.

```
bash -lc 'set -a; [ -f ~/.aienv ] && . ~/.aienv; [ -f ~/.env ] && . ~/.env; set +a; cd <checkout> && setsid nohup uv run --no-project python scripts/merged_pr_log.py --out <out dir> >> <out dir>/run.log 2>&1 < /dev/null &'; exit 1
```

`uv run --no-project` is used on purpose: a plain `uv run` inside a checkout can rewrite `uv.lock`, which an unattended job must not do. The script itself reads credentials only from environment variables; the command above only loads the workspace's own environment first. If the five variables are already in the environment of the process Orca starts (the Coder user secret delivers them as environment variables), drop the two `. ~/...` loads.

## Environment variables (names only; no value belongs in any file)

- `GH_TOKEN`: a token that can read pull requests in both IronbellyOrg and IronbellyGroup.
- `CLICKUP_API_TOKEN`: a ClickUp personal token.
- `CLICKUP_WORKSPACE_ID`, `CLICKUP_DOC_ID`, `CLICKUP_PAGE_ID`: the ids of the ClickUp workspace, the Doc and the page inside it that the script rewrites.

Optional, not secret: `DIGEST_TZ` and `DIGEST_LOOKBACK_DAYS`.

## Human steps, in order

- Create the ClickUp Doc and one page in it, in the team's workspace. Share the Doc with the team only and leave public links off. Confirm the workspace's ClickUp plan allows the Docs API and shows the Doc to people who are not in a Coder workspace; the research behind this log did not confirm the plan.
- Note the workspace id, the Doc id and the page id, and check them against the ClickUp API before use.
- Create a GitHub token that can read pull requests in both orgs. The scheduler research found that a fine-grained token targets one org, so confirm which kind of token covers both before relying on one. Create a ClickUp personal token.
- Put the five variables above into the workspace environment without writing a value in any file, for example with `printf %s "$GH_TOKEN" | coder secret create aienv --env GH_TOKEN` for each name.
- Run the script once by hand with `--dry-run`: `uv run --no-project python scripts/merged_pr_log.py --out <out dir> --dry-run`. Read the two `rate limit` lines it prints (core, graphql and search remaining before and after) to see how much of the request budget one run uses. Then compare the size of `<out dir>/digest.md` with what a ClickUp page accepts; the page size limit is not confirmed.
- Run it once by hand without `--dry-run` and open the ClickUp page to check the content.
- Create the automation in Orca from the fields at the top of this file and leave it switched off.
- Clay switches the automation on.

## When a run fails

A failed run exits non-zero and leaves the page that is already in ClickUp as it was, so a partial log never replaces a good one. Because the name stays out of the daily work report, nothing else reports the failure. The `Generated` line at the top of the ClickUp page shows when it was last rebuilt, and `<out dir>/run.log` holds the error text (it never holds a token).
