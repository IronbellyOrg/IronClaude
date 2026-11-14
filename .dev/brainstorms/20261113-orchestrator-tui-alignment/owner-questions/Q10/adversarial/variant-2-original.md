# Proposal B: never for the sweep, and leave its sentences alone until the consumption test settles the fact

## Answer

No: the sweep never reads Orca messages, as a standing rule; its two report sentences are not edited now, but once, after the seeded consumption test (OB-03) gives a result, so the text changes only when the fact is known.

## What happens next if the owner picks it

- The ledger records "Q10: never for the sweep, date"; `check` stays outside the sweep's allow-list (NFR-014, `probes.py:49-60`) permanently.
- SW-07's sentence change (item 3) waits for OB-03: if OB-03 shows no consumption on the seeded Run, the sentences become "This command reads no messages. Questions are read by `superclaude observe`."; if it shows consumption, the current caution stays with "measured on <date>, build <string>".
- SW-07's other items (the #409 "unmerged" sentence, the cursor wording) proceed in W3 as planned.

## What it unlocks

- One clear division of labour: the sweep reports workers and worktrees, the observer shows questions; neither program has to explain the other's behaviour.
- The sweep keeps its strongest property: it sends Orca nothing that could change a mailbox.
- Avoids an interim sentence ("not established") that has to be edited again when OB-03 lands.

## What it costs or risks

- The current text ("pending questions cannot be read without consuming them", `report.py:534-535`) stays in the shipped sweep for longer, and ADJ says it overstates what is established (X-016, unproven both ways; ADJ line 813).
- Ties a wording fix to a live test that needs the Orca app reachable and two more owner answers (Q24, Q30); if OB-03 never runs, the overstatement never gets fixed.
- "Never" rules out the sweep reading questions even if consumption is disproven, which may be the wrong call for a coordinator that only has the sweep open.
- Differs from the spec, which fixes the sentences now as part of SW-07.

## What stays unresolved

Whether the observer's read is safe (Q6, OB-03); when OB-03 runs.
