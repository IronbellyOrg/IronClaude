# Refactoring Plan

Base: Variant 2. Auto-approved.

## Planned Changes
1. Add V3 halt table + citation obligation + slim E-* into STOP/QA sections.
2. Replace V2 unbounded "fix or Ruling" with V1 one-fix-then-HALT; operator-only Ruling.
3. Replace item-text-is-AC with V3 verb+object else E-NO-AC before edit.
4. Add start-SHA (V1/V3). Add refs/qa.md + refs/ledger.md (not a third intake ref).
5. Keep V2 delete-table verbatim. Keep no 20-cap; add warn at N≥20.
6. MDTM: this protocol; `/task` only in Will-Not.

## Changes NOT Being Made
- V1 MDTM STOP-redirect (detector untestable; majority V2+V3 R2)
- V3 20-task hard cap / `--allow-large`
- V2 executor-authored Ruling on `extra`
- `--reviewer` / `--force` flags
- Python CLI / selfcheck.py as required (optional grep fixtures only)
