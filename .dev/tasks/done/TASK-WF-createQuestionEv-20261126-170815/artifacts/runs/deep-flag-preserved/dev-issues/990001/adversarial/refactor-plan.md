# Refactoring Plan

## Overview
- Base: Variant 2 (flags-t1.md)
- Incorporated: Variant 1 (flags-user.md); the shared qualifications A-001, A-002
- Planned changes: 3
- Overall risk: Low (additive)

## Planned Changes

1. **Record the user's flags as the filing decision.** Source: Variant 1, "Decided by: user (taken as given)" and Mode `bug`. Target: a new "Filing" section after the table. Approach: append. Rationale: both Round 1 advocates (C-001 verdicts) said the user's flag stays authoritative and the evidence becomes dissent. Risk: Low.
2. **Add the A-001 boundary.** Source: shared QUALIFY (both advocates). Target: a new "Agreed qualifications" section. Approach: append. Text: the count line prints after the Step 10 retire step and also on the `sys.exit(1)` path (`main.py:271-296`). Risk: Low.
3. **Add the A-002 count definition.** Source: shared QUALIFY. Target: "Agreed qualifications". Approach: append. Text: "copied" = the installed bucket of `install_all_skills` (`install_skills.py:119`), not the skipped, served-by-command or failed buckets; the zero case (`install_skills.py:142-143`) still prints a 0 line. Risk: Low.

## Changes NOT Being Made
- C-003: keep Variant 2's evidence-cited reasons; Variant 1's "passed as flag" adds nothing (conceded).
- Mode cell in the table: kept as Variant 2's `feature` (the evidence verdict). The filing decision in Change 1 is separate from it.

## Risk Summary
All changes are additive to a decision record; rollback means deleting the appended sections.

## Review Status
Auto-approved (non-interactive), 2026-11-26.
