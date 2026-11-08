# Issue watcher: owner setup and runbook

## 0. Purpose and status

This runbook is for the owner of the issue watcher. It lists, in order, the steps you do by hand to set the watcher up, test it in shadow mode and, later, switch it on. Nothing in the implementation runs any of it, and the task that built the watcher performed none of these steps, so every command here is yours to run. The design is [issue-watcher.md](issue-watcher.md). No cron entry is enabled and `enabled` stays `false` until an owner-run live test (follow-up FU-1, section 14) has passed; you write the live-test record `docs/designs/issue-watcher-live-test.md` yourself during FU-1, and the implementation does not write it. Sections 0 to 7 cover setup and the shadow run; sections 8 to 15 cover the step before cron, the kill switch, exit codes, recovery, alerting, the rules while enabled, the deployment gate and the residual risks.

## 1. Pre-flight

Do these checks first. Each one fails early and cheaply, before the watcher makes a single call.

### 1.1 GitHub login and scopes

```bash
gh auth status
```

This must show a logged-in account for github.com. That account is the login the watcher runs as: it is the only assignee the watcher accepts on an issue (section 6). The watcher also reads the Project that holds the issues. If that read fails, add the scope and log in again in the browser:

```bash
gh auth refresh -s read:project
```

A cycle that cannot read the Project exits 3 (section 10). Neither command above is repository-scoped, so neither carries `--repo`.

### 1.2 The Orca CLI

The watcher looks for `orca-ide` first and then `orca` on the `PATH`. Find which one you have:

```bash
command -v orca-ide || command -v orca
```

The watcher accepts a binary only if its answer to the next command lists a topic named `orca-cli`. Run it with the name you found (use `orca` in place of `orca-ide` if that is the one):

```bash
orca-ide skills list --json
```

Read the reply and confirm that an entry named `orca-cli` is in it. Owner check: this runbook does not state the shape of Orca's reply. If no binary passes, a real cycle that reaches a launch ends exit 2 with `orca_not_found`.

### 1.3 The worktree and its origin

The claim session starts in one worktree, the `worktree` value of your configuration file (section 2). It must exist and its `origin` must be the fork:

```bash
git -C /absolute/path/to/worktree remote get-url origin
```

The output must name `IronbellyOrg/IronClaude` on github.com. `check-config` only tests that the worktree is an existing directory. The origin is checked by the cycle itself, which ends exit 2 with `origin_mismatch` when it differs, so run this check by hand now rather than learn it from the first dry run.

### 1.4 The watcher's own check

The watcher runs on Linux only: `once`, `check-config` and `init-state` exit 2 on any other platform. Confirm the command is installed:

```bash
superclaude issue-watch --help
```

It lists five commands: `once`, `status`, `check-config`, `init-state` and `reset`. Then validate your setup:

```bash
superclaude issue-watch check-config
```

It writes nothing. Exit 0 means the configuration, the worktree directory and the approvers file are valid; it prints `configuration is valid`, the state directory, the approvers file's modification time and the number of approver ids. A failure is exit 2 and a one-line reason on stderr. The configuration file and the approvers file do not exist yet, so come back to this step at the end of section 3.

## 2. The configuration file

The default path is `~/.config/superclaude/issue-watch.json`. Every command takes `--config <path>` to read another file, and a leading `~` in that option is expanded. The file is JSON, so it cannot hold comments. All behaviour comes from this file: there are no flags for the labels, the project, the worktree, the approvers file or the state directory.

```json
{
  "schema_version": 1,
  "enabled": false,
  "labels": {
    "trigger": "issue-watch:trigger",
    "approval": "issue-watch:approved"
  },
  "project_id": "PVT_REPLACE_WITH_PROJECT_NODE_ID",
  "owner_account_id": 1234567,
  "worktree": "/home/coder/workspaces/worktrees/IronClaude/issue-watch",
  "approvers_file": "/home/coder/.config/superclaude/issue-watch-approvers.txt",
  "state_dir": "/home/coder/.local/state/superclaude/issue-watch"
}
```

Replace every placeholder value. The fields:

| Field | Required | Default | Rule |
|---|---|---|---|
| `schema_version` | yes | none | The integer `1` |
| `enabled` | no | `false` | A JSON boolean. `false` makes `once` exit 0 with `not_enabled` before any external call; `once --dry-run` ignores it |
| `labels.trigger` | no | `issue-watch:trigger` | 1 to 50 characters, no control character, no comma, no double quote, not starting with a dash; matched exactly, case-sensitive |
| `labels.approval` | no | `issue-watch:approved` | Same rules, and different from `labels.trigger` |
| `project_id` | yes | none | `PVT_` followed by 1 to 64 letters, digits, `_` or `-` |
| `owner_account_id` | no | absent | A whole number from 1 up to 10^20 minus 1. When present, a cycle whose logged-in account has another id exits 2 with `account_id_mismatch` |
| `worktree` | yes | none | An absolute path to an existing directory |
| `approvers_file` | yes | none | An absolute path to the file of section 3 |
| `state_dir` | no | `${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/issue-watch/` | An absolute path, not on a network filesystem (nfs, nfs4, cifs, smb3, sshfs, fuse.sshfs, 9p); the check is skipped if the mount table cannot be read |

Rules that are easy to miss:

- Unknown keys are rejected, at the top level and inside `labels`, with exit 2 `config_invalid`. A typo such as `enable` fails loudly instead of leaving the default in place.
- A `~` or `$HOME` inside a JSON value is not expanded. `worktree`, `approvers_file` and `state_dir` must be written out as absolute paths.
- Labels must not contain a comma or a double quote, because the label is passed to the GitHub CLI's issue list filter, which splits on commas.
- `project_id` is the node id of the GitHub Project, not the project number. Owner action to verify: `gh project view <number> --owner IronbellyOrg --format json` is expected to print it as a value starting with `PVT_` (this needs the `read:project` scope of section 1.1). The design does not verify that prefix for your Project (follow-up FU-3). `check-config` checks only the shape of the value, so a wrong id shows up first in the shadow run of section 7, not in `check-config`.

## 3. The approvers file

The approvers file lists the GitHub accounts whose approval label counts. An approval label counts only when it was applied by a user account that is in this file.

