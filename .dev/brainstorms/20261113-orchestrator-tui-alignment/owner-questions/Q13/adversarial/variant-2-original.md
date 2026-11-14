# Proposal B: no; align the observer to the sweep's rule

## Answer

No. The observer should resolve Orca the way the sweep does: `$ORCA_CLI_COMMAND` when set, else `orca-ide`, never a bare `orca`, so that every read-only reader of Orca on a host reads the same binary; the existing `skills list --json` check can stay as a validation of that one choice.

## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date.
- A small observer PR (new work item, in its own Orca worktree from `origin/master`) changes the observer's binary lookup in `src/superclaude/cli/observe/adapter.py` (today it imports `_find_orca`, line 21) to honour `ORCA_CLI_COMMAND`, then `orca-ide`, and keeps the `skills list --json` probe as a check on that single candidate. Tests in `tests/observe/` change to match. Opened by a PR session with `/sc:pr-submit --monitor 3` under the owner's grant row.
- The watcher (`issue_watch/launch.py`) is left as it is, because it starts agents and is outside the observer-sweep contract; the note says so.
- The contract note records one rule for the two read-only programs.

## What it unlocks

- One answer to "which Orca did we read": observer and sweep reports from the same host can be compared without a hidden binary difference, which the planned shared capture and the dispatch-id comparison (XC-03, XC-04) depend on.
- `ORCA_CLI_COMMAND` means the same thing to both read-only programs.
- Removes the bare-name fallback that the observer's own code says usually means the GNOME screen reader on Linux (`install_user_setup.py` docstring).

## What it costs or risks

- A code and test change to a merged, working program, for a divergence never seen on a real host (INV-016: "no host with both names was shown").
- Hosts where only `orca` exists (for example inside some Orca terminals) stop working until the person sets `ORCA_CLI_COMMAND`; on this host both names exist, so it does not break here.
- One more PR in a queue already waiting on #539 and on owner grants.

## What stays unresolved

- Whether the watcher should follow later.
- Build divergence within one binary name (A-009) is not fixed by this.
