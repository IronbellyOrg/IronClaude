# Diff Analysis: Position Paper Comparison (D10 wake transport)

## Metadata
- Generated: 2026-11-20 (Step 1, orchestrator-run analysis; no model-agent was needed for 2 short variants)
- Variants compared: 2 (Variant 1 = OURS `variant-1-original.md`; Variant 2 = CLAY `variant-2-original.md`)
- Total differences found: 13 (structural 1, content 8, contradictions 2, unique 4 listed separately, shared assumptions 4)
- Categories: structural (1), content (8), contradictions (2), unique (4), shared assumptions (4)
- Mode: A (compare existing files), depth standard, unattended, no `--interactive`

## Structural Differences

| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Severity |
|---|------|------------------|------------------|----------|
| S-001 | Mechanism length | 3 steps (launch, claim files, coordinator reads) | 5 steps (file, mailbox, typed line, ack, session start) | Low |

Both papers use the same section skeleton (claim, mechanism, cited facts, costs, risks, gets right). No other structural difference.

## Content Differences

| # | Topic | Variant 1 (OURS) | Variant 2 (CLAY) | Severity |
|---|-------|------------------|------------------|----------|
| C-001 | Channel from the poll to the coordinator | No new channel: launch a claim session by `orca agent launch` with an integer-only prompt; coordinator reads the claim's files at its own gates | Wake file (truth) plus Orca mailbox message plus typed line to an idle session | High |
| C-002 | Acknowledgment and delivery guarantee | None; poll cannot tell the coordinator saw the claim; `pending` record guards only against double launch | At-least-once: ack file, resend up to 3 times, then unread mark and exit 7 | High |
| C-003 | Coder issue 477 listener | Rejected by D1 option A, NG-1, owner Q3 (narrow to read-only, no prompt routing) | Rejected (same documents, D:66) | Low (agreement) |
| C-004 | Starting a session when none is live | `orca agent launch --agent claude --prompt ...` (one Orca verb, receipt, operation id, retry) | `terminal create`, type `ccsession <tag> --tier <t>`, answer the "Session name" question, wait for idle | Medium |
| C-005 | Reuse of Orca terminal code | No copy; relies on one Orca verb | About 100 to 150 lines copied from `orca_term.py`; no parity test; accepted as K16 with a follow-up | Medium |
| C-006 | Typing into a terminal | Owner decision 6 dropped typed text as an approval route | Typed line allowed to an idle session; line holds only a pattern-checked wake id | Medium |
| C-007 | Cost per assignment | One model session per claim | Script-only until a session reads the wake; idle poll costs no tokens | Medium |
| C-008 | Coordinator down | "Nothing starts while the coordinator is down" (`issue-watcher.md:43`) | Poll starts a session when none is live | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Is the typed-line wake "a pattern that runs" or unproven? | Unproven by Clay's own register (K11, U5, U25) | "Existing practice on master" (report waker) | Medium |
| X-002 | Where the "no GitHub text reaches a prompt" rule belongs | The owner's D3 (integer only), built and tested | New in the wake design, stated for every channel (typed line, mailbox subject, argv) | Medium |

Resolution notes (evidence read by the analyst): X-001 is partly both. The report waker (`waker.py`, `orca_term.py`) exists on master and sends a typed wake line to the report session; the orchestrator wake itself has no live run (design K11 `D:1233`, U5 `D:1263`). X-002 is not a factual conflict: Clay's design calls its rule "the carried-over ... rule in its new form" (D:155), so the rule is the owner's D3 generalized.

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | Variant 1 | Owner Q3 narrowed Coder 477 to read-only with no prompt routing; owner decision 6 dropped typed text for approvals | High |
| U-002 | Variant 1 | Launch already merged with crash protection (pending write, operation id retry) and parity tests for its helpers | Medium |
| U-003 | Variant 2 | Durable wake file plus ack, resend, unread mark (K14): a loss of a wake is loud | High |
| U-004 | Variant 2 | The rule extended to mailbox subject and every argv built from a wake field (D:234 guarantee 2); the weakness that a title travels in `plan_requests[]` is disclosed | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Promoted | Impact |
|-------|-----------|------------------|----------------|----------|--------|
| A-001 | The poll must push a signal; the coordinator itself cannot discover new work (e.g. by its own `check --wait` loop plus a cheap script read of the claim store) | Both treat "wake" as a message to be sent | UNSTATED | Yes | High: if the coordinator can poll the durable file itself, the typed line and mailbox become optional accelerators |
| A-002 | Orca screen state (`draft`, `lastOutputAt`, `tui-idle`) is reliable enough to decide that typing is safe | CLAY states it; OURS avoids it | STATED (by CLAY only) | No | Medium |
| A-003 | Poll, coordinator session and `/proc` are on one host (single-host) | Both; CLAY's `/proc` lookup and local wake file require it; owner Q4 line "single-host" | UNSTATED | Yes | Medium: a coordinator on another workspace cannot be woken by file, `/proc` lookup or local typed line |
| A-004 | The transport is separable from the contested trigger and plan-hold rules (it can carry ids only) | CLAY asserts it (H-map "worth folding in"); OURS does not contest | STATED | No | Medium |

## Summary
- Total structural differences: 1
- Total content differences: 8
- Total contradictions: 2
- Total unique contributions: 4
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, A-001
- Taxonomy tags (AD-5): C-001 L2 (structural), C-002 L3 (state mechanics: acknowledgment, retry), C-005 L1/L2, C-006 L3 (guard), A-001 L3 (state), A-003 L3 (boundary)
