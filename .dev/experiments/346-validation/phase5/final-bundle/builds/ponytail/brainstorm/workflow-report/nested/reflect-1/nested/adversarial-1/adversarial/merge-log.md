# Merge Execution Log

## Metadata
- Base: Variant 3 (`variant-3-original.md` = reviewer-3-card.yaml, refactorer, opus, calibrated C 0.81)
- Executor: merge-executor agent
- Changes applied: 14 of 14
- Status: success
- Timestamp: 2026-11-08T19:05:00Z
- Output: `../merged-findings.yaml`

## Changes Applied

### Change 1: Restructure into merged schema and add header
- **Status**: Applied
- **Source**: S-001, S-002, S-003 (unanimous)
- **Target**: whole document
- **Before**: base card with top-level `reviewer`, `persona`, `model_class`, `self_confidence`, `findings` (R3-F1..R3-F6), `actively_checked`, `calibration`
- **After**: provenance header (3 required `#` lines plus one comment naming the plan and spec abbreviations); top-level keys `merged_from` (3 cards under `../../reviewer-cards/` with persona, model_class, calibrated C), `weighting`, `severity_rule`, `findings`, `recorded_not_findings`, `dropped`, `probe_raised`, `actively_checked`, `checked_sound`, `debate_status` (convergence 1.00 diff-point alignment, BLOCKED_BY_INVARIANTS by INV-001 and INV-003, rounds 2 + 2.5, depth standard)
- **Provenance tag**: `# Source: Base (original, modified) — ... per Change #1` on `merged_from`; `# Source: Change #1` on `weighting`, `severity_rule`, `debate_status`
- **Validation**: key list matches Change 1 exactly, in order

### Change 2: F-01 = C-001 drift pin vs no-src pin
- **Status**: Applied
- **Source**: Variant 1 R1-F1; INV-005
- **Target**: findings[0] (insert)
- **Before**: absent from base
- **After**: blocking, necessary deviation (spec-inherited); evidence spec-panel.md:220, plan:134, 147, src.md:237-239, INV-005 cmp result; recommendation keeps V1's two options with INV-005's cost for each; owner call; debate 95%, no dissent
- **Provenance tag**: `# Source: Variant 1, R1-F1 — merged per Change #2 (...INV-005)`
- **Validation**: R1-F1 exists in reviewer-1-card.yaml

### Change 3: F-02 = C-005 FR-8/FR-9 protection
- **Status**: Applied
- **Source**: base R3-F2; V1 R1-F6; V2 Round 2 evidence (src.md:140); INV-007
- **Target**: findings[1] (modify base)
- **Before**: R3-F2 blocking, claimed "K6 in Task 3 cannot refuse reverting such an id"; recommendation required a state.json protected flag
- **After**: blocking, drift; "K6 cannot refuse" removed; evidence adds no FR-8/FR-9 string in the plan, plan:55, 58, AC plan:64 vs src.md:231, src.md:140, INV-007; recommendation = tag as state.json flag or fix-list class/blocking flag from spec-panel.md:259, plus src.md:231 test, K6 CHECK_FAIL case, K4 pinned to the fix-list grade cell; debate 85%
- **Provenance tag**: `# Source: Base (original, modified) R3-F2 — narrowed per Round 2 ...; Variant 1, R1-F6 — merged per Change #3; Invariant probe INV-007 ...`
- **Validation**: R3-F2, R1-F6 exist in their cards

### Change 4: F-03 = C-002 Usage flags, downgraded to minor
- **Status**: Applied
- **Source**: base R3-F1; V1 R1-F2
- **Target**: findings[2] (modify base)
- **Before**: R3-F1 blocking; recommendation "decide on `[--improve]`"
- **After**: minor, drift; narrowed to `--unattended` and `--report-dir` (`--improve` used in person mode, spec-panel.md:35); V3 fix kept; INV-006 note added
- **Provenance tag**: `# Source: Base (original, modified) R3-F1 — downgraded ...; Variant 1, R1-F2 — merged per Change #4`
- **Validation**: R3-F1, R1-F2 exist

