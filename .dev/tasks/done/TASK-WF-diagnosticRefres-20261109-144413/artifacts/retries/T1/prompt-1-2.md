8365c62c3b202c1af844fd81a67754e15788d65a
Review one task for spec compliance.

Task brief: ## Task 1: Capture private backup and checked source-target baselines

Implements R-001, R-002, R-003, R-005, R-006, R-007 and the pre-install part of R-010. Inspect the existing src/superclaude/cli/install_skill.py source-resolution and delete-before-copy implementation. Under the actual uv runtime record the loaded installer module path, resolved canonical sc-troubleshoot-protocol source, the explicit intended target under ~/.claude/skills, target/source realpaths and symlink safety. Record those checks, genuine authorization and verified helper model mapping in ./artifacts/authorization-and-binding.json. Assert source resolves to this checkout's src/superclaude/skills/sc-troubleshoot-protocol and target to the existing owner's sc-troubleshoot-protocol skill, never an alternate package.

Create ./artifacts/compatibility-before.json with selected source/installed file inventories (names, types, modes and SHA256), exact canonical/project closed-roster agreement, and the three expected stale files (SKILL.md, refs/doc-discovery.md, refs/diagnosability-audit.md). Include before hashes for canonical/project/global analyst profiles and existing project/global permission/settings files, digests of unrelated installed skills and all project mirrors. Record unexpected extras/drift explicitly and stop if any appears. With umask077, preserve the complete prior installed package as ./artifacts/installed-skill-before.tar.gz, mode0600, and verify archived bytes/types/modes against the inventory without extracting or executing it. Preserve the backup, do not replace an existing backup or automatically restore by hand. Run tests/troubleshoot/test_diagnostic_worker_contract.py and save ./artifacts/canonical-contract-before.log. Do not mutate installed/profile/settings/project-mirror or canonical files.

Acceptance criteria:
- T1.AC1: R-001, R-002, R-003, R-005: recorded actual runtime source/target binding and realpath checks match the approved checkout and owner target; authorization and explicit Tier1b mapping are preserved; canonical/active closed rosters match without changed tools or weakened gates.
- T1.AC2: R-006, R-007: complete inventories and all invariance baselines exist; only the exact three expected stale skill files differ, no unexpected extras/unsafe paths; complete private0600 backup verifies bytes/types/modes before any deletion. Any failed prerequisite is a blocker, not an assumed pass.
- T1.AC3: R-010: focused canonical contract/install tests pass with actual output. No install or unrelated mutation occurred; earlier failed reports/plan/check and0.80 score remain unchanged.
Global constraints: ## Constraints

