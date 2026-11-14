# Proposal B: the owner runs the live reads by hand

## Answer

The owner runs the read-only capture (XC-03), the join comparison (XC-04) and the seeded test (OB-03) personally, from a plain terminal that holds no Run, following written procedures an agent prepares. No agent session touches live Orca for these items.

## What happens next if the owner picks it

1. An agent writes three step-by-step procedures into the ledger: the exact read commands for XC-03, the sweep and observer commands for XC-04, and the seeded-test steps for OB-03 (plain terminal, `run-create` only, never `run-use`, `run-current` recorded before and after: ADJ line 459).
2. The owner runs XC-03 when convenient in W1 and pastes or saves the sanitised output; an agent checks it against the procedure and writes the dated capture file.
3. After PR #539 merges and the sweep is runnable, the owner runs XC-04 the same way in W3.
4. The owner runs OB-03 when they choose; its record names them as the actor.

## What it unlocks

- The most direct authority: a person, not an agent, makes every live Orca call, so no permission row is delegated to an agent for live reads.
- No dependence on whether the 409 session is alive (UNVERIFIED), and no new worktree.
- Matches ADJ's own phrasing for the seeded test, "owner or 409 session" (ADJ lines 192, 459, 470).

## What it costs or risks

- Owner time is the scarcest resource in this program ("Owner latency is the real schedule", merged-requirements.md line 523); three live sittings add to it.
- Hand-run commands are more likely to drift from the procedure (a typo, a different terminal, a `check` run by mistake, which consumes messages).
- The records are pasted output; an agent cannot re-run them to check.

## What stays unresolved

- When the owner has time for each sitting.
