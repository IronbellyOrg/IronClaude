# Should the sweep report mark sessions that a program started, not a person?

## Question in one sentence
May the sweep (the read-only report a coordinator session writes about its workers) label a session as "started by a program" separately from "started by a person", and if so, when and from what data?

## Why you are being asked
The label work item (SW-10) cannot start without your answer. Today, a session the issue watcher launched can appear in the report as a person's session or as "could not determine". A later step, handing approved issues from the watcher to an orchestrator (WA-07, not built), lists this label as one of its prerequisites.

## Background you need
- The issue watcher is a small program that starts a Claude session to claim an approved GitHub issue. Its first live test (FU-1) has not run yet.
- Orca is the local app that runs agent sessions. Its command `worktree ps --json` lists sessions with two text fields, `prompt` and `paneKey`. Nobody knows yet whether those fields show who started a session: on 27 live rows checked, `prompt` was empty or not a command.
- The sweep may run only commands on a list you signed. `worktree ps --json` is already on it.
- Showing a program's session as a person's is the safer mistake: person sessions are never sent messages by the coordinator.

## Your options

### 1. Yes, in Phase 2, from Orca's fields, only after the watcher's first live test (recommended)
- If you pick this: after the live test records one real row, a worker adds the label with a test; if the fields carry nothing usable, the work stops and says so. A missing signal stays "could not determine", never "person". The blind spot is written into the sweep design now.
- Upside: no new command or data source for the sweep; nothing is guessed.
- Downside: may well end with "no usable signal"; waits on the live test, which waits on your answers about the watcher (Q2 claim level, Q20 who owns its agent).

### 2. Yes, but from the watcher's own record of what it launched
- If you pick this: the sweep matches sessions against the watcher's store file `dispatch.json` (it holds the launch id and folder, with a version number), after the live test shows the match key.
- Upside: a purpose-written, versioned record; Orca changes cannot break it.
- Downside: you must approve the sweep reading another program's file; the match key may not exist; a fallback on folder name would mislabel a person's session as a program's.

### 3. Not now; write the blind spot down and decide with the handoff design
- If you pick this: no label; the docs say the sweep cannot tell; the question returns when the handoff design (SW-13, no date) is accepted.
- Upside: no work built on an unmeasured signal.
- Downside: the report can keep misleading a reader; the handoff step's prerequisite list must be edited; the question comes back later without this context.

## What the debate found
- Three advocates debated; 8 of 10 points agreed; option 1 won 6 points, option 2 won 1.
- Everyone agreed option 1's "stop if no usable signal" rule is the best failure handling, and that option 2's folder fallback errs the wrong way.
- The debate found the watcher already keeps a versioned record (`dispatch.json`), which makes option 2 the natural backup if Orca's fields prove useless.

## Recommendation and confidence
Option 1, about 78 percent. It adds nothing to what the sweep may run and refuses to guess.

## If you do not answer
The label work (SW-10) does not start. The report keeps today's behaviour, and the handoff step stays blocked on this item.

## What this answer does not authorize
It does not let the sweep run any new Orca command, read the watcher's files, or send anything to any session. Option 2's file read would need its own approval.

## How to answer
Type: "Q21: option 1" (or "Q21: option 2", "Q21: option 3").
