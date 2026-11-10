# Refactoring Plan: Merge into Base (Variant 3)

## Overview
- Base: Variant 3 (`variant-3-original.md` = reviewer-3-card.yaml, refactorer, opus, C 0.81)
- Incorporating strengths from: Variant 1 (analyzer, C 0.76), Variant 2 (qa, C 0.75), Round 2.5 invariant probe
- Output: `../merged-findings.yaml` (YAML; provenance as `# Source:` comments, because the cards are YAML)
- Merged schema per finding: `id`, `severity` (blocking|minor), `category` (authorized expansion | necessary deviation | drift | regression, optional "(spec-inherited)"), `cards` (card numbers that raised it), `card_ids`, `plan_task`, `spec_ref`, `summary` (one line), `evidence` (list of quoted or cited lines), `claim_tag`, `recommendation`, `debate` (consensus and dissent)
- Planned changes: 14
- Risk level: Low (data merge; no source code)

## Planned Changes

### Change 1: Restructure into merged schema and add header (all variants)
- **Source**: S-001, S-002, S-003 (unanimous)
- **Target**: whole document (restructure)
- **Rationale**: one deduplicated list; V2 `category` field and list evidence adopted; R1-F9 split.
- **Integration point**: top-level keys `merged_from`, `weighting`, `severity_rule`, `findings`, `recorded_not_findings`, `dropped`, `probe_raised`, `actively_checked`, `checked_sound`, `debate_status`.
- **Risk**: Low

### Change 2: F-01 = C-001 drift pin vs no-src pin (from V1 R1-F1), blocking
- **Source**: V1 R1-F1; INV-005
- **Target**: findings[0] (insert)
- **Rationale**: unanimous blocking, 95%; two Task 8 ACs cannot both pass (spec-panel.md:220; plan:134, 147; src.md:237, 239). Category: necessary deviation (spec-inherited).
- **Integration point**: recommendation keeps V1's two options and adds INV-005's costs (option b changes TDD behaviour because the installed template differs from `src/superclaude/examples/release-spec-template.md`; option a ships a `src/superclaude/examples` reference against plan:29 and the project CLAUDE.md rule); owner call.
- **Risk**: Low

### Change 3: F-02 = C-005 FR-8/FR-9 protection (base R3-F2, plus V1 R1-F6), blocking, narrowed
- **Source**: base R3-F2; V1 R1-F6; V2 Round 2 evidence (src.md:140); INV-007
- **Target**: findings[1] (modify base)
- **Rationale**: unanimous blocking after Round 2; plan has no FR-8/FR-9 string; plan:55, 58 drop the tag; AC plan:64 lacks the src.md:231 test. Drop "K6 cannot refuse" (conceded). Category: drift.
- **Integration point**: recommendation = carry the tag (state.json protected flag, or a fix-list class or blocking flag set from Review Loop bullet 2, spec-panel.md:259) + the src.md:231 test + a K6 CHECK_FAIL case; pin K4 to the fix-list grade cell so a tag does not fail every row (INV-007).
- **Risk**: Low

### Change 4: F-03 = C-002 Usage flags (base R3-F1 + V1 R1-F2), downgrade to minor
- **Source**: base R3-F1; V1 R1-F2
- **Target**: findings[2] (modify base)
- **Rationale**: unanimous minor (V3 conceded): the guard keys on the section heading; T08a never passes the flag. Narrow to `--unattended` and `--report-dir` (`--improve` is used in person mode, spec-panel.md:35). Category: drift.
- **Integration point**: keep V3's fix (drop the two tokens as an enumerated Task 7 difference; Task 8 asserts `--unattended` absent); note INV-006 (Fix Audit sentence "behaves exactly as /sc:spec-panel" becomes false).
- **Risk**: Low

### Change 5: F-04 = C-003 exit 2 on DISAGREE (base R3-F3 + V1 R1-F7 + V2 QA-001), minor
- **Source**: base R3-F3; V1 R1-F7; V2 QA-001
- **Target**: findings[3] (modify base)
- **Rationale**: unanimous minor (V2 conceded); FAIL still forced (plan:101, 114); spec self-inconsistent (src.md:133 vs 183). Category: drift.
- **Integration point**: merge V2's test recommendation (427-mode disagreement and a closed-minor id graded blocking by review 3 both assert exit 2).
- **Risk**: Low

### Change 6: F-05 = C-004 DOWNGRADE on failed check (base R3-F4 + V1 R1-F4), minor
- **Source**: base R3-F4; V1 R1-F4; INV-008, INV-002
- **Target**: findings[4] (modify base)
- **Rationale**: unanimous minor at 75%; probe notes the registered owner count is inflated on `skipped(check failed)` and APPLY_STOP paths (wrong-behaviour risk, recorded as dissent-by-probe). Category: drift.
- **Integration point**: recommendation = count DOWNGRADE ids only when state is `applied(...)`, after APPLY_STOP records its state (INV-002); add CHECK_FAIL and APPLY_STOP plus DOWNGRADE fixtures.
- **Risk**: Low