- One decimal account id per line, for example `1234567`. The id is the number, not the login. No spaces around it and no leading zero.
- A line that starts with `#` in the first column is a comment. Blank lines are ignored. Any other line makes the whole file invalid.
- At least one id. Duplicates are merged.
- It must be a regular file (a symlink is refused), owned by the user that runs the watcher, and not writable by group or other.

A safe way to create it, with the owner as the only approver (replace the id):

```bash
mkdir -p ~/.config/superclaude
printf '%s\n' '# approvers for the issue watcher' '1234567' > ~/.config/superclaude/issue-watch-approvers.txt
chmod 600 ~/.config/superclaude/issue-watch-approvers.txt
```

How to find an account id is an owner action to verify, because the design does not state it. The watcher itself reads the id of the logged-in account from `gh api user`, so `gh api user --jq .id` is expected to print your own id. For another person, `gh api users/<login> --jq .id` is expected to work but is not verified here. Compare the number you get with the account before you trust it.

`check-config` prints only the file's modification time (UTC) and the number of ids, nothing else about its content. Note both values after each deliberate edit, so that you can notice a change you did not make.

Now run `superclaude issue-watch check-config` again. It must exit 0 before you go on.

## 4. Label setup

The two labels must exist in the repository before anyone can apply them. The watcher never creates labels and never writes to GitHub at all, and `/sc:issue` does not create them either. You create them once, by hand. These commands are documented here and are not run by the implementation:

```bash
gh label create issue-watch:trigger --repo IronbellyOrg/IronClaude
gh label create issue-watch:approved --repo IronbellyOrg/IronClaude
```

If you set other names under `labels` in the configuration file, create those names instead. `gh label create` also takes `--description` and `--color` if you want them. Confirm the result with:

```bash
gh label list --repo IronbellyOrg/IronClaude
```

Owner check: the design marks this exact `gh label create` form as not yet confirmed against the live repository. If `gh` refuses (for example because a label already exists), read its message and fix the cause. Do not substitute a different label name unless you also change the configuration file.

## 5. Create the state and re-approve earlier issues

Run `init-state` once, before the 24-hour shadow run of section 7:

```bash
superclaude issue-watch init-state
```

It creates the state directory (mode 0700), the store `dispatch.json` (0600) and the lock file `lock` (0600), and prints `state created: <state_dir>`. It never overwrites: when a store already exists it changes nothing, says so and exits 6. A cycle run before `init-state` ends exit 6 with `lock_missing`, because a cycle takes the lock before it reads the store; `store_missing` is what a cycle reports when the lock file exists but `dispatch.json` does not (section 11.5). `init-state` refuses to run when either file already exists.

The store records the time it was created, and an approval label applied at or before that time never counts (the decision line says `approval_before_init`). A dry run uses the same rule. So approvals from before the watcher was set up are never acted on. For every issue that was approved before `init-state` and that you want the watcher to consider, apply the approval label again, as one of the approvers of section 3. Remove the label first and wait a few seconds before you add it back, because two label events in the same second make the cycle skip the issue as `events_incomplete`:

```bash
gh issue edit 42 --repo IronbellyOrg/IronClaude --remove-label issue-watch:approved
sleep 5
gh issue edit 42 --repo IronbellyOrg/IronClaude --add-label issue-watch:approved
```

Do not edit the issue after you re-approve it (section 6).

## 6. Setup order for each issue

For each open issue you want the watcher to pick up, do these three steps in this order. The order matters because the approval has to be later than the trigger.

1. Assign the issue to the owner, which means the GitHub login the watcher runs as, and nobody else. The watcher accepts an issue only when the assignee set is exactly that one login. An issue with no assignee is skipped as `unassigned`; one with any other assignee, alone or in addition, is skipped as `assigned_other`.
2. Add the trigger label.
3. Wait a few seconds, then, as one of the approvers, add the approval label. An approval that is not strictly later than the trigger label event is skipped as `approval_before_trigger`, and two label events in the same second are skipped as `events_incomplete`.

```bash
gh issue edit 42 --repo IronbellyOrg/IronClaude --add-assignee @me
gh issue edit 42 --repo IronbellyOrg/IronClaude --add-label issue-watch:trigger
sleep 5
gh issue edit 42 --repo IronbellyOrg/IronClaude --add-label issue-watch:approved
```

`@me` is whoever `gh` is logged in as on the machine where you run the command; it must be the watcher's login. If the approver is a different person, that person runs the last command.

Two more conditions are checked on every cycle, so prepare them before step 3:

- The issue must be on the Project of `project_id`, in the Backlog status, and not archived. Otherwise it is skipped as `project_mismatch` (or `project_unreadable` when the Project cannot be read).
- Nothing may change after the approval. An edit to the issue body or title, or a comment by anyone other than the watcher's own login, made at or after the approval time makes the issue `edited_after_approval`. Finish all edits first, then approve.

## 7. Shadow rollout

The shadow run shows that the watcher decides the way you expect before it can start a single session. In a dry run the watcher reads GitHub, applies every rule and writes its decision lines, but it never calls Orca and never writes `dispatch.json`. `enabled` stays `false` throughout; a dry run ignores it.

Prerequisites: sections 1 to 6 are done and `check-config` exits 0.

Run this on a schedule for 24 hours, every 5 minutes (the cadence the timeouts are sized for):

```bash
superclaude issue-watch once --dry-run
```

The scheduler is your choice. This runbook does not prescribe one, and the Coder cron entry is follow-up FU-2. Each run prints `cycle: <reason>` and `exit: <code>`. When a run reaches an issue it would have launched, it also prints `probe: skipped` and `would_launch: <issue number>`. A run that finds the lock held exits 75 (`lock_held`), which is harmless when two runs overlap; if it keeps happening, make the interval longer.

Every run appends JSON lines to `<state_dir>/audit.jsonl`, one object per line, and the lines a dry run writes carry `"dry_run": true`. Look at the lines of the shadow run (use your own `state_dir` in place of the default shown):

```bash
grep '"dry_run": true' ~/.local/state/superclaude/issue-watch/audit.jsonl
```

There are two kinds of line to read:

- A `cycle` line has `exit`, `reason`, `gh_calls` and `duration_ms`. A cycle that ran to its end has `exit` 0 and the reason `cycle_complete`. Any other exit or reason is explained in section 10.
- A `decision` line has `issue`, `reason`, `approver_id`, `approval_event_id` and `approved_at`. The reason `launched` on a line with `"dry_run": true` means "would launch". Any other reason says why the issue was skipped, for example `unassigned`, `approval_before_trigger`, `not_approved`, `project_mismatch`, `edited_after_approval` or `day_cap`.

