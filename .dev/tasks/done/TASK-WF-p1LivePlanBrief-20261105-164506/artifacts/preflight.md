# Preflight (Task 1)

Run in /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1 at 2026-11-05T18:49:42Z

## ORCA_TERMINAL_HANDLE is set
```
$ bash -c echo "$ORCA_TERMINAL_HANDLE"
term_558daf54-f38b-4498-b0d1-0d2e8c036e7c
rc=0
```
- ORCA_TERMINAL_HANDLE is set: PASS

## git rev-parse HEAD (saved to branch-tip.txt)
```
$ git rev-parse HEAD
0b44374513780b69f59d9018c06cbf0b4af420ad
rc=0
```
- git rev-parse HEAD (saved to branch-tip.txt): PASS

## branch is ironbelly/OrcaCLICommandRefactor-P1
```
$ git branch --show-current
ironbelly/OrcaCLICommandRefactor-P1
rc=0
```
- branch is ironbelly/OrcaCLICommandRefactor-P1: PASS

## refs/heads tip equals HEAD
```
$ git rev-parse refs/heads/ironbelly/OrcaCLICommandRefactor-P1
0b44374513780b69f59d9018c06cbf0b4af420ad
rc=0
```
- refs/heads tip equals HEAD: PASS

## 7127c247 is an ancestor of HEAD
```
$ git merge-base --is-ancestor 7127c2478756c9444afc600af3e3066b3f7f24db HEAD

rc=0
```
- 7127c247 is an ancestor of HEAD: PASS

## clean tracked tree under src plugins tests
```
$ git status --porcelain -- src plugins tests

rc=0
```
- clean tracked tree under src plugins tests: PASS

## orca --version
```
$ cat .dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/orca-version.txt
1.4.245-aidev02.dfe1eb410300
rc=0
```
- orca --version: PASS

## origin remote
```
$ git remote get-url origin
https://github.com/IronbellyOrg/IronClaude
rc=0
```
- origin remote: PASS

## AC-C6 nestedWorkerMaxDepth
```
$ bash -c grep -ho "\"nestedWorkerMaxDepth\":[0-9]*" "${ORCA_RUNTIME_SOURCE_PROFILE_PATH:-$HOME/.config/orca}"/profiles/*/orca-data.json
"nestedWorkerMaxDepth":1
rc=0
```
- AC-C6 nestedWorkerMaxDepth: PASS

