# Invariant Probe Results

## Round 2.5: Fault-Finder Analysis (opus-class independent fault-finder; condensed by the orchestrator, evidence refs unchanged)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | The plan's tasks alone make sure no agent-launched session is stuck at the naming question | ADDRESSED (as a documented condition: orchestrators pass a task or a name; plan:125, owner decision (a)) | HIGH | `CCSESSION_NAME` is set nowhere in the repo (only CCSESSION_NAME_KEY at ccsession:270,347,438); a task typed after the question appears is read as a name (ccsession:1482-1489) and resumes a saved label (ccsession:1681-1706); keys-waiting check looks once, before the question (ccsession:1431-1437); Coder hook and bare claude wrapper out of scope, covered by the Task 11 handoff |
| INV-002 | count_divergence | Dropping the --name lift needs no other change | UNADDRESSED | MEDIUM | Task 3 criterion 2 (plan:61) and Task 7 (plan:104) still require the lift; Task 4 (plan:69) is silent on a launch with its own Claude --name; auto-naming it gives two --name options (ccsession:1712), breaking the label-equals-name rule (ccsession:1689-1690) |
| INV-003 | collection_boundaries | An auto-name cut to 80 characters always passes validate_label | UNADDRESSED | MEDIUM | validate_label limit is 245 bytes after name_to_file (ccsession:296-299) and rejects control characters (ccsession:287); plan:31 cleans only the task words; a worktree folder name with 4-byte characters or a control character makes --auto-name fail under set -e (ccsession-orca:34) |
| INV-004 | collection_boundaries | "At most 80 characters" and "-2 appended" both hold | UNADDRESSED | LOW | plan:31, plan:35-36; 80 plus "-2" is 82; the stamp should be kept and the folder name cut first |
| INV-005 | guard_conditions | Any non-option argument means the launch carries a task | UNADDRESSED | MEDIUM | plan:57 classifier, like `*) plain=0` at ccsession-orca:78, counts option values (--model opus, --permission-mode plan) as positionals; the question is skipped and the auto-name built from the option value |
| INV-006 | state_variables | The --auto-name collision check sees every saved label | UNADDRESSED | LOW | early fast path (ccsession:597-628) runs before ensure_names_migrated; the --name launch migrates afterwards (ccsession:1657) |
| INV-007 | interaction_effects | An --ask failure no longer kills ccsession-orca | ADDRESSED | MEDIUM | Task 4 removes `|| name=""` at ccsession-orca:108; with set -e a bare `name=$(...)` exits; capture rc (V1 F13) and the plan:72 criterion cover it |
| INV-008 | interaction_effects | CCSESSION_NAME does not leak into nested launches | ADDRESSED | MEDIUM | env exclusion in tests (C-002) and unset before exec; skipping the name when CLAUDECODE is set (ccsession:1620) would harden it |
| INV-009 | guard_conditions | The plain-relaunch reopen ignores CCSESSION_NAME safely | UNADDRESSED | LOW | an explicit --name blocks the reopen (ccsession-orca:75); plan:21 freezes the reopen conditions so CCSESSION_NAME does not |
| INV-010 | interaction_effects | Task 4's environment criterion can be met | UNADDRESSED | LOW | plan:72 sets CCSESSION_ASK_TIMEOUT=1 and also requires it absent from Claude's environment; needs unset before the final exec |
| INV-011 | count_divergence | The exit-3 text fits in one argument | PARTLY ADDRESSED (executor note) | LOW | Linux refuses a single exec argument over 128 KiB; under set -e Claude would not start |
| INV-012 | guard_conditions | The 30-second limit keeps a worker inside Orca's 60-second readiness window | ADDRESSED | LOW | about 25 s margin after the model refresh (about 2 s, ccsession:1577) and shim start |

## Summary

- **Total findings**: 12
- **ADDRESSED**: 4 (INV-001, INV-007, INV-008, INV-012); 1 partly (INV-011)
- **UNADDRESSED**: 7
  - HIGH: 0
  - MEDIUM: 3 (INV-002, INV-003, INV-005)
  - LOW: 4 (INV-004, INV-006, INV-009, INV-010)
- Gate result: no HIGH + UNADDRESSED item, so convergence is NOT blocked by the invariant gate. MEDIUM items are warnings and are carried into the merged verdict as required plan notes.
