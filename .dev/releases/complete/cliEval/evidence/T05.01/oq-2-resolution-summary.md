# T05.01 Evidence — OQ-2 Resolution Summary

**Task:** T05.01 — Clarify: E3–E15 eval body content per OQ-2 resolution
**Deliverable:** D-0082
**Date proposed:** 2026-05-20
**Date resolved:** 2026-05-20
**Status:** 🟢 RESOLVED — RyanW — 2026-05-20 (signature landed at T06.09 / R12 in the SC5 single-sweep sign-off pass; decisions.md §"OQ-2 Resolution" + §"SC5 OQ resolution ledger" → OQ-2 row)

## Summary

OQ-2 resolution proposed in `artifacts/D-0082/spec.md`:

| Eval | Title | Capability tag |
|---|---|---|
| E3  | SessionStart unmatched (session-init) hook fires | — |
| E4  | SessionStart matcher=* freshness hook fires | — |
| E5  | UserPromptSubmit freshness hook fires | — |
| E6  | PreToolUse Edit matcher fires | — |
| E7  | PreToolUse Write matcher fires | — |
| E8  | PreToolUse serena matcher fires | `mcp_server.serena` |
| E9  | PostToolUse Read async hook fires | — |
| E10 | SubagentStart hook fires | — |
| E11 | SubagentStop hook fires | — |
| E12 | Hook deploy idempotency | — |
| E13 | Hook stderr error fails open | — |
| E14 | Concurrent SessionStart bursts (callback) | — |
| E15 | Hook timeout fail-open (per design-spec §11) | — |

## Coverage assertion

100% v1 hook-event coverage (all 6 events) and 100% v1 matcher coverage (3 PreToolUse, 2 PostToolUse).
D-5 falsifiable contract satisfied by construction.

## Unblocks

T05.07–T05.21 (13 authoring tasks) become unblocked upon sign-off.

## Sign-off location

`decisions.md` §"OQ-2 Resolution — E3..E15 eval body shapes frozen (T05.01)" (sign-off table flipped 🟠 PROPOSED → 🟢 RESOLVED) + §"SC5 OQ resolution ledger (T06.09)" → OQ-2 row (status: resolved, signed_off_by: RyanW, signed_off_date: 2026-05-20).

## Files

- `../../artifacts/D-0082/spec.md` — full body shapes
- `../../artifacts/D-0082/notes.md` — design decisions
- `../../artifacts/D-0082/evidence.md` — cross-reference verification