### Change 7: F-06 = C-010 post-`os.replace` recovery (from V2 QA-002), minor, fix required
- **Source**: V2 QA-002; V1 Round 2 evidence; INV-011
- **Target**: findings[5] (insert)
- **Rationale**: unanimous minor after Round 2 (V2 conceded), top minor, fix required; owner count can drop (plan:101 vs plan:21). Category: necessary deviation (spec-inherited) (2/3; V1: drift (spec-inherited)).
- **Integration point**: recommendation = restore S from `D/current-before-audit.md` with `audit: skipped(apply failed)` on any failure after the replace, or write the metadata before the replace; fault-injection tests for readback and each metadata write.
- **Risk**: Low

### Change 8: F-07 = C-006 staging (base R3-F5 + V1 R1-F9 part b), minor
- **Source**: base R3-F5; V1 R1-F9b
- **Target**: findings[6] (modify base)
- **Rationale**: unanimous minor; category drift.
- **Integration point**: as base recommendation.
- **Risk**: Low

### Change 9: F-08 = C-007 fix_audit.py missing from the no-src pin (from V1 R1-F9 part a), minor
- **Source**: V1 R1-F9a; V3 Round 2 evidence (plan:29, 182)
- **Target**: findings[7] (insert)
- **Rationale**: unanimous minor; category necessary deviation (spec-inherited) (2/3; V1: drift (spec-inherited)).
- **Risk**: Low

### Change 10: F-09 = C-009 brittle source.md path (from V1 R1-F5), minor
- **Source**: V1 R1-F5
- **Target**: findings[8] (insert)
- **Rationale**: unanimous minor; INFERRED; category regression (2/3; V2: drift).
- **Risk**: Low

### Change 11: Move base R3-F6 (+ V1 R1-F3) to recorded_not_findings as N-01
- **Source**: base R3-F6; V1 R1-F3
- **Target**: `recorded_not_findings` (restructure)
- **Rationale**: unanimous after Round 2: authorized expansion (owner ruling msg_2000b167e322); note: the plan should cite the ruling at plan:193 and may label T10 control-arm reference only.
- **Risk**: Low

### Change 12: Record V1 R1-F8 (C-011) under `dropped` as D-01
- **Source**: V1 R1-F8
- **Rationale**: calibrator not-confirmed; V1 conceded; speculative.
- **Risk**: Low

### Change 13: Add `probe_raised` (no card raised these)
- **Source**: invariant-probe.md
- **Target**: new section after findings
- **Rationale**: the invariant gate blocks convergence on INV-001 and INV-003 (HIGH, UNADDRESSED); they were not debated (no Round 3 at standard depth), so they carry `severity_candidate`, not a merged severity, and `cards: []`. Add INV-002, INV-004 (MEDIUM) as minor candidates; list LOW items INV-006, INV-009, INV-010, INV-012 by id.
- **Risk**: Medium — new, undebated items; the caller must validate them before treating them as findings.

### Change 14: Merge coverage statements
- **Source**: base `actively_checked`; V1 `checked_sound`; V2 `actively_checked`
- **Target**: `actively_checked` (union), `checked_sound` (V1's A1-A3)
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base / Consensus |
|------------|-------------------|---------------------------------------|
| C-003 / X-002 | V2: blocking | V2 conceded; FAIL line still forced (plan:101, 114) |
| C-010 | V2 Round 1: blocking | V2 conceded; I/O-fault trigger only; both AC sets can pass |
| C-002 / X-001 | base V3: blocking | V3 conceded; guard fails closed |
| C-008 | V1 Round 1: keep as minor finding | V1 conceded in Round 2; authorized expansion, kept as a note |
| C-007, C-010 labels | V1: drift (spec-inherited) | 2/3 majority: the plan copies the spec faithfully, so the remedy is a necessary deviation |
| C-005 fix | V3 Round 1: state.json flag required | V3 accepted V1's narrower fix (flag or class), Round 2 |
| C-004 severity | probe INV-008: meets the wrong-behaviour half | debate consensus minor (75%); recorded in `debate.dissent` rather than overridden by an undebated probe item |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1-12, 14 | Low | A finding mis-merged | Re-derive from variant-N-original.md |
| 13 | Medium | Undebated probe items read as merged findings | They sit in a separate `probe_raised` section with `cards: []` |

## Review Status
- [x] Auto-approved (default; `--unattended`, no `--interactive`)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-08T19:05:00Z
