# Contract Delta — Current vs Target Field/Version State (Step 1.5)

**Date:** 2026-06-10
**File audited:** `src/superclaude/skills/sc-reflect-protocol/SKILL.md`
**Reference:** R2 research §1 (field list), §6 (version-site list)

## `remediation_task_path` hit count

**0 hits** — FR-8 gap CONFIRMED. The new field does not yet exist (additive 1.3.0→1.4.0 bump required). ✅ matches R2.

## `task_file_path` line

**Line 744:** `task_file_path: <path> | null`

Matches R2 §1 anchor (`SKILL.md:744`) EXACTLY. This is the existing Tier-3 field with unspecified
semantics; per Open-Question/R2 §1 it is NOT repurposed — `remediation_task_path` will be added as a
NEW key. ✅

## `1.3.0` occurrences (all 5 R2 §6 sites)

| Line | Site | R2 §6 anchor | Shift |
|---|---|---|---|
| 651 | §9.1 header `### 9.1 Stable contract (contract_version: 1.3.0)` | 651 | none |
| 654 | emitted field `contract_version: "1.3.0"` | 654 | none |
| 791 | §9.1 closing prose `Contract version is \`v1.3.0\`.` | 791 | none |
| 1627 | §15.1 `runs.jsonl` example `"skill_version": "1.3.0"` | 1627 | none |
| 1758 | §18 grader assertion `return-contract.yaml contract_version == "1.3.0"` | 1758 | none |

All five literal `1.3.0` sites present at the EXACT R2-anchored line numbers — **zero line shift**
on this base (the freeze captured the same SKILL.md the R2 research was run against). ✅

## State vs R2 — concordance

- `remediation_task_path` ABSENT (0) ✅ matches R2
- `task_file_path` PRESENT @744 ✅ matches R2
- 5 × `1.3.0` contract-version sites ✅ matches R2

**No divergence, no line shift, canonical base confirmed.** No blocker.
