c5d741ea37613a64f6604fc4a30c3edb4fd13521
Review one task for spec compliance.

Task brief: ## Task 2: Refresh one installed skill and return independently checked readiness

Depends on: Task 1

Implements R-004, R-008, R-009, R-010, R-011 and R-012, retaining R-001/R-002/R-003/R-006/R-007 as prerequisites. Immediately before installation recheck source/target identity, private backup, selected file state and all captured invariance hashes; stop on any unexpected change. Run only `uv run superclaude install-skill sc-troubleshoot-protocol --target ~/.claude/skills --force`, with HOME/realpath already bound to the approved owner target. Capture exact command, stdout/stderr and exit in ./artifacts/selective-install.json. A copy/install failure yields blocked with actual target state; no automatic hand-copy, broad install, profile fallback or false unchanged claim.

Write ./artifacts/compatibility-after.json proving exact unchanged canonical-to-installed parity, the exact three stale-file byte changes, unchanged closed analyst roster/profile hashes, unchanged settings/permission hashes, unchanged unrelated installed skill digests and unchanged project-mirror digests. Do not run make sync-dev: no canonical or project-copy change is needed. Run the focused contract suite and read-only make verify-sync, saving ./artifacts/canonical-contract-after.log and ./artifacts/verify-sync.log. Launch one troubleshoot-analyst with explicit verified model=sonnet/Tier1b to Read only the new installed contract and a small existing source excerpt and return data to the parent; preserve actual response and invocation provenance in ./artifacts/restricted-worker-smoke.json. It must not run commands, tests, experiments, mutations or delegation. A fresh explicit Tier1b reviewer checks installation evidence, invariance and smoke and returns ./artifacts/compatibility-review.json. Stop at compatibility readiness or a precise blocker, not PR remediation or merge.

Acceptance criteria:
- T2.AC1: R-004, R-008, R-009: the guarded selective installer succeeds; exact canonical parity and only the three approved byte changes are proven. All profile/permission/settings/unrelated-skill/project-mirror baselines remain unchanged; no broad-copy, extra capability, alternative profile or installed hand-edit is used.
- T2.AC2: R-002, R-010, R-011: actual focused tests and read-only sync verification pass; explicit Tier1b restricted worker completes the tiny allowed Read-only smoke with actual data and invocation provenance. Missing/incorrect model, unavailable worker, failed tests or changed invariants block readiness rather than trigger fallback.
- T2.AC3: R-001, R-012: fresh independent Tier1b review confirms compatibility and preserved boundaries with real evidence. The final outcome gives readiness or a precise blocker and actual artifact paths, preserves all old failed reports/caps and first plan/check, and makes no claim of reader/CI repair, PR push, extra review allowance, merge or closure. .dev/tasks remains staged and .claude mirrors are never staged.
Global constraints: ## Constraints