- R-001, R-002, R-003: genuine owner authorization is coordinator msg_fbc81030bd4f, scoped to compatibility only. Every helper uses explicit verified sonnet/Tier1b (claude-gw-tier1b[1m]); no Opus/fork/other-tier fallback. Preserve all prior failed diagnostics, their0.80 cap, and the first unexecuted plan/check unchanged.
- R-003, R-004: canonical source/profile already agree; change no canonical source, agent profile, tool capability, permission/settings file or gate. Use no full installer/update, hand-edited installed primitive, global-agent substitute, project-mirror write or make sync-dev. Only the existing selective skill installer can replace the approved installed target. Unexpected canonical gap or drift blocks this plan.
- R-001, R-010, R-011, R-012: no reader repair, PR fix commit/push, extra review allowance, experiments, huge files, benchmark, merge or issue closure. Codex remains optional, not a gate waiver for confirmed code/CI findings.
- R-007, R-012: evidence belongs in ./artifacts; private backup outside installed primitive directories, archive0600 under umask077. Preserve all old evidence. Stage .dev/tasks, never .claude mirrors. Do not claim projected tests/smoke or an earlier failed check passed.
Start sha: 8365c62c3b202c1af844fd81a67754e15788d65a
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/authorization-and-binding.json b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/authorization-and-binding.json
new file mode 100644
index 000000000..6150fdd07
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/authorization-and-binding.json
@@ -0,0 +1,71 @@
+{
+  "owner_message": "msg_fbc81030bd4f",
+  "owner_provenance": "2026-11-09T14:12UTC direct genuine owner message relayed by coordinator:441 pr469 authorized; checked compatibility only",
+  "scope": "No permissions/profile/tool/gate broadening; normal one-skill installer; old failures/caps preserved; no merge/closure",
+  "owner_decision_A": {
+    "decision": "A: mode-only exception for the 19 install-skill entries AUTHORIZED",
+    "source": "owner reply '1' at 2026-11-10T00:02Z, relayed by the coordinator",
+    "verbatim": "(A) AUTHORIZED: the mode-only exception for the 19 install-skill entries (2 directories, 17 refs files; source 700/600 vs installed 755/644; the install makes installed copies stricter). It covers ONLY those 19 entries and ONLY mode differences. Any other drift, any content-hash difference, or any mode difference that loosens permissions = STOP and report.",
+    "count_note": "The recorded entry set is 3 directories (., refs, refs/probe-packs) and 16 files; the total of 19 and the mode pairs match the wording.",
+    "entries": [
+      ".",
+      "refs",
+      "refs/agent-assertions.md",
+      "refs/calibrator-eval-cases.md",
+      "refs/contract-enumeration.md",
+      "refs/effective-input-proof.md",
+      "refs/environment-deltas.md",
+      "refs/escalation-rubric.md",
+      "refs/hardening-output-contract.md",
+      "refs/hypothesis-card-template.md",
+      "refs/pipeline-hardening-closure.md",
+      "refs/primitive-differential.md",
+      "refs/probe-packs",
+      "refs/probe-packs/read-parse.md",
+      "refs/remediation-handoff.md",
+      "refs/report-template.md",
+      "refs/runtime-entrypoint-verification.md",
+      "refs/triage-checklist.md",
+      "refs/unmask-and-sweep.md"
+    ]
+  },
+  "owner_decision_B": {
+    "decision": "B: settings.json rebaseline stays approved with conditions",
+    "source": "owner reply '1' at 2026-11-10T00:02Z, relayed by the coordinator",
+    "provenance": "owner ran /model in the coordinator session on 2026-11-09 ~19:38Z; the default model changed and was saved; setup-bmad is an unrelated tooling skill"
+  },
+  "binding": {
+    "module": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/cli/install_skill.py",
+    "module_state": {
+      "kind": "file",
+      "mode": 384,
+      "size": 4197,
+      "sha256": "dba905ac3d3e7407f380146ada15cffa957d174e3371a5140a1fc2d06e3537c8"
+    },
+    "source": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-troubleshoot-protocol",
+    "target": "/home/coder/.claude/skills/sc-troubleshoot-protocol",
+    "source_realpath": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-troubleshoot-protocol",
+    "target_realpath": "/home/coder/.claude/skills/sc-troubleshoot-protocol",
+    "model_alias": "sonnet",
+    "model_mapping": "claude-gw-tier1b[1m]"
+  },
+  "source_target_verified": true,
+  "profile_roster": [
+    "Glob",
+    "Grep",
+    "Read",
+    "mcp__auggie__codebase-retrieval",
+    "mcp__codegraph__codegraph_callers",
+    "mcp__codegraph__codegraph_impact",
+    "mcp__codegraph__codegraph_node",
+    "mcp__codegraph__codegraph_search",
+    "mcp__litellm__augment_code-augment_code_search"
+  ],
+  "backup": {
+    "path": "./artifacts/installed-skill-before.tar.gz",
+    "kind": "file",
+    "mode": 384,
+    "size": 106556,
+    "sha256": "77e304762480a13a83589c62f3ca1dc8ddf8cd4ab3b0b0afc7920ec2341a3707"
+  }
+}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/authorization-and-binding.prev.json b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/authorization-and-binding.prev.json
new file mode 100644
index 000000000..592096709
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/authorization-and-binding.prev.json
@@ -0,0 +1,39 @@
+{
+  "owner_message": "msg_fbc81030bd4f",
+  "owner_provenance": "2026-11-09T14:12UTC direct genuine owner message relayed by coordinator:441 pr469 authorized; checked compatibility only",
+  "scope": "No permissions/profile/tool/gate broadening; normal one-skill installer; old failures/caps preserved; no merge/closure",
+  "binding": {
+    "module": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/cli/install_skill.py",
+    "module_state": {
+      "kind": "file",
+      "mode": 384,
+      "size": 4197,
+      "sha256": "dba905ac3d3e7407f380146ada15cffa957d174e3371a5140a1fc2d06e3537c8"
+    },
+    "source": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-troubleshoot-protocol",
+    "target": "/home/coder/.claude/skills/sc-troubleshoot-protocol",
+    "source_realpath": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-troubleshoot-protocol",
+    "target_realpath": "/home/coder/.claude/skills/sc-troubleshoot-protocol",
+    "model_alias": "sonnet",
+    "model_mapping": "claude-gw-tier1b[1m]"
+  },
+  "source_target_verified": true,
+  "profile_roster": [
+    "Glob",
+    "Grep",
+    "Read",
+    "mcp__auggie__codebase-retrieval",
+    "mcp__codegraph__codegraph_callers",
+    "mcp__codegraph__codegraph_impact",
+    "mcp__codegraph__codegraph_node",
+    "mcp__codegraph__codegraph_search",
+    "mcp__litellm__augment_code-augment_code_search"
+  ],
+  "backup": {
+    "path": "./artifacts/installed-skill-before.tar.gz",
+    "kind": "file",
+    "mode": 384,
+    "size": 106556,
+    "sha256": "77e304762480a13a83589c62f3ca1dc8ddf8cd4ab3b0b0afc7920ec2341a3707"
+  }
+}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/backup-and-inventory-corrected.log b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/backup-and-inventory-corrected.log
new file mode 100644
index 000000000..1b9228731
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/backup-and-inventory-corrected.log
@@ -0,0 +1 @@
+{"phase": "before", "drift": ["SKILL.md", "refs/diagnosability-audit.md", "refs/doc-discovery.md"], "backup_verified": true, "archive_mode": "0600", "file_entries": 22, "profiles_settings_unchanged": true}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/backup-and-inventory.log b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/backup-and-inventory.log
new file mode 100644
index 000000000..6477bae57
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/backup-and-inventory.log
@@ -0,0 +1,5 @@
+Traceback (most recent call last):
+  File "/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py", line 91, in <module>
+    assert drift==EXPECTED_DRIFT,drift
+           ^^^^^^^^^^^^^^^^^^^^^
+AssertionError: ['.', 'SKILL.md', 'refs', 'refs/agent-assertions.md', 'refs/calibrator-eval-cases.md', 'refs/contract-enumeration.md', 'refs/diagnosability-audit.md', 'refs/doc-discovery.md', 'refs/effective-input-proof.md', 'refs/environment-deltas.md', 'refs/escalation-rubric.md', 'refs/hardening-output-contract.md', 'refs/hypothesis-card-template.md', 'refs/pipeline-hardening-closure.md', 'refs/primitive-differential.md', 'refs/probe-packs', 'refs/probe-packs/read-parse.md', 'refs/remediation-handoff.md', 'refs/report-template.md', 'refs/runtime-entrypoint-verification.md', 'refs/triage-checklist.md', 'refs/unmask-and-sweep.md']
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/backup-sha256.log b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/backup-sha256.log
new file mode 100644
index 000000000..1e621fc1a
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/backup-sha256.log
@@ -0,0 +1 @@
+77e304762480a13a83589c62f3ca1dc8ddf8cd4ab3b0b0afc7920ec2341a3707  .dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/installed-skill-before.tar.gz
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/before-rerun.log b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/before-rerun.log
new file mode 100644
index 000000000..1b9228731
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/before-rerun.log
@@ -0,0 +1 @@
+{"phase": "before", "drift": ["SKILL.md", "refs/diagnosability-audit.md", "refs/doc-discovery.md"], "backup_verified": true, "archive_mode": "0600", "file_entries": 22, "profiles_settings_unchanged": true}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/blocked-before-state.json b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/blocked-before-state.json
new file mode 100644
index 000000000..86fff9bdf
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/blocked-before-state.json
@@ -0,0 +1,383 @@
+{
+  "source": {
+    ".": {
+      "kind": "dir",
+      "mode": 448
+    },
+    "SKILL.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 133005,
+      "sha256": "0dd9d33fbdf6fc398cb717bd491587e3a5e4119eaa609336c6823128479acb9a"
+    },
+    "refs": {
+      "kind": "dir",
+      "mode": 448
+    },
+    "refs/agent-assertions.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 5957,
+      "sha256": "7bcd5b7c17957a903baee9933bcffb04adebfb093163576731a37cfecf8407fa"
+    },
+    "refs/calibrator-eval-cases.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 5256,
+      "sha256": "ef705ec12e75d8d91731013bb81416c7acca36744f8a433dc4dd9e3d9d16ffba"
+    },
+    "refs/contract-enumeration.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 2831,
+      "sha256": "8cf9c1e6fe6a086cbc2055f78ae07ee8fa2815eb1cce8e6918b4d68dd0433d5e"
+    },
+    "refs/diagnosability-audit.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 38873,
+      "sha256": "e86a3a4124c359c51827bbfbe5195bbe7c9670257a5121854c0cd94be32302d1"
+    },
+    "refs/doc-discovery.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 9312,
+      "sha256": "0b9d5a38b1ac4fb0fc7c9e62846a486e3ba799990c1cb44e2ddee3daaa88d8cd"
+    },
+    "refs/effective-input-proof.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 1872,
+      "sha256": "f40412b36e13a5271bb5b426376efe2b837ff0d09c7e78c0b7ad61f19c95853c"
+    },
+    "refs/environment-deltas.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 2188,
+      "sha256": "a868fd374ec2c84981e2b7bde02334f9b75cf9f64a6b7abee9e028e63205ecff"
+    },
+    "refs/escalation-rubric.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 8058,
+      "sha256": "c72b5afc2c6b85cc979e5c071399d2c5825aae08d06e659d36c9b105b1067037"
+    },
+    "refs/hardening-output-contract.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 9819,
+      "sha256": "0a477f3addde441a0b617b909d0e1660bbb1b526dd7e5503d4d8c4731ee0faa6"
+    },
+    "refs/hypothesis-card-template.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 16316,
+      "sha256": "cfad9e91ac7816b22d1d3d5bc1c7db70c544a7a0783e63cabe0d3d0d253ee8cb"
+    },
+    "refs/pipeline-hardening-closure.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 7284,
+      "sha256": "597db5c60bc2e28f11ddd9062eb59e3180307f4b6db5a950cb69c3f9004f5625"
+    },
+    "refs/primitive-differential.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 6149,
+      "sha256": "12d8a49e5ee2749b56b822028f6676940eb57655c9852fa85273444d0c5156ce"
+    },
+    "refs/probe-packs": {
+      "kind": "dir",
+      "mode": 448
+    },
+    "refs/probe-packs/read-parse.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 632,
+      "sha256": "95f0397e7eb5f0620764ac77a475ce8b405018eb0841b42c25e19e569f993498"
+    },
+    "refs/remediation-handoff.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 16290,
+      "sha256": "aebafa75d8b1998a2e8573028cae63b7497fd25202e51afca245fb57d73610b1"
+    },
+    "refs/report-template.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 28985,
+      "sha256": "faa943d063f4078e3c9c5a5b58145fd530ed79a03a2296d6a4f23f71c838d7ce"
+    },
+    "refs/runtime-entrypoint-verification.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 3609,
+      "sha256": "d83f98cba7130cb0c61a5beda16c9d33420b22466de4c84781e886e94759a971"
+    },
+    "refs/triage-checklist.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 7584,
+      "sha256": "847c8a198ffff5818bbfedf4a7f6c21dae4b854ffcaa82223d31e6b8c4a5a19d"
+    },
+    "refs/unmask-and-sweep.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 3971,
+      "sha256": "460e1b8305242aeb085f6c426bfe2c50fbb8983050173b4d3cbde8437ebd2be8"
+    }
+  },
+  "installed": {
+    ".": {
+      "kind": "dir",
+      "mode": 493
+    },
+    "SKILL.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 131516,
+      "sha256": "6d1b226cba4c2fbe9dae7bcbbfe954ee9463a20473e4e33bdc679cda39b2f3e5"
+    },
+    "refs": {
+      "kind": "dir",
+      "mode": 493
+    },
+    "refs/agent-assertions.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5957,
+      "sha256": "7bcd5b7c17957a903baee9933bcffb04adebfb093163576731a37cfecf8407fa"
+    },
+    "refs/calibrator-eval-cases.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5256,
+      "sha256": "ef705ec12e75d8d91731013bb81416c7acca36744f8a433dc4dd9e3d9d16ffba"
+    },
+    "refs/contract-enumeration.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 2831,
+      "sha256": "8cf9c1e6fe6a086cbc2055f78ae07ee8fa2815eb1cce8e6918b4d68dd0433d5e"
+    },
+    "refs/diagnosability-audit.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 38706,
+      "sha256": "953901f262b0f4092297e03d3611e3c14cc678ed3d7072c55e604c8cd30ad944"
+    },
+    "refs/doc-discovery.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 9256,
+      "sha256": "57c0795ca5bec46c51cadf4ae02f156e3a112b2f592081921eeb4c729379e9aa"
+    },
+    "refs/effective-input-proof.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 1872,
+      "sha256": "f40412b36e13a5271bb5b426376efe2b837ff0d09c7e78c0b7ad61f19c95853c"
+    },
+    "refs/environment-deltas.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 2188,
+      "sha256": "a868fd374ec2c84981e2b7bde02334f9b75cf9f64a6b7abee9e028e63205ecff"
+    },
+    "refs/escalation-rubric.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 8058,
+      "sha256": "c72b5afc2c6b85cc979e5c071399d2c5825aae08d06e659d36c9b105b1067037"
+    },
+    "refs/hardening-output-contract.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 9819,
+      "sha256": "0a477f3addde441a0b617b909d0e1660bbb1b526dd7e5503d4d8c4731ee0faa6"
+    },
+    "refs/hypothesis-card-template.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 16316,
+      "sha256": "cfad9e91ac7816b22d1d3d5bc1c7db70c544a7a0783e63cabe0d3d0d253ee8cb"
+    },
+    "refs/pipeline-hardening-closure.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 7284,
+      "sha256": "597db5c60bc2e28f11ddd9062eb59e3180307f4b6db5a950cb69c3f9004f5625"
+    },
+    "refs/primitive-differential.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 6149,
+      "sha256": "12d8a49e5ee2749b56b822028f6676940eb57655c9852fa85273444d0c5156ce"
+    },
+    "refs/probe-packs": {
+      "kind": "dir",
+      "mode": 493
+    },
+    "refs/probe-packs/read-parse.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 632,
+      "sha256": "95f0397e7eb5f0620764ac77a475ce8b405018eb0841b42c25e19e569f993498"
+    },
+    "refs/remediation-handoff.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 16290,
+      "sha256": "aebafa75d8b1998a2e8573028cae63b7497fd25202e51afca245fb57d73610b1"
+    },
+    "refs/report-template.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 28985,
+      "sha256": "faa943d063f4078e3c9c5a5b58145fd530ed79a03a2296d6a4f23f71c838d7ce"
+    },
+    "refs/runtime-entrypoint-verification.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 3609,
+      "sha256": "d83f98cba7130cb0c61a5beda16c9d33420b22466de4c84781e886e94759a971"
+    },
+    "refs/triage-checklist.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 7584,
+      "sha256": "847c8a198ffff5818bbfedf4a7f6c21dae4b854ffcaa82223d31e6b8c4a5a19d"
+    },
+    "refs/unmask-and-sweep.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 3971,
+      "sha256": "460e1b8305242aeb085f6c426bfe2c50fbb8983050173b4d3cbde8437ebd2be8"
+    }
+  },
+  "profiles": {
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/agents/troubleshoot-analyst.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5306,
+      "sha256": "fe25f8713a400250cd2ed7387ae0c30d32e787318cb41f6034bb2f70a9767f44"
+    },
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/.claude/agents/troubleshoot-analyst.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 5306,
+      "sha256": "fe25f8713a400250cd2ed7387ae0c30d32e787318cb41f6034bb2f70a9767f44"
+    },
+    "/home/coder/.claude/agents/troubleshoot-analyst.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5258,
+      "sha256": "a952b4060db11be65b5bac546c6af3f2422615bc5cc3433179560a1d23c61213"
+    }
+  },
+  "settings": {
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/.claude/settings.json": {
+      "kind": "file",
+      "mode": 384,
+      "size": 1632,
+      "sha256": "1f535104e6bb9145585a88418d0a094a4b38d6432e3b5fbd6226d550da33d41c"
+    },
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/.claude/settings.local.json": {
+      "kind": "absent"
+    },
+    "/home/coder/.claude/settings.json": {
+      "kind": "file",
+      "mode": 420,
+      "size": 55659,
+      "sha256": "e0c2e76c60cfdd98dacdf6d751782c619875fb4c858f5037858af2e1a883f761"
+    },
+    "/home/coder/.claude/settings.local.json": {
+      "kind": "absent"
+    }
+  },
+  "other_installed_digest": "55c0781e55cedb83fa5cb02e3cdfc8a8421288bb9d3b37b56f12cca971947b77",
+  "other_installed_entries": 45,
+  "project_mirrors": {
+    "skills": "474014884b6aaea81afc9519a245c844fcebb9b7fef3e9a32246c64dae0084b0",
+    "agents": "17f317b9b649b82789e5ce1c629f79743bcb20b3c5c84f57060fe5f431ab7c71",
+    "commands": "7f3c2978d5181c7fb2071df9082046a3410fb476b64f74d6e6ec9b380b6bd2ca",
+    "hooks": "32b821fa8cbf12814d9a1717baef1e8a0eb260f9339c5af7b1b9e20f587fe767",
+    "templates": "0388b1822767a0ee29d0e3c5171aedb524a795eb23173d084c1ebb4c7cff0eda"
+  },
+  "binding": {
+    "module": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/cli/install_skill.py",
+    "module_state": {
+      "kind": "file",
+      "mode": 384,
+      "size": 4197,
+      "sha256": "dba905ac3d3e7407f380146ada15cffa957d174e3371a5140a1fc2d06e3537c8"
+    },
+    "source": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-troubleshoot-protocol",
+    "target": "/home/coder/.claude/skills/sc-troubleshoot-protocol",
+    "source_realpath": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-troubleshoot-protocol",
+    "target_realpath": "/home/coder/.claude/skills/sc-troubleshoot-protocol",
+    "model_alias": "sonnet",
+    "model_mapping": "claude-gw-tier1b[1m]"
+  },
+  "roster": [
+    "Glob",
+    "Grep",
+    "Read",
+    "mcp__auggie__codebase-retrieval",
+    "mcp__codegraph__codegraph_callers",
+    "mcp__codegraph__codegraph_impact",
+    "mcp__codegraph__codegraph_node",
+    "mcp__codegraph__codegraph_search",
+    "mcp__litellm__augment_code-augment_code_search"
+  ],
+  "observed_drift": [
+    ".",
+    "SKILL.md",
+    "refs",
+    "refs/agent-assertions.md",
+    "refs/calibrator-eval-cases.md",
+    "refs/contract-enumeration.md",
+    "refs/diagnosability-audit.md",
+    "refs/doc-discovery.md",
+    "refs/effective-input-proof.md",
+    "refs/environment-deltas.md",
+    "refs/escalation-rubric.md",
+    "refs/hardening-output-contract.md",
+    "refs/hypothesis-card-template.md",
+    "refs/pipeline-hardening-closure.md",
+    "refs/primitive-differential.md",
+    "refs/probe-packs",
+    "refs/probe-packs/read-parse.md",
+    "refs/remediation-handoff.md",
+    "refs/report-template.md",
+    "refs/runtime-entrypoint-verification.md",
+    "refs/triage-checklist.md",
+    "refs/unmask-and-sweep.md"
+  ],
+  "content_drift": [
+    "SKILL.md",
+    "refs/diagnosability-audit.md",
+    "refs/doc-discovery.md"
+  ],
+  "mode_drift": [
+    ".",
+    "refs",
+    "refs/agent-assertions.md",
+    "refs/calibrator-eval-cases.md",
+    "refs/contract-enumeration.md",
+    "refs/effective-input-proof.md",
+    "refs/environment-deltas.md",
+    "refs/escalation-rubric.md",
+    "refs/hardening-output-contract.md",
+    "refs/hypothesis-card-template.md",
+    "refs/pipeline-hardening-closure.md",
+    "refs/primitive-differential.md",
+    "refs/probe-packs",
+    "refs/probe-packs/read-parse.md",
+    "refs/remediation-handoff.md",
+    "refs/report-template.md",
+    "refs/runtime-entrypoint-verification.md",
+    "refs/triage-checklist.md",
+    "refs/unmask-and-sweep.md"
+  ]
+}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/blocked-preflight.log b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/blocked-preflight.log
new file mode 100644
index 000000000..b2cee81c5
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/blocked-preflight.log
@@ -0,0 +1,5 @@
+{"phase": "blocked_before", "content_drift": ["SKILL.md", "refs/diagnosability-audit.md", "refs/doc-discovery.md"], "mode_drift_count": 19, "examples": {".": {"source": "0o700", "installed": "0o755"}, "refs": {"source": "0o700", "installed": "0o755"}, "refs/agent-assertions.md": {"source": "0o600", "installed": "0o644"}, "refs/calibrator-eval-cases.md": {"source": "0o600", "installed": "0o644"}, "refs/contract-enumeration.md": {"source": "0o600", "installed": "0o644"}}, "installer_run": false, "backup_exists": false}
+Traceback (most recent call last):
+  File "/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py", line 98, in <module>
+    raise AssertionError('Unexpected metadata drift; preserved state, no installation')
+AssertionError: Unexpected metadata drift; preserved state, no installation
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/canonical-contract-before.log b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/canonical-contract-before.log
new file mode 100644
index 000000000..e776bae64
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/canonical-contract-before.log
@@ -0,0 +1,12 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-441
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collected 51 items
+
+tests/troubleshoot/test_diagnostic_worker_contract.py .................. [ 35%]
+.................................                                        [100%]
+
+============================== 51 passed in 0.48s ==============================
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-before.json b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-before.json
new file mode 100644
index 000000000..a1d2c89ca
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-before.json
@@ -0,0 +1,495 @@
+{
+  "source": {
+    ".": {
+      "kind": "dir",
+      "mode": 448
+    },
+    "SKILL.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 133005,
+      "sha256": "0dd9d33fbdf6fc398cb717bd491587e3a5e4119eaa609336c6823128479acb9a"
+    },
+    "refs": {
+      "kind": "dir",
+      "mode": 448
+    },
+    "refs/agent-assertions.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 5957,
+      "sha256": "7bcd5b7c17957a903baee9933bcffb04adebfb093163576731a37cfecf8407fa"
+    },
+    "refs/calibrator-eval-cases.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 5256,
+      "sha256": "ef705ec12e75d8d91731013bb81416c7acca36744f8a433dc4dd9e3d9d16ffba"
+    },
+    "refs/contract-enumeration.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 2831,
+      "sha256": "8cf9c1e6fe6a086cbc2055f78ae07ee8fa2815eb1cce8e6918b4d68dd0433d5e"
+    },
+    "refs/diagnosability-audit.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 38873,
+      "sha256": "e86a3a4124c359c51827bbfbe5195bbe7c9670257a5121854c0cd94be32302d1"
+    },
+    "refs/doc-discovery.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 9312,
+      "sha256": "0b9d5a38b1ac4fb0fc7c9e62846a486e3ba799990c1cb44e2ddee3daaa88d8cd"
+    },
+    "refs/effective-input-proof.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 1872,
+      "sha256": "f40412b36e13a5271bb5b426376efe2b837ff0d09c7e78c0b7ad61f19c95853c"
+    },
+    "refs/environment-deltas.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 2188,
+      "sha256": "a868fd374ec2c84981e2b7bde02334f9b75cf9f64a6b7abee9e028e63205ecff"
+    },
+    "refs/escalation-rubric.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 8058,
+      "sha256": "c72b5afc2c6b85cc979e5c071399d2c5825aae08d06e659d36c9b105b1067037"
+    },
+    "refs/hardening-output-contract.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 9819,
+      "sha256": "0a477f3addde441a0b617b909d0e1660bbb1b526dd7e5503d4d8c4731ee0faa6"
+    },
+    "refs/hypothesis-card-template.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 16316,
+      "sha256": "cfad9e91ac7816b22d1d3d5bc1c7db70c544a7a0783e63cabe0d3d0d253ee8cb"
+    },
+    "refs/pipeline-hardening-closure.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 7284,
+      "sha256": "597db5c60bc2e28f11ddd9062eb59e3180307f4b6db5a950cb69c3f9004f5625"
+    },
+    "refs/primitive-differential.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 6149,
+      "sha256": "12d8a49e5ee2749b56b822028f6676940eb57655c9852fa85273444d0c5156ce"
+    },
+    "refs/probe-packs": {
+      "kind": "dir",
+      "mode": 448
+    },
+    "refs/probe-packs/read-parse.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 632,
+      "sha256": "95f0397e7eb5f0620764ac77a475ce8b405018eb0841b42c25e19e569f993498"
+    },
+    "refs/remediation-handoff.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 16290,
+      "sha256": "aebafa75d8b1998a2e8573028cae63b7497fd25202e51afca245fb57d73610b1"
+    },
+    "refs/report-template.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 28985,
+      "sha256": "faa943d063f4078e3c9c5a5b58145fd530ed79a03a2296d6a4f23f71c838d7ce"
+    },
+    "refs/runtime-entrypoint-verification.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 3609,
+      "sha256": "d83f98cba7130cb0c61a5beda16c9d33420b22466de4c84781e886e94759a971"
+    },
+    "refs/triage-checklist.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 7584,
+      "sha256": "847c8a198ffff5818bbfedf4a7f6c21dae4b854ffcaa82223d31e6b8c4a5a19d"
+    },
+    "refs/unmask-and-sweep.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 3971,
+      "sha256": "460e1b8305242aeb085f6c426bfe2c50fbb8983050173b4d3cbde8437ebd2be8"
+    }
+  },
+  "installed": {
+    ".": {
+      "kind": "dir",
+      "mode": 493
+    },
+    "SKILL.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 131516,
+      "sha256": "6d1b226cba4c2fbe9dae7bcbbfe954ee9463a20473e4e33bdc679cda39b2f3e5"
+    },
+    "refs": {
+      "kind": "dir",
+      "mode": 493
+    },
+    "refs/agent-assertions.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5957,
+      "sha256": "7bcd5b7c17957a903baee9933bcffb04adebfb093163576731a37cfecf8407fa"
+    },
+    "refs/calibrator-eval-cases.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5256,
+      "sha256": "ef705ec12e75d8d91731013bb81416c7acca36744f8a433dc4dd9e3d9d16ffba"
+    },
+    "refs/contract-enumeration.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 2831,
+      "sha256": "8cf9c1e6fe6a086cbc2055f78ae07ee8fa2815eb1cce8e6918b4d68dd0433d5e"
+    },
+    "refs/diagnosability-audit.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 38706,
+      "sha256": "953901f262b0f4092297e03d3611e3c14cc678ed3d7072c55e604c8cd30ad944"
+    },
+    "refs/doc-discovery.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 9256,
+      "sha256": "57c0795ca5bec46c51cadf4ae02f156e3a112b2f592081921eeb4c729379e9aa"
+    },
+    "refs/effective-input-proof.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 1872,
+      "sha256": "f40412b36e13a5271bb5b426376efe2b837ff0d09c7e78c0b7ad61f19c95853c"
+    },
+    "refs/environment-deltas.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 2188,
+      "sha256": "a868fd374ec2c84981e2b7bde02334f9b75cf9f64a6b7abee9e028e63205ecff"
+    },
+    "refs/escalation-rubric.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 8058,
+      "sha256": "c72b5afc2c6b85cc979e5c071399d2c5825aae08d06e659d36c9b105b1067037"
+    },
+    "refs/hardening-output-contract.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 9819,
+      "sha256": "0a477f3addde441a0b617b909d0e1660bbb1b526dd7e5503d4d8c4731ee0faa6"
+    },
+    "refs/hypothesis-card-template.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 16316,
+      "sha256": "cfad9e91ac7816b22d1d3d5bc1c7db70c544a7a0783e63cabe0d3d0d253ee8cb"
+    },
+    "refs/pipeline-hardening-closure.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 7284,
+      "sha256": "597db5c60bc2e28f11ddd9062eb59e3180307f4b6db5a950cb69c3f9004f5625"
+    },
+    "refs/primitive-differential.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 6149,
+      "sha256": "12d8a49e5ee2749b56b822028f6676940eb57655c9852fa85273444d0c5156ce"
+    },
+    "refs/probe-packs": {
+      "kind": "dir",
+      "mode": 493
+    },
+    "refs/probe-packs/read-parse.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 632,
+      "sha256": "95f0397e7eb5f0620764ac77a475ce8b405018eb0841b42c25e19e569f993498"
+    },
+    "refs/remediation-handoff.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 16290,
+      "sha256": "aebafa75d8b1998a2e8573028cae63b7497fd25202e51afca245fb57d73610b1"
+    },
+    "refs/report-template.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 28985,
+      "sha256": "faa943d063f4078e3c9c5a5b58145fd530ed79a03a2296d6a4f23f71c838d7ce"
+    },
+    "refs/runtime-entrypoint-verification.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 3609,
+      "sha256": "d83f98cba7130cb0c61a5beda16c9d33420b22466de4c84781e886e94759a971"
+    },
+    "refs/triage-checklist.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 7584,
+      "sha256": "847c8a198ffff5818bbfedf4a7f6c21dae4b854ffcaa82223d31e6b8c4a5a19d"
+    },
+    "refs/unmask-and-sweep.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 3971,
+      "sha256": "460e1b8305242aeb085f6c426bfe2c50fbb8983050173b4d3cbde8437ebd2be8"
+    }
+  },
+  "profiles": {
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/agents/troubleshoot-analyst.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5306,
+      "sha256": "fe25f8713a400250cd2ed7387ae0c30d32e787318cb41f6034bb2f70a9767f44"
+    },
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/.claude/agents/troubleshoot-analyst.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 5306,
+      "sha256": "fe25f8713a400250cd2ed7387ae0c30d32e787318cb41f6034bb2f70a9767f44"
+    },
+    "/home/coder/.claude/agents/troubleshoot-analyst.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5258,
+      "sha256": "a952b4060db11be65b5bac546c6af3f2422615bc5cc3433179560a1d23c61213"
+    }
+  },
+  "settings": {
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/.claude/settings.json": {
+      "kind": "file",
+      "mode": 384,
+      "size": 1632,
+      "sha256": "1f535104e6bb9145585a88418d0a094a4b38d6432e3b5fbd6226d550da33d41c"
+    },
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/.claude/settings.local.json": {
+      "kind": "absent"
+    },
+    "/home/coder/.claude/settings.json": {
+      "kind": "file",
+      "mode": 420,
+      "size": 55663,
+      "sha256": "b39dd56864118734fa84bf885f45efcf9d0a8ddd9357be9f6b8793de39c47d06"
+    },
+    "/home/coder/.claude/settings.local.json": {
+      "kind": "absent"
+    }
+  },
+  "other_installed_digest": "aee68bf0b5fc006765e8299de6a7283e73fd29830836c140a939934813fdc64c",
+  "other_installed_entries": 46,
+  "project_mirrors": {
+    "skills": "474014884b6aaea81afc9519a245c844fcebb9b7fef3e9a32246c64dae0084b0",
+    "agents": "17f317b9b649b82789e5ce1c629f79743bcb20b3c5c84f57060fe5f431ab7c71",
+    "commands": "7f3c2978d5181c7fb2071df9082046a3410fb476b64f74d6e6ec9b380b6bd2ca",
+    "hooks": "32b821fa8cbf12814d9a1717baef1e8a0eb260f9339c5af7b1b9e20f587fe767",
+    "templates": "0388b1822767a0ee29d0e3c5171aedb524a795eb23173d084c1ebb4c7cff0eda"
+  },
+  "binding": {
+    "module": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/cli/install_skill.py",
+    "module_state": {
+      "kind": "file",
+      "mode": 384,
+      "size": 4197,
+      "sha256": "dba905ac3d3e7407f380146ada15cffa957d174e3371a5140a1fc2d06e3537c8"
+    },
+    "source": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-troubleshoot-protocol",
+    "target": "/home/coder/.claude/skills/sc-troubleshoot-protocol",
+    "source_realpath": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-troubleshoot-protocol",
+    "target_realpath": "/home/coder/.claude/skills/sc-troubleshoot-protocol",
+    "model_alias": "sonnet",
+    "model_mapping": "claude-gw-tier1b[1m]"
+  },
+  "roster": [
+    "Glob",
+    "Grep",
+    "Read",
+    "mcp__auggie__codebase-retrieval",
+    "mcp__codegraph__codegraph_callers",
+    "mcp__codegraph__codegraph_impact",
+    "mcp__codegraph__codegraph_node",
+    "mcp__codegraph__codegraph_search",
+    "mcp__litellm__augment_code-augment_code_search"
+  ],
+  "selected_mode_tightening": {
+    ".": {
+      "source": 448,
+      "installed": 493
+    },
+    "refs": {
+      "source": 448,
+      "installed": 493
+    },
+    "refs/agent-assertions.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/calibrator-eval-cases.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/contract-enumeration.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/effective-input-proof.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/environment-deltas.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/escalation-rubric.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/hardening-output-contract.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/hypothesis-card-template.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/pipeline-hardening-closure.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/primitive-differential.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/probe-packs": {
+      "source": 448,
+      "installed": 493
+    },
+    "refs/probe-packs/read-parse.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/remediation-handoff.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/report-template.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/runtime-entrypoint-verification.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/triage-checklist.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/unmask-and-sweep.md": {
+      "source": 384,
+      "installed": 420
+    }
+  },
+  "backup_reused": true,
+  "backup": {
+    "path": "./artifacts/installed-skill-before.tar.gz",
+    "kind": "file",
+    "mode": 384,
+    "size": 106556,
+    "sha256": "77e304762480a13a83589c62f3ca1dc8ddf8cd4ab3b0b0afc7920ec2341a3707"
+  },
+  "differing_files": [
+    "SKILL.md",
+    "refs/diagnosability-audit.md",
+    "refs/doc-discovery.md"
+  ],
+  "rebaseline": {
+    "reason": "Files outside the plan changed after the baseline; not made by this run.",
+    "approval": {
+      "ask_message": "msg_396f577fa3cd",
+      "answer_message": "msg_da4599a5fd9c",
+      "answer_text": "ok",
+      "interpretation": "Literal answer 'ok' to a question that recommended rebaseline-and-continue; read as approval of that option."
+    },
+    "settings_global": {
+      "path": "/home/coder/.claude/settings.json",
+      "old_sha256": "e0c2e76c60cfdd98dacdf6d751782c619875fb4c858f5037858af2e1a883f761",
+      "new_sha256": "b39dd56864118734fa84bf885f45efcf9d0a8ddd9357be9f6b8793de39c47d06",
+      "pre_change_copy": "/home/coder/.claude/settings.json.bak",
+      "top_level_keys_changed": [
+        "hooks",
+        "model"
+      ],
+      "permissions_equal": true,
+      "model_old": "claude-gw-tier1b[1m]",
+      "model_new": "claude-gw-gpt-6-luna[1m]",
+      "hooks_same_set": true
+    },
+    "other_installed": {
+      "old_entries": 45,
+      "new_entries": 46,
+      "old_digest": "55c0781e55cedb83fa5cb02e3cdfc8a8421288bb9d3b37b56f12cca971947b77",
+      "new_digest": "aee68bf0b5fc006765e8299de6a7283e73fd29830836c140a939934813fdc64c",
+      "known_new_entry": "setup-bmad (created 2026-11-09T16:03Z, after the baseline at 15:43Z)"
+    },
+    "unchanged_and_rechecked": [
+      "source",
+      "installed",
+      "profiles",
+      "project_mirrors",
+      "binding",
+      "roster",
+      "backup"
+    ]
+  },
+  "owner_decision_A": {
+    "decision": "A: mode-only exception for the 19 install-skill entries AUTHORIZED",
+    "source": "owner reply '1' at 2026-11-10T00:02Z, relayed by the coordinator",
+    "verbatim": "(A) AUTHORIZED: the mode-only exception for the 19 install-skill entries (2 directories, 17 refs files; source 700/600 vs installed 755/644; the install makes installed copies stricter). It covers ONLY those 19 entries and ONLY mode differences. Any other drift, any content-hash difference, or any mode difference that loosens permissions = STOP and report.",
+    "count_note": "The recorded entry set is 3 directories (., refs, refs/probe-packs) and 16 files; the total of 19 and the mode pairs match the wording.",
+    "entries": [
+      ".",
+      "refs",
+      "refs/agent-assertions.md",
+      "refs/calibrator-eval-cases.md",
+      "refs/contract-enumeration.md",
+      "refs/effective-input-proof.md",
+      "refs/environment-deltas.md",
+      "refs/escalation-rubric.md",
+      "refs/hardening-output-contract.md",
+      "refs/hypothesis-card-template.md",
+      "refs/pipeline-hardening-closure.md",
+      "refs/primitive-differential.md",
+      "refs/probe-packs",
+      "refs/probe-packs/read-parse.md",
+      "refs/remediation-handoff.md",
+      "refs/report-template.md",
+      "refs/runtime-entrypoint-verification.md",
+      "refs/triage-checklist.md",
+      "refs/unmask-and-sweep.md"
+    ]
+  },
+  "owner_decision_B": {
+    "decision": "B: settings.json rebaseline stays approved with conditions",
+    "source": "owner reply '1' at 2026-11-10T00:02Z, relayed by the coordinator",
+    "provenance": "owner ran /model in the coordinator session on 2026-11-09 ~19:38Z; the default model changed and was saved; setup-bmad is an unrelated tooling skill"
+  }
+}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-before.original.json b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-before.original.json
new file mode 100644
index 000000000..99363ac08
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-before.original.json
@@ -0,0 +1,423 @@
+{
+  "source": {
+    ".": {
+      "kind": "dir",
+      "mode": 448
+    },
+    "SKILL.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 133005,
+      "sha256": "0dd9d33fbdf6fc398cb717bd491587e3a5e4119eaa609336c6823128479acb9a"
+    },
+    "refs": {
+      "kind": "dir",
+      "mode": 448
+    },
+    "refs/agent-assertions.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 5957,
+      "sha256": "7bcd5b7c17957a903baee9933bcffb04adebfb093163576731a37cfecf8407fa"
+    },
+    "refs/calibrator-eval-cases.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 5256,
+      "sha256": "ef705ec12e75d8d91731013bb81416c7acca36744f8a433dc4dd9e3d9d16ffba"
+    },
+    "refs/contract-enumeration.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 2831,
+      "sha256": "8cf9c1e6fe6a086cbc2055f78ae07ee8fa2815eb1cce8e6918b4d68dd0433d5e"
+    },
+    "refs/diagnosability-audit.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 38873,
+      "sha256": "e86a3a4124c359c51827bbfbe5195bbe7c9670257a5121854c0cd94be32302d1"
+    },
+    "refs/doc-discovery.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 9312,
+      "sha256": "0b9d5a38b1ac4fb0fc7c9e62846a486e3ba799990c1cb44e2ddee3daaa88d8cd"
+    },
+    "refs/effective-input-proof.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 1872,
+      "sha256": "f40412b36e13a5271bb5b426376efe2b837ff0d09c7e78c0b7ad61f19c95853c"
+    },
+    "refs/environment-deltas.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 2188,
+      "sha256": "a868fd374ec2c84981e2b7bde02334f9b75cf9f64a6b7abee9e028e63205ecff"
+    },
+    "refs/escalation-rubric.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 8058,
+      "sha256": "c72b5afc2c6b85cc979e5c071399d2c5825aae08d06e659d36c9b105b1067037"
+    },
+    "refs/hardening-output-contract.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 9819,
+      "sha256": "0a477f3addde441a0b617b909d0e1660bbb1b526dd7e5503d4d8c4731ee0faa6"
+    },
+    "refs/hypothesis-card-template.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 16316,
+      "sha256": "cfad9e91ac7816b22d1d3d5bc1c7db70c544a7a0783e63cabe0d3d0d253ee8cb"
+    },
+    "refs/pipeline-hardening-closure.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 7284,
+      "sha256": "597db5c60bc2e28f11ddd9062eb59e3180307f4b6db5a950cb69c3f9004f5625"
+    },
+    "refs/primitive-differential.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 6149,
+      "sha256": "12d8a49e5ee2749b56b822028f6676940eb57655c9852fa85273444d0c5156ce"
+    },
+    "refs/probe-packs": {
+      "kind": "dir",
+      "mode": 448
+    },
+    "refs/probe-packs/read-parse.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 632,
+      "sha256": "95f0397e7eb5f0620764ac77a475ce8b405018eb0841b42c25e19e569f993498"
+    },
+    "refs/remediation-handoff.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 16290,
+      "sha256": "aebafa75d8b1998a2e8573028cae63b7497fd25202e51afca245fb57d73610b1"
+    },
+    "refs/report-template.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 28985,
+      "sha256": "faa943d063f4078e3c9c5a5b58145fd530ed79a03a2296d6a4f23f71c838d7ce"
+    },
+    "refs/runtime-entrypoint-verification.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 3609,
+      "sha256": "d83f98cba7130cb0c61a5beda16c9d33420b22466de4c84781e886e94759a971"
+    },
+    "refs/triage-checklist.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 7584,
+      "sha256": "847c8a198ffff5818bbfedf4a7f6c21dae4b854ffcaa82223d31e6b8c4a5a19d"
+    },
+    "refs/unmask-and-sweep.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 3971,
+      "sha256": "460e1b8305242aeb085f6c426bfe2c50fbb8983050173b4d3cbde8437ebd2be8"
+    }
+  },
+  "installed": {
+    ".": {
+      "kind": "dir",
+      "mode": 493
+    },
+    "SKILL.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 131516,
+      "sha256": "6d1b226cba4c2fbe9dae7bcbbfe954ee9463a20473e4e33bdc679cda39b2f3e5"
+    },
+    "refs": {
+      "kind": "dir",
+      "mode": 493
+    },
+    "refs/agent-assertions.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5957,
+      "sha256": "7bcd5b7c17957a903baee9933bcffb04adebfb093163576731a37cfecf8407fa"
+    },
+    "refs/calibrator-eval-cases.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5256,
+      "sha256": "ef705ec12e75d8d91731013bb81416c7acca36744f8a433dc4dd9e3d9d16ffba"
+    },
+    "refs/contract-enumeration.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 2831,
+      "sha256": "8cf9c1e6fe6a086cbc2055f78ae07ee8fa2815eb1cce8e6918b4d68dd0433d5e"
+    },
+    "refs/diagnosability-audit.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 38706,
+      "sha256": "953901f262b0f4092297e03d3611e3c14cc678ed3d7072c55e604c8cd30ad944"
+    },
+    "refs/doc-discovery.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 9256,
+      "sha256": "57c0795ca5bec46c51cadf4ae02f156e3a112b2f592081921eeb4c729379e9aa"
+    },
+    "refs/effective-input-proof.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 1872,
+      "sha256": "f40412b36e13a5271bb5b426376efe2b837ff0d09c7e78c0b7ad61f19c95853c"
+    },
+    "refs/environment-deltas.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 2188,
+      "sha256": "a868fd374ec2c84981e2b7bde02334f9b75cf9f64a6b7abee9e028e63205ecff"
+    },
+    "refs/escalation-rubric.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 8058,
+      "sha256": "c72b5afc2c6b85cc979e5c071399d2c5825aae08d06e659d36c9b105b1067037"
+    },
+    "refs/hardening-output-contract.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 9819,
+      "sha256": "0a477f3addde441a0b617b909d0e1660bbb1b526dd7e5503d4d8c4731ee0faa6"
+    },
+    "refs/hypothesis-card-template.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 16316,
+      "sha256": "cfad9e91ac7816b22d1d3d5bc1c7db70c544a7a0783e63cabe0d3d0d253ee8cb"
+    },
+    "refs/pipeline-hardening-closure.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 7284,
+      "sha256": "597db5c60bc2e28f11ddd9062eb59e3180307f4b6db5a950cb69c3f9004f5625"
+    },
+    "refs/primitive-differential.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 6149,
+      "sha256": "12d8a49e5ee2749b56b822028f6676940eb57655c9852fa85273444d0c5156ce"
+    },
+    "refs/probe-packs": {
+      "kind": "dir",
+      "mode": 493
+    },
+    "refs/probe-packs/read-parse.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 632,
+      "sha256": "95f0397e7eb5f0620764ac77a475ce8b405018eb0841b42c25e19e569f993498"
+    },
+    "refs/remediation-handoff.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 16290,
+      "sha256": "aebafa75d8b1998a2e8573028cae63b7497fd25202e51afca245fb57d73610b1"
+    },
+    "refs/report-template.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 28985,
+      "sha256": "faa943d063f4078e3c9c5a5b58145fd530ed79a03a2296d6a4f23f71c838d7ce"
+    },
+    "refs/runtime-entrypoint-verification.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 3609,
+      "sha256": "d83f98cba7130cb0c61a5beda16c9d33420b22466de4c84781e886e94759a971"
+    },
+    "refs/triage-checklist.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 7584,
+      "sha256": "847c8a198ffff5818bbfedf4a7f6c21dae4b854ffcaa82223d31e6b8c4a5a19d"
+    },
+    "refs/unmask-and-sweep.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 3971,
+      "sha256": "460e1b8305242aeb085f6c426bfe2c50fbb8983050173b4d3cbde8437ebd2be8"
+    }
+  },
+  "profiles": {
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/agents/troubleshoot-analyst.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5306,
+      "sha256": "fe25f8713a400250cd2ed7387ae0c30d32e787318cb41f6034bb2f70a9767f44"
+    },
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/.claude/agents/troubleshoot-analyst.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 5306,
+      "sha256": "fe25f8713a400250cd2ed7387ae0c30d32e787318cb41f6034bb2f70a9767f44"
+    },
+    "/home/coder/.claude/agents/troubleshoot-analyst.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5258,
+      "sha256": "a952b4060db11be65b5bac546c6af3f2422615bc5cc3433179560a1d23c61213"
+    }
+  },
+  "settings": {
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/.claude/settings.json": {
+      "kind": "file",
+      "mode": 384,
+      "size": 1632,
+      "sha256": "1f535104e6bb9145585a88418d0a094a4b38d6432e3b5fbd6226d550da33d41c"
+    },
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/.claude/settings.local.json": {
+      "kind": "absent"
+    },
+    "/home/coder/.claude/settings.json": {
+      "kind": "file",
+      "mode": 420,
+      "size": 55659,
+      "sha256": "e0c2e76c60cfdd98dacdf6d751782c619875fb4c858f5037858af2e1a883f761"
+    },
+    "/home/coder/.claude/settings.local.json": {
+      "kind": "absent"
+    }
+  },
+  "other_installed_digest": "55c0781e55cedb83fa5cb02e3cdfc8a8421288bb9d3b37b56f12cca971947b77",
+  "other_installed_entries": 45,
+  "project_mirrors": {
+    "skills": "474014884b6aaea81afc9519a245c844fcebb9b7fef3e9a32246c64dae0084b0",
+    "agents": "17f317b9b649b82789e5ce1c629f79743bcb20b3c5c84f57060fe5f431ab7c71",
+    "commands": "7f3c2978d5181c7fb2071df9082046a3410fb476b64f74d6e6ec9b380b6bd2ca",
+    "hooks": "32b821fa8cbf12814d9a1717baef1e8a0eb260f9339c5af7b1b9e20f587fe767",
+    "templates": "0388b1822767a0ee29d0e3c5171aedb524a795eb23173d084c1ebb4c7cff0eda"
+  },
+  "binding": {
+    "module": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/cli/install_skill.py",
+    "module_state": {
+      "kind": "file",
+      "mode": 384,
+      "size": 4197,
+      "sha256": "dba905ac3d3e7407f380146ada15cffa957d174e3371a5140a1fc2d06e3537c8"
+    },
+    "source": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-troubleshoot-protocol",
+    "target": "/home/coder/.claude/skills/sc-troubleshoot-protocol",
+    "source_realpath": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-troubleshoot-protocol",
+    "target_realpath": "/home/coder/.claude/skills/sc-troubleshoot-protocol",
+    "model_alias": "sonnet",
+    "model_mapping": "claude-gw-tier1b[1m]"
+  },
+  "roster": [
+    "Glob",
+    "Grep",
+    "Read",
+    "mcp__auggie__codebase-retrieval",
+    "mcp__codegraph__codegraph_callers",
+    "mcp__codegraph__codegraph_impact",
+    "mcp__codegraph__codegraph_node",
+    "mcp__codegraph__codegraph_search",
+    "mcp__litellm__augment_code-augment_code_search"
+  ],
+  "selected_mode_tightening": {
+    ".": {
+      "source": 448,
+      "installed": 493
+    },
+    "refs": {
+      "source": 448,
+      "installed": 493
+    },
+    "refs/agent-assertions.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/calibrator-eval-cases.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/contract-enumeration.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/effective-input-proof.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/environment-deltas.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/escalation-rubric.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/hardening-output-contract.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/hypothesis-card-template.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/pipeline-hardening-closure.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/primitive-differential.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/probe-packs": {
+      "source": 448,
+      "installed": 493
+    },
+    "refs/probe-packs/read-parse.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/remediation-handoff.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/report-template.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/runtime-entrypoint-verification.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/triage-checklist.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/unmask-and-sweep.md": {
+      "source": 384,
+      "installed": 420
+    }
+  },
+  "backup": {
+    "path": "./artifacts/installed-skill-before.tar.gz",
+    "kind": "file",
+    "mode": 384,
+    "size": 106556,
+    "sha256": "77e304762480a13a83589c62f3ca1dc8ddf8cd4ab3b0b0afc7920ec2341a3707"
+  },
+  "differing_files": [
+    "SKILL.md",
+    "refs/diagnosability-audit.md",
+    "refs/doc-discovery.md"
+  ]
+}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-before.rebaselined.json b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-before.rebaselined.json
new file mode 100644
index 000000000..61e9a0bec
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-before.rebaselined.json
@@ -0,0 +1,462 @@
+{
+  "source": {
+    ".": {
+      "kind": "dir",
+      "mode": 448
+    },
+    "SKILL.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 133005,
+      "sha256": "0dd9d33fbdf6fc398cb717bd491587e3a5e4119eaa609336c6823128479acb9a"
+    },
+    "refs": {
+      "kind": "dir",
+      "mode": 448
+    },
+    "refs/agent-assertions.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 5957,
+      "sha256": "7bcd5b7c17957a903baee9933bcffb04adebfb093163576731a37cfecf8407fa"
+    },
+    "refs/calibrator-eval-cases.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 5256,
+      "sha256": "ef705ec12e75d8d91731013bb81416c7acca36744f8a433dc4dd9e3d9d16ffba"
+    },
+    "refs/contract-enumeration.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 2831,
+      "sha256": "8cf9c1e6fe6a086cbc2055f78ae07ee8fa2815eb1cce8e6918b4d68dd0433d5e"
+    },
+    "refs/diagnosability-audit.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 38873,
+      "sha256": "e86a3a4124c359c51827bbfbe5195bbe7c9670257a5121854c0cd94be32302d1"
+    },
+    "refs/doc-discovery.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 9312,
+      "sha256": "0b9d5a38b1ac4fb0fc7c9e62846a486e3ba799990c1cb44e2ddee3daaa88d8cd"
+    },
+    "refs/effective-input-proof.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 1872,
+      "sha256": "f40412b36e13a5271bb5b426376efe2b837ff0d09c7e78c0b7ad61f19c95853c"
+    },
+    "refs/environment-deltas.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 2188,
+      "sha256": "a868fd374ec2c84981e2b7bde02334f9b75cf9f64a6b7abee9e028e63205ecff"
+    },
+    "refs/escalation-rubric.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 8058,
+      "sha256": "c72b5afc2c6b85cc979e5c071399d2c5825aae08d06e659d36c9b105b1067037"
+    },
+    "refs/hardening-output-contract.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 9819,
+      "sha256": "0a477f3addde441a0b617b909d0e1660bbb1b526dd7e5503d4d8c4731ee0faa6"
+    },
+    "refs/hypothesis-card-template.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 16316,
+      "sha256": "cfad9e91ac7816b22d1d3d5bc1c7db70c544a7a0783e63cabe0d3d0d253ee8cb"
+    },
+    "refs/pipeline-hardening-closure.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 7284,
+      "sha256": "597db5c60bc2e28f11ddd9062eb59e3180307f4b6db5a950cb69c3f9004f5625"
+    },
+    "refs/primitive-differential.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 6149,
+      "sha256": "12d8a49e5ee2749b56b822028f6676940eb57655c9852fa85273444d0c5156ce"
+    },
+    "refs/probe-packs": {
+      "kind": "dir",
+      "mode": 448
+    },
+    "refs/probe-packs/read-parse.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 632,
+      "sha256": "95f0397e7eb5f0620764ac77a475ce8b405018eb0841b42c25e19e569f993498"
+    },
+    "refs/remediation-handoff.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 16290,
+      "sha256": "aebafa75d8b1998a2e8573028cae63b7497fd25202e51afca245fb57d73610b1"
+    },
+    "refs/report-template.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 28985,
+      "sha256": "faa943d063f4078e3c9c5a5b58145fd530ed79a03a2296d6a4f23f71c838d7ce"
+    },
+    "refs/runtime-entrypoint-verification.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 3609,
+      "sha256": "d83f98cba7130cb0c61a5beda16c9d33420b22466de4c84781e886e94759a971"
+    },
+    "refs/triage-checklist.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 7584,
+      "sha256": "847c8a198ffff5818bbfedf4a7f6c21dae4b854ffcaa82223d31e6b8c4a5a19d"
+    },
+    "refs/unmask-and-sweep.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 3971,
+      "sha256": "460e1b8305242aeb085f6c426bfe2c50fbb8983050173b4d3cbde8437ebd2be8"
+    }
+  },
+  "installed": {
+    ".": {
+      "kind": "dir",
+      "mode": 493
+    },
+    "SKILL.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 131516,
+      "sha256": "6d1b226cba4c2fbe9dae7bcbbfe954ee9463a20473e4e33bdc679cda39b2f3e5"
+    },
+    "refs": {
+      "kind": "dir",
+      "mode": 493
+    },
+    "refs/agent-assertions.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5957,
+      "sha256": "7bcd5b7c17957a903baee9933bcffb04adebfb093163576731a37cfecf8407fa"
+    },
+    "refs/calibrator-eval-cases.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5256,
+      "sha256": "ef705ec12e75d8d91731013bb81416c7acca36744f8a433dc4dd9e3d9d16ffba"
+    },
+    "refs/contract-enumeration.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 2831,
+      "sha256": "8cf9c1e6fe6a086cbc2055f78ae07ee8fa2815eb1cce8e6918b4d68dd0433d5e"
+    },
+    "refs/diagnosability-audit.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 38706,
+      "sha256": "953901f262b0f4092297e03d3611e3c14cc678ed3d7072c55e604c8cd30ad944"
+    },
+    "refs/doc-discovery.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 9256,
+      "sha256": "57c0795ca5bec46c51cadf4ae02f156e3a112b2f592081921eeb4c729379e9aa"
+    },
+    "refs/effective-input-proof.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 1872,
+      "sha256": "f40412b36e13a5271bb5b426376efe2b837ff0d09c7e78c0b7ad61f19c95853c"
+    },
+    "refs/environment-deltas.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 2188,
+      "sha256": "a868fd374ec2c84981e2b7bde02334f9b75cf9f64a6b7abee9e028e63205ecff"
+    },
+    "refs/escalation-rubric.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 8058,
+      "sha256": "c72b5afc2c6b85cc979e5c071399d2c5825aae08d06e659d36c9b105b1067037"
+    },
+    "refs/hardening-output-contract.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 9819,
+      "sha256": "0a477f3addde441a0b617b909d0e1660bbb1b526dd7e5503d4d8c4731ee0faa6"
+    },
+    "refs/hypothesis-card-template.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 16316,
+      "sha256": "cfad9e91ac7816b22d1d3d5bc1c7db70c544a7a0783e63cabe0d3d0d253ee8cb"
+    },
+    "refs/pipeline-hardening-closure.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 7284,
+      "sha256": "597db5c60bc2e28f11ddd9062eb59e3180307f4b6db5a950cb69c3f9004f5625"
+    },
+    "refs/primitive-differential.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 6149,
+      "sha256": "12d8a49e5ee2749b56b822028f6676940eb57655c9852fa85273444d0c5156ce"
+    },
+    "refs/probe-packs": {
+      "kind": "dir",
+      "mode": 493
+    },
+    "refs/probe-packs/read-parse.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 632,
+      "sha256": "95f0397e7eb5f0620764ac77a475ce8b405018eb0841b42c25e19e569f993498"
+    },
+    "refs/remediation-handoff.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 16290,
+      "sha256": "aebafa75d8b1998a2e8573028cae63b7497fd25202e51afca245fb57d73610b1"
+    },
+    "refs/report-template.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 28985,
+      "sha256": "faa943d063f4078e3c9c5a5b58145fd530ed79a03a2296d6a4f23f71c838d7ce"
+    },
+    "refs/runtime-entrypoint-verification.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 3609,
+      "sha256": "d83f98cba7130cb0c61a5beda16c9d33420b22466de4c84781e886e94759a971"
+    },
+    "refs/triage-checklist.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 7584,
+      "sha256": "847c8a198ffff5818bbfedf4a7f6c21dae4b854ffcaa82223d31e6b8c4a5a19d"
+    },
+    "refs/unmask-and-sweep.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 3971,
+      "sha256": "460e1b8305242aeb085f6c426bfe2c50fbb8983050173b4d3cbde8437ebd2be8"
+    }
+  },
+  "profiles": {
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/agents/troubleshoot-analyst.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5306,
+      "sha256": "fe25f8713a400250cd2ed7387ae0c30d32e787318cb41f6034bb2f70a9767f44"
+    },
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/.claude/agents/troubleshoot-analyst.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 5306,
+      "sha256": "fe25f8713a400250cd2ed7387ae0c30d32e787318cb41f6034bb2f70a9767f44"
+    },
+    "/home/coder/.claude/agents/troubleshoot-analyst.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5258,
+      "sha256": "a952b4060db11be65b5bac546c6af3f2422615bc5cc3433179560a1d23c61213"
+    }
+  },
+  "settings": {
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/.claude/settings.json": {
+      "kind": "file",
+      "mode": 384,
+      "size": 1632,
+      "sha256": "1f535104e6bb9145585a88418d0a094a4b38d6432e3b5fbd6226d550da33d41c"
+    },
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/.claude/settings.local.json": {
+      "kind": "absent"
+    },
+    "/home/coder/.claude/settings.json": {
+      "kind": "file",
+      "mode": 420,
+      "size": 55663,
+      "sha256": "b39dd56864118734fa84bf885f45efcf9d0a8ddd9357be9f6b8793de39c47d06"
+    },
+    "/home/coder/.claude/settings.local.json": {
+      "kind": "absent"
+    }
+  },
+  "other_installed_digest": "aee68bf0b5fc006765e8299de6a7283e73fd29830836c140a939934813fdc64c",
+  "other_installed_entries": 46,
+  "project_mirrors": {
+    "skills": "474014884b6aaea81afc9519a245c844fcebb9b7fef3e9a32246c64dae0084b0",
+    "agents": "17f317b9b649b82789e5ce1c629f79743bcb20b3c5c84f57060fe5f431ab7c71",
+    "commands": "7f3c2978d5181c7fb2071df9082046a3410fb476b64f74d6e6ec9b380b6bd2ca",
+    "hooks": "32b821fa8cbf12814d9a1717baef1e8a0eb260f9339c5af7b1b9e20f587fe767",
+    "templates": "0388b1822767a0ee29d0e3c5171aedb524a795eb23173d084c1ebb4c7cff0eda"
+  },
+  "binding": {
+    "module": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/cli/install_skill.py",
+    "module_state": {
+      "kind": "file",
+      "mode": 384,
+      "size": 4197,
+      "sha256": "dba905ac3d3e7407f380146ada15cffa957d174e3371a5140a1fc2d06e3537c8"
+    },
+    "source": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-troubleshoot-protocol",
+    "target": "/home/coder/.claude/skills/sc-troubleshoot-protocol",
+    "source_realpath": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-troubleshoot-protocol",
+    "target_realpath": "/home/coder/.claude/skills/sc-troubleshoot-protocol",
+    "model_alias": "sonnet",
+    "model_mapping": "claude-gw-tier1b[1m]"
+  },
+  "roster": [
+    "Glob",
+    "Grep",
+    "Read",
+    "mcp__auggie__codebase-retrieval",
+    "mcp__codegraph__codegraph_callers",
+    "mcp__codegraph__codegraph_impact",
+    "mcp__codegraph__codegraph_node",
+    "mcp__codegraph__codegraph_search",
+    "mcp__litellm__augment_code-augment_code_search"
+  ],
+  "selected_mode_tightening": {
+    ".": {
+      "source": 448,
+      "installed": 493
+    },
+    "refs": {
+      "source": 448,
+      "installed": 493
+    },
+    "refs/agent-assertions.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/calibrator-eval-cases.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/contract-enumeration.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/effective-input-proof.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/environment-deltas.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/escalation-rubric.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/hardening-output-contract.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/hypothesis-card-template.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/pipeline-hardening-closure.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/primitive-differential.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/probe-packs": {
+      "source": 448,
+      "installed": 493
+    },
+    "refs/probe-packs/read-parse.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/remediation-handoff.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/report-template.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/runtime-entrypoint-verification.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/triage-checklist.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/unmask-and-sweep.md": {
+      "source": 384,
+      "installed": 420
+    }
+  },
+  "backup": {
+    "path": "./artifacts/installed-skill-before.tar.gz",
+    "kind": "file",
+    "mode": 384,
+    "size": 106556,
+    "sha256": "77e304762480a13a83589c62f3ca1dc8ddf8cd4ab3b0b0afc7920ec2341a3707"
+  },
+  "differing_files": [
+    "SKILL.md",
+    "refs/diagnosability-audit.md",
+    "refs/doc-discovery.md"
+  ],
+  "rebaseline": {
+    "reason": "Files outside the plan changed after the baseline; not made by this run.",
+    "approval": {
+      "ask_message": "msg_396f577fa3cd",
+      "answer_message": "msg_da4599a5fd9c",
+      "answer_text": "ok",
+      "interpretation": "Literal answer 'ok' to a question that recommended rebaseline-and-continue; read as approval of that option."
+    },
+    "settings_global": {
+      "path": "/home/coder/.claude/settings.json",
+      "old_sha256": "e0c2e76c60cfdd98dacdf6d751782c619875fb4c858f5037858af2e1a883f761",
+      "new_sha256": "b39dd56864118734fa84bf885f45efcf9d0a8ddd9357be9f6b8793de39c47d06",
+      "pre_change_copy": "/home/coder/.claude/settings.json.bak",
+      "top_level_keys_changed": [
+        "hooks",
+        "model"
+      ],
+      "permissions_equal": true,
+      "model_old": "claude-gw-tier1b[1m]",
+      "model_new": "claude-gw-gpt-6-luna[1m]",
+      "hooks_same_set": true
+    },
+    "other_installed": {
+      "old_entries": 45,
+      "new_entries": 46,
+      "old_digest": "55c0781e55cedb83fa5cb02e3cdfc8a8421288bb9d3b37b56f12cca971947b77",
+      "new_digest": "aee68bf0b5fc006765e8299de6a7283e73fd29830836c140a939934813fdc64c",
+      "known_new_entry": "setup-bmad (created 2026-11-09T16:03Z, after the baseline at 15:43Z)"
+    },
+    "unchanged_and_rechecked": [
+      "source",
+      "installed",
+      "profiles",
+      "project_mirrors",
+      "binding",
+      "roster",
+      "backup"
+    ]
+  }
+}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py
index 894d6c660..03cfb7258 100644
--- a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py
@@ -1,4 +1,5 @@
 """Approved compatibility inventory/backup only. This helper never installs a skill."""
