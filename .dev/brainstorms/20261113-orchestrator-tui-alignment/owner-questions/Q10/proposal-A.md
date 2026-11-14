# Proposal A: yes, later: let the sweep read pending questions once the consumption tests pass

## Answer

Yes, conditionally: once the seeded consumption test (OB-03) and the live-layout attempt (OB-04) show that `check --all --types question` does not remove messages on a coordinator Run, the owner signs one new allow-list template so the sweep can list its own Run's pending questions; until then the sweep reads none and its two sentences are corrected now.

## What happens next if the owner picks it

- Now (W3, SW-07): the two report sentences are corrected to "This command reads no messages. A plain `check` consumes them. Whether `check --all --types question` consumes on a live Run is not established." (`merged-requirements.md:196`).
- After OB-03 and OB-04 pass and the Orca build is pinned (OB-05): a new #534 follow-up row and a separate PR adds `("orchestration", "check", "--all", "--types", "question", "--run", "<run>", "--json")` as an eleventh template in `ALLOWED_ORCA` (`probes.py:49-60`), with an owner-signed allow-list note (NFR-014), tests, and a report section listing pending questions for the coordinator's own Run only.
- "Messages coverage" in the report changes from "partial" to the measured state; the pinned test (`test_report.py:590`) changes in that PR.
- If OB-03 shows consumption, this answer turns into "never" automatically and the template is not added.

## What it unlocks

- The coordinator sees its own workers' pending questions in the same report it already reads every sweep, so it does not need a second program open; the sweep runs in the coordinator's own session, which is the terminal that holds its Run and so the only one that can read them (gate test Q-1 failed, ADJ INV-024).
- Closes the "Messages coverage: partial" gap in the sweep's own output.
- Uses evidence the program is producing anyway (OB-03, OB-04, OB-05).

## What it costs or risks

- Reading on the coordinator's own live Run is exactly the case the seeded test cannot fully prove (a live Run has `--wait` listeners and an acknowledge cycle; `merged-requirements.md:1156`); a wrong pass could make the sweep remove the questions the coordinator must answer.
- A second reader of the same mailbox (the observer) plus the sweep doubles the exposure if consumption is ever found.
- Widens an owner-signed allow-list that was kept read-only toward Orca; the sweep's claim to read no messages ends.
- Duplicates the observer's question panel; ADJ keeps the two programs separate (one contract note, both programs kept, Q5).

## What stays unresolved

Whether the observer and the sweep should both read questions long-term; what the sweep does with them (it "recommends nothing", WC-16).