Compare these with what you expect, for each issue you prepared in section 6:

- An issue you prepared correctly shows `launched` in a dry-run decision line, with the `approver_id` of the approver you used.
- An issue you prepared wrongly shows the skip reason that names the mistake. It helps to prepare one deliberately wrong issue, for example one approved by an account that is not in the approvers file (which gives `not_approved`), to see that the watcher refuses it.
- At most one issue is reported as would-launch per cycle, and the candidates after it are not examined in that cycle. At most 6 would-launch decisions are made in any 24 hours; after that the reason is `day_cap`. A dry run records no launch for an issue, so the same issue may be reported as would-launch again in a later cycle (each report counts toward the day cap); judge by the first.
- `status` reflects real cycles only. Until the first real cycle, `status` reports no completed cycle and exits 1. That is expected during the shadow run and is not an error.

When the 24 hours are up and the lines match your expectation, you may remove `--dry-run`. Do not set `enabled: true` yet: section 8 lists what else must be done before any real cycle runs on a timer.

## 8. Before cron

Section 7 ends with a shadow run that decides the way you expect. Do not set `enabled` to `true` until every item below is done, in this order. The commands in sections 8 to 13 use the default state directory `~/.local/state/superclaude/issue-watch`. If you set `state_dir` in the configuration file, use that path instead (`check-config` prints it). If your configuration file is not at the default path, add `--config <path>` to every `superclaude issue-watch` command.

### 8.1 Review the shadow run

Read all the audit lines of the 24 hours, not only the would-launch decisions. First list the cycles that did not end with exit 0:

```bash
grep '"kind": "cycle"' ~/.local/state/superclaude/issue-watch/audit.jsonl | grep -v '"exit": 0'
```

No output means every cycle ended with exit 0. Each line printed is a cycle that did not: look its `reason` up in section 10 and fix the cause first. An exit 75 line (`lock_held`) is harmless on its own. Then read the `warning` lines (`clock_skew`, `discovery_count` and `dry_run_shadow_reset`, explained in section 10) and repeat the comparison of section 7 for every issue you prepared.

The timeouts, the day cap of 6 launches in 24 hours, the 60-minute lease and the limit of 10 candidates per cycle are fixed in the code, not in the configuration file. The design lists them as proposals for you to confirm after the shadow run. If one of them has to change, that is a code change, not a configuration edit.

### 8.2 Two-process lock test

The lock keeps two cycles from running at the same time. Test it on the real state directory: hold the lock from one process and start a cycle in another. `flock` is the util-linux command, and it takes the same kind of lock as the watcher:

```bash
flock ~/.local/state/superclaude/issue-watch/lock sleep 60 &
sleep 1
superclaude issue-watch once --dry-run
wait
```

The second command must print `cycle: lock_held` and `exit: 75`, and the audit log gets a `cycle` line with `"reason": "lock_held"` and `"exit": 75`. Use `--dry-run`: while `enabled` is `false`, a run without it stops at `not_enabled` before it reaches the lock. When `wait` returns, run `superclaude issue-watch once --dry-run` once more. It must run normally and not report `lock_held`. If `flock` is not installed on the machine, you need another way to hold a `flock` lock on that file for a minute; this runbook has not verified one.

### 8.3 The state directory survives a restart

The at-most-once guarantee lives in the state directory. A new, empty state directory has no memory of earlier launches (risk R5 of the design). Record what the directory looks like now:

```bash
ls -ld --time-style=full-iso ~/.local/state/superclaude/issue-watch ~/.local/state/superclaude/issue-watch/dispatch.json
grep -m1 '"created_at"' ~/.local/state/superclaude/issue-watch/dispatch.json
```

Restart the workspace the way you normally do, then run both commands again and run `superclaude issue-watch status`. The directory and `dispatch.json` must still exist, the `created_at` line must be the same, and `status` must not exit 6. If the directory is gone, `$HOME` is not persistent on your workspace template. Set `state_dir` in the configuration file to an absolute path on storage that persists (follow-up FU-2 covers this), run `check-config` and `init-state` again, and re-apply the approval labels as in section 5, because the new store has a new creation time. The audit log of the shadow run is lost with the old directory.

### 8.4 The staleness alert

Wire up the alert of section 12. No real cycle has completed yet, so `status` exits 1 right now and your alert should fire. Confirm that it does. It clears after the first real cycle that ends with exit 0.

### 8.5 The live-test record

The live test (follow-up FU-1, section 14) must have passed, and its record `docs/designs/issue-watcher-live-test.md` must be committed. You write that file; the implementation does not.

### 8.6 Set enabled

Only now change `"enabled": false` to `"enabled": true` in the configuration file:

```json
"enabled": true
```

Run `superclaude issue-watch check-config` again. The first real cycle starts a session for any issue that passes every check, so before you change the file, list which issues carry both labels, and keep the kill switch of section 9 at hand. Once a real cycle has ended with exit 0 and the reason `cycle_complete`, `superclaude issue-watch status` exits 0.

The cron entry is follow-up FU-2 and this work does not enable it. Its schedule is `"0 */5 * * * *"`: six fields, seconds first, which is every 5 minutes. FU-2 also covers a persisted `state_dir` if `$HOME` is not persistent.

## 9. The kill switch

To stop the watcher from starting anything new, create a file named `DISABLED` in the state directory:

```bash
touch ~/.local/state/superclaude/issue-watch/DISABLED
```

To enable it again, remove the file:

```bash
rm ~/.local/state/superclaude/issue-watch/DISABLED
```

The file's content does not matter, and a dangling symlink with that name counts as present. Nothing else needs to change and no lock is taken. What it does:

- A cycle checks for the file right after it takes the lock, before any call to GitHub. If it is there, the cycle ends with exit 0 and the reason `disabled`. This holds for `once --dry-run` as well.
- A cycle checks again just before the launch step. If the file appeared in between, the cycle starts nothing and ends with exit 0 and the reason `disabled_mid_cycle`.
- `status` shows the time the file was last touched as `disabled since`.
- `check-config`, `init-state` and `reset` do not look at the file.