+
 import hashlib
 import json
 import os
@@ -11,110 +12,414 @@ from pathlib import Path
 import superclaude.cli.install_skill as installer
 
 os.umask(0o077)
-ROOT=Path('/home/coder/workspaces/worktrees/IronClaude/issue-441')
-PKG=ROOT/'.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413'
-OUT=PKG/'artifacts'
-SOURCE=ROOT/'src/superclaude/skills/sc-troubleshoot-protocol'
-TARGET=Path('/home/coder/.claude/skills/sc-troubleshoot-protocol')
-PROFILES=[ROOT/'src/superclaude/agents/troubleshoot-analyst.md',ROOT/'.claude/agents/troubleshoot-analyst.md',Path('/home/coder/.claude/agents/troubleshoot-analyst.md')]
-SETTINGS=[ROOT/'.claude/settings.json',ROOT/'.claude/settings.local.json',Path('/home/coder/.claude/settings.json'),Path('/home/coder/.claude/settings.local.json')]
-EXPECTED={'Read','Grep','Glob','mcp__litellm__augment_code-augment_code_search','mcp__auggie__codebase-retrieval','mcp__codegraph__codegraph_search','mcp__codegraph__codegraph_node','mcp__codegraph__codegraph_callers','mcp__codegraph__codegraph_impact'}
-EXPECTED_DRIFT=['SKILL.md','refs/diagnosability-audit.md','refs/doc-discovery.md']
+ROOT = Path("/home/coder/workspaces/worktrees/IronClaude/issue-441")
+PKG = ROOT / ".dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413"
+OUT = PKG / "artifacts"
+SOURCE = ROOT / "src/superclaude/skills/sc-troubleshoot-protocol"
+TARGET = Path("/home/coder/.claude/skills/sc-troubleshoot-protocol")
+PROFILES = [
+    ROOT / "src/superclaude/agents/troubleshoot-analyst.md",
+    ROOT / ".claude/agents/troubleshoot-analyst.md",
+    Path("/home/coder/.claude/agents/troubleshoot-analyst.md"),
+]
+SETTINGS = [
+    ROOT / ".claude/settings.json",
+    ROOT / ".claude/settings.local.json",
+    Path("/home/coder/.claude/settings.json"),
+    Path("/home/coder/.claude/settings.local.json"),
+]
+EXPECTED = {
+    "Read",
+    "Grep",
+    "Glob",
+    "mcp__litellm__augment_code-augment_code_search",
+    "mcp__auggie__codebase-retrieval",
+    "mcp__codegraph__codegraph_search",
+    "mcp__codegraph__codegraph_node",
+    "mcp__codegraph__codegraph_callers",
+    "mcp__codegraph__codegraph_impact",
+}
+EXPECTED_DRIFT = ["SKILL.md", "refs/diagnosability-audit.md", "refs/doc-discovery.md"]
+# Owner decision A (reply '1', 2026-11-10T00:02Z, relayed by the coordinator): exactly these
+# 19 entries may differ in mode only, source 0700/0600 against installed 0755/0644 (the
+# install tightens the installed copy). Any other mode difference, any loosening, or any
+# value other than these pairs stops the run.
+_DIRS = (".", "refs", "refs/probe-packs")
+_FILES = (
+    "refs/agent-assertions.md",
+    "refs/calibrator-eval-cases.md",
+    "refs/contract-enumeration.md",
+    "refs/effective-input-proof.md",
+    "refs/environment-deltas.md",
+    "refs/escalation-rubric.md",
+    "refs/hardening-output-contract.md",
+    "refs/hypothesis-card-template.md",
+    "refs/pipeline-hardening-closure.md",
+    "refs/primitive-differential.md",
+    "refs/probe-packs/read-parse.md",
+    "refs/remediation-handoff.md",
+    "refs/report-template.md",
+    "refs/runtime-entrypoint-verification.md",
+    "refs/triage-checklist.md",
+    "refs/unmask-and-sweep.md",
+)
+AUTHORIZED_MODE_TIGHTENING = {
+    **{k: {"source": 0o700, "installed": 0o755} for k in _DIRS},
+    **{k: {"source": 0o600, "installed": 0o644} for k in _FILES},
+}
+OWNER_DECISION_A = {
+    "decision": "A: mode-only exception for the 19 install-skill entries AUTHORIZED",
+    "source": "owner reply '1' at 2026-11-10T00:02Z, relayed by the coordinator",
+    "verbatim": (
+        "(A) AUTHORIZED: the mode-only exception for the 19 install-skill entries "
+        "(2 directories, 17 refs files; source 700/600 vs installed 755/644; the install "
+        "makes installed copies stricter). It covers ONLY those 19 entries and ONLY mode "
+        "differences. Any other drift, any content-hash difference, or any mode difference "
+        "that loosens permissions = STOP and report."
+    ),
+    "count_note": (
+        "The recorded entry set is 3 directories (., refs, refs/probe-packs) and 16 files; "
+        "the total of 19 and the mode pairs match the wording."
+    ),
+    "entries": sorted(AUTHORIZED_MODE_TIGHTENING),
+}
+OWNER_DECISION_B = {
+    "decision": "B: settings.json rebaseline stays approved with conditions",
+    "source": "owner reply '1' at 2026-11-10T00:02Z, relayed by the coordinator",
+    "provenance": (
+        "owner ran /model in the coordinator session on 2026-11-09 ~19:38Z; the default "
+        "model changed and was saved; setup-bmad is an unrelated tooling skill"
+    ),
+}
+
 
 def hash_stream(stream):
