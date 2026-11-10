---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-diagnosticCompat-20261109-141620
version: "1"
priority: Medium
created_date: "2026-11-09"
---

# Reconcile the installed diagnostic contract with canonical source

Source: ./source.md
Goal: Restore exact canonical diagnostic-profile compatibility through the normal selective installer, with independently checked evidence and no capability broadening, so the existing PR remediation can resume through its unchanged gates.

## Constraints

- Authorization is the narrowly scoped genuine owner decision relayed in coordinator msg_fbc81030bd4f. Preserve its exact provenance and both failed diagnostic attempts, including the independent 0.80 score, locus_unknown cap and required escalation. Do not reinterpret earlier failures as passes.
- Every helper is explicitly model=sonnet, verified to resolve through ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b[1m]. No Opus or other-tier fallback; unavailable Tier1b means report blocked rather than substitute.
- No agent profile, permission setting, native tool capability, independent gate, confidence threshold or unrelated canonical source change. The canonical skill/profile already agree and tests pin the roster. If inspection instead finds a new canonical gap or unrelated installed customization, stop and report it; do not invent a broader source repair.
- Use only the normal existing selective install-skill command after preserving and checking the target. No full install/update, hand-edited installed primitive, global-agent substitution, or generated-mirror workaround. Do not stage any .claude path; .dev/tasks is always staged.
- Python only through uv. No large-file/memory-pressure experiment, unrestricted diagnostic worker, PR push, extra review allowance, merge or issue closure in this compatibility package. Codex is optional by owner decision; confirmed code findings and CI remain real work outside this package.
- Task evidence goes under ./artifacts. Back up the old installed skill outside installed primitive folders, preserving every prior file and a manifest. No original evidence is deleted. The plan/source snapshot remain pinned during execution.

## Phase 1: Preserve the actual compatibility boundary

## Task 1: Record canonical agreement and preserve the installed package

Inspect src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md, refs/doc-discovery.md and refs/diagnosability-audit.md; src/superclaude/agents/troubleshoot-analyst.md; active project .claude/agents/troubleshoot-analyst.md; installed ~/.claude/skills/sc-troubleshoot-protocol and its corresponding global agent when relevant. Inspect the existing selective installer at src/superclaude/cli/install_skill.py before using its destructive force replacement. Produce ./artifacts/compatibility-before.json with exact file inventories, hashes, roster comparison and drift, and preserve the entire previous installed skill package as ./artifacts/installed-skill-before.tar.gz plus an extraction-free inventory/hash verification. Record genuine owner authorization, verified Tier1b model mapping and current PR469 head/state in ./artifacts/authorization-and-scope.md. Run the existing focused tests/troubleshoot/test_diagnostic_worker_contract.py and save ./artifacts/canonical-contract-tests.log. Do not change canonical or installed files in this task.

Acceptance criteria:
- The record proves canonical source skill and selected active agent declare the same exact nine-tool read-only roster, while the stale installed protocol lacks the existing retrieval alias; all three differing installed package files and any unexpected extras are listed. Unexpected drift or a mismatched canonical roster blocks installation.
- The complete previous installed package is preserved with matching file bytes/hashes, without changing installed/profile/permission files. The focused canonical contract suite passes with its actual result recorded.
- Authorization provenance, PR head/state, helper model mapping and unchanged safety boundaries are explicit. Evidence does not claim old failed diagnoses or the 0.80 calibration passed.

## Phase 2: Refresh the skill through the normal installer

## Task 2: Install the existing canonical skill and prove restricted readiness

Depends on: Task 1

Use the verified normal command `uv run superclaude install-skill sc-troubleshoot-protocol --force` to refresh only the existing installed skill from canonical source; save ./artifacts/selective-install.log. Verify source and installed package exact parity and unchanged canonical/project/global agent profile hashes and permission-setting hashes in ./artifacts/compatibility-after.json. Run the focused contract suite again and the normal make sync-dev/make verify-sync checks, saving their actual logs. Perform one narrowly read-only troubleshoot-analyst smoke check with explicit model=sonnet/Tier1b that reads the installed contract and a small existing source excerpt, returns data only and neither executes experiments nor delegates; persist its returned data as ./artifacts/restricted-worker-smoke.json. Have a fresh explicit Tier1b reviewer compare current boundaries and evidence, with output ./artifacts/compatibility-review.json. Do not change the reader code, PR head or old diagnostic evidence; hand verified readiness back to the existing monitor.

Acceptance criteria:
- The selective installer succeeds and installed skill files exactly equal current canonical files. No extra files, changed agent rosters, new capabilities or permission changes are introduced, and unrelated installed skills remain untouched.
- Focused contract tests and sync verification pass. The explicitly Tier1b restricted worker completes only the permitted read-only smoke task; unavailable or incorrect model/profile yields blocked, never an unrestricted fallback or invented pass.
- Independent Tier1b review confirms the canonical compatibility reconciliation and preserved safety gates, with exact evidence. The outcome reports readiness or a precise blocker and the actual artifacts. No PR fix, push, merge or issue closure is claimed by this package.
