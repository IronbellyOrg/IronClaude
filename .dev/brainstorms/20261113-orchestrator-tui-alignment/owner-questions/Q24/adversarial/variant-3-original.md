# Proposal C: the 409 session runs them, read-only, from a terminal that holds no Run

## Answer

The session that owns the `issue-409-mvp` worktree (the observer's build session) runs the read-only capture (XC-03) in one sitting in wave W1, and the join comparison (XC-04) in a second sitting in wave W3 once the sweep is merged and runnable. It also runs the seeded test (OB-03) under that test's own permission row.

## What happens next if the owner picks it

1. At W0 intake (XC-10 item (1)) the coordinator confirms the 409 session exists, is reachable, and can run Orca read commands from a terminal that holds no Run. If it cannot, Q24's default is recorded and the owner is asked again.
2. Under `GRANT(XC-03,live-read)` the 409 session runs XC-03 with read commands only, no `check` and no message sent, and writes the dated capture file with the Orca build string.
3. Under `GRANT(OB-03,seeded-write)` (a separate row) it runs the seeded test from a plain terminal: `run-create` only, never `run-use`, `run-current` recorded before and after (ADJ line 459).
4. After PR #539 merges and the sweep is runnable on this host, it runs XC-04 under `GRANT(XC-04,live-read)`, with the sweep run on master code (`superclaude sweep run --run <id>`), and records the actor, revision, `--root` and report path (merged-requirements.md line 452).

## What it unlocks

- The session that knows the observer best reads the observer's ids and Orca's fields; it built the code that parses them.
- One runner for all live work tied to the observer, which keeps the record of who did what simple.
- XC-03 and OB-03 in W1; XC-04 in W3. V2-02 can then pass, and OB-06 gets its OB-03 record.

## What it costs or risks

- The 409 session's survival is UNVERIFIED today; if it has ended, this answer falls back to the default (nothing runs) until the owner names someone else.
- Its worktree is on an unmerged branch (`f104ca51a`, `origin/master` not an ancestor: merged-requirements.md line 234), so XC-04's "master code" requirement means it must run the installed CLI or switch code, and it must not disturb the unpushed commits and records that must survive until OB-01.
- ADJ's "one sitting" no longer holds: XC-04 was moved to W3, so this is two sittings.
- One session holds three permission rows, including one that writes seeded messages; the rows stay separate.

## What stays unresolved

- Whether the 409 session is alive and holds no Run, until XC-10.
