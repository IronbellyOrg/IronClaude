# Pull request note for issue 780 (Orca project id of this repository)

Source readings: ./artifacts/t1-before.txt and ./artifacts/t2-after.txt. This note carries only a count of this repository's worktrees and the `worktrees preserved:` line, never worktree ids. The folder `.dev/troubleshoot/` (the one-off script and its once-only marker) is not staged and is not part of the pull request.

## Outcome

`outcome: applied-not-effective` (path taken: run). The one `repo.update` call that stores upstream null for this repository was sent once and reported success, and the stored upstream now reads null. The project id in `orca worktree current --json` still reads `github:superclaude-org/superclaude_framework`, right after the call (2026-11-26T12:13:09Z) and about 27 seconds later (2026-11-26T12:13:36Z). So the override did not correct the id as far as these readings show.

## Decided route

Question: Change Orca so origin wins, or override the stored upstream once? Decided: Try the one-time override first; if it does not hold, change Orca.

## Evidence

Before the call (2026-11-26T12:10:36Z):

```text
projectId: github:superclaude-org/superclaude_framework
{
  "upstream": {
    "owner": "SuperClaude-Org",
    "repo": "SuperClaude_Framework",
    "host": "github.com"
  },
  "gitRemoteIdentity": {
    "canonicalKey": "github.com/IronbellyOrg/IronClaude",
    "remoteName": "origin",
    "remoteUrl": "https://github.com/IronbellyOrg/IronClaude"
  },
  "repoIcon": {
    "type": "image",
    "source": "github"
  }
}
worktrees of this repository: 32 (count only)
```

After the call (2026-11-26T12:13:09Z):

```text
orca worktree current --json answered: true
orca repo list listed the repo with id e8e07d51-c261-4936-815e-06aeceeb5bf8: yes
projectId: github:superclaude-org/superclaude_framework
repo show: {"upstream":null,"gitRemoteIdentity":{"canonicalKey":"github.com/IronbellyOrg/IronClaude","remoteName":"origin","remoteUrl":"https://github.com/IronbellyOrg/IronClaude"},"repoIcon":{"type":"image","source":"github"}}
worktrees of this repository: 32 (count only)
worktrees preserved: yes
```

Extra read-only reading (2026-11-26T12:13:36Z): projectId `github:superclaude-org/superclaude_framework`, upstream null.

## Owner checks that remain

Restart Orca and open the repo's Settings panel (the agent did neither), then read `orca repo show --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json` and `orca worktree current --json` again, expecting upstream null and project id `github:ironbellyorg/ironclaude`. Durability across a restart and after opening the Settings panel is unverified, and so is whether the id is only recomputed after a restart.

## Fallback

If the id still shows the upstream, or reverts, the next try is the second state change that also replaces the repo icon, which needs the owner's approval, then changing Orca so the fork's own git remote wins. The decided fallback of changing Orca applies because the override did not correct the id in these readings.

## Issue 769

Issue 769 (trimming the CLAUDE.md startup context) also touches the same Orca paragraph in CLAUDE.md and asks for fresh identity evidence. The Evidence part above supplies it: the stored upstream before (SuperClaude-Org/SuperClaude_Framework) and after (null), and the project id before and after (unchanged).

## Rollback

Send the same `repo.update` call with `updates: { upstream: { owner: 'SuperClaude-Org', repo: 'SuperClaude_Framework' } }`. The previous record is kept in `~/.config/orca/profiles/local-default/orca-data.json.sqlite-export.1.json`.

## Keyword line

Write `Refs #780` and not `Fixes #780`, because durability is unverified, the id is not shown to be corrected, and the link-flag ban stays until the owner agrees to lift it. What is left: the two owner checks above (restart Orca; open the repo's Settings panel and read the two states again) and the lifting of the link-flag ban.

## Pull request body

Outcome: `outcome: applied-not-effective`. The one-time override stored upstream null for this repository and the stored upstream now reads null, but `orca worktree current --json` still shows project id `github:superclaude-org/superclaude_framework` right after the call and 27 seconds later. The change in this pull request is the Orca paragraph of CLAUDE.md, which now states the verified cause and this result without claiming the id was corrected.

Decided for this work: Question: Change Orca so origin wins, or override the stored upstream once? Decided: Try the one-time override first; if it does not hold, change Orca.

Evidence, before the call (2026-11-26T12:10:36Z):

```text
projectId: github:superclaude-org/superclaude_framework
{
  "upstream": {
    "owner": "SuperClaude-Org",
    "repo": "SuperClaude_Framework",
    "host": "github.com"
  },
  "gitRemoteIdentity": {
    "canonicalKey": "github.com/IronbellyOrg/IronClaude",
    "remoteName": "origin",
    "remoteUrl": "https://github.com/IronbellyOrg/IronClaude"
  },
  "repoIcon": {
    "type": "image",
    "source": "github"
  }
}
worktrees of this repository: 32 (count only)
```

Evidence, after the call (2026-11-26T12:13:09Z):

```text
orca worktree current --json answered: true
orca repo list listed the repo with id e8e07d51-c261-4936-815e-06aeceeb5bf8: yes
projectId: github:superclaude-org/superclaude_framework
repo show: {"upstream":null,"gitRemoteIdentity":{"canonicalKey":"github.com/IronbellyOrg/IronClaude","remoteName":"origin","remoteUrl":"https://github.com/IronbellyOrg/IronClaude"},"repoIcon":{"type":"image","source":"github"}}
worktrees of this repository: 32 (count only)
worktrees preserved: yes
```

Extra read-only reading (2026-11-26T12:13:36Z): projectId `github:superclaude-org/superclaude_framework`, upstream null.

Owner checks that remain: restart Orca and open the repo's Settings panel, then read `orca repo show --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json` and `orca worktree current --json` again, expecting upstream null and project id `github:ironbellyorg/ironclaude`. Durability is unverified.

Fallback: if the id still shows the upstream, or reverts, the next try is the second state change that also replaces the repo icon (needs the owner's approval), then changing Orca so the fork's git remote wins. Rollback: the same `repo.update` call with the upstream object `SuperClaude-Org/SuperClaude_Framework`.

Issue 769 (trimming the CLAUDE.md startup context) also touches the same Orca paragraph and asks for fresh identity evidence; the evidence above is that evidence.

Refs #780 (not Fixes): the id is not shown to be corrected, durability is unverified, and the Orca link-flag ban stays until the owner agrees to lift it.