-    h=hashlib.sha256()
-    for chunk in iter(lambda:stream.read(65536),b''): h.update(chunk)
+    h = hashlib.sha256()
+    for chunk in iter(lambda: stream.read(65536), b""):
+        h.update(chunk)
     return h.hexdigest()
 
+
 def file_state(path):
-    if not os.path.lexists(path): return {'kind':'absent'}
-    st=path.lstat(); mode=stat.S_IMODE(st.st_mode)
-    if stat.S_ISLNK(st.st_mode): return {'kind':'symlink','mode':mode,'target':os.readlink(path)}
-    if stat.S_ISDIR(st.st_mode): return {'kind':'dir','mode':mode}
-    if not stat.S_ISREG(st.st_mode): return {'kind':'special','mode':mode}
-    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
-    with os.fdopen(fd,'rb') as f:
-        actual=os.fstat(f.fileno())
-        assert stat.S_ISREG(actual.st_mode) and (actual.st_dev,actual.st_ino)==(st.st_dev,st.st_ino),path
-        return {'kind':'file','mode':mode,'size':actual.st_size,'sha256':hash_stream(f)}
+    if not os.path.lexists(path):
+        return {"kind": "absent"}
+    st = path.lstat()
+    mode = stat.S_IMODE(st.st_mode)
+    if stat.S_ISLNK(st.st_mode):
+        return {"kind": "symlink", "mode": mode, "target": os.readlink(path)}
+    if stat.S_ISDIR(st.st_mode):
+        return {"kind": "dir", "mode": mode}
+    if not stat.S_ISREG(st.st_mode):
+        return {"kind": "special", "mode": mode}
+    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
+    with os.fdopen(fd, "rb") as f:
+        actual = os.fstat(f.fileno())
+        assert stat.S_ISREG(actual.st_mode) and (actual.st_dev, actual.st_ino) == (
+            st.st_dev,
+            st.st_ino,
+        ), path
+        return {
+            "kind": "file",
+            "mode": mode,
+            "size": actual.st_size,
+            "sha256": hash_stream(f),
+        }
+
 
 def manifest(folder):