## orca status
```
$ orca status --json
{
  "id": "local-status",
  "ok": true,
  "result": {
    "target": {
      "kind": "local"
    },
    "app": {
      "running": true,
      "pid": 343,
      "desktopWindowStatus": "openable"
    },
    "runtime": {
      "state": "ready",
      "reachable": true,
      "connectionState": "connected",
      "runtimeId": "f03c04aa-bfec-42ed-aad0-6d0e9c1cc7bc",
      "appVersion": "1.4.245-aidev02.dfe1eb410300",
      "remoteUpdateSupport": {
        "installMode": "unsupported-headless-serve",
        "automatic": false,
        "reason": "manual-service-update-required"
      },
      "capabilities": [
        "agent-session.saved-resume-origin.v1",
        "runtime.status.compat.v1",
        "runtime.environments.v1",
        "remote-runtime.shared-control.v1",
        "runtime.automatic-work.v1",
        "updater.remote-control.v1",
        "managed-runtime.install.v1",
        "managed-runtime.remove.v1",
        "runtime-source-fence.v1",
        "ssh.target-management.v1",
        "pairing.device-key.v1",
        "pairing.device-key-ephemeral.v1",
        "mobile.tasks.v1",
        "notifications.remote-push.v1",
        "notifications.desktop-presence.v1",
        "pairing.delegated-mobile-devices.v1",
        "mobile.desktop-relay.v1",
        "orcad.stale-lock-reclaim.v1",
        "orcad.terminal-census.v1",
        "orcad.migration-catalog.v1",
        "orcad.migration-catalog-abort-by-reference.v1",
        "accounts.host-launch-env.v1",
        "orcad.peer-desktops.v1",
        "orchestration.federation.v1",
        "orchestration.federation-control-mail.v1",
        "orchestration.federation-lifecycle-settlement.v1",
        "orchestration.worker-stop-verdict.v1",
        "orchestration.worker-launch-preferences.v1",
        "orchestration.federation-structured-read.v1",
        "orchestration.federation-fleet-snapshot.v1",
        "orchestration.federation-release-archive.v1",
        "orchestration.contract.v1",
        "agent.launch.chat-options.v1",
        "settings.agent-launch.v1",
        "settings.agent-launch.auto-permissions.v1",
        "settings.agent-launch.native-chat-permissions.v1",
        "settings.agent-permission.v1",
        "agent.launch.v2",
        "agent.launch.replay.v1",
        "agent.launch.replay-required.v1",
        "agent.launch.prompt-carry.v1",
        "agent.launch.prompt-unconfirmed.v1",
        "agent.launch.placement.v1",
        "agent.launch.local-presentation.v1",
        "agent.launch.create-folder-workspace.v1",
        "agent.launch.surface.v1",
        "agent-session.conversation-stop.v1",
        "agent-session.prompt-cancel.v1",
        "agent-session.repeated-stop.v1",
        "agent-session.send-selection.v1",
        "agent-session.send-usage-limit-continuation.v1",
        "agentSession.create.tab-id.v1",
        "agentSession.create.message.v1",
        "agentSession.create.options-mode.v1",
        "agentSession.create.tab-placement.v1",
        "agent-session.send-options.v1",
        "agent-session.account-env.v1",
        "agent-session.send-skills.v1",
        "agent-session.resume-effort.v1",
        "agent-session.session-boundary.v1",
        "agent-session.host-authority.v1",
        "agent-session.omp-resume-path.v1",
        "agent-session.keyboard.v1",
        "agent-session.structured.v1",
        "agent-session.current-requests.v1",
        "agent-session.structured.client-launch-mode.v1",
        "agent-session.pending-send-result.v1",
        "agent-session.accepted-send.v1",
        "agent-session.send-answers-proof.v1",
        "agent-session.queued-commands.v1",
        "agent-session.queued-message-edit.v1",
        "agent-session.queued-message-reorder.v1",
        "agent-session.queued-message-image-edit.v1",
        "agent-session.queued-message-skills-edit.v1",
        "agent-session.continue-interrupted.v1",
        "agent-session.permission-modes.v1",
        "agent-session.commands-on-request.v1",
        "agent-session.permission-own.v1",
        "agent-session.coherent-model-catalog.v1",
        "agent-session.structured.hold.v1",
        "agent-session.structured.reveal.v1",
        "agent-session.structured.registered-agents.v1",
        "agent-session.structured.pi-dialogs.v1",
        "agent-session.structured.resume-history.v1",
        "agent-session.structured.resume-linked-cwd.v1",
        "agent-session.structured.cli-source.v1",
        "agent-session.model-catalog.saved-only.v1",
        "agent-session.structured.availability.v1",
        "agent-session.structured.regenerate-name.v1",
        "agent-session.structured.rename.v1",
        "agent-session.status-feed.v1",
        "agent-session.turn-completion.v1",
        "agent-session.attention-ack.v1",
        "agent-session.workspace-sleep-mark.v1",
        "agent-session.rewind.v1",
        "agent-session.rewind-recovery.v1",
        "agent-session.conversation-outline.v1",
        "agent-session.continuation-context.v1",
        "agent-session.item-detail.v1",
        "agent-session.background-task-stop.v1",
        "agent-session.question-answers.v1",
        "agent-session.attachments.v1",
        "agent-session.attachments.phone.v1",
        "agent-session.turn-item.v1",
        "agent-session.background-task-row-stop.v1",
        "agent-session.background-task-child-views.v1",
        "agent-session.kimi-resume.v1",
        "agent-session.cursor-resume.v1",
        "agent-session.opencode2-resume.v1",
        "agent-session.muse-resume.v1",
        "agent-session.dsh-resume.v1",
        "agent-session.kiro-resume.v1",
        "agent-session.hermes-resume.v1",
        "agent-session.qoder-resume.v1",
        "agent-session.qoder-cn-resume.v1",
        "agent-session.qwen-code-resume.v1",
        "agent-session.codebuddy-resume.v1",
        "agent-session.zcode-resume.v1",
        "accounts.import-host-credentials.v1",
        "accounts.claude-sign-in.v1",
        "accounts.antigravity-native.v1",
        "accounts.antigravity-chat-sign-in.v1",
        "accounts.managed-data-profiles.v1",
        "accounts.codex-reset-credit.v1",
        "accounts.usage-credentials.v1",
        "accounts.host-sign-in.v1",
        "skills.install.v1",
        "skills.install.bundle.v1",
        "skills.install-cancel.v1",
        "skills.install-progress.v1",
        "skills.install-result.v2",
        "skills.upload.v1",
        "skills.manage.v1",
        "skills.install-providers.v1",
        "skills.delete.v1",
        "skills.bundled-orca.v1",
        "skills.discover-workspace.v1",
        "automation.list-host-scope.v1",
        "automation.owner-fencing.v1",
        "automation.create-idempotency.v1",
        "automations.extra-agent-args.v1",
        "worktree.rename-error-dismiss.v1",
        "worktree.open-existing-branch.v1",
        "worktree.open-existing-branch.v2",
        "worktree.open-existing-branch.v2-request.v1",
        "project-host-setup.v1",
        "project-host-setup.host-target.v1",
        "workspace-run-context.v1",
        "worktree.provisioned-root.v1",
        "worktree.linked-work-item-context.v1",
        "worktree.linked-items.v1",
        "worktree.linked-items-delta.v1",
        "worktree.github-pr-suppression.v1",
        "repo.search-qualified-refs.v1",
        "folder-workspace.path-status.v1",
        "worktree.create-idempotency.v1",
        "worktree.archive-failure-blocking.v1",
        "worktree.visibility-defaults.v1",
        "worktree.visibility-source-defaults.v1",
        "worktree.create.client-automation-provenance.v1",
        "preflight.workspace-scoped.v1",
        "preflight.project-launch-context.v1",
        "preflight.other-runtime-refusal.v1",
        "workspace-ports.v1",
        "workspace-ports.host-scoped.v1",
        "session.tabs.qoderOwnedCreate.v1",
        "session-tabs.close-intent.v1",
        "session-tabs.close-force.v1",
        "session-tabs.close-replay-reason.v1",
        "session-tabs.authoritative-inventory.v1",
        "session-tabs.split-group-placement.v1",
        "session.tabs.chat-fork-cli.v1",
        "session-tabs.empty-worktree-answer.v1",
        "session-tabs.create-terminal-shell.v1",
        "session-tabs.move-pane-to-new-tab.v1",
        "terminal.limit-policy.v1",
        "terminal.binary-stream.v1",
        "terminal.program-status.v1",
        "terminal.multiplex.v1",
        "terminal.query-reply-input.v1",
        "terminal.prompt-delivery.v1",
        "terminal.paired-parking.v1",
        "agent-status.turn-ended-at.v1",
        "terminal.spawn-intent.v1",
        "terminal.quick-commands.v1",
        "terminal.quick-commands.long-prompts.v1",
        "terminal.quick-commands.large-lists.v1",
        "terminal.create-idempotency.v2",
        "terminal.create-shell-selection.v1",
        "terminal.split-retry.v1",
        "files.pathsExist",
        "files.resolve-terminal-path.cross-workspace.v1",
        "files.resolve-terminal-path.absolute-files.v1",
        "files.readDocPreview",
        "files.readDir.paged.v1",
        "files.write.disk-precondition.v1",
        "files.write.identical-noop.v1",
        "files.mutation-ownership.v1",
        "files.write.staged.v1",
        "files.replace-with-upload.v1",
        "browser.google-cookie-clear.v1",
        "browser.screencast.v1",
        "browser.tab-create-known-id.v1",
        "browser.clientHost.v1",
        "browser.clientHost.pageMetadata.v1",
        "browser.clientHost.automation.v1",
        "browser.clientHost.fileChannel.v1",
        "network.browserTunnel.v1",
        "network.browserTunnel.executionHosts.v1",
        "git.antigravity-configured-model.v1",
        "github.markPRReadyForReview",
        "mobile.github.markPRReadyForReview.v1",
        "gitlab.updateMR.readyForReview.v1",
        "task-source-context.v1",
        "linear.issue-attribute-filter.v1",
        "jira.transition-fields.v1",
        "jira.agent-access.v1",
        "jira.current-sprint.v1",
        "jira.user-fields.v1",
        "jira.attachment-images.v1",
        "jira.issue-summary-generation.v1",
        "jira.saved-filter-state.v1",
        "jira.issue-list-statuses.v1",
        "aiVault.v1",
        "aiVault.session-titles.v1",
        "aiVault.delete-session.v1",
        "ai-vault.chat-fork-source.v1",
        "browser.headless.v1",
        "browser.identity.v1",
        "orcad.migration-blob.v1",
        "orcad.migration-blob.terminal-restore-hints.v1",
        "orcad.migration-blob.shell-history.v1",
        "browser.certificate-trust.v1",
        "mobileWeb.bundle.v1"
      ]
    },
    "graph": {
      "state": "ready"
    }
  },
  "_meta": {
    "runtimeId": "f03c04aa-bfec-42ed-aad0-6d0e9c1cc7bc"
  }
}
rc=0
```
- orca status: PASS

