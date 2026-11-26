# Refactoring Plan

## Overview

- Base variant: Variant 2 (`flags-t1.md`)
- Incorporated variants: Variant 1 (`flags-user.md`)
- Planned changes: 2
- Overall risk: Low (additive wording only)

## Planned Changes

1. **Note the shared `update` path in the Type reason.** Source: Variant 1 advocate, A-002. Target: Type row, Reason column. Approach: append. Rationale: A-002 was rejected by both advocates with code evidence (`main.py:401-403`). Risk: Low.
2. **Record that the area is contested.** Source: debate X-001 (unresolved, 50%). Target: Type row, Reason column. Approach: append "`cli` (the user's flag) is also defensible". Risk: Low.
3. **Decided-by line.** Target: header. Approach: replace with "sc:adversarial merge (base: issue-worker-t1; incorporated: user flags)". Risk: Low.

## Changes NOT Being Made

- X-001: the Type value stays `install` (base). It was not resolved in debate; the base keeps its value, and the issue is still filed with the user's `cli` (refs/create.md Wave 2), with the difference explained in the pushback comment.
- C-002: Mode reason wording is kept from the base; it is equivalent.

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1-3 | Low | Wording of one reason and the header | Revert to `flags-t1.md` |

## Review Status

Auto-approved, 2026-11-26T18:37:54Z.