-    return {'.':file_state(folder),**{str(p.relative_to(folder)):file_state(p) for p in sorted(folder.rglob('*'))}}
+    return {
+        ".": file_state(folder),
+        **{
+            str(p.relative_to(folder)): file_state(p) for p in sorted(folder.rglob("*"))
+        },
+    }
+
+
+def digest(value):
+    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()
+
 
-def digest(value): return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()
 def roster(path):
-    front=re.match(r'\A---\n(.*?)\n---',path.read_text(),re.S)
-    assert front,path
-    tools=re.search(r'^tools:\s*(.+)$',front[1],re.M)
-    assert tools,path
-    return set(x.strip() for x in tools[1].split(','))
+    front = re.match(r"\A---\n(.*?)\n---", path.read_text(), re.S)
+    assert front, path
+    tools = re.search(r"^tools:\s*(.+)$", front[1], re.M)
+    assert tools, path
+    return set(x.strip() for x in tools[1].split(","))
+
+
 def contract_roster(path):
-    match=re.search(r'closed roster `([^`]+)`',path.read_text())
-    assert match,path
-    return set(x.strip() for x in match[1].split(','))
+    match = re.search(r"closed roster `([^`]+)`", path.read_text())
+    assert match, path
+    return set(x.strip() for x in match[1].split(","))
+
 
 def current():
-    assert os.environ.get('ANTHROPIC_DEFAULT_SONNET_MODEL')=='claude-gw-tier1b[1m]','Unverified helper mapping'
-    assert SOURCE.resolve()==SOURCE and TARGET.resolve()==TARGET and TARGET.is_dir()
-    assert installer._get_skill_source('sc-troubleshoot-protocol').resolve()==SOURCE
-    assert Path(installer.__file__).resolve()==ROOT/'src/superclaude/cli/install_skill.py'
-    assert Path.home()==Path('/home/coder')
-    source=manifest(SOURCE); installed=manifest(TARGET)
-    assert all(v['kind'] in ('file','dir') for v in source.values())
-    assert all(v['kind'] in ('file','dir') for v in installed.values())
-    assert roster(PROFILES[0])==roster(PROFILES[1])==contract_roster(SOURCE/'SKILL.md')==EXPECTED
-    profiles={str(p):file_state(p) for p in PROFILES}
-    settings={str(p):file_state(p) for p in SETTINGS}
-    other={str(p.name):digest(manifest(p)) if p.is_dir() and not p.is_symlink() else file_state(p) for p in sorted(TARGET.parent.iterdir()) if p!=TARGET}
-    mirrors={name:digest(manifest(ROOT/'.claude'/name)) for name in ('skills','agents','commands','hooks','templates')}
-    binding={'module':str(Path(installer.__file__).resolve()),'module_state':file_state(Path(installer.__file__)),'source':str(SOURCE),'target':str(TARGET),'source_realpath':str(SOURCE.resolve()),'target_realpath':str(TARGET.resolve()),'model_alias':'sonnet','model_mapping':os.environ['ANTHROPIC_DEFAULT_SONNET_MODEL']}
-    return {'source':source,'installed':installed,'profiles':profiles,'settings':settings,'other_installed_digest':digest(other),'other_installed_entries':len(other),'project_mirrors':mirrors,'binding':binding,'roster':sorted(EXPECTED)}
+    assert os.environ.get("ANTHROPIC_DEFAULT_SONNET_MODEL") == "claude-gw-tier1b[1m]", (
+        "Unverified helper mapping"
+    )
+    assert SOURCE.resolve() == SOURCE and TARGET.resolve() == TARGET and TARGET.is_dir()
+    assert installer._get_skill_source("sc-troubleshoot-protocol").resolve() == SOURCE
+    assert (
+        Path(installer.__file__).resolve()
+        == ROOT / "src/superclaude/cli/install_skill.py"
+    )
+    assert Path.home() == Path("/home/coder")
+    source = manifest(SOURCE)
+    installed = manifest(TARGET)
+    assert all(v["kind"] in ("file", "dir") for v in source.values())
+    assert all(v["kind"] in ("file", "dir") for v in installed.values())
+    assert (
+        roster(PROFILES[0])
+        == roster(PROFILES[1])
+        == contract_roster(SOURCE / "SKILL.md")
+        == EXPECTED
+    )
+    profiles = {str(p): file_state(p) for p in PROFILES}
+    settings = {str(p): file_state(p) for p in SETTINGS}
+    other = {
+        str(p.name): digest(manifest(p))
+        if p.is_dir() and not p.is_symlink()
+        else file_state(p)
+        for p in sorted(TARGET.parent.iterdir())
+        if p != TARGET
+    }
+    mirrors = {
+        name: digest(manifest(ROOT / ".claude" / name))
+        for name in ("skills", "agents", "commands", "hooks", "templates")
+    }
+    binding = {
+        "module": str(Path(installer.__file__).resolve()),
+        "module_state": file_state(Path(installer.__file__)),
+        "source": str(SOURCE),
+        "target": str(TARGET),
+        "source_realpath": str(SOURCE.resolve()),
+        "target_realpath": str(TARGET.resolve()),
+        "model_alias": "sonnet",
+        "model_mapping": os.environ["ANTHROPIC_DEFAULT_SONNET_MODEL"],
+    }
+    return {
+        "source": source,
+        "installed": installed,
+        "profiles": profiles,
+        "settings": settings,
+        "other_installed_digest": digest(other),
+        "other_installed_entries": len(other),
+        "project_mirrors": mirrors,
+        "binding": binding,
+        "roster": sorted(EXPECTED),
+    }
+
 
 def verify_backup(before):
-    backup=OUT/'installed-skill-before.tar.gz'
-    assert stat.S_IMODE(backup.stat().st_mode)==0o600
-    with tarfile.open(backup,'r:gz') as archive:
-        actual={}
+    backup = OUT / "installed-skill-before.tar.gz"
+    assert stat.S_IMODE(backup.stat().st_mode) == 0o600
+    with tarfile.open(backup, "r:gz") as archive:
+        actual = {}
         for member in archive.getmembers():