What it cannot do: a session that has already been started cannot be stopped by it (risk R15). Neither does removing an approval label after the spawn has started stop that session. To end a running session, close it in Orca yourself; this runbook gives no command for that.

While the file exists, `status` goes unhealthy (exit 1) once 900 seconds have passed since the last completed cycle, because a cycle that ends `disabled` is not counted as completed. Expect the staleness alert of section 12 to fire during a planned stop. Setting `enabled` to `false` in the configuration file has the same effect on `once` (exit 0, `not_enabled`), except that `--dry-run` ignores it.

## 10. Exit codes and reason codes

### 10.1 Exit codes

`once` prints `cycle: <reason>` and `exit: <code>`, then ends with that code. The same code is in the `cycle` line it appends to the audit log. The other commands use the codes that the table marks.

| Exit | Meaning | Cycle reasons that give it |
|---|---|---|
| 0 | The cycle ended without a fault: it ran to its end or stopped on purpose. Skipped issues are not faults | `cycle_complete`, `disabled`, `disabled_mid_cycle`, `not_enabled` |
| 1 | `status`: unhealthy. `once`: an unexpected exception ended the cycle | `cycle_crashed` |
| 2 | Usage, configuration, platform, origin or Orca probe. `reset` also uses it for a refused request | `config_invalid`, `approvers_invalid`, `platform_unsupported`, `worktree_invalid`, `origin_mismatch`, `orca_not_found`, `account_id_mismatch` |
| 3 | GitHub login, scope, timeout or a reply that is not JSON | `login_invalid`, `gh_auth_failed`, `gh_timeout`, `gh_non_json`, `project_read_failed` |
| 4 | Discovery was cut off or repeated an issue | `truncated`, `discovery_duplicate` |
| 5 | Rate limited | `rate_limited`, `rate_limit_clamped` |
| 6 | Store or lock. `status`, `init-state` and `reset` also use it | `store_invalid`, `store_missing`, `lock_missing`, `lock_invalid`, `state_dir_unwritable` |
| 7 | An entry was written `failed`, `unknown` or `abandoned` (`spawn_error`) in this cycle | `prompt_invalid`, `revalidation_transient`, `launch_unknown`, `spawn_error` |
| 75 | The lock is held by another process, or the lock file was replaced. `reset` also uses it | `lock_held` |

What to do for each:

- **0.** Nothing. For `disabled` see section 9, for `not_enabled` see section 8.6.
- **1 from `status`.** The last completed cycle is more than 900 seconds old, or there is none yet. See section 12.
- **1 from `once` (`cycle_crashed`).** Stderr shows `issue-watch: cycle_crashed: <exception class name>` and one JSON line. Only the class name is printed, never the message, and no audit line is written for it. The lock was released. A `pending` entry may already have been saved; the next cycle makes it `abandoned` (`pending_orphan`) and does not launch it again, so check that issue's session (section 11). Run `check-config` and then `once --dry-run`. If the crash repeats, it is a defect to report. A cycle that dies from something that is not an ordinary exception, such as a signal or `SystemExit`, writes no audit line and no `cycle_crashed` line either; the operating system releases the lock when the process ends.
- **2.** Run `superclaude issue-watch check-config`; its stderr line names the reason. `origin_mismatch`: section 1.3. `orca_not_found`: section 1.2; it is found only when a launch is about to happen. `account_id_mismatch`: the logged-in account is not the one in `owner_account_id`; check `gh auth status`, or correct the value. `reset` exits 2 as well, as `reset_refused`, when you gave it wrong arguments or the issue has no `abandoned` or `unknown` entry (section 11).
- **3.** Run `gh auth status`. If the Project read is refused, run `gh auth refresh -s read:project` (section 1.1). `gh_timeout` is often transient; it also covers a cycle whose 240-second budget left no time to start the origin check, which then runs no git call. On the two shared reads (login and discovery), a `gh` failure the watcher cannot classify is reported as `gh_auth_failed` (design question Q4), so a persistent `gh_auth_failed` is not always a login problem. `gh_non_json`: `gh` printed something that is not the expected JSON; check that `gh` is current.
- **4.** `truncated` means 100 or more open issues carry the trigger label and are assigned to the watcher's login. Remove the trigger label from issues that are already claimed (section 13). The `discovery_count` warning appears at 80. `discovery_duplicate` means GitHub's reply repeated an issue number; the cycle launches nothing. The design gives no operator fix for it, so if it repeats, report it.
- **5.** Wait. `status` shows `next permitted at`; a cycle that starts before that time ends `rate_limited` without calling GitHub. When GitHub's reply carries no usable reset time, the wait is 3600 seconds (`rate_limit_clamped`; design question Q3). `reset --rate-limit` clears the wait (section 11); do that only when you know the limit has been lifted.
- **6.** `lock_missing` on a new setup (you have not run `init-state` yet, or the state directory is gone): run `init-state` (section 5); if the directory existed before and is gone, see section 8.3. `store_missing` (the lock file exists but `dispatch.json` does not), `store_invalid`, `lock_invalid`, and a `lock_missing` that appears where the directory still exists: section 11. `state_dir_unwritable`: writing failed (full disk, read-only mount or permissions); fix the cause. This reason is written to stderr only, because the audit log lives in the same directory.
- **7.** Run `superclaude issue-watch status` and find the issue in the cycle's decision lines (section 10.3). Section 11 says what to do for each entry state.
- **75.** Another cycle or a `reset` holds the lock. One occurrence is harmless. If every cycle reports it, look for a long-running `superclaude issue-watch` process, or make the interval longer. A cycle needs at most 240 seconds, inside the 5-minute cadence.

**Precedence.** When several conditions hold in one cycle, the exit code is the first present of 2, 6, 7, 5, 3, 4. Exit 75 is returned only when nothing else happened. A 7 (an entry written `failed`, or the `launch_unknown` or `spawn_error` outcome of a launch) ends the cycle's work: nothing after a launch-step outcome is read or written, so no `gh` call and no rate-limit stop can follow it, and in practice 7 is the last condition a cycle raises. Only a 6 can still follow it (the final write of the store), and then the exit is 6.

### 10.2 Reason codes

