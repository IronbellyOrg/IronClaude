<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (proposal-B) -->
<!-- Merge date: 2026-11-14 -->

# Merged proposal: the sweep summary only, until the contract note exists

<!-- Source: Base (original) -->
## Answer

The static chat report is the sweep's counts-and-path reply (the read-only sweep's summary of session counts plus the path of the one report file it wrote), and nothing else, until the contract note between the observer and the sweep exists. The question of adding the observer's `observe --once` text is reopened when that note lands.

<!-- Source: Base (original, modified) - Change 1 appended -->
## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date; section 6.7 of the spec (the coordinator's status output rule) already says this (merged-requirements.md:1040), so no spec text changes.
- Nothing in code changes: the sweep skill already prints counts and path as its only exempt reply (sc-sweep-protocol/SKILL.md:31-43; pragmatic.md:22-23).
- The worker contract and the sweep skill keep not naming `superclaude observe` (V5 D2, variant-5-original.md:222).
- When the contract note (XC-05) is written, it carries a line saying whether `observe --once` text joins the chat report.
- The ledger row also says that no recurring coordinator loop exists yet, so no "every 3 to 5 minutes" cadence is claimed as met; the sweep is capped at once every 5 minutes and that cap is not a schedule (WORKER-CONTRACT.md:109; ADJ glossary line 81). (Change 1, from Variant 3)

<!-- Source: Base (original, modified) - Change 3 inserted -->
## What it unlocks

- The #409-layout static report already exists: it is the sweep's report file, whose layout was copied from #409 (docs/designs/orchestrator-mode.md:603), matching the owner's 2026-11-07 first-PR scope of "a read-only `/sc:sweep` plus the static orchestrator status report on the #409 layout" (seed-brief.md:17). The chat reply points at it. (Change 3)
- One source of truth in chat while the two programs still use different word lists.
- No edit to PR #539 (the open sweep PR), the worker contract or the output style.
- Keeps the read-only promise simple: the sweep is already allowed and capped at once every 5 minutes (WORKER-CONTRACT.md:109).

<!-- Source: Base (original) -->
## What it costs or risks

- The chat text is counts plus a path, not a #409-style fleet picture; the person must open the report file to see detail.
- "Every 3 minutes" is not met.
- "Until the note exists" has no date; the note waits on other work (Q5, XC-05).

<!-- Source: Base (original, modified) - Change 2 appended -->
## What stays unresolved

- Whether the observer text joins later, and in what format.
- The recurring loop that would print the report every few minutes is not built.
- Before observer text can ever join, someone must check that `superclaude observe --once --run <run>` run from the coordinator's own terminal shows that coordinator's Run; the observer's gate test Q-1 failed for an unbound terminal (ADJ glossary line 87) and the coordinator case is UNVERIFIED. (Change 2, from Variant 1)
