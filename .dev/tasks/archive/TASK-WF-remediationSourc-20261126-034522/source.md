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