The audit log accepts only the 59 names below (`REASON_TABLE` in the package's `audit.py`); a name outside the table cannot be written. The rows are grouped by exit code and then by the kind of line that carries the reason. Two names, `cycle_complete` and `cycle_crashed`, are [PROPOSAL] names added while the watcher was built; confirm or rename them after the shadow run.

| Exit | Line | Reason | Meaning |
|---|---|---|---|
| 0 | cycle | `disabled` | The `DISABLED` file exists (section 9) |
| 0 | cycle | `disabled_mid_cycle` | `DISABLED` appeared just before the launch; nothing was started |
| 0 | cycle | `not_enabled` | `enabled` is `false` and this was not a dry run; no external call was made |
| 0 | cycle | `cycle_complete` [PROPOSAL] | The cycle ran to its end with no stop |
| 0 | decision, skip | `not_approved` | No approval counts: the label is absent or was removed later, or its latest application was not by a user account in the approvers file |
| 0 | decision, skip | `approval_before_trigger` | The approval is not strictly later than the trigger label |
| 0 | decision, skip | `approval_before_init` | The approval is at or before the store's creation time (section 5) |
| 0 | decision, skip | `events_incomplete` | The label history cannot be trusted: two label events in the same second, or no trigger label event found |
| 0 | decision, skip | `events_unreadable` | The label history could not be read |
| 0 | decision, skip | `edited_after_approval` | The issue body or title, or a comment by someone else, changed at or after the approval |
| 0 | decision, skip | `project_mismatch` | The issue is not on the configured Project, not in Backlog, or archived |
| 0 | decision, skip | `project_unreadable` | The Project could not be read for this issue |
| 0 | decision, skip | `unassigned` | The issue has no assignee |
| 0 | decision, skip | `assigned_other` | The assignee set is not exactly the watcher's login |
| 0 | decision, skip | `already_dispatched` | The store holds an entry for the issue that blocks a launch |
| 0 | decision, skip | `in_backoff` | An earlier attempt `failed`; the watcher waits 10 minutes |
| 0 | decision, skip | `day_cap` | 6 launches already count in the last 24 hours |
| 0 | decision, skip | `budget_exhausted` | The limit of 35 `gh` calls per cycle or the cycle's time ran out; the issue is not marked as examined and is tried again |
| 0 | decision, skip | `revalidation_failed` | The re-read just before the launch found a change: the issue closed, a label gone, another assignee, the approval voided or replaced, or the Project check failed |
| 0 | decision, skip | `marker_unreadable` | The issue's comments, where a claim marker would be, could not be read |
| 0 | decision, skip | `edits_unreadable` | The issue's edit history could not be read |
| 0 | decision, entry | `attempts_exhausted` | The third `failed` attempt; the entry is `abandoned` and the issue is not launched again unless you reset it |
| 0 | decision, entry | `pending_orphan` | A `pending` entry was found at the start of a cycle; it is now `abandoned`. A session may have started, so check it (section 11) |
| 0 | decision, entry | `claim_not_observed` | A `launched` entry whose 60-minute lease ended with no claim marker; it is now `abandoned` |
| 0 | decision, entry | `launched` | The launch call succeeded and the entry is `launched`. In a dry run it means "would launch" and no entry is written |
| 0 | decision, entry | `claimed` | The session's own claim marker was seen (also when someone claimed the issue by hand); this state is final |
| 0 | decision, note | `re-approved` | Not a reason: the value of the `note` key, written when the approval event differs from the stored one |
| 0 | warning | `discovery_count` | 80 or more trigger-labelled issues were found; at 100 the exit is 4 |
| 0 | warning | `clock_skew` | GitHub's clock and the machine's clock differ by more than 60 seconds |
| 0 | warning | `dry_run_shadow_reset` | `dry-run.json` could not be read and was replaced by an empty one |
| 0 | decision or warning | `operator_reset` | Written by `reset`: a decision line for a reset issue, a warning line for `--rate-limit` |
| 1 | cycle | `cycle_crashed` [PROPOSAL] | An unexpected exception ended `once`; written to stderr only |
| 2 | cycle | `config_invalid` | The configuration file is missing or malformed, or breaks a rule of section 2 (including a `state_dir` on a network filesystem) |
| 2 | cycle | `approvers_invalid` | The approvers file breaks a rule of section 3 |
| 2 | cycle | `platform_unsupported` | The machine is not Linux |
| 2 | cycle | `worktree_invalid` | `worktree` is not an existing directory |
| 2 | cycle | `origin_mismatch` | The worktree's `origin` is not the fork (section 1.3); checked at the start and again just before a launch |
| 2 | cycle | `orca_not_found` | No Orca binary passed the `orca-cli` check (section 1.2) |
| 2 | cycle | `account_id_mismatch` | The logged-in account's id differs from `owner_account_id` |
| 2 | warning | `reset_refused` | `reset` refused the request and changed nothing |
| 3 | cycle | `login_invalid` | The logged-in login does not have the shape of a GitHub login |
| 3 | cycle | `gh_auth_failed` | `gh` refused, or a failure on a shared read could not be classified |
| 3 | cycle | `gh_timeout` | A call timed out, or the 240-second budget left no time to start one |
| 3 | cycle | `gh_non_json` | `gh` printed something that is not the expected JSON |
| 3 | cycle | `project_read_failed` | The Project read failed, usually for a missing scope (section 1.1) |
| 4 | cycle | `truncated` | 100 or more matching issues were returned |
| 4 | cycle | `discovery_duplicate` | An issue number appeared twice in the discovery reply |
| 5 | cycle | `rate_limited` | A rate limit applies: GitHub gave a reset time within 3600 seconds, or `next_permitted_at` is still in the future |
| 5 | cycle | `rate_limit_clamped` | GitHub gave no usable reset time, so the wait is 3600 seconds |
| 6 | cycle | `store_invalid` | `dispatch.json` is unreadable or invalid |
| 6 | cycle | `store_missing` | `dispatch.json` does not exist although `lock` does (section 11.5) |
| 6 | cycle | `lock_missing` | The `lock` file does not exist (on a new setup: run `init-state`) |
| 6 | cycle | `lock_invalid` | `lock` is a symlink, a directory, or not owned by you |
| 6 | cycle | `state_dir_unwritable` | Writing to the state directory failed; stderr only |
| 7 | decision, entry | `prompt_invalid` | The prompt builder refused the issue number; the entry is `failed` |
| 7 | decision, entry | `revalidation_transient` | The re-read before the launch timed out or got a server error; the entry is `failed`, retried after 10 minutes, and abandoned after the third failure |
| 7 | decision, entry | `spawn_error` | Orca could not be started; the entry is `abandoned` |
| 7 | decision, entry | `launch_unknown` | Orca's outcome is not known (timeout, malformed reply or non-zero exit); the entry is `unknown` |
| 75 | cycle | `lock_held` | Another process holds the lock, or the lock file was replaced |

### 10.3 Reading the audit log

`audit.jsonl` has one JSON object per line, with sorted keys. It is rotated at 5 MiB into `audit.jsonl.1` to `audit.jsonl.4`. No issue title, body, label name or error text is ever written to it. A cycle writes its decision lines first and its one `cycle` line last. Every line has `kind`, `ts`, `host`, `login`, `cycle_id`, `dry_run` and `reason`. The kinds add these keys:

| Kind | Further keys |
|---|---|
| `cycle` | `exit`, `gh_calls`, `duration_ms`; optional `discovery_count`, and `clock_skew_s` (the offset in whole seconds between GitHub's clock and the machine's, on every cycle that read GitHub's date; the `clock_skew` warning is written only above 60 seconds) |
| `decision` | `issue`, `approver_id`, `approval_event_id`, `approved_at`; optional `state` (only when an entry was written, never in a dry run) and `note` |
| `warning` | optional `issue`, `discovery_count`, `clock_skew_s` |

To follow one issue, search for its decision lines:

```bash
grep '"issue": 42,' ~/.local/state/superclaude/issue-watch/audit.jsonl
```

Three facts help when you read it:

- The candidate that stops a cycle gets no decision line. The `cycle` line carries the stop reason, so a cycle that ends `origin_mismatch` or `rate_limited` shows no line for the issue it was examining.
- A cycle looks at 10 candidates at most and launches at most one issue.
- When the audit file cannot be written, or a failure happens before the state directory is known, the same facts go to stderr as one JSON line with `kind`, `ts`, `host`, `exit` and `reason`. `reset` also writes that line for the usage errors it finds before it reads the configuration.

### 10.4 The status command

`superclaude issue-watch status` reads `dispatch.json` and the `DISABLED` file and nothing else: it takes no lock, writes nothing and calls neither GitHub nor Orca. It exits 0 when healthy, 1 when unhealthy (the last completed cycle is more than 900 seconds old, or there is none) and 6 when the store cannot be read. `superclaude issue-watch status --json` prints these fields:

| Field | Type | Meaning |
|---|---|---|
| `healthy` | bool | The last completed cycle is no more than 900 seconds old |
| `last_completed_cycle_age_seconds` | int or null | Seconds since the last cycle that ended with exit 0 and no stop; null when there is none |
| `disabled_since` | UTC string or null | The time the `DISABLED` file was last touched |
| `next_permitted_at` | UTC string or null | The end of a rate-limit wait |
| `counts` | object | The number of entries in each state |
| `day_cap_used` | int | Launches that count in the last 24 hours, out of 6 |
| `stale` | list of `{issue, state, last_reason, updated_at}` | `unknown` entries, and `abandoned` entries with the reason `pending_orphan`, that are older than 24 hours |
| `retry` | list of `{issue, operation_id, cwd, argv}` | `unknown` entries that carry an operation id, with the command to retry them (section 11) |

Dry runs never count as completed cycles, so `status` reflects real cycles only. The text form prints the same facts, one per line, and the retry commands under `retry:`.

### 10.5 The SLO numbers

The design defines four service numbers: the 95th percentile of the time from approval to launch, the share of cycles in the last 7 days that ended with exit 0, the share of launched entries that were claimed within the 60-minute lease, and the count of stale entries. The function that computes them, `cycle.slo_numbers`, has no command. To call it, run this from a checkout of the repository, or with the Python that has `superclaude` installed in place of `uv run python`. Replace the path with your `state_dir`:

```bash
uv run python -I - ~/.local/state/superclaude/issue-watch <<'PY'
import json
import sys
from pathlib import Path

from superclaude.cli.issue_watch import cycle, record

state = Path(sys.argv[1])
lines = []
for name in ("audit.jsonl.4", "audit.jsonl.3", "audit.jsonl.2", "audit.jsonl.1", "audit.jsonl"):
    path = state / name
    if path.exists():
        lines += [json.loads(t) for t in path.read_text().splitlines() if t.strip()]
doc = record.FileStore(state).load()
print(cycle.slo_numbers(lines, doc, cycle.SystemClock().now()))
PY
```

It prints `approval_to_launch_p95_s`, `cycle_exit0_share`, `claimed_within_lease_share` and `stale_count`; the first three are `None` when there are no samples. Dry-run lines count toward none of the first three, and cycles that ended `disabled` or `not_enabled` are left out of the second. Review the numbers after the first 7 days live (follow-up FU-10).

## 11. Recovery

Recover only with the commands below. Never edit `dispatch.json`, `lock` or `audit.jsonl` by hand. `reset` takes the same lock as `once`; if it exits 75, wait a moment and run it again. Each `reset` outcome writes one audit line, a `decision` or `warning` line and never a `cycle` line.

### 11.1 Look first

Run `superclaude issue-watch status`. The `counts` line shows how many entries are in each state:

| State | What it means | Your action |
|---|---|---|
| `failed` | A step before the launch failed. The watcher tries again after 10 minutes, up to 3 attempts | None |
| `pending` | A launch was being started. It is seen only inside a cycle; a later cycle makes it `abandoned` (`pending_orphan`) | Check the session (11.2) |
| `launched` | Orca was asked to start the session. The watcher waits up to 60 minutes for the claim marker | None |
| `unknown` | Orca's outcome is not known. The entry leaves this state only by a claim or a `reset` | 11.2 or 11.4 |
| `abandoned` | The watcher gave up: `spawn_error`, `pending_orphan`, `claim_not_observed` or `attempts_exhausted` | 11.2 |
| `claimed` | The session's claim marker was seen. This state is final | None |

For an `unknown` or `abandoned` entry, every cycle also looks in the issue's comments for the session's claim marker. If the session did start after all, the entry becomes `claimed` by itself and needs no reset. The `stale` list of `status` holds `unknown` entries and `pending_orphan` entries older than 24 hours.

### 11.2 Forfeit the guarantee for one issue

By default the watcher launches an issue at most once. `reset` removes that protection for one issue. Use it only for an entry in the state `abandoned` or `unknown`, and only after you have checked the session:

1. Look at the issue for the claim comment written by the watcher's login (it carries the hidden text `<!-- sc:issue:claim -->`) and look in Orca for a session for that issue. This runbook gives no Orca command for the second check. Owner check: use whatever Orca view you normally use.
2. If a session exists or the comment is there, do not reset. The next cycle records `claimed` from the comment.
3. If there is no session, run:

```bash
superclaude issue-watch reset 42 --forfeit-guarantee
```

On success it prints `issue 42 may now be launched a second time` and exits 0. That sentence is a warning: the entry is removed, and the issue goes through every check again. If its labels and approval are still valid, a later cycle launches it again. The earlier launch still counts toward the day cap for 24 hours.

The command refuses with exit 2, and changes nothing, when the issue has no entry or the entry is in another state; it prints `issue-watch: reset refused: issue 42 has no abandoned or unknown entry; nothing changed`. It also exits 2 for a wrong argument list: an issue number without `--forfeit-guarantee`, or `--rate-limit` together with an issue number, or neither of the two. It exits 6 for a store or lock fault and 75 when the lock is held.

### 11.3 Clear a rate-limit wait

```bash
superclaude issue-watch reset --rate-limit
```

It prints `rate limit cleared` and clears only `next_permitted_at`. Use it when `status` shows `next permitted at` in the future and you know the limit is over. If the limit is still in force, the next cycle meets it again and sets a new wait.

### 11.4 The retry command for an unknown entry

For each `unknown` entry that carries an operation id, `status` prints the issue number, the directory to run from (the one stored with the entry) and a command:

```text
retry: 1
  issue 42: run from /absolute/path/to/worktree
    <orca> agent launch ... --retry-launch <operation id> --json
```

The command is the original launch command with `--retry-launch <operation id>` inserted before `--json`, and it starts with the bare name `orca-ide` or `orca`, whichever is first on your `PATH`. Change to the printed directory and run the printed line unchanged. It does not change the store. If the session starts, the next cycle sees the claim marker and records `claimed`. If it does not, the entry stays `unknown` and shows under `stale` after 24 hours; then use 11.2. Owner check: what Orca does with a retry for an operation id it does not know is not verified here; the live test (follow-up FU-1) records it.

### 11.5 A broken store or lock

The reasons `store_invalid`, `store_missing` and `lock_invalid` (exit 6), and a `lock_missing` where the state directory still exists, mean the store or the lock file is damaged. (`lock_missing` on a new setup is not damage: run `init-state`, section 5.) Do not repair the files and do not restore an older copy of the store, because an older copy allows launches that already happened (risk R11). Move the whole state directory aside and create a new one. First stop whatever runs `once` on a timer, if anything does. Then keep the old directory as evidence:

```bash
mv ~/.local/state/superclaude/issue-watch ~/.local/state/superclaude/issue-watch.broken
```

Then create the new state and check it:

```bash
superclaude issue-watch init-state
superclaude issue-watch check-config
```

The new store has a new creation time, so every earlier approval is void. Apply the approval label again to the issues you want considered, as in section 5. The new store also does not remember earlier launches; that record is in the `.broken` directory. Do not re-approve an issue whose session already started. `state_dir_unwritable` is different: it is not damage. Fix the disk, the mount or the permissions, and nothing else needs to change.

## 12. Alerting

The watcher sends no alerts itself. The rule is: alert when `last_completed_cycle_age_seconds` is above 900 or null. 900 seconds is three missed 5-minute cycles. `superclaude issue-watch status` already applies it: it exits 1 when the rule is met and 6 when the store cannot be read, so the check can be one command whose non-zero exit raises the alert:

```bash
superclaude issue-watch status > /dev/null || echo "issue watcher needs attention"
```

The `echo` stands in for your alert. `status` reads only the local store, takes no lock and calls neither GitHub nor Orca, so it is cheap to run often. Three things to know:

- A planned stop raises the alert too. A cycle that ends `disabled` or `not_enabled` does not count as completed (section 9), and neither does a dry run, so `status` is unhealthy during the shadow run and while the kill switch is on.
- A check that runs inside the same workspace is silent when that workspace is stopped, and a stopped workspace polls nothing (risk R9 of the design). Run the check somewhere else if you need to hear about that.
- The alert sink is follow-up FU-4 and has not been chosen. FU-4 also proposes an alert after three bad cycles in a row, meaning exit 3, 4, 5, 6 or 7. `status` does not read the audit log, so that rule is not built; until FU-4, look for such cycles yourself with the command of section 8.1.

## 13. While enabled

These rules hold from the moment `enabled` is `true`:

- **Never claim by hand an issue that carries the trigger label** (risk R14). A hand claim and a launched session can then run at the same time and do the same work twice. If you want to work an issue yourself, remove the trigger label from it first.
- **Remove the trigger label from issues that are claimed** (risk R3). The watcher reads at most 100 open trigger-labelled issues assigned to its login and ends exit 4 (`truncated`) at 100, so claimed issues that keep the label eventually stop all dispatch. The `discovery_count` warning appears at 80. The command is shown below the list.
- **Run one enabled workspace per GitHub login** (OD-8 of the design). The local record cannot see another workspace, so two enabled workspaces on one login could launch the same issue twice. Every audit line carries `host`, so a double enablement shows up as lines from two hosts for one `login`. Every workspace also multiplies the GitHub calls. By the design's proposed figures, one workspace makes 2 calls in an idle cycle (24 an hour, 0.48% of the 5,000-an-hour limit) and at most 37 in a busy one.
- **Leave an approved issue alone.** Any edit to the title or body, or a comment by someone other than the watcher's login, made at or after the approval time makes the issue `edited_after_approval`, and anyone who can comment can cause that (risk R17). The issue waits until you apply the approval label again: remove it, wait a few seconds, and add it back as one of the approvers (section 5).
- **Change the approvers file deliberately.** It is the only list of who can approve. After each edit, run `check-config` and compare the modification time and the count with your notes (section 3; risk R10).
- **Expect sessions to stay open.** A launched session runs until it ends (risk R7 of the design). The watcher starts at most one session per cycle and at most 6 in 24 hours, so look at the open sessions now and then.
- **Check `status` regularly.** It lists `stale` entries (section 11) and shows the day cap used.

To remove the trigger label from a claimed issue (42 here):

```bash
gh issue edit 42 --repo IronbellyOrg/IronClaude --remove-label issue-watch:trigger
```

## 14. Deployment gate and permissions

### 14.1 The live test (follow-up FU-1)

No cron entry is enabled and `enabled` stays `false` until you have run one live test on a test issue and committed its record. The test must:

- show that a prompt that begins with `/sc:issue` runs as a slash command in the launched session; if it does not, nothing works (risk R1);
- record the permission mode the session ran in (section 14.2);
- capture Orca's real replies for a successful launch and for an `unknown` outcome, and the real shapes of the issue events, the `lastEditedAt` field and the `projectItems` field;
- replace every `_assumed_shape` fixture in `tests/issue_watch/` with those captured replies, with `uv run pytest tests/issue_watch/` still passing.

You commit the record as `docs/designs/issue-watcher-live-test.md`. The design and the implementation do not write it. The design says only "one owner-run launch on a test issue" and does not say how to run it while `enabled` is `false`. Launch it by hand with the Orca CLI while `enabled` is still `false`, and say in the record exactly how you did it. Do not run a real `once` with `enabled` set to `true` for the test: such a cycle examines up to 10 candidates and launches the first eligible one, which need not be the test issue, and the safeguards of section 8.6 (list the issues that carry both labels first, keep the kill switch of section 9 at hand) apply only once the test has passed. `enabled` changes to `true` only in section 8.6.

### 14.2 Permissions of the launched session

The launch command carries no permission flag; a test pins it to its 12 elements with nothing extra (threat T10). So the session runs in its default, interactive mode, which keeps a human between the session and any write. That matters because the session reads text that anyone with comment access can write: the claim reads the issue's title, body and comments (risks R13 and R18). The rules are:

- **Default: no override.** Do not add a permission flag or a default argument to the launch.
- **A bypass mode needs your written acceptance.** Any mode that skips permission prompts is allowed only after you have accepted the risk in writing. This runbook suggests recording that acceptance in the live-test record.
- **Record the mode you saw.** Owner check: the design asks to trace whether Orca applies its own default arguments to a launched agent (follow-up FU-6). Read the mode off the session in the live test and do not assume it.
- **Do not add a second approver before FU-6.** Per-actor permission checks inside the launched session are not built.

## 15. Residual risks and follow-ups

### 15.1 Residual risks R10 to R18

The design accepts these. Their likelihood and impact ratings are proposals in the design and are not repeated here.

| Id | Risk | Mitigation or acceptance |
|---|---|---|
| R10 | An approver who is demoted, removed or compromised stays valid until you edit the approvers file | `check-config` prints the file's modification time and count; follow-up FU-9; accepted |
| R11 | A restored older store allows launches that already happened | Restoring a backup of the store is unsupported |
| R12 | Two stores on one login (two workspaces) can launch an issue twice | One enabled workspace per login; the `host` key on every audit line; the API cost multiplies by the number of workspaces |
| R13 | Edits or comments made after the re-read reach the session | The deployment gate and the permission mode (section 14) |
| R14 | A hand claim at the same time as a launch duplicates work | Section 13: never claim a trigger-labelled issue by hand |
| R15 | An approval removed, or `DISABLED` created, after the spawn has started cannot stop the session | Accepted; the check before the launch stops anything not yet started |
| R16 | Clock jumps distort the lease, the backoff, the day cap and the ordering, but never the launch count | Accepted; the 300-second tolerance for claim markers and the `clock_skew` warning make a skew visible |
| R17 | Any commenter can stall an approved issue until it is approved again | Apply the approval label again (section 13) |
| R18 | The integer-only prompt keeps issue text out of the prompt but not out of the session, because the claim reads title, body and comments | The deployment gate, the permission mode and the rule "unchanged since approval"; accepted |

### 15.2 When to revisit the design

The design chose a poller in each workspace (option A). Follow-up FU-7 tracks the nine conditions under which to revisit that choice:

1. Stopped workspaces cause excessive waiting.
2. Latency or API use becomes unacceptable.
3. Centralized approval or audit becomes necessary.
4. Duplicate claims persist.
5. Account binding becomes available.
6. Workspace tokens cannot read Projects.
7. Event-time Project changes matter.
8. A shared ledger becomes necessary.
9. Recurring workspace execution proves impossible.

### 15.3 Follow-ups

None of these is built by this work.

| Id | Item | When |
|---|---|---|
| FU-1 | Live test; replace every `_assumed_shape` fixture | Before any cron entry (section 14) |
| FU-2 | Cron entry `"0 */5 * * * *"` (six fields, seconds first), and a persisted `state_dir` if `$HOME` is not | After FU-1 and the shadow run |
| FU-3 | Fine-grained token scope; confirm the `read:project` scope and the Project read with a workspace token. A GitHub label relay (option D) is the first fallback if workspace Project access fails | When you move off the CLI login |
| FU-4 | Alerting on staleness, and after three bad cycles in a row; the sink is not chosen | When a sink is chosen |
| FU-5 | ETag conditional reads to cut the cost of unchanged reads | When the call budget is under pressure |
| FU-6 | Per-actor permission checks in the launched session; trace whether Orca applies default agent arguments | Before a second approver |
| FU-7 | Track the nine revisit conditions of section 15.2 | Ongoing |
| FU-8 | Automatic retry with `--retry-launch`, after the live test records Orca's retry rule | After FU-1 confirms the retry command |
| FU-9 | Approver role check, if the collaborator permission endpoint works with a workspace token | When the approver set grows |
| FU-10 | SLO review with `cycle.slo_numbers` (section 10.5) | After 7 days live |
| FU-11 | A size bound or pruning rule for finished entries, which are never removed and grow by about 2,200 a year at the day cap | When the store is above 1 MiB |
| FU-12 | Replace the network-filesystem deny-list for `state_dir` with an allow-list of local filesystem types | When per-host facts are gathered |

### 15.4 Coder#477

> Option A makes IronbellyOrg/Coder#477 unnecessary unless B or C is revisited. Options B and C, and Coder#477, return only on a revisit condition: the workspace cannot run a reliable cron, or one poller per login becomes unworkable.
