# Merge log (Steps 4 and 5)

Base: V3 (opus:refactorer). Source findings: 24 (R1 8, R2 4, R3 12). Result: 18 merged findings, 1 rejected.

## Source to merged mapping

| Source | Merged | Action |
|---|---|---|
| R1-F1 | MF2 | merged with R2-F2 (C-001); blocking set true (X-002) |
| R1-F2 | MF4 | merged with R3-F1 (C-002) |
| R1-F3 | MF11 | kept (C-007, distinct from R3-F11) |
| R1-F4 | MF13 | kept; claim strengthened with the engage-halt-before-request case (INV-008) |
| R1-F5 | MF8 | kept; not merged with R3-F8 (different defect, C-005) |
| R1-F6 | MF5 + MF6 | split: the corrupt-line part merged into MF5 (C-003); the row 11 `notes` part became MF6 |
| R1-F7 | MF18 | kept |
| R1-F8 | MF10 | merged with R3-F12 (C-006) |
| R2-F1 | MF1 | kept; verified against plan:124 and spec:240 |
| R2-F2 | MF2 | merged with R1-F1; its wider case list adopted |
| R2-F3 | MF7 | merged with R3-F5 (C-004) |
| R2-F4 | MF5 | merged (C-003) |
| R3-F1 | MF4 | merged |
| R3-F2 | MF3 | kept; supersedes T1 H3 (X-001), verified against all Depends-on lines |
| R3-F3 | rejected | not a defect (see merged-output.md) |
| R3-F4 | MF14 | kept; downgraded from MAJOR to MINOR (conditional on O2, plausible owner at plan:108, loud failure at plan:142) |
| R3-F5 | MF7 | merged |
| R3-F6 | MF15 | kept |
| R3-F7 | MF16 | kept |
| R3-F8 | MF9 | kept; claim focused on the unspecified form in Task 12's AC |
| R3-F9 | MF5 | merged |
| R3-F10 | MF17 | kept |
| R3-F11 | MF12 | kept; "every named fold AC" narrowed (INV-009) |
| R3-F12 | MF10 | merged |

Check: 24 of 24 source findings accounted for. R1-F6 maps to two merged findings because it bundled two defects.

## Rules applied

- **Confidence**: the panel calibration of the source finding; for merged duplicates, the maximum of the duplicates.
  - MF2: max(0.80, 0.70) = 0.80.
  - MF4: max(0.65, 0.60) = 0.65.
  - MF5: max(0.65, 0.72, 0.65) = 0.72.
  - MF7: max(0.65, 0.75) = 0.75.
  - MF10: max(0.60, 0.60) = 0.60.
  - MF6 takes R1-F6's 0.65.
- **Citations**: the union of the source citations, with an overlapping range collapsed into its covering range (MF7: plan:154 sits inside plan:150-154). The maximum is 6, under the cap of 8. All come from the two frozen inputs.
- **Severity changes**:
  - R3-F4 lowered from MAJOR to MINOR.
  - R1-F1 kept at MAJOR, with blocking raised from false to true.
  - No other severity changed.
- **Ordering**: MAJOR blocking first, then MAJOR, then MINOR in diff-point order.

## Judge evidence beyond the source citations

- MF1: spec:240 (the ref row: "sections 3 and 4.1 to 4.4"); plan:166 (the scenario driver appends its own events).
- MF3: plan:96, 106, 120 (Tasks 6, 7 and 8 do declare Task 1); plan:135, 148, 180, 191 (the transitive chain).
- MF13: spec:140 (engage row 8 halts before any request); spec:112 (no record at ordinal 3 gives `released`).
- MF14: plan:108 ("any script list that Task 1 O2 shows is required").
