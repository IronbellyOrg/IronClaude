# Proposal C: accept the risk with caveats, no code change

## Answer

(a) Accept the finding for this setup (the F3 option): no code change to how `git status` runs; every statement in #539's files that calls the sweep read-only or says it changes nothing gets a caveat in the same PR, and the owner records a written acceptance of the risk. (b) The acceptance names every measured channel (fsmonitor, clean and process filters, `include.path`/`includeIf`, per-worktree config, `GIT_*`/`GIT_CONFIG_*` variables) as accepted, so nothing is accepted by silence.

## What happens next if the owner picks it

1. The owner posts the ruling on the Codex security thread on PR #539 (SW-01), stating the premise it relies on: one owner, one OS user, one host; a program runs only if config on this host already names it (a clone cannot ship config, and `.gitattributes` alone ran nothing); and every launched session already runs with permission checks off (ADJ E-11), so the sweep grants no privilege a session does not already have.
2. The #539 author adds the caveat (for example "read-only toward Orca; `git status` may run programs your own git config names") at every location the grep finds: at least 16, keeping the mirror byte-equal (probe INV-011).
3. The acceptance goes into the ledger with its date and the condition that would void it (a second user, a second host, or untrusted config).
4. #539 merges after the other thread and CI clear.

## What it unlocks

- The shortest path to merging #539: no allow-list change, no new test design, no path-scope separation (INV-009, INV-039 do not apply).
- The claims in the docs become honest immediately.
- Matches the measured severity: Medium in practice on this single-owner, single-host setup (worker brief, 2026-11-13).

## What it costs or risks

- The hole stays. Anyone or anything that can write this host's git config, an included config file, or the sweep's environment can make every sweep run a program in every listed worktree, at least 18 of 29 of which share one config (ADJ line 206).
- An acceptance is reversible only before merge (SW-01 row); after merge, reversing it means a new fix PR.
- The one real-id comparison (XC-04) is forbidden to run "the unfixed sweep" (XC-04 row (4)); under this answer that lane needs either a fix later or an explicit owner exception, which the spec does not provide.
- A caveated "read-only" claim is weaker for any future reader, including the v2 knowledge layer and other programs that rely on the sweep.

## What stays unresolved

- Whether the premise still holds when the setup changes (a second host, a shared Coder workspace, the watcher starting sessions from issue text).
- How the one real-id comparison lane proceeds under the "never the unfixed sweep" rule.
