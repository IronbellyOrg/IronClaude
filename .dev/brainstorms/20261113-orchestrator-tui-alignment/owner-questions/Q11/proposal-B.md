# Proposal B: the sweep summary only, until the contract note exists

## Answer

The static chat report is the sweep's counts-and-path reply (the read-only sweep's summary of session counts plus the path of the one report file it wrote), and nothing else, until the contract note between the observer and the sweep exists. The question of adding the observer's `observe --once` text is reopened when that note lands.

## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date; section 6.7 of the spec (the coordinator's status output rule) already says this (merged-requirements.md:1040), so no spec text changes.
- Nothing in code changes: the sweep skill already prints counts and path as its only exempt reply (sc-sweep-protocol/SKILL.md:31-43; pragmatic.md:22-23).
- The worker contract and the sweep skill keep not naming `superclaude observe` (V5 D2, variant-5-original.md:222).
- When the contract note (XC-05) is written, it carries a line saying whether `observe --once` text joins the chat report.

## What it unlocks

- One source of truth in chat while the two programs still use different word lists.
- No edit to PR #539 (the open sweep PR), the worker contract or the output style.
- Keeps the read-only promise simple: the sweep is already allowed and capped at once every 5 minutes (WORKER-CONTRACT.md:109).

## What it costs or risks

- The chat report is counts plus a path, not a #409-style fleet picture; the person must open the report file to see detail. That is narrower than #339's "taking inspiration from #409" wording (variant-5-original.md:221).
- The sweep runs at most once every 5 minutes, so "every 3 minutes" is not met; it is a cap, not a schedule (ADJ glossary line 81).
- "Until the note exists" has no date; the note waits on other work (Q5, XC-05).

## What stays unresolved

- Whether the observer text joins later, and in what format.
- The recurring loop that would print the report every few minutes is not built.
