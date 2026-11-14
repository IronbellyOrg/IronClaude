# Proposal A: yes, the observer may use bare `orca` because it proves the binary first

## Answer

Yes. The observer may fall back to a bare `orca` on PATH because it accepts a candidate only after `skills list --json` shows the `orca-cli` topic; the contract note records both rules and why they differ, and no code changes.

## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date.
- The contract note draft (work item XC-05, `docs/designs/observe-sweep-contract.md`) carries one binary-resolution row: observer and watcher use `_find_orca` (`orca-ide` then `orca`, each proven by `skills list --json`, `install_user_setup.py:247-270`); the sweep uses `$ORCA_CLI_COMMAND` else `orca-ide` with no probe (`probes.py:201-202`); both are accepted, with the reason for each.
- Neither program's code changes; PR #539 (the open sweep PR) is untouched.

## What it unlocks

- The contract note can state a verdict instead of two unexplained rules.
- The observer keeps working inside Orca's own terminals, where `orca` is the Orca CLI shim and `orca-ide` may or may not be present (on this host both exist, question.md fact 6).
- The guard that matters is kept: the probe rejects the GNOME screen reader, which is what a bare `orca` usually is on Linux outside Orca terminals (`install_user_setup.py` docstring).

## What it costs or risks

- The observer and the sweep can still read different Orca binaries on one host: the sweep honours `ORCA_CLI_COMMAND`, the observer ignores it (variant-5-original.md:113). A person who sets that variable to a second Orca install sees two programs disagree.
- The probe itself runs whatever is first on PATH under each name, once, with a 10-second timeout; it proves the program speaks Orca's `skills list`, not which Orca build it is (A-009 open, ADJ line 141).
- Two rules stay in the codebase, so any future third caller must pick one.

## What stays unresolved

- Whether both names resolve to the same Orca build on hosts where both exist; the note's "record the Orca build string next to each capture" rule (ADJ line 233) is the check.
