# Proposal A: No. This coordinator follows the worker contract's loop only

## Answer

No. The 2026-11-05 ten-minute check does not apply to this program's coordinator; it keeps only the worker contract's coordinator loop (WC-16: re-arm the Orca wait on every expiry, and the sweep pass at most once every 5 minutes on a wake or wait timeout), and Q31 is recorded as answered "no".

## What happens next if the owner picks it

- The ledger records Q31 = no, with the date. The last row of the cadence record (section 6.6, line 1026) is marked "not in force for this program".
- The coordinator creates no recurring cron job. It reads GitHub state at wave gates, before each edit, and each PR at coordinator wakes (section 6.6, line 1025), which already exists.
- Peer sessions that are not Orca workers are watched only when the coordinator subscribes to them for a specific reason; nothing re-subscribes them on a timer.

## What it unlocks

- One clock family only: the coordinator's behaviour is fully described by a file that is checked into the repo (`WORKER-CONTRACT.md:288`), not by a memory note. A reviewer can audit the cadence from the contract alone.
- No added load: no extra `gh` calls every 10 minutes across two repos, no extra ListAgents output, no question of whether a cron fire is a "coordinator wake" that triggers a sweep pass.
- No 7-day cron expiry to manage (CronCreate jobs auto-expire after 7 days).

## What it costs or risks

- It overrides a standing owner order that exists because of a real failure: on 2026-11-05 a lapsed wait left sessions unwatched, and peer sessions "do not appear in the Orca message queue at all" (memory `coordinator-never-stop-polling.md`). A program that coordinates top-level PR sessions (Q25) and a #539 author session (Q33) has exactly those non-worker peers. If one goes quiet or finishes, nothing in WC-16 notices it.
- PR state between wakes (a new review comment, CI turning red) is only seen at the next wake or gate; on a quiet day that could be long.
- The owner may later find the program "not polling" and treat it as a breach of the earlier order.

## What stays unresolved

- Whether the 2026-11-05 order still applies to other coordinators outside this program. This answer covers this program only.
- How non-worker peers (PR sessions, the #539 author) are supervised between their own reports.
