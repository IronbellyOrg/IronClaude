# Remediation: Troubleshoot Report (Orca project id of this repository)

Goal: Apply the fix described in /home/coder/workspaces/worktrees/IronClaude/issue-780/.dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/REPORT.md

## Summary

Orca names this repository's project github:superclaude-org/superclaude_framework because its stored record for the repo carries upstream equal to SuperClaude-Org/SuperClaude_Framework (GitHub's fork parent), and Orca's id derivation lets a non-empty stored upstream win over the fork's own git remote. The cause is a stored field in Orca's own state, not anything in this repository (pyproject.toml and package.json are not read, and nothing under src/ consumes the id). The decided route for this work is to try a one-time override first and to change Orca only if the override does not hold. The override is a single repo.update call that stores upstream as null for this repo. The Orca command line has no verb for it, so it is sent through the app's own client class in a one-off script that is not committed. Read from the installed code, a stored null is left alone by the background backfill, but the repo's Settings panel asks GitHub again when it opens for a repo with a GitHub avatar icon, which this repo has, so the override may not be durable. The agent running this plan must not restart Orca (it hosts every running agent session) and must not open its Settings panel, so durability across a restart and a panel opening cannot be proven by this run and must be reported as unverified. The only change to this repository is the Orca paragraph in CLAUDE.md.

## Files

- CLAUDE.md (only the Orca paragraph that begins with Orca: inside the section ABSOLUTE RULE: PR Target = Fork; about line 54)
- A one-off script outside the repository, for example under the troubleshoot output directory, never staged or committed
- Files that must not change: pyproject.toml and package.json, any file under src/superclaude, the files orca-data.json and its backups, the Orca database, and any git remote

## Acceptance

- Before any change, two readings are recorded as text in the plan's notes: the projectId from orca worktree current --json and the upstream and gitRemoteIdentity from orca repo show with the selector id:e8e07d51-c261-4936-815e-06aeceeb5bf8, and the environment variables ORCA_PAIRING_CODE, ORCA_REMOTE_PAIRING and ORCA_ENVIRONMENT are confirmed unset so the call cannot reach a remote runtime.
- The rollback record is confirmed present before the change: the file orca-data.json.sqlite-export.1.json under the Orca profile directory holds the stored upstream object for this repo.
- The one-off script from the REPORT.md Proposed Fix is written outside the repository and run once. It sends repo.update for id:e8e07d51-c261-4936-815e-06aeceeb5bf8 with updates upstream null and nothing else. No Orca link flag is passed, no worktree is created, no upstream git remote is added, and the upstream repository is not contacted.
- After the call, the same two readings are repeated. If upstream reads null and projectId reads github:ironbellyorg/ironclaude, the override took effect now. If the call fails, or the readings do not change, the result is recorded as not applied or not effective and the plan stops short of the paragraph change that claims success.
- If the id reverted or never changed, the stop is a reported finding for the owner and not a failure of the plan. The decided fallback is to change Orca, and a second state change that also replaces the repo icon (REPORT.md Proposed Fix, step B) is not run without the owner's approval.
- Orca is not restarted and the repo's Settings panel is not opened by the agent. The final report states that durability across a restart and after opening the panel is unverified and names both checks for the owner.
- The Orca paragraph in CLAUDE.md is rewritten to state the verified cause (Orca derives the id from its stored upstream field before the git remote, and pyproject.toml and package.json are not read) and the observed result of the override with its date, and keeps the sentence that Orca link flags (--issue, --pr and others) are never passed for this repo until the owner agrees to lift that ban. If the override was not applied or did not take effect, the paragraph states only the verified cause and that the id still shows the upstream.
- The change is limited to the files listed under Files.
- No new lint or type errors are introduced, and the repository checks for documentation and synchronization still pass.
- The pull request notes that issue 769 (trimming the CLAUDE.md startup context) also touches this paragraph and asks for fresh identity evidence, and gives that evidence.

## References

- REPORT.md: /home/coder/workspaces/worktrees/IronClaude/issue-780/.dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/REPORT.md
- Audit log: /home/coder/workspaces/worktrees/IronClaude/issue-780/.dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/audit.log
- Hypothesis card (chosen): /home/coder/workspaces/worktrees/IronClaude/issue-780/.dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/tier1-hypothesis.md
- Observations: /home/coder/workspaces/worktrees/IronClaude/issue-780/.dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/tier1-observation.md
- Issue summary with the decided route: /home/coder/workspaces/worktrees/IronClaude/issue-780/.dev/issues/780/issue-summary.md

## One-off script (from REPORT.md Proposed Fix)

