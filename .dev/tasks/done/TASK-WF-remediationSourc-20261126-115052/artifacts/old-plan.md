---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-remediationSourc-20261126-044652
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Apply the one-time Orca upstream override for issue 780 and record the result in CLAUDE.md

Source: ./source.md
Goal: Orca's stored record for this repository stops naming the upstream project as its identity when the one-time override takes effect (stored upstream null, project id github:ironbellyorg/ironclaude); the result, effective or not, is observed and written down with evidence; and the Orca paragraph of CLAUDE.md states the verified cause and the observed result without claiming more than was observed.

## Constraints

- Orca state is changed by exactly one repo.update call that carries only `upstream: null` for the repo with id e8e07d51-c261-4936-815e-06aeceeb5bf8. The Orca command line has no verb for it, so the call goes through the app's own client class in a one-off script. The call is sent at most once across every attempt of Task 2: a once-only marker file (named in Task 2) is written before the call and checked first, so a restart or retry of the task cannot send it again.
- The agent must not restart Orca (it hosts every running agent session) and must not open this repo's Settings panel. Durability across an Orca restart and after opening that panel therefore stays unverified and is reported as such.
- No Orca link flag (`--issue`, `--pr` or any other) is passed in any command, no worktree is created, no upstream git remote is added, and the upstream repository (SuperClaude-Org/SuperClaude_Framework) is not contacted.
- Every `orca` command in this plan is read-only and is run only after the three environment variables ORCA_PAIRING_CODE, ORCA_REMOTE_PAIRING and ORCA_ENVIRONMENT are confirmed unset in that same step, because a set variable can point the Orca command line at a remote runtime. A variable that is set to an empty value counts as set. A set variable's value is never printed.
- Files that must not change: pyproject.toml, package.json, anything under src/superclaude, the Orca files orca-data.json and its backups, the Orca database (it is never edited directly; the one allowed call changes it through Orca's own client), any git remote, the captured fixtures tests/sweep/fixtures/captured-worktree-current.json and tests/sweep/fixtures/captured-worktree-list.json (they record the old id as history), and every part of CLAUDE.md outside the Orca paragraph.
- The second state change that also replaces the repo icon (step B of the REPORT.md Proposed Fix) is not run without the owner's approval. If the override does not take effect, the decided fallback is to change Orca, which is outside this plan and is reported for the owner.
- Evidence files are written under ./artifacts/ inside this package. The one-off script and its once-only marker are not delivery files: they live in the folder `.dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/` (the spec's own example location), stay untracked and are never staged or committed. `git add` is never run on that folder.
- Timestamps written into any evidence file are copied from the output of `date -u +%Y-%m-%dT%H:%M:%SZ`, never typed from memory.

## Phase 1: Prepare the override

## Task 1: Write the one-off override script and record the before state

Create the file `.dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/override-upstream-null.js` with the script text taken verbatim from the section "One-off script (from REPORT.md Proposed Fix)" of ./source.md. Then write `./artifacts/t1-before.txt` with a UTC timestamp from `date -u` and these items in this order. First, whether each of the environment variables ORCA_PAIRING_CODE, ORCA_REMOTE_PAIRING and ORCA_ENVIRONMENT is set or unset (test with `${VAR+set}` so an empty value counts as set; never print a value). Second, only when all three are unset, the before readings: the projectId printed by `orca worktree current --json`; the `upstream`, `gitRemoteIdentity` and `repoIcon` (type and source) fields printed by `orca repo show --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json`; and the id of every worktree printed by `orca worktree list --json`. When any variable is set, run no `orca` command and say so. Third, whether the file `~/.config/orca/profiles/local-default/orca-data.json.sqlite-export.1.json` exists and holds an `upstream` object for the repo with id e8e07d51-c261-4936-815e-06aeceeb5bf8 (the rollback record). Fourth, the output of `node --version`. The last line of the file is `pre-conditions: pass` when all three variables are unset, the rollback record is present, node is available, the projectId reads github:superclaude-org/superclaude_framework and the stored upstream is the SuperClaude-Org/SuperClaude_Framework object; otherwise it is `pre-conditions: fail (` followed by each failed item and the value observed for it, followed by `)`. Use only read-only commands with no link flag.

Acceptance criteria:
- The script file exists at the path above, contains a single `repo.update` call whose updates object holds only `upstream: null`, and contains no link flag, no marker logic and no other update field.
- `./artifacts/t1-before.txt` records each of the three environment variables as set or unset (no value printed), the rollback record as present or absent, node as available or missing, a UTC timestamp from `date -u`, and ends with a line that is exactly `pre-conditions: pass` or starts with `pre-conditions: fail (`; the line agrees with the items recorded above it.
- When all three variables are unset, the file also holds the before readings (projectId, upstream, gitRemoteIdentity, repoIcon type and source, and the id of every listed worktree) exactly as the commands printed them; when any variable is set, the file says that no `orca` command was run.
- No Orca state was changed by this task: every `orca` command it ran is a read (`worktree current`, `repo show`, `worktree list`), none carries a link flag, and the once-only marker file `.dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/override-upstream-null.called` does not exist after the task.

## Phase 2: Apply the override and observe

## Task 2: Run the override once and record the outcome

Depends on: Task 1

Read `./artifacts/t1-before.txt` and choose exactly one of three paths, in this order.

- Path earlier-call: the marker file `.dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/override-upstream-null.called` already exists, so an earlier attempt of this task may already have sent the call. Do not run the script. If the three environment variables are still unset, take the after readings; otherwise take none.
- Path run: the marker does not exist and the last line of `./artifacts/t1-before.txt` is `pre-conditions: pass`. Confirm again that the three environment variables are unset. Write the marker file with one line, a UTC timestamp from `date -u`, and only then run the script `.dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/override-upstream-null.js` once with `node`, with no retry, and capture its standard output and error. Then take the after readings.
- Path stopped: the marker does not exist and the last line of `./artifacts/t1-before.txt` starts with `pre-conditions: fail (`. Do not write the marker, run no script and run no `orca` command.

The after readings repeat the readings of Task 1: the projectId from `orca worktree current --json`; `upstream`, `gitRemoteIdentity` and `repoIcon` from `orca repo show --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json`; the id of every worktree from `orca worktree list --json`; and whether `orca repo list` still lists the repo with that id. Write `./artifacts/t2-after.txt` with a UTC timestamp from `date -u`, the path taken, the exact commands run, and: on path run, the script's result reduced to success or failure with its error text and, from its response, only the `upstream`, `gitRemoteIdentity` and `repoIcon` fields (the rest of the response is not saved); on path earlier-call, the marker's own timestamp and a line that the script output is not available; on every path but stopped, the after readings and a line `worktrees preserved: yes` when every worktree id listed in `./artifacts/t1-before.txt` is still listed, otherwise `worktrees preserved: no` with the missing ids; on path stopped, the failed pre-conditions copied from `./artifacts/t1-before.txt` and no readings.

Write `./artifacts/t2-outcome.md`. Its first line is exactly one of these three, chosen by this rule. `outcome: effective` when the after readings show upstream null and projectId github:ironbellyorg/ironclaude and the script, if it ran, did not report a failure. `outcome: not-applied` when the path is stopped, or the path is earlier-call and the readings show the upstream unchanged, or the script reported a failure and the readings show the upstream unchanged. `outcome: applied-not-effective` for every other combination, including readings that still show the upstream after a call that reported success, an upstream that reads missing instead of null, a script that reported a failure while the readings show the change landed, and a reading that failed; for these, quote the raw readings and the script error. Later lines state the path taken; that Orca was not restarted and the repo's Settings panel was not opened; that durability across a restart and after opening that panel is unverified; the two checks the owner should make (restart Orca and open the repo's Settings panel, then read the two states again); the rollback: the same `repo.update` call with `updates: { upstream: { owner: 'SuperClaude-Org', repo: 'SuperClaude_Framework' } }`, and the rollback record path `~/.config/orca/profiles/local-default/orca-data.json.sqlite-export.1.json`. When the outcome is `not-applied` on path stopped, add a line that the override was not tried, that the failed pre-condition is fixed first and the override then tried, and that the decided fallback of changing Orca applies only if the override then does not hold. When the outcome is any other value but `effective`, add a line that the decided fallback is to change Orca and that the repo-icon change needs the owner's approval.

Acceptance criteria:
- `./artifacts/t2-after.txt` names exactly one path. On path run, the script command appears once, after the marker was written, and the marker file exists after the task; on paths earlier-call and stopped, no command in the file runs the script. Across every attempt the script has been started at most once.
- `./artifacts/t2-after.txt` lists every command that was run, and none carries a link flag (`--issue`, `--pr` or similar), a worktree creation or a git remote change.
- On paths run and earlier-call with the variables unset, `./artifacts/t2-after.txt` holds the after readings and the `worktrees preserved:` line, and the first line of `./artifacts/t2-outcome.md` is exactly one of the three outcome values and agrees with those readings by the rule above; on path run it also holds the reduced script result, and no part of the response beyond the three named fields is saved.
- On path stopped, `./artifacts/t2-after.txt` holds the failed pre-conditions and the timestamp, no `orca` command and no script were run, and the first line of `./artifacts/t2-outcome.md` is `outcome: not-applied`. This path passes this task: a stop is a reported finding for the owner, not a failure of the plan.
- `./artifacts/t2-outcome.md` states that no Orca restart and no Settings panel opening took place, names the two owner checks, and gives the rollback call and the rollback record path.
- On paths run and earlier-call with the variables unset, `orca worktree current --json` still answers and `orca repo list` still lists the repo with id e8e07d51-c261-4936-815e-06aeceeb5bf8.
- If the outcome is not `effective`, the tracked source files are unchanged by this task and the reason is written in `./artifacts/t2-outcome.md`.

## Phase 3: Record the result in the repository

## Task 3: Rewrite the Orca paragraph of CLAUDE.md

Depends on: Task 2

Before editing, write the baseline: run `npx --yes markdownlint-cli@0.38.0 CLAUDE.md` (no `--fix`) and save its exit status and output to `./artifacts/t3-lint-before.txt`, and run `make verify-sync` and save its exit status and output to `./artifacts/t3-verify-sync-before.txt`. Then edit only the paragraph of CLAUDE.md that begins `**Orca:**` (line 54, inside the section "ABSOLUTE RULE: PR Target = Fork"). Replace the sentence that says the source of the id is unverified (possibly the upstream URLs in pyproject.toml or package.json) with the verified cause: Orca derives the project id from the upstream field stored in its repo record before it looks at the git remote, the stored value equals the fork's GitHub parent, and pyproject.toml and package.json are not read. Then state the observed result by the first line of `./artifacts/t2-outcome.md`. For `outcome: effective`, give the new id github:ironbellyorg/ironclaude and the UTC date (`YYYY-MM-DD`) taken from the timestamp line of `./artifacts/t2-after.txt`, keep the existing statement of the earlier reading dated 2026-11-02 as its own dated statement, and say that durability across an Orca restart and after opening the repo's Settings panel is not verified. For any other outcome, say only the verified cause and what the readings showed (quoted from `./artifacts/t2-after.txt`, or that no reading was taken on path stopped), and make no claim that the id was corrected. Keep the rule that Orca link flags (`--issue`, `--pr` and others) are never passed for this repo, now worded as holding until the owner agrees to lift the ban (a corrected id alone does not lift it). Do not touch the section "Parallel Development with Git Worktrees": tests/core/test_claude_md_worktree_rule.py pins text there. The static fixtures tests/sweep/fixtures/captured-worktree-current.json and tests/sweep/fixtures/captured-worktree-list.json keep the old id as history and are not edited. After the edit, repeat the lint and `make verify-sync` runs into `./artifacts/t3-lint-after.txt` and `./artifacts/t3-verify-sync-after.txt`.

Acceptance criteria:
- The paragraph still begins with `**Orca:**`, names the verified cause (stored upstream read before the git remote; pyproject.toml and package.json not read), and no longer contains the phrase "possibly the upstream URLs in".
- The paragraph's result statement matches the first line of `./artifacts/t2-outcome.md`. For `effective` it carries the new id and a date equal to the date part of the timestamp line of `./artifacts/t2-after.txt`, and the 2026-11-02 reading stays a separate dated statement. For any other outcome it makes no claim that the id was corrected.
- The sentence that Orca link flags are never passed for this repo is kept and says the ban holds until the owner agrees to lift it.
- `git diff --stat` shows CLAUDE.md as the only tracked file changed by this task, and `git diff` for CLAUDE.md touches only the Orca paragraph.
- `./artifacts/t3-lint-after.txt` shows the same exit status and no finding that `./artifacts/t3-lint-before.txt` does not also show, and the lint was run without `--fix`.
- `./artifacts/t3-verify-sync-after.txt` shows the same exit status and the same output as `./artifacts/t3-verify-sync-before.txt` (the edit touches no file under src/superclaude or .claude; a pre-existing drift in this checkout is not caused by it).
- `uv run pytest tests/core/test_claude_md_worktree_rule.py tests/core/test_claude_md_routing_block.py tests/core/test_orca_session_launch_guidance.py tests/core/test_default_branch_agreement.py tests/core/test_research_routing_rule.py tests/core/test_how_we_work_routing_table.py -q` passes, and no Python file was edited.

## Phase 4: Hand over for the pull request

## Task 4: Write the pull request note with the identity evidence

Depends on: Task 3

Write `./artifacts/t4-pr-note.md`, the text the pull request description is made from. It holds these labelled parts: the outcome (the first line of `./artifacts/t2-outcome.md` with one sentence of meaning, and the path taken); the evidence (the before and after readings copied from `./artifacts/t1-before.txt` and `./artifacts/t2-after.txt`, or, on path stopped, the before readings and the recorded stop); the owner checks that remain (restart Orca and open the repo's Settings panel, then read `orca repo show --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json` and `orca worktree current --json` again, expecting upstream null and project id github:ironbellyorg/ironclaude); the fallback (on path stopped, fix the failed pre-condition and try the override, and only if it then does not hold change Orca; otherwise, if the id reverts, the next try is the second state change that also replaces the repo icon, which needs the owner's approval, then changing Orca); a line that issue 769 (trimming the CLAUDE.md startup context) also touches the same paragraph and asks for fresh identity evidence, which this note supplies; the rollback call and record path from `./artifacts/t2-outcome.md`; and the keyword line, which says to write `Refs #780` and not `Fixes #780`, because durability is unverified and the link-flag ban stays until the owner agrees to lift it. The note also carries the decided route word for word: Question: Change Orca so origin wins, or override the stored upstream once? Decided: Try the one-time override first; if it does not hold, change Orca. The last part, labelled `Pull request body`, is the exact text to pass as the `--body` of `/sc:pr-submit`: the outcome line, the decided route sentence, the evidence, the owner checks, the fallback, the issue 769 line and the keyword line. The note also says that the folder `.dev/troubleshoot/` (script and marker) is not staged.

Acceptance criteria:
- `./artifacts/t4-pr-note.md` exists and holds the outcome, the before and after readings, the owner checks, the fallback, the issue 769 line, the rollback and the keyword line, each as its own labelled part, and ends with the part labelled `Pull request body`.
- The decided route sentence appears in the note word for word as written in this task, and again inside the `Pull request body` part.
- The readings in the note equal the readings in `./artifacts/t1-before.txt` and `./artifacts/t2-after.txt`, and the note makes no claim of durability.
- The note's keyword line says `Refs #780`, and the note names what is left (the two owner checks and the lifting of the link-flag ban).
- `git status --short .dev/troubleshoot/` shows the folder as untracked (`??`) and no path under it as staged.
