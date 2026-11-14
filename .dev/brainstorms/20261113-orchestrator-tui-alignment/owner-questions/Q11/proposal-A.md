# Proposal A: both reports, now

## Answer

The static chat report is both: the sweep's counts-and-path reply (the read-only sweep's one-line summary of session counts plus the path of the report file it wrote) and the text that `superclaude observe --once --width 80 --ascii` prints (the built observer dashboard's one-shot plain-text view of Orca workers). The owner states this on #339 now, without waiting for the contract note between the two programs.

## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date.
- Section 6.7 of the spec (the coordinator's status output rule) is reworded to allow both texts in chat.
- When the coordinator loop is later built, its loop rule (WC-16 in WORKER-CONTRACT.md) and the sweep skill's tool list would have to name `superclaude observe --once` (today they do not; variant-5-original.md:222). The output-style exception that lets the sweep reply skip the DONE / NEXT table (pragmatic.md:22-23) covers only the sweep reply, so an observe block either keeps ordinary formatting or needs its own exception.

## What it unlocks

- The chat report looks like #409's dashboard, which is what #339 literally asks for ("taking inspiration" from #409; variant-5-original.md:221).
- `observe --once` writes no file unless `--snapshot` is passed (ADJ E-17), so it can run between sweeps without breaking the sweep's one-report-per-run rule (NFR-001), and it can fill the 3-minute end of "3 to 5 minutes" that the sweep's 5-minute cap cannot.
- No new program is needed: both commands exist.

## What it costs or risks

- The observer's gate test Q-1 failed (an unbound terminal cannot read another terminal's Run, ADJ line 87); whether the coordinator's own terminal sees its own Run through `observe --once` is UNVERIFIED.
- Two programs printing overlapping facts with different words (stale, unknown, historical) before the contract note fixes one word list (variant-5-original.md:216) can confuse the reader.
- Extra Orca calls per cycle; combined load was never measured (INV-032).
- Edits to the worker contract, the skill and the output style, none of which are scheduled.

## What stays unresolved

- The contract note (XC-05) and its shared word list.
- Whether the observer's Run binding works from a coordinator terminal.
- Whether the observer's coordinator-questions panel is on (its guard is off on master; Q6).
