# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Independent fault-finder probing the emerging consensus from Round 2 across the 5-category boundary-condition checklist. Findings target invariants that the consensus implicitly assumes but does not explicitly handle.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | The `Tier:` frontmatter enum value persists across F1 resumption boundaries without runtime mutation | ADDRESSED | LOW | R2 (Advocate-1, Advocate-3): CR-FM-03 compat shim provides parse-stability; INV-04 holds at schema layer per all three R2 positions |
| INV-002 | state_variables | The `verifier_roster` initial value on non-STRICT tiers is consistent across implementers (consensus did not address it) | UNADDRESSED | MEDIUM | Source plan line 226: CR-TASK-05 specifies `[rf-qa, quality-engineer]` on STRICT but is silent on other tiers; R2 consensus did not address |
| INV-003 | guard_conditions | The `git_status` guard at STRICT pre-flight covers all observable failure modes, not just `clean` and `dirty` | ADDRESSED | MEDIUM | R2 (Advocate-1, Advocate-2): the F-03 closure asymmetry distinction (input-invalid vs environment-non-ideal) resolves the policy; AC-ATK-02 binds the five-row matrix |
| INV-004 | guard_conditions | The baseline-trinary trigger predicate (`absent|empty|malformed`) is unambiguous given a single observer (consensus pinned the disposition but not the observer order) | UNADDRESSED | MEDIUM | R3 (Advocate-3): adopt V2's four-state table {absent, empty, parse-fail, schema-fail}; observer-order still implicit — `os.path.exists` → `os.path.getsize` → `yaml.safe_load` → `<schema>` chain is the implementer's responsibility |
| INV-005 | count_divergence | The 79 row-instance / 65 distinct CR-ID condensation arithmetic is correct and complete (no orphan rows) | ADDRESSED | HIGH | R2 (Advocate-1, Advocate-3): concede V2's bucket-condensation gap; the merged spec mandates a reconciliation table as a Phase 7.5 patch obligation |
| INV-006 | collection_boundaries | The CR-TASK-12 seven-diff audit can re-run after CR-DEP-03 deletes the donor file | UNADDRESSED | MEDIUM | R2 (Advocate-2 + V3 § 6 concur): snapshot-fixture mitigation is named but not currently in the source plan; the audit has finite lifetime ending at Step 6 |
| INV-007 | collection_boundaries | The set of in-flight MDTM task files that reference deprecated surfaces is fully covered by CR-FM-03's parse-level "validates clean" guarantee | UNADDRESSED | **HIGH** | R3 (Advocate-3): 96 files reference `/sc:task`, `sc-task-protocol`, or `task-unified` (V3 § 2 grep); CR-FM-03 detects none; INV-04 semantic exposure is unhandled by the source plan as written. **Round 3 resolution**: extend CR-FM-03 with content-level audit + warn-and-continue per ME-3 |
| INV-008 | interaction_effects | The S-1 PRD precondition + S-2 atomic-commit + S-3 sync-rule constraints can all be satisfied in a single linear merge sequence without conflicting timeline assumptions | ADDRESSED | LOW | R2 (Advocate-3): S-1 `--max-wait` 14-day default + S-2 server-side pre-push hook + S-3 `flock` discipline are independently additive; no constraint interaction |
| INV-009 | interaction_effects | The F-05 mid-phase rf-qa invocation point + future authorized widenings preserve INV-03 floor monotonically (each widening strictly adds, never removes, an invocation site) | ADDRESSED | LOW | R3 (Advocate-1 + Advocate-2 hybrid): one-time-carve-out disclaimer in § 0 explicitly closes the precedent loophole; obligation #7 binds future widenings |

## Summary

- **Total findings**: 9
- **ADDRESSED**: 4 (INV-001, INV-003, INV-005, INV-008, INV-009)
  - Actually 5 — recount: INV-001, INV-003, INV-005, INV-008, INV-009 = 5 ADDRESSED
- **UNADDRESSED**: 4
  - HIGH: 1 (INV-007)
  - MEDIUM: 3 (INV-002, INV-004, INV-006)
  - LOW: 0

**Convergence gate status:** 1 HIGH-severity UNADDRESSED invariant detected after Round 2. Round 3 was triggered to resolve INV-007.

**Post-Round 3 status:** INV-007 resolved via consensus adoption of V3's CR-FM-03 content-level audit extension with explicit warn-and-continue HALT disposition (preserves INV-01 progress guarantee per ME-3). HIGH UNADDRESSED count drops to 0. **Convergence is no longer blocked.**

**Residual MEDIUM items** (INV-002, INV-004, INV-006) are acknowledged as Phase 7.5 patch obligations rather than convergence blockers. The merged spec carries them forward as named open items, not silent omissions.