## orca repo list
```
$ orca repo list --json
{
  "id": "c8b66321-532e-4997-a9af-4cf26f0ddae9",
  "ok": true,
  "result": {
    "repos": [
      {
        "id": "e1ca5238-cca0-4dce-80d7-2512a554fa93",
        "path": "/home/coder/workspaces/Coder",
        "displayName": "Coder",
        "badgeColor": "#737373",
        "addedAt": 1792855093958,
        "kind": "git",
        "externalWorktreeVisibilityLegacy": false,
        "externalWorktreeVisibility": "show",
        "repoIcon": {
          "type": "image",
          "src": "https://github.com/IronbellyOrg.png?size=64",
          "source": "github",
          "label": "IronbellyOrg/Coder"
        },
        "upstream": null,
        "gitRemoteIdentity": {
          "canonicalKey": "github.com/IronbellyOrg/Coder",
          "remoteName": "origin",
          "remoteUrl": "https://github.com/IronbellyOrg/Coder"
        },
        "gitUsername": "",
        "hookSettings": {
          "mode": "auto",
          "setupRunPolicy": "run-by-default",
          "setupAgentStartupPolicy": "start-immediately",
          "scripts": {
            "setup": "",
            "archive": ""
          }
        }
      },
      {
        "id": "de550e99-fa3c-42e2-abfe-1d092771c759",
        "path": "/home/coder/workspaces/IronClaude",
        "displayName": "IronClaude",
        "badgeColor": "#737373",
        "addedAt": 1792865736882,
        "kind": "git",
        "externalWorktreeVisibilityLegacy": false,
        "externalWorktreeVisibility": "show",
        "hookSettings": {
          "mode": "auto",
          "setupRunPolicy": "skip-by-default",
          "setupAgentStartupPolicy": "start-immediately",
          "scripts": {
            "setup": "npm install",
            "archive": ""
          },
          "commandSourcePolicy": "local-only"
        },
        "repoIcon": {
          "type": "image",
          "src": "https://github.com/IronbellyOrg.png?size=64",
          "source": "github",
          "label": "IronbellyOrg/IronClaude"
        },
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
        "gitUsername": ""
      },
      {
        "id": "2c12da7f-7b7e-4a5c-9d43-ce9369c5964a",
        "path": "/home/coder/workspaces/IronOrca",
        "displayName": "IronOrca",
        "badgeColor": "#737373",
        "addedAt": 1793112441525,
        "kind": "git",
        "externalWorktreeVisibilityLegacy": false,
        "repoIcon": {
          "type": "image",
          "src": "https://github.com/IronbellyOrg.png?size=64",
          "source": "github",
          "label": "IronbellyOrg/IronOrca"
        },
        "upstream": {
          "owner": "stablyai",
          "repo": "orca",
          "host": "github.com"
        },
        "gitRemoteIdentity": {
          "canonicalKey": "github.com/IronbellyOrg/IronOrca",
          "remoteName": "origin",
          "remoteUrl": "https://github.com/IronbellyOrg/IronOrca.git"
        },
        "gitUsername": "",
        "hookSettings": {
          "mode": "auto",
          "setupRunPolicy": "run-by-default",
          "setupAgentStartupPolicy": "start-immediately",
          "scripts": {
            "setup": "",
            "archive": ""
          }
        },
        "externalWorktreeVisibility": "hide"
      },
      {
        "id": "4daf624c-6502-4191-ab5f-ad45c1e0ac18",
        "path": "/home/coder/workspaces/Ironeye",
        "displayName": "Ironeye",
        "badgeColor": "#737373",
        "addedAt": 1793113762237,
        "kind": "git",
        "externalWorktreeVisibilityLegacy": false,
        "repoIcon": {
          "type": "image",
          "src": "https://github.com/IronbellyOrg.png?size=64",
          "source": "github",
          "label": "IronbellyOrg/Ironeye"
        },
        "upstream": null,
        "gitRemoteIdentity": {
          "canonicalKey": "github.com/IronbellyOrg/Ironeye",
          "remoteName": "origin",
          "remoteUrl": "https://github.com/IronbellyOrg/Ironeye.git"
        },
        "gitUsername": "",
        "hookSettings": {
          "mode": "auto",
          "setupRunPolicy": "run-by-default",
          "setupAgentStartupPolicy": "start-immediately",
          "scripts": {
            "setup": "",
            "archive": ""
          }
        },
        "externalWorktreeVisibility": "hide"
      },
      {
        "id": "fc2498b3-908f-405c-bd9a-ba282d320996",
        "path": "/home/coder/workspaces/Ironbrain",
        "displayName": "Ironbrain",
        "badgeColor": "#737373",
        "addedAt": 1793162549383,
        "kind": "git",
        "externalWorktreeVisibilityLegacy": false,
        "repoIcon": {
          "type": "image",
          "src": "https://github.com/IronbellyOrg.png?size=64",
          "source": "github",
          "label": "IronbellyOrg/Ironbrain"
        },
        "upstream": null,
        "gitRemoteIdentity": {
          "canonicalKey": "github.com/IronbellyOrg/Ironbrain",
          "remoteName": "origin",
          "remoteUrl": "https://github.com/IronbellyOrg/Ironbrain.git"
        },
        "gitUsername": "",
        "hookSettings": {
          "mode": "auto",
          "setupRunPolicy": "run-by-default",
          "setupAgentStartupPolicy": "start-immediately",
          "scripts": {
            "setup": "",
            "archive": ""
          }
        },
        "externalWorktreeVisibility": "hide"
      }
    ]
  },
  "_meta": {
    "runtimeId": "f03c04aa-bfec-42ed-aad0-6d0e9c1cc7bc"
  }
}
rc=0
```
- orca repo list: PASS

