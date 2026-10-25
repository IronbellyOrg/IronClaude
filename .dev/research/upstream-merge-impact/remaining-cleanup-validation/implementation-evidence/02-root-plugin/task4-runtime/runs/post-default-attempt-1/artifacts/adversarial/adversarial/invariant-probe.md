# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis
Fault-finder: general-purpose Task worker, model sonnet (independent of the opus advocates), agentId a65ba8f4df080ff63, Read/Grep/Glob only. No branch-trace.md existed, so sufficiency findings use an inline source enumeration. Note: the fault-finder also read outside the snapshot (the live fixture directory and the ancestor worktree pyproject.toml), read-only.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | "`python -m pytest` from the project root, exit 0, 2 collected" alone closes R-003; "root" is unambiguous with no ambient config | UNADDRESSED | MEDIUM | Gates G1 runner config/rootdir and G2 `src.greeting` import are never shown (execution.log:1,5; tier1-card.yaml:42); G3-G5 static only (tests/test_greeting.py:4-13; src/greeting.py:2-4). The fixture is nested in the IronClaude worktree, whose /config/workspace/IronClaude/.dev/worktrees/ci-followup/pyproject.toml has [tool.pytest.ini_options] (:107-116) and a pytest11 plugin superclaude.pytest_plugin (:75-76); ancestor ini discovery could load unrelated config/plugin; possible `src` namespace-portion merge [INFERRED] |
| INV-002 | collection_boundaries | "2 tests collected" is stable and "no package markers" was verified for the real project | UNADDRESSED | MEDIUM | "Root" is ambiguous (fixture, snapshot, worktree); worktree testpaths=["tests"] (pyproject.toml:108) would collect the IronClaude suite; the verifier needs an explicit path/cwd. The C-004 Glob was of the curated snapshot (input-snapshot.yaml:17 file_count 6); a live fixtures/** Glob confirms no markers. proposed.md exists outside the snapshot (tier1-card.yaml:61; proposed.md:9-10 consistent); A-001 unresolved (tied) |
| INV-003 | state_variables | A recorded run proves R-003 for the audited artefacts; scope inclusion does not invalidate audit state | UNADDRESSED | MEDIUM | Audit state pinned by input_tree_sha256/per-file hashes (input-snapshot.yaml:1,13-16); closure does not bind the run to those hashes; A-004/A-005 unresolved; tests untracked, no commits (tier1-card.yaml:35); scope change alters the hash set; the carry-over of static acceptance/confidence is unstated (tier_decision.yaml) |
| INV-004 | guard_conditions | The `if not name` breadth is non-gating; test_empty is a faithful R-002 exercise | ADDRESSED (breadth via CG-1) / UNADDRESSED (secondary) | LOW | Whitespace accepted (variant-3 CG-1); None gets ValueError not TypeError (tier1-card.yaml:50), safe only under A-006, whose reuse evidence is degraded grep-level (reuse-audit.yaml); test_empty accepts any ValueError (tests/test_greeting.py:11) but is mutation-sensitive (line 13); pytest exit 5 on zero collected, so "2 collected" is required |
| INV-005 | count_divergence | "0/0/0/0, regression_present false, all 30 agreed ≥2/3" is a coherent count basis | UNADDRESSED | MEDIUM | 0/0/0/0 beside two open gaps can read as clean; regression_present means "not observed", not "ruled out" (nothing executed); 3 tasks vs 2 classified rows + 1 pointer row; ties are not ≥2/3 agreement of a winner; adopted U-005/U-006 lie outside the 30 points; diff-analysis totals 37/30/24 differ by basis |
| INV-006 | interaction_effects | The recommendations are independent and order-safe | UNADDRESSED | MEDIUM | Adding src/__init__.py / pythonpath is a new unmapped hunk (the Drift pattern) and changes namespace behaviour; run order before/after REC-2 differs; plain pytest vs python -m pytest verifiers test different import paths; narrowing to name == "" makes greet(None) return "Hello, None!"; editing the guard invalidates R-002 static acceptance and the hashes; the T1 DEV-1 reclassification must be explicit |
| INV-007 | sufficiency_challenge | "Captured failure counts as evidence" and "scope AND run" are jointly decidable by the user | UNADDRESSED | LOW | The scope decision is the user's (tier1-card.yaml:37-39) but the run is an orchestrator action (reviewer allowlist has no Bash); no actor is defined for the combined closure; the post-failure state transition (regression/necessary re-evaluation, reopening 0/0/0/0) is undefined |
| INV-008 | state_variables | completed.md `status: done` and the execution.log T-lines do not affect acceptance | ADDRESSED | LOW | completed.md:2,8 and execution.log:4 are claims; execution.log:1,5 disclaim execution; the consensus records the completed.md rule (U-006); residual: provenance unsupported rather than refuted (A-004 tie) |

## Summary

- **Total findings**: 8
- **ADDRESSED**: 1 (INV-008) + 1 partial (INV-004 breadth)
- **UNADDRESSED**: 7 (counting INV-004's secondary part)
  - HIGH: 0
  - MEDIUM: 5 (INV-001, INV-002, INV-003, INV-005, INV-006)
  - LOW: 2 (INV-004 secondary, INV-007)

Invariant probe gate: no HIGH+UNADDRESSED items, so convergence is not blocked. WARNING: 5 MEDIUM-severity UNADDRESSED invariant(s): INV-001, INV-002, INV-003, INV-005, INV-006. These do not block convergence but must be carried into the merge.
