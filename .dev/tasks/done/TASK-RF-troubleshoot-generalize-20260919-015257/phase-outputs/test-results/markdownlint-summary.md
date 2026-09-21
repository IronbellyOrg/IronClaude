# Item 5.1 — Markdownlint validation

Status: PASS

Run the actual pre-commit markdownlint hook on the exact 19 Markdown files specified in task lines 1086–1091. Compare SHA-256 snapshots before and after execution and check changed paths against the 19 Markdown files, `.pre-commit-config.yaml`, and the two existing troubleshoot tests. No staging, commits, sync, checklist updates, or future items.

## Attempt 1 — before hook

SHA-256 snapshot captured for all 18124 tracked/untracked nonignored existing files.

| Expected path | Before SHA-256 |
| --- | --- |
| `.pre-commit-config.yaml` | `3ceb438e5461d09e9fa082d8d9c2bcc037e4ed723fb2ca89b9713b3a8c7f331a` |
| `src/superclaude/agents/confidence-calibrator.md` | `497a46f2cd46a41899f1d6a035a1c36e189b07ef30ccdc98bfd587c352154bd9` |
| `src/superclaude/agents/evidence-validator.md` | `1f38ac4b288388dedf913ecd061e437365015956fb9cf4486aaa763a12dee167` |
| `src/superclaude/commands/troubleshoot.md` | `579ca2e90d28b1d5b4456cf8628245da5c4510efb0ea17af124d4d6c07774ed1` |
| `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` | `f0193926827abe961f7bdc22c437096621be6eb92c3cd588caa733a75cd3e007` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/agent-assertions.md` | `c7d542effb9f253e2971cf56e1d45d4855217cb7f1b95205ac7b9f9e62078ac2` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/contract-enumeration.md` | `1307b863c32610946a6edf9b44b02fe5ede2501b384d6cb2af3c76d794ef43d6` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md` | `3eb5ec4f9bd2bf4262804b96d53fdb80d371af154a8adf18fd305f7bcbb86242` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/effective-input-proof.md` | `f40412b36e13a5271bb5b426376efe2b837ff0d09c7e78c0b7ad61f19c95853c` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/environment-deltas.md` | `7ec1aaeedad39c0f7b9ba61f5c8d5973a82e6171635242ad606941e61b3eec5d` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` | `f81319668504ec8a8a95761a6d50a35f570974bcacb76175af2b79bb6eb5f1de` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/hardening-output-contract.md` | `a6c9c9840bf458c6184cfe3b6b6f416fdcfd0edefc32daacbee9149ec024df53` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` | `3f201fb255ba7557eee9439f0069c0ddb6e0f3e579b883e87e100b86f630ef12` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/pipeline-hardening-closure.md` | `597db5c60bc2e28f11ddd9062eb59e3180307f4b6db5a950cb69c3f9004f5625` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/primitive-differential.md` | `482686f3194c1b387b2beda00a1c483308e750dbe999f843a196c797c0ce045a` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md` | `07a7d4a663cdf34d73f98dd7be4cd9140d3028f0cd104159c02a484186fbf2fa` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` | `9c9ccc072a3fa10d6545dfcd6e8d8dfbf4cb8daf5d1132b95ff5a04e72e686c0` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/runtime-entrypoint-verification.md` | `d83f98cba7130cb0c61a5beda16c9d33420b22466de4c84781e886e94759a971` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/triage-checklist.md` | `f8db54e7bccb5ab99a38be4ee4852de1cfa9b8ddb352c91b39f816b597af140b` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/unmask-and-sweep.md` | `460e1b8305242aeb085f6c426bfe2c50fbb8983050173b4d3cbde8437ebd2be8` |
| `tests/troubleshoot/test_hardening_h1.py` | `b81074d03500756ade8bac051095c3fe474a59e2a07aa9ef6943333f68f2f68b` |
| `tests/troubleshoot/test_hardening_verdict.py` | `d5ed4f0da06bb05fa14e95981e1bc43faf00c1c184289d7da746cfd407dcb23f` |

## Attempt 1 — after hook

| Expected path | After SHA-256 |
| --- | --- |
| `.pre-commit-config.yaml` | `3ceb438e5461d09e9fa082d8d9c2bcc037e4ed723fb2ca89b9713b3a8c7f331a` |
| `src/superclaude/agents/confidence-calibrator.md` | `497a46f2cd46a41899f1d6a035a1c36e189b07ef30ccdc98bfd587c352154bd9` |
| `src/superclaude/agents/evidence-validator.md` | `1f38ac4b288388dedf913ecd061e437365015956fb9cf4486aaa763a12dee167` |
| `src/superclaude/commands/troubleshoot.md` | `579ca2e90d28b1d5b4456cf8628245da5c4510efb0ea17af124d4d6c07774ed1` |
| `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` | `f0193926827abe961f7bdc22c437096621be6eb92c3cd588caa733a75cd3e007` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/agent-assertions.md` | `c7d542effb9f253e2971cf56e1d45d4855217cb7f1b95205ac7b9f9e62078ac2` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/contract-enumeration.md` | `1307b863c32610946a6edf9b44b02fe5ede2501b384d6cb2af3c76d794ef43d6` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md` | `3eb5ec4f9bd2bf4262804b96d53fdb80d371af154a8adf18fd305f7bcbb86242` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/effective-input-proof.md` | `f40412b36e13a5271bb5b426376efe2b837ff0d09c7e78c0b7ad61f19c95853c` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/environment-deltas.md` | `7ec1aaeedad39c0f7b9ba61f5c8d5973a82e6171635242ad606941e61b3eec5d` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` | `f81319668504ec8a8a95761a6d50a35f570974bcacb76175af2b79bb6eb5f1de` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/hardening-output-contract.md` | `a6c9c9840bf458c6184cfe3b6b6f416fdcfd0edefc32daacbee9149ec024df53` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` | `3f201fb255ba7557eee9439f0069c0ddb6e0f3e579b883e87e100b86f630ef12` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/pipeline-hardening-closure.md` | `597db5c60bc2e28f11ddd9062eb59e3180307f4b6db5a950cb69c3f9004f5625` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/primitive-differential.md` | `482686f3194c1b387b2beda00a1c483308e750dbe999f843a196c797c0ce045a` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md` | `07a7d4a663cdf34d73f98dd7be4cd9140d3028f0cd104159c02a484186fbf2fa` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` | `9c9ccc072a3fa10d6545dfcd6e8d8dfbf4cb8daf5d1132b95ff5a04e72e686c0` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/runtime-entrypoint-verification.md` | `d83f98cba7130cb0c61a5beda16c9d33420b22466de4c84781e886e94759a971` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/triage-checklist.md` | `f8db54e7bccb5ab99a38be4ee4852de1cfa9b8ddb352c91b39f816b597af140b` |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/unmask-and-sweep.md` | `460e1b8305242aeb085f6c426bfe2c50fbb8983050173b4d3cbde8437ebd2be8` |
| `tests/troubleshoot/test_hardening_h1.py` | `b81074d03500756ade8bac051095c3fe474a59e2a07aa9ef6943333f68f2f68b` |
| `tests/troubleshoot/test_hardening_verdict.py` | `d5ed4f0da06bb05fa14e95981e1bc43faf00c1c184289d7da746cfd407dcb23f` |

- Actual hook exit: 0
- Rewritten/created/deleted nonignored files: []
- Changed-file scope: 22/22 expected paths
- Unexpected paths: []
- Missing expected paths: []
- Index unchanged: True
- Final raw capture lines containing exit=0: 1

Status: PASS
