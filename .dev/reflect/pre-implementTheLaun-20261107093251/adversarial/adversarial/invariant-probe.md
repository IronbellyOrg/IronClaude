# Invariant Probe Results

## Round 2.5: Fault-Finder Analysis (independent opus-class agent; evidence read from the files named)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | After M-01 (fixture migration) and M-03 (ownership predicate) Task 20's "L2 present and owned, launch proceeds" test can be built | UNADDRESSED | HIGH | PLAN:318-320 needs an owned shared hook file plus a contract marker; its install place U28 is unverified (DESIGN:377,457; PLAN:333); the shared pre-push is "proposed, blocked by B-CTX" (DESIGN:41) and L2 is built only after B-CTX (DESIGN:366); DESIGN:512 rejects a header as ownership proof. No fixture can stand in for an owned L2 while the path and format are open. |
| INV-002 | guard_conditions | Task 18's jq and CLAUDE_CONFIG_DIR checks describe the environment the guard will run in | UNADDRESSED | MEDIUM | The check runs in the claim script's process (PLAN:291-293); the agent starts via orca agent launch (OW:951-954); DESIGN:316 lists hook HOME and CLAUDE_CONFIG_DIR as still to observe in OB-H2; the test double copies os.environ (TOW:102-111). |
| INV-003 | guard_conditions | The remedy "superclaude install, then claim again" repairs a stale or stub guard | UNADDRESSED | MEDIUM | _copy_scripts skips an existing destination unless force is set (IH:252-254); install passes force=force (src/superclaude/cli/main.py:217); main.py:394 calls install_hooks(force=True) for an unchecked command. A version-line refusal could repeat. |
| INV-004 | count_divergence | "12 tests" is the full set that breaks and "31 uses" means call sites | UNADDRESSED | LOW | 12 "launched" asserts (TOW:1051,1124,1196,1210,1234,1265,1276,1301,1481,1534,1571,1594); also la2 (TOW:1090-1103), TOW:1246,1291,1313 and pr425 (TOW:1491,1513-1519); 31 occurrences include the definition at TOW:994, so 30 call sites. |
| INV-005 | interaction_effects | The order of the new IR-4 and IR-7 checks inside cmd_launch does not matter | UNADDRESSED | MEDIUM | Current order: already_launched (OW:915-933), stale_prompt (OW:934-936), enforcement_status (OW:937), publish_pending (OW:941); the stale-prompt tests (TOW:1617-1677) and la3 (TOW:1147,1165) flip with the order. |
| INV-006 | collection_boundaries | "--pipeline none is unaffected" is testable as Task 20 plans | UNADDRESSED | MEDIUM | PLAN:320 asks for it; the launch subcommand rejects --level none with exit 2 (TOW:1373); none is handled at the skill level only (SKILL.md:136,150; refs/claim.md:136). |
| INV-007 | count_divergence | Task 2 has "exactly twelve" skips and Task 22 allows only observation skips | UNADDRESSED | LOW | Task 14 adds a pending hook-order observation test (PLAN:242) against PLAN:59; existing environment skips remain (tests/hooks/test_launch_job_identity.py:18; tests/hooks/test_freshness_subagent_start_policy.py:72). |
| INV-008 | interaction_effects | Task 12's order (guard before identity) holds on every install | UNADDRESSED | LOW | On upgrade _merge_settings appends new registrations at the end (IH:448) and refreshes owned entries in place (IH:410-444), so an installed identity hook stays ahead; only fresh installs are covered (HJ:75-106; TIH:826-856). |
| INV-009 | sufficiency_challenge | The gate ordering in M-02 makes the observation path reachable | UNADDRESSED | MEDIUM | DESIGN:367 allows no real governed launch before OB-H2 and OB-H3 pass; OB-H2 needs IR-4 refusals and observed hook execution (DESIGN:316,352); Task 20 refuses every governed launch (DESIGN:355; PLAN:318), so the hook behaviour OB-H2 needs cannot be observed in a governed launch (a circular gate). |
| INV-010 | state_variables | "Launch entry removed" is one place for IR-5 | UNADDRESSED | LOW | The entry is read from the record and the git-dir mirror (OW:916-919); removing one still returns already_launched; la2 removes both (TOW:1106-1125). |

## Summary

- **Total findings**: 10
- **ADDRESSED**: 0
- **UNADDRESSED**: 10
  - HIGH: 1 (INV-001)
  - MEDIUM: 5 (INV-002, INV-003, INV-005, INV-006, INV-009)
  - LOW: 4 (INV-004, INV-007, INV-008, INV-010)

Convergence gate: CONVERGENCE BLOCKED: 1 HIGH-severity UNADDRESSED invariant detected. Blocking items: INV-001. At depth standard there is no Round 3; the item is carried into the return contract as `unaddressed_invariants` and the status is partial. MEDIUM items are warnings.