- R-001, R-002, R-003: genuine owner authorization is coordinator msg_fbc81030bd4f, scoped to compatibility only. Every helper uses explicit verified sonnet/Tier1b (claude-gw-tier1b[1m]); no Opus/fork/other-tier fallback. Preserve all prior failed diagnostics, their0.80 cap, and the first unexecuted plan/check unchanged.
- R-003, R-004: canonical source/profile already agree; change no canonical source, agent profile, tool capability, permission/settings file or gate. Use no full installer/update, hand-edited installed primitive, global-agent substitute, project-mirror write or make sync-dev. Only the existing selective skill installer can replace the approved installed target. Unexpected canonical gap or drift blocks this plan.
- R-001, R-010, R-011, R-012: no reader repair, PR fix commit/push, extra review allowance, experiments, huge files, benchmark, merge or issue closure. Codex remains optional, not a gate waiver for confirmed code/CI findings.
- R-007, R-012: evidence belongs in ./artifacts; private backup outside installed primitive directories, archive0600 under umask077. Preserve all old evidence. Stage .dev/tasks, never .claude mirrors. Do not claim projected tests/smoke or an earlier failed check passed.
Start sha: c5d741ea37613a64f6604fc4a30c3edb4fd13521
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/canonical-contract-after.log b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/canonical-contract-after.log
new file mode 100644
index 000000000..c14f5c108
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/canonical-contract-after.log
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
+============================== 51 passed in 1.52s ==============================
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-after.json b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-after.json
new file mode 100644
index 000000000..9eb13cced
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-after.json
@@ -0,0 +1,425 @@
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
+  "changed_files": [
+    "SKILL.md",
+    "refs/diagnosability-audit.md",
+    "refs/doc-discovery.md"
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
+  "protected_invariants_unchanged": true,
+  "exact_canonical_parity": true,
+  "backup": {
+    "path": "./artifacts/installed-skill-before.tar.gz",
+    "kind": "file",
+    "mode": 384,
+    "size": 106556,
+    "sha256": "77e304762480a13a83589c62f3ca1dc8ddf8cd4ab3b0b0afc7920ec2341a3707"
+  }
+}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-review.json b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-review.json
new file mode 100644
index 000000000..0450b94bd
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-review.json
@@ -0,0 +1,44 @@
+{
+  "reviewer": {
+    "agent_type": "general-purpose",
+    "model_alias": "sonnet",
+    "model_mapping": "claude-gw-tier1b[1m]",
+    "agent_id": "a3730953750fd4778",
+    "fresh": true,
+    "mode": "read-only; no pytest, make, write or delegation",
+    "usage": {"tool_uses": 14, "duration_ms": 120984, "subagent_tokens": 151843},
+    "harness_note": "The harness flagged the reviewer output for an instruction-shaped pattern (settings-json). The text only describes the settings.json hash check; no instruction was followed."
+  },
+  "verdict": "PASS",
+  "checks": [
+    {"n": 1, "name": "Installed vs source content parity (live sha256)", "result": "met", "evidence": "Both trees list the same 22 entries and entry types. sha256sum over every regular file gives identical hashes. No symlinks in the installed tree. The three files that changed between before and after are SKILL.md, refs/diagnosability-audit.md and refs/doc-discovery.md. All other files have unchanged hashes. The before-state backup tar is mode 600, sha256 77e30476..., matching the recorded value."},
+    {"n": 2, "name": "Modes installed vs source, and vs before", "result": "met", "evidence": "Installed modes are identical to source. Before-to-after mode changes are exactly 19 entries: 3 directories 755 to 700 (., refs, refs/probe-packs) and 16 files 644 to 600. Each is a strict subset of the old bits, so none is looser. The three content-changed files kept mode 644 on both sides. The backup tar still records the old modes, so rollback is possible."},
+    {"n": 3, "name": "~/.claude/settings.json unchanged from baseline", "result": "met", "evidence": "Live sha256 b39dd56864118734fa84bf885f45efcf9d0a8ddd9357be9f6b8793de39c47d06 equals the value in compatibility-before.json, compatibility-after.json and rebaseline-record.json. mtime 2026-11-09 19:38:25 is before the install at 2026-11-10 00:18:27."},
+    {"n": 4, "name": "setup-bmad unchanged", "result": "met", "evidence": "setup-bmad mtime 2026-11-09 16:03 (before the install). Recomputed the 46-entry unrelated-skills digest with the checker's algorithm: aee68bf0b5fc006765e8299de6a7283e73fd29830836c140a939934813fdc64c, equal to the recorded value."},
+    {"n": 5, "name": "No other directory under ~/.claude/skills changed", "result": "met", "evidence": "The 46-entry digest matches before and after. Nothing under ~/.claude/skills outside sc-troubleshoot-protocol has a ctime newer than 00:18:27. Project .claude mirror digests (skills, agents, commands, hooks, templates) recomputed live match the recorded values."},
+    {"n": 6, "name": "verify-sync drift claim", "result": "met", "evidence": "The only non-OK lines in verify-sync.log are 22-23 (DIFFERS: sc-issue-protocol, orca_worktree.py) and 223-224 (Drift detected, make error). The troubleshoot skill, agent and command are OK. git status shows only orca_worktree.py modified under src. git show HEAD:...orca_worktree.py equals the .claude mirror. The edit is an uncommitted 24-line change (capped read helper) with mtime before the install. diff -r of the troubleshoot skill between src and .claude is empty."},
+    {"n": 7, "name": "Restricted-worker smoke", "result": "met", "evidence": "restricted-worker-smoke.json: troubleshoot-analyst, alias sonnet mapped to claude-gw-tier1b[1m], two Read calls, no delegation. The 9-name roster matches SKILL.md line 31 in the same order, and install_skill.py line 58 is def _get_skill_source(skill_name: str) -> Optional[Path]."},
+    {"n": 8, "name": "Installer touched only the skill folder", "result": "met", "evidence": "Files newer than 00:18:27 outside session and state areas: skills/ (the install), a 20-byte plugins/store file, and harness state. Nothing changed in agents/, commands/, hooks/, rules/ or the top-level files. settings.json and the global agents/troubleshoot-analyst.md keep their pre-install mtimes. The installer module sha256 dba905ac... equals HEAD."},
+    {"n": 9, "name": "Focused tests", "result": "met", "evidence": "canonical-contract-after.log shows 51 passed, the same as canonical-contract-before.log."}
+  ],
+  "findings": [
+    {"id": "F2.1", "severity": "minor", "text": "The acceptance criterion says read-only sync verification must pass. make verify-sync exited 1 (make reports 2). The failure is the unrelated uncommitted edit to sc-issue-protocol orca_worktree.py; every troubleshoot component is OK. The readiness report must say verify-sync fails only on that unrelated drift, never that it passed.", "citation": "verify-sync.log:22-23,223-224; verify-sync-analysis.log"},
+    {"id": "F2.2", "severity": "minor", "text": "Owner wording says 2 directories and 17 refs files; the recorded set is 3 directories and 16 files. The total of 19 and the mode pairs match, and count_note discloses this.", "citation": "authorization-and-binding.json owner_decision_A.count_note; compatibility_state.py:80-83"},
+    {"id": "F2.3", "severity": "minor", "text": "The global agent profile ~/.claude/agents/troubleshoot-analyst.md (sha a952b406...) still lacks mcp__litellm__augment_code-augment_code_search, which the source and project profiles (fe25f871...) include. Unchanged by this plan (before equals after), outside Task 2 scope, loosens nothing. Known carry-over F1.3.", "citation": "compatibility-after.json profiles; restricted-worker-smoke.json caveat"},
+    {"id": "F2.4", "severity": "minor", "text": "The smoke record gives an approximate launch time and does not say which agent definition (project or global) was resolved. Tool use is self-reported by the worker. Acknowledged in its caveat; acceptable for a read-only smoke test.", "citation": "restricted-worker-smoke.json"},
+    {"id": "F2.5", "severity": "minor", "text": "New artifacts are untracked until git add .dev/tasks is run. Do not stage .claude mirrors.", "citation": "git status --short on the package directory"},
+    {"id": "F2.6", "severity": "minor", "text": "The installed skill folder is now owner-only (700/600) where it was 755/644. Authorized by decision A; stricter, not looser.", "citation": "compatibility-after.json selected_mode_tightening"}
+  ],
+  "verify_sync_blocks_readiness": false,
+  "verify_sync_reason": "The only drift is src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py, an uncommitted earlier #441 edit not yet synced to .claude. The .claude copy equals HEAD. The install changed nothing under src or .claude. The plan forbids make sync-dev, and sync-dev plus verify-sync run as the normal pre-commit step afterwards. Readiness is conditional on that step; the verify-sync non-pass is disclosed, not rounded up.",
+  "self_audit": "Recomputed against the live filesystem: per-file sha256, entry sets, types and modes; recorded before/after states entry by entry; live settings.json sha256 and mtime; the 46-entry unrelated digest and five project-mirror digests; ctime and mtime sweeps of ~/.claude; verify-sync.log in full plus the HEAD-vs-mirror cmp; the smoke answers against the files; the backup tar; the installer module hash. Not verified: owner-message provenance, the worker's tool-use trace, who made the orca_worktree.py edit.",
+  "parent_readback": {
+    "date": "2026-11-10",
+    "settings_json_sha256_prefix": "b39dd56864118734 (live, matches)",
+    "verify_sync_log_lines": "22-23 and 223-224 as cited",
+    "installed_vs_source": "diff -r empty (content parity)",
+    "modes": "installed dir 700, SKILL.md 644",
+    "backup_tar_sha256_prefix": "77e304762480a13a (matches)",
+    "git_status_src": "only src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py modified"
+  }
+}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/restricted-worker-smoke.json b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/restricted-worker-smoke.json
new file mode 100644
index 000000000..6b81b9e76
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/restricted-worker-smoke.json
@@ -0,0 +1,34 @@
+{
+  "invocation": {
+    "agent_type": "troubleshoot-analyst",
+    "model_alias": "sonnet",
+    "model_mapping": "claude-gw-tier1b[1m]",
+    "launched_at": "2026-11-10T00:19Z (approximate; to the minute)",
+    "agent_id": "a0a623f90f2feb0ef",
+    "mode": "background, single agent, no delegation",
+    "prompt": "Restricted read-only smoke test. Use only the Read tool, at most two calls. Do not run commands, tests, experiments, edits or delegation. (1) Read /home/coder/.claude/skills/sc-troubleshoot-protocol/SKILL.md line 31 and return the exact list of tool names inside the backticked closed roster as a JSON array. (2) Read src/superclaude/cli/install_skill.py lines 58-72 and return the function name at line 58 and its return type annotation. Reply with one JSON object only: {roster, function, return_type, tools_used}."
+  },
+  "actual_response": {
+    "roster": [
+      "Read",
+      "Grep",
+      "Glob",
+      "mcp__litellm__augment_code-augment_code_search",
+      "mcp__auggie__codebase-retrieval",
+      "mcp__codegraph__codegraph_search",
+      "mcp__codegraph__codegraph_node",
+      "mcp__codegraph__codegraph_callers",
+      "mcp__codegraph__codegraph_impact"
+    ],
+    "function": "_get_skill_source",
+    "return_type": "Optional[Path]",
+    "tools_used": ["Read", "Read"]
+  },
+  "usage": {"tool_uses": 2, "duration_ms": 4307, "subagent_tokens": 34774},
+  "parent_readback": {
+    "SKILL.md:31": "closed roster text matches the returned array (9 names, same order as the installed file)",
+    "install_skill.py:58": "def _get_skill_source(skill_name: str) -> Optional[Path]:"
+  },
+  "verdict": "pass: the worker used only Read (2 calls), no commands, tests, edits or delegation; both answers match the files on disk",
+  "caveat": "Tool use is taken from the worker's own report and its usage record (2 tool uses); it is not an independent trace. The global agent file ~/.claude/agents/troubleshoot-analyst.md (carry-over F1.3) was not changed by this plan."
+}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/selective-install.json b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/selective-install.json
new file mode 100644
index 000000000..d15ee67a9
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/selective-install.json
@@ -0,0 +1,9 @@
+{
+  "command": "uv run superclaude install-skill sc-troubleshoot-protocol --target ~/.claude/skills --force",
+  "cwd": "/home/coder/workspaces/worktrees/IronClaude/issue-441",
+  "started": "2026-11-10T00:18:27Z",
+  "finished": "2026-11-10T00:18:27Z",
+  "exit_code": 0,
+  "stdout": "\ud83d\udce6 Installing skill 'sc-troubleshoot-protocol' to /home/coder/.claude/skills...\n\u2705 Skill 'sc-troubleshoot-protocol' installed successfully to /home/coder/.claude/skills/sc-troubleshoot-protocol\n",
+  "stderr": ""
+}
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/verify-sync-analysis.log b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/verify-sync-analysis.log
new file mode 100644
index 000000000..231334f4e
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/verify-sync-analysis.log
@@ -0,0 +1,9 @@
+verify-sync exit 2 analysis, 2026-11-10T00:18:55Z
+only DIFFERS line in verify-sync.log: sc-issue-protocol orca_worktree.py (log line 22-23)
+HEAD copy of src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py is byte-identical to .claude/skills/sc-issue-protocol/scripts/orca_worktree.py => mirror matches committed source
+ 1 file changed, 24 insertions(+), 3 deletions(-)
+cause: uncommitted capped-hook-read edit from the earlier worker (not the install, not the troubleshoot skill)
+1
+35:  ✅ sc-troubleshoot-protocol
+93:  ✅ troubleshoot-analyst.md
+138:  ✅ troubleshoot.md
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/verify-sync.log b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/verify-sync.log
new file mode 100644
index 000000000..d94e1b9e7
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/verify-sync.log
@@ -0,0 +1,224 @@
+🔍 Verifying src/superclaude/ ↔ .claude/ sync...
+
+=== Skills ===
+  ✅ ccsession-tag
+  ✅ confidence-check
+  ✅ operational-guide
+  ✅ prd
+  ✅ readme
+  ✅ roadmap
+  ✅ sc-adversarial-protocol
+  ✅ sc-auggie-review-protocol
+  ✅ sc-bare-review
+  ✅ sc-brainstorm-protocol
+  ✅ sc-cleanup-audit-protocol
+  ✅ sc-cli-eval-protocol
+  ✅ sc-cli-portify-protocol
+  ✅ sc-crash-recovery
+  ✅ sc-graph-protocol
+  ✅ sc-impact-protocol
+  ✅ sc-implement-protocol
+  ✅ sc-init-lite-protocol
+  ⚠️  DIFFERS: sc-issue-protocol
+      Files src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py and .claude/skills/sc-issue-protocol/scripts/orca_worktree.py differ
+  ✅ sc-pm-protocol
+  ✅ sc-post-release-protocol
+  ✅ sc-pr-submit-protocol
+  ✅ sc-recommend
+  ✅ sc-reflect-protocol
+  ✅ sc-release-split-protocol
+  ✅ sc-review-translation-protocol
+  ✅ sc-roadmap-protocol
+  ✅ sc-swarm-wizard-protocol
+  ✅ sc-task-protocol
+  ✅ sc-tasklist-protocol
+  ✅ sc-troubleshoot-protocol
+  ✅ sc-validate-roadmap-protocol
+  ✅ sc-validate-tests-protocol
+  ✅ sc-workflow-protocol
+  ✅ task-builder
+  ✅ task
+  ✅ tdd
+  ✅ tech-reference
+  ✅ tech-research
+
+=== Agents ===
+  ✅ audit-analyzer.md
+  ✅ audit-comparator.md
+  ✅ audit-consolidator.md
+  ✅ audit-scanner.md
+  ✅ audit-validator.md
+  ✅ auggie-reviewer.md
+  ✅ backend-architect.md
+  ✅ business-panel-experts.md
+  ✅ confidence-calibrator.md
+  ✅ debate-orchestrator.md
+  ✅ deep-research-agent.md
+  ✅ deep-research.md
+  ✅ devops-architect.md
+  ✅ eval-docs-loader.md
+  ✅ eval-run-reporter.md
+  ✅ eval-suite-author.md
+  ✅ evidence-validator.md
+  ✅ frontend-architect.md
+  ✅ implement-retry-adviser.md
+  ✅ issue-worker-t1.md
+  ✅ issue-worker-t2.md
+  ✅ issue-worker-t3.md
+  ✅ learning-guide.md
+  ✅ merge-executor.md
+  ✅ performance-engineer.md
+  ✅ pm-agent.md
+  ✅ python-expert.md
+  ✅ quality-engineer.md
+  ✅ refactoring-expert.md
+  ✅ reflect-reviewer.md
+  ✅ repo-index.md
+  ✅ requirements-analyst.md
+  ✅ reuse-auditor.md
+  ✅ rf-analyst.md
+  ✅ rf-assembler.md
+  ✅ rf-qa-qualitative.md
+  ✅ rf-qa.md
+  ✅ rf-task-builder.md
+  ✅ rf-task-executor.md
+  ✅ rf-task-researcher.md
+  ✅ rf-team-lead.md
+  ✅ root-cause-analyst.md
+  ✅ security-engineer.md
+  ✅ self-review.md
+  ✅ socratic-mentor.md
+  ✅ system-architect.md
+  ✅ technical-writer.md
+  ✅ troubleshoot-analyst.md
+
+=== Commands ===
+  ✅ adversarial.md
+  ✅ agent.md
+  ✅ analyze.md
+  ✅ auggie-review.md
+  ✅ brainstorm.md
+  ✅ build.md
+  ✅ business-panel.md
+  ✅ cleanup-audit.md
+  ✅ cleanup.md
+  ✅ cli-eval.md
+  ✅ cli-portify.md
+  ✅ design.md
+  ✅ document.md
+  ✅ explain.md
+  ✅ git.md
+  ✅ graph.md
+  ✅ help.md
+  ✅ impact.md
+  ✅ implement.md
+  ✅ improve.md
+  ✅ index-repo.md
+  ✅ index.md
+  ✅ init-lite.md
+  ✅ issue.md
+  ✅ load.md
+  ✅ pm.md
+  ✅ post-release.md
+  ✅ pr-submit.md
+  ✅ recommend.md
+  ✅ reflect.md
+  ✅ release-split.md
+  ✅ research.md
+  ✅ review-translation.md
+  ✅ roadmap.md
+  ✅ save.md
+  ✅ spawn.md
+  ✅ spec-panel.md
+  ✅ swarm-wizard.md
+  ✅ task.md
+  ✅ tasklist.md
+  ✅ tdd.md
+  ✅ test.md
+  ✅ troubleshoot.md
+  ✅ validate-roadmap.md
+  ✅ validate-tests.md
+  ✅ workflow.md
+
+=== Hooks ===
+  ✅ auggie-flag-clear.sh
+  ✅ block-bare-python.sh
+  ✅ codegraph-session-start.sh
+  ✅ freshness-file-changed.sh
+  ✅ freshness-post-read.sh
+  ✅ freshness-pre-edit.sh
+  ✅ freshness-session-start.sh
+  ✅ freshness-subagent-start.sh
+  ✅ freshness-subagent-stop.sh
+  ✅ freshness-user-prompt.sh
+  ✅ launch-job-identity.sh
+  ✅ launch-level-guard.sh
+  ✅ launch-level-pre-push.sh
+  ✅ reject-workspace-writes.sh
+  ✅ require-orca-worktree-agent.sh
+  ✅ sc-recommend-phase0.sh
+  ✅ pragmatic-subagent.js
+
+=== Templates ===
+  ✅ workflow/05_prd_template.md
+  ✅ workflow/03_project_plan_template.md
+  ✅ workflow/03_component_authoring_template.md
+  ✅ workflow/00_mdtm_template_simple_task.md
+  ✅ workflow/01_mdtm_template_generic_task__gfdoc.md
+  ✅ workflow/06_architecture_proposal_template.md
+  ✅ workflow/02_mdtm_template_complex_task.md
+  ✅ workflow/04_feature_brief_template.md
+  ✅ workflow/changelog_template.md
+  ✅ workflow/01_mdtm_template_generic_task.md
+  ✅ workflow/99_mdtm_template_generic_task_old.md
+  ✅ documents/prd_template.md
+  ✅ documents/operational_guide_template.md
+  ✅ documents/GFxAI_Master_Documentation_Template.md
+  ✅ documents/tdd_template.md
+  ✅ documents/agent_template_analysis.md
+  ✅ documents/supplemental-doc-creation-checklist.md
+  ✅ documents/agent_template_qa.md
+  ✅ documents/skill_template.md
+  ✅ documents/roadmap_template.md
+  ✅ documents/agent_template_worker.md
+  ✅ documents/release-spec-template.md
+  ✅ documents/supplemental_doc_template.md
+  ✅ documents/technical_reference_template.md
+  ✅ documents/readme_template.md
+  ✅ modularization-template-review/qa-fix-summary_template.md
+  ✅ modularization-template-review/qa-task-research-alignment_report_template.md
+  ✅ modularization-template-review/analyst-synthesis-review_report_template.md
+  ✅ modularization-template-review/research-notes_template.md
+  ✅ modularization-template-review/synthetic-dnsp-finding.contract
+  ✅ modularization-template-review/INDEX.md
+  ✅ modularization-template-review/qa-task-validation-structure_report_template.md
+  ✅ modularization-template-review/qa-cross-source-contradictions_template.md
+  ✅ modularization-template-review/track-scope-map_template.md
+  ✅ modularization-template-review/claim-evidence-matrix_template.md
+  ✅ modularization-template-review/qa-inventory_report_template.md
+  ✅ modularization-template-review/analyst-coverage-matrix_template.md
+  ✅ modularization-template-review/codebase-research_template.md
+  ✅ modularization-template-review/analyst-completeness_report_template.md
+  ✅ modularization-template-review/analyst-gap-analysis_template.md
+  ✅ modularization-template-review/qa-lens_report_template.md
+  ✅ modularization-template-review/qa-consolidated-findings_template.md
+  ✅ modularization-template-review/qa-task-validation-b2_report_template.md
+  ✅ modularization-template-review/qa-research-gap_report_template.md
+  ✅ modularization-template-review/qa-research-evidence_report_template.md
+  ✅ modularization-template-review/qa-qualitative-operational_report_template.md
+  ✅ modularization-template-review/qa-qualitative-sufficiency_report_template.md
+  ✅ modularization-template-review/analyst-cross-validation_report_template.md
+  ✅ modularization-template-review/qa-acceptance-methodology-audit_template.md
+  ✅ modularization-template-review/pipeline-complete_report_template.md
+  ✅ modularization-template-review/qa-source-fidelity_template.md
+  ✅ modularization-template-review/qa-research-depth_report_template.md
+  ✅ modularization-template-review/web-research_template.md
+
+=== Installer Registration ===
+  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh and *.js
+
+=== Hooks Cross-Consistency ===
+  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes
+
+❌ Drift detected! Run 'make sync-dev' to fix, or copy .claude/ changes to src/.
+make: *** [Makefile:168: verify-sync] Error 1
diff --git a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/progress.md b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/progress.md
index 927dc8366..9bb518c31 100644
--- a/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/progress.md
+++ b/.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/progress.md
@@ -2,3 +2,4 @@
 PLAN: sha256=f497896cc273c8a3976876b6f9fb08865a210cd6817a4c5b688f7ecfc7f72a4c source_sha256=f4be1c7f599cc933868fcf4181d0e9895045870787749eb3e208260391542da4
 T1: start sha=8365c62c3b202c1af844fd81a67754e15788d65a
 T1: complete verdict=compliant ac=T1.AC1,T1.AC2,T1.AC3 evidence=T1.AC1@./artifacts/authorization-and-binding.json:5,T1.AC2@./artifacts/compatibility_state.py:267,T1.AC3@./artifacts/canonical-contract-before.log:12,notes@./artifacts/retries/T1/notes.md:1-4 extras=lint:skip,typecheck:skip,test:pass files=.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility_state.py,.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/compatibility-before.json,.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/authorization-and-binding.json,.dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413/artifacts/rebaseline-record.json
+T2: start sha=c5d741ea37613a64f6604fc4a30c3edb4fd13521
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

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
