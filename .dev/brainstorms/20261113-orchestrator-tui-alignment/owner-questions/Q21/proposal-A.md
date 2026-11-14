# Proposal A: yes, but the label comes from the watcher's own record, not from Orca's agent rows

## Answer

Yes, the sweep may label machine-started sessions, but only by matching a session against the issue watcher's own record of what it launched (the claim number, the Orca operation id and the configured watcher worktree), never by guessing from the `prompt` and `paneKey` fields of Orca's `worktree ps` agent rows. A session with no matching watcher record keeps today's label.

## What happens next if the owner picks it

1. FU-1 (the watcher's first live test, work item WA-04) still runs first; its item (f) records the real path of the operation id in Orca's launch reply, and item (e) records one `worktree ps --json` agent row, so the match key is known from a real launch rather than assumed.
2. SW-10 (the label work item) is rewritten: input is the watcher's record (its `status --json` output or its state store; which one carries enough to match a session is UNVERIFIED until FU-1), joined to the session by operation id or worktree path. The `prompt` and `paneKey` fields may be shown as supporting notes but never decide the label.
3. Because the sweep would read a new input, the owner either signs a widened allow-list (NFR-014, the owner-signed list of commands the sweep may run) for `superclaude issue-watch status --json`, or names a file path the sweep may read. The contract note (XC-05) registers the watcher record as an input with its version rule.
4. SW-10 lands in Phase 2 (wave W4) as planned, opened by the PR session.

## What it unlocks

- A label that rests on a record the watcher writes on purpose, so it does not break if Orca changes what it puts in `prompt` (on 27 live rows `prompt` was empty or not a slash command: ADJ line 162).
- A cleaner input for the later handoff WA-07, whose item (3) needs the handed-off session visible as a labelled row.
- A false "machine-started" label is unlikely: it needs a positive match with a watcher record.

## What it costs or risks

- The sweep gains a dependency on a second program's output. The watcher's `status --json` has no `schema_version` (merged-requirements.md line 453), so a watcher change can silently break the label unless the note's versioning rule is applied.
- The sweep's allow-list must widen, or a new file-read path must be approved, which is an owner signature on a security-relevant list.
- The watcher records only an operation id today (merged-requirements.md line 128); whether that id can be joined to a session or transcript is unknown until FU-1 (D-A). If it cannot, this proposal falls back to worktree-path matching, which is coarse: any session a person opens in the watcher worktree would be labelled machine-started.
- More design work than the plain label.

## What stays unresolved

- Which watcher field is the join key (operation id, worktree path, or claim number): decided by FU-1's record.
- Whether the sweep should read a command's output or a file.
- D-A: whether `agent launch` creates a Run at all.