-            rel=str(Path(member.name).relative_to(TARGET.name))
-            if member.isdir(): actual[rel]={'kind':'dir','mode':member.mode}
+            rel = str(Path(member.name).relative_to(TARGET.name))
+            if member.isdir():
+                actual[rel] = {"kind": "dir", "mode": member.mode}
             elif member.isfile():
-                with archive.extractfile(member) as stream: actual[rel]={'kind':'file','mode':member.mode,'size':member.size,'sha256':hash_stream(stream)}
-            else: raise AssertionError('Unexpected archive member type')
-    assert actual==before['installed'],'Archive does not preserve every byte/type/mode'
-    return {'path':'./artifacts/installed-skill-before.tar.gz',**file_state(backup)}
-
-phase=sys.argv[1]
-if phase=='before':
-    state=current()
-    drift=sorted(k for k in set(state['source'])|set(state['installed']) if state['source'].get(k)!=state['installed'].get(k))
-    assert drift==EXPECTED_DRIFT,drift
-    assert set(state['source'])==set(state['installed']),'Unexpected extra or missing entry'
-    assert contract_roster(TARGET/'SKILL.md')==EXPECTED-{'mcp__litellm__augment_code-augment_code_search'}
-    backup=OUT/'installed-skill-before.tar.gz'
-    assert not backup.exists(),'Do not overwrite an existing backup; inspect resume evidence'
-    with tarfile.open(backup,'w:gz') as archive: archive.add(TARGET,arcname=TARGET.name,recursive=True)
-    os.chmod(backup,0o600)
-    state['backup']=verify_backup(state); state['differing_files']=drift
-    (OUT/'compatibility-before.json').write_text(json.dumps(state,indent=2)+'\n')
-    (OUT/'authorization-and-binding.json').write_text(json.dumps({'owner_message':'msg_fbc81030bd4f','owner_provenance':'2026-11-09T14:12UTC direct genuine owner message relayed by coordinator:441 pr469 authorized; checked compatibility only','scope':'No permissions/profile/tool/gate broadening; normal one-skill installer; old failures/caps preserved; no merge/closure','binding':state['binding'],'source_target_verified':True,'profile_roster':state['roster'],'backup':state['backup']},indent=2)+'\n')
-    print(json.dumps({'phase':'before','drift':drift,'backup_verified':True,'archive_mode':'0600','file_entries':len(state['installed']),'profiles_settings_unchanged':True}))
-elif phase in ('guard','after','verify'):
-    before=json.loads((OUT/'compatibility-before.json').read_text()); state=current()
-    assert verify_backup(before)==before['backup']
-    for key in ('source','profiles','settings','other_installed_digest','other_installed_entries','project_mirrors','binding','roster'): assert state[key]==before[key],key+' changed'
-    if phase=='guard':
-        assert state['installed']==before['installed'],'Target changed since backup'
-        print(json.dumps({'phase':'guard','all_prerequisites_unchanged':True,'backup_reverified':True}))
+                with archive.extractfile(member) as stream:
+                    actual[rel] = {
+                        "kind": "file",
+                        "mode": member.mode,
+                        "size": member.size,
+                        "sha256": hash_stream(stream),
+                    }
+            else:
+                raise AssertionError("Unexpected archive member type")
+    assert actual == before["installed"], (
+        "Archive does not preserve every byte/type/mode"
+    )
+    return {"path": "./artifacts/installed-skill-before.tar.gz", **file_state(backup)}
+
+
+phase = sys.argv[1]
+if phase == "before":
+    state = current()
+    keys = set(state["source"]) | set(state["installed"])
+    assert set(state["source"]) == set(state["installed"]), (
+        "Unexpected extra or missing entry"
+    )
+    assert all(
+        state["source"][k]["kind"] == state["installed"][k]["kind"] for k in keys
+    ), "Entry type drift"
+    drift = sorted(
+        k
+        for k in keys
+        if state["source"][k].get("sha256") != state["installed"][k].get("sha256")
+    )
+    mode_changes = {
+        k: {
+            "source": state["source"][k]["mode"],
+            "installed": state["installed"][k]["mode"],
+        }
+        for k in sorted(keys)
+        if state["source"][k]["mode"] != state["installed"][k]["mode"]
+    }
+    assert all((v["source"] & ~v["installed"]) == 0 for v in mode_changes.values()), (
+        "Normal refresh would broaden filesystem permissions"
+    )
+    state["selected_mode_tightening"] = mode_changes
+    # Plan Task 1: stop on any drift beyond the three stale files. The only mode difference
+    # allowed is the exact owner-authorized set above (decision A), value for value.
+    if drift != EXPECTED_DRIFT or mode_changes != AUTHORIZED_MODE_TIGHTENING:
+        keys = set(state["source"]) | set(state["installed"])
+        state["observed_drift"] = drift
+        state["content_drift"] = sorted(
+            k
+            for k in keys
+            if state["source"].get(k, {}).get("sha256")
+            != state["installed"].get(k, {}).get("sha256")
+        )
+        state["mode_drift"] = sorted(
+            k
+            for k in keys
+            if state["source"].get(k, {}).get("mode")
+            != state["installed"].get(k, {}).get("mode")
+        )
+        (OUT / "blocked-before-state.json").write_text(
+            json.dumps(state, indent=2) + "\n"
+        )
+        print(
+            json.dumps(
+                {
+                    "phase": "blocked_before",
+                    "content_drift": state["content_drift"],
+                    "mode_drift_count": len(state["mode_drift"]),
+                    "examples": {
+                        k: {
+                            "source": oct(state["source"][k]["mode"]),
+                            "installed": oct(state["installed"][k]["mode"]),
+                        }
+                        for k in state["mode_drift"][:5]
+                    },
+                    "installer_run": False,
+                    "backup_exists": (OUT / "installed-skill-before.tar.gz").exists(),
+                }
+            )
+        )
+        raise AssertionError(
+            "Unexpected metadata drift; preserved state, no installation"
+        )
+    assert set(state["source"]) == set(state["installed"]), (
+        "Unexpected extra or missing entry"
+    )
+    assert contract_roster(TARGET / "SKILL.md") == EXPECTED - {
+        "mcp__litellm__augment_code-augment_code_search"
+    }
+    backup = OUT / "installed-skill-before.tar.gz"
+    # A backup from the first run is never overwritten: a re-run must prove the existing
+    # backup still matches the (unchanged) installed folder byte for byte, type and mode.
+    state["backup_reused"] = backup.exists()
+    if not backup.exists():
+        with tarfile.open(backup, "w:gz") as archive:
+            archive.add(TARGET, arcname=TARGET.name, recursive=True)
+        os.chmod(backup, 0o600)
+    state["backup"] = verify_backup(state)
+    state["differing_files"] = drift
+    old_before = OUT / "compatibility-before.json"
+    if old_before.exists():
+        prev = json.loads(old_before.read_text())
+        if "rebaseline" in prev:
+            state["rebaseline"] = prev["rebaseline"]
+    state["owner_decision_A"] = OWNER_DECISION_A
+    state["owner_decision_B"] = OWNER_DECISION_B
+    (OUT / "compatibility-before.json").write_text(json.dumps(state, indent=2) + "\n")
+    (OUT / "authorization-and-binding.json").write_text(
+        json.dumps(
+            {
+                "owner_message": "msg_fbc81030bd4f",
+                "owner_provenance": "2026-11-09T14:12UTC direct genuine owner message relayed by coordinator:441 pr469 authorized; checked compatibility only",
+                "scope": "No permissions/profile/tool/gate broadening; normal one-skill installer; old failures/caps preserved; no merge/closure",
+                "owner_decision_A": OWNER_DECISION_A,
+                "owner_decision_B": OWNER_DECISION_B,
+                "binding": state["binding"],
+                "source_target_verified": True,
+                "profile_roster": state["roster"],
+                "backup": state["backup"],
+            },
+            indent=2,
+        )
+        + "\n"
+    )
+    print(
+        json.dumps(
+            {
+                "phase": "before",
+                "drift": drift,
+                "backup_verified": True,
+                "archive_mode": "0600",
+                "file_entries": len(state["installed"]),
+                "profiles_settings_unchanged": True,
+            }
+        )
+    )
+elif phase in ("guard", "after", "verify"):
+    before = json.loads((OUT / "compatibility-before.json").read_text())
+    state = current()
+    assert verify_backup(before) == before["backup"]
+    for key in (
+        "source",
+        "profiles",
+        "settings",
+        "other_installed_digest",
+        "other_installed_entries",
+        "project_mirrors",
+        "binding",
+        "roster",
+    ):
+        assert state[key] == before[key], key + " changed"
+    if phase == "guard":
+        assert state["installed"] == before["installed"], "Target changed since backup"
+        print(
+            json.dumps(
+                {
+                    "phase": "guard",
+                    "all_prerequisites_unchanged": True,
+                    "backup_reverified": True,
+                }
+            )
+        )
     else:
-        assert state['installed']==state['source'],'Installed package not exactly canonical'
-        changed=sorted(k for k in state['installed'] if state['installed'][k]!=before['installed'][k])
-        assert changed==EXPECTED_DRIFT,changed
-        assert contract_roster(TARGET/'SKILL.md')==EXPECTED
-        state.update({'changed_files':changed,'protected_invariants_unchanged':True,'exact_canonical_parity':True,'backup':before['backup']})
-        if phase=='after':
-            (OUT/'compatibility-after.json').write_text(json.dumps(state,indent=2)+'\n')
+        assert state["installed"] == state["source"], (
+            "Installed package not exactly canonical"
+        )
+        changed = sorted(
+            k
+            for k in state["installed"]
+            if state["installed"][k].get("sha256")
+            != before["installed"][k].get("sha256")
+        )
+        assert changed == EXPECTED_DRIFT, changed
+        assert contract_roster(TARGET / "SKILL.md") == EXPECTED
+        state.update(
+            {
+                "changed_files": changed,
+                "selected_mode_tightening": before["selected_mode_tightening"],
+                "protected_invariants_unchanged": True,
+                "exact_canonical_parity": True,
+                "backup": before["backup"],
+            }
+        )
+        if phase == "after":
+            (OUT / "compatibility-after.json").write_text(
+                json.dumps(state, indent=2) + "\n"
+            )
         else:
-            assert state==json.loads((OUT/'compatibility-after.json').read_text()),'Live state changed after recorded installation'
-        print(json.dumps({'phase':phase,'exact_canonical_parity':True,'changed_files':changed,'protected_invariants_unchanged':True}))
-else: raise ValueError(phase)
+            assert state == json.loads(
+                (OUT / "compatibility-after.json").read_text()
+            ), "Live state changed after recorded installation"
+        print(
+            json.dumps(
+                {
+                    "phase": phase,
+                    "exact_canonical_parity": True,
+                    "changed_files": changed,
+                    "protected_invariants_unchanged": True,
+                }
+            )
+        )
+else:
+    raise ValueError(phase)
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/pr-state-before.json b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/pr-state-before.json
new file mode 100644
index 000000000..aede133db
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/pr-state-before.json
@@ -0,0 +1 @@
+{"headRefOid":"94e609ccef2a5ee67fa8918426157046be1f32c8","isDraft":true,"state":"OPEN","url":"https://github.com/IronbellyOrg/IronClaude/pull/469"}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/rebaseline-record.json b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/rebaseline-record.json
new file mode 100644
index 000000000..24303de48
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/rebaseline-record.json
@@ -0,0 +1,51 @@
+{
+  "reason": "Files outside the plan changed after the baseline; not made by this run.",
+  "approval": {
+    "ask_message": "msg_396f577fa3cd",
+    "answer_message": "msg_da4599a5fd9c",
+    "answer_text": "ok",
+    "interpretation": "Literal answer 'ok' to a question that recommended rebaseline-and-continue; read as approval of that option."
+  },
+  "settings_global": {
+    "path": "/home/coder/.claude/settings.json",
+    "old_sha256": "e0c2e76c60cfdd98dacdf6d751782c619875fb4c858f5037858af2e1a883f761",
+    "new_sha256": "b39dd56864118734fa84bf885f45efcf9d0a8ddd9357be9f6b8793de39c47d06",
+    "pre_change_copy": "/home/coder/.claude/settings.json.bak",
+    "top_level_keys_changed": [
+      "hooks",
+      "model"
+    ],
+    "permissions_equal": true,
+    "model_old": "claude-gw-tier1b[1m]",
+    "model_new": "claude-gw-gpt-6-luna[1m]",
+    "hooks_same_set": true
+  },
+  "other_installed": {
+    "old_entries": 45,
+    "new_entries": 46,
+    "old_digest": "55c0781e55cedb83fa5cb02e3cdfc8a8421288bb9d3b37b56f12cca971947b77",
+    "new_digest": "aee68bf0b5fc006765e8299de6a7283e73fd29830836c140a939934813fdc64c",
+    "known_new_entry": "setup-bmad (created 2026-11-09T16:03Z, after the baseline at 15:43Z)"
+  },
+  "unchanged_and_rechecked": [
+    "source",
+    "installed",
+    "profiles",
+    "project_mirrors",
+    "binding",
+    "roster",
+    "backup"
+  ],
+  "owner_decision_B": {
+    "source": "owner reply '1' at 2026-11-10T00:02Z, relayed by the coordinator (earlier coordinator message msg_bf66b7bcfc84 approved the same rebaseline-and-continue)",
+    "provenance": "the owner ran /model in the coordinator session on 2026-11-09 ~19:38Z; the default model changed and was saved (observed diff: the model key changed and hook entries were reordered, same set of hooks); setup-bmad is an unrelated tooling skill",
+    "conditions": [
+      "record old/new hashes with this provenance",
+      "fresh reviewer checks the diff",
+      "re-take the before-state",
+      "install ONLY sc-troubleshoot-protocol",
+      "afterwards verify ~/.claude/settings.json, ~/.claude/skills/setup-bmad and every unrelated file byte-identical to the before-state"
+    ],
+    "before_state_retaken": "compatibility-before.json (phase before re-run 2026-11-10, settings sha256 b39dd568...)"
+  }
+}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/rebaseline.py b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/rebaseline.py
new file mode 100644
index 000000000..d375c5722
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/rebaseline.py
@@ -0,0 +1,77 @@
+"""Re-baseline only the externally drifted fields. Never installs, never touches the backup.
+
+Run: uv run python -I <this file>   (from the repo root)
+Reuses current() from compatibility_state.py without running its phase dispatch.
+"""
+
+import json
+import shutil
+import sys
+from pathlib import Path
+
+HERE = Path(__file__).resolve().parent
+src = (HERE / "compatibility_state.py").read_text().split("\nphase = sys.argv[1]")[0]
+ns = {"__name__": "compatibility_state_lib"}
+sys.argv = ["compatibility_state.py", "lib"]
+exec(compile(src, str(HERE / "compatibility_state.py"), "exec"), ns)
+
+before_path = HERE / "compatibility-before.json"
+original = HERE / "compatibility-before.original.json"
+assert not original.exists(), "already re-baselined; inspect evidence"
+before = json.loads(before_path.read_text())
+state = ns["current"]()
+assert ns["verify_backup"](before) == before["backup"], "backup no longer verifies"
+
+DRIFT_KEYS = ("settings", "other_installed_digest", "other_installed_entries")
+for key in before:
+    if key in DRIFT_KEYS or key in ("backup", "selected_mode_tightening", "differing_files"):
+        continue
+    assert state[key] == before[key], key + " changed beyond the approved drift"
+assert state["installed"] == before["installed"], "target changed since backup"
+
+home = Path("/home/coder/.claude")
+moved = [p for p in before["settings"] if state["settings"][p] != before["settings"][p]]
+assert moved == [str(home / "settings.json")], moved  # only the global file may differ
+old =json.loads((home / "settings.json.bak").read_text())
+new = json.loads((home / "settings.json").read_text())
+old_sha = before["settings"][str(home / "settings.json")]["sha256"]
+bak_sha = ns["file_state"](home / "settings.json.bak")["sha256"]
+assert bak_sha == old_sha, "settings.json.bak is not the baseline copy"
+changed_keys = sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))
+record = {
+    "reason": "Files outside the plan changed after the baseline; not made by this run.",
+    "approval": {
+        "ask_message": "msg_396f577fa3cd",
+        "answer_message": "msg_da4599a5fd9c",
+        "answer_text": "ok",
+        "interpretation": "Literal answer 'ok' to a question that recommended rebaseline-and-continue; read as approval of that option.",
+    },
+    "settings_global": {
+        "path": str(home / "settings.json"),
+        "old_sha256": old_sha,
+        "new_sha256": new and state["settings"][str(home / "settings.json")]["sha256"],
+        "pre_change_copy": str(home / "settings.json.bak"),
+        "top_level_keys_changed": changed_keys,
+        "permissions_equal": old.get("permissions") == new.get("permissions"),
+        "model_old": old.get("model"),
+        "model_new": new.get("model"),
+        "hooks_same_set": sorted(json.dumps(x, sort_keys=True) for v in old.get("hooks", {}).values() for x in v)
+        == sorted(json.dumps(x, sort_keys=True) for v in new.get("hooks", {}).values() for x in v),
+    },
+    "other_installed": {
+        "old_entries": before["other_installed_entries"],
+        "new_entries": state["other_installed_entries"],
+        "old_digest": before["other_installed_digest"],
+        "new_digest": state["other_installed_digest"],
+        "known_new_entry": "setup-bmad (created 2026-11-09T16:03Z, after the baseline at 15:43Z)",
+    },
+    "unchanged_and_rechecked": [
+        "source", "installed", "profiles", "project_mirrors", "binding", "roster", "backup",
+    ],
+}
+shutil.copy2(before_path, original)
+before.update({k: state[k] for k in DRIFT_KEYS})
+before["rebaseline"] = record
+before_path.write_text(json.dumps(before, indent=2) + "\n")
+(HERE / "rebaseline-record.json").write_text(json.dumps(record, indent=2) + "\n")
+print(json.dumps({k: record[k] for k in ("settings_global", "other_installed")}, indent=2))
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/task1-proof.log b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/task1-proof.log
new file mode 100644
index 000000000..876b3d01d
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/task1-proof.log
@@ -0,0 +1 @@
+{"backup_sha256": "77e304762480a13a83589c62f3ca1dc8ddf8cd4ab3b0b0afc7920ec2341a3707", "backup_mode": "0o600", "content_drift": ["SKILL.md", "refs/diagnosability-audit.md", "refs/doc-discovery.md"], "mode_only_tightening": 19, "installed_profiles_settings_mirrors_unchanged_since_first_attempt": true}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/progress.md b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/progress.md
new file mode 100644
index 000000000..80d4b0634
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/progress.md
@@ -0,0 +1,3 @@
+# implement ledger — source: ./TASK-WF-diagnosticRefres-20261109-144413.md — created: 2026-11-09T15:33:35Z
+PLAN: sha256=f497896cc273c8a3976876b6f9fb08865a210cd6817a4c5b688f7ecfc7f72a4c source_sha256=f4be1c7f599cc933868fcf4181d0e9895045870787749eb3e208260391542da4
+T1: start sha=8365c62c3b202c1af844fd81a67754e15788d65a

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/authorization-and-binding.json b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/authorization-and-binding.json
index 592096709..6150fdd07 100644
--- a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/authorization-and-binding.json
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/authorization-and-binding.json
@@ -2,6 +2,38 @@
   "owner_message": "msg_fbc81030bd4f",
   "owner_provenance": "2026-11-09T14:12UTC direct genuine owner message relayed by coordinator:441 pr469 authorized; checked compatibility only",
   "scope": "No permissions/profile/tool/gate broadening; normal one-skill installer; old failures/caps preserved; no merge/closure",