```js
// node <file>  (no link flags; touches no remote)
const { RuntimeClient } = require('/opt/Orca/resources/app.asar.unpacked/out/cli/runtime-client.js');
(async () => {
  const c = new RuntimeClient();
  const r = await c.call('repo.update', { repo: 'id:e8e07d51-c261-4936-815e-06aeceeb5bf8', updates: { upstream: null } });
  console.log(JSON.stringify(r));
})().catch(e => { console.error('FAILED', e && e.message); process.exit(1); });
```

## Pipeline Hardening

pipeline_hardening_verdict: not_applicable
waiver_status: none
(Downstream stages must not re-green a blocked/advisory closure — spec section 5.4.)

## Revision 1: blocking review findings to fix

A first plan for this source was reviewed and had four blocking findings. This revision replaces that plan. Fix these four, and do not repeat the Medium and Note findings that follow them. Everything above this section stays in force.

Blocking finding M-01. The plan's second task requires after readings and script output on the branch where a pre-condition failed, while the same task says to run nothing on that branch. The fourth task requires the same after readings. Both tasks then fail their own acceptance checks on a stop that this source calls not a failure of the plan. Fix: write the acceptance criteria of the second and fourth tasks per branch (script run, script not run because an earlier attempt already made the call, script not run because a pre-condition failed), so that each branch can pass. If after readings are taken on the stopped branch, they must be gated on the environment-variable check, because a set pairing variable can point the Orca command line at a remote runtime.

Blocking finding M-02. Nothing stops the second task from sending the live repo.update call a second time. When /sc:implement restarts or retries a task, it starts from the task's start snapshot and moves the failed attempt's files under the package artifacts folder away, while the first task's before-state file stays and still says every pre-condition passed. Fix: a once-only marker kept outside the package artifacts folder, which the second task writes before the call and checks first. Verified fact: the retry revert domain excludes the folder `.dev/troubleshoot/` (retry.md of the implement skill, fixed exclusion 5, line 206), so a marker file in the troubleshoot folder named in the Files section survives a retry. If the marker already exists, the task does not run the script.

Blocking finding M-03. The paragraph must carry the observed result with its date, and the third task says to give the date, but no acceptance criterion checks it and nothing says where the date comes from. Fix: an acceptance criterion that the result sentence carries the UTC date taken from the timestamp line of the after-readings file, and that this date is distinct from the older date 2026-11-02 already in the paragraph.

Blocking finding M-04. This source requires no new lint errors and passing documentation and synchronization checks, but the plan runs only five test files and no markdown lint. Three of those five read the packaged copy src/superclaude/core/CLAUDE.md, not the root CLAUDE.md that is edited. Fix: add the sixth test file tests/core/test_how_we_work_routing_table.py, which reads the root CLAUDE.md, and add a markdown lint run in a non-fixing mode with a baseline taken before the edit. Verified facts from this checkout: the lint command `npx --yes markdownlint-cli@0.38.0 CLAUDE.md` (the version the repository's pre-commit configuration pins, run without the --fix option because the hook's --fix could rewrite lines outside the Orca paragraph) exits 0 with no findings on the unedited file; the six test files give 80 passed on the unedited file; `make verify-sync` reads only src/superclaude and .claude, never the root CLAUDE.md, and already exits non-zero in this checkout because of drift that has nothing to do with this work, so the check is that its exit status and output are the same before and after the edit, and CI runs it on the pull request in a clean checkout.

Medium and Note findings from the same review. These were counted toward the route and the new plan should not repeat them.

- The three outcome values must cover every state. Add one catch-all rule: a call that reported failure while the readings show the change landed, an upstream that reads missing rather than null, or a reading that failed after the call is recorded as applied-not-effective with the raw readings and the script error quoted. The third task then states only the verified cause and what the readings showed, without claiming the id was corrected.
- The script and its once-only marker are never staged or committed (the spec says never staged or committed, the first plan said only not added to any commit). The staged file list is checked.
- The live call needs no approval stop (the story sets plan approval to no), but after the call the plan checks that every worktree listed by `orca worktree list --json` before is still listed, and the outcome file carries the rollback call and the path of the rollback record.
- The second task's gate rechecks the before values: the projectId is github:superclaude-org/superclaude_framework and the stored upstream is the SuperClaude-Org/SuperClaude_Framework object. A different before value means the script is not run and the difference is reported.
- The fourth task's note ends with a labelled part that is the exact text to pass as the body of the pull request, so the pull request step has one thing to paste.
- When the outcome is not-applied because a pre-condition failed, the override was never tried: the note says to fix the pre-condition and try the override, and says the decided fallback of changing Orca applies only if the override then does not hold.
- Wording: say the Orca database is not edited directly (the one allowed call writes it); say the tracked source files are unchanged rather than the repository; save only the upstream, gitRemoteIdentity and repoIcon fields of the repo.update response in the evidence file, not the whole response.
