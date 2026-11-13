# Refactor plan (brief)

Base: V3 (opus:refactorer) card. The changes below turn it into merged-output.md.

1. **Import from V2**:
   - R2-F1 becomes MF1 (MAJOR, blocking).
   - R2-F2 merges with R1-F1 into MF2 (MAJOR, blocking), with V2's wider case list.
2. **Import from V1** the defects V3 lacks:
   - R1-F3 becomes MF11.
   - R1-F4 becomes MF13, with the halt-before-request case added.
   - R1-F5 becomes MF8.
   - R1-F6's second part (row 11 `notes`) becomes MF6.
   - R1-F7 becomes MF18.
3. **Deduplicate into V3's findings**:
   - R1-F2 into R3-F1 (MF4).
   - R1-F6 (first part) and R2-F4 into R3-F9 (MF5).
   - R2-F3 into R3-F5 (MF7).
   - R1-F8 into R3-F12 (MF10).
4. **Correct the base**:
   - Reject R3-F3.
   - Downgrade R3-F4 to MINOR (MF14).
   - Narrow R3-F11's claim (MF12).
   - Refocus R3-F8 on Task 12's unspecified form (MF9).
5. **Keep V3's unique findings unchanged**: F2 (MF3), F6 (MF15), F7 (MF16), F10 (MF17).
6. **Renumber** as MF1 to MF18: blocking MAJOR, then MAJOR, then MINOR. Use the highest calibrated confidence and the union of citations (cap 8).

Integration risk is low: every change is a row-level addition, merge or correction, and no claim depends on another row.
