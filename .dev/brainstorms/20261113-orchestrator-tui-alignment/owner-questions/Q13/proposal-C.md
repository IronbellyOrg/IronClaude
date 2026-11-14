# Proposal C: no ruling now; the note records both rules side by side

## Answer

No verdict for now. The contract note records the observer's rule and the sweep's rule side by side, as facts, with no statement that either is accepted, and the question is asked again only if a host is ever seen where the two programs read different Orca binaries or builds.

## What happens next if the owner picks it

- The ledger records "Q13: no ruling; both rules recorded" with its date.
- The contract note draft (work item XC-05) carries the binary-resolution row exactly as the adjudicated findings already state it (ADJ line 243), plus the note's existing rule "record the Orca build string next to each capture" (ADJ line 233), and no verdict sentence.
- No code changes in either program.

## What it unlocks

- XC-05 is not held for this answer: it can be drafted with the two facts.
- The owner spends no decision on a difference that has not caused a problem on any shown host (INV-016, LOW, "no host with both names was shown").
- Keeps every option open: if the build-string records later show divergence, the owner decides with evidence.

## What it costs or risks

- The note states two rules without saying which is right, so a reader or a future third Orca caller has no guidance.
- `ORCA_CLI_COMMAND` keeps meaning different things to the two programs, unflagged as a decision.
- If divergence happens, it is found only after the fact, by comparing recorded build strings.

## What stays unresolved

- Which rule a new caller should copy.
- Whether the observer's bare-name fallback is acceptable.