### Change 5: F-04 = C-003 exit 2 on DISAGREE
- **Status**: Applied
- **Source**: base R3-F3; V1 R1-F7; V2 QA-001
- **Target**: findings[3] (modify base)
- **Before**: R3-F3 minor, one-line evidence, recommendation "test the exit code"
- **After**: minor, drift; V2's quoted lines (src.md:183, plan:101, plan:114); V2's test recommendation (427-mode disagreement and closed-minor id graded blocking by review 3); debate 90%
- **Provenance tag**: `# Source: Base (original, modified) R3-F3 — ...; Variant 1, R1-F7 and Variant 2, QA-001 — merged per Change #5`
- **Validation**: R3-F3, R1-F7, QA-001 exist

### Change 6: F-05 = C-004 DOWNGRADE on failed check
- **Status**: Applied
- **Source**: base R3-F4; V1 R1-F4; INV-008, INV-002
- **Target**: findings[4] (modify base)
- **Before**: R3-F4 minor; recommendation "read DOWNGRADE lines only when check passed, or narrow the AC"
- **After**: minor, drift; recommendation = count DOWNGRADE ids only when state is `applied(...)`, after APPLY_STOP records its state; CHECK_FAIL and APPLY_STOP plus DOWNGRADE fixtures; INV-008 recorded as dissent-by-probe; debate 75%
- **Provenance tag**: `# Source: Base (original, modified) R3-F4 — ...; Variant 1, R1-F4 — merged per Change #6; Invariant probe INV-008, INV-002 ...`
- **Validation**: R3-F4, R1-F4 exist

### Change 7: F-06 = C-010 post-`os.replace` recovery
- **Status**: Applied
- **Source**: V2 QA-002; V1 Round 2 evidence; INV-011
- **Target**: findings[5] (insert)
- **Before**: absent from base; QA-002 was blocking, drift
- **After**: minor (fix required), necessary deviation (spec-inherited); V2's quoted lines plus V2 Round 1 and V1 Round 2 owner-count evidence (plan:101 vs plan:21); recommendation = restore S from `D/current-before-audit.md` with `audit: skipped(apply failed)`, or write metadata before the replace, plus fault-injection tests; dissent V1 drift (spec-inherited)
- **Provenance tag**: `# Source: Variant 2, QA-002 — merged per Change #7 (...)`
- **Validation**: QA-002 exists in reviewer-2-card.yaml

### Change 8: F-07 = C-006 staging
- **Status**: Applied
- **Source**: base R3-F5; V1 R1-F9 part b
- **Target**: findings[6]
- **Before**: R3-F5 minor
- **After**: minor, drift; base recommendation unchanged; R1-F9 part b evidence added
- **Provenance tag**: `# Source: Base (original) R3-F5; Variant 1, R1-F9 part b — merged per Change #8`
- **Validation**: R3-F5, R1-F9 exist

### Change 9: F-08 = C-007 fix_audit.py missing from the no-src pin
- **Status**: Applied
- **Source**: V1 R1-F9 part a; V3 Round 2 evidence (plan:29, 182)
- **Target**: findings[7] (insert)
- **Before**: bundled inside R1-F9
- **After**: minor, necessary deviation (spec-inherited); dissent V1 drift (spec-inherited)
- **Provenance tag**: `# Source: Variant 1, R1-F9 part a — merged per Change #9 (...)`
- **Validation**: R1-F9 exists

### Change 10: F-09 = C-009 brittle source.md path
- **Status**: Applied
- **Source**: V1 R1-F5
- **Target**: findings[8] (insert)
- **Before**: absent from base
- **After**: minor, regression, INFERRED; dissent V2 drift; debate 75%
- **Provenance tag**: `# Source: Variant 1, R1-F5 — merged per Change #10`
- **Validation**: R1-F5 exists

### Change 11: N-01 recorded, not a finding
- **Status**: Applied
- **Source**: base R3-F6; V1 R1-F3
- **Target**: `recorded_not_findings`
- **Before**: R3-F6 a minor finding in base
- **After**: N-01, authorized expansion (owner ruling msg_2000b167e322); note: plan should cite the ruling at plan:193 and may label T10 control-arm reference only
- **Provenance tag**: `# Source: Base (original, modified) R3-F6 — moved out of findings per Change #11; Variant 1, R1-F3 — merged per Change #11`
- **Validation**: R3-F6, R1-F3 exist

