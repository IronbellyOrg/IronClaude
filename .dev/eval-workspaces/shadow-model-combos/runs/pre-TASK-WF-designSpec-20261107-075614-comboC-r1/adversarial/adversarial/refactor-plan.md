# Refactoring Plan (base: variant 2)

## Overview
Base variant 2 (qa card). Incorporated: V1 (C-002, C-004, C-011), V3 (C-010, C-012), probe (INV-001, INV-002, INV-007). Changes planned: 9; rejected: 4. Overall risk: Low (severity and blocking edits only). Approval: auto-approved.

## Planned Changes
1. Set all seven `blocking: true` flags of V2 to false (debate: all three advocates, V2 conceded). Risk Low.
2. Drop F1 to MINOR and rewrite as the mislabel only (M9). Risk Low.
3. Rewrite F3 as the criterion gap only (M8). Risk Low.
4. Rewrite F6 as a partial-assertion gap (M10). Risk Low.
5. Keep F5 (M2), F7 (M3), F4 (M4), F2 (M6) as MAJOR non-blocking. Risk Low.
6. Add V1 F1 as M1 (MAJOR, Task 7 timeline count). Risk Low.
7. Add V1 F2 as M7, lowered to MINOR after the base-commit protocol read. Risk Low.
8. Add V3 F1 and F2 as M11 (MINOR); V1 F3 as M12.
9. Add probe INV-001 as M5 (MAJOR), INV-002 as M13, INV-007 merged into M14 with V2 F11.

## Changes NOT Being Made
- V3 F3 and F4 (classification entry versus criterion; `_RESOLUTION_SCRIPTS`): calibrated 0.45 and 0.55, advocate-3 conceded F3 weak; left out of the merged list, noted here.
- V2 F8, F9, F10, F12 (phase string case, three rules without criterion, byte-identical start text, matrix omissions): MINOR, folded into the notes of the report, not separate findings.
- Probe INV-003 and INV-004 (LOW): noted in the report body only.
- V1 "dependencies complete": withdrawn.

## Review Status
Auto-approved.
