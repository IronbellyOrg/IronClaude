---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-diagnosticRefres-20261109-144413
version: "1"
priority: Medium
created_date: "2026-11-09"
---

# Refresh only the stale installed diagnostic skill

Source: ./source.md
Goal: Restore exact canonical protocol/profile compatibility by the normal selective installer after a private complete backup, with unchanged permissions/profiles/project mirrors and independently observed restricted-worker readiness.

## Constraints

- R-001, R-002, R-003: genuine owner authorization is coordinator msg_fbc81030bd4f, scoped to compatibility only. Every helper uses explicit verified sonnet/Tier1b (claude-gw-tier1b[1m]); no Opus/fork/other-tier fallback. Preserve all prior failed diagnostics, their0.80 cap, and the first unexecuted plan/check unchanged.
- R-003, R-004: canonical source/profile already agree; change no canonical source, agent profile, tool capability, permission/settings file or gate. Use no full installer/update, hand-edited installed primitive, global-agent substitute, project-mirror write or make sync-dev. Only the existing selective skill installer can replace the approved installed target. Unexpected canonical gap or drift blocks this plan.
- R-001, R-010, R-011, R-012: no reader repair, PR fix commit/push, extra review allowance, experiments, huge files, benchmark, merge or issue closure. Codex remains optional, not a gate waiver for confirmed code/CI findings.
- R-007, R-012: evidence belongs in ./artifacts; private backup outside installed primitive directories, archive0600 under umask077. Preserve all old evidence. Stage .dev/tasks, never .claude mirrors. Do not claim projected tests/smoke or an earlier failed check passed.

## Phase 1: Preserve and bind the exact installation boundary

## Task 1: Capture private backup and checked source-target baselines

Implements R-001, R-002, R-003, R-005, R-006, R-007 and the pre-install part of R-010. Inspect the existing src/superclaude/cli/install_skill.py source-resolution and delete-before-copy implementation. Under the actual uv runtime record the loaded installer module path, resolved canonical sc-troubleshoot-protocol source, the explicit intended target under ~/.claude/skills, target/source realpaths and symlink safety. Record those checks, genuine authorization and verified helper model mapping in ./artifacts/authorization-and-binding.json. Assert source resolves to this checkout's src/superclaude/skills/sc-troubleshoot-protocol and target to the existing owner's sc-troubleshoot-protocol skill, never an alternate package.

Create ./artifacts/compatibility-before.json with selected source/installed file inventories (names, types, modes and SHA256), exact canonical/project closed-roster agreement, and the three expected stale files (SKILL.md, refs/doc-discovery.md, refs/diagnosability-audit.md). Include before hashes for canonical/project/global analyst profiles and existing project/global permission/settings files, digests of unrelated installed skills and all project mirrors. Record unexpected extras/drift explicitly and stop if any appears. With umask077, preserve the complete prior installed package as ./artifacts/installed-skill-before.tar.gz, mode0600, and verify archived bytes/types/modes against the inventory without extracting or executing it. Preserve the backup, do not replace an existing backup or automatically restore by hand. Run tests/troubleshoot/test_diagnostic_worker_contract.py and save ./artifacts/canonical-contract-before.log. Do not mutate installed/profile/settings/project-mirror or canonical files.

Acceptance criteria:
- R-001, R-002, R-003, R-005: recorded actual runtime source/target binding and realpath checks match the approved checkout and owner target; authorization and explicit Tier1b mapping are preserved; canonical/active closed rosters match without changed tools or weakened gates.
- R-006, R-007: complete inventories and all invariance baselines exist; only the exact three expected stale skill files differ, no unexpected extras/unsafe paths; complete private0600 backup verifies bytes/types/modes before any deletion. Any failed prerequisite is a blocker, not an assumed pass.
- R-010: focused canonical contract/install tests pass with actual output. No install or unrelated mutation occurred; earlier failed reports/plan/check and0.80 score remain unchanged.

## Phase 2: Perform only the normal selective refresh

## Task 2: Refresh one installed skill and return independently checked readiness

Depends on: Task 1

Implements R-004, R-008, R-009, R-010, R-011 and R-012, retaining R-001/R-002/R-003/R-006/R-007 as prerequisites. Immediately before installation recheck source/target identity, private backup, selected file state and all captured invariance hashes; stop on any unexpected change. Run only `uv run superclaude install-skill sc-troubleshoot-protocol --target ~/.claude/skills --force`, with HOME/realpath already bound to the approved owner target. Capture exact command, stdout/stderr and exit in ./artifacts/selective-install.json. A copy/install failure yields blocked with actual target state; no automatic hand-copy, broad install, profile fallback or false unchanged claim.

Write ./artifacts/compatibility-after.json proving exact unchanged canonical-to-installed parity, the exact three stale-file byte changes, unchanged closed analyst roster/profile hashes, unchanged settings/permission hashes, unchanged unrelated installed skill digests and unchanged project-mirror digests. Do not run make sync-dev: no canonical or project-copy change is needed. Run the focused contract suite and read-only make verify-sync, saving ./artifacts/canonical-contract-after.log and ./artifacts/verify-sync.log. Launch one troubleshoot-analyst with explicit verified model=sonnet/Tier1b to Read only the new installed contract and a small existing source excerpt and return data to the parent; preserve actual response and invocation provenance in ./artifacts/restricted-worker-smoke.json. It must not run commands, tests, experiments, mutations or delegation. A fresh explicit Tier1b reviewer checks installation evidence, invariance and smoke and returns ./artifacts/compatibility-review.json. Stop at compatibility readiness or a precise blocker, not PR remediation or merge.

Acceptance criteria:
- R-004, R-008, R-009: the guarded selective installer succeeds; exact canonical parity and only the three approved byte changes are proven. All profile/permission/settings/unrelated-skill/project-mirror baselines remain unchanged; no broad-copy, extra capability, alternative profile or installed hand-edit is used.
- R-002, R-010, R-011: actual focused tests and read-only sync verification pass; explicit Tier1b restricted worker completes the tiny allowed Read-only smoke with actual data and invocation provenance. Missing/incorrect model, unavailable worker, failed tests or changed invariants block readiness rather than trigger fallback.
- R-001, R-012: fresh independent Tier1b review confirms compatibility and preserved boundaries with real evidence. The final outcome gives readiness or a precise blocker and actual artifact paths, preserves all old failed reports/caps and first plan/check, and makes no claim of reader/CI repair, PR push, extra review allowance, merge or closure. .dev/tasks remains staged and .claude mirrors are never staged.