### Change 12: D-01 dropped
- **Status**: Applied
- **Source**: V1 R1-F8
- **Target**: `dropped`
- **Before**: R1-F8 minor in V1
- **After**: D-01 with reason (calibrator not-confirmed, V1 conceded, speculative)
- **Provenance tag**: `# Source: Variant 1, R1-F8 — merged per Change #12`
- **Validation**: R1-F8 exists

### Change 13: `probe_raised`
- **Status**: Applied
- **Source**: invariant-probe.md
- **Target**: new section after findings
- **Before**: absent
- **After**: P-01 INV-001 and P-02 INV-003 (severity_candidate blocking), P-03 INV-002 and P-04 INV-004 (severity_candidate minor), each `cards: []`, status "not debated; caller must validate", evidence from the probe table; then a `low_items` entry listing INV-006, INV-009, INV-010, INV-012 with one-line summaries
- **Provenance tag**: `# Source: Invariant probe INV-NNN — merged per Change #13` on the section and on each item
- **Validation**: all 8 INV ids exist in invariant-probe.md with the stated severities

### Change 14: Coverage statements
- **Status**: Applied
- **Source**: base `actively_checked`; V2 `actively_checked`; V1 `checked_sound`
- **Target**: `actively_checked` (union, per-reviewer entries), `checked_sound` (A1-A3)
- **Before**: one string per card
- **After**: `actively_checked` lists reviewer 3 and reviewer 2 texts verbatim (reviewer 2 entry notes its T1 Q1 dismissal was conceded in Round 2, per base-selection.md); `checked_sound` lists V1's A1-A3
- **Provenance tag**: `# Source: Base (original, modified) actively_checked — union with Variant 2 ... per Change #14`; `# Source: Variant 1, checked_sound — merged per Change #14`
- **Validation**: text matches the source cards

## Post-Merge Validation

### Structural Integrity
- YAML parses: yes, via `uv run --no-project --with pyyaml python -I -c "...yaml.safe_load..."`. The exact prescribed command `uv run --no-project python -c ...` failed with `ModuleNotFoundError: No module named 'yaml'`; the `python3 -c` fallback was blocked by the session's UV-only hook, so PyYAML was supplied with `--with pyyaml`.
- Top-level keys: all 10 present, in the Change 1 order.
- Finding ids: contiguous F-01..F-09; every finding has all 12 schema fields.
- 23 `# Source:` comments; the 3 provenance header lines are the first lines of the file.

### Internal References
- Every `card_id` in `findings`, `recorded_not_findings` and `dropped` was checked against the `findings` ids of its source card (`../../reviewer-cards/reviewer-N-card.yaml`), and its card number is in the item's `cards` list.
- Count: total 18, resolved 18, broken 0.
- Every card finding id (R1-F1..R1-F9, QA-001, QA-002, R3-F1..R3-F6) is placed somewhere; none left out.

### Contradiction Re-Scan
- No finding carries two severities (F-01, F-02 blocking; F-03..F-09 minor).
- Only card id in two findings: R1-F9 (F-07 part b, F-08 part a), the split the plan prescribes (S-003, Changes 8 and 9).
- Probe items carry `severity_candidate`, not `severity`, and `cards: []`, so they cannot be read as merged findings.

## Summary
All 14 planned changes applied in order to the Variant 3 base. Output holds 9 findings (2 blocking: F-01, F-02), 1 recorded note (N-01), 1 dropped item (D-01), 4 probe-raised candidates (2 blocking candidates INV-001, INV-003) plus 4 LOW probe items. Validation passed. Deviations, all structural, none changing content:
1. `probe_raised` is a list; `low_items` is its last element (a one-key mapping), because a YAML list cannot also carry a sibling `low_items` key.
2. One extra header comment line names the plan (`plan:N`) and spec (`src.md:N`) abbreviations used in the evidence.
3. The YAML parse used `--with pyyaml` (see Structural Integrity).
