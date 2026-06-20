# FR-3.7 / M-ARC2 — Retention-Sweep Prefix Extension (cross-spec dependency)

**Date:** 2026-06-03
**Step:** Phase 4, Step 4.8

## Requirement
FR-3's Wave-6 handoff memories use the `reflect/handoff-{slug}-{timestamp}` namespace. Without retention,
these would accumulate unbounded across `--remediate` runs (one per Tier-3 run). FR-3.7 / M-ARC2 requires
that `reflect/handoff-*` be pruned under the shared 90-day-expire / 20-entry-cap policy.

## Cross-spec coordination
- **The retention sweep itself is implemented in the low-spec FR-RV3-LOW.8** (SKILL.md §6.3 "Retention sweep
  (Wave 5/0, FR-8)" — the `list_memories` → `delete_memory`/`rename_memory`/`edit_memory` CRUD sweep). The
  low-spec task `TASK-RF-20260602-135209` (DONE) owns the sweep logic.
- **This medium task records the required prefix extension:** the sweep's prefix set MUST include
  `reflect/handoff-*` (alongside `reflect/last-pass-*` and `reflect/deviation-patterns-*`). This is now noted
  in SKILL.md §6.3 at two sites: the handoff-schema paragraph and the FR-8 sweep "Sweep rules" bullet
  ("Handoff-prefix membership (FR-3.7 / M-ARC2)"). The medium edit does NOT duplicate the sweep logic — it
  only records prefix membership.

## Verification
This is verified by an eval (Phase 6 `serena-handoff` case) asserting that **N > 20 handoff entries trigger a
sweep** that prunes `reflect/handoff-*` down to the 20-entry cap. The low-spec sweep is the owner; the medium
eval confirms the prefix is in-scope.

## Sweep owner
- Owner task: `TASK-RF-20260602-135209` (low-spec FR-RV3-LOW.8) — DONE.
- This record: the prefix-extension coordination note required by FR-3.7.