+  "owner_decision_A": {
+    "decision": "A: mode-only exception for the 19 install-skill entries AUTHORIZED",
+    "source": "owner reply '1' at 2026-11-10T00:02Z, relayed by the coordinator",
+    "verbatim": "(A) AUTHORIZED: the mode-only exception for the 19 install-skill entries (2 directories, 17 refs files; source 700/600 vs installed 755/644; the install makes installed copies stricter). It covers ONLY those 19 entries and ONLY mode differences. Any other drift, any content-hash difference, or any mode difference that loosens permissions = STOP and report.",
+    "count_note": "The recorded entry set is 3 directories (., refs, refs/probe-packs) and 16 files; the total of 19 and the mode pairs match the wording.",
+    "entries": [
+      ".",
+      "refs",
+      "refs/agent-assertions.md",
+      "refs/calibrator-eval-cases.md",
+      "refs/contract-enumeration.md",
+      "refs/effective-input-proof.md",
+      "refs/environment-deltas.md",
+      "refs/escalation-rubric.md",
+      "refs/hardening-output-contract.md",
+      "refs/hypothesis-card-template.md",
+      "refs/pipeline-hardening-closure.md",
+      "refs/primitive-differential.md",
+      "refs/probe-packs",
+      "refs/probe-packs/read-parse.md",
+      "refs/remediation-handoff.md",
+      "refs/report-template.md",
+      "refs/runtime-entrypoint-verification.md",
+      "refs/triage-checklist.md",
+      "refs/unmask-and-sweep.md"
+    ]
+  },
+  "owner_decision_B": {
+    "decision": "B: settings.json rebaseline stays approved with conditions",
+    "source": "owner reply '1' at 2026-11-10T00:02Z, relayed by the coordinator",
+    "provenance": "owner ran /model in the coordinator session on 2026-11-09 ~19:38Z; the default model changed and was saved; setup-bmad is an unrelated tooling skill"
+  },
   "binding": {
     "module": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/cli/install_skill.py",
     "module_state": {
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/authorization-and-binding.prev.json b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/authorization-and-binding.prev.json
new file mode 100644
index 000000000..592096709
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/authorization-and-binding.prev.json
@@ -0,0 +1,39 @@
+{
+  "owner_message": "msg_fbc81030bd4f",
+  "owner_provenance": "2026-11-09T14:12UTC direct genuine owner message relayed by coordinator:441 pr469 authorized; checked compatibility only",
+  "scope": "No permissions/profile/tool/gate broadening; normal one-skill installer; old failures/caps preserved; no merge/closure",
+  "binding": {
+    "module": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/cli/install_skill.py",
+    "module_state": {
+      "kind": "file",
+      "mode": 384,
+      "size": 4197,
+      "sha256": "dba905ac3d3e7407f380146ada15cffa957d174e3371a5140a1fc2d06e3537c8"
+    },
+    "source": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-troubleshoot-protocol",
+    "target": "/home/coder/.claude/skills/sc-troubleshoot-protocol",
+    "source_realpath": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-troubleshoot-protocol",
+    "target_realpath": "/home/coder/.claude/skills/sc-troubleshoot-protocol",
+    "model_alias": "sonnet",
+    "model_mapping": "claude-gw-tier1b[1m]"
+  },
+  "source_target_verified": true,
+  "profile_roster": [
+    "Glob",
+    "Grep",
+    "Read",
+    "mcp__auggie__codebase-retrieval",
+    "mcp__codegraph__codegraph_callers",
+    "mcp__codegraph__codegraph_impact",
+    "mcp__codegraph__codegraph_node",
+    "mcp__codegraph__codegraph_search",
+    "mcp__litellm__augment_code-augment_code_search"
+  ],
+  "backup": {
+    "path": "./artifacts/installed-skill-before.tar.gz",
+    "kind": "file",
+    "mode": 384,
+    "size": 106556,
+    "sha256": "77e304762480a13a83589c62f3ca1dc8ddf8cd4ab3b0b0afc7920ec2341a3707"
+  }
+}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/before-rerun.log b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/before-rerun.log
new file mode 100644
index 000000000..1b9228731
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/before-rerun.log
@@ -0,0 +1 @@
+{"phase": "before", "drift": ["SKILL.md", "refs/diagnosability-audit.md", "refs/doc-discovery.md"], "backup_verified": true, "archive_mode": "0600", "file_entries": 22, "profiles_settings_unchanged": true}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-before.json b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-before.json
index 61e9a0bec..a1d2c89ca 100644
--- a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-before.json
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-before.json
@@ -408,6 +408,7 @@
       "installed": 420
     }
   },
+  "backup_reused": true,
   "backup": {
     "path": "./artifacts/installed-skill-before.tar.gz",
     "kind": "file",
@@ -458,5 +459,37 @@
       "roster",
       "backup"
     ]
+  },
+  "owner_decision_A": {
+    "decision": "A: mode-only exception for the 19 install-skill entries AUTHORIZED",
+    "source": "owner reply '1' at 2026-11-10T00:02Z, relayed by the coordinator",
+    "verbatim": "(A) AUTHORIZED: the mode-only exception for the 19 install-skill entries (2 directories, 17 refs files; source 700/600 vs installed 755/644; the install makes installed copies stricter). It covers ONLY those 19 entries and ONLY mode differences. Any other drift, any content-hash difference, or any mode difference that loosens permissions = STOP and report.",
+    "count_note": "The recorded entry set is 3 directories (., refs, refs/probe-packs) and 16 files; the total of 19 and the mode pairs match the wording.",
+    "entries": [
+      ".",
+      "refs",
+      "refs/agent-assertions.md",
+      "refs/calibrator-eval-cases.md",
+      "refs/contract-enumeration.md",
+      "refs/effective-input-proof.md",
+      "refs/environment-deltas.md",
+      "refs/escalation-rubric.md",
+      "refs/hardening-output-contract.md",
+      "refs/hypothesis-card-template.md",
+      "refs/pipeline-hardening-closure.md",
+      "refs/primitive-differential.md",
+      "refs/probe-packs",
+      "refs/probe-packs/read-parse.md",
+      "refs/remediation-handoff.md",
+      "refs/report-template.md",
+      "refs/runtime-entrypoint-verification.md",
+      "refs/triage-checklist.md",
+      "refs/unmask-and-sweep.md"
+    ]
+  },
+  "owner_decision_B": {
+    "decision": "B: settings.json rebaseline stays approved with conditions",
+    "source": "owner reply '1' at 2026-11-10T00:02Z, relayed by the coordinator",
+    "provenance": "owner ran /model in the coordinator session on 2026-11-09 ~19:38Z; the default model changed and was saved; setup-bmad is an unrelated tooling skill"
   }
 }
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-before.rebaselined.json b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-before.rebaselined.json
new file mode 100644
index 000000000..61e9a0bec
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-before.rebaselined.json
@@ -0,0 +1,462 @@
+{
+  "source": {
+    ".": {
+      "kind": "dir",
+      "mode": 448
+    },
+    "SKILL.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 133005,
+      "sha256": "0dd9d33fbdf6fc398cb717bd491587e3a5e4119eaa609336c6823128479acb9a"
+    },
+    "refs": {
+      "kind": "dir",
+      "mode": 448
+    },
+    "refs/agent-assertions.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 5957,
+      "sha256": "7bcd5b7c17957a903baee9933bcffb04adebfb093163576731a37cfecf8407fa"
+    },
+    "refs/calibrator-eval-cases.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 5256,
+      "sha256": "ef705ec12e75d8d91731013bb81416c7acca36744f8a433dc4dd9e3d9d16ffba"
+    },
+    "refs/contract-enumeration.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 2831,
+      "sha256": "8cf9c1e6fe6a086cbc2055f78ae07ee8fa2815eb1cce8e6918b4d68dd0433d5e"
+    },
+    "refs/diagnosability-audit.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 38873,
+      "sha256": "e86a3a4124c359c51827bbfbe5195bbe7c9670257a5121854c0cd94be32302d1"
+    },
+    "refs/doc-discovery.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 9312,
+      "sha256": "0b9d5a38b1ac4fb0fc7c9e62846a486e3ba799990c1cb44e2ddee3daaa88d8cd"
+    },
+    "refs/effective-input-proof.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 1872,
+      "sha256": "f40412b36e13a5271bb5b426376efe2b837ff0d09c7e78c0b7ad61f19c95853c"
+    },
+    "refs/environment-deltas.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 2188,
+      "sha256": "a868fd374ec2c84981e2b7bde02334f9b75cf9f64a6b7abee9e028e63205ecff"
+    },
+    "refs/escalation-rubric.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 8058,
+      "sha256": "c72b5afc2c6b85cc979e5c071399d2c5825aae08d06e659d36c9b105b1067037"
+    },
+    "refs/hardening-output-contract.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 9819,
+      "sha256": "0a477f3addde441a0b617b909d0e1660bbb1b526dd7e5503d4d8c4731ee0faa6"
+    },
+    "refs/hypothesis-card-template.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 16316,
+      "sha256": "cfad9e91ac7816b22d1d3d5bc1c7db70c544a7a0783e63cabe0d3d0d253ee8cb"
+    },
+    "refs/pipeline-hardening-closure.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 7284,
+      "sha256": "597db5c60bc2e28f11ddd9062eb59e3180307f4b6db5a950cb69c3f9004f5625"
+    },
+    "refs/primitive-differential.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 6149,
+      "sha256": "12d8a49e5ee2749b56b822028f6676940eb57655c9852fa85273444d0c5156ce"
+    },
+    "refs/probe-packs": {
+      "kind": "dir",
+      "mode": 448
+    },
+    "refs/probe-packs/read-parse.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 632,
+      "sha256": "95f0397e7eb5f0620764ac77a475ce8b405018eb0841b42c25e19e569f993498"
+    },
+    "refs/remediation-handoff.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 16290,
+      "sha256": "aebafa75d8b1998a2e8573028cae63b7497fd25202e51afca245fb57d73610b1"
+    },
+    "refs/report-template.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 28985,
+      "sha256": "faa943d063f4078e3c9c5a5b58145fd530ed79a03a2296d6a4f23f71c838d7ce"
+    },
+    "refs/runtime-entrypoint-verification.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 3609,
+      "sha256": "d83f98cba7130cb0c61a5beda16c9d33420b22466de4c84781e886e94759a971"
+    },
+    "refs/triage-checklist.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 7584,
+      "sha256": "847c8a198ffff5818bbfedf4a7f6c21dae4b854ffcaa82223d31e6b8c4a5a19d"
+    },
+    "refs/unmask-and-sweep.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 3971,
+      "sha256": "460e1b8305242aeb085f6c426bfe2c50fbb8983050173b4d3cbde8437ebd2be8"
+    }
+  },
+  "installed": {
+    ".": {
+      "kind": "dir",
+      "mode": 493
+    },
+    "SKILL.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 131516,
+      "sha256": "6d1b226cba4c2fbe9dae7bcbbfe954ee9463a20473e4e33bdc679cda39b2f3e5"
+    },
+    "refs": {
+      "kind": "dir",
+      "mode": 493
+    },
+    "refs/agent-assertions.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5957,
+      "sha256": "7bcd5b7c17957a903baee9933bcffb04adebfb093163576731a37cfecf8407fa"
+    },
+    "refs/calibrator-eval-cases.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5256,
+      "sha256": "ef705ec12e75d8d91731013bb81416c7acca36744f8a433dc4dd9e3d9d16ffba"
+    },
+    "refs/contract-enumeration.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 2831,
+      "sha256": "8cf9c1e6fe6a086cbc2055f78ae07ee8fa2815eb1cce8e6918b4d68dd0433d5e"
+    },
+    "refs/diagnosability-audit.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 38706,
+      "sha256": "953901f262b0f4092297e03d3611e3c14cc678ed3d7072c55e604c8cd30ad944"
+    },
+    "refs/doc-discovery.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 9256,
+      "sha256": "57c0795ca5bec46c51cadf4ae02f156e3a112b2f592081921eeb4c729379e9aa"
+    },
+    "refs/effective-input-proof.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 1872,
+      "sha256": "f40412b36e13a5271bb5b426376efe2b837ff0d09c7e78c0b7ad61f19c95853c"
+    },
+    "refs/environment-deltas.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 2188,
+      "sha256": "a868fd374ec2c84981e2b7bde02334f9b75cf9f64a6b7abee9e028e63205ecff"
+    },
+    "refs/escalation-rubric.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 8058,
+      "sha256": "c72b5afc2c6b85cc979e5c071399d2c5825aae08d06e659d36c9b105b1067037"
+    },
+    "refs/hardening-output-contract.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 9819,
+      "sha256": "0a477f3addde441a0b617b909d0e1660bbb1b526dd7e5503d4d8c4731ee0faa6"
+    },
+    "refs/hypothesis-card-template.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 16316,
+      "sha256": "cfad9e91ac7816b22d1d3d5bc1c7db70c544a7a0783e63cabe0d3d0d253ee8cb"
+    },
+    "refs/pipeline-hardening-closure.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 7284,
+      "sha256": "597db5c60bc2e28f11ddd9062eb59e3180307f4b6db5a950cb69c3f9004f5625"
+    },
+    "refs/primitive-differential.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 6149,
+      "sha256": "12d8a49e5ee2749b56b822028f6676940eb57655c9852fa85273444d0c5156ce"
+    },
+    "refs/probe-packs": {
+      "kind": "dir",
+      "mode": 493
+    },
+    "refs/probe-packs/read-parse.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 632,
+      "sha256": "95f0397e7eb5f0620764ac77a475ce8b405018eb0841b42c25e19e569f993498"
+    },
+    "refs/remediation-handoff.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 16290,
+      "sha256": "aebafa75d8b1998a2e8573028cae63b7497fd25202e51afca245fb57d73610b1"
+    },
+    "refs/report-template.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 28985,
+      "sha256": "faa943d063f4078e3c9c5a5b58145fd530ed79a03a2296d6a4f23f71c838d7ce"
+    },
+    "refs/runtime-entrypoint-verification.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 3609,
+      "sha256": "d83f98cba7130cb0c61a5beda16c9d33420b22466de4c84781e886e94759a971"
+    },
+    "refs/triage-checklist.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 7584,
+      "sha256": "847c8a198ffff5818bbfedf4a7f6c21dae4b854ffcaa82223d31e6b8c4a5a19d"
+    },
+    "refs/unmask-and-sweep.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 3971,
+      "sha256": "460e1b8305242aeb085f6c426bfe2c50fbb8983050173b4d3cbde8437ebd2be8"
+    }
+  },
+  "profiles": {
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/agents/troubleshoot-analyst.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5306,
+      "sha256": "fe25f8713a400250cd2ed7387ae0c30d32e787318cb41f6034bb2f70a9767f44"
+    },
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/.claude/agents/troubleshoot-analyst.md": {
+      "kind": "file",
+      "mode": 384,
+      "size": 5306,
+      "sha256": "fe25f8713a400250cd2ed7387ae0c30d32e787318cb41f6034bb2f70a9767f44"
+    },
+    "/home/coder/.claude/agents/troubleshoot-analyst.md": {
+      "kind": "file",
+      "mode": 420,
+      "size": 5258,
+      "sha256": "a952b4060db11be65b5bac546c6af3f2422615bc5cc3433179560a1d23c61213"
+    }
+  },
+  "settings": {
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/.claude/settings.json": {
+      "kind": "file",
+      "mode": 384,
+      "size": 1632,
+      "sha256": "1f535104e6bb9145585a88418d0a094a4b38d6432e3b5fbd6226d550da33d41c"
+    },
+    "/home/coder/workspaces/worktrees/IronClaude/issue-441/.claude/settings.local.json": {
+      "kind": "absent"
+    },
+    "/home/coder/.claude/settings.json": {
+      "kind": "file",
+      "mode": 420,
+      "size": 55663,
+      "sha256": "b39dd56864118734fa84bf885f45efcf9d0a8ddd9357be9f6b8793de39c47d06"
+    },
+    "/home/coder/.claude/settings.local.json": {
+      "kind": "absent"
+    }
+  },
+  "other_installed_digest": "aee68bf0b5fc006765e8299de6a7283e73fd29830836c140a939934813fdc64c",
+  "other_installed_entries": 46,
+  "project_mirrors": {
+    "skills": "474014884b6aaea81afc9519a245c844fcebb9b7fef3e9a32246c64dae0084b0",
+    "agents": "17f317b9b649b82789e5ce1c629f79743bcb20b3c5c84f57060fe5f431ab7c71",
+    "commands": "7f3c2978d5181c7fb2071df9082046a3410fb476b64f74d6e6ec9b380b6bd2ca",
+    "hooks": "32b821fa8cbf12814d9a1717baef1e8a0eb260f9339c5af7b1b9e20f587fe767",
+    "templates": "0388b1822767a0ee29d0e3c5171aedb524a795eb23173d084c1ebb4c7cff0eda"
+  },
+  "binding": {
+    "module": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/cli/install_skill.py",
+    "module_state": {
+      "kind": "file",
+      "mode": 384,
+      "size": 4197,
+      "sha256": "dba905ac3d3e7407f380146ada15cffa957d174e3371a5140a1fc2d06e3537c8"
+    },
+    "source": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-troubleshoot-protocol",
+    "target": "/home/coder/.claude/skills/sc-troubleshoot-protocol",
+    "source_realpath": "/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-troubleshoot-protocol",
+    "target_realpath": "/home/coder/.claude/skills/sc-troubleshoot-protocol",
+    "model_alias": "sonnet",
+    "model_mapping": "claude-gw-tier1b[1m]"
+  },
+  "roster": [
+    "Glob",
+    "Grep",
+    "Read",
+    "mcp__auggie__codebase-retrieval",
+    "mcp__codegraph__codegraph_callers",
+    "mcp__codegraph__codegraph_impact",
+    "mcp__codegraph__codegraph_node",
+    "mcp__codegraph__codegraph_search",
+    "mcp__litellm__augment_code-augment_code_search"
+  ],
+  "selected_mode_tightening": {
+    ".": {
+      "source": 448,
+      "installed": 493
+    },
+    "refs": {
+      "source": 448,
+      "installed": 493
+    },
+    "refs/agent-assertions.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/calibrator-eval-cases.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/contract-enumeration.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/effective-input-proof.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/environment-deltas.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/escalation-rubric.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/hardening-output-contract.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/hypothesis-card-template.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/pipeline-hardening-closure.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/primitive-differential.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/probe-packs": {
+      "source": 448,
+      "installed": 493
+    },
+    "refs/probe-packs/read-parse.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/remediation-handoff.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/report-template.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/runtime-entrypoint-verification.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/triage-checklist.md": {
+      "source": 384,
+      "installed": 420
+    },
+    "refs/unmask-and-sweep.md": {
+      "source": 384,
+      "installed": 420
+    }
+  },
+  "backup": {
+    "path": "./artifacts/installed-skill-before.tar.gz",
+    "kind": "file",
+    "mode": 384,
+    "size": 106556,
+    "sha256": "77e304762480a13a83589c62f3ca1dc8ddf8cd4ab3b0b0afc7920ec2341a3707"
+  },
+  "differing_files": [
+    "SKILL.md",
+    "refs/diagnosability-audit.md",
+    "refs/doc-discovery.md"
+  ],
+  "rebaseline": {
+    "reason": "Files outside the plan changed after the baseline; not made by this run.",
+    "approval": {
+      "ask_message": "msg_396f577fa3cd",
+      "answer_message": "msg_da4599a5fd9c",
+      "answer_text": "ok",
+      "interpretation": "Literal answer 'ok' to a question that recommended rebaseline-and-continue; read as approval of that option."
+    },
+    "settings_global": {
+      "path": "/home/coder/.claude/settings.json",
+      "old_sha256": "e0c2e76c60cfdd98dacdf6d751782c619875fb4c858f5037858af2e1a883f761",
+      "new_sha256": "b39dd56864118734fa84bf885f45efcf9d0a8ddd9357be9f6b8793de39c47d06",
+      "pre_change_copy": "/home/coder/.claude/settings.json.bak",
+      "top_level_keys_changed": [
+        "hooks",
+        "model"
+      ],
+      "permissions_equal": true,
+      "model_old": "claude-gw-tier1b[1m]",
+      "model_new": "claude-gw-gpt-6-luna[1m]",
+      "hooks_same_set": true
+    },
+    "other_installed": {
+      "old_entries": 45,
+      "new_entries": 46,
+      "old_digest": "55c0781e55cedb83fa5cb02e3cdfc8a8421288bb9d3b37b56f12cca971947b77",
+      "new_digest": "aee68bf0b5fc006765e8299de6a7283e73fd29830836c140a939934813fdc64c",
+      "known_new_entry": "setup-bmad (created 2026-11-09T16:03Z, after the baseline at 15:43Z)"
+    },
+    "unchanged_and_rechecked": [
+      "source",
+      "installed",
+      "profiles",
+      "project_mirrors",
+      "binding",
+      "roster",
+      "backup"
+    ]
+  }
+}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py
index 1a851c0e4..03cfb7258 100644
--- a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py
@@ -40,6 +40,57 @@ EXPECTED = {
     "mcp__codegraph__codegraph_impact",
 }
 EXPECTED_DRIFT = ["SKILL.md", "refs/diagnosability-audit.md", "refs/doc-discovery.md"]