## Install line
merge-base master HEAD = 4eb75698d9d477ad21b515f05d470ece60497a02
compared paths: 62 ; differing: 0
```
0  src/superclaude/commands/adversarial.md  /home/coder/.claude/commands/sc/adversarial.md
0  src/superclaude/commands/agent.md  /home/coder/.claude/commands/sc/agent.md
0  src/superclaude/commands/analyze.md  /home/coder/.claude/commands/sc/analyze.md
0  src/superclaude/commands/auggie-review.md  /home/coder/.claude/commands/sc/auggie-review.md
0  src/superclaude/commands/brainstorm.md  /home/coder/.claude/commands/sc/brainstorm.md
0  src/superclaude/commands/build.md  /home/coder/.claude/commands/sc/build.md
0  src/superclaude/commands/business-panel.md  /home/coder/.claude/commands/sc/business-panel.md
0  src/superclaude/commands/cleanup-audit.md  /home/coder/.claude/commands/sc/cleanup-audit.md
0  src/superclaude/commands/cleanup.md  /home/coder/.claude/commands/sc/cleanup.md
0  src/superclaude/commands/cli-eval.md  /home/coder/.claude/commands/sc/cli-eval.md
0  src/superclaude/commands/cli-portify.md  /home/coder/.claude/commands/sc/cli-portify.md
0  src/superclaude/commands/design.md  /home/coder/.claude/commands/sc/design.md
0  src/superclaude/commands/document.md  /home/coder/.claude/commands/sc/document.md
0  src/superclaude/commands/explain.md  /home/coder/.claude/commands/sc/explain.md
0  src/superclaude/commands/git.md  /home/coder/.claude/commands/sc/git.md
0  src/superclaude/commands/graph.md  /home/coder/.claude/commands/sc/graph.md
0  src/superclaude/commands/help.md  /home/coder/.claude/commands/sc/help.md
0  src/superclaude/commands/impact.md  /home/coder/.claude/commands/sc/impact.md
0  src/superclaude/commands/implement.md  /home/coder/.claude/commands/sc/implement.md
0  src/superclaude/commands/improve.md  /home/coder/.claude/commands/sc/improve.md
0  src/superclaude/commands/index-repo.md  /home/coder/.claude/commands/sc/index-repo.md
0  src/superclaude/commands/index.md  /home/coder/.claude/commands/sc/index.md
0  src/superclaude/commands/init-lite.md  /home/coder/.claude/commands/sc/init-lite.md
0  src/superclaude/commands/issue.md  /home/coder/.claude/commands/sc/issue.md
0  src/superclaude/commands/load.md  /home/coder/.claude/commands/sc/load.md
0  src/superclaude/commands/pm.md  /home/coder/.claude/commands/sc/pm.md
0  src/superclaude/commands/post-release.md  /home/coder/.claude/commands/sc/post-release.md
0  src/superclaude/commands/pr-submit.md  /home/coder/.claude/commands/sc/pr-submit.md
0  src/superclaude/commands/recommend.md  /home/coder/.claude/commands/sc/recommend.md
0  src/superclaude/commands/reflect.md  /home/coder/.claude/commands/sc/reflect.md
0  src/superclaude/commands/release-split.md  /home/coder/.claude/commands/sc/release-split.md
0  src/superclaude/commands/research.md  /home/coder/.claude/commands/sc/research.md
0  src/superclaude/commands/review-translation.md  /home/coder/.claude/commands/sc/review-translation.md
0  src/superclaude/commands/roadmap.md  /home/coder/.claude/commands/sc/roadmap.md
0  src/superclaude/commands/save.md  /home/coder/.claude/commands/sc/save.md
0  src/superclaude/commands/spawn.md  /home/coder/.claude/commands/sc/spawn.md
0  src/superclaude/commands/spec-panel.md  /home/coder/.claude/commands/sc/spec-panel.md
0  src/superclaude/commands/swarm-wizard.md  /home/coder/.claude/commands/sc/swarm-wizard.md
0  src/superclaude/commands/task.md  /home/coder/.claude/commands/sc/task.md
0  src/superclaude/commands/tasklist.md  /home/coder/.claude/commands/sc/tasklist.md
0  src/superclaude/commands/tdd.md  /home/coder/.claude/commands/sc/tdd.md
0  src/superclaude/commands/test.md  /home/coder/.claude/commands/sc/test.md
0  src/superclaude/commands/troubleshoot.md  /home/coder/.claude/commands/sc/troubleshoot.md
0  src/superclaude/commands/validate-roadmap.md  /home/coder/.claude/commands/sc/validate-roadmap.md
0  src/superclaude/commands/validate-tests.md  /home/coder/.claude/commands/sc/validate-tests.md
0  src/superclaude/commands/workflow.md  /home/coder/.claude/commands/sc/workflow.md
0  src/superclaude/skills/ccsession-tag/README.md  /home/coder/.claude/skills/ccsession-tag/README.md
0  src/superclaude/skills/ccsession-tag/ccsession  /home/coder/.claude/skills/ccsession-tag/ccsession
0  src/superclaude/skills/ccsession-tag/ccsession-orca  /home/coder/.claude/skills/ccsession-tag/ccsession-orca
0  src/superclaude/skills/sc-adversarial-protocol/SKILL.md  /home/coder/.claude/skills/sc-adversarial-protocol/SKILL.md
0  src/superclaude/skills/sc-brainstorm-protocol/SKILL.md  /home/coder/.claude/skills/sc-brainstorm-protocol/SKILL.md
0  src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md  /home/coder/.claude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
0  src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md  /home/coder/.claude/skills/sc-cleanup-audit-protocol/SKILL.md
0  src/superclaude/skills/sc-graph-protocol/SKILL.md  /home/coder/.claude/skills/sc-graph-protocol/SKILL.md
0  src/superclaude/skills/sc-impact-protocol/SKILL.md  /home/coder/.claude/skills/sc-impact-protocol/SKILL.md
0  src/superclaude/skills/sc-init-lite-protocol/SKILL.md  /home/coder/.claude/skills/sc-init-lite-protocol/SKILL.md
0  src/superclaude/skills/sc-issue-protocol/refs/chains.md  /home/coder/.claude/skills/sc-issue-protocol/refs/chains.md
0  src/superclaude/skills/sc-issue-protocol/refs/tiers.md  /home/coder/.claude/skills/sc-issue-protocol/refs/tiers.md
0  src/superclaude/skills/sc-workflow-protocol/SKILL.md  /home/coder/.claude/skills/sc-workflow-protocol/SKILL.md
0  src/superclaude/skills/sc-workflow-protocol/refs/input-parse.md  /home/coder/.claude/skills/sc-workflow-protocol/refs/input-parse.md
0  src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md  /home/coder/.claude/skills/sc-workflow-protocol/refs/return-contract.md
0  src/superclaude/core/WORKER-CONTRACT.md  /home/coder/.claude/WORKER-CONTRACT.md
```
- Install line: PASS

run-create rc=0

## Summary
check failures (excluding install line): 0 ; install differing: 0