+# Owner decision A (reply '1', 2026-11-10T00:02Z, relayed by the coordinator): exactly these
+# 19 entries may differ in mode only, source 0700/0600 against installed 0755/0644 (the
+# install tightens the installed copy). Any other mode difference, any loosening, or any
+# value other than these pairs stops the run.
+_DIRS = (".", "refs", "refs/probe-packs")
+_FILES = (
+    "refs/agent-assertions.md",
+    "refs/calibrator-eval-cases.md",
+    "refs/contract-enumeration.md",
+    "refs/effective-input-proof.md",
+    "refs/environment-deltas.md",
+    "refs/escalation-rubric.md",
+    "refs/hardening-output-contract.md",
+    "refs/hypothesis-card-template.md",
+    "refs/pipeline-hardening-closure.md",
+    "refs/primitive-differential.md",
+    "refs/probe-packs/read-parse.md",
+    "refs/remediation-handoff.md",
+    "refs/report-template.md",
+    "refs/runtime-entrypoint-verification.md",
+    "refs/triage-checklist.md",
+    "refs/unmask-and-sweep.md",
+)
+AUTHORIZED_MODE_TIGHTENING = {
+    **{k: {"source": 0o700, "installed": 0o755} for k in _DIRS},
+    **{k: {"source": 0o600, "installed": 0o644} for k in _FILES},
+}
+OWNER_DECISION_A = {
+    "decision": "A: mode-only exception for the 19 install-skill entries AUTHORIZED",
+    "source": "owner reply '1' at 2026-11-10T00:02Z, relayed by the coordinator",
+    "verbatim": (
+        "(A) AUTHORIZED: the mode-only exception for the 19 install-skill entries "
+        "(2 directories, 17 refs files; source 700/600 vs installed 755/644; the install "
+        "makes installed copies stricter). It covers ONLY those 19 entries and ONLY mode "
+        "differences. Any other drift, any content-hash difference, or any mode difference "
+        "that loosens permissions = STOP and report."
+    ),
+    "count_note": (
+        "The recorded entry set is 3 directories (., refs, refs/probe-packs) and 16 files; "
+        "the total of 19 and the mode pairs match the wording."
+    ),
+    "entries": sorted(AUTHORIZED_MODE_TIGHTENING),
+}
+OWNER_DECISION_B = {
+    "decision": "B: settings.json rebaseline stays approved with conditions",
+    "source": "owner reply '1' at 2026-11-10T00:02Z, relayed by the coordinator",
+    "provenance": (
+        "owner ran /model in the coordinator session on 2026-11-09 ~19:38Z; the default "
+        "model changed and was saved; setup-bmad is an unrelated tooling skill"
+    ),
+}
 
 
 def hash_stream(stream):
@@ -211,7 +262,9 @@ if phase == "before":
         "Normal refresh would broaden filesystem permissions"
     )
     state["selected_mode_tightening"] = mode_changes
-    if drift != EXPECTED_DRIFT:
+    # Plan Task 1: stop on any drift beyond the three stale files. The only mode difference
+    # allowed is the exact owner-authorized set above (decision A), value for value.
+    if drift != EXPECTED_DRIFT or mode_changes != AUTHORIZED_MODE_TIGHTENING:
         keys = set(state["source"]) | set(state["installed"])
         state["observed_drift"] = drift
         state["content_drift"] = sorted(
@@ -257,14 +310,22 @@ if phase == "before":
         "mcp__litellm__augment_code-augment_code_search"
     }
     backup = OUT / "installed-skill-before.tar.gz"
-    assert not backup.exists(), (
-        "Do not overwrite an existing backup; inspect resume evidence"
-    )
-    with tarfile.open(backup, "w:gz") as archive:
-        archive.add(TARGET, arcname=TARGET.name, recursive=True)
-    os.chmod(backup, 0o600)
+    # A backup from the first run is never overwritten: a re-run must prove the existing
+    # backup still matches the (unchanged) installed folder byte for byte, type and mode.
+    state["backup_reused"] = backup.exists()
+    if not backup.exists():
+        with tarfile.open(backup, "w:gz") as archive:
+            archive.add(TARGET, arcname=TARGET.name, recursive=True)
+        os.chmod(backup, 0o600)
     state["backup"] = verify_backup(state)
     state["differing_files"] = drift
+    old_before = OUT / "compatibility-before.json"
+    if old_before.exists():
+        prev = json.loads(old_before.read_text())
+        if "rebaseline" in prev:
+            state["rebaseline"] = prev["rebaseline"]
+    state["owner_decision_A"] = OWNER_DECISION_A
+    state["owner_decision_B"] = OWNER_DECISION_B
     (OUT / "compatibility-before.json").write_text(json.dumps(state, indent=2) + "\n")
     (OUT / "authorization-and-binding.json").write_text(
         json.dumps(
@@ -272,6 +333,8 @@ if phase == "before":
                 "owner_message": "msg_fbc81030bd4f",
                 "owner_provenance": "2026-11-09T14:12UTC direct genuine owner message relayed by coordinator:441 pr469 authorized; checked compatibility only",
                 "scope": "No permissions/profile/tool/gate broadening; normal one-skill installer; old failures/caps preserved; no merge/closure",
+                "owner_decision_A": OWNER_DECISION_A,
+                "owner_decision_B": OWNER_DECISION_B,
                 "binding": state["binding"],
                 "source_target_verified": True,
                 "profile_roster": state["roster"],
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/rebaseline-record.json b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/rebaseline-record.json
index cea0edc1f..24303de48 100644
--- a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/rebaseline-record.json
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/rebaseline-record.json
@@ -35,5 +35,17 @@
     "binding",
     "roster",
     "backup"
-  ]
+  ],
+  "owner_decision_B": {
+    "source": "owner reply '1' at 2026-11-10T00:02Z, relayed by the coordinator (earlier coordinator message msg_bf66b7bcfc84 approved the same rebaseline-and-continue)",
+    "provenance": "the owner ran /model in the coordinator session on 2026-11-09 ~19:38Z; the default model changed and was saved (observed diff: the model key changed and hook entries were reordered, same set of hooks); setup-bmad is an unrelated tooling skill",
+    "conditions": [
+      "record old/new hashes with this provenance",
+      "fresh reviewer checks the diff",
+      "re-take the before-state",
+      "install ONLY sc-troubleshoot-protocol",
+      "afterwards verify ~/.claude/settings.json, ~/.claude/skills/setup-bmad and every unrelated file byte-identical to the before-state"
+    ],
+    "before_state_retaken": "compatibility-before.json (phase before re-run 2026-11-10, settings sha256 b39dd568...)"
+  }
 }
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=T1.AC2 at=.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py:202-213 anchor="only the exact three expected stale skill files differ" chk=y,n,n,n family=mode-drift-gate fix=Treat the 19 mode-only differences as drift beyond the three files. Report Task 1 as blocked on that precise drift, or record an explicit owner/coordinator authorization for the mode-tightening exception inside `compatibility-before.json` and `authorization-and-binding.json`. first=start origin=new: 19 entries (the two directories plus 17 refs files, `compatibility-before.json:333` onward) differ from source in mode (700/600 against installed 755/644).
F1.2 sev=blocking trigger=B4 ac=scope at=.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py:196-213 anchor="Record unexpected extras/drift explicitly and stop if any appears." chk=n,n,n,y family=mode-drift-gate fix=Restore a stop on mode drift, or attach a recorded authorization for the exception, before the baseline and backup count as passed. first=start origin=new: the first run stopped on this drift (`blocked-preflight.log:4-5`, "Unexpected metadata drift; preserved state, no installation"). The helper was then edited so that `drift` is computed from sha256 only. The 19 mode differences became `selected_mode_tightening` and the run continued. No approval for this relaxation is recorded; the only approval in the record (`msg_da4599a5fd9c`, "ok") covers the later settings rebaseline.
Saved-probe re-check hit locations (may be empty): .dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py:42:EXPECTED_DRIFT = ["SKILL.md", "refs/diagnosability-audit.md", "refs/doc-discovery.md"]
.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py:66:AUTHORIZED_MODE_TIGHTENING = {
.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py:84:    "entries": sorted(AUTHORIZED_MODE_TIGHTENING),
.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py:253:    mode_changes = {
.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py:261:    assert all((v["source"] & ~v["installed"]) == 0 for v in mode_changes.values()), (
.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py:264:    state["selected_mode_tightening"] = mode_changes
.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py:267:    if drift != EXPECTED_DRIFT or mode_changes != AUTHORIZED_MODE_TIGHTENING:
.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py:395:        assert changed == EXPECTED_DRIFT, changed
.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py:400:                "selected_mode_tightening": before["selected_mode_tightening"],

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
